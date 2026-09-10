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


# ---------------------------------------------------------------------------
# Mega factbase: every county follows a structured profile so the same
# facts (capital, county code, governor) and the generated per-county
# entries never contradict each other. County code = position in the
# official 2013 numbering (Mombasa 001 ... Nairobi 047).
#
#   key: (county_code, capital, region, notable_towns, note, governor)
# ---------------------------------------------------------------------------
_KENYA_COUNTY_PROFILES = {
    "mombasa": (1, "Mombasa City", "Coast",
                ("Mombasa", "Nyali", "Bamburi", "Likoni"),
                "Kenya's historic port and old Swahili capital: Fort Jesus, the "
                "Old Town, Diani-side beaches (across the ferry), and Mombasa "
                "Marine National Park.",
                "Abdullswamad Sheriff Nassir"),
    "kwale": (2, "Kwale town", "Coast",
              ("Diani", "Ukunda", "Kwale"),
              "Coastal county south of Mombasa: Diani and Tiwi beaches, Shimba "
              "Hills National Reserve (elephants, sable antelope) and the Digo "
              "people.",
              "Fatuma Achani"),
    "kilifi": (3, "Kilifi town", "Coast",
               ("Kilifi", "Malindi", "Watamu", "Mariakani"),
              "Coastal county north of Mombasa: Mnarani and Gede ruins, the "
              "UNESCO Kaya forests, Watamu Marine Park, Arabuko-Sokoke Forest "
              "and the Malindi coast.",
              "Gideon Mung'aro"),
    "tana river": (4, "Hola", "Coast",
                   ("Hola", "Garsen", "Ngao"),
                   "Dry county along Kenya's longest river with Tana Delta "
                   "floodplains, huge sisal estates and the Pokomo and Orma "
                   "peoples.",
                   "Dhadho Godhana"),
    "lamu": (5, "Lamu town", "Coast",
             ("Lamu", "Shela", "Manda", "Faza"),
             "Island county on the north coast: Lamu Old Town and the Lamu "
             "archipelago (UNESCO), dhow culture, Swahili architecture and the "
             "Maulidi festival.",
             "Issa Timamy"),
    "taita-taveta": (6, "Voi", "Coast",
                     ("Voi", "Taveta", "Wundanyi"),
                     "County on the Tanzanian border that hosts most of Tsavo "
                     "East and West national parks, the Taita Hills and "
                     "saltlick/lake lodges around Taveta.",
                     "Andrew Mwadime"),
    "garissa": (7, "Garissa town", "North Eastern",
                ("Garissa", "Ijara", "Bura"),
                "County on the lower Tana River and the gateway to Kenya's "
                "Somali-speaking north-east, built on riverine and pastoral "
                "economies.",
                "Nathif Jama"),
    "wajir": (8, "Wajir town", "North Eastern",
              ("Wajir", "Eldas", "Griftu"),
              "Huge semi-arid county bordering Somalia, one of Kenya's largest "
              "and sparsest; pastoralist heartland.",
              "Ahmed Abdullahi"),
    "mandera": (9, "Mandera town", "North Eastern",
                ("Mandera", "Elwak", "Rhamu"),
                "Kenya's northernmost county, the remote 'three-nation finger' "
                "where Kenya, Ethiopia and Somalia meet.",
                "Mohamed Adan Khalif"),
    "marsabit": (10, "Marsabit town", "Eastern",
                 ("Marsabit", "Moyale", "Solor"),
                 "Counting in its misty volcanic mountains and the fossil-rich "
                 "shores of Lake Turkana - part of the Cradle of Mankind.",
                 "Mohamud Ali"),
    "isiolo": (11, "Isiolo town", "Eastern",
               ("Isiolo", "Garbatulla"),
               "Gateway to northern Kenya on the LAPSSET corridor; Buffalo "
               "Springs and Shaba reserves sit at its north end.",
               "Abdi Guyo"),
    "meru": (12, "Meru town", "Eastern",
             ("Meru", "Maua", "Nkubu"),
             "On the north-eastern slopes of Mount Kenya - tea, coffee and "
             "miraa, plus Meru National Park and the Nyambene Hills.",
             "Kawira Mwangaza"),
    "tharaka-nithi": (13, "Kathwana", "Eastern",
                      ("Chuka", "Kathwana", "Marimanti"),
                      "Along the eastern flank of Mount Kenya - tea, coffee and "
                      "the Chuka and Mwimbi peoples; HQ Kathwana.",
                      "Muthomi Njuki"),
    "embu": (14, "Embu town", "Eastern",
             ("Embu", "Runyenjes"),
             "Arable county on Mount Kenya's southern slopes - coffee, tea, "
             "miraa and the Mwea rice scheme.",
             "Cecily Mbarire"),
    "kitui": (15, "Kitui town", "Eastern",
              ("Kitui", "Mwingi"),
              "Large semi-arid county east of Nairobi - baobab trees, Mwingi "
              "town and recent gold-mining finds.",
              "Julius Malombe"),
    "machakos": (16, "Machakos town", "Eastern",
                 ("Machakos", "Kangundo", "Mavoko"),
                 "Fast-growing county south-east of Nairobi - the Machakos "
                 "Hills, the first colonial capital, and booming satellite "
                 "towns like Athi River (Mavoko).",
                 "Wavinya Ndeti"),
    "makueni": (17, "Wote", "Eastern",
                ("Wote", "Makueni", "Kibwezi"),
                "Agro-pastoral county in Ukambani - honey, mangoes and macadamia "
                "around Wote and the Kibwezi highlands.",
                "Mutula Kilonzo Jr"),
    "nyandarua": (18, "Ol Kalou", "Central",
                  ("Ol Kalou", "Nyahururu", "Mipango"),
                  "Cool highland county on the Aberdare Range - potatoes, dairy "
                  "and the old 'Happy Valley' around Nyeri's doorstep.",
                  "Moses Badilisha Kiarie"),
    "nyeri": (19, "Nyeri town", "Central",
              ("Nyeri", "Othaya", "Karatina"),
              "At the foot of Mount Kenya - the Aberdares, coffee, and the "
              "final resting place of Jomo Kenyatta and Dedan Kimathi; "
              "gateway to the mountain.",
              "Mutahi Kahiga"),
    "kirinyaga": (20, "Kerugoya (Kutus)", "Central",
                  ("Kerugoya", "Kutus", "Sagana"),
                  "Compact Mount Kenya county - Mwea rice, tea, and the home "
                  "county of President Mwai Kibaki.",
                  "Anne Waiguru"),
    "murang'a": (21, "Murang'a town", "Central",
                 ("Murang'a", "Kangema", "Maragua"),
                 "On Mount Kenya's slopes - tea, coffee and avocado country, "
                 "and a historic centre of Gikuyu migration.",
                 "Irungu Kang'ata"),
    "kiambu": (22, "Kiambu town", "Central",
               ("Kiambu", "Ruiru", "Limuru", "Gatundu"),
               "Dynamic county just north of Nairobi - Thika Road industries, "
               "Ruiru university town, Limuru tea and Gatundu, home of the "
               "Kenyattas.",
               "Kimani Wamatangi"),
    "turkana": (23, "Lodwar", "Rift Valley",
                ("Lodwar", "Kakuma", "Loiyangalani"),
                "Kenya's second-largest county - the Jade Sea (Lake Turkana), "
                "desert, the Turkana people, Kakuma refugee camp and "
                "Loiyangalani's wind power.",
                "Jeremiah Lomorukai"),
    "west pokot": (24, "Kapenguria", "Rift Valley",
                   ("Kapenguria", "Chepareria"),
                   "Rugged county on the Uganda border - the Kapenguria trial "
                   "of the Kapenguria Six, Pokot highlands and the Wei Wei "
                   "valley.",
                   "Simon Kachapin"),
    "samburu": (25, "Maralal", "Rift Valley",
                ("Maralal", "Archers Post", "Baragoi"),
                "Semi-arid county north of Mount Kenya - Samburu National "
                "Reserve's 'special five', the Ewaso Ng'iro and Maralal town.",
                "Jonathan Lati Lelelit"),
    "trans nzoia": (26, "Kitale", "Rift Valley",
                    ("Kitale", "Kiminini"),
                    "Arable 'granary' county - Kitale, the maize belt, the "
                    "Suam/Tororo border gate and the foothills of Mount Elgon.",
                    "George Natembeya"),
    "uasin gishu": (27, "Eldoret", "Rift Valley",
                    ("Eldoret", "Turbo", "Moiben"),
                    "North Rift highland 'home of champions' - Eldoret, "
                    "long-distance running legends, dairying and an "
                    "international airport.",
                    "Jonathan Bii"),
    "elgeyo-marakwet": (28, "Iten", "Rift Valley",
                        ("Iten", "Tambach", "Kapsowar"),
                        "The Kerio valley escarpment county - Iten, the "
                        "world-famous training town of steeplechase champions, "
                        "Cherangany hills and the Rimoi reserve.",
                        "Wesley Rotich"),
    "nandi": (29, "Kapsabet", "Rift Valley",
              ("Kapsabet", "Nandi Hills", "Mosoriot"),
              "North Rift county of forests and tea - Kapsabet, Nandi Hills "
              "and the homeland of Kipchoge Keino's running heritage.",
              "Stephen Sang"),
    "baringo": (30, "Kabarnet", "Rift Valley",
                ("Kabarnet", "Marigat", "Eldama Ravine"),
                "Rift Valley county around Lakes Baringo and Bogoria - "
                "flamingos, hot springs, Tugen hills and the home turf of "
                "Daniel arap Moi.",
                "Benjamin Cheboi"),
    "laikipia": (31, "Nanyuki", "Rift Valley",
                 ("Nanyuki", "Rumuruti", "Ngarua"),
                 "The Laikipia Plateau - Nanyuki at Mount Kenya's foot, big "
                 "game conservancies (Ol Pejeta, Lewa) and ranching.",
                 "Joshua Irungu"),
    "nakuru": (32, "Nakuru town", "Rift Valley",
               ("Nakuru", "Naivasha", "Molo", "Gilgil"),
               "Rift Valley hub - Lake Nakuru's flamingos, Naivasha's flower "
               "farms, the Menengai Crater and the Great Rift escarpment "
               "views.",
               "Susan Kihika"),
    "narok": (33, "Narok town", "Rift Valley",
              ("Narok", "Kilgoris", "Mai Mahiu"),
              "The Maasai county of the Mara - Maasai Mara National Reserve, "
              "the annual wildebeest migration and Maasai culture.",
              "Patrick Ntutu"),
    "kajiado": (34, "Kajiado town", "Rift Valley",
                ("Kajiado", "Kitengela", "Namanga", "Ngong"),
                "Maasai county south of Nairobi - Amboseli below Kilimanjaro, "
                "the Namanga border post, Kitengela sprawl and Lake Magadi's "
                "soda flats.",
                "Joseph Ole Lenku"),
    "kericho": (35, "Kericho town", "Rift Valley",
                ("Kericho", "Litein", "Londiani"),
                "Kenya's tea heartland - vast tawny estates roll across these "
                "highlands, the source of a large share of the world's black "
                "tea.",
                "Erick Mutai Kipkoech"),
    "bomet": (36, "Bomet town", "Rift Valley",
              ("Bomet", "Sotik", "Longisa"),
              "South Rift highland county - tea, pyrethrum and Kipsigis "
              "heartland around Bomet and Sotik.",
              "Hillary Barchok"),
    "kakamega": (37, "Kakamega town", "Western",
                 ("Kakamega", "Mumias", "Butere"),
                 "Western county of the Luhya peoples - the beautiful Kakamega "
                 "Forest (Kenya's last tropical rainforest), sugar belt and "
                 "Mumias.",
                 "Fernandes Barasa"),
    "vihiga": (38, "Vihiga (Mbale)", "Western",
               ("Mbale", "Vihiga", "Maji Mazuri"),
               "Tiny, densely populated western county - rolling Maragoli "
               "hills, tea and a famously educated population.",
               "Wilber Ottichilo"),
    "bungoma": (39, "Bungoma town", "Western",
                ("Bungoma", "Webuye", "Kimilili"),
                "Western county on Uganda's doorstep - Bukusu heartland, the "
                "Webuye paper/sugar mills and Mount Elgon's slopes.",
                "Kenneth Lusaka"),
    "busia": (40, "Busia town", "Western",
              ("Busia", "Malaba", "Nambale"),
              "Border county - the busy Busia and Malaba crossings into "
              "Uganda, Lake Victoria's shores and cross-border trade.",
              "Paul Otuoma"),
    "siaya": (41, "Siaya town", "Nyanza",
              ("Siaya", "Bondo", "Ugenya"),
              "Luo heartland on Lake Victoria - the home counties of Jaramogi "
              "Oginga Odinga and Raila Odinga.",
              "James Orengo"),
    "kisumu": (42, "Kisumu city", "Nyanza",
               ("Kisumu", "Ahero", "Muhoroni"),
               "Lakeside commercial hub - Kisumu city and port on Lake "
               "Victoria, the Dunga boardwalk, and Nyanza's rice and sugar "
               "lands.",
               "Anyang' Nyong'o"),
    "homa bay": (43, "Homa Bay town", "Nyanza",
                 ("Homa Bay", "Mbita", "Oyugis"),
                 "Around the great bay of Lake Victoria - Mbita, Ruma National "
                 "Park, Rusinga Island and the airlift-era home of Tom Mboya.",
                 "Gladys Wanga"),
    "migori": (44, "Migori town", "Nyanza",
               ("Migori", "Isebania", "Kehancha"),
               "South-western county bordering Tanzania - the Isebania border, "
               "sugarcane and the Kisii-Kuria lands.",
               "Ochillo Ayacko"),
    "kisii": (45, "Kisii town", "Nyanza",
              ("Kisii", "Tabaka", "Suneka"),
              "Highland Abagusii county - bananas, tea and the soapstone "
              "carving town of Tabaka.",
              "Simba Arati"),
    "nyamira": (46, "Nyamira town", "Nyanza",
                ("Nyamira", "Keroka"),
                "Small, fertile highland county in Gusiiland - tea, bananas "
                "and dramatic green ridges.",
                "Amos Nyaribo"),
    "nairobi": (47, "Nairobi city", "Nairobi",
                ("Nairobi", "Karen", "Lang'ata", "Eastleigh"),
                "Kenya's capital county - the only county that is also a city, "
                "hosting the CBD, JKIA, Nairobi National Park and Africa's "
                "major UN hub.",
                "Johnson Sakaja"),
}


