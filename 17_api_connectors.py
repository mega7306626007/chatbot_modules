"""External API connectors: weather/currency/trivia/news, opt-in (Section 13)
Auto-split from the original single-file chatbot.py - see main.py for load order.
"""

# SECTION 13: EXTERNAL API CONNECTORS (opt-in, real HTTP, fail-closed)
# ==============================================================================
#
# Every connector in this section follows the exact same contract as
# LLMConnector (Section 6I): plain urllib (no extra SDK dependency),
# fails closed on ANY problem (returns None/an error dict rather than
# raising), and is never load-bearing - the rest of the bot works fully
# offline without any of these. Unlike LLMConnector, most of these use
# APIs that don't require a key (Open-Meteo for weather, the Frankfurter
# ECB-rates API for currency, Open Trivia Database for bonus trivia),
# so there's less config-file ceremony, but the same fail-closed
# philosophy applies: no network in this environment, a bad response
# shape, a timeout, or a non-200 status all just mean "this feature
# isn't available right now," never a crash.
#
# A tiny shared REST client (_RestApiClient) centralizes the actual
# HTTP mechanics - timeout handling, JSON parsing, retry-with-backoff,
# and a short-lived in-memory response cache - so each connector class
# below is mostly just "which URL, which fields do I care about."

class _RestApiClient:
    """
    A minimal, dependency-free REST client shared by the connectors
    below. Not a general HTTP library - just enough machinery (GET with
    query params, JSON parsing, timeout, retry-with-backoff, a short
    TTL cache) to avoid repeating the same 20 lines of urllib
    boilerplate in every connector class.
    """

    def __init__(self, timeout_seconds: float = 8.0, cache_ttl_seconds: float = 120.0):
        self.timeout_seconds = timeout_seconds
        self.cache_ttl_seconds = cache_ttl_seconds
        self._cache = {}  # url -> (fetched_at, parsed_json)

    def get_json(self, url: str, params: dict = None, max_attempts: int = 2):
        """
        Performs a GET request and returns the parsed JSON body, or a
        dict {"error": str} on any failure - callers check for the
        "error" key rather than catching exceptions. Retries transient
        failures (timeouts, 5xx) once with a short backoff, same
        philosophy as LLMConnector.generate_reply_with_retry.
        """
        full_url = url
        if params:
            query = urllib.parse.urlencode(params)
            full_url = f"{url}?{query}"

        cached = self._cache.get(full_url)
        if cached is not None:
            fetched_at, payload = cached
            if time.time() - fetched_at < self.cache_ttl_seconds:
                return payload

        last_error = None
        for attempt in range(1, max_attempts + 1):
            try:
                request = urllib.request.Request(full_url, headers={"User-Agent": "offline-chatbot/1.0"})
                with urllib.request.urlopen(request, timeout=self.timeout_seconds) as response:
                    if response.status != 200:
                        last_error = f"HTTP {response.status}"
                        continue
                    body = response.read().decode("utf-8")
                    payload = json.loads(body)
                    self._cache[full_url] = (time.time(), payload)
                    return payload
            except urllib.error.HTTPError as e:
                last_error = f"HTTP {e.code}"
                if e.code < 500:
                    break  # client errors (404, 400, ...) won't fix themselves on retry
            except urllib.error.URLError as e:
                last_error = f"couldn't reach the API ({e.reason})"
            except TimeoutError:
                last_error = "request timed out"
            except (json.JSONDecodeError, ValueError) as e:
                last_error = f"malformed response ({e})"
                break  # a retry won't un-malform the same response
            if attempt < max_attempts:
                time.sleep(0.5 * attempt)

        return {"error": last_error or "unknown error"}

    def clear_cache(self):
        self._cache = {}


_shared_rest_client = _RestApiClient()


