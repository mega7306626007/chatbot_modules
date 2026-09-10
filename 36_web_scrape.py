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
# Stopwords used by the title-phrase relevance gate (EN, SW, FR).
_STOPWORDS = {
    "the", "a", "an", "of", "and", "or", "for", "in", "on", "at", "to",
    "from", "with", "by", "is", "are", "was", "were", "it", "its", "this",
    "that", "these", "those", "as", "be", "been", "being", "have", "has",
    "had", "do", "does", "did", "but", "not", "no", "can", "could", "will",
    "would", "should", "about", "over", "under", "between", "into", "out",
    "up", "down", "off", "him", "her", "his", "their", "they", "them", "you",
    "your", "my", "we", "our", "us", "i", "me", "he", "she",
    "kwa", "na", "ya", "za", "wa", "ni", "si", "tu", "la", "li", "lo", "ku",
    "katika", "kutoka", "juu", "chini", "hii", "hizo", "hapa", "kwenye",
    "le", "la", "de", "du", "des", "un", "une", "et", "ou", "pour", "sur",
    "dans", "avec", "par", "est", "sont", "ce", "cette", "ces", "les", "au",
}
_IDLE_REFRESH_SECONDS = 15  # wait/scroll window for Selenium pages

# Search engines sometimes hand back URLs of their own landing pages
# ("duckduckgo.com/N'Golo_Kanté" etc.), which are nav junk and never a
# real source; deep-read skips them.
_DOGFOOD_HOSTS = {
    "duckduckgo.com", "www.duckduckgo.com", "duck.co", "lite.duckduckgo.com",
    "www.bing.com", "bing.com",
    "youtube.com", "www.youtube.com", "m.youtube.com", "youtu.be",
    "facebook.com", "www.facebook.com", "twitter.com", "x.com",
    "instagram.com", "www.instagram.com", "tiktok.com", "www.tiktok.com",
    "mymemory.translated.net", "translate.google.com", "translate.yandex.com",
    "wordhippo.com", "www.wordhippo.com",
}

# Distinctive Swahili / French clue words used by _guess_phrase_lang.
_SW_CLUES = {
    "kwa", "heri", "jina", "maana", "nini", "wapi", "lini", "nani", "hii",
    "hizo", "katika", "kutoka", "juu", "chini", "kwaheri", "asante", "sema",
    "kusema", "safari", "mzee", "mwalimu", "mwanafunzi", "shule", "nyumba",
    "chakula", "maji", "bahari", "mlima", "nchi", "mjini", "dunia",
    "chakula", "habari", "sasa", "bado", "lakini", "ndiyo", "hapana",
    "rafiki", "familia", "mama", "baba", "watoto", "kaka", "dada",
}
_FR_CLUES = {
    "le", "la", "les", "des", "un", "une", "du", "de", "et", "ou", "pour",
    "sur", "dans", "avec", "par", "est", "sont", "a", "au", "aux", "ce",
    "cette", "ces", "il", "elle", "nous", "vous", "ils", "elles", "pas",
    "quoi", "comment", "pourquoi", "ou", "qui", "que", "bonjour", "merci",
}

# Hand-verified common phrases (lowercased query -> English translation)
# so the trilingual bot answers everyday Swahili/French idioms correctly
# instead of falling back to web-search noise.
_TRANSLATIONS = {
    "kwa heri": ("goodbye",),
    "kwaheri": ("goodbye",),
    "asante": ("thank you",),
    "asante sana": ("thank you very much",),
    "habari": ("news / hello",),
    "habari yako": ("how are you?",),
    "habari za asubuhi": ("good morning",),
    "habari za jioni": ("good evening",),
    "mambo": ("what's up",),
    "poa": ("cool",),
    "karibu": ("welcome",),
    "karibu sana": ("you're welcome",),
    "ndiyo": ("yes",),
    "hapana": ("no",),
    "sijui": ("i don't know",),
    "ninafurahi kukusikia": ("nice to meet you",),
    "usiku mwema": ("good night",),
    "lala salama": ("sleep well",),
    "jina lako ni nani": ("what is your name?",),
    "nakupenda": ("i love you",),
    "nimekuelewa": ("i understand you",),
    "sielewi": ("i don't understand",),
    "tafadhali": ("please",),
    "samahani": ("sorry / excuse me",),
    "naweza kusaidiaje": ("how can i help",),
    "bonjour": ("hello",),
    "bonsoir": ("good evening",),
    "bonne nuit": ("good night",),
    "merci": ("thank you",),
    "merci beaucoup": ("thank you very much",),
    "s'il vous plait": ("please",),
    "au revoir": ("goodbye",),
    "comment ca va": ("how are you",),
    "comment-allez-vous": ("how are you",),
    "je vous en prie": ("you're welcome",),
    "de rien": ("you're welcome",),
    "pardon": ("excuse me",),
    "excusez-moi": ("excuse me",),
    "bienvenue": ("welcome",),
}