def _mk_county_fact(name, code, capital, region, towns, note, governor):
    """Builds a factbase entry for one county from its structured
    profile, so the county list, the capital/governor mini-question
    answers and the plain lookups never disagree."""
    town_line = "".join(f" {t}," for t in towns).rstrip(",")
    gov_line = f" Governor (2022 election): {governor}." if governor else ""
    return {
        "extract": (
            f"{capital.capitalize()} is the capital of {name} County "
            f"(county code {code:03d}, {region} Kenya).{gov_line}"
            f" Notable places: {town_line}. {note}"
        ),
        "url": ("https://en.wikipedia.org/wiki/"
                + urllib.parse.quote(f"{name} County".replace("\\_", "_"))),
    }


for _cname, (_code, _cap, _reg, _towns, _note, _gov) in _KENYA_COUNTY_PROFILES.items():
    _KENYA_FACTS[_cname] = _mk_county_fact(
        _cname, _code, _cap, _reg, _towns, _note, _gov)
    # the county name doubles as an alias for its own entry
    _CANONICAL_FACT_ALIASES.setdefault(_cname, _cname)
    _pos_top = [t.lower() for t in _towns]
    for _t in _pos_top:
        # town -> its county, but never overwrite a real standalone
        # entry or a more specific alias already in place.
        if _t not in _KENYA_FACTS and _t not in _KENYA_COUNTIES_LOWER:
            _CANONICAL_FACT_ALIASES.setdefault(_t, _cname)

# The county alphabet itself has no standalone entry; point its name at
# the profile, and keep the old self-alias harmless.
for _cnt in _KENYA_COUNTIES_LOWER:
    if _cnt not in _KENYA_FACTS:
        _CANONICAL_FACT_ALIASES[_cnt] = _cnt

# Distinct capital towns of counties that don't share their county name.
_CAPITAL_ALIASES = {
    "kitale": "trans nzoia", "kapenguria": "west pokot",
    "iten": "elgeyo-marakwet", "kabarnet": "baringo",
    "kapsabet": "nandi", "kathwana": "tharaka-nithi",
    "voi": "taita-taveta", "hola": "tana river",
    "kerugoya": "kirinyaga", "kutus": "kirinyaga",
    "rumuruti": "laikipia", "mbale": "vihiga",
    "lodwar": "turkana", "maralal": "samburu",
    "ol kalou": "nyandarua", "wote": "makueni",
    "eldoret town": "uasin gishu",
}
_CANONICAL_FACT_ALIASES.update(_CAPITAL_ALIASES)

# Reverse town -> county index for the 'which/where is X' Q&A: every
# town AND capital named in a county profile maps to that county, so
# answers like "where is nanyuki" work even when the town has no
# factbase entry of its own.
_TOWN_INDEX = {}
for _cname, (_code, _cap, _reg, _towns, _note, _gov) in _KENYA_COUNTY_PROFILES.items():
    for _t in list(_towns) + [_cap]:
        _TOWN_INDEX.setdefault(str(_t).lower(), _cname)