class WeatherAPIConnector:
    """
    Real current-weather + short forecast lookups via Open-Meteo
    (open-meteo.com), chosen specifically because its core endpoints
    need NO API key - reduces this to "does the bot have a network
    connection" rather than also requiring config-file key management
    like LLMConnector. Two real HTTP calls happen per lookup: one to
    Open-Meteo's free geocoding endpoint (turns a place name into
    latitude/longitude) and one to the forecast endpoint itself.
    """

    GEOCODE_URL = "https://geocoding-api.open-meteo.com/v1/search"
    FORECAST_URL = "https://api.open-meteo.com/v1/forecast"

    # A small subset of Open-Meteo's WMO weather codes, human-readable.
    # (Full table has ~30 codes; these cover the common cases.)
    _WEATHER_CODE_DESCRIPTIONS = {
        0: "clear sky", 1: "mostly clear", 2: "partly cloudy", 3: "overcast",
        45: "fog", 48: "depositing rime fog",
        51: "light drizzle", 53: "moderate drizzle", 55: "dense drizzle",
        61: "slight rain", 63: "moderate rain", 65: "heavy rain",
        71: "slight snow", 73: "moderate snow", 75: "heavy snow",
        80: "rain showers", 81: "moderate rain showers", 82: "violent rain showers",
        95: "thunderstorm", 96: "thunderstorm with light hail", 99: "thunderstorm with heavy hail",
    }

    def __init__(self, client: _RestApiClient = None):
        self.client = client or _shared_rest_client

    def geocode(self, place_name: str):
        """Returns {"name", "latitude", "longitude", "country"} for the
        best-matching place, or None if nothing was found/reachable."""
        result = self.client.get_json(self.GEOCODE_URL, params={"name": place_name, "count": 1})
        if "error" in result:
            return None
        matches = result.get("results") or []
        if not matches:
            return None
        top = matches[0]
        return {
            "name": top.get("name", place_name),
            "latitude": top.get("latitude"),
            "longitude": top.get("longitude"),
            "country": top.get("country", ""),
        }

    def current_weather(self, place_name: str):
        """Returns a dict with current temperature/weather description
        for the given place, or {"error": str} on any failure."""
        location = self.geocode(place_name)
        if location is None:
            return {"error": f"I couldn't find a place called '{place_name}'."}

        result = self.client.get_json(self.FORECAST_URL, params={
            "latitude": location["latitude"],
            "longitude": location["longitude"],
            "current": "temperature_2m,relative_humidity_2m,wind_speed_10m,weather_code",
            "temperature_unit": "celsius",
        })
        if "error" in result:
            return {"error": f"Couldn't reach the weather service ({result['error']})."}

        current = result.get("current")
        if not current:
            return {"error": "Weather service returned an unexpected response shape."}

        code = current.get("weather_code")
        return {
            "place": location["name"],
            "country": location["country"],
            "temperature_c": current.get("temperature_2m"),
            "humidity_percent": current.get("relative_humidity_2m"),
            "wind_speed_kmh": current.get("wind_speed_10m"),
            "description": self._WEATHER_CODE_DESCRIPTIONS.get(code, "unknown conditions"),
        }

    def forecast(self, place_name: str, days: int = 3):
        """Returns a real multi-day forecast (high/low temps,
        conditions, precipitation chance per day) - Open-Meteo's daily
        aggregation endpoint, same API/no-key setup as current_weather,
        just a different set of query params. Added alongside the
        broader push to make every online feature richer, not just
        reachable."""
        days = max(1, min(days, 7))  # Open-Meteo's free tier caps at 16; 7 is plenty for a chat reply
        location = self.geocode(place_name)
        if location is None:
            return {"error": f"I couldn't find a place called '{place_name}'."}

        result = self.client.get_json(self.FORECAST_URL, params={
            "latitude": location["latitude"],
            "longitude": location["longitude"],
            "daily": "weather_code,temperature_2m_max,temperature_2m_min,precipitation_probability_max",
            "temperature_unit": "celsius",
            "forecast_days": days,
        })
        if "error" in result:
            return {"error": f"Couldn't reach the weather service ({result['error']})."}

        daily = result.get("daily")
        if not daily or "time" not in daily:
            return {"error": "Weather service returned an unexpected response shape."}

        days_out = []
        for i, date_str in enumerate(daily["time"]):
            code = daily.get("weather_code", [None] * len(daily["time"]))[i]
            days_out.append({
                "date": date_str,
                "high_c": daily.get("temperature_2m_max", [None])[i],
                "low_c": daily.get("temperature_2m_min", [None])[i],
                "precipitation_chance_percent": daily.get("precipitation_probability_max", [None])[i],
                "description": self._WEATHER_CODE_DESCRIPTIONS.get(code, "unknown conditions"),
            })

        return {"place": location["name"], "country": location["country"], "days": days_out}

    def format_current_weather(self, place_name: str) -> str:
        result = self.current_weather(place_name)
        if "error" in result:
            return result["error"]
        location_label = result["place"] + (f", {result['country']}" if result["country"] else "")
        return (f"Weather in {location_label}: {result['description']}, "
                f"{result['temperature_c']}°C, humidity {result['humidity_percent']}%, "
                f"wind {result['wind_speed_kmh']} km/h.")

    def format_forecast(self, place_name: str, days: int = 3) -> str:
        result = self.forecast(place_name, days)
        if "error" in result:
            return result["error"]
        location_label = result["place"] + (f", {result['country']}" if result["country"] else "")
        lines = [f"{len(result['days'])}-day forecast for {location_label}:"]
        for day in result["days"]:
            rain_note = (f", {day['precipitation_chance_percent']}% chance of rain"
                         if day["precipitation_chance_percent"] not in (None, 0) else "")
            lines.append(f"  {day['date']}: {day['description']}, "
                         f"{day['low_c']}-{day['high_c']}°C{rain_note}")
        return "\n".join(lines)