def _guess_phrase_lang(phrase: str):
    """Best-effort guess whether a phrase is Swahili or French, based
    on distinctive clue words. Returns "sw", "fr", or None."""
    words = set(re.split(r"\W+", phrase.lower()))
    if words & _SW_CLUES:
        return "sw"
    if words & _FR_CLUES:
        return "fr"
    return None


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
        # Wikipedia-family pages bury the real content under navigation
        # junk; drop the classic culprits (sidebars, jump links, footer,
        # category lists, edit links) before extracting text.
        for sel in ("#mw-navigation", "#mw-panel", ".vector-menu", "[role='navigation']",
                    ".mw-jump-link", ".mw-portlet", "#catlinks", ".printfooter",
                    ".noprint", ".sidebar", ".mw-editsection", ".mw-references-wrap",
                    "#siteSub", ".mw-empty-elt", "#p-lang", ".vector-user-links",
                    "#left-navigation", "#right-navigation", ".mw-body-header"):
            for node in soup.select(sel):
                node.decompose()
        text = _WS_RE.sub(" ", soup.get_text(" ", strip=True))
        # Drop short boilerplate lines the page chrome leaves behind.
        _BOILERPLATE = re.compile(
            r"^(jump to content|search|edit links|from wikipedia, the free "
            r"encyclopedia|hidden categories|page information|permalink|"
            r"cite this page)$", re.IGNORECASE)
        text = "\n".join(
            ln for ln in re.split(r"(?<=[.!?;:])\s+", text)
            if ln and not _BOILERPLATE.match(ln.strip()) and len(ln.strip()) > 1
        )
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
        self.timeout_seconds = 8.0

    # -- bs4 dependency story, exposed for commands that want it -------
    @staticmethod
    def bs4_available() -> bool:
        return BS4_AVAILABLE

    @staticmethod
    def _is_wiki_url(url: str) -> bool:
        """True if the URL is a Wikipedia-family article page."""
        return bool(re.match(r"https?://[a-z]{2,3}\.wikipedia\.org/wiki/.+", url))

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

    # -- multi-engine, multi-language lookup/search chain ------------
    #
    # A single topic can live in many places: simple English Wikipedia,
    # the main English Wikipedia, the Swahili or French Wikipedia,
    # Wiktionary (words), Wikiquote (people), or only on the wider web.
    # lookup() walks those sources in order and returns the FIRST one
    # that answers - and the web step still reads the top result's real
    # content, not just its title, so "alliance high school" or a local
    # club gets a genuinely deep answer instead of a dead end. Every
    # step stays fail-closed: a dead source is skipped, never fatal.

    _WIKI_HOSTS = {
        "simple": "https://simple.wikipedia.org",
        "en": "https://en.wikipedia.org",
        "sw": "https://sw.wikipedia.org",
        "fr": "https://fr.wikipedia.org",
    }
    _WIKI_LANGS = ("simple", "en", "sw", "fr")
    _WIKIQUOTE_HOST = "https://en.wikiquote.org"
    _WIKTIONARY_HOST = "https://en.wiktionary.org"

    def _wiki_api(self, lang: str, params: dict):
        """Calls a Wikipedia-family action API (en/sw/fr/simple, or
        "quotes" for Wikiquote) with browser-grade UA. Returns a JSON
        dict or an error dict."""
        if lang == "quotes":
            host = self._WIKIQUOTE_HOST
        elif lang == "wiktionary":
            host = self._WIKTIONARY_HOST
        else:
            host = self._WIKI_HOSTS.get(lang, self._WIKI_HOSTS["en"])
        params = dict(params)
        params.setdefault("format", "json")
        params.setdefault("formatversion", "2")
        url = host + "/w/api.php?" + urllib.parse.urlencode(params)
        raw = _fetch_html_ua(url, timeout=self.timeout_seconds, headers=_WEB_UA)
        if isinstance(raw, dict):
            return {"error": raw["error"]}
        try:
            data = json.loads(_decode(raw))
        except (json.JSONDecodeError, ValueError):
            return {"error": "couldn't parse the result"}
        return data if isinstance(data, dict) else {"error": "unexpected result"}

    def wikipedia_summary(self, query: str, lang: str = "simple"):
        """Concise intro summary from Wikipedia's REST endpoint (no API
        key). lang is one of "simple", "en", "sw", "fr". Returns
        {"title", "extract", "url", "source"} or {"error": str}."""
        topic = query.strip()
        if not topic:
            return {"error": "what should I look up?"}
        host = self._WIKI_HOSTS.get(lang, self._WIKI_HOSTS["en"])
        api_url = (
            host + "/api/rest_v1/page/summary/"
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
            # disambiguation or missing page: let the caller move on
            return {"error": f"no article on {lang}.wikipedia for '{topic}'"}
        return {
            "title": data.get("title") or topic,
            "extract": _WS_RE.sub(" ", data.get("extract") or "").strip()[: _MAX_TEXT_CHARS],
            "url": data.get("content_urls", {}).get("desktop", {}).get("page") or api_url,
            "source": f"{lang}.wikipedia.org",
        }

    def wikipedia_extract(self, query: str, lang: str = "en", max_chars: int = 2500):
        """DEEPER Wikipedia lookup than the REST summary: uses the
        action=query prop=extracts endpoint to pull the full article
        plaintext (capped for chat). Returns {"title", "extract", "url",
        "source"} or {"error": str}."""
        topic = query.strip()
        if not topic:
            return {"error": "what should I look up?"}
        data = self._wiki_api(lang, {
            "action": "query", "prop": "extracts", "explaintext": "1",
            "redirects": "1", "titles": topic,
        })
        if "error" in data:
            return data
        pages = data.get("query", {}).get("pages") or []
        page = pages[0] if pages else {}
        extract = page.get("extract") if isinstance(page, dict) else ""
        if not extract:
            return {"error": f"no deep Wikipedia article for '{topic}'"}
        host = self._WIKI_HOSTS.get(lang, self._WIKI_HOSTS["en"])
        title = page.get("title") or topic
        return {
            "title": title,
            "extract": _WS_RE.sub(" ", extract).strip()[:max_chars],
            "url": host + "/wiki/" + urllib.parse.quote(title.replace(" ", "_")),
            "source": f"{lang}.wikipedia.org (full extract)",
        }

    def wiktionary_define(self, word: str):
        """Dictionary definition from Wiktionary (part of the Wikimedia
        family, no API key). Returns {"title", "extract", "url",
        "source"} or {"error": str} - intended for single words."""
        word = word.strip().lower()
        if not word:
            return {"error": "what word should I define?"}
        data = self._wiki_api("wiktionary", {
            "action": "query", "prop": "extracts", "explaintext": "1",
            "exintro": "1", "titles": word,
        })
        if "error" in data:
            return data
        pages = data.get("query", {}).get("pages") or []
        page = pages[0] if pages else {}
        extract = page.get("extract") if isinstance(page, dict) else ""
        if not extract:
            return {"error": f"Wiktionary has no entry for '{word}'"}
        return {
            "title": page.get("title") or word,
            "extract": _WS_RE.sub(" ", extract).strip()[: _MAX_TEXT_CHARS],
            "url": "https://en.wiktionary.org/wiki/" + urllib.parse.quote(word.replace(" ", "_")),
            "source": "Wiktionary",
        }

    def wikiquote(self, name: str):
        """Famous-quotes profile from Wikiquote. Returns {"title",
        "extract", "url", "source"} or {"error": str}."""
        name = name.strip()
        if not name:
            return {"error": "who should I pull quotes for?"}
        data = self._wiki_api("quotes", {
            "action": "query", "prop": "extracts", "explaintext": "1",
            "exintro": "1", "titles": name,
        })
        if "error" in data:
            return data
        pages = data.get("query", {}).get("pages") or []
        page = pages[0] if pages else {}
        extract = page.get("extract") if isinstance(page, dict) else ""
        if not extract:
            return {"error": f"Wikiquote has no profile for '{name}'"}
        return {
            "title": page.get("title") or name,
            "extract": _WS_RE.sub(" ", extract).strip()[: _MAX_TEXT_CHARS],
            "url": "https://en.wikiquote.org/wiki/" + urllib.parse.quote(name.replace(" ", "_")),
            "source": "Wikiquote",
        }

    def _phase(self, query: str):
        """Wikipedia title search for a near-exact phrase match, using
        the full-text search API (better recall than opensearch). Only
        results that actually share a meaningful token with the query
        are trusted - full-text search loves returning unrelated pages
        ('kwa heri' -> '63rd Locarno Film Festival'), which is worse
        than no answer."""
        tokens = set()
        for tok in re.split(r"\W+", query.lower()):
            if len(tok) > 1 and tok not in _STOPWORDS:
                tokens.add(tok)
        titles = self.wikipedia_search(query, limit=8)
        if "error" in titles:
            return titles
        tried = set()
        for item in titles["results"]:
            title = item["title"]
            for candidate in (title, title.split(" (")[0]):
                if candidate.lower() in tried:
                    continue
                tried.add(candidate.lower())
                if tokens:
                    title_terms = {w for w in re.split(r"\W+", candidate.lower())
                                   if len(w) > 1 and w not in _STOPWORDS}
                    if not title_terms.intersection(tokens):
                        # zero overlap = irrelevant page; skip it
                        continue
                cand = self.wikipedia_extract(candidate, lang="en")
                if "error" not in cand:
                    return cand
        return {"error": f"no Wikipedia article for '{query}'"}

    def lookup(self, query: str):
        """Deep multi-source lookup. Walks, in order:
          1. Wikipedia REST summaries - simple, en, sw, fr
          2. Wikipedia full-extract (deep) - en, then sw for a
             Swahili-sounding query
          3. Wikipedia title search -> full extract of the match
          4. Wiktionary (single words) and Wikiquote (people, bands)
          5. Merged web search (DuckDuckGo + Bing)
          6. Deep read: fetch the TOP web result and summarize it, so
             even obscure local topics get real content.
        Returns the FIRST source that answers. Always fail-closed."""
        topic = query.strip()
        if not topic:
            return {"error": "what should I look up?"}

        # Hard budget for the wiki-probing part of the chain: network
        # throttling should degrade us to web search, never pile 10+
        # timeouts onto one reply.
        _start = time.monotonic()
        _BUDGET = 20.0

        def _out_of_budget() -> bool:
            return time.monotonic() - _start > _BUDGET

        # 1) Wikipedia REST summaries: probe simple + en IN PARALLEL (a slow
        #    miss on one never blocks a fast hit - e.g. 'serendipity'),
        #    and only reach for sw + fr if both missed. Two-at-a-time
        #    keeps Wikipedia happy and throttling-free.
        try:
            import concurrent.futures as _cf
            with _cf.ThreadPoolExecutor(max_workers=2) as pool:
                for langs in ((self._WIKI_LANGS[0], self._WIKI_LANGS[1]),
                              (self._WIKI_LANGS[2], self._WIKI_LANGS[3])):
                    futures = {pool.submit(self.wikipedia_summary, topic, lang): lang
                               for lang in langs}
                    for fut in _cf.as_completed(futures):
                        try:
                            first = fut.result()
                        except Exception:
                            continue
                        if "error" not in first and first.get("extract"):
                            return first
            # if all four probes missed but one looked "close", the phase
            # search below still rescues via a loose title match.
        except Exception:
            # threads unavailable - fall back to sequential probing
            for lang in self._WIKI_LANGS:
                first = self.wikipedia_summary(topic, lang=lang)
                if "error" not in first and first.get("extract"):
                    return first

        # 2) Wikipedia title search -> extract of the best match. This
        #    is the reliable path for multi-word topics ('kikuyu town',
        #    'alliance high school'); retry once against throttling.
        if not _out_of_budget():
            for attempt in (1, 2):
                phased = self._phase(topic)
                if "error" not in phased:
                    return phased
                if attempt == 1 and not _out_of_budget():
                    time.sleep(0.6)
                elif attempt == 1:
                    break

        # 3) Deep extracts (when the title search missed, e.g. the page
        #    lives under a different exact title) - en, then sw.
        if not _out_of_budget():
            deep = self.wikipedia_extract(topic, lang="en")
            if "error" not in deep:
                return deep
        if not _out_of_budget():
            deep_sw = self.wikipedia_extract(topic, lang="sw")
            if "error" not in deep_sw:
                return deep_sw

        # 4) Wiktionary first (single words AND common phrases, e.g.
        #    "kwa heri" - both are real Wiktionary entries), then
        #    Wikiquote for famous people.
        if not _out_of_budget():
            wikt = self.wiktionary_define(topic)
            if "error" not in wikt:
                return wikt
        if not _out_of_budget():
            quote = self.wikiquote(topic)
            if "error" not in quote:
                return quote

        # 4b) Common Swahili / French phrases that aren't Wikipedia
        #     subjects -> last-resort curated translation dictionary
        #     (hand-verified, so the bot never confidently says
        #     something wrong like "kwa heri is Swahili for 'To a gat'".
        lang = _guess_phrase_lang(topic)
        if lang:
            key = topic.strip().lower()
            trans = _TRANSLATIONS.get(key)
            if trans:
                return {
                    "title": trans[0],
                    "extract": (f"'{topic}' is {lang} for "
                                f"'{trans[0]}'."),
                    "url": "https://en.wiktionary.org",
                    "source": "translation",
                }

        # 5) Wide web search (multiple engines, merged + deduped).
        web = self.web_search(topic, limit=8)
        if "error" in web:
            return web

        # 6) DEPTH: read the top result page itself - a real answer,
        #    not just a headline. Wikipedia URLs get the clean extract
        #    API treatment (their HTML is navigation-heavy); everything
        #    else uses the plain-text reader. Scan up to four candidates
        #    (search engines lead with their own redirect pages), but
        #    never perform more than two real page reads.
        #    Dogfood URLs from the search engines (DDG landing pages)
        #    are never worth deep-reading.
        reads_left = 2
        for item in web["results"][:4]:
            if reads_left <= 0:
                break
            url = item["url"]
            host = (url.split("//", 1)[-1].split("/", 1)[0] if "//" in url else "").lower()
            if host in _DOGFOOD_HOSTS:
                continue
            reads_left -= 1
            if self._is_wiki_url(url):
                m = re.match(r"https?://([a-z]+)\.wikipedia\.org/wiki/(.+)", url)
                lang = m.group(1) if m else "en"
                cand = self.wikipedia_extract(
                    urllib.parse.unquote(m.group(2).replace("_", " ")) if m else url,
                    lang=lang if lang in self._WIKI_LANGS else "en",
                )
                if "error" not in cand:
                    return {
                        "title": f"{cand['title']} ({url})",
                        "extract": cand["extract"],
                        "url": url,
                        "urls": [r["url"] for r in web["results"]],
                        "source": "web search (deep read)",
                    }
                continue
            page = self.read_page(url)
            if "error" not in page and page.get("summary"):
                return {
                    "title": f"{page['title']} ({url})",
                    "extract": page["summary"],
                    "url": url,
                    "urls": [r["url"] for r in web["results"]],
                    "source": "web search (deep read)",
                }
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

    def web_search(self, query: str, limit: int = 8):
        """Multi-engine web search: DuckDuckGo first (JSON then lite
        HTML), Bing as a second engine, results merged + deduped by
        URL. Returns {"results": [{"title", "snippet", "url"}, ...]}
        or {"error": str}."""
        all_results = []
        for engine in (self._ddg_json, self._ddg_lite, self.bing_search):
            try:
                results = engine(query, limit)
                if isinstance(results, list):
                    all_results.extend(results)
            except Exception:
                continue
            if len(all_results) >= limit:
                break
        deduped = []
        seen = set()
        for r in all_results:
            url = r.get("url", "")
            try:
                key = urllib.parse.unquote(url).lower().split("&")[0].rstrip("/")
            except Exception:
                key = url.lower().split("&")[0].rstrip("/")
            # note: the search engines' own landing pages are NOT dropped
            # here - their snippets are still informative, and the deep-
            # read step (which fetches a URL's body) skips them anyway.
            if not key or key in seen:
                continue
            seen.add(key)
            deduped.append(r)
            if len(deduped) >= limit:
                break
        if not deduped:
            return {"error": f"no web results for '{query}'"}
        return {"results": deduped}

    def _ddg_json(self, query: str, limit: int = 8):
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

    def _ddg_lite(self, query: str, limit: int = 8):
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

    def bing_search(self, query: str, limit: int = 8):
        """Bing HTML search results (browser UA required). Returns a
        results list (possibly empty) - used as a second engine."""
        url = "https://www.bing.com/search?q=" + urllib.parse.quote(query) + "&count=20"
        raw = _fetch_html_ua(url, timeout=self.timeout_seconds, headers=_WEB_UA)
        if isinstance(raw, dict):
            return []
        html = _decode(raw)
        results = []
        if BS4_AVAILABLE:
            soup = BeautifulSoup(html, "html.parser")
            for li in soup.select("li.b_algo"):
                a = li.select_one("h2 a")
                if a is None:
                    continue
                href = a.get("href", "")
                title = a.get_text(" ", strip=True)
                p = li.select_one(".b_caption p") or li.select_one("p")
                snippet = p.get_text(" ", strip=True) if p else ""
                if href and title:
                    results.append({"title": title[:80], "snippet": snippet, "url": href})
                if len(results) >= limit:
                    break
        else:
            for m in re.finditer(
                r'<li class="b_algo".*?<a[^>]*href="([^"]+)"[^>]*>(.*?)</a>',
                html, flags=re.I | re.S,
            ):
                title = _WS_RE.sub(" ", _HTML_TAG_RE.sub(" ", m.group(2))).strip()
                if title and m.group(1).startswith("http"):
                    results.append({"title": title[:80], "snippet": "", "url": m.group(1)})
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

    def wikipedia_search(self, query: str, limit: int = 6):
        """Full-text Wikipedia title search (better recall than the old
        opensearch prefix match). Returns {"results": [{"title":
        "url"}...]} or {"error": str}."""
        data = self._wiki_api("en", {
            "action": "query", "list": "search", "srsearch": query,
            "srlimit": str(limit),
        })
        if "error" in data:
            return data
        pages = data.get("query", {}).get("search") or []
        if not pages:
            return {"error": f"no Wikipedia results for '{query}'"}
        host = self._WIKI_HOSTS["en"]
        return {"results": [
            {"title": p.get("title", ""),
             "url": host + "/wiki/" + urllib.parse.quote(p.get("title", "").replace(" ", "_"))}
            for p in pages
        ]}

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
        the deep multi-source lookup chain (Wikipedia in 4 languages,
        full extracts, Wiktionary, Wikiquote, then merged web search
        with a deep read of the top result)."""
        result = self.lookup(query)
        if "error" in result:
            # maybe no network or no article - say so gracefully
            return f"I couldn't find anything on '{query}': {result['error']}."

        lines = [f"**{result['title']}**"]
        if result.get("extract"):
            lines.append(result["extract"])
        if result.get("urls"):
            lines.append("")
            lines.append("Sources:")
            for u in result["urls"]:
                lines.append(f"- {u}")
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