# ---------------------------------------------------------------------------
# The rest of the mega factbase, in themed blocks.
# ---------------------------------------------------------------------------
_EXTRA_KENYA_FACTS = {
    # -- national symbols ----------------------------------------------------
    "kenya flag": {
        "extract": "Kenya's flag (adopted 1963) has black (the people), red "
                   "(the blood of independence), and green (the land and "
                   "agriculture) horizontal stripes with white fimbriations "
                   "(peace and unity), centred on a Maasai shield with crossed "
                   "spears.",
        "url": "https://en.wikipedia.org/wiki/Flag_of_Kenya",
    },
    "kenya anthem": {
        "extract": "Kenya's national anthem, 'Ee Mungu Nguvu Yetu' (Oh God of "
                   "All Creation), was composed by a Kenyan team in Swahili and "
                   "adopted at independence in 1963 - one of the first national "
                   "anthems to be specially commissioned rather than borrowed.",
        "url": "https://en.wikipedia.org/wiki/National_anthem_of_Kenya",
    },
    "motto of kenya": {
        "extract": "Kenya's national motto is 'Harambee' - Swahili for 'let's "
                   "all pull together' - adopted as the rallying idea of "
                   "nation-building in 1963.",
        "url": "https://en.wikipedia.org/wiki/Harambee",
    },
    "harambee": {
        "extract": "Harambee (Swahili: 'all pull together') is Kenya's motto "
                   "and a self-help tradition where communities pool labour "
                   "and money for schools, clinics, harambee projects and "
                   "fundraisers.",
        "url": "https://en.wikipedia.org/wiki/Harambee",
    },
    "kenya independence": {
        "extract": "Kenya became independent on 12 December 1963 (now Jamhuri "
                   "Day, the national holiday) and a republic on 12 December "
                   "1964 under first President Jomo Kenyatta. Madaraka Day on "
                   "1 June remembers internal self-rule from 1963.",
        "url": "https://en.wikipedia.org/wiki/Jamhuri_Day",
    },
    "mau mau": {
        "extract": "The Mau Mau uprising (1952-1960) was Kenya's armed "
                   "resistance to British colonial rule, strongest in the "
                   "Central Highlands and Aberdares. It forced the "
                   "independence negotiations and is remembered through its "
                   "leader Dedan Kimathi and the detainees of Kapenguria and "
                   "Manyani.",
        "url": "https://en.wikipedia.org/wiki/Mau_Mau_uprising",
    },
    "swahili coast": {
        "extract": "The Swahili Coast has traded across the Indian Ocean for "
                   "over a thousand years - city-states like Mombasa, Malindi, "
                   "Pate and Lamu knitted African, Arab, Persian and Indian "
                   "influences into the Swahili language and culture, distinct "
                   "from the inland world.",
        "url": "https://en.wikipedia.org/wiki/Swahili_coast",
    },
    "fort jesus": {
        "extract": "Fort Jesus in Mombasa, built by the Portuguese in 1593, is "
                   "a UNESCO World Heritage Site and Kenya's most famous "
                   "historical landmark, guarding the old harbour through "
                   "centuries of Omani and British rule.",
        "url": "https://en.wikipedia.org/wiki/Fort_Jesus",
    },
    "gede ruins": {
        "extract": "The Gede Ruins near Malindi are the remains of a wealthy "
                   "13th-century Swahili town abandoned in the 17th century - "
                   "stone houses, a mosque and palace within a giant coconut "
                   "and baobab forest.",
        "url": "https://en.wikipedia.org/wiki/Gede,_Kenya",
    },
    "thimlich ohinga": {
        "extract": "Thimlich Ohinga in Migori County is a dry-stone-walled "
                   "settlement (the name means 'frightening dense forest' in "
                   "Dholuo), built from around the 16th century and now a "
                   "UNESCO World Heritage Site.",
        "url": "https://en.wikipedia.org/wiki/Thimlich_Ohinga",
    },
    "koobi fora": {
        "extract": "Koobi Fora on the eastern shore of Lake Turkana is one of "
                   "the world's richest fossil sites of early human ancestors - "
                   "part of Kenya's 'Cradle of Mankind' along with tools "
                   "hundreds of thousands of years old.",
        "url": "https://en.wikipedia.org/wiki/Koobi_Fora",
    },
    "national museum of kenya": {
        "extract": "The Nairobi National Museum tells East Africa's natural and "
                   "human story in one building - the Turkana Boy and "
                   "human-origins galleries, the Great Rift Valley geology and "
                   "bird collections - beside the Snake Park, with the Karen "
                   "Blixen, Railway and Olorgesailie museums nearby.",
        "url": "https://en.wikipedia.org/wiki/Nairobi_National_Museum",
    },
    # -- geography: mountains, rivers, lakes --------------------------------
    "aberdare range": {
        "extract": "The Aberdare Range is a volcanic highland 'spine' north of "
                   "Nairobi - moorland, bamboo forest, waterfalls and the "
                   "Aberdare National Park, home to bongo antelope, with "
                   "peaks (Satima, 4,001 m) catching both Mount Kenya's and "
                   "the Rift's rain.",
        "url": "https://en.wikipedia.org/wiki/Aberdare_Range",
    },
    "mount longonot": {
        "extract": "Mount Longonot is a stratovolcano just off the Nairobi-"
                   "Naivasha highway (2,776 m) whose crater rim is a perfect "
                   "hiking loop - a striking landmark of the Rift floor.",
        "url": "https://en.wikipedia.org/wiki/Mount_Longonot",
    },
    "menengai crater": {
        "extract": "The Menengai Crater near Nakuru is one of the world's "
                   "largest volcanic calderas and the site of Kenya's "
                   "Menengai geothermal power project.",
        "url": "https://en.wikipedia.org/wiki/Menengai_Crater",
    },
    "athi river": {
        "extract": "The Athi River (called the Galana in its lower course) "
                   "drains south-eastern Kenya from the Aberdares through "
                   "Machakos, Tsavo and to the Indian Ocean near Malindi.",
        "url": "https://en.wikipedia.org/wiki/Athi-Galana-Sabaki_River",
    },
    "ewaso ng'iro": {
        "extract": "The Ewaso Ng'iro river begins on the Leiria and Aberdare "
                   "highlands and runs north-east across Samburu and Isiolo to "
                   "the Lorian Swamp - the lifeline of Samburu's wildlife.",
        "url": "https://en.wikipedia.org/wiki/Ewaso_Ng%27iro",
    },
    "nzoia river": {
        "extract": "The Nzoia River drains the North Rift and Mount Elgon "
                   "highlands westwards through Trans Nzoia and Busia into Lake "
                   "Victoria - the lake's largest Kenyan tributary.",
        "url": "https://en.wikipedia.org/wiki/Nzoia_River",
    },
    "kerio river": {
        "extract": "The Kerio River runs down the dramatic Kerio Valley "
                   "between the Elgeyo escarpment and the Tugen hills into "
                   "Lake Turkana.",
        "url": "https://en.wikipedia.org/wiki/Kerio_River",
    },
    "yala delta": {
        "extract": "The Yala River's swamp on Lake Victoria's north shore is "
                   "Kenya's largest wetland - a Ramsar site of papyrus, "
                   "hippos and one of Africa's biggest heronries.",
        "url": "https://en.wikipedia.org/wiki/Yala_Swamp",
    },
    "lake chala": {
        "extract": "Lake Chala is a crater lake on the Kenya-Tanzania border "
                   "at the foot of Kilimanjaro, ringed by sheer cliffs and "
                   "fed by the mountain's underground springs.",
        "url": "https://en.wikipedia.org/wiki/Lake_Chala",
    },
    "lake jipe": {
        "extract": "Lake Jipe straddles the Kenya-Tanzania border at the foot "
                   "of the North Pare Mountains, a shallow wetland with "
                   "hippos, birds and a papyrus fringe near Taveta.",
        "url": "https://en.wikipedia.org/wiki/Lake_Jipe",
    },
    # -- parks & reserves beyond the headliners ------------------------------
    "meru national park": {
        "extract": "Meru National Park, made famous by Joy Adamson's 'Born "
                   "Free' lioness Elsa, covers savanna, the Tana and Rojeweru "
                   "rivers and the Nyambene foothills with elephants, lions "
                   "and leopards.",
        "url": "https://en.wikipedia.org/wiki/Meru_National_Park",
    },
    "shimba hills": {
        "extract": "Shimba Hills National Reserve above the Kwale coast has "
                   "sable and roan antelope and elephants, with the Sheldrick "
                   "Falls and one of the country's largest coastal forests.",
        "url": "https://en.wikipedia.org/wiki/Shimba_Hills_National_Reserve",
    },
    "arabuko-sokoke": {
        "extract": "Arabuko-Sokoke Forest, Kenya's largest intact coastal "
                   "forest near Watamu, shelters the endangered Sokoke scops "
                   "owl and golden-rumped elephant shrew and dozens of endemic "
                   "species.",
        "url": "https://en.wikipedia.org/wiki/Arabuko-Sokoke_Forest",
    },
    "saiwa swamp": {
        "extract": "Saiwa Swamp National Reserve in Trans Nzoia protects the "
                   "endangered Sitatunga antelope and De Brazza's monkey in "
                   "Kenya's only swamp national park.",
        "url": "https://en.wikipedia.org/wiki/Saiwa_Swamp_National_Reserve",
    },
    "ruma national park": {
        "extract": "Ruma National Park in Homa Bay County is Kenya's only "
                   "home of the roan antelope and a refuge for the rare blue "
                   "swallow, along the Lambwe valley.",
        "url": "https://en.wikipedia.org/wiki/Ruma_National_Park",
    },
    "ol pejeta": {
        "extract": "Ol Pejeta Conservancy in Laikipia is East Africa's largest "
                   "black rhino sanctuary and the last home of Najin and Fatu, "
                   "the world's final two northern white rhinos, plus a "
                   "chimpanzee sanctuary.",
        "url": "https://en.wikipedia.org/wiki/Ol_Pejeta_Conservancy",
    },
    "lewa conservancy": {
        "extract": "Lewa Wildlife Conservancy in Laikipia - a private rhino, "
                   "elephant and Grevy's zebra reserve and a UNESCO World "
                   "Heritage Site, known for its annual marathon.",
        "url": "https://en.wikipedia.org/wiki/Lewa_Wildlife_Conservancy",
    },
    "chyulu hills": {
        "extract": "The Chyulu Hills are Kenya's youngest volcanic range "
                   "(about 10,000 years old), a green spine of lava country "
                   "between Amboseli and Tsavo with caves like the Leviathan.",
        "url": "https://en.wikipedia.org/wiki/Chyulu_Hills",
    },
    "buffalo springs": {
        "extract": "Buffalo Springs National Reserve in Isiolo, along the "
                   "Ewaso Ng'iro, is famous for its wildlife, springs and the "
                   "view of Mount Kenya - often counted with Shaba and "
                   "Samburu.",
        "url": "https://en.wikipedia.org/wiki/Buffalo_Springs_National_Reserve",
    },
    "shaba reserve": {
        "extract": "Shaba National Reserve in Isiolo (of Joy and George "
                   "Adamson's lioness fame) is a dry savanna reserve along the "
                   "Ewaso Ng'iro with gerenuk, Grevy's zebra and golden caves.",
        "url": "https://en.wikipedia.org/wiki/Shaba_National_Reserve",
    },
    # -- people and ethnic groups ---------------------------------------------
    "kikuyu": {
        "extract": "The Kikuyu (Agikuyu) are Kenya's largest ethnic group, "
                   "traditionally farming the fertile Central Highlands "
                   "north of Nairobi. Their oral tradition places origin at "
                   "Mount Kenya; many of Kenya's political and business "
                   "elites, and the Kenyatta family, are Kikuyu.",
        "url": "https://en.wikipedia.org/wiki/Kikuyu_people",
    },
    "luhya": {
        "extract": "The Luhya (Luyia) of western Kenya are the second-largest "
                   "ethnic group, a family of Bantu-speaking sub-tribes "
                   "(Bukusu, Maragoli, Wanga...) numbering millions across "
                   "Kakamega, Vihiga, Bungoma and Busia counties.",
        "url": "https://en.wikipedia.org/wiki/Luhya_people",
    },
    "kalenjin": {
        "extract": "The Kalenjin are a group of Highland Nilotic peoples "
                   "(Nandi, Kipsigis, Tugen, Keiyo, Pokot...) of the Rift "
                   "Valley, world-famous for long-distance running and the "
                   "homeland of Presidents Moi and Ruto.",
        "url": "https://en.wikipedia.org/wiki/Kalenjin_people",
    },
    "luo": {
        "extract": "The Luo of Nyanza and western Kenya are a Nilotic people "
                   "around Lake Victoria, famous for fishing, politics (the "
                   "Odingas) and music. Their main language is Dholuo.",
        "url": "https://en.wikipedia.org/wiki/Luo_people",
    },
    "kamba": {
        "extract": "The Kamba (Akamba) of Ukambani (Machakos, Makueni, Kitui) "
                   "are a Bantu people historically known as traders and "
                   "carriers, skilled wood-carvers and (formerly) hunters.",
        "url": "https://en.wikipedia.org/wiki/Kamba_people",
    },
    "somali": {
        "extract": "The Somali are the dominant people of Kenya's North "
                   "Eastern counties (Garissa, Wajir, Mandera) - Muslim, "
                   "pastoral, Somali-speaking, with deep trade ties across "
                   "the Horn of Africa border.",
        "url": "https://en.wikipedia.org/wiki/Somali_people",
    },
    "kisii": {
        "extract": "The Kisii (Abagusii) of Nyanza's highlands around Kisii "
                   "town are a Bantu people famous for soapstone carving at "
                   "Tabaka, coffee and tea farming and one of Kenya's "
                   "densest populations.",
        "url": "https://en.wikipedia.org/wiki/Kisii_people",
    },
    "mijikenda": {
        "extract": "The Mijikenda ('nine homes') are the coastal Bantu peoples "
                   "- Giriama, Digo, Duruma, Chonyi, Ribe, Rabai, Jibana, "
                   "Kauma, Kambe - whose sacred kaya forests are UNESCO World "
                   "Heritage Sites.",
        "url": "https://en.wikipedia.org/wiki/Mijikenda_people",
    },
    "maasai": {
        "extract": "The Maasai are semi-nomadic pastoralists of Narok, "
                   "Kajiado and the Rift, known worldwide for their red "
                   "shukas, beadwork, jumping adamu dance and close bond with "
                   "the savanna and the Mara ecosystem.",
        "url": "https://en.wikipedia.org/wiki/Maasai_people",
    },
    "turkana": {
        "extract": "The Turkana are pastoral Nilotic people of the vast "
                   "north-west desert around Lake Turkana, who migrated there "
                   "in the 18th century and adapted to one of Africa's harshest "
                   "environments.",
        "url": "https://en.wikipedia.org/wiki/Turkana_people",
    },
    "pokot": {
        "extract": "The Pokot of West Pokot and Baringo straddle the "
                   "Kalenjin-Nilotic divide - cattle keepers and herders in "
                   "one of Kenya's most rugged borderlands.",
        "url": "https://en.wikipedia.org/wiki/Pokot_people",
    },
    "samburu": {
        "extract": "The Samburu are cousins of the Maasai, pastoralists of "
                   "northern Kenya's Samburu County with a distinctive "
                   "colour-full beadwork culture and traditional warriors.",
        "url": "https://en.wikipedia.org/wiki/Samburu_people",
    },
    "embu people": {
        "extract": "The Embu are the Bantu people of Mount Kenya's southern "
                   "slopes in Embu County, closely related to the Kikuyu and "
                   "Mbeere, known for coffee, tea and miraa farming.",
        "url": "https://en.wikipedia.org/wiki/Embu_people",
    },
    "meru people": {
        "extract": "The Meru are the Bantu people on Mount Kenya's north-east "
                   "flanks, whose oral tradition says they migrated via the "
                   "coast under a leader named Mbwaa; tied to the Njuri "
                   "Ncheke council of elders.",
        "url": "https://en.wikipedia.org/wiki/Meru_people",
    },
    "taita": {
        "extract": "The Taita (Wataita) inhabit the Taita Hills of "
                   "Taita-Taveta County - farmers on isolated cloud-forest "
                   "hills surrounded by Tsavo savanna.",
        "url": "https://en.wikipedia.org/wiki/Taita_people",
    },
    "rendille": {
        "extract": "The Rendille are an Eastern Cushitic camel-herding people "
                   "of Marsabit County's Kaisut desert, culturally tied to the "
                   "Samburu with whom they share festivals.",
        "url": "https://en.wikipedia.org/wiki/Rendille_people",
    },
    "borana": {
        "extract": "The Borana are Oromo-speaking pastoralists of Marsabit and "
                   "Isiolo counties who follow the age-set 'gada' system, "
                   "herding cattle and camels across the northern frontier.",
        "url": "https://en.wikipedia.org/wiki/Borana_people",
    },
    "swahili people": {
        "extract": "The Swahili (Waswahili) are the people of the East African "
                   "coast - Muslim, coastal, and heirs of the Indian Ocean "
                   "trade; their language Swahili became East Africa's lingua "
                   "franca and one of Kenya's two official tongues.",
        "url": "https://en.wikipedia.org/wiki/Swahili_people",
    },
    "el molo": {
        "extract": "The El Molo of Lake Turkana's south-eastern shore are "
                   "Kenya's smallest and most endangered ethnic group - "
                   "traditionally fisher-people now numbering only a few "
                   "hundred.",
        "url": "https://en.wikipedia.org/wiki/El_Molo_people",
    },
    "ogiek": {
        "extract": "The Ogiek are an indigenous hunter-gatherer people of the "
                   "Mau Forest, recognised by Kenya's constitution as one of "
                   "its historical marginalised minorities.",
        "url": "https://en.wikipedia.org/wiki/Ogiek_people",
    },
    "teso": {
        "extract": "The Teso (Iteso) are a Nilotic people straddling western "
                   "Kenya (Busia) and Uganda, known for farming and their "
                   "stone 'aqis' homestead tradition.",
        "url": "https://en.wikipedia.org/wiki/Teso_people",
    },
    "kuria": {
        "extract": "The Kuria of Migori County straddle the Kenya-Tanzania "
                   "border around Isebania - farmers and cattle keepers whose "
                   "initiation traditions and abagambi clans define social "
                   "life.",
        "url": "https://en.wikipedia.org/wiki/Kuria_people",
    },
    "gikuyu mount kenya": {
        "extract": "For the Kikuyu and related Bantu peoples, Mount Kenya "
                   "(Kirinyaga, 'place of brightness') is the sacred home of "
                   "the creator god Ngai - houses were traditionally built "
                   "with the door facing the mountain.",
        "url": "https://en.wikipedia.org/wiki/Kirinyaga_(mountain)",
    },
    # -- media ---------------------------------------------------------------
    "daily nation": {
        "extract": "The Daily Nation (Nation Media Group) is Kenya's "
                   "bestselling English newspaper and website, founded in 1960 "
                   "by the Aga Khan's Nation group; it also runs NTV, "
                   "Nation FM and Taifa Leo.",
        "url": "https://en.wikipedia.org/wiki/Daily_Nation",
    },
    "the standard": {
        "extract": "The Standard (Standard Group) is Kenya's oldest newspaper, "
                   "founded in 1902, with the KTN television channel and "
                   "Radio Maisha; its website is standardmedia.co.ke.",
        "url": "https://en.wikipedia.org/wiki/The_Standard_(Kenya)",
    },
    "citizen tv": {
        "extract": "Citizen TV (Royal Media Services) is Kenya's most-watched "
                   "television channel, with Citizen Digital and Radio "
                   "Citizen - known for strong news coverage and "
                   "investigative reporting.",
        "url": "https://en.wikipedia.org/wiki/Citizen_TV_(Kenya)",
    },
    "kbc": {
        "extract": "The Kenya Broadcasting Corporation (KBC) is the state "
                   "broadcaster, offering radio in many languages and national "
                   "television since 1964 (formerly Voice of Kenya).",
        "url": "https://en.wikipedia.org/wiki/Kenya_Broadcasting_Corporation",
    },
    "ntv kenya": {
        "extract": "NTV is Nation Media Group's television channel, known for "
                   "prime-time news, current affairs and entertainment; "
                   "launched in 1999 as Nation TV.",
        "url": "https://en.wikipedia.org/wiki/NTV_(Kenya)",
    },
    "ktn": {
        "extract": "KTN (Kenya Television Network) is Standard Group's TV "
                   "channel - Kenya's first private television station, "
                   "launched 1990.",
        "url": "https://en.wikipedia.org/wiki/KTN_(Kenya)",
    },
    "capital fm": {
        "extract": "Capital FM is a Nairobi-centred English radio and news "
                   "house (Capital Group) known for urban hits, business and "
                   "the power breakfast show.",
        "url": "https://en.wikipedia.org/wiki/Capital_FM_(Kenya)",
    },
    "the star kenya": {
        "extract": "The Star is a Nairobi English newspaper and website "
                   "(Radio Africa Group, founded 2002) known for sharp "
                   "political reporting and the 'political barometer' column.",
        "url": "https://en.wikipedia.org/wiki/The_Star_(Kenya)",
    },
    "taifa leo": {
        "extract": "Taifa Leo is Kenya's leading Swahili daily newspaper, "
                   "published by Nation Media Group since 1960 - a pillar of "
                   "Kiswahili journalism.",
        "url": "https://en.wikipedia.org/wiki/Taifa_Leo",
    },
    # -- sport ---------------------------------------------------------------
    "harambee stars": {
        "extract": "Harambee Stars is Kenya's national football team. Kenya "
                   "has never yet qualified for a FIFA World Cup; its biggest "
                   "moments include the 2004 African Nations Cup and runs to "
                   "the CHAN semi-finals.",
        "url": "https://en.wikipedia.org/wiki/Kenya_national_football_team",
    },
    "harambee starlets": {
        "extract": "Harambee Starlets is Kenya's national women's football "
                   "team, first to qualify Kenya (2016) for the Africa Women "
                   "Cup of Nations.",
        "url": "https://en.wikipedia.org/wiki/Kenya_women%27s_national_football_team",
    },
    "kenya sevens": {
        "extract": "Kenya's rugby sevens team, nicknamed Shujaa, is a "
                   "perennial World Rugby Sevens Series core side and has won "
                   "the Safari Sevens alongside regional trophies.",
        "url": "https://en.wikipedia.org/wiki/Kenya_national_rugby_sevens_team",
    },
    "gor mahia": {
        "extract": "Gor Mahia FC of Nairobi is Kenya's most successful "
                   "football club, with many Kenyan Premier League titles, "
                   "CECAFA championships, and a devoted following since 1968.",
        "url": "https://en.wikipedia.org/wiki/Gor_Mahia_F.C.",
    },
    "afc leopards": {
        "extract": "AFC Leopards of Nairobi, founded 1964 as Abaluhya United, "
                   "is Gor Mahia's great rival - the two sides contest the "
                   "intense 'Mashemeji derby' in the Kenyan Premier League.",
        "url": "https://en.wikipedia.org/wiki/AFC_Leopards",
    },
    "david rudisha": {
        "extract": "David Rudisha (born 1988) is Kenya's 800m legend - "
                   "two-time Olympic champion (2012, 2016) and world-record "
                   "holder 1:40.91 from London 2012.",
        "url": "https://en.wikipedia.org/wiki/David_Rudisha",
    },
    "faith kipyegon": {
        "extract": "Faith Kipyegon (born 1994) is Kenya's middle-distance "
                   "superstar - Olympic 1,500m champion (2016, 2020, 2024) and "
                   "world-record holder over 1,500m and the mile.",
        "url": "https://en.wikipedia.org/wiki/Faith_Kipyegon",
    },
    "julius yego": {
        "extract": "Julius Yego (born 1989), nicknamed 'the YouTube javelin "
                   "man' for teaching himself from online videos, became "
                   "Kenya's first world javelin champion in 2015 and an "
                   "Olympic silver medallist.",
        "url": "https://en.wikipedia.org/wiki/Julius_Yego",
    },
    "kevin kiptum": {
        "extract": "Kevin Kiptum (2000-2024) broke the marathon world record "
                   "with 2:00:35 at Chicago 2023, becoming the first man under "
                   "2:01; he died in a road accident in February 2024.",
        "url": "https://en.wikipedia.org/wiki/Kelvin_Kiptum",
    },
    "vivian cheruiyot": {
        "extract": "Vivian Cheruiyot (born 1983) is one of Kenya's greatest "
                   "distance runners - world cross-country and track champion "
                   "in the 5,000m/10,000m and 2016 Olympic silver in the "
                   "5,000m.",
        "url": "https://en.wikipedia.org/wiki/Vivian_Cheruiyot",
    },
    # -- business, tech & money ----------------------------------------------
    "m-pesa": {
        "extract": "M-PESA is Kenya's mobile-money platform launched by "
                   "Safaricom in 2007 - the world's most successful "
                   "phone-based payments system, used by over 30 million "
                   "Kenyans for transfers, payments, loans (M-Shwari, "
                   "Fuliza) and savings.",
        "url": "https://en.wikipedia.org/wiki/M-Pesa",
    },
    "safaricom": {
        "extract": "Safaricom is Kenya's largest mobile network operator - a "
                   "Nairobi-listed company part-owned by the government and "
                   "Vodafone, running M-PESA, fibre and mobile services in "
                   "Kenya and Safaricom Ethiopia.",
        "url": "https://en.wikipedia.org/wiki/Safaricom",
    },
    "equity group": {
        "extract": "Equity Group Holdings is Kenya's biggest bank by customer "
                   "count - grown by CEO James Mwangi from a micro-lender into "
                   "a pan-African bank operating across the region.",
        "url": "https://en.wikipedia.org/wiki/Equity_Bank_Limited",
    },
    "kcb": {
        "extract": "KCB Group, founded 1896, is one of Kenya's oldest and "
                   "largest banks - full name Kenya Commercial Bank - with "
                   "operations across East Africa after buying the former "
                   "NBK.",
        "url": "https://en.wikipedia.org/wiki/KCB_Group",
    },
    "nairobi securities exchange": {
        "extract": "The Nairobi Securities Exchange (NSE, founded 1954) is "
                   "East Africa's largest stock market, headquartered in "
                   "Nairobi with a main and alternative market segment.",
        "url": "https://en.wikipedia.org/wiki/Nairobi_Securities_Exchange",
    },
    "kenya airways": {
        "extract": "Kenya Airways, 'the Pride of Africa', is Kenya's flag "
                   "carrier based at JKIA in Nairobi - a member of the SkyTeam "
                   "alliance flying across Africa, Europe, the Gulf and Asia.",
        "url": "https://en.wikipedia.org/wiki/Kenya_Airways",
    },
    "standard gauge railway": {
        "extract": "The Standard Gauge Railway (SGR) is Kenya's modern "
                   "freight and passenger line from Mombasa to Nairobi and "
                   "Naivasha, built with Chinese financing and opened from "
                   "2017 - replacing the colonial-era metre-gauge railway.",
        "url": "https://en.wikipedia.org/wiki/Mombasa%E2%80%93Nairobi_Standard_Gauge_Railway",
    },
    "lapsset": {
        "extract": "LAPSSET (Lamu Port-South Sudan-Ethiopia-Transport "
                   "corridor) is Kenya's grand infrastructure project: a new "
                   "port at Lamu, an oil pipeline, roads and rail to link "
                   "landlocked Ethiopia and South Sudan to the Indian Ocean.",
        "url": "https://en.wikipedia.org/wiki/LAPSSET_Corridor_Project",
    },
    "konza technopolis": {
        "extract": "Konza Technopolis is Kenya's planned 'silicon savannah' "
                   "smart city south-east of Nairobi, envisioned as an IT, "
                   "call-centre and research cluster along the Machakos "
                   "corridor.",
        "url": "https://en.wikipedia.org/wiki/Konza_Technopolis",
    },
    "olkaria geothermal": {
        "extract": "The Olkaria geothermal fields near Naivasha host Kenya's "
                   "flagship geothermal power stations - among Africa's "
                   "largest - feeding much of Nairobi's electricity via the "
                   "Olkaria V plants.",
        "url": "https://en.wikipedia.org/wiki/Olkaria_Geothermal_Power_Station",
    },
    "lake turkana wind power": {
        "extract": "Lake Turkana Wind Power near Loiyangalani (opened 2019) "
                   "is Africa's largest wind farm - 365 turbines supplying "
                   "about 15% of Kenya's national grid capacity.",
        "url": "https://en.wikipedia.org/wiki/Lake_Turkana_Wind_Power_Station",
    },
    "m-kopa": {
        "extract": "M-KOPA is a Nairobi-born 'pay-as-you-go' solar company "
                   "that finances solar home systems, phones and loans for "
                   "millions of customers across Kenya, Uganda and beyond.",
        "url": "https://en.wikipedia.org/wiki/M-KOPA",
    },
    "twiga foods": {
        "extract": "Twiga Foods is a Nairobi-based B2B food-distribution "
                   "platform that connects smallholder farmers directly to "
                   "urban kiosks and vendors, cutting out the middleman.",
        "url": "https://en.wikipedia.org/wiki/Twiga_Foods",
    },
    "ihub": {
        "extract": "iHub, founded in Nairobi in 2010, pioneered East "
                   "Africa's innovation hubs - a co-working, incubator and "
                   "developer community space credited with seeding Kenya's "
                   "tech ecosystem.",
        "url": "https://en.wikipedia.org/wiki/IHub",
    },
    # -- arts, culture & literature -------------------------------------------
    "ngugi wa thiong'o": {
        "extract": "Ngugi wa Thiong'o (born 1938, Nyeri) is Kenya's most "
                   "famous writer - author of 'Weep Not, Child', 'A Grain of "
                   "Wheat' and 'Petals of Blood', and a fearless champion of "
                   "writing African literature in African languages.",
        "url": "https://en.wikipedia.org/wiki/Ngugi_wa_Thiong%27o",
    },
    "lupita nyong'o": {
        "extract": "Lupita Nyong'o (born 1983, Mexico City, raised in Kenya) "
                   "won the 2014 Best Supporting Actress Oscar for '12 Years "
                   "a Slave' - the first Kenyan actor to win an Academy "
                   "Award.",
        "url": "https://en.wikipedia.org/wiki/Lupita_Nyong%27o",
    },
    "sauti sol": {
        "extract": "Sauti Sol is Kenya's award-winning afro-pop boy band "
                   "(founded 2005) - albums like 'Midnight Train' and "
                   "hits such as 'Sura Yako' won them a global following and "
                   "a Grammy nomination.",
        "url": "https://en.wikipedia.org/wiki/Sauti_Sol",
    },
    "fadhili william": {
        "extract": "Fadhili William (1938-2001) is the Mombasa-born composer "
                   "of 'Malaika', one of East Africa's most beloved songs - "
                   "covered worldwide by Harry Belafonte, Miriam Makeba and "
                   "Boney M.",
        "url": "https://en.wikipedia.org/wiki/Fadhili_William",
    },
    "nyashinski": {
        "extract": "Nyashinski (Kamau Njihia) is a Kenyan rapper and singer, "
                   "a solo superstar after the hip-hop group Kleptomaniax, "
                   "with hits like 'Mala' and 'Now You Know'.",
        "url": "https://en.wikipedia.org/wiki/Nyashinski",
    },
    "mekatilili wa menza": {
        "extract": "Mekatilili wa Menza (c.1860-1924) was the Giriama "
                   "prophetess and women's leader who defied the British "
                   "colonial administration's forced-labour conscription in "
                   "coastal Kenya after 1913 - a heroine of early resistance.",
        "url": "https://en.wikipedia.org/wiki/Mekatilili_wa_Menza",
    },
    "oginga odinga": {
        "extract": "Jaramogi Oginga Odinga (1911-1994) was Kenya's first "
                   "Vice-President after independence, later the fireside "
                   "opposition voice, and father of Raila Odinga - the "
                   "founding father of Kenyan multiparty democracy.",
        "url": "https://en.wikipedia.org/wiki/Oginga_Odinga",
    },
    "jm kariuki": {
        "extract": "J.M. Kariuki (1929-1975), 'JM', was one of the post-"
                   "independence era's most popular MPs - a Mau Mau veteran "
                   "and crusader for the poor whose 1975 assassination "
                   "shocked the nation.",
        "url": "https://en.wikipedia.org/wiki/Josiah_Mwangi_Kariuki",
    },
    "ronald ngala": {
        "extract": "Ronald Ngala (1923-1972) led the coastal KADU party in "
                   "the independence negotiations, championing majimboism "
                   "(regionalism) and minority protection in Kenya's "
                   "constitution.",
        "url": "https://en.wikipedia.org/wiki/Ronald_Ngala",
    },
    "pio gama pinto": {
        "extract": "Pio Gama Pinto (1927-1965) was a Kenyan-Goan "
                   "independence activist and anti-colonial journalist, "
                   "assassinated in 1965 - among the first political murders "
                   "of independent Kenya.",
        "url": "https://en.wikipedia.org/wiki/Pio_Gama_Pinto",
    },
    "louis leakey": {
        "extract": "Louis Leakey (1903-1972) and wife Mary (1913-1996) were "
                   "the paleoanthropologists who made the Great Rift Valley "
                   "famous - their Olduvai and Koobi Fora finds helped prove "
                   "humans evolved in Africa.",
        "url": "https://en.wikipedia.org/wiki/Louis_Leakey",
    },
    "richard leakey": {
        "extract": "Richard Leakey (1944-2022), son of Louis and Mary, led "
                   "fossil-hunting expeditions that uncovered Homo habilis "
                   "and Homo erectus remains, and later headed the Kenya "
                   "Wildlife Service in the ivory war.",
        "url": "https://en.wikipedia.org/wiki/Richard_Leakey",
    },
    # -- more national schools ------------------------------------------------
    "maranda high school": {
        "extract": "Maranda High School is a national boys' school in "
                   "Bondo, Siaya County (est. 1946) - one of Kenya's "
                   "top-performing schools, alma mater of many leaders and "
                   "professionals.",
        "url": "https://en.wikipedia.org/wiki/Maranda_High_School",
    },
    "kakamega high school": {
        "extract": "Kakamega High School is a national boys' school in "
                   "Kakamega town (est. 1931), consistently among Kenya's "
                   "best, with the Green Commandos football tradition.",
        "url": "https://en.wikipedia.org/wiki/Kakamega_High_School",
    },
    "nakuru high school": {
        "extract": "Nakuru High School is a national boys' school in "
                   "Nakuru - a school with strong academic results and a "
                   "rich hockey history.",
        "url": "https://en.wikipedia.org/wiki/Nakuru_High_School",
    },
    "nyeri high school": {
        "extract": "Nyeri High School is a national boys' school in Nyeri "
                   "town (est. 1947), with top KCSE results and a proud "
                   "agricultural heritage.",
        "url": "https://en.wikipedia.org/wiki/Nyeri_High_School",
    },
    "kapsabet boys": {
        "extract": "Kapsabet High School is a national boys' school in "
                   "Nandi County - among Kenya's best-performing, with a "
                   "long list of doctors, engineers and leaders.",
        "url": "https://en.wikipedia.org/wiki/Kapsabet_High_School",
    },
    "butere girls": {
        "extract": "Butere Girls' High School is a national girls' school "
                   "in western Kenya (est. 1931), historically a sister "
                   "school to Maseno, producing many leaders and academics.",
        "url": "https://en.wikipedia.org/wiki/Butere_High_School",
    },
    "mary leakey high school": {
        "extract": "Mary Leakey High School (Mbotela, Molo) is a national "
                   "girls' school, consistently among Kenya's best "
                   "performing, named after the paleoanthropologist Mary "
                   "Leakey.",
        "url": "https://en.wikipedia.org/wiki/Mary_Leakey_High_School",
    },
    "moi girls eldoret": {
        "extract": "Moi Girls' High School Eldoret is a national girls' "
                   "school in the North Rift with stellar KCSE results and "
                   "the alma mater of many leading women.",
        "url": "https://en.wikipedia.org/wiki/Moi_Girls_Eldoret",
    },
    "cardinal otunga school": {
        "extract": "Cardinal Otunga High School Mosocho (Kisii County) is a "
                   "national boys' catholic school (est. 1942) with a "
                   "legendary academic record.",
        "url": "https://en.wikipedia.org/wiki/Cardinal_Otunga_High_School_Mosocho",
    },
    "kisii school": {
        "extract": "Kisii School is a national boys' school in Kisii town "
                   "(est. 1932), one of Kenya's oldest, alma mater of "
                   "politicians, judges and professionals.",
        "url": "https://en.wikipedia.org/wiki/Kisii_High_School",
    },
    "chewoyet high": {
        "extract": "Chewoyet High School is a national boys' school near "
                   "Kapenguria, West Pokot - a rising KCSE power in the "
                   "North Rift.",
        "url": "https://en.wikipedia.org/wiki/Chewoyet_High_School",
    },
    "sacho high school": {
        "extract": "Sacho High School is a national boys' school in "
                   "Koibatek, Baringo County - alma mater of Daniel arap "
                   "Moi and many Kalenjin professionals.",
        "url": "https://en.wikipedia.org/wiki/Sacho_High_School",
    },
    # -- more universities ----------------------------------------------------
    "moi university": {
        "extract": "Moi University in Eldoret (chartered 1984) is Kenya's "
                   "second national university, strong in health sciences, "
                   "forestry and engineering, with its main campus at "
                   "Kesses.",
        "url": "https://en.wikipedia.org/wiki/Moi_University",
    },
    "egerton university": {
        "extract": "Egerton University in Njoro (chartered 1987, from a 1939 "
                   "agricultural college) is Kenya's specialist agricultural "
                   "university, famous for agronomy and animal-science "
                   "research.",
        "url": "https://en.wikipedia.org/wiki/Egerton_University",
    },
    "maseno university": {
        "extract": "Maseno University sits on the equator near Kisumu "
                   "(chartered 2001), leading in health, education and "
                   "environmental sciences.",
        "url": "https://en.wikipedia.org/wiki/Maseno_University",
    },
    "masinde muliro university": {
        "extract": "Masinde Muliro University of Science and Technology "
                   "(MMUST, Kakamega, chartered 2007) takes its name from "
                   "the independence politician Masinde Muliro.",
        "url": "https://en.wikipedia.org/wiki/Masinde_Muliro_University_of_Science_and_Technology",
    },
    "mount kenya university": {
        "extract": "Mount Kenya University (MKU, Thika) is Kenya's largest "
                   "private university by student numbers, with campuses "
                   "across Kenya and in Uganda and Rwanda.",
        "url": "https://en.wikipedia.org/wiki/Mount_Kenya_University",
    },
    "strathmore university": {
        "extract": "Strathmore University in Nairobi (from a 1961 accountancy "
                   "college, university 2002) is Kenya's leading business "
                   "and law university, with the Strathmore Law School and "
                   "iLabAfrica.",
        "url": "https://en.wikipedia.org/wiki/Strathmore_University",
    },
    "kca university": {
        "extract": "KCA University in Ruaraka, Nairobi (chartered 2007) grew "
                   "out of the Kenya College of Accountancy - strong in "
                   "accounting, business and IT.",
        "url": "https://en.wikipedia.org/wiki/KCA_University",
    },
    "usiu-africa": {
        "extract": "United States International University-Africa (USIU-"
                   "Africa) in Nairobi is a private university with an "
                   "American-style curriculum, strong in business and "
                   "international relations.",
        "url": "https://en.wikipedia.org/wiki/United_States_International_University_Africa",
    },
    "daystar university": {
        "extract": "Daystar University in Nairobi is a private Christian "
                   "university (chartered 1994) known for communication, "
                   "journalism and leadership training.",
        "url": "https://en.wikipedia.org/wiki/Daystar_University",
    },
    "cuea": {
        "extract": "The Catholic University of Eastern Africa (CUEA, "
                   "Lang'ata, Nairobi) is the region's main Catholic "
                   "university, training priests, theologians and "
                   "professionals since 1992.",
        "url": "https://en.wikipedia.org/wiki/Catholic_University_of_Eastern_Africa",
    },
    "aga khan university": {
        "extract": "Aga Khan University (AKU), with its Nairobi campus, is "
                   "the region's premier private health-sciences university, "
                   "running the Aga Khan University Hospital in Nairobi.",
        "url": "https://en.wikipedia.org/wiki/Aga_Khan_University",
    },
    "jooust": {
        "extract": "Jaramogi Oginga Odinga University of Science and "
                   "Technology (JOOUST) in Bondo, Siaya County, chartered "
                   "2013, is named after Jaramogi Oginga Odinga.",
        "url": "https://en.wikipedia.org/wiki/Jaramogi_Oginga_Odinga_University_of_Science_and_Technology",
    },
    "kisii university": {
        "extract": "Kisii University (chartered 2007 from a 1965 college) is "
                   "the highlands university of Nyanza, with campuses in "
                   "Kisii, Eldoret and Kericho.",
        "url": "https://en.wikipedia.org/wiki/Kisii_University",
    },
    "karatina university": {
        "extract": "Karatina University in Nyeri County (chartered 2013, "
                   "from Karatina College) serves Mount Kenya's education "
                   "belt with tourism and agribusiness courses.",
        "url": "https://en.wikipedia.org/wiki/Karatina_University",
    },
    "chuka university": {
        "extract": "Chuka University on the slopes of Mount Kenya (from "
                   "Egerton's Chuka campus, university 2013) specialises in "
                   "agriculture, education and business.",
        "url": "https://en.wikipedia.org/wiki/Chuka_University",
    },
    "dedan kimathi university": {
        "extract": "Dedan Kimathi University of Technology (DeKUT) in Nyeri "
                   "is a technical university founded from a JKUAT campus, "
                   "named in honour of the Mau Mau leader.",
        "url": "https://en.wikipedia.org/wiki/Dedan_Kimathi_University_of_Technology",
    },
    "technical university of kenya": {
        "extract": "The Technical University of Kenya (TUK, formerly Kenya "
                   "Polytechnic, Nairobi) is Kenya's oldest technical "
                   "institution (1961), now a full university of engineering "
                   "and technology.",
        "url": "https://en.wikipedia.org/wiki/Technical_University_of_Kenya",
    },
    "technical university of mombasa": {
        "extract": "The Technical University of Mombasa (TUM, from Mombasa "
                   "Polytechnic, chartered 2013) is the coast's technology "
                   "university.",
        "url": "https://en.wikipedia.org/wiki/Technical_University_of_Mombasa",
    },
    "south eastern kenya university": {
        "extract": "South Eastern Kenya University (SEKU, in Kitui county, "
                   "chartered 2013 from JKUAT Kitui campus) serves eastern "
                   "Kenya's drier counties.",
        "url": "https://en.wikipedia.org/wiki/South_Eastern_Kenya_University",
    },
    "university of eldoret": {
        "extract": "The University of Eldoret (chartered 2013, from Moi "
                   "University's Chepkoilel campus) specialises in "
                   "agriculture, forestry and environmental sciences.",
        "url": "https://en.wikipedia.org/wiki/University_of_Eldoret",
    },
    "laikipia university": {
        "extract": "Laikipia University in Nyahururu (chartered 2013) is the "
                   "central Rift's university, strong in education and "
                   "conservation sciences near the Laikipia ranches.",
        "url": "https://en.wikipedia.org/wiki/Laikipia_University",
    },
    "university of embu": {
        "extract": "The University of Embu (from Egerton's Embu campus, "
                   "chartered 2013) specialises in agriculture, food "
                   "science and veterinary medicine.",
        "url": "https://en.wikipedia.org/wiki/University_of_Embu",
    },
}
_KENYA_FACTS.update(_EXTRA_KENYA_FACTS)