class CurrencyExchangeConnector:
    """
    Real currency conversion via the Frankfurter API (frankfurter.dev),
    which republishes European Central Bank reference rates and, like
    Open-Meteo, needs no API key. ECB rates update once per business
    day, which this connector's 2-minute cache (via _RestApiClient)
    comfortably respects without adding its own caching logic.
    """

    RATES_URL = "https://api.frankfurter.dev/v1/latest"
    HISTORICAL_URL_TEMPLATE = "https://api.frankfurter.dev/v1/{date}"
    CURRENCIES_URL = "https://api.frankfurter.dev/v1/currencies"

    def __init__(self, client: _RestApiClient = None):
        self.client = client or _shared_rest_client

    def convert(self, amount: float, from_currency: str, to_currency: str):
        from_currency = from_currency.upper().strip()
        to_currency = to_currency.upper().strip()
        result = self.client.get_json(self.RATES_URL, params={"base": from_currency, "symbols": to_currency})
        if "error" in result:
            return {"error": f"Couldn't reach the exchange rate service ({result['error']})."}

        rates = result.get("rates", {})
        rate = rates.get(to_currency)
        if rate is None:
            return {"error": f"No rate found for {from_currency} -> {to_currency}. Check the currency codes."}

        return {
            "amount": amount,
            "from": from_currency,
            "to": to_currency,
            "rate": rate,
            "converted": round(amount * rate, 2),
            "date": result.get("date", "unknown"),
        }

    def convert_to_many(self, amount: float, from_currency: str, to_currencies: list):
        """Converts to SEVERAL target currencies in one call, rather
        than making the caller loop convert() once per currency -
        Frankfurter supports a comma-separated 'symbols' param, so
        this is one real HTTP request either way."""
        from_currency = from_currency.upper().strip()
        to_currencies = [c.upper().strip() for c in to_currencies]
        result = self.client.get_json(self.RATES_URL, params={
            "base": from_currency, "symbols": ",".join(to_currencies),
        })
        if "error" in result:
            return {"error": f"Couldn't reach the exchange rate service ({result['error']})."}

        rates = result.get("rates", {})
        if not rates:
            return {"error": f"No rates found for {from_currency}. Check the currency codes."}

        conversions = {code: round(amount * rate, 2) for code, rate in rates.items()}
        return {"amount": amount, "from": from_currency, "conversions": conversions,
                "date": result.get("date", "unknown")}

    def historical_comparison(self, amount: float, from_currency: str, to_currency: str, days_ago: int = 7):
        """Compares today's rate against the rate `days_ago` days back,
        so a conversion answer can say whether the currency has
        strengthened or weakened recently - genuinely more useful than
        a single static number, and Frankfurter's historical endpoint
        (just a date in the URL path instead of 'latest') makes this a
        second real HTTP call, not a guess."""
        from_currency = from_currency.upper().strip()
        to_currency = to_currency.upper().strip()

        today_result = self.convert(amount, from_currency, to_currency)
        if "error" in today_result:
            return today_result

        past_date = (dt.date.today() - dt.timedelta(days=days_ago)).isoformat()
        past_result = self.client.get_json(
            self.HISTORICAL_URL_TEMPLATE.format(date=past_date),
            params={"base": from_currency, "symbols": to_currency},
        )
        if "error" in past_result:
            # Historical data failing shouldn't sink the whole request -
            # today's rate is still useful on its own.
            today_result["historical_error"] = past_result["error"]
            return today_result

        past_rate = past_result.get("rates", {}).get(to_currency)
        if past_rate is None:
            today_result["historical_error"] = "no historical rate available for that date"
            return today_result

        change_percent = ((today_result["rate"] - past_rate) / past_rate) * 100
        today_result["past_rate"] = past_rate
        today_result["past_date"] = past_result.get("date", past_date)
        today_result["change_percent"] = round(change_percent, 2)
        return today_result

    def list_currencies(self):
        result = self.client.get_json(self.CURRENCIES_URL)
        if "error" in result:
            return {"error": f"Couldn't reach the exchange rate service ({result['error']})."}
        return {"currencies": result}

    def format_conversion(self, amount: float, from_currency: str, to_currency: str) -> str:
        result = self.convert(amount, from_currency, to_currency)
        if "error" in result:
            return result["error"]
        return (f"{result['amount']} {result['from']} = {result['converted']} {result['to']} "
                f"(rate {result['rate']}, as of {result['date']}).")

    def format_multi_conversion(self, amount: float, from_currency: str, to_currencies: list) -> str:
        result = self.convert_to_many(amount, from_currency, to_currencies)
        if "error" in result:
            return result["error"]
        lines = [f"{result['amount']} {result['from']} converts to (as of {result['date']}):"]
        for code, converted in result["conversions"].items():
            lines.append(f"  {converted} {code}")
        return "\n".join(lines)

    def format_historical_comparison(self, amount: float, from_currency: str, to_currency: str,
                                      days_ago: int = 7) -> str:
        result = self.historical_comparison(amount, from_currency, to_currency, days_ago)
        if "error" in result:
            return result["error"]
        base = (f"{result['amount']} {result['from']} = {result['converted']} {result['to']} "
                f"(rate {result['rate']}, as of {result['date']})")
        if "change_percent" not in result:
            note = result.get("historical_error", "no historical comparison available")
            return f"{base}. ({note})"
        direction = "stronger" if result["change_percent"] > 0 else "weaker"
        return (f"{base}. {result['from']} is {abs(result['change_percent'])}% {direction} against "
                f"{result['to']} than it was on {result['past_date']} "
                f"(rate was {result['past_rate']}).")


