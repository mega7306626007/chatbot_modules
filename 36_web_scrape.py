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
    "news.google.com", "mojeek.com", "www.mojeek.com",
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
    "heri": ("luck / blessing (as in 'kwa heri' = goodbye)",),
    "baraka": ("blessing",),
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


# Swahili sides of the phrase dictionary (the rest are French). Kept
# separate because clue-word guessing ("heri") misses single words.
_SW_PHRASES = {
    "kwa heri", "kwaheri", "asante", "asante sana", "habari", "heri",
    "baraka", "habari yako", "habari za asubuhi", "habari za jioni",
    "mambo", "poa", "karibu", "karibu sana", "ndiyo", "hapana", "sijui",
    "ninafurahi kukusikia", "usiku mwema", "lala salama",
    "jina lako ni nani", "nakupenda", "nimekuelewa", "sielewi",
    "tafadhali", "samahani", "naweza kusaidiaje",
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
# Kenya-first knowledge base
# ---------------------------------------------------------------------------
# The user-facing personality of this bot is Kenyan-centric, so the
# lookup chain checks this curated, offline, deterministic factbase
# FIRST. It never needs the network, is always correct, and keeps the
# answers "Kenyan centralised" without blocking anything else: queries
# outside it fall straight through to the global Wikipedia/news/place/
# web-search chain unchanged.
_CANONICAL_FACT_ALIASES = {
    "masai mara": "maasai mara", "mara": "maasai mara",
    "mt kenya": "mount kenya", "mt. kenya": "mount kenya",
    "mt elgon": "mount elgon", "mt. elgon": "mount elgon",
    "lake naivasha": "naivasha", "lake baringo": "baringo",
    "lake bogoria": "bogoria", "lake elementaita": "elementaita",
    "lake magadi": "magadi", "lake jipe": "lake jipe",
    "lake turkana": "turkana", "lake nakuru": "nakuru",
    "lake victoria": "victoria", "fort jesus mombasa": "fort jesus",
    "nairobi national park": "nairobi park", "hells gate": "hell's gate",
    "masai mara national reserve": "maasai mara",
    "university of nairobi": "university of nairobi",
    "uon": "university of nairobi", "u.o.n": "university of nairobi",
    "u o n": "university of nairobi",
    "jkuat": "jomo kenyatta university", "kenyatta university": "kenyatta university",
    "kicd": "kicd", "knec": "knec", "kra": "kra", "kdf": "kdf",
    "jkia": "jomo kenyatta international airport",
    "kimathi": "dedan kimathi", "tom mboya": "tom mboya",
    "wangari maathai": "wangari maathai", "kipchoge keino": "kipchoge keino",
    "eliud kipchoge": "eliud kipchoge", "kipchoge": "eliud kipchoge",
    "raila": "raila odinga", "odinga": "raila odinga",
    "uhuru": "uhuru kenyatta", "jomo": "jomo kenyatta",
    "daniel arap moi": "daniel arap moi", "moi": "daniel arap moi",
    "mwai kibaki": "mwai kibaki", "kibaki": "mwai kibaki",
    "william ruto": "william ruto", "ruto": "william ruto",
    "alliance high school": "alliance high school", "mangu high": "mangu high",
    "lenana": "lenana school", "kenya high": "kenya high school",
    "starehe": "starehe boys", "starehe boys": "starehe boys",
    "maseno school": "maseno school", "kabarak": "kabarak high school",
    "kwale": "kwale", "kisumu": "kisumu", "nakuru town": "nakuru",
    "eldoret": "eldoret", "thika": "thika", "malindi": "malindi",
    "lamu": "lamu", "naivasha town": "naivasha", "nyeri": "nyeri",
    "kitui town": "kitui", "machakos town": "machakos", "embu town": "embu",
    "meru town": "meru", "kericho": "kericho", "vihiga": "vihiga",
    "busia town": "busia", "garissa town": "garissa", "wajir town": "wajir",
    "nanyuki": "nanyuki", "kitale": "kitale", "kakamega town": "kakamega",
    "wote": "makueni", "migori": "migori", "homa bay": "homa bay",
    "siaya": "siaya", "kajiado": "kajiado", "narok": "narok",
    "isiolo": "isiolo", "marsabit": "marsabit", "lodwar": "lodwar",
    "maralal": "maralal", "baringo county": "baringo",
    "ol kalou": "nyandarua", "kapsabet": "nandi", "iten": "itanda",
}

_KENYA_FACTS = {
    # -- country -----------------------------------------------------------------
    "kenya": {
        "extract": "Kenya is a country in East Africa. Capital and largest city: "
                   "Nairobi. Official languages: English and Swahili. Currency: "
                   "Kenyan shilling (KES). Population: about 55 million. It "
                   "became independent from Britain on 12 December 1963 and a "
                   "republic in 1964, with the motto 'Harambee'. It has 47 "
                   "counties and borders Tanzania, Uganda, South Sudan, Ethiopia "
                   "and Somalia, with the Indian Ocean to the south-east.",
        "url": "https://sw.wikipedia.org/wiki/Kenya",
    },
    "nairobi": {
        "extract": "Nairobi is the capital and largest city of Kenya. It is "
                   "nicknamed 'the Green City in the Sun'. It hosts the UN "
                   "offices, Jomo Kenyatta International Airport (JKIA), Nairobi "
                   "National Park (the only national park inside a capital "
                   "city), and big informal settlements like Kibera.",
        "url": "https://sw.wikipedia.org/wiki/Nairobi",
    },
    "mombasa": {
        "extract": "Mombasa is Kenya's second-largest city and its major port "
                   "on the Indian Ocean coast. It is the old Swahili capital "
                   "and home to Fort Jesus (a UNESCO World Heritage Site), the "
                   "historic Old Town, and Moi International Airport.",
        "url": "https://sw.wikipedia.org/wiki/Mombasa",
    },
    "kisumu": {
        "extract": "Kisumu is Kenya's third-largest city, a port on the shores "
                   "of Lake Victoria and headquarters of Kisumu County. It is "
                   "the main city of the Luo region and gateway to the lake "
                   "and its fish trade.",
        "url": "https://sw.wikipedia.org/wiki/Kisumu",
    },
    "nakuru": {
        "extract": "Nakuru is the capital of Nakuru County in the Rift Valley, "
                   "about 160 km north-west of Nairobi. It is the fourth-largest "
                   "town in Kenya and the gateway to Lake Nakuru National Park, "
                   "famous for its flamingos and rhinos.",
        "url": "https://sw.wikipedia.org/wiki/Nakuru",
    },
    "eldoret": {
        "extract": "Eldoret is the capital of Uasin Gishu County in the North "
                   "Rift, one of Kenya's largest towns and home to many of its "
                   "long-distance running champions. It has an international "
                   "airport and is a major cereals and dairy hub.",
        "url": "https://sw.wikipedia.org/wiki/Eldoret",
    },
    "thika": {
        "extract": "Thika is an industrial town in Kiambu County, about 40 km "
                   "north-east of Nairobi, on the road to Nyeri and Mount "
                   "Kenya. It is known for pineapple farming and the Thika "
                   "Superhighway.",
        "url": "https://sw.wikipedia.org/wiki/Thika",
    },
    "malindi": {
        "extract": "Malindi is a coastal town in Kilifi County, Kenya, north of "
                   "Mombasa. It is a major beach destination, famous for its "
                   "Swahili heritage, Vasco da Gama's pillar, and the nearby "
                   "Watamu marine parks where sea turtles nest.",
        "url": "https://sw.wikipedia.org/wiki/Malindi",
    },
    "lamu": {
        "extract": "Lamu Island and Lamu Town (Lamu County) on Kenya's north "
                   "coast are a UNESCO World Heritage Site, the oldest and "
                   "best-preserved Swahili settlement in East Africa. Known for "
                   "its architecture, dhow boat culture and the Maulidi "
                   "festival.",
        "url": "https://en.wikipedia.org/wiki/Lamu",
    },
    "naivasha": {
        "extract": "Naivasha is a town and freshwater lake in Nakuru County, "
                   "about 90 km north-west of Nairobi. Lake Naivasha is famous "
                   "for hippos, birdlife and flower farms; nearby is Hell's "
                   "Gate National Park and the Menengai Crater (at Nakuru).",
        "url": "https://sw.wikipedia.org/wiki/Naivasha",
    },
    "nyeri": {
        "extract": "Nyeri town is the capital of Nyeri County in Central Kenya, "
                   "the historic home of the Kikuyu people and a gateway to "
                   "Mount Kenya and the Aberdare Range. Jomo Kenyatta and Dedan "
                   "Kimathi are both buried nearby.",
        "url": "https://sw.wikipedia.org/wiki/Nyeri",
    },
    "kericho": {
        "extract": "Kericho is the capital of Kericho County in the South Rift, "
                   "Kenya's tea-producing heartland - some of the world's "
                   "largest tea estates lie here.",
        "url": "https://sw.wikipedia.org/wiki/Kericho",
    },
    "kakamega": {
        "extract": "Kakamega town is the capital of Kakamega County in Western "
                   "Kenya, home to the Kakamega Forest, Kenya's last remnant of "
                   "the Guineo-Congolian tropical rainforest with its own "
                   "unique birds, monkeys and butterflies.",
        "url": "https://sw.wikipedia.org/wiki/Kakamega",
    },
    "embu": {
        "extract": "Embu town is the capital of Embu County in Eastern Kenya, "
                   "on the slopes of Mount Kenya, known for coffee, tea, miraa "
                   "and the nearby Mwea rice fields.",
        "url": "https://sw.wikipedia.org/wiki/Embu",
    },
    "machakos": {
        "extract": "Machakos is the capital of Machakos County, about 64 km "
                   "south-east of Nairobi, one of the fastest-growing towns in "
                   "Eastern Kenya, historically the first colonial capital of "
                   "Kenya.",
        "url": "https://en.wikipedia.org/wiki/Machakos",
    },
    "meru": {
        "extract": "Meru town is the capital of Meru County on the north-eastern "
                   "slopes of Mount Kenya, a centre of agriculture (tea, coffee, "
                   "miraa) and mountaineering tourism.",
        "url": "https://sw.wikipedia.org/wiki/Meru",
    },
    "kitui": {
        "extract": "Kitui is the capital of Kitui County in Eastern Kenya, a "
                   "semi-arid county known for its baobab trees, palm wine and "
                   "recent gold mining finds.",
        "url": "https://en.wikipedia.org/wiki/Kitui",
    },
    "narok": {
        "extract": "Narok town is the capital of Narok County and the main "
                   "gateway to the Maasai Mara National Reserve, famous for the "
                   "annual wildebeest migration and Maasai culture.",
        "url": "https://sw.wikipedia.org/wiki/Narok",
    },
    "kajiado": {
        "extract": "Kajiado is the capital of Kajiado County south of Nairobi, "
                   "in Maasai country, home of Kitengela and the border "
                   "crossing at Namanga into Tanzania, plus the Amboseli-"
                   "Elephant Corridor.",
        "url": "https://en.wikipedia.org/wiki/Kajiado",
    },

    # -- physical geography -------------------------------------------------------
    "mount kenya": {
        "extract": "Mount Kenya (5,199 m) is Kenya's highest mountain and the "
                   "second-highest in Africa after Kilimanjaro. Its peaks are "
                   "glaciated and crowned by Batian and Nelion. It is the source "
                   "of the Tana river and a UNESCO World Heritage Site.",
        "url": "https://sw.wikipedia.org/wiki/Mlima_Kenya",
    },
    "mount elgon": {
        "extract": "Mount Elgon is an extinct volcano on the Kenya-Uganda "
                   "border, with one of the world's largest intact calderas - "
                   "its slopes rise to over 4,300 m.",
        "url": "https://en.wikipedia.org/wiki/Mount_Elgon",
    },
    "maasai mara": {
        "extract": "The Maasai Mara National Reserve in Narok County, southern "
                   "Kenya, is famous for the Great Migration - millions of "
                   "wildebeest, zebras and gazelles crossing from the Serengeti "
                   "every July to October - and the Big Five in its savanna.",
        "url": "https://sw.wikipedia.org/wiki/Hifadhi_ya_Maasai_Mara",
    },
    "amboseli": {
        "extract": "Amboseli National Park, at the foot of Mount Kilimanjaro in "
                   "Kajiado County, is famous for its large elephant herds and "
                   "sweeping views of Kilimanjaro (across the Tanzanian border).",
        "url": "https://sw.wikipedia.org/wiki/Amboseli",
    },
    "tsavo": {
        "extract": "Tsavo National Park is Kenya's largest park, split into "
                   "Tsavo East and Tsavo West. It is famous for the 'man-eaters "
                   "of Tsavo' lions, the Galana River, and combining savanna, "
                   "volcanic rock and swamp habitats in Taita-Taveta County.",
        "url": "https://en.wikipedia.org/wiki/Tsavo_National_Park",
    },
    "samburu": {
        "extract": "Samburu National Reserve in Samburu County, along the Ewaso "
                   "Ng'iro river, is famous for the rare 'Samburu special five': "
                   "the Grevy's zebra, reticulated giraffe, Somali ostrich, "
                   "beisa oryx and gerenuk.",
        "url": "https://en.wikipedia.org/wiki/Samburu_National_Reserve",
    },
    "nakuru park": {
        "extract": "Lake Nakuru National Park in Nakuru County is world-famous "
                   "for its flamingos - at their peak over a million birds - "
                   "plus rhinos (both black and white) and its soda lake.",
        "url": "https://en.wikipedia.org/wiki/Lake_Nakuru_National_Park",
    },
    "nairobi park": {
        "extract": "Nairobi National Park is the only national park in the world "
                   "inside a capital city, 7 km from Nairobi's centre, with "
                   "lions, rhinos, giraffes and wildebeest against the backdrop "
                   "of city skyscrapers.",
        "url": "https://en.wikipedia.org/wiki/Nairobi_National_Park",
    },
    "hell's gate": {
        "extract": "Hell's Gate National Park near Naivasha (Nakuru County) is "
                   "a dramatic gorge park with geothermal towers, cliffs and "
                   "hot springs - no predators, so visitors can cycle through it.",
        "url": "https://en.wikipedia.org/wiki/Hell%27s_Gate_National_Park",
    },
    "victoria": {
        "extract": "Lake Victoria is the largest lake in Africa and the world's "
                   "biggest tropical lake, shared by Kenya, Uganda and Tanzania. "
                   "Kenya's part forms the western border, with Kisumu and "
                   "Homa Bay on its shores and a booming Nile perch fisheries.",
        "url": "https://sw.wikipedia.org/wiki/Ziwa_Victoria",
    },
    "turkana": {
        "extract": "Lake Turkana, northern Kenya, is the world's largest "
                   "permanent desert lake and the largest alkaline lake. It is a "
                   "UNESCO World Heritage Site famous for fossil finds of early "
                   "human ancestors (Koobi Fora).",
        "url": "https://en.wikipedia.org/wiki/Lake_Turkana",
    },
    "bogoria": {
        "extract": "Lake Bogoria in Baringo County is a soda lake famous for "
                   "its hot springs, geysers and huge flocks of flamingos - up "
                   "to a million birds at times.",
        "url": "https://en.wikipedia.org/wiki/Lake_Bogoria",
    },
    "baringo": {
        "extract": "Lake Baringo is a freshwater lake in Baringo County, one of "
                   "Kenya's two freshwater Rift Valley lakes (with Naivasha). It "
                   "is famous for its 400+ bird species, crocodiles and hippos.",
        "url": "https://en.wikipedia.org/wiki/Lake_Baringo",
    },
    "elementaita": {
        "extract": "Lake Elementaita is a shallow soda lake in Nakuru County, "
                   "part of the Kenya Lake System UNESCO site, a major flamingo "
                   "and bird sanctuary.",
        "url": "https://en.wikipedia.org/wiki/Lake_Elementaita",
    },
    "magadi": {
        "extract": "Lake Magadi in Kajiado County is an intensely alkaline soda "
                   "lake - dense with flamingos - where Kenya's soda ash is "
                   "mined by the Magadi Soda Company.",
        "url": "https://en.wikipedia.org/wiki/Lake_Magadi",
    },
    "tana": {
        "extract": "The Tana River is Kenya's longest river (~1,000 km). It "
                   "drains Mount Kenya and the Aberdares through Garissa to the "
                   "Indian Ocean, feeding hydroelectric dams at Masinga and "
                   "Kiambere.",
        "url": "https://en.wikipedia.org/wiki/Tana_River_(Kenya)",
    },

    # -- presidents & heroes ------------------------------------------------------
    "jomo kenyatta": {
        "extract": "Mzee Jomo Kenyatta (1897-1978) was Kenya's first President "
                   "(1964-78), a Pan-African leader, author of 'Facing Mount "
                   "Kenya', and the first leader of an independent Kenya in "
                   "1963. He is Kenya's founding father.",
        "url": "https://sw.wikipedia.org/wiki/Jomo_Kenyatta",
    },
    "daniel arap moi": {
        "extract": "Daniel arap Moi (1924-2020) was Kenya's second President "
                   "(1978-2002), the longest-serving, from the Rift Valley's "
                   "Tugen community. He coined the philosophy of 'Nyayo' "
                   "(following in the founding father's footsteps).",
        "url": "https://sw.wikipedia.org/wiki/Daniel_arap_Moi",
    },
    "mwai kibaki": {
        "extract": "Mwai Kibaki (1931-2022) was Kenya's third President "
                   "(2002-2013). His government introduced free primary "
                   "education, the Constituency Development Fund, vision 2030 "
                   "and the new 2010 constitution.",
        "url": "https://sw.wikipedia.org/wiki/Mwai_Kibaki",
    },
    "uhuru kenyatta": {
        "extract": "Uhuru Kenyatta (born 1961) was Kenya's fourth President "
                   "(2013-2022), son of Jomo Kenyatta, who oversaw the "
                   "standard-gauge railway (SGR) and big-four agenda. He is now "
                   "a peace envoy in the region.",
        "url": "https://sw.wikipedia.org/wiki/Uhuru_Kenyatta",
    },
    "william ruto": {
        "extract": "William Ruto (born 1966) is Kenya's fifth and current "
                   "President, first elected in 2022, from the Kalenjin "
                   "community of Uasin Gishu. He was previously Deputy "
                   "President (2013-2022).",
        "url": "https://sw.wikipedia.org/wiki/William_Ruto",
    },
    "dedan kimathi": {
        "extract": "Dedan Kimathi (1920-1957) was the most famous leader of the "
                   "Mau Mau uprising against British colonial rule in the 1950s. "
                   "He was captured in 1956, executed in 1957, and is honoured "
                   "as a hero of Kenya's independence struggle.",
        "url": "https://sw.wikipedia.org/wiki/Dedan_Kimathi",
    },
    "tom mboya": {
        "extract": "Tom Mboya (1930-1969) was one of Kenya's most brilliant "
                   "young nationalists and a trade-unionist, an architect of the "
                   "independence constitution and the 'airlift' that sent "
                   "hundreds of Kenyans to US universities. He was assassinated "
                   "in Nairobi in 1969.",
        "url": "https://sw.wikipedia.org/wiki/Tom_Mboya",
    },
    "wangari maathai": {
        "extract": "Wangari Maathai (1940-2011) was a Kenyan environmentalist "
                   "who founded the Green Belt Movement (planting millions of "
                   "trees). In 2004 she became the first African woman to win "
                   "the Nobel Peace Prize.",
        "url": "https://sw.wikipedia.org/wiki/Wangari_Maathai",
    },
    "raila odinga": {
        "extract": "Raila Odinga (born 1945) is a veteran Kenyan opposition "
                   "leader and former Prime Minister (2008-2013). Son of "
                   "independence leader Oginga Odinga, he has contested the "
                   "presidency several times and led major reform coalitions.",
        "url": "https://sw.wikipedia.org/wiki/Raila_Odinga",
    },
    "kipchoge keino": {
        "extract": "Kipchoge Keino (born 1940) is a Kenyan running legend who "
                   "won Olympic gold in Mexico 1968 (1,500 m) and Munich 1972 "
                   "(3,000 m steeplechase), and later headed Kenya's Olympic "
                   "committee.",
        "url": "https://en.wikipedia.org/wiki/Kipchoge_Keino",
    },
    "eliud kipchoge": {
        "extract": "Eliud Kipchoge (born 1984) is Kenya's greatest marathon "
                   "runner: world record 2:01:09 (Berlin 2022), two Olympic "
                   "marathon golds (2016, 2020), and the first human to run the "
                   "marathon under two hours (1:59:40, Vienna 2019).",
        "url": "https://en.wikipedia.org/wiki/Eliud_Kipchoge",
    },

    # -- schools & universities ----------------------------------------------------
    "alliance high school": {
        "extract": "Alliance High School is a national boys' school in Kikuyu, "
                   "Kiambu County, founded in 1926 - the oldest of Kenya's elite "
                   "national schools, alma mater of many of the country's "
                   "leaders and academics.",
        "url": "https://en.wikipedia.org/wiki/Alliance_High_School",
    },
    "mangu high": {
        "extract": "Mang'u High School (Mangu High School) is a national "
                   "Catholic boys' school in Thika, Kiambu County. It produces "
                   "some of Kenya's top KCSE results and many professionals.",
        "url": "https://en.wikipedia.org/wiki/Mangu_High_School",
    },
    "lenana school": {
        "extract": "Lenana School is a national boys' school in Kilimani, "
                   "Nairobi, founded in 1949 and named after the Maasai leader "
                   "Lenana. It is known for strong academics and rugby.",
        "url": "https://en.wikipedia.org/wiki/Lenana_School",
    },
    "kenya high school": {
        "extract": "The Kenya High School is a national girls' school in "
                   "Kileleshwa, Nairobi (founded 1910), consistently among "
                   "Kenya's best-performing schools.",
        "url": "https://en.wikipedia.org/wiki/The_Kenya_High_School",
    },
    "starehe boys": {
        "extract": "Starehe Boys' Centre in Nairobi is a famous charitable "
                   "national school founded in 1959 by Geoffrey Griffin to give "
                   "needy boys a top education - many of Kenya's leaders, "
                   "judges and professionals are alumni.",
        "url": "https://en.wikipedia.org/wiki/Starehe_Boys_Centre_and_School",
    },
    "maseno school": {
        "extract": "Maseno School, near Kisumu, is one of Kenya's oldest "
                   "national schools (founded 1906), historically a church "
                   "school that educated many Luo leaders.",
        "url": "https://en.wikipedia.org/wiki/Maseno_School",
    },
    "kabarak high school": {
        "extract": "Kabarak High School is a national academy school near "
                   "Nakuru, founded in 1985 by President Daniel arap Moi, known "
                   "for prayer, discipline and strong academics.",
        "url": "https://en.wikipedia.org/wiki/Kabarak_High_School",
    },
    "university of nairobi": {
        "extract": "The University of Nairobi (UoN), founded 1970, is Kenya's "
                   "oldest and largest public university, with its main campus "
                   "on the edge of the CBD in Nairobi.",
        "url": "https://en.wikipedia.org/wiki/University_of_Nairobi",
    },
    "jomo kenyatta university": {
        "extract": "Jomo Kenyatta University of Agriculture and Technology "
                   "(JKUAT), in Juja, Kiambu County, is a leading public "
                   "university strong in engineering, technology and "
                   "agriculture.",
        "url": "https://en.wikipedia.org/wiki/Jomo_Kenyatta_University_of_Agriculture_and_Technology",
    },
    "kenyatta university": {
        "extract": "Kenyatta University (KU), in Kahawa, off Thika Road, is "
                   "one of Kenya's largest public universities, founded 1985 "
                   "from a teachers' college.",
        "url": "https://en.wikipedia.org/wiki/Kenyatta_University",
    },

    # -- institutions & landmarks -------------------------------------------------
    "jomo kenyatta international airport": {
        "extract": "Jomo Kenyatta International Airport (JKIA) in Nairobi is "
                   "Kenya's main international airport and the busiest aviation "
                   "hub in East Africa, serving as the base for Kenya Airways.",
        "url": "https://en.wikipedia.org/wiki/Jomo_Kenyatta_International_Airport",
    },
    "fort jesus": {
        "extract": "Fort Jesus in Mombasa, built by the Portuguese in 1593, is "
                   "a UNESCO World Heritage Site and Kenya's most famous "
                   "historical landmark, guarding the old harbour through "
                   "centuries of Omani and British rule.",
        "url": "https://en.wikipedia.org/wiki/Fort_Jesus",
    },
    "kibera": {
        "extract": "Kibera, in Nairobi, is one of Africa's largest informal "
                   "settlements (estimated hundreds of thousands of people), "
                   "famous for its community-led programmes and the railway "
                   "that runs through it.",
        "url": "https://en.wikipedia.org/wiki/Kibera",
    },
    "kicd": {
        "extract": "The Kenya Institute of Curriculum Development (KICD) is the "
                   "state agency in Nairobi that develops and approves Kenya's "
                   "curriculum - currently the Competency Based Curriculum "
                   "(CBC).",
        "url": "https://en.wikipedia.org/wiki/Kenya_Institute_of_Curriculum_Development",
    },
    "kra": {
        "extract": "The Kenya Revenue Authority (KRA) is Kenya's tax-collection "
                   "agency, mandated to assess, collect and account for all "
                   "government revenue (income tax, VAT, customs duty).",
        "url": "https://en.wikipedia.org/wiki/Kenya_Revenue_Authority",
    },
    "kdf": {
        "extract": "The Kenya Defence Forces (KDF) comprise the Kenyan Army, "
                   "Air Force and Navy, under a Chief of Defence Forces. They "
                   "defend Kenya and participate in regional peacekeeping "
                   "(notably in Somalia and the DRC).",
        "url": "https://en.wikipedia.org/wiki/Kenya_Defence_Forces",
    },
    "knec": {
        "extract": "The Kenya National Examinations Council (KNEC) sets and "
                   "administers Kenya's national exams - KCPE, KCSE, and now "
                   "the Competency-Based Assessments (KPSEA, KCSE continues).",
        "url": "https://en.wikipedia.org/wiki/Kenya_National_Examinations_Council",
    },
}

# The 47 counties, newest devolution units of Kenya (2010 constitution).
_KENYA_COUNTIES = (
    "Mombasa", "Kwale", "Kilifi", "Tana River", "Lamu", "Taita-Taveta",
    "Garissa", "Wajir", "Mandera", "Marsabit", "Isiolo", "Meru",
    "Tharaka-Nithi", "Embu", "Kitui", "Machakos", "Makueni", "Nyandarua",
    "Nyeri", "Kirinyaga", "Murang'a", "Kiambu", "Turkana", "West Pokot",
    "Samburu", "Trans Nzoia", "Uasin Gishu", "Elgeyo-Marakwet", "Nandi",
    "Baringo", "Laikipia", "Nakuru", "Narok", "Kajiado", "Kericho",
    "Bomet", "Kakamega", "Vihiga", "Bungoma", "Busia", "Siaya", "Kisumu",
    "Homa Bay", "Migori", "Kisii", "Nyamira", "Nairobi",
)
_KENYA_COUNTIES_LOWER = {c.lower() for c in _KENYA_COUNTIES}


def _title_relevant(title: str, query: str) -> bool:
    """True if a Wikipedia result's title still concerns the query. The
    REST summary endpoint follows redirects, and simple.wikipedia
    sometimes maps a topic onto a *different* article (ngorongoro ->
    Serengeti) when the exact page doesn't exist; sharing at least one
    meaningful token guards against answering with the wrong subject."""
    t = (title or "").lower()
    q = (query or "").lower()
    if not q:
        return True
    q_tokens = {w for w in re.split(r"\W+", q) if len(w) > 1 and w not in _STOPWORDS}
    if not q_tokens:
        return True
    t_tokens = {w for w in re.split(r"\W+", t) if len(w) > 1 and w not in _STOPWORDS}
    shared = q_tokens & t_tokens
    if shared:
        return True
    # fall back to substring containment for names/places ("ngorongoro"
    # in "Ngorongoro Conservation Area", "kibera" in "Kibera Slum").
    for tok in q_tokens:
        if tok in t:
            return True
    return False


def _is_kenyan_query(topic: str):
    """Heuristic: is this query clearly about a Kenyan entity (used to
    bias search/language/news order toward Kenya, never to restrict)."""
    t = topic.strip().lower()
    if not t:
        return False
    tokens = set(re.split(r"\W+", t))
    if "kenya" in tokens or "kenyan" in tokens or "kenyans" in tokens:
        return True
    # county names match as substrings too ("nakuru county").
    for county in _KENYA_COUNTIES_LOWER:
        if county in t:
            return True
    for key in _KENYA_FACTS:
        if key in t:
            return True
    for alias, canonical in _CANONICAL_FACT_ALIASES.items():
        if alias in t and canonical in _KENYA_FACTS:
            return True
    return False


# Wikidata property IDs we know how to read + a friendly label for each
# (used by the structured "fast facts" enrichment in wikidata_facts).
_WIKIDATA_CLAIM_LABELS = {
    "P31": "type",
    "P17": "country",
    "P36": "capital",
    "P1082": "population",
    "P569": "born",
    "P570": "died",
    "P106": "occupation",
    "P27": "citizenship",
    "P131": "located in",
    "P19": "birthplace",
    "P20": "deathplace",
    "P856": "official website",
    "P571": "inception",
    "P112": "founder",
    "P136": "genre",
    "P856": "website",
    "P175": "performer",
    "P57": "director",
    "P161": "starring",
    "P937": "work location",
    "P1416": "affiliation",
}

# View names for common Wikidata instance-of (P31) items, so a country
# or a school reads naturally instead of "instance of: Q6256".
_WIKIDATA_P31_LABELS = {
    "Q6256": "country",
    "Q3918": "girls' school",
    "Q9842": "boys' school",
    "Q10383": "municipality",
    "Q515": "city",
    "Q532": "town",
    "Q486972": "town",
    "Q13442814": "school",
    "Q3914": "school",
    "Q35657": "public school",
    "Q11446": "secondary school",
    "Q159334": "persons / people",
    "Q5": "human",
    "Q16521": "taxon",
    "Q44395": "football club",
    "Q43229": "organisation",
    "Q4830453": "business",
    "Q150": "music",
    "Q11424": "film",
    "Q11460": "book",
    "Q3918": "college",
    "Q18702": "mountain",
    "Q23397": "lake",
    "Q573344": "river",
    "Q40397": "game",
    "Q7187": "gene",
    "Q128342": "disease",
}

# Google News RSS feeds DO need a browser-ish UA and give usable
# headlines with zero API key; links are news.google.com redirects
# (skipped by deep-read via _DOGFOOD_HOSTS).
_GOOGLE_NEWS_RSS = "https://news.google.com/rss/search?q={q}&hl=en-US&gl=US&ceid=US:en"

# Wikidata has no write API for anonymous users - perfect for
# structured facts. Its action=wbgetentities endpoint is key-less.
_WIKIDATA_API = "https://www.wikidata.org/w/api.php"

# OpenStreetMap Nominatim geocoding (free, no key): places.
_NOMINATIM_API = "https://nominatim.openstreetmap.org/search"

# Mojeek is key-less and index-friendly, giving us a 4th engine.
_MOJEEK_PAGE = "https://www.mojeek.com/search"


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
    _WIKTIONARY_HOSTS = {
        "en": "https://en.wiktionary.org",
        "sw": "https://sw.wiktionary.org",
        "fr": "https://fr.wiktionary.org",
    }

    def _wiki_api(self, lang: str, params: dict):
        """Calls a Wikipedia-family action API (en/sw/fr/simple, or
        "quotes" for Wikiquote) with browser-grade UA. Returns a JSON
        dict or an error dict."""
        if lang == "quotes":
            host = self._WIKIQUOTE_HOST
        elif lang == "wiktionary":
            host = self._WIKTIONARY_HOST
        elif lang.startswith("wiktionary-"):
            host = self._WIKTIONARY_HOSTS.get(
                lang.split("-", 1)[1], self._WIKTIONARY_HOST)
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
        """Dictionary definition from the Wiktionary family (en, then the
        Swahili edition for Swahili words), no API key. Returns
        {"title", "extract", "url", "source"} or {"error": str} -
        intended for single words; Kenyan/Swahili words are answered
        from the sw.wiktionary when en has nothing."""
        word = word.strip().lower()
        if not word:
            return {"error": "what word should I define?"}
        for _ed in ("wiktionary", "wiktionary-sw", "wiktionary-fr"):
            data = self._wiki_api(_ed, {
                "action": "query", "prop": "extracts", "explaintext": "1",
                "exintro": "1", "titles": word,
            })
            if "error" in data:
                continue
            pages = data.get("query", {}).get("pages") or []
            page = pages[0] if pages else {}
            extract = page.get("extract") if isinstance(page, dict) else ""
            if not extract:
                continue
            edition = self._WIKTIONARY_HOSTS.get(
                _ed.split("-", 1)[1], self._WIKTIONARY_HOST)
            return {
                "title": page.get("title") or word,
                "extract": _WS_RE.sub(" ", extract).strip()[: _MAX_TEXT_CHARS],
                "url": edition + "/wiki/" + urllib.parse.quote(word.replace(" ", "_")),
                "source": _ed.replace("wiktionary", "Wiktionary"),
            }
        return {"error": f"Wiktionary has no entry for '{word}'"}

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

    def kenya_fact_lookup(self, query: str):
        """Offline, deterministic, Kenya-first lookup from the curated
        factbase. Returns {"title", "extract", "url", "source"} or
        {"error": str}. Also covers the county list, which is a major
        Kenya question ('list the counties of kenya')."""
        topic = query.strip().strip(".").lower()
        if not topic:
            return {"error": "what should I look up?"}
        # "list of counties" special forms - only when the user asks for the
        # list, never for a specific county ("nakuru county" = Nakuru entry).
        _listy = ("list" in topic or "all" in topic or "names" in topic
                  or "how many" in topic or "kaunti" in topic)
        _county_mention = ("county" in topic or "counties" in topic)
        if _listy and _county_mention:
            half = len(_KENYA_COUNTIES) // 2
            cols = "\n".join(
                f"  {a}  |  {b}"
                for a, b in zip(_KENYA_COUNTIES[:half], _KENYA_COUNTIES[half:])
            )
            return {
                "title": "All 47 counties of Kenya",
                "extract": f"Kenya has {len(_KENYA_COUNTIES)} counties (2010 "
                           f"constitution):\n{cols}",
                "url": "https://sw.wikipedia.org/wiki/Mkoa_wa_Kenya",
                "source": "Kenya factbase",
            }
        if topic in _CANONICAL_FACT_ALIASES:
            topic = _CANONICAL_FACT_ALIASES[topic]
        if topic not in _KENYA_FACTS:
            # allow trailing qualifiers: "nakuru county", "nairobi kenya"
            for suffix in (" county", " kenya", " town", " city", " region"):
                if topic.endswith(suffix):
                    base = topic[: -len(suffix)]
                    if base in _KENYA_FACTS:
                        topic = base
                        break
        entry = _KENYA_FACTS.get(topic)
        if not entry:
            return {"error": f"no Kenya factbase entry for '{query}'"}
        return {
            "title": topic.title(),
            "extract": entry["extract"],
            "url": entry["url"],
            "source": "Kenya factbase",
        }

    def wikidata_facts(self, query: str):
        """Structured fact sheet from Wikidata (no API key). Returns
        {"title", "description", "facts": [(label, value), ...]} or
        {"error": str}. Facts are a handful of statements - population,
        country, born/died, occupation, etc. - resolved to labels."""
        try:
            subject = query.strip()
            if not subject:
                return {"error": "what should I look up?"}
            # 1) resolve the enwiki title to a Wikidata entity id
            url = (_WIKIDATA_API + "?action=wbgetentities&sites=enwiki&titles="
                   + urllib.parse.quote(subject) + "&props=labels|descriptions"
                     "&languages=en&format=json&formatversion=2")
            raw = _fetch_html_ua(url, timeout=self.timeout_seconds, headers=_WEB_UA)
            if isinstance(raw, dict):
                return {"error": raw["error"]}
            data = json.loads(_decode(raw))
            ent = data.get("entities") or {}
            entity = None
            for eid, ent_data in ent.items():
                if eid != "-1" and ent_data and ent_data.get("id"):
                    entity = ent_data
                    break
            if not entity or (entity.get("missing") and not entity.get("claims")):
                return {"error": f"no Wikidata entry for '{subject}'"}
            entity_id = entity["id"]
            if "claims" not in entity:
                # labels-only probe above; fetch claims now
                url = (_WIKIDATA_API + "?action=wbgetentities&ids=" + entity_id
                       + "&props=claims&format=json&formatversion=2")
                raw = _fetch_html_ua(url, timeout=self.timeout_seconds, headers=_WEB_UA)
                if isinstance(raw, dict):
                    return {"error": raw["error"]}
                data = json.loads(_decode(raw))
                entity = (data.get("entities") or {}).get(entity_id, {})
            claims = entity.get("claims") or {}
            if not claims:
                return {"error": f"no structured facts for '{subject}'"}
            # 2) batch-resolve referenced entity values to English labels
            ref_ids = set()
            picked = []
            for pid, label in _WIKIDATA_CLAIM_LABELS.items():
                for claim in claims.get(pid, [])[:1]:
                    v = claim.get("mainsnak", {}).get("datavalue", {})
                    if not v:
                        continue
                    if v.get("type") == "wikibase-entityid":
                        ref = v["value"]["id"]
                        if ref in _WIKIDATA_P31_LABELS:
                            picked.append((label, _WIKIDATA_P31_LABELS[ref]))
                        else:
                            ref_ids.add(ref)
                            # placeholder filled after batch resolve
                            picked.append((label, ref + "\x00"))
                    elif v.get("type") == "time":
                        dt = v["value"]["time"]
                        picked.append((label, dt[1:5] if len(dt) >= 5 else dt))
                    elif v.get("type") == "quantity":
                        amt = v["value"]["amount"]
                        try:
                            picked.append((label, f"{int(float(amt)):,}"))
                        except (ValueError, TypeError):
                            picked.append((label, amt))
                    else:
                        picked.append((label, str(v.get("value", ""))))
            resolved = {}
            if ref_ids:
                url = (_WIKIDATA_API + "?action=wbgetentities&ids="
                       + "|".join(sorted(ref_ids)[:50])
                       + "&props=labels&languages=en&format=json&formatversion=2")
                raw = _fetch_html_ua(url, timeout=self.timeout_seconds, headers=_WEB_UA)
                if not isinstance(raw, dict):
                    data = json.loads(_decode(raw))
                    for eid, ent_data in (data.get("entities") or {}).items():
                        resolved[eid] = (ent_data.get("labels") or {}).get("en", {}).get("value", eid)
            facts = []
            seen_ids = set()
            for label, value in picked:
                if value.endswith("\x00"):
                    ref_id = value[:-1]
                    value = resolved.get(ref_id, ref_id)
                if value.endswith("\x00"):
                    value = value[:-1]
                facts.append((label, value))
            # drop placeholder resolution junk
            facts = [(l, v) for l, v in facts if v and "\x00" not in v]
            if not facts:
                return {"error": f"no readable facts for '{subject}'"}
            return {
                "title": (entity.get("labels") or {}).get("en", {}).get("value") or subject.title(),
                "description": (entity.get("descriptions") or {}).get("en", {}).get("value", ""),
                "facts": facts,
            }
        except (json.JSONDecodeError, ValueError):
            return {"error": "couldn't parse the structured-facts result"}
        except Exception as e:  # fail-closed, never raise
            return {"error": f"structured facts unavailable ({e})"}

    def news_search(self, query: str, limit: int = 6, kenyan: bool = None):
        """Fresh headlines from Google News RSS (no API key). Kenyan
        queries get the Swahili Kenya edition by default. Returns a
        results list, or None when the feed is unreachable."""
        if kenyan is None:
            kenyan = _is_kenyan_query(query)
        if kenyan:
            hl_gl = "hl=sw&gl=KE&ceid=KE:sw"
        else:
            hl_gl = "hl=en-US&gl=US&ceid=US:en"
        url = ("https://news.google.com/rss/search?q=" + urllib.parse.quote(query)
               + "&" + hl_gl)
        raw = _fetch_html_ua(url, timeout=self.timeout_seconds, headers=_WEB_UA)
        if isinstance(raw, dict):
            return None
        html = _decode(raw)
        # parse RSS <item> blocks with stdlib (feedparser not installed)
        items = re.findall(
            r"<item>(.*?)</item>", html, flags=re.IGNORECASE | re.DOTALL)
        results = []
        for block in items[:limit]:
            title_m = re.search(r"<title>(.*?)</title>", block, re.IGNORECASE | re.DOTALL)
            link_m = re.search(r"<link>(.*?)</link>", block, re.IGNORECASE | re.DOTALL)
            if not title_m or not link_m:
                continue
            title = re.sub(r"<[^>]+>", "", title_m.group(1)).strip()
            link = link_m.group(1).strip()
            if not title or not link:
                continue
            results.append({
                "title": title[:120],
                "snippet": "(news)" if False else title[:120],
                "url": link,
            })
            if len(results) >= limit:
                break
        return results or None

    def place_lookup(self, query: str):
        """OpenStreetMap Nominatim lookup for places. Kenyan queries are
        tried against Kenya first, then the whole world. Returns
        {"title", "extract", "url", "source"} making clear it is a
        place, or {"error": str}."""
        # Nominatim will happily match a single short lowercase word to
        # some unrelated settlement anywhere on Earth ('heri' -> a
        # village in Lebanon) - for plain words that are not Kenyan we
        # skip straight to web search, which is far more honest.
        tq = query.strip()
        if (not _is_kenyan_query(tq) and len(tq) > 2 and len(tq) < 20
                and tq == tq.lower() and not any(ch.isspace() for ch in tq)):
            return {"error": f"'{query}' does not look like a place"}
        try:
            kenyan = _is_kenyan_query(query)
            candidates = [("KE", "Kenya")] if kenyan else []
            candidates.append((None, "the world"))
            for cc, label in candidates:
                base = (_NOMINATIM_API + "?q=" + urllib.parse.quote(query)
                        + "&format=jsonv2&limit=1&accept-language=en")
                if cc:
                    base = base + "&countrycodes=" + cc
                raw = _fetch_html_ua(
                    base, timeout=self.timeout_seconds, headers=_WEB_UA)
                if isinstance(raw, dict):
                    continue
                data = json.loads(_decode(raw))
                if isinstance(data, list) and data and isinstance(data[0], dict):
                    hit = data[0]
                    display = hit.get("display_name", "") or query
                    ptype = (hit.get("type") or "place").replace("_", " ")
                    extra = ""
                    if hit.get("extratags"):
                        weg = hit["extratags"].get("website")
                        if weg:
                            extra = f" Website: {weg}."
                    return {
                        "title": f"{query.title()} ({ptype} in Kenya)"
                                 if cc else f"{query.title()} ({ptype})",
                        "extract": (
                            f"{display}.{extra} Coordinate: lat "
                            f"{hit.get('lat', '?')}, lon {hit.get('lon', '?')}."
                        ),
                        "url": (
                            f"https://www.openstreetmap.org/?mlat={hit.get('lat')}"
                            f"&mlon={hit.get('lon')}#map=13/{hit.get('lat')}/{hit.get('lon')}"
                        ),
                        "source": f"OpenStreetMap ({label})",
                    }
            return {"error": f"no place found for '{query}'"}
        except (json.JSONDecodeError, ValueError):
            return {"error": "couldn't parse the place-lookup result"}
        except Exception as e:
            return {"error": f"place lookup unavailable ({e})"}

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
        """Deep, Kenya-centralized multi-source lookup. Walks, in order:
          0. Kenya factbase (offline, instant, always-correct)
          1. Wikipedia REST summaries - language order depends on
             whether the query is Kenyan (sw first) or not
          2. Wikipedia title search -> full extract of the match
          3. Deep full-article extracts (en, then sw)
          4. Wiktionary (words & phrases) and Wikiquote (people)
          5. Common Swahili/French phrases -> curated dictionary
          6. OpenStreetMap place lookup (Kenya-first filtering)
          7. Merged web search (DuckDuckGo + lite + Bing + Mojeek) +
             recent Google News, with a deep multi-page read of the
             best live pages, attributed per source.
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

        # 0) Kenya factbase - instant, offline, deterministic.
        fact = self.kenya_fact_lookup(topic)
        if "error" not in fact:
            return fact

        # 0b) Curated Swahili/French phrase dictionary also answers
        # instantly and is verified, so it must come BEFORE Wikipedia:
        # otherwise 'karibu' would return a random unrelated article
        # ('Karibu Airways' airline) instead of 'welcome'.
        _key = topic.strip().lower()
        _trans = _TRANSLATIONS.get(_key)
        if _trans:
            _pl = _guess_phrase_lang(_key) or (
                "sw" if _key in _SW_PHRASES else "fr")
            return {
                "title": _trans[0],
                "extract": f"'{topic}' is {_pl} for '{_trans[0]}'.",
                "url": "https://en.wiktionary.org",
                "source": "translation",
            }

        kenyan = _is_kenyan_query(topic)
        langs = (self._WIKI_LANGS[0], self._WIKI_LANGS[1])  # keep default
        # Kenya-first language ordering: Swahili Wikipedia has the most
        # substance on East African topics, but only for Kenyan topics -
        # "homestuck" stays on simple/en so we don't answer with a stub.
        if kenyan:
            langs = (self._WIKI_LANGS[2], self._WIKI_LANGS[0])  # sw, simple
        rest_langs = tuple(l for l in self._WIKI_LANGS if l not in langs)

        # 1) Wikipedia REST summaries: probe the first two IN PARALLEL (a slow
        #    miss on one never blocks a fast hit - e.g. 'serendipity'),
        #    and only reach for the others if both missed. Two-at-a-time
        #    keeps Wikipedia happy and throttling-free.
        try:
            import concurrent.futures as _cf
            with _cf.ThreadPoolExecutor(max_workers=2) as pool:
                for grp in (langs, rest_langs[:2], rest_langs[2:]):
                    if not grp or _out_of_budget():
                        break
                    futures = {pool.submit(self.wikipedia_summary, topic, lang): lang
                               for lang in grp}
                    for fut in _cf.as_completed(futures):
                        try:
                            first = fut.result()
                        except Exception:
                            continue
                        if ("error" not in first and first.get("extract")
                                and _title_relevant(first.get("title"), topic)):
                            return first
            # if all probes missed but one looked "close", the phase
            # search below still rescues via a loose title match.
        except Exception:
            # threads unavailable - fall back to sequential probing
            for lang in (langs + rest_langs):
                first = self.wikipedia_summary(topic, lang=lang)
                if ("error" not in first and first.get("extract")
                        and _title_relevant(first.get("title"), topic)):
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
        key = topic.strip().lower()
        trans = _TRANSLATIONS.get(key)
        if trans:
            if not lang:
                lang = "sw" if key in _SW_PHRASES else "fr"
            return {
                "title": trans[0],
                "extract": (f"'{topic}' is {lang} for "
                            f"'{trans[0]}'."),
                "url": "https://en.wiktionary.org",
                "source": "translation",
            }

        # 5) OpenStreetMap place lookup - Kenya-first filtering for
        #    Kenyan-sounding topics, world-wide otherwise. Only reached
        #    when the factbase/Wikipedia side has already failed, so it
        #    mainly rescues small towns, market centres, rivers etc.
        if not _out_of_budget():
            place = self.place_lookup(topic)
            if "error" not in place:
                return place

        # 6) Wide web search (multiple engines, merged + deduped), with
        #    recent Google News folded in when there's room - so current
        #    Kenyan stories surface alongside evergreen pages.
        web = self.web_search(topic, limit=8)
        if "error" in web:
            return web
        news = self.news_search(topic, limit=4)
        if news:
            known = {urllib.parse.unquote(r["url"]).lower() for r in web["results"]}
            for n in news:
                if urllib.parse.unquote(n["url"]).lower() not in known:
                    n["via"] = "news"
                    web["results"].append(n)

        # 7) DEPTH: read the top result pages themselves - real answers,
        #    not just headlines. Wikipedia URLs get the clean extract API
        #    treatment (their HTML is navigation-heavy); everything else
        #    uses the plain-text reader. Up to two successful page reads,
        #    scanning past the engines' own redirect pages. No dogfood.
        reads_left = 2
        collected = []  # (char_count, dict) for possible merge
        for item in web["results"][:6]:
            if reads_left <= 0:
                break
            url = item["url"]
            host = (url.split("//", 1)[-1].split("/", 1)[0] if "//" in url else "").lower()
            if host in _DOGFOOD_HOSTS or item.get("via") == "news":
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
                    collected.append((len(cand["extract"]), {
                        "title": f"{cand['title']} ({url})",
                        "extract": cand["extract"],
                        "url": url,
                    }))
                continue
            page = self.read_page(url)
            if "error" not in page and page.get("summary"):
                collected.append((len(page["summary"]), {
                    "title": f"{page['title']} ({url})",
                    "extract": page["summary"],
                    "url": url,
                }))

        if collected:
            # richest page is the main answer; a second good read gets
            # appended as a short "also from" tail.
            collected.sort(key=lambda pair: -pair[0])
            main = collected[0][1]
            out = dict(main)
            out["urls"] = [r["url"] for r in web["results"]]
            out["source"] = "web search (deep read)"
            if len(collected) > 1:
                second = collected[1][1]
                tail = _WS_RE.sub(" ", second["extract"]).strip()
                if tail:
                    out["extract"] = (main["extract"] + "\n\nAlso from "
                                      + second["title"].split(" (")[0] + ": "
                                      + tail[:_MAX_TEXT_CHARS // 2])
            return out

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

    def mojeek_search(self, query: str, limit: int = 8):
        """Mojeek - a key-less, private, index-friendly engine (no
        region bias controls, but adds engine diversity). Returns a
        results list or [] when it can't be parsed."""
        params = urllib.parse.urlencode({"q": query})
        raw = _fetch_html_ua(_MOJEEK_PAGE + "?" + params,
                             timeout=self.timeout_seconds, headers=_WEB_UA)
        if isinstance(raw, dict):
            return []
        html = _decode(raw)
        results = []
        if BS4_AVAILABLE:
            soup = BeautifulSoup(html, "html.parser")
            for li in soup.select("li.result, li.standard, ul.results-standard li"):
                a = li.select_one("h2 a, .title a, a[href^='http']")
                if a is None:
                    continue
                href = a.get("href", "")
                title = a.get_text(" ", strip=True)
                p = li.select_one("p.s") or li.select_one(".summary") or li.select_one("p")
                snippet = p.get_text(" ", strip=True) if p else ""
                if href.startswith("http") and title:
                    results.append({"title": title[:80], "snippet": snippet[:200], "url": href})
                if len(results) >= limit:
                    break
        else:
            for m in re.finditer(
                r'<li[^>]*class="[^"]*result[^"]*".*?<a[^>]*href="([^"]+)"[^>]*>(.*?)</a>',
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