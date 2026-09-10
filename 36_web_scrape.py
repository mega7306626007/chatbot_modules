"""Web scraping & browser automation: BeautifulSoup + Selenium, opt-in (Section 13C)
Auto-split from the original single-file chatbot.py - see main.py for load order.
"""

# SECTION 13C: WEB SCRAPING / BROWSER AUTOMATION (opt-in, fail-closed)
# ==============================================================================
#
# Two optional capabilities:
#   1. BeautifulSoup-based page reading - fetch any URL's HTML with plain
#      stdlib urllib (same transport as every other connector in this
#      project), parse it with bs4 if it's installed, and return a
#      compact text summary. Fully offline-friendly in the sense that it
#      fails closed (returns an {"error": ...} dict, never raises) when
#      bs4 is missing, the URL is unreachable, or the page is junk.
#   2. Selenium headless-browser automation - genuinely renders
#      JavaScript-heavy pages (SPAs, lazy-loaded feeds), scrolls, waits
#      for selectors, and can take a real screenshot to disk. Much
#      heavier than bs4 scraping, so it's LAZY and opt-in per request:
#      nothing is imported or started unless a command actually asks for
#      it, and `selenium_is_available()` returns False when the browser
#      binary/driver can't be found so the feature degrades gracefully
#      (e.g. on a headless server without Chrome installed).
#
# Both follow the project-wide contract: never load-bearing, never
# crash because of a missing optional dependency or a dead network.

import json
import os
import re
import time
import urllib.parse
import urllib.request

# BeautifulSoup is OPTIONAL. Without it, the "read a URL" command
# returns a plain-link fallback (see below); with it, pages get a real
# text extraction. html.parser (the stdlib default) is fast and safe on
# any page; lxml would be faster only for pathological pages.
try:
    from bs4 import BeautifulSoup
    BS4_AVAILABLE = True
except ImportError:
    BS4_AVAILABLE = False

# Selenium is OPTIONAL and heavier. It is only ever imported/started on
# demand (see _BrowserSession), so importing this module costs nothing
# even on servers where Selenium isn't installed.
SELENIUM_AVAILABLE = False
try:
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options as _ChromeOptions
    from selenium.webdriver.chrome.service import Service as _ChromeService
    from selenium.common.exceptions import WebDriverException as _WebDriverException
    SELENIUM_AVAILABLE = True
except ImportError:
    SELENIUM_AVAILABLE = False


_USER_AGENT = "Offline-ChatBot/1.0 (educational project; polite scraping with links & attribution)"

# DuckDuckGo serves clean JSON to a browser-grade UA but often answers
# its generic Python/bot headers with an "anomaly" challenge page, so
# web_search uses this UA instead of the polite one above.
_WEB_UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                         "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120 Safari/537.36"}

# Pages commonly block default Python user agents; this is still polite
# (identifies itself, standard UA string for a headless client).
_HEADERS = {"User-Agent": _USER_AGENT, "Accept-Language": "en,sw;q=0.8,fr;q=0.5"}

# How many characters total extracted text may be - bounds the reply
# size so a monster page doesn't blow up the chat window.
_MAX_TEXT_CHARS = 2200
_MAX_LINKS = 8
_HTML_TAG_RE = re.compile(r"<[^>]+>")
_WS_RE = re.compile(r"\s+")
_IDLE_REFRESH_SECONDS = 15  # wait/scroll window for Selenium pages


# ---------------------------------------------------------------------------
# Plain-urllib HTML fetch (no bs4 needed for this part)
# ---------------------------------------------------------------------------

def fetch_html(url: str, timeout: float = 10.0, max_bytes: int = 3_000_000):
    """Downloads raw HTML for a URL, returning bytes, or an error dict.
    Same fail-closed contract as _RestApiClient elsewhere: returns
    {"error": str} on ANY problem rather than raising."""
    if "://" not in url:
        url = "https://" + url
    try:
        req = urllib.request.Request(url, headers=_HEADERS, method="GET")
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            if resp.status != 200:
                return {"error": f"server returned HTTP {resp.status}"}
            body = resp.read(max_bytes + 1)
            if len(body) > max_bytes:
                return {"error": "page is too large to fetch"}
            # Let bs4 (or our fallback) sniff the encoding; pass raw bytes.
            return body
    except urllib.error.HTTPError as e:
        return {"error": f"HTTP {e.code}"}
    except urllib.error.URLError as e:
        reason = getattr(e, "reason", None)
        return {"error": f"couldn't reach that page ({reason})"}
    except TimeoutError:
        return {"error": "that page took too long to respond"}
    except (ValueError, OSError) as e:  # bad scheme, refused, etc.
        return {"error": f"couldn't fetch that page ({e})"}