class OnlineTriviaConnector:
    """
    Supplements FunExtras' offline TRIVIA bank (Section 6B) with fresh
    questions from the Open Trivia Database (opentdb.com) - a free,
    no-key-required trivia API. Explicitly a SUPPLEMENT, not a
    replacement: FunExtras.random_trivia() (offline, instant, always
    available) remains the default; this connector is only reached when
    the caller specifically wants a fresh/online question, and always
    fails closed back to the offline bank on any network problem.
    """

    API_URL = "https://opentdb.com/api.php"
    CATEGORIES_URL = "https://opentdb.com/api_category.php"

    # Open Trivia DB's actual response_code meanings - previously
    # ignored entirely (only an empty results list was checked, which
    # meant a rate-limited or "not enough questions for this category"
    # response looked identical to a generic connection problem).
    _RESPONSE_CODE_MESSAGES = {
        1: "not enough questions exist for that category/difficulty combination",
        2: "invalid parameter (check the category ID or difficulty)",
        3: "session token not found",
        4: "all available questions for this token have been used",
        5: "rate limited by the trivia service - wait a few seconds and try again",
    }

    def __init__(self, client: _RestApiClient = None):
        self.client = client or _shared_rest_client

    @staticmethod
    def _unescape(text: str) -> str:
        """Open Trivia DB HTML-encodes special characters; this decodes
        the small set that actually shows up in practice (quotes,
        apostrophes, ampersands) without pulling in html.unescape's
        full entity table for what's typically a handful of cases."""
        replacements = {
            "&quot;": '"', "&#039;": "'", "&amp;": "&",
            "&eacute;": "é", "&uuml;": "ü", "&ntilde;": "ñ",
        }
        for entity, char in replacements.items():
            text = text.replace(entity, char)
        return text

    def list_categories(self):
        """Real category list from the API (34 categories as of
        writing, e.g. 'Science: Computers', 'Sports', 'History') -
        needed since fetch_question's category param takes a numeric
        ID, not a free-text name."""
        result = self.client.get_json(self.CATEGORIES_URL)
        if "error" in result:
            return {"error": f"Couldn't reach the trivia service ({result['error']})."}
        categories = result.get("trivia_categories")
        if not categories:
            return {"error": "Trivia service returned an unexpected response shape."}
        return {"categories": [(c["id"], c["name"]) for c in categories]}

    def fetch_question(self, difficulty: str = None, category_id: int = None):
        params = {"amount": 1, "type": "multiple"}
        if difficulty in ("easy", "medium", "hard"):
            params["difficulty"] = difficulty
        if category_id is not None:
            params["category"] = category_id

        result = self.client.get_json(self.API_URL, params=params)
        if "error" in result:
            return {"error": f"Couldn't reach the online trivia service ({result['error']})."}

        # BUGFIX: response_code was never actually checked - a
        # rate-limited or "no questions match this filter" response
        # (which still comes back as HTTP 200 with an empty results
        # list) was indistinguishable from "the service is down",
        # giving a misleading error message either way.
        response_code = result.get("response_code")
        if response_code and response_code != 0:
            reason = self._RESPONSE_CODE_MESSAGES.get(response_code, f"response code {response_code}")
            return {"error": f"Couldn't get a trivia question ({reason})."}

        results = result.get("results") or []
        if not results:
            return {"error": "The trivia service didn't return a question."}

        item = results[0]
        question = self._unescape(item.get("question", ""))
        correct = self._unescape(item.get("correct_answer", ""))
        incorrect = [self._unescape(a) for a in item.get("incorrect_answers", [])]
        choices = incorrect + [correct]
        random.shuffle(choices)

        return {
            "question": question,
            "choices": choices,
            "answer": correct.lower(),
            "category": item.get("category", ""),
            "difficulty": item.get("difficulty", ""),
        }

    def format_question(self, difficulty: str = None, category_id: int = None) -> str:
        result = self.fetch_question(difficulty, category_id)
        if "error" in result:
            return result["error"]
        letters = ["A", "B", "C", "D"]
        lines = [f"[{result['category']}, {result['difficulty']}] {result['question']}"]
        for letter, choice in zip(letters, result["choices"]):
            lines.append(f"  {letter}) {choice}")
        return "\n".join(lines)

    def format_categories(self) -> str:
        result = self.list_categories()
        if "error" in result:
            return result["error"]
        lines = ["Trivia categories:"]
        for cat_id, name in result["categories"]:
            lines.append(f"  {cat_id}: {name}")
        return "\n".join(lines)


