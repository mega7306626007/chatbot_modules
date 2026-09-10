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

    def wikipedia_summary(self, query: str):
        """Pulls a concise intro summary for a topic from Wikipedia's
        simple REST endpoint (no API key). Returns a dict with
        {"title", "extract", "url"} or {"error": str}."""
        topic = query.strip()
        if not topic:
            return {"error": "what should I look up?"}
        api_url = (
            "https://simple.wikipedia.org/api/rest_v1/page/summary/"
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
        if data.get("type") in ("disambiguation", "redirect") or data.get("extract") is None:
            # disambiguation page: fall back to a plain search over titles
            return self.wikipedia_search(topic)
        return {
            "title": data.get("title") or topic,
            "extract": _WS_RE.sub(" ", data.get("extract") or "").strip()[: _MAX_TEXT_CHARS],
            "url": data.get("content_urls", {}).get("desktop", {}).get("page") or api_url,
        }

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
        """Human-friendly reply for the 'look up <topic>' command."""
        result = self.wikipedia_summary(query)
        if "error" in result:
            # maybe no network or no article - say so gracefully
            return f"I couldn't find anything on '{query}': {result['error']}."
        lines = [f"**{result['title']}** – from Wikipedia"]
        if result.get("extract"):
            lines.append(result["extract"])
        lines.append(f"More: {result['url']}")
        return "\n".join(lines)

    def format_search(self, query: str) -> str:
        """Human-friendly reply for the 'search <topic>' command."""
        result = self.wikipedia_search(query)
        if "error" in result:
            return f"I couldn't search for '{query}': {result['error']}."
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