# --- third batch: holders of the roles above + broad 10x coverage ---------
#
# Everything here is a *short, safe, offline* one-paragraph answer. Sources
# are the ordinary public encyclopedias/databases already used elsewhere in
# this module; nothing here is scraped, paid or API-gated.
_EXTRA_KENYA_FACTS_2 = {
    # -- current holders of the roles matched in _EXTRA_GOV_ROLES -------------
    "martha koome": {
        "extract": "Martha Koome has been Chief Justice of Kenya since 2021 "
                   "and the first woman to hold the office, chairing the "
                   "Supreme Court after a long career as an advocate.",
        "url": "https://en.wikipedia.org/wiki/Martha_Koome",
    },
    "kithure kindiki": {
        "extract": "Kithure Kindiki has been Deputy President of Kenya since "
                   "October 2024, a Tharaka-Nithi senator and constitutional "
                   "law professor who previously served as Interior cabinet "
                   "secretary.",
        "url": "https://en.wikipedia.org/wiki/Kithure_Kindiki",
    },
    "moses wetang'ula": {
        "extract": "Moses Wetang'ula is Speaker of Kenya's National Assembly "
                   "(2022-), a Bungoma senator and former Finance and Foreign "
                   "Affairs minister who chairs the Ford Kenya party.",
        "url": "https://en.wikipedia.org/wiki/Moses_Wetang%27ula",
    },
    "amason kingi": {
        "extract": "Amason Kingi is Speaker of Kenya's Senate (2013-), "
                   "former Kilifi governor and earlier a member of the "
                   "coastal CNC movement.",
        "url": "https://en.wikipedia.org/wiki/Amason_Kingi",
    },
    # -- universities ---------------------------------------------------------
    "taita taveta university": {
        "extract": "Taita Taveta University, chartered in 2016 at Voi, is a "
                   "public university strong in mining, geology, water and "
                   "agricultural engineering for the coastal uplands.",
        "url": "https://en.wikipedia.org/wiki/Taita_Taveta_University",
    },
    "kirinyaga university": {
        "extract": "Kirinyaga University is a public university chartered in "
                   "2016 at Kerugoya, teaching agriculture, business and "
                   "technology in central Kenya.",
        "url": "https://en.wikipedia.org/wiki/Kirinyaga_University",
    },
    "murang'a university of technology": {
        "extract": "Murang'a University of Technology, a public university "
                   "chartered in 2021, focuses on engineering and technology "
                   "in central Kenya.",
        "url": "https://en.wikipedia.org/wiki/Murang%27a_University_of_Technology",
    },
    "rongo university": {
        "extract": "Rongo University is a public university in Migori "
                   "County, grown from an Egerton University campus and "
                   "chartered in 2016.",
        "url": "https://en.wikipedia.org/wiki/Rongo_University",
    },
    "garissa university": {
        "extract": "Garissa University is a public university in north-"
                   "eastern Kenya offering agriculture, education and "
                   "Islamic studies, chartered in 2015.",
        "url": "https://en.wikipedia.org/wiki/Garissa_University",
    },
    "maasai mara university": {
        "extract": "Maasai Mara University, chartered in 2013 in Narok, is "
                   "the public university beside the Maasai Mara, strong in "
                   "tour guiding, wildlife and education.",
        "url": "https://en.wikipedia.org/wiki/Maasai_Mara_University",
    },
    "co-operative university of kenya": {
        "extract": "The Co-operative University of Kenya (CUK) in Nairobi is "
                   "the university of the cooperative movement, offering "
                   "business, finance and cooperatives programmes.",
        "url": "https://en.wikipedia.org/wiki/Co-operative_University_of_Kenya",
    },
    "kabarak university": {
        "extract": "Kabarak University is a private university in Nakuru "
                   "County founded with the Moi family in 2002, known for "
                   "education, business and health sciences.",
        "url": "https://en.wikipedia.org/wiki/Kabarak_University",
    },
    "zetech university": {
        "extract": "Zetech University is a private university at Ruiru "
                   "focused on technology, business and applied sciences for "
                   "young urban learners.",
        "url": "https://en.wikipedia.org/wiki/Zetech_University",
    },
    "st paul's university": {
        "extract": "Saint Paul's University in Limuru is a private "
                   "(Anglican) university, one of Kenya's oldest institutions "
                   "of higher learning.",
        "url": "https://en.wikipedia.org/wiki/St._Paul%27s_University,_Kenya",
    },
    # -- towns & settlements --------------------------------------------------
    "ruiru": {
        "extract": "Ruiru is a fast-growing industrial and commuter town in "
                   "Kiambu County on the Thika superhighway north of "
                   "Nairobi, a hub of factories and new estates.",
        "url": "https://en.wikipedia.org/wiki/Ruiru",
    },
    "kitengela": {
        "extract": "Kitengela is a booming satellite town in Kajiado County "
                   "on the southern edge of Nairobi, home of the A.I.C. "
                   "Girls' School and the Kitengela glass artists.",
        "url": "https://en.wikipedia.org/wiki/Kitengela",
    },
    "ongata rongai": {
        "extract": "Ongata Rongai is a residential town in Kajiado County "
                   "just south of Nairobi, growing fast along the Magadi "
                   "road.",
        "url": "https://en.wikipedia.org/wiki/Ongata_Rongai",
    },
    "limuru": {
        "extract": "Limuru is a tea-growing highland town in Kiambu County, "
                   "home of Wambugu Farmers' and the late novelist Ngugi wa "
                   "Thiong'o's birthplace country.",
        "url": "https://en.wikipedia.org/wiki/Limuru",
    },
    "nanyuki": {
        "extract": "Nanyuki is a garrison and farming town on the equator at "
                   "the foot of Mount Kenya in Laikipia County, gateway to "
                   "the mountain and a big horse-and-safari base.",
        "url": "https://en.wikipedia.org/wiki/Nanyuki",
    },
    "maralal": {
        "extract": "Maralal is the rugged frontier town of Samburu County, "
                   "famous for the Maralal Camel Derby and the UK David "
                   "Sheldrick-era independence history of northern Kenya.",
        "url": "https://en.wikipedia.org/wiki/Maralal",
    },
    "lodwar": {
        "extract": "Lodwar is Turkana County's hot frontier capital on the "
                   "road and air route to Lake Turkana, a centre of the "
                   "north-western pastoral economy.",
        "url": "https://en.wikipedia.org/wiki/Lodwar",
    },
    "moyale": {
        "extract": "Moyale is a busy border town on the Kenya-Ethiopia "
                   "frontier in Marsabit County, the southern end of the "
                   "LAPSSET highway corridor.",
        "url": "https://en.wikipedia.org/wiki/Moyale",
    },
    "watamu": {
        "extract": "Watamu is a palm-fringed resort and turtle-nesting "
                   "village in Kilifi County beside Watamu Marine National "
                   "Park and the Gede ruins.",
        "url": "https://en.wikipedia.org/wiki/Watamu",
    },
    "diani": {
        "extract": "Diani Beach, near Ukunda on the south coast, is Kenya's "
                   "best-known white-sand resort stretch, lined with "
                   "hotels and coral reefs.",
        "url": "https://en.wikipedia.org/wiki/Diani_Beach",
    },
    "ukunda": {
        "extract": "Ukunda is the busy gateway town of the south coast that "
                   "serves Diani Beach, with its airstrip and buzzing "
                   "market.",
        "url": "https://en.wikipedia.org/wiki/Ukunda",
    },
    "ol donyo sabuk": {
        "extract": "Ol Donyo Sabuk, also called Kilimambogo, is the lonely "
                   "mountain east of Thika where the 14 Falls flow - a "
                   "former MacMillan estate now a national park.",
        "url": "https://en.wikipedia.org/wiki/Ol_Donyo_Sabuk",
    },
    "kilimambogo": {
        "extract": "Kilimambogo is the Kikuyu name of Ol Donyo Sabuk, the "
                   "mountain east of Nairobi with the historic MacMillan "
                   "burial site at its peak.",
        "url": "https://en.wikipedia.org/wiki/Ol_Donyo_Sabuk",
    },
    # -- lakes ------------------------------------------------------------------
    "lake naivasha": {
        "extract": "Lake Naivasha is Kenya's sweet-water Rift Valley lake of "
                   "hippos and pelicans, west of Nairobi, ringed by flower "
                   "farms and the historic Happy Valley country.",
        "url": "https://en.wikipedia.org/wiki/Lake_Naivasha",
    },
    "lake nakuru": {
        "extract": "Lake Nakuru, the flamingo lake inside Lake Nakuru "
                   "National Park, is an alkaline soda lake in the Rift "
                   "Valley that also shelters rhinos.",
        "url": "https://en.wikipedia.org/wiki/Lake_Nakuru",
    },
    "lake baringo": {
        "extract": "Lake Baringo is a fresh-water Rift Valley lake north of "
                   "Nakuru, famed for its bird life, crocodiles and the "
                   "island camps of the Njemps people.",
        "url": "https://en.wikipedia.org/wiki/Lake_Baringo",
    },
    "simbi nyaima": {
        "extract": "Simbi Nyaima is the legendary 'vanishing village' lake "
                   "in Homa Bay County - Luo folklore says a thriving "
                   "village sank beneath the waters that now fill it.",
        "url": "https://en.wikipedia.org/wiki/Simbi_Nyaima",
    },
    # -- rivers -----------------------------------------------------------------
    "mara river": {
        "extract": "The Mara River is the river of the great wildebeest "
                   "migration, crossed each year by hundreds of thousands of "
                   "animals entering the Maasai Mara from the Serengeti.",
        "url": "https://en.wikipedia.org/wiki/Mara_River",
    },
    "nairobi river": {
        "extract": "The Nairobi River flows through Kenya's capital into the "
                   "Athi system, passing the National Museum and the "
                   "watershed that shapes the city's valleys.",
        "url": "https://en.wikipedia.org/wiki/Nairobi_River",
    },
    "mbagathi river": {
        "extract": "The Mbagathi River marks the southern boundary of Nairobi "
                   "National Park, where lions shelter a few minutes from "
                   "the city centre.",
        "url": "https://en.wikipedia.org/wiki/Mbagathi_River",
    },
    "turkwell": {
        "extract": "The Turkwell (Turkwel) River drains the western "
                   "highlands into Lake Turkana, dammed at Turkwel Gorge for "
                   "Kenya's biggest hydro station.",
        "url": "https://en.wikipedia.org/wiki/Turkwel_River",
    },
    "sondu miriu": {
        "extract": "The Sondu-Miriu River tumbles from the Nandi highlands "
                   "to Lake Victoria and powers a small hydro plant that "
                   "feeds the western grid.",
        "url": "https://en.wikipedia.org/wiki/Sondu_Miriu_River",
    },
    # -- parks & reserves -------------------------------------------------------
    "kakamega forest": {
        "extract": "Kakamega Forest is Kenya's only tropical rainforest, a "
                   "western refuge of monkeys, 400 bird species and the "
                   "endemic Kakamega glass frog.",
        "url": "https://en.wikipedia.org/wiki/Kakamega_Forest",
    },
    "watamu marine": {
        "extract": "Watamu Marine National Park off the Kilifi coast "
                   "protects the coral gardens, turtles and sea birds of the "
                   "Mida Creek ecosystem.",
        "url": "https://en.wikipedia.org/wiki/Watamu_Marine_National_Park",
    },
    "kiunga marine": {
        "extract": "Kiunga Marine National Reserve along the Lamu coast "
                   "protects a chain of coral islands, mangroves and "
                   "dugongs in the northern Indian Ocean.",
        "url": "https://en.wikipedia.org/wiki/Kiunga_Marine_National_Reserve",
    },
    "ndere island": {
        "extract": "Ndere Island National Park sits as a bird sanctuary in "
                   "Lake Victoria off Kisumu Bay, where herons and cormorants "
                   "nest and Ogaa, the sacred rock, is revered.",
        "url": "https://en.wikipedia.org/wiki/Ndere_Island_National_Park",
    },
    "dongo kundu": {
        "extract": "Dongo Kundu is the industrial and freeport zone being "
                   "developed between Mombasa and the mainland, part of the "
                   "new Kipevu mega-container development.",
        "url": "https://en.wikipedia.org/wiki/Dongo_Kundu",
    },
    # -- economy, utilities & public services -----------------------------------
    "kengen": {
        "extract": "KenGen, Kenya Electricity Generating Company, is the "
                   "state power producer running the Olkaria geothermal "
                   "fields, dams on Seven Forks and wind at Ngong.",
        "url": "https://en.wikipedia.org/wiki/KenGen",
    },
    "kenya power": {
        "extract": "Kenya Power (KPLC) is the national electricity "
                   "distribution utility that buys from KenGen and others "
                   "and sells to homes and businesses over the national "
                   "grid.",
        "url": "https://en.wikipedia.org/wiki/Kenya_Power",
    },
    "kenya ports authority": {
        "extract": "The Kenya Ports Authority (KPA) operates the Port of "
                   "Mombasa, East Africa's main gate, and the newly built "
                   "Lamu Port.",
        "url": "https://en.wikipedia.org/wiki/Kenya_Ports_Authority",
    },
    "eabl": {
        "extract": "East African Breweries Limited (EABL), brewer of Tusker "
                   "and Pilsner, is Kenya's biggest drinks company and one "
                   "of the largest listed firms.",
        "url": "https://en.wikipedia.org/wiki/East_African_Breweries",
    },
    "airtel kenya": {
        "extract": "Airtel Kenya is the second mobile network operator, "
                   "offering voice, data and the Airtel Money wallet in "
                   "competition with Safaricom.",
        "url": "https://en.wikipedia.org/wiki/Airtel_Kenya",
    },
    "co-op bank": {
        "extract": "The Co-operative Bank of Kenya, built from the "
                   "cooperative movement, is one of the country's largest "
                   "banks with a strong SME base.",
        "url": "https://en.wikipedia.org/wiki/Co-operative_Bank_of_Kenya",
    },
    "e-citizen": {
        "extract": "e-Citizen is the Kenyan government's online services "
                   "portal where citizens pay taxes, apply for licences and "
                   "passports and do business with the state digitally.",
        "url": "https://en.wikipedia.org/wiki/ECitizen",
    },
    "huduma centre": {
        "extract": "Huduma Centres are one-stop government service points in "
                   "counties across Kenya where citizens renew IDs, driving "
                   "licences and permits under one roof.",
        "url": "https://hudumacentres.go.ke",
    },
    "kenya railways": {
        "extract": "Kenya Railways operates the colonial-era metre-gauge "
                   "line once called the 'Lunatic Express' and today's "
                   "Standard Gauge Railway commuter services on the "
                   "Nairobi-Mombasa corridor.",
        "url": "https://en.wikipedia.org/wiki/Kenya_Railways",
    },
    "kws": {
        "extract": "The Kenya Wildlife Service (KWS) is the state agency "
                   "that protects national parks and reserves and their "
                   "animals - the rangers of Tsavo, the Mara and the rest.",
        "url": "https://en.wikipedia.org/wiki/Kenya_Wildlife_Service",
    },
    "ntsa": {
        "extract": "NTSA, the National Transport and Safety Authority, "
                   "issues the numbered plates and driving licences Kenyans "
                   "pay for via e-Citizen.",
        "url": "https://en.wikipedia.org/wiki/National_Transport_and_Safety_Authority",
    },
    "kenya shilling": {
        "extract": "The Kenya shilling (KES) is Kenya's currency, issued by "
                   "the Central Bank of Kenya, and a major East African "
                   "trading currency.",
        "url": "https://en.wikipedia.org/wiki/Kenyan_shilling",
    },
    "central bank of kenya": {
        "extract": "The Central Bank of Kenya (CBK), founded in 1966, issues "
                   "the shilling, manages the nation's reserves and licences "
                   "the commercial banks.",
        "url": "https://en.wikipedia.org/wiki/Central_Bank_of_Kenya",
    },
    # -- holidays & national days -------------------------------------------------
    "mashujaa day": {
        "extract": "Mashujaa Day (Heroes' Day), October 20, honours Kenya's "
                   "freedom heroes - the Mau Mau veterans and all who "
                   "fought for independence.",
        "url": "https://en.wikipedia.org/wiki/Mashujaa_Day",
    },
    "jamhuri day": {
        "extract": "Jamhuri Day, December 12, marks Kenya becoming a "
                   "republic in 1964, after independence from Britain in "
                   "1963.",
        "url": "https://en.wikipedia.org/wiki/Jamhuri_Day",
    },
    "madaraka day": {
        "extract": "Madaraka Day, June 1, celebrates Kenya's internal "
                   "self-governance of 1963, when the first true Kenyan "
                   "government took office.",
        "url": "https://en.wikipedia.org/wiki/Madaraka_Day",
    },
    "utamaduni day": {
        "extract": "Utamaduni Day, added to the calendar in 2020 around "
                   "Christmas, honours Kenya's cultural heritage and the "
                   "nations that make it one country.",
        "url": "https://en.wikipedia.org/wiki/Utamaduni_Day",
    },
    # -- food, wildlife & culture ---------------------------------------------------
    "ugali": {
        "extract": "Ugali - maize meal cooked firm - is Kenya's staple food, "
                   "eaten with sukuma wiki, fish or meat across the "
                   "country.",
        "url": "https://en.wikipedia.org/wiki/Posho",
    },
    "nyama choma": {
        "extract": "Nyama choma (roasted meat) is Kenya's favourite eating-"
                   "out food, served from roadside kibandas and upmarket "
                   "choma joints alike.",
        "url": "https://en.wikipedia.org/wiki/Nyama_choma",
    },
    "chapati": {
        "extract": "Chapati, the layered flatbread that came with Indian "
                   "migrants, is a daily staple in Kenyan homes and "
                   "hotels.",
        "url": "https://en.wikipedia.org/wiki/Chapati",
    },
    "githeri": {
        "extract": "Githeri - boiled maize and beans - is the classic "
                   "highland meal of central Kenya, often served with "
                   "avocado.",
        "url": "https://en.wikipedia.org/wiki/Githeri",
    },
    "mandazi": {
        "extract": "Mandazi, the sweet fried doughnut of the Swahili coast, "
                   "is Kenya's most popular breakfast snack.",
        "url": "https://en.wikipedia.org/wiki/Mandazi",
    },
    "mukimo": {
        "extract": "Mukimo is the mashed potato-banana-and-maize dish of "
                   "the Mount Kenya peoples, coloured with pumpkin and "
                   "greens.",
        "url": "https://en.wikipedia.org/wiki/Mukimo",
    },
    "mursik": {
        "extract": "Mursik is the Kalenjin soured-milk drink, fermented in "
                   "a sotet gourd with charcoal - a traditional Rift Valley "
                   "staple.",
        "url": "https://en.wikipedia.org/wiki/Mursik",
    },
    "big five": {
        "extract": "The Big Five - lion, leopard, elephant, rhino and "
                   "buffalo - are the safari big game Kenya is world-famous "
                   "for.",
        "url": "https://en.wikipedia.org/wiki/Big_five_game",
    },
    "great migration": {
        "extract": "The Great Migration is the yearly movement of over a "
                   "million wildebeest between Tanzania's Serengeti and "
                   "Kenya's Maasai Mara, crossing the Mara River at the "
                   "famous crossings.",
        "url": "https://en.wikipedia.org/wiki/Great_migration_(Serengeti)",
    },
    "giraffe": {
        "extract": "Kenya is home to the rare Rothschild's giraffe and to "
                   "retics east of the Rift, protected at Giraffe Centre and "
                   "in national parks.",
        "url": "https://en.wikipedia.org/wiki/Giraffe",
    },
    "lion": {
        "extract": "Lions prowl the Maasai Mara, Amboseli and Tsavo - Tsavo "
                   "once produced the man-eating lions of 1898, now a tourist "
                   "icon.",
        "url": "https://en.wikipedia.org/wiki/Lion",
    },
    "african elephant": {
        "extract": "Kenya's elephants, led by the great tuskers of Amboseli "
                   "and Tsavo, are among the world's largest land animals "
                   "and a top safari draw.",
        "url": "https://en.wikipedia.org/wiki/African_bush_elephant",
    },
    "cheetah": {
        "extract": "Kenya's plains - the Mara, Amboseli and the Laikipia "
                   "plateau - still shelter the world's fastest land animal, "
                   "the cheetah.",
        "url": "https://en.wikipedia.org/wiki/Cheetah",
    },
    "black rhino": {
        "extract": "Kenya is a rhino stronghold, guarding black rhinos at "
                   "Ol Pejeta, Nakuru and Tsavo and the last northern white "
                   "rhinos in the world at Ol Pejeta.",
        "url": "https://en.wikipedia.org/wiki/Black_rhinoceros",
    },
    "malkia strikers": {
        "extract": "Malkia Strikers, Kenya's national women's volleyball "
                   "team, have been queens of African volleyball for "
                   "decades, qualifying for the Olympics.",
        "url": "https://en.wikipedia.org/wiki/Kenya_women%27s_national_volleyball_team",
    },
    # -- landscapes, people & history extras ---------------------------------------
    "ngong hills": {
        "extract": "The Ngong Hills are the green ridge above Nairobi in "
                   "Kajiado County - the backdrop of Isak Dinesen's 'Out of "
                   "Africa' and a favourite weekend hike.",
        "url": "https://en.wikipedia.org/wiki/Ngong_Hills",
    },
    "east africa": {
        "extract": "East Africa - Kenya, Uganda, Tanzania, Rwanda, Burundi "
                   "and South Sudan - is the region Kenya anchors, home of "
                   "the EAC bloc and the Swahili coast.",
        "url": "https://en.wikipedia.org/wiki/East_Africa",
    },
    "great rift valley": {
        "extract": "The Great Rift Valley slices through Kenya from the "
                   "Turkana basin to beyond the Maasai Mara - a cradle of "
                   "humanity and a chain of soda lakes and escarpments.",
        "url": "https://en.wikipedia.org/wiki/Great_Rift_Valley",
    },
    "mau forest complex": {
        "extract": "The Mau Forest Complex is Kenya's biggest 'water tower', "
                   "feeding the Mara, Mbagathi and dozens of rivers that "
                   "supply lakes Victoria and Nakuru.",
        "url": "https://en.wikipedia.org/wiki/Mau_Forest",
    },
    "cherangani hills": {
        "extract": "The Cherangani Hills are one of Kenya's five water "
                   "towers, stretching the western highlands where Kerio and "
                   "Turkwell rise.",
        "url": "https://en.wikipedia.org/wiki/Cherangani_Hills",
    },
    "mount suswa": {
        "extract": "Mount Suswa is the double-crater volcano between "
                   "Nairobi and Narok, famous for its lava caves, pink "
                   "baboons and the Maasai community around it.",
        "url": "https://en.wikipedia.org/wiki/Mount_Suswa",
    },
    "lunatic express": {
        "extract": "The 'Lunatic Express' was the British nickname for the "
                   "1901 Mombasa-Nairobi railway, built by thousands of "
                   "workers and costing many lives through the wilderness.",
        "url": "https://en.wikipedia.org/wiki/Lunatic_Express",
    },
    "vasco da gama pillar": {
        "extract": "Vasco da Gama's pillar (1499) still stands in Malindi as "
                   "one of Africa's oldest European monuments, erected by "
                   "the Portuguese explorer.",
        "url": "https://en.wikipedia.org/wiki/Vasco_da_Gama_Pillar",
    },
    "jumba la mtwana": {
        "extract": "Jumba la Mtwana ('great house of the slave') is the 14th-"
                   "century Swahili ruin of coral houses near Mtwapa, one of "
                   "the coastal ruins of the Kilifi area.",
        "url": "https://en.wikipedia.org/wiki/Jumba_la_Mtwana",
    },
    "presidents of kenya": {
        "extract": "Kenya has had five presidents since independence in "
                   "1963: Jomo Kenyatta (1964-78), Daniel arap Moi "
                   "(1978-2002), Mwai Kibaki (2002-13), Uhuru Kenyatta "
                   "(2013-22) and William Ruto (2022- ).",
        "url": "https://en.wikipedia.org/wiki/President_of_Kenya",
    },
}
_KENYA_FACTS.update(_EXTRA_KENYA_FACTS_2)