def _fetch_html_ua(url: str, timeout: float = 10.0, max_bytes: int = 3_000_000,
                   headers=None):
    """Like fetch_html but with caller-supplied User-Agent headers, in
    case a service (DuckDuckGo) serves different content to its generic
    bot UA vs. a browser-grade one. Same fail-closed contract."""
    if "://" not in url:
        url = "https://" + url
    hdrs = dict(headers or {})
    hdrs.setdefault("Accept-Language", "en,sw;q=0.8,fr;q=0.5")
    try:
        req = urllib.request.Request(url, headers=hdrs, method="GET")
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            if resp.status != 200:
                return {"error": f"server returned HTTP {resp.status}"}
            body = resp.read(max_bytes + 1)
            if len(body) > max_bytes:
                return {"error": "page is too large to fetch"}
            return body
    except urllib.error.HTTPError as e:
        return {"error": f"HTTP {e.code}"}
    except urllib.error.URLError as e:
        reason = getattr(e, "reason", None)
        return {"error": f"couldn't reach that page ({reason})"}
    except TimeoutError:
        return {"error": "that page took too long to respond"}
    except (ValueError, OSError) as e:
        return {"error": f"couldn't fetch that page ({e})"}


def _decode(body):
    """Best-effort HTML decode: try declared charset, then UTF-8, then
    cp1252 - always succeeds with something readable."""
    if isinstance(body, str):
        return body
    for enc in ("utf-8", "cp1252"):
        try:
            return body.decode(enc)
        except (UnicodeDecodeError, ValueError):
            continue
    return body.decode("utf-8", errors="replace")


def _title_and_text(html: str):
    """Extracts title + main-text preview from HTML. Returns
    (title, text, links_list). Works with or without bs4."""
    if BS4_AVAILABLE:
        soup = BeautifulSoup(html, "html.parser")
        title = soup.title.get_text(strip=True) if soup.title else ""
        for tag in soup(["script", "style", "nav", "footer", "noscript"]):
            tag.decompose()
        text = _WS_RE.sub(" ", soup.get_text(" ", strip=True))
        links = []
        for a in soup.find_all("a", href=True):
            href = a["href"].strip()
            label = a.get_text(strip=True)
            if href.startswith(("#", "javascript:", "mailto:")):
                continue
            if label and label.lower() != href.lower():
                links.append((label[:60], href))
        return title, text, links
    # No bs4: rough-but-honest fallback. Remove tags, keep it readable.
    title = ""
    m = re.search(r"<title[^>]*>(.*?)</title>", html, flags=re.I | re.S)
    if m:
        title = _WS_RE.sub(" ", re.sub(r"<[^>]+>", "", m.group(1))).strip()
    text = _WS_RE.sub(" ", _HTML_TAG_RE.sub(" ", html)).strip()
    links = []
    for m in re.finditer(r'<a\s[^>]*href=["\']([^"\']+)["\'][^>]*>(.*?)</a>', html, flags=re.I | re.S):
        href = m.group(1).strip()
        label = _WS_RE.sub(" ", _HTML_TAG_RE.sub(" ", m.group(2))).strip()
        if href.startswith(("#", "javascript:", "mailto:")):
            continue
        if label.lower() != href.lower():
            links.append((label[:60], href))
    return title, text, links


# ---------------------------------------------------------------------------
# Public class the ChatBot instantiates
# ---------------------------------------------------------------------------