class TranslationAPIConnector:
    """
    Machine translation with TWO backends:
      - MyMemory (api.mymemory.translated.net) - free, no API key,
        used by DEFAULT. Rate-limited (1,000 words/day anonymously)
        but that's a perfectly reasonable ceiling for a chat feature,
        and it means translation now genuinely works with zero setup,
        unlike the LibreTranslate-only version of this connector.
      - LibreTranslate - opt-in, config-file based (same pattern as
        LLMConnector), for anyone who wants a self-hosted instance or
        has their own API key and prefers it over MyMemory.
    MyMemory is tried first whenever LibreTranslate isn't explicitly
    enabled in the config, so 'translate to spanish: hello' works
    immediately rather than needing any setup at all. Kept clearly
    separate from LanguageDetector (Section 7B), which only DETECTS a
    language via a fixed keyword dictionary and never translates -
    actual translation needs a real model, which is exactly what this
    connector calls out to (either backend).
    """

    DEFAULT_ENDPOINT = "https://libretranslate.com/translate"
    MYMEMORY_URL = "https://api.mymemory.translated.net/get"

    def __init__(self, config_path: str):
        self.config_path = config_path
        self.config = self._load_or_create_config()
        self.client = _RestApiClient(cache_ttl_seconds=3600.0)  # translations of the same text don't change

    def _load_or_create_config(self):
        template = {
            "_instructions": (
                "Translation works out of the box via the free MyMemory API "
                "(no setup needed, ~1000 words/day). To use LibreTranslate "
                "instead (e.g. a self-hosted instance, or your own API key "
                "for higher limits), set 'use_libretranslate' to true and "
                "fill in 'endpoint'/'api_key'."
            ),
            "use_libretranslate": False,
            "endpoint": self.DEFAULT_ENDPOINT,
            "api_key": "",
        }
        if not os.path.exists(self.config_path):
            try:
                with open(self.config_path, "w", encoding="utf-8") as f:
                    json.dump(template, f, indent=2, ensure_ascii=False)
            except OSError:
                pass
            return template
        try:
            with open(self.config_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            merged = dict(template)
            merged.update(data)
            return merged
        except (json.JSONDecodeError, OSError):
            return template

    def is_available(self) -> bool:
        # Always available now (MyMemory needs no config) - kept as a
        # method rather than removed outright since other code may
        # still call it expecting a capability check.
        return True

    def _translate_mymemory(self, text: str, target_lang: str, source_lang: str):
        # MyMemory wants ISO 639-1 codes joined with '|', and "auto"
        # isn't a real source option for it the way it is for
        # LibreTranslate - default to English as a reasonable guess
        # when the caller passes "auto", since most callers in this
        # bot are translating FROM whatever LanguageDetector already
        # identified, not truly unknown text.
        source = "en" if source_lang == "auto" else source_lang
        result = self.client.get_json(self.MYMEMORY_URL, params={
            "q": text, "langpair": f"{source}|{target_lang}",
        })
        if "error" in result:
            return {"error": f"Couldn't reach the translation API ({result['error']})."}

        response_data = result.get("responseData", {})
        translated = response_data.get("translatedText")
        response_status = result.get("responseStatus")
        if not translated or (response_status and response_status != 200):
            return {"error": "Translation API returned an unexpected response shape."}
        return {"translated_text": translated}

    def _translate_libretranslate(self, text: str, target_lang: str, source_lang: str):
        payload = {"q": text, "source": source_lang, "target": target_lang, "format": "text"}
        if self.config.get("api_key"):
            payload["api_key"] = self.config["api_key"]

        try:
            body = json.dumps(payload).encode("utf-8")
            request = urllib.request.Request(
                self.config["endpoint"], data=body, method="POST",
                headers={"Content-Type": "application/json"},
            )
            with urllib.request.urlopen(request, timeout=8) as response:
                data = json.loads(response.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            return {"error": f"Translation API returned HTTP {e.code}"}
        except urllib.error.URLError as e:
            return {"error": f"Couldn't reach the translation API ({e.reason})"}
        except (TimeoutError, json.JSONDecodeError, KeyError) as e:
            return {"error": f"Translation request failed ({e})"}

        translated = data.get("translatedText")
        if not translated:
            return {"error": "Translation API returned an unexpected response shape."}
        return {"translated_text": translated}

    def translate(self, text: str, target_lang: str, source_lang: str = "auto"):
        if self.config.get("use_libretranslate") and self.config.get("endpoint"):
            result = self._translate_libretranslate(text, target_lang, source_lang)
            if "error" not in result:
                return result
            # Fall through to MyMemory rather than failing outright if
            # the configured LibreTranslate instance is unreachable.
        return self._translate_mymemory(text, target_lang, source_lang)

    def format_translation(self, text: str, target_lang: str, source_lang: str = "auto") -> str:
        result = self.translate(text, target_lang, source_lang)
        if "error" in result:
            return result["error"]
        return result["translated_text"]


class NewsHeadlinesConnector:
    """
    Fetches current top-story headlines via the Hacker News Firebase
    API (hacker-news.firebaseio.com) - like Open-Meteo and Frankfurter,
    this needs NO API key, so it's usable with zero config. Two-stage
    fetch, same shape as most feed-style REST APIs: one call for a list
    of story IDs, then one call per ID for the story details - capped
    at a small number of items so a single "what's in the news" request
    doesn't turn into dozens of HTTP calls.
    """

    TOP_STORIES_URL = "https://hacker-news.firebaseio.com/v0/topstories.json"
    ITEM_URL_TEMPLATE = "https://hacker-news.firebaseio.com/v0/item/{item_id}.json"
    # HN's Firebase API exposes several story feeds beyond "top" - all
    # free, same endpoint shape, just a different list. Added so "top
    # headlines" isn't the only option.
    _STORY_TYPE_URLS = {
        "top": "https://hacker-news.firebaseio.com/v0/topstories.json",
        "best": "https://hacker-news.firebaseio.com/v0/beststories.json",
        "new": "https://hacker-news.firebaseio.com/v0/newstories.json",
        "ask": "https://hacker-news.firebaseio.com/v0/askstories.json",
        "show": "https://hacker-news.firebaseio.com/v0/showstories.json",
    }

    def __init__(self, client: _RestApiClient = None):
        self.client = client or _shared_rest_client

    def top_headlines(self, limit: int = 5, story_type: str = "top"):
        limit = max(1, min(limit, 10))
        story_type = story_type if story_type in self._STORY_TYPE_URLS else "top"
        story_ids = self.client.get_json(self._STORY_TYPE_URLS[story_type])
        if isinstance(story_ids, dict) and "error" in story_ids:
            return {"error": f"Couldn't reach the news service ({story_ids['error']})."}
        if not isinstance(story_ids, list) or not story_ids:
            return {"error": "News service returned an unexpected response shape."}

        headlines = []
        for item_id in story_ids[:limit]:
            item = self.client.get_json(self.ITEM_URL_TEMPLATE.format(item_id=item_id))
            if isinstance(item, dict) and "error" not in item and item.get("title"):
                headlines.append({
                    "title": item["title"],
                    "url": item.get("url", f"https://news.ycombinator.com/item?id={item_id}"),
                    "score": item.get("score", 0),
                })
        if not headlines:
            return {"error": "Couldn't fetch any headline details."}
        return {"headlines": headlines, "story_type": story_type}

    def format_headlines(self, limit: int = 5, story_type: str = "top") -> str:
        result = self.top_headlines(limit, story_type)
        if "error" in result:
            return result["error"]
        label = {"top": "TOP HEADLINES", "best": "BEST STORIES", "new": "NEWEST STORIES",
                  "ask": "ASK HN", "show": "SHOW HN"}.get(result["story_type"], "HEADLINES")
        lines = [f"{label} (Hacker News)", ""]
        for i, item in enumerate(result["headlines"], start=1):
            lines.append(f"  {i}. {item['title']} ({item['score']} points)")
            lines.append(f"     {item['url']}")
        return "\n".join(lines)


class RealPhotoConnector:
    """
    Fetches an actual, real, openly-licensed PHOTOGRAPH matching a
    search query via Openverse (openverse.org - the Creative Commons
    image search API WordPress runs), rather than generating one.
    Chosen specifically because its search endpoint needs NO API key,
    same reasoning as WeatherAPIConnector above.

    This is the honest answer to "make the CNN generate actual
    photos": no from-scratch, phone-trainable model actually produces
    real photographs - that needs a large pretrained diffusion/GAN
    model (gigabytes of weights, real GPU compute, and typically a
    paid API), none of which fits this project's offline-first, no-
    API-key-required design. What CAN honestly deliver a genuine
    photograph is fetching a REAL one, correctly licensed for reuse -
    so that's what this does, with CNNImageGenerator's procedural
    renderer (Section 12B) as the automatic fallback whenever there's
    no network, the API is unreachable, or nothing licensed for reuse
    matches the query. Every image returned includes its photographer
    credit and license, since that's a condition of the CC licenses
    Openverse indexes.
    """

    SEARCH_URL = "https://api.openverse.org/v1/images/"

    # Maps this bot's abstract shape vocabulary to a real-world,
    # PHOTOGRAPHABLE object noun - searching Openverse for "red circle"
    # mostly returns clip art/vector graphics (since that's what
    # actually gets tagged that way), while "red ball" returns actual
    # photographs of physical objects.
    SHAPE_TO_OBJECT_NOUN = {
        "circle": "ball",
        "square": "cube block",
        "triangle": "pyramid",
    }

    def __init__(self, client: _RestApiClient = None):
        self.client = client or _shared_rest_client

    def search(self, query: str):
        """Returns {"url", "title", "creator", "license"} for the
        top reusable-photo match, or {"error": str} on any failure -
        including "no results", which is a normal, expected outcome
        for an unusual query, not a bug."""
        result = self.client.get_json(self.SEARCH_URL, params={
            "q": query,
            "page_size": 1,
            # Restricting to actual photographs (not illustrations,
            # digitized art, or 3D renders) is the whole point here -
            # this filter is what makes the result an honest "photo".
            "category": "photograph",
            "license_type": "commercial,modification",
        })
        if "error" in result:
            return {"error": f"couldn't reach the photo search service ({result['error']})"}

        matches = result.get("results") or []
        if not matches:
            return {"error": f"no reusable photo found for '{query}'"}

        top = matches[0]
        return {
            "url": top.get("url"),
            "title": top.get("title", query),
            "creator": top.get("creator", "unknown"),
            "license": (top.get("license", "") or "").upper(),
        }

    def fetch_and_save(self, shape: str, color: str, output_path: str):
        """Searches for a real photo of '{color} {object noun for
        shape}' and downloads it to output_path. Returns
        {"path", "title", "creator", "license"} on success, or
        {"error": str} on any failure (network, no results, bad image
        data) - callers should fall back to CNNImageGenerator on any
        error dict, exactly like every other connector in this file.

        Retries with just the object noun (no color) if the exact
        color+object query comes back empty - "red pyramid" is a much
        narrower search than "pyramid", and a real photo of some other
        color is still far more useful than no photo at all, as long
        as the fallback is disclosed (see the returned "note" field)."""
        object_noun = self.SHAPE_TO_OBJECT_NOUN.get(shape, shape)
        query = f"{color} {object_noun}"

        found = self.search(query)
        used_fallback_query = False
        if "error" in found:
            found = self.search(object_noun)
            used_fallback_query = True
            if "error" in found:
                return found

        image_url = found.get("url")
        if not image_url:
            return {"error": "search result had no image URL"}

        try:
            request = urllib.request.Request(image_url, headers={"User-Agent": "offline-chatbot/1.0"})
            with urllib.request.urlopen(request, timeout=self.client.timeout_seconds) as response:
                if response.status != 200:
                    return {"error": f"image download failed (HTTP {response.status})"}
                image_bytes = response.read()
        except (urllib.error.URLError, TimeoutError) as e:
            return {"error": f"couldn't download the image ({e})"}

        if not PILLOW_AVAILABLE:
            return {"error": "Pillow isn't installed, so the downloaded image can't be processed"}
        try:
            with open(output_path, "wb") as f:
                f.write(image_bytes)
            # Round-trip through PIL once, both to validate it's a real,
            # decodable image (not an HTML error page or truncated
            # download) and to normalize it to RGB at a consistent size,
            # same as every image this bot saves.
            img = Image.open(output_path).convert("RGB")
            img = img.resize((GENERATOR_IMAGE_SIZE, GENERATOR_IMAGE_SIZE), Image.LANCZOS)
            img.save(output_path)
        except Exception as e:
            return {"error": f"downloaded file wasn't a valid image ({e})"}

        result = {
            "path": output_path, "title": found["title"],
            "creator": found["creator"], "license": found["license"],
        }
        if used_fallback_query:
            result["note"] = f"no '{query}' photo found, so this is just '{object_noun}' instead"
        return result


# ==============================================================================