# Central-government roles that people most often ask about.
_EXTRA_GOV_ROLES = {
    "president of kenya": "william ruto",
    "the president of kenya": "william ruto",
    "the president": "william ruto",
    "chief justice of kenya": "martha koome",
    "the chief justice of kenya": "martha koome",
    "chief justice": "martha koome",
    "the chief justice": "martha koome",
    "deputy president of kenya": "kithure kindiki",
    "the deputy president of kenya": "kithure kindiki",
    "deputy president": "kithure kindiki",
    "the deputy president": "kithure kindiki",
    "vice president": "kithure kindiki",
    "the vice president": "kithure kindiki",
    "speaker of the national assembly": "moses wetang'ula",
    "the speaker of the national assembly": "moses wetang'ula",
    "speaker of the senate": "amason kingi",
    "the speaker of the senate": "amason kingi",
    "senate speaker": "amason kingi",
    "the senate speaker": "amason kingi",
}
for _role, _holder in _EXTRA_GOV_ROLES.items():
    _CANONICAL_FACT_ALIASES[_role] = _holder

# Short aliases for the added entries (acronyms, brand names, variants).
_EXTRA_ALIASES = {
    "kplc": "kenya power",
    "sgr": "standard gauge railway",
    "kpa": "kenya ports authority",
    "cbk": "central bank of kenya",
    "tusker": "eabl",
    "eac": "east africa",
    "east african community": "east africa",
    "diani beach": "diani",
    "kenya currency": "kenya shilling",
    "kenyan currency": "kenya shilling",
    "what is the currency of kenya": "kenya shilling",
}
for _alias, _canon in _EXTRA_ALIASES.items():
    _CANONICAL_FACT_ALIASES[_alias] = _canon


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