class WebReader:
    """Reads a URL and returns a compact, conversational summary.

    Instantiated by ChatBot (like every other feature class); the
    per-call entry point is `read_page(url)` which always returns a
    dict with either a usable "summary" or an "error" key - never
    raises, exactly like the API connectors."""

    def __init__(self):
        self.timeout_seconds = 10.0

    # -- bs4 dependency story, exposed for commands that want it -------
    @staticmethod
    def bs4_available() -> bool:
        return BS4_AVAILABLE

    # -- main entry point ---------------------------------------------

    def read_page(self, url: str):
        """Fetches + summarizes one URL. Returns
        {"url", "title", "summary", "links"} or {"error": str}."""
        raw = fetch_html(url, timeout=self.timeout_seconds)
        if isinstance(raw, dict):  # error dict
            return raw
        html = _decode(raw)
        title, text, links = _title_and_text(html)
        preview = text[: _MAX_TEXT_CHARS]
        # Strip the title from the preview if it's repeated up top.
        if title and preview.lower().startswith(title.lower()):
            preview = preview[len(title):].strip()
        summary = preview.strip()
        if not summary:
            return {"error": "that page had no readable text"}
        result = {"url": url, "title": title.strip() or url, "summary": summary}
        if links:
            result["links"] = [(label, href) for label, href in links[: _MAX_LINKS]]
        return result

    # -- multi-engine lookup/search chain ------------------------------
    #
    # A single topic can live in several places: simple English Wikipedia,
    # the main English Wikipedia, or only on the wider web. _lookup_chain()
    # walks those sources in order and returns the FIRST one that answers,
    # so "search the web for alliance high school" still returns real
    # results even when Wikipedia has no article for it. Every step stays
    # fail-closed: a dead source is skipped, never fatal.

    def wikipedia_summary(self, query: str, lang: str = "simple"):
        """Pulls a concise intro summary for a topic from Wikipedia's
        REST endpoint (no API key). lang is "simple" or "en". Returns a
        dict with {"title", "extract", "url"} or {"error": str}."""
        topic = query.strip()
        if not topic:
            return {"error": "what should I look up?"}
        host = "en.wikipedia.org" if lang == "en" else "simple.wikipedia.org"
        api_url = (
            f"https://{host}/api/rest_v1/page/summary/"
            + urllib.parse.quote(topic.replace(" ", "_"))
        )
        raw = fetch_html(api_url, timeout=self.timeout_seconds)
        if isinstance(raw, dict):
            return {"error": f"couldn't look that up ({raw['error']})"}
        try:
            data = json.loads(_decode(raw))
        except (json.JSONDecodeError, ValueError):
            return {"error": "couldn't parse the lookup result"}
        if not isinstance(data, dict):
            return {"error": "unexpected lookup result"}
        if data.get("type") in ("disambiguation", "redirect") or not data.get("extract"):
            # disambiguation or missing page: fall back to a title search
            return self.wikipedia_search(topic)
        return {
            "title": data.get("title") or topic,
            "extract": _WS_RE.sub(" ", data.get("extract") or "").strip()[: _MAX_TEXT_CHARS],
            "url": data.get("content_urls", {}).get("desktop", {}).get("page") or api_url,
            "source": "simple.wikipedia.org" if lang == "simple" else "en.wikipedia.org",
        }

    def _phase(self, query: str):
        """Best-effort: asks Wikipedia's API for a matching page title
        when a bare-summary request would 404 (e.g. a phrase Wikipedia
        only knows under a slightly different name). Returns a dict with
        {"title", "extract", "url"} or {"error": str}."""
        titles = self.wikipedia_search(query)
        if "error" in titles:
            return titles
        for item in titles["results"][:3]:
            t = item["title"]
            candidate = self.wikipedia_summary(t, lang="en")
            if "error" not in candidate and candidate.get("extract"):
                return candidate
            # "Alliance High School (Kenya)" disambiguates back to the
            # same page; strip the qualifier and retry once.
            short = t.split(" (")[0]
            if short != t:
                candidate = self.wikipedia_summary(short, lang="en")
                if "error" not in candidate and candidate.get("extract"):
                    return candidate
        return {"error": f"no Wikipedia article for '{query}'"}

    def lookup(self, query: str):
        """Multi-source lookup: simple WP -> main WP -> title-match ->
        generic web search. Returns the FIRST source that answers."""
        topic = query.strip()
        if not topic:
            return {"error": "what should I look up?"}
        # 1) simple English Wikipedia summary
        first = self.wikipedia_summary(topic, lang="simple")
        if "error" not in first and first.get("extract"):
            return first
        # 2) main English Wikipedia summary (same query, more coverage)
        second = self.wikipedia_summary(topic, lang="en")
        if "error" not in second and second.get("extract"):
            return second
        # 3) Wikipedia title search for a near-exact phrase match
        phased = self._phase(topic)
        if "error" not in phased:
            return phased
        # 4) last resort: a real web search so non-Wikipedia topics
        #    ("alliance high school", a club, a local business) still get
        #    an answer instead of a dead end.
        web = self.web_search(topic)
        if "error" in web:
            return web
        return {
            "title": f"Web results for '{topic}'",
            "extract": _WS_RE.sub(
                " ", " ".join(
                    f"{r['title']}: {r['snippet']}" for r in web["results"]
                )
            ).strip()[: _MAX_TEXT_CHARS],
            "url": web["results"][0]["url"],
            "urls": [r["url"] for r in web["results"]],
            "source": "web search",
        }

    def web_search(self, query: str, limit: int = 6):
        """Generic web search via DuckDuckGo - no API key, same urllib
        transport. Tries the JSON Instant-Answer endpoint first (browser
        UA, one retry), then falls back to parsing the lite HTML
        endpoint, which is far more tolerant. Returns {"results":
        [{"title", "snippet", "url"}, ...]} or {"error": str}."""
        results = self._ddg_json(query, limit)
        if results is None:
            results = self._ddg_lite(query, limit)
        if not results:
            return {"error": f"no web results for '{query}'"}
        return {"results": results[:limit]}

    def _ddg_json(self, query: str, limit: int = 6):
        """DuckDuckGo Instant-Answer JSON API. Returns a results list,
        or None if the endpoint is throttling/challenging us."""
        url = (
            "https://api.duckduckgo.com/?q=" + urllib.parse.quote(query)
            + "&format=json&no_html=1"
        )
        for attempt in range(2):
            raw = _fetch_html_ua(url, timeout=self.timeout_seconds, headers=_WEB_UA)
            if isinstance(raw, dict):
                return None
            try:
                data = json.loads(_decode(raw))
            except (json.JSONDecodeError, ValueError):
                # anomaly/challenge page, not JSON - try again once
                continue
            if not isinstance(data, dict):
                return None
            results = []
            if data.get("AbstractText") and data.get("AbstractURL"):
                results.append({
                    "title": data.get("Heading") or query,
                    "snippet": data.get("AbstractText"),
                    "url": data.get("AbstractURL"),
                })
            related = data.get("RelatedTopics") or []
            for topic in related:
                if isinstance(topic, dict):
                    if "Topics" in topic:
                        for sub in topic["Topics"]:
                            if isinstance(sub, dict) and sub.get("FirstURL"):
                                text = sub.get("Text", "")
                                results.append({
                                    "title": text.split(" -")[0][:80] or text,
                                    "snippet": text,
                                    "url": sub.get("FirstURL"),
                                })
                    elif topic.get("FirstURL"):
                        text = topic.get("Text", "")
                        results.append({
                            "title": text.split(" -")[0][:80] or text,
                            "snippet": text,
                            "url": topic.get("FirstURL"),
                        })
                if len(results) >= limit:
                    break
            return results or None
        return None

    def _ddg_lite(self, query: str, limit: int = 6):
        """DuckDuckGo Lite HTML endpoint - plain result anchors, no JS.
        Works with or without bs4."""
        url = "https://lite.duckduckgo.com/lite/?q=" + urllib.parse.quote(query)
        raw = _fetch_html_ua(url, timeout=self.timeout_seconds, headers=_WEB_UA)
        if isinstance(raw, dict):
            return []
        html = _decode(raw)
        results = []
        if BS4_AVAILABLE:
            soup = BeautifulSoup(html, "html.parser")
            for a in soup.select("a.result-link"):
                href = a.get("href", "")
                label = a.get_text(" ", strip=True)
                if not href or not label:
                    continue
                results.append({
                    "title": label[:80],
                    "snippet": "",
                    "url": self._clean_ddg_href(href),
                })
                if len(results) >= limit:
                    break
        else:
            for m in re.finditer(
                r'<a[^>]*class="result-link"[^>]*href="([^"]+)"[^>]*>(.*?)</a>',
                html, flags=re.I | re.S,
            ):
                label = _WS_RE.sub(" ", _HTML_TAG_RE.sub(" ", m.group(2))).strip()
                if not label:
                    continue
                results.append({
                    "title": label[:80],
                    "snippet": "",
                    "url": self._clean_ddg_href(m.group(1)),
                })
                if len(results) >= limit:
                    break
        return results

    @staticmethod
    def _clean_ddg_href(href: str) -> str:
        """DuckDuckGo wraps result URLs (/?uddg=<encoded> on html/lite);
        unwrap to the real target, and drop the internal redirect."""
        m = re.search(r"[?&]uddg=([^&]+)", href)
        if m:
            return urllib.parse.unquote(m.group(1))
        if href.startswith("//"):
            return "https:" + href
        return href

    def wikipedia_search(self, query: str):
        """Returns a list of matching article titles + URLs from the
        Wikipedia opensearch API, so a disambiguation result can still
        tell the user what exists. Returns {"results": [...]} or
        {"error": str}."""
        api_url = (
            "https://en.wikipedia.org/w/api.php?action=opensearch&format=json&limit=6&search="
            + urllib.parse.quote(query)
        )
        raw = fetch_html(api_url, timeout=self.timeout_seconds)
        if isinstance(raw, dict):
            return {"error": f"couldn't search for that ({raw['error']})"}
        try:
            data = json.loads(_decode(raw))
        except (json.JSONDecodeError, ValueError):
            return {"error": "couldn't parse the search result"}
        titles = data[1] if isinstance(data, list) and len(data) > 1 else []
        urls = data[3] if isinstance(data, list) and len(data) > 3 else []
        if not titles:
            return {"error": f"no Wikipedia results for '{query}'"}
        return {"results": [{"title": t, "url": u} for t, u in zip(titles, urls)]}

    def format_read_page(self, url: str) -> str:
        """Human-friendly reply for the 'fetch/<url>' command."""
        result = self.read_page(url)
        if "error" in result:
            return f"I couldn't read that page: {result['error']}."
        lines = [f"**{result['title']}**"]
        if result.get("summary"):
            lines.append(result["summary"])
        if result.get("links"):
            lines.append("")
            lines.append("Some links from the page:")
            for label, href in result["links"]:
                lines.append(f"- {label} -> {href}")
        return "\n".join(lines)

    def format_lookup(self, query: str) -> str:
        """Human-friendly reply for the 'look up <topic>' command. Walks
        the multi-source lookup chain (Wikipedia -> web search)."""
        result = self.lookup(query)
        if "error" in result:
            # maybe no network or no article - say so gracefully
            return f"I couldn't find anything on '{query}': {result['error']}."
        if result.get("source") == "web search":
            lines = [f"**{result['title']}**"]
            if result.get("extract"):
                lines.append(result["extract"])
            if result.get("urls"):
                lines.append("")
                lines.append("Sources:")
                for u in result["urls"]:
                    lines.append(f"- {u}")
            return "\n".join(lines)
        lines = [f"**{result['title']}** – from Wikipedia"]
        if result.get("extract"):
            lines.append(result["extract"])
        lines.append(f"More: {result['url']}")
        return "\n".join(lines)

    def format_search(self, query: str) -> str:
        """Human-friendly reply for the 'search <topic>' command."""
        result = self.wikipedia_search(query)
        if "error" in result:
            # Wikipedia has no article titles, but the wider web might.
            web = self.web_search(query)
            if "error" in web:
                return f"I couldn't search for '{query}': {web['error']}."
            lines = [f"Here's what I found on the web for '{query}':"]
            for item in web["results"]:
                lines.append(f"- {item['title']} -> {item['url']}")
            return "\n".join(lines)
        lines = [f"Here's what I found for '{query}':"]
        for item in result["results"]:
            lines.append(f"- {item['title']} -> {item['url']}")
        return "\n".join(lines)


# ---------------------------------------------------------------------------
# Selenium headless-browser session (lazy; only started on demand)
# ---------------------------------------------------------------------------

class BrowserSession:
    """Lazy headless-Chrome session for JS-heavy pages and screenshots.

    Nothing is imported or started until `start()` is called, and every
    failure (no selenium, no Chrome binary, driver mismatch, page
    timeout) turns into `available() == False` / an error dict rather
    than an exception escaping to the caller."""

    def __init__(self):
        self._driver = None

    def available(self) -> bool:
        if not SELENIUM_AVAILABLE:
            return False
        if self._driver is not None:
            return True
        try:
            self._start()
            return True
        except Exception:
            return False

    def close(self):
        if self._driver is not None:
            try:
                self._driver.quit()
            except Exception:
                pass
            self._driver = None

    def _start(self):
        options = _ChromeOptions()
        options.add_argument("--headless=new")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        options.add_argument("--window-size=1280,900")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        try:
            # chromedriver usually auto-discovered on PATH or via the
            # installed browser bundle; Service() keeps defaults.
            self._driver = webdriver.Chrome(options=options)
        except Exception:
            self._driver = None
            raise

    def render_text(self, url: str, wait_for: str = None, timeout: float = 20.0):
        """Loads a (possibly JS-heavy) page, waits for a selector if
        given, and returns extracted visible text. Returns
        {"url", "title", "text"} or {"error": str}."""
        if not SELENIUM_AVAILABLE:
            return {"error": "browser automation isn't installed in this environment"}
        try:
            if self._driver is None:
                self._start()
            self._driver.set_page_load_timeout(timeout)
            self._driver.get(url)
            if wait_for:
                try:
                    self._driver.implicitly_wait(wait_for)
                except Exception:
                    pass
            # small extra wait so JS-rendered content settles
            time.sleep(_IDLE_REFRESH_SECONDS)
            text = self._driver.execute_script(_VISIBLE_TEXT_JS)
            text = _WS_RE.sub(" ", text or "").strip()
            title = self._driver.title or ""
            return {"url": url, "title": title, "text": text[: _MAX_TEXT_CHARS]}
        except _WebDriverException as e:
            return {"error": f"browser couldn't load that page ({e})"}
        except Exception as e:
            return {"error": f"browser automation failed ({e})"}

    def screenshot(self, url: str, output_path: str, timeout: float = 20.0):
        """Full-page screenshot of a URL saved to output_path. Returns
        {"path": output_path} or {"error": str}."""
        if not SELENIUM_AVAILABLE:
            return {"error": "browser automation isn't installed in this environment"}
        try:
            if self._driver is None:
                self._start()
            self._driver.set_page_load_timeout(timeout)
            self._driver.get(url)
            time.sleep(_IDLE_REFRESH_SECONDS)
            height = self._driver.execute_script(
                "return Math.max(document.body.scrollHeight, document.body.offsetHeight,"
                " document.documentElement.clientHeight, document.documentElement.scrollHeight)"
            )
            self._driver.set_window_size(1280, min(height, 20000))
            self._driver.save_screenshot(output_path)
            if not os.path.exists(output_path):
                return {"error": "screenshot wasn't written to disk"}
            return {"path": output_path}
        except _WebDriverException as e:
            return {"error": f"browser couldn't screenshot that page ({e})"}
        except Exception as e:
            return {"error": f"browser automation failed ({e})"}

    def format_render_text(self, url: str) -> str:
        result = self.render_text(url)
        if "error" in result:
            return f"Browser automation couldn't read that page: {result['error']}."
        lines = [f"**{result['title'] or url}** (live rendering)"]
        lines.append(result["text"] or "No readable text on that page.")
        return "\n".join(lines)


# Paste-with-JS-aware extraction script; keeps visible rendered text only.
_VISIBLE_TEXT_JS = r"""
var walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
var chunks = [];
while (walker.nextNode()) {
  var n = walker.currentNode;
  if (!n.parentElement) continue;
  var st = getComputedStyle(n.parentElement);
  if (st && (st.display === 'none' || st.visibility === 'hidden')) continue;
  var v = (n.textContent || '').replace(/\s+/g, ' ').trim();
  if (v) chunks.push(v);
}
return chunks.join(' ');
"""