def _cap_name(subject):
    """Title-case a name without breaking apostrophes: 'murang'a'
    -> 'Murang'a' (str.title() would give 'Murang'A')."""
    return " ".join(
        w[:1].upper() + w[1:] for w in str(subject).split(" ") if w)


def _resolve_county_name(subject):
    """Normalize a town/county subject to a canonical county profile key,
    or None. 'kitale' -> 'trans nzoia' via the alias map, 'busia county'
    -> 'busia' by stripping the qualifier."""
    subj = (subject or "").strip().strip("?").strip(".").strip("!").lower()
    if not subj:
        return None
    if subj in _KENYA_COUNTY_PROFILES:
        return subj
    aliased = _CANONICAL_FACT_ALIASES.get(subj, subj)
    if aliased in _KENYA_COUNTY_PROFILES:
        return aliased
    for suf in (" county", " town", " city", " municipality"):
        if subj.endswith(suf) and subj[: -len(suf)] in _KENYA_COUNTY_PROFILES:
            return subj[: -len(suf)]
        if aliased.endswith(suf) and aliased[: -len(suf)] in _KENYA_COUNTY_PROFILES:
            return aliased[: -len(suf)]
    # town/capital index from the county profiles
    idx = _TOWN_INDEX.get(subj)
    if idx:
        return idx
    idx = _TOWN_INDEX.get(aliased)
    if idx:
        return idx
    return None


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
        "de": "https://de.wikipedia.org",
        "es": "https://es.wikipedia.org",
        "pt": "https://pt.wikipedia.org",
        "zh": "https://zh.wikipedia.org",
        "hi": "https://hi.wikipedia.org",
        "ar": "https://ar.wikipedia.org",
        "ru": "https://ru.wikipedia.org",
        "ja": "https://ja.wikipedia.org",
    }
    # First probe always English or Swahili-first for Kenyan topics;
    # the longer tail widens global recall for obscure subjects. The
    # 20s budget still caps how many of those probes ever fire.
    _WIKI_LANGS = ("simple", "en", "sw", "fr",
                   "de", "es", "pt", "zh", "hi", "ar", "ru", "ja")
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
        key). lang is one of the _WIKI_LANGS family. The REST path is
        case-sensitive ("mount kilimanjaro" 404s), so on a miss we retry
        once with a title-cased page name - but only for the primary
        prongs (simple/en/sw) so the global-recall tail stays cheap.
        Returns {"title", "extract", "url", "source"} or {"error": str}."""
        topic = query.strip()
        if not topic:
            return {"error": "what should I look up?"}
        capped = _cap_name(topic)
        for attempt, page in enumerate((topic, capped)):
            if attempt and (page == topic or lang not in ("simple", "en", "sw")):
                break
            host = self._WIKI_HOSTS.get(lang, self._WIKI_HOSTS["en"])
            api_url = (
                host + "/api/rest_v1/page/summary/"
                + urllib.parse.quote(page.replace(" ", "_"))
            )
            raw = fetch_html(api_url, timeout=self.timeout_seconds)
            if isinstance(raw, dict):
                if attempt == 0:
                    continue  # maybe a case issue; one capped retry
                return {"error": f"couldn't look that up ({raw['error']})"}
            try:
                data = json.loads(_decode(raw))
            except (json.JSONDecodeError, ValueError):
                if attempt == 0:
                    continue
                return {"error": "couldn't parse the lookup result"}
            if not isinstance(data, dict):
                return {"error": "unexpected lookup result"}
            if data.get("type") in ("disambiguation", "redirect") or not data.get("extract"):
                # disambiguation or missing page: let the caller move on
                if attempt == 0:
                    continue
                return {"error": f"no article on {lang}.wikipedia for '{topic}'"}
            return {
                "title": data.get("title") or page,
                "extract": _WS_RE.sub(" ", data.get("extract") or "").strip()[: _MAX_TEXT_CHARS],
                "url": data.get("content_urls", {}).get("desktop", {}).get("page") or api_url,
                "source": f"{lang}.wikipedia.org",
            }
        return {"error": f"no article on {lang}.wikipedia for '{topic}'"}

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
                  or "how many" in topic or "kaunti" in topic or "zote" in topic
                  or "orodha" in topic or "ngapi" in topic or "majina" in topic)
        _county_mention = ("county" in topic or "counties" in topic
                           or "kaunti" in topic)
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
            "title": _cap_name(topic),
            "extract": entry["extract"],
            "url": entry["url"],
            "source": "Kenya factbase",
        }

    def kenya_fact_qa(self, query: str):
        """Natural-language Kenya questions answered instantly from the
        same county profiles + factbase: 'who is the governor of busia',
        'what is the capital of nakuru', 'which county is kitale in',
        'how many counties does kenya have', 'who is the president'.
        Returns a result dict or None - everything else keeps flowing
        down the lookup() chain, so a wrong guess never blocks a real
        answer from Wikipedia or web search."""
        q = (query or "").strip().strip("?").strip(".").lower()
        q = _WS_RE.sub(" ", q)
        if not q:
            return None

        def _rdict(title, extract, url):
            return {"title": title, "extract": extract,
                    "url": url, "source": "Kenya factbase"}

        # 1) national roles: "who is the president", "who's the chief justice"
        m = re.search(
            r"\b(?:who is|who was|who's|who are|tell me who)\s+"
            r"(?:the\s+)?(president(?: of kenya)?|deputy president(?: of kenya)?|"
            r"vice president(?: of kenya)?|chief justice(?: of kenya)?|"
            r"speaker of the national assembly|speaker of the senate)\s*$", q)
        if m and re.search(r"president|justice|speaker|deputy|vice", m.group(1)):
            _role = m.group(1)
            fb = self.kenya_fact_lookup(_role)
            if "error" in fb and not _role.startswith("the "):
                # "president" alone isn't a factbase key - "the president" is.
                fb = self.kenya_fact_lookup("the " + _role)
            if "extract" in fb:
                return fb

        # 2) governor questions: "who is the governor of busia"
        gov_subj = None
        m = (re.search(r"\bgovernor of\s+(.+?)\s*$", q)
             or re.search(r"\bgoverns\s+(.+?)\s*$", q))
        if m:
            gov_subj = m.group(1).strip().strip("?").strip(".").strip()
        if "governor" in q or "governs" in q:
            if gov_subj and gov_subj in ("kenya", "the republic", "the nation"):
                return _rdict(
                    "Kenya's leadership",
                    "Kenya's head of state is the President (William Ruto). "
                    "Each of Kenya's 47 counties also elects its own "
                    "governor.",
                    "https://en.wikipedia.org/wiki/Governor_(Kenya)")
            cname = _resolve_county_name(gov_subj) if gov_subj else None
            if cname:
                _p = _KENYA_COUNTY_PROFILES[cname]
                if _p[5]:
                    return _rdict(
                        f"Governor of {_cap_name(cname)} County",
                        f"The governor of {_cap_name(cname)} County ({_p[2]} "
                        f"Kenya) is {_p[5]} (elected 2022).",
                        f"https://en.wikipedia.org/wiki/"
                        f"{cname.replace(' ', '_')}_County")
            if any(w in q for w in ("list", "all", "names", "how many",
                                    "who are", "counties", "kenya")):
                lines = [f"   {_cap_name(_cc)} - {_pp[5]}" for _cc, _pp
                         in sorted(_KENYA_COUNTY_PROFILES.items()) if _pp[5]]
                if lines:
                    return _rdict(
                        "Governors of the 47 counties",
                        "Every one of Kenya's 47 counties has an elected "
                        "governor (2022 general election):\n"
                        + "\n".join(lines),
                        "https://en.wikipedia.org/wiki/Governor_(Kenya)")

        # 3) capital questions: "what is the capital of nakuru"
        m = re.search(r"\bcapital of\s+(.+?)\s*$", q)
        if m:
            subj = m.group(1).strip().strip("?").strip(".").strip()
            if subj in ("kenya", "the country", "the nation",
                        "the republic of kenya"):
                return _rdict(
                    "Capital of Kenya",
                    "Nairobi is the capital of Kenya - the capital since "
                    "1907, when it was moved from Mombasa.",
                    "https://en.wikipedia.org/wiki/Nairobi")
            cname = _resolve_county_name(subj)
            if cname:
                _p = _KENYA_COUNTY_PROFILES[cname]
                return _rdict(
                    f"Capital of {_cap_name(cname)} County",
                    f"{_cap_name(_p[1])} is the capital of {_cap_name(cname)} "
                    f"County ({_p[2]} Kenya, county code {_p[0]:03d}).",
                    f"https://en.wikipedia.org/wiki/"
                    f"{cname.replace(' ', '_')}_County")

        # 4) which county / where: "which county is kitale in", "where is voi"
        m = (re.search(r"\bwhich county (?:is|has)\s+(.+?)\s*$", q)
             or re.search(r"\bwhat county (?:is|has)\s+(.+?)\s*$", q)
             or re.match(r"^where\s+(?:is|are)\s+(.+?)\s*$", q))
        if m:
            subj = m.group(1).strip().strip("?").strip(".").strip()
            subj = re.sub(r"\s+in\s*$", "", subj).strip()
            cname = _resolve_county_name(subj)
            if cname:
                _p = _KENYA_COUNTY_PROFILES[cname]
                return _rdict(
                    f"{_cap_name(subj)} County",
                    f"{_cap_name(subj)} is in {_cap_name(cname)} County ({_p[2]} "
                    f"Kenya; county capital {_cap_name(_p[1])}).",
                    f"https://en.wikipedia.org/wiki/"
                    f"{cname.replace(' ', '_')}_County")

        # 5) how many counties - same guarantee as the factbase list.
        if "how many" in q and ("count" in q or "counties" in q or "county"
                                in q or "kaunti" in q):
            return _rdict(
                "All 47 counties of Kenya",
                "Kenya is divided into 47 counties (established by the 2010 "
                "constitution). Each has its own elected governor and "
                "county assembly.",
                "https://sw.wikipedia.org/wiki/Mkoa_wa_Kenya")

        # 6) nothing Kenya-specific - let the rest of the chain answer.
        return None

    def facts_list(self, topic: str, n: int = 5):
        """'10 facts about X' / 'facts about X'. For counties the answer
        is structured straight from the profile; for other factbase
        entries it splits the extract into numbered bullets. Returns a
        result dict or None (topic not in the factbase)."""
        try:
            n = max(1, min(int(n), 12))
        except Exception:
            n = 5
        t = (topic or "").strip().strip("?").strip(".").lower()
        if not t:
            return None
        cname = _resolve_county_name(t)
        if cname:
            p = _KENYA_COUNTY_PROFILES[cname]
            facts = [
                f"Official name: {_cap_name(cname)} County",
                f"County code {p[0]:03d} in {p[2]} Kenya",
                f"County capital: {_cap_name(p[1])}",
            ]
            if p[5]:
                facts.append(f"Governor (2022 election): {p[5]}")
            if p[3]:
                facts.append("Main towns: " + ", ".join(
                    _cap_name(x) for x in p[3]))
            if p[4]:
                facts.append(p[4].rstrip(".") + ".")
            return {
                "title": f"{n} facts about {_cap_name(cname)} County",
                "extract": "\n".join(f"  - {f}" for f in facts[:n]),
                "url": ("https://en.wikipedia.org/wiki/"
                        + cname.replace(" ", "_") + "_County"),
                "source": "Kenya factbase",
            }
        key = _CANONICAL_FACT_ALIASES.get(t, t)
        entry = _KENYA_FACTS.get(key)
        if entry:
            sentences = [s.strip() for s in re.findall(
                r"[^.!?]+[.!?]+", entry["extract"]) if s.strip()]
            if len(sentences) < 2:
                sentences = [entry["extract"].strip()]
            return {
                "title": f"{n} facts about {_cap_name(key)}",
                "extract": "\n".join(
                    f"  - {s}" for s in sentences[:n]),
                "url": entry["url"],
                "source": "Kenya factbase",
            }
        return None

    def format_facts(self, query: str, n: int = 5):
        """Formats the facts-list answer, falling back to a normal
        lookup if the topic isn't in the factbase."""
        fl = self.facts_list(query, n)
        if fl and "extract" in fl:
            return (f"{fl['title']}\n\n{fl['extract']}\n\n"
                    f"(Source: {fl['source']} - {fl['url']})")
        return self.format_lookup(query)

    def wikidata_facts(self, query: str):
        """Structured fact sheet from Wikidata (no API key). Returns
        {"title", "description", "facts": [(label, value), ...]} or
        {"error": str}. Facts are a handful of statements - population,
        country, born/died, occupation, etc. - resolved to labels."""
        try:
            subject = query.strip()
            if not subject:
                return {"error": "what should I look up?"}
            # 1) resolve the enwiki title to a Wikidata entity id (the
            #    titles= probe is case-sensitive -> retry once capped)
            entity = None
            for _cand in dict.fromkeys((subject, _cap_name(subject))):
                url = (_WIKIDATA_API + "?action=wbgetentities&sites=enwiki&titles="
                       + urllib.parse.quote(_cand) + "&props=labels|descriptions"
                         "&languages=en&format=json&formatversion=2")
                raw = _fetch_html_ua(url, timeout=self.timeout_seconds, headers=_WEB_UA)
                if isinstance(raw, dict):
                    return {"error": raw["error"]}
                data = json.loads(_decode(raw))
                ent = data.get("entities") or {}
                for eid, ent_data in ent.items():
                    if eid != "-1" and ent_data and ent_data.get("id"):
                        entity = ent_data
                        break
                if entity and not (entity.get("missing") and not entity.get("claims")):
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
                "title": (entity.get("labels") or {}).get("en", {}).get("value") or _cap_name(subject),
                "description": (entity.get("descriptions") or {}).get("en", {}).get("value", ""),
                "facts": facts,
            }
        except (json.JSONDecodeError, ValueError):
            return {"error": "couldn't parse the structured-facts result"}
        except Exception as e:  # fail-closed, never raise
            return {"error": f"structured facts unavailable ({e})"}

    _KENYA_NEWS_SITES = (
        "nation.africa", "citizen.digital", "standardmedia.co.ke", "bbc.com")

    def news_search(self, query: str, limit: int = 6, kenyan: bool = None):
        """Fresh headlines from Google News RSS (no API key). Kenyan
        queries get the Swahili Kenya edition, plus a second feed
        scoped to the big Kenyan outlets (Daily Nation, Citizen,
        Standard, BBC Africa) so local coverage actually surfaces.
        Returns a results list, or None when every feed fails."""
        if kenyan is None:
            kenyan = _is_kenyan_query(query)
        quoted = urllib.parse.quote(query)
        urls = []
        if kenyan:
            urls.append(("https://news.google.com/rss/search?q=" + quoted
                         + "&hl=sw&gl=KE&ceid=KE:sw"))
            sites = " OR ".join(f"site:{s}" for s in self._KENYA_NEWS_SITES)
            urls.append(("https://news.google.com/rss/search?q="
                         + urllib.parse.quote(query + " (" + sites + ")")
                         + "&hl=en-US&gl=KE&ceid=KE:en"))
        else:
            urls.append(("https://news.google.com/rss/search?q=" + quoted
                         + "&hl=en-US&gl=US&ceid=US:en"))

        results = []
        seen = set()
        for url in urls:
            raw = _fetch_html_ua(url, timeout=self.timeout_seconds, headers=_WEB_UA)
            if isinstance(raw, dict):
                continue
            html = _decode(raw)
            items = re.findall(
                r"<item>(.*?)</item>", html, flags=re.IGNORECASE | re.DOTALL)
            for block in items:
                if len(results) >= limit:
                    break
                title_m = re.search(r"<title>(.*?)</title>", block,
                                    re.IGNORECASE | re.DOTALL)
                link_m = re.search(r"<link>(.*?)</link>", block,
                                   re.IGNORECASE | re.DOTALL)
                if not title_m or not link_m:
                    continue
                title = re.sub(r"<[^>]+>", "", title_m.group(1)).strip()
                link = link_m.group(1).strip()
                if not title or not link:
                    continue
                key = (link, title)
                if key in seen:
                    continue
                seen.add(key)
                results.append({
                    "title": title[:120],
                    "snippet": title[:120],
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
                        "title": f"{_cap_name(query)} ({ptype} in Kenya)"
                                 if cc else f"{_cap_name(query)} ({ptype})",
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
          0a. Natural Kenya questions (governor/capital/which-county)
          1. Wikipedia REST summaries - language order depends on
             whether the query is Kenyan (sw first) or not, with a
             ~12-language tail widening global recall for misses
          2. Wikipedia title search -> full extract of the match
          3. Deep full-article extracts (en, then sw)
          4. Wiktionary (words & phrases) and Wikiquote (people)
          4a. Wikidata structured facts (people/places/things backstop)
          5. Common Swahili/French phrases -> curated dictionary
          6. OpenStreetMap place lookup (Kenya-first filtering)
          7. Merged web search (DuckDuckGo + lite + Bing) + recent
             Google News, with a deep multi-page read of the best
             live pages, attributed per source.
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

        # 0a) Natural Kenya questions ("who is the governor of busia",
        # "capital of nakuru", "which county is kitale in") resolve
        # instantly from the same county profiles.
        qa = self.kenya_fact_qa(topic)
        if qa:
            return qa

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

        # 4a) Wikidata structured facts as a final encyclopedic backstop:
        #     prose sources have already had their chance, so this mainly
        #     rescues niche entities that Wikidata knows even when their
        #     Wikipedia page is a stub. Budget-guarded like every call.
        if not _out_of_budget():
            wd = self.wikidata_facts(topic)
            if "error" not in wd and wd.get("facts"):
                _desc = (wd.get("description") or "").strip()
                _facts_txt = "\n".join(
                    f"- {_k}: {_v}" for _k, _v in wd["facts"][:8])
                return {
                    "title": wd.get("title") or topic,
                    "extract": (_desc + "\n" + _facts_txt).strip(),
                    "url": "https://www.wikidata.org",
                    "source": "Wikidata",
                }

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
        the deep multi-source lookup chain (Kenya factbase, Wikipedia in
        12 languages, full extracts, Wiktionary, Wikiquote, Wikidata,
        then merged web search with a deep read of the top result)."""
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