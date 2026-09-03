"""Section 8-EXT2: further supplementary variety
Part of the response-bank data set - see chatbot_modules/13_response_banks_loader.py.
"""

# SECTION 8-EXT2: FURTHER SUPPLEMENTARY RESPONSE VARIETY (second auto-templated pass)
# ==============================================================================
#
# A second, differently-worded round of the same idea as SECTION 8-EXT above:
# more auto-templated filler phrasing merged into every response bank, using a
# fresh template set (seeded differently) so it doesn't just repeat the first
# supplementary pass. Still fixed, deterministic text - nothing generated or
# fetched at runtime.
_EXTRA_RESPONSE_PHRASES_2 = {
    "GREETING_RESPONSES": {
        "en": [
            "However you want to take greeting from here works for me.",
            "I'm following along on greeting, keep going.",
            "That's a nice thread on greeting, want to keep pulling it?",
            "You can circle back to greeting any time - I'll still be here.",
        ],
        "sw": [
            "Hilo ni wazo zuri kuhusu greeting, tuendelee?",
            "Ni vizuri kujua unavyoona greeting.",
            "Unaweza kurudi kwenye greeting wakati wowote - bado nitakuwepo.",
        ],
        "fr": [
            "Je suis toujours partant pour parler de greeting.",
            "Merci de me parler de greeting.",
            "Peu importe comment tu veux aborder greeting, ça me va.",
        ],
    },
    "FAREWELL_RESPONSES": {
        "en": [
            "No rush - farewell can take as long as you need.",
            "That's a fair way to look at farewell.",
            "I'm following along on farewell, keep going.",
            "I'm always up for talking farewell whenever you are.",
        ],
        "sw": [
            "Ni vizuri kujua unavyoona farewell.",
            "Nitakumbuka ulizungumzia farewell.",
            "Hilo ni wazo zuri kuhusu farewell, tuendelee?",
        ],
        "fr": [
            "Peu importe comment tu veux aborder farewell, ça me va.",
            "C'est un beau sujet, farewell - on continue ?",
            "Ça vaut la peine de s'arrêter un instant sur farewell.",
        ],
    },
    "THANKS_RESPONSES": {
        "en": [
            "However you want to take thanks from here works for me.",
            "That's a fair way to look at thanks.",
            "That's a nice thread on thanks, want to keep pulling it?",
            "You can circle back to thanks any time - I'll still be here.",
        ],
        "sw": [
            "Nitakumbuka ulizungumzia thanks.",
            "Unaweza kurudi kwenye thanks wakati wowote - bado nitakuwepo.",
            "Inafaa kutafakari kidogo kuhusu thanks.",
        ],
        "fr": [
            "Je suis toujours partant pour parler de thanks.",
            "Pas de pression - thanks peut prendre tout le temps qu'il faut.",
            "C'est bon de savoir ce que tu penses de thanks.",
        ],
    },
    "HOW_ARE_YOU_RESPONSES": {
        "en": [
            "I'll remember you brought up how are you.",
            "Worth sitting with for a second - how are you, that is.",
            "However you want to take how are you from here works for me.",
            "Honestly, how are you is a good thing to check in about.",
        ],
        "sw": [
            "Nashukuru kunieleza kuhusu how are you.",
            "Hakuna haraka - how are you inaweza kuchukua muda unaohitaji.",
            "Kwa kweli, how are you ni jambo zuri la kuzungumzia.",
        ],
        "fr": [
            "Peu importe comment tu veux aborder how are you, ça me va.",
            "C'est un beau sujet, how are you - on continue ?",
            "Ça vaut la peine de s'arrêter un instant sur how are you.",
        ],
    },
    "UNKNOWN_RESPONSES": {
        "en": [
            "No rush - unknown can take as long as you need.",
            "I'm always up for talking unknown whenever you are.",
            "I'll remember you brought up unknown.",
            "I'm following along on unknown, keep going.",
        ],
        "sw": [
            "Hilo ni wazo zuri kuhusu unknown, tuendelee?",
            "Nitakumbuka ulizungumzia unknown.",
            "Kwa kweli, unknown ni jambo zuri la kuzungumzia.",
        ],
        "fr": [
            "Ça vaut la peine de s'arrêter un instant sur unknown.",
            "Tu peux revenir sur unknown quand tu veux, je serai là.",
            "C'est un beau sujet, unknown - on continue ?",
        ],
    },
    "COMPLIMENT_RESPONSES": {
        "en": [
            "I'm following along on compliment, keep going.",
            "You can circle back to compliment any time - I'll still be here.",
            "I'll remember you brought up compliment.",
            "That's a fair way to look at compliment.",
        ],
        "sw": [
            "Hakuna haraka - compliment inaweza kuchukua muda unaohitaji.",
            "Unaweza kurudi kwenye compliment wakati wowote - bado nitakuwepo.",
            "Kwa kweli, compliment ni jambo zuri la kuzungumzia.",
        ],
        "fr": [
            "Je suis toujours partant pour parler de compliment.",
            "Honnêtement, compliment vaut la peine d'en reparler.",
            "Tu peux revenir sur compliment quand tu veux, je serai là.",
        ],
    },
    "WEATHER_SMALLTALK_RESPONSES": {
        "en": [
            "I'll remember you brought up weather smalltalk.",
            "That's a fair way to look at weather smalltalk.",
            "However you want to take weather smalltalk from here works for me.",
            "I'm always up for talking weather smalltalk whenever you are.",
        ],
        "sw": [
            "Njia yoyote unayotaka kuchukua kuhusu weather smalltalk inafaa kwangu.",
            "Niko tayari kuzungumza kuhusu weather smalltalk wakati wowote.",
            "Unaweza kurudi kwenye weather smalltalk wakati wowote - bado nitakuwepo.",
        ],
        "fr": [
            "Merci de me parler de weather smalltalk.",
            "Honnêtement, weather smalltalk vaut la peine d'en reparler.",
            "Peu importe comment tu veux aborder weather smalltalk, ça me va.",
        ],
    },
    "FEELINGS_HAPPY_RESPONSES": {
        "en": [
            "Worth sitting with for a second - feelings happy, that is.",
            "You can circle back to feelings happy any time - I'll still be here.",
            "No rush - feelings happy can take as long as you need.",
            "However you want to take feelings happy from here works for me.",
        ],
        "sw": [
            "Hilo ni wazo zuri kuhusu feelings happy, tuendelee?",
            "Kwa kweli, feelings happy ni jambo zuri la kuzungumzia.",
            "Ni vizuri kujua unavyoona feelings happy.",
        ],
        "fr": [
            "Je me souviendrai que tu as mentionné feelings happy.",
            "Merci de me parler de feelings happy.",
            "Peu importe comment tu veux aborder feelings happy, ça me va.",
        ],
    },
    "FEELINGS_SAD_RESPONSES": {
        "en": [
            "You can circle back to feelings sad any time - I'll still be here.",
            "Worth sitting with for a second - feelings sad, that is.",
            "I'll remember you brought up feelings sad.",
            "Honestly, feelings sad is a good thing to check in about.",
        ],
        "sw": [
            "Unaweza kurudi kwenye feelings sad wakati wowote - bado nitakuwepo.",
            "Ni vizuri kujua unavyoona feelings sad.",
            "Njia yoyote unayotaka kuchukua kuhusu feelings sad inafaa kwangu.",
        ],
        "fr": [
            "Je suis toujours partant pour parler de feelings sad.",
            "C'est bon de savoir ce que tu penses de feelings sad.",
            "Pas de pression - feelings sad peut prendre tout le temps qu'il faut.",
        ],
    },
    "FEELINGS_TIRED_RESPONSES": {
        "en": [
            "You can circle back to feelings tired any time - I'll still be here.",
            "I appreciate you letting me in on feelings tired.",
            "I'm following along on feelings tired, keep going.",
            "Good to know where you stand on feelings tired.",
        ],
        "sw": [
            "Njia yoyote unayotaka kuchukua kuhusu feelings tired inafaa kwangu.",
            "Unaweza kurudi kwenye feelings tired wakati wowote - bado nitakuwepo.",
            "Hilo ni wazo zuri kuhusu feelings tired, tuendelee?",
        ],
        "fr": [
            "Pas de pression - feelings tired peut prendre tout le temps qu'il faut.",
            "Ça vaut la peine de s'arrêter un instant sur feelings tired.",
            "Je me souviendrai que tu as mentionné feelings tired.",
        ],
    },
    "FOOD_HUNGRY_RESPONSES": {
        "en": [
            "That's a nice thread on food hungry, want to keep pulling it?",
            "I appreciate you letting me in on food hungry.",
            "I'm always up for talking food hungry whenever you are.",
            "Worth sitting with for a second - food hungry, that is.",
        ],
        "sw": [
            "Unaweza kurudi kwenye food hungry wakati wowote - bado nitakuwepo.",
            "Niko tayari kuzungumza kuhusu food hungry wakati wowote.",
            "Nashukuru kunieleza kuhusu food hungry.",
        ],
        "fr": [
            "Honnêtement, food hungry vaut la peine d'en reparler.",
            "C'est bon de savoir ce que tu penses de food hungry.",
            "Ça vaut la peine de s'arrêter un instant sur food hungry.",
        ],
    },
    "FOOD_THIRSTY_RESPONSES": {
        "en": [
            "That's a nice thread on food thirsty, want to keep pulling it?",
            "However you want to take food thirsty from here works for me.",
            "That's a fair way to look at food thirsty.",
            "Worth sitting with for a second - food thirsty, that is.",
        ],
        "sw": [
            "Njia yoyote unayotaka kuchukua kuhusu food thirsty inafaa kwangu.",
            "Ni vizuri kujua unavyoona food thirsty.",
            "Hakuna haraka - food thirsty inaweza kuchukua muda unaohitaji.",
        ],
        "fr": [
            "Ça vaut la peine de s'arrêter un instant sur food thirsty.",
            "Pas de pression - food thirsty peut prendre tout le temps qu'il faut.",
            "Je suis toujours partant pour parler de food thirsty.",
        ],
    },
    "HOBBIES_RESPONSES": {
        "en": [
            "You can circle back to hobbies any time - I'll still be here.",
            "Honestly, hobbies is a good thing to check in about.",
            "Worth sitting with for a second - hobbies, that is.",
            "However you want to take hobbies from here works for me.",
        ],
        "sw": [
            "Nitakumbuka ulizungumzia hobbies.",
            "Hilo ni wazo zuri kuhusu hobbies, tuendelee?",
            "Nashukuru kunieleza kuhusu hobbies.",
        ],
        "fr": [
            "C'est un beau sujet, hobbies - on continue ?",
            "Merci de me parler de hobbies.",
            "Je suis toujours partant pour parler de hobbies.",
        ],
    },
    "FAMILY_RESPONSES": {
        "en": [
            "I'm following along on family, keep going.",
            "Worth sitting with for a second - family, that is.",
            "That's a nice thread on family, want to keep pulling it?",
            "Good to know where you stand on family.",
        ],
        "sw": [
            "Njia yoyote unayotaka kuchukua kuhusu family inafaa kwangu.",
            "Nashukuru kunieleza kuhusu family.",
            "Nitakumbuka ulizungumzia family.",
        ],
        "fr": [
            "Je suis toujours partant pour parler de family.",
            "Je me souviendrai que tu as mentionné family.",
            "Peu importe comment tu veux aborder family, ça me va.",
        ],
    },
    "WORK_SCHOOL_RESPONSES": {
        "en": [
            "I appreciate you letting me in on work school.",
            "I'm always up for talking work school whenever you are.",
            "No rush - work school can take as long as you need.",
            "I'm following along on work school, keep going.",
        ],
        "sw": [
            "Inafaa kutafakari kidogo kuhusu work school.",
            "Nitakumbuka ulizungumzia work school.",
            "Unaweza kurudi kwenye work school wakati wowote - bado nitakuwepo.",
        ],
        "fr": [
            "Merci de me parler de work school.",
            "Peu importe comment tu veux aborder work school, ça me va.",
            "C'est bon de savoir ce que tu penses de work school.",
        ],
    },
    "AGREEMENT_RESPONSES": {
        "en": [
            "However you want to take agreement from here works for me.",
            "That's a fair way to look at agreement.",
            "Good to know where you stand on agreement.",
            "You can circle back to agreement any time - I'll still be here.",
        ],
        "sw": [
            "Nashukuru kunieleza kuhusu agreement.",
            "Njia yoyote unayotaka kuchukua kuhusu agreement inafaa kwangu.",
            "Nitakumbuka ulizungumzia agreement.",
        ],
        "fr": [
            "C'est un beau sujet, agreement - on continue ?",
            "Peu importe comment tu veux aborder agreement, ça me va.",
            "Ça vaut la peine de s'arrêter un instant sur agreement.",
        ],
    },
    "DISAGREEMENT_RESPONSES": {
        "en": [
            "That's a nice thread on disagreement, want to keep pulling it?",
            "Worth sitting with for a second - disagreement, that is.",
            "Honestly, disagreement is a good thing to check in about.",
            "That's a fair way to look at disagreement.",
        ],
        "sw": [
            "Nashukuru kunieleza kuhusu disagreement.",
            "Hilo ni wazo zuri kuhusu disagreement, tuendelee?",
            "Unaweza kurudi kwenye disagreement wakati wowote - bado nitakuwepo.",
        ],
        "fr": [
            "Merci de me parler de disagreement.",
            "Peu importe comment tu veux aborder disagreement, ça me va.",
            "C'est un beau sujet, disagreement - on continue ?",
        ],
    },
    "APOLOGY_RESPONSES": {
        "en": [
            "However you want to take apology from here works for me.",
            "Worth sitting with for a second - apology, that is.",
            "I'm following along on apology, keep going.",
            "Honestly, apology is a good thing to check in about.",
        ],
        "sw": [
            "Niko tayari kuzungumza kuhusu apology wakati wowote.",
            "Hakuna haraka - apology inaweza kuchukua muda unaohitaji.",
            "Hilo ni wazo zuri kuhusu apology, tuendelee?",
        ],
        "fr": [
            "Honnêtement, apology vaut la peine d'en reparler.",
            "Pas de pression - apology peut prendre tout le temps qu'il faut.",
            "Merci de me parler de apology.",
        ],
    },
    "BOREDOM_RESPONSES": {
        "en": [
            "That's a fair way to look at boredom.",
            "You can circle back to boredom any time - I'll still be here.",
            "No rush - boredom can take as long as you need.",
            "I'll remember you brought up boredom.",
        ],
        "sw": [
            "Hilo ni wazo zuri kuhusu boredom, tuendelee?",
            "Nashukuru kunieleza kuhusu boredom.",
            "Njia yoyote unayotaka kuchukua kuhusu boredom inafaa kwangu.",
        ],
        "fr": [
            "Je me souviendrai que tu as mentionné boredom.",
            "Pas de pression - boredom peut prendre tout le temps qu'il faut.",
            "Merci de me parler de boredom.",
        ],
    },
    "LOVE_RELATIONSHIPS_RESPONSES": {
        "en": [
            "That's a nice thread on love relationships, want to keep pulling it?",
            "Honestly, love relationships is a good thing to check in about.",
            "I'm always up for talking love relationships whenever you are.",
            "I appreciate you letting me in on love relationships.",
        ],
        "sw": [
            "Niko tayari kuzungumza kuhusu love relationships wakati wowote.",
            "Kwa kweli, love relationships ni jambo zuri la kuzungumzia.",
            "Hakuna haraka - love relationships inaweza kuchukua muda unaohitaji.",
        ],
        "fr": [
            "Peu importe comment tu veux aborder love relationships, ça me va.",
            "Merci de me parler de love relationships.",
            "Ça vaut la peine de s'arrêter un instant sur love relationships.",
        ],
    },
    "MUSIC_RESPONSES": {
        "en": [
            "No rush - music can take as long as you need.",
            "That's a fair way to look at music.",
            "Good to know where you stand on music.",
            "I appreciate you letting me in on music.",
        ],
        "sw": [
            "Hilo ni wazo zuri kuhusu music, tuendelee?",
            "Niko tayari kuzungumza kuhusu music wakati wowote.",
            "Njia yoyote unayotaka kuchukua kuhusu music inafaa kwangu.",
        ],
        "fr": [
            "Peu importe comment tu veux aborder music, ça me va.",
            "Tu peux revenir sur music quand tu veux, je serai là.",
            "Merci de me parler de music.",
        ],
    },
    "SPORTS_RESPONSES": {
        "en": [
            "I'll remember you brought up sports.",
            "Worth sitting with for a second - sports, that is.",
            "You can circle back to sports any time - I'll still be here.",
            "Good to know where you stand on sports.",
        ],
        "sw": [
            "Nitakumbuka ulizungumzia sports.",
            "Njia yoyote unayotaka kuchukua kuhusu sports inafaa kwangu.",
            "Hakuna haraka - sports inaweza kuchukua muda unaohitaji.",
        ],
        "fr": [
            "Pas de pression - sports peut prendre tout le temps qu'il faut.",
            "Tu peux revenir sur sports quand tu veux, je serai là.",
            "Ça vaut la peine de s'arrêter un instant sur sports.",
        ],
    },
    "BOOKS_RESPONSES": {
        "en": [
            "I appreciate you letting me in on books.",
            "That's a nice thread on books, want to keep pulling it?",
            "I'm following along on books, keep going.",
            "I'll remember you brought up books.",
        ],
        "sw": [
            "Ni vizuri kujua unavyoona books.",
            "Njia yoyote unayotaka kuchukua kuhusu books inafaa kwangu.",
            "Unaweza kurudi kwenye books wakati wowote - bado nitakuwepo.",
        ],
        "fr": [
            "Je me souviendrai que tu as mentionné books.",
            "C'est bon de savoir ce que tu penses de books.",
            "Tu peux revenir sur books quand tu veux, je serai là.",
        ],
    },
    "TECHNOLOGY_RESPONSES": {
        "en": [
            "I'm always up for talking technology whenever you are.",
            "No rush - technology can take as long as you need.",
            "That's a nice thread on technology, want to keep pulling it?",
            "I'll remember you brought up technology.",
        ],
        "sw": [
            "Hakuna haraka - technology inaweza kuchukua muda unaohitaji.",
            "Kwa kweli, technology ni jambo zuri la kuzungumzia.",
            "Niko tayari kuzungumza kuhusu technology wakati wowote.",
        ],
        "fr": [
            "Ça vaut la peine de s'arrêter un instant sur technology.",
            "Je me souviendrai que tu as mentionné technology.",
            "Je suis toujours partant pour parler de technology.",
        ],
    },
    "PETS_ANIMALS_RESPONSES": {
        "en": [
            "Worth sitting with for a second - pets animals, that is.",
            "That's a fair way to look at pets animals.",
            "Honestly, pets animals is a good thing to check in about.",
            "No rush - pets animals can take as long as you need.",
        ],
        "sw": [
            "Nashukuru kunieleza kuhusu pets animals.",
            "Kwa kweli, pets animals ni jambo zuri la kuzungumzia.",
            "Inafaa kutafakari kidogo kuhusu pets animals.",
        ],
        "fr": [
            "Peu importe comment tu veux aborder pets animals, ça me va.",
            "Merci de me parler de pets animals.",
            "Tu peux revenir sur pets animals quand tu veux, je serai là.",
        ],
    },
    "TRAVEL_RESPONSES": {
        "en": [
            "You can circle back to travel any time - I'll still be here.",
            "Good to know where you stand on travel.",
            "Honestly, travel is a good thing to check in about.",
            "However you want to take travel from here works for me.",
        ],
        "sw": [
            "Kwa kweli, travel ni jambo zuri la kuzungumzia.",
            "Ni vizuri kujua unavyoona travel.",
            "Inafaa kutafakari kidogo kuhusu travel.",
        ],
        "fr": [
            "Pas de pression - travel peut prendre tout le temps qu'il faut.",
            "C'est un beau sujet, travel - on continue ?",
            "Merci de me parler de travel.",
        ],
    },
    "HEALTH_RESPONSES": {
        "en": [
            "You can circle back to health any time - I'll still be here.",
            "I'll remember you brought up health.",
            "Honestly, health is a good thing to check in about.",
            "However you want to take health from here works for me.",
        ],
        "sw": [
            "Hilo ni wazo zuri kuhusu health, tuendelee?",
            "Ni vizuri kujua unavyoona health.",
            "Niko tayari kuzungumza kuhusu health wakati wowote.",
        ],
        "fr": [
            "Je me souviendrai que tu as mentionné health.",
            "Tu peux revenir sur health quand tu veux, je serai là.",
            "Merci de me parler de health.",
        ],
    },
    "MONEY_RESPONSES": {
        "en": [
            "I appreciate you letting me in on money.",
            "That's a fair way to look at money.",
            "Worth sitting with for a second - money, that is.",
            "I'm always up for talking money whenever you are.",
        ],
        "sw": [
            "Hakuna haraka - money inaweza kuchukua muda unaohitaji.",
            "Hilo ni wazo zuri kuhusu money, tuendelee?",
            "Unaweza kurudi kwenye money wakati wowote - bado nitakuwepo.",
        ],
        "fr": [
            "Ça vaut la peine de s'arrêter un instant sur money.",
            "Pas de pression - money peut prendre tout le temps qu'il faut.",
            "Je suis toujours partant pour parler de money.",
        ],
    },
    "BIRTHDAY_RESPONSES": {
        "en": [
            "I'm following along on birthday, keep going.",
            "That's a fair way to look at birthday.",
            "I'm always up for talking birthday whenever you are.",
            "You can circle back to birthday any time - I'll still be here.",
        ],
        "sw": [
            "Unaweza kurudi kwenye birthday wakati wowote - bado nitakuwepo.",
            "Ni vizuri kujua unavyoona birthday.",
            "Niko tayari kuzungumza kuhusu birthday wakati wowote.",
        ],
        "fr": [
            "Honnêtement, birthday vaut la peine d'en reparler.",
            "Pas de pression - birthday peut prendre tout le temps qu'il faut.",
            "Peu importe comment tu veux aborder birthday, ça me va.",
        ],
    },
    "CONFUSION_RESPONSES": {
        "en": [
            "You can circle back to confusion any time - I'll still be here.",
            "Worth sitting with for a second - confusion, that is.",
            "That's a nice thread on confusion, want to keep pulling it?",
            "I'm following along on confusion, keep going.",
        ],
        "sw": [
            "Inafaa kutafakari kidogo kuhusu confusion.",
            "Kwa kweli, confusion ni jambo zuri la kuzungumzia.",
            "Ni vizuri kujua unavyoona confusion.",
        ],
        "fr": [
            "Peu importe comment tu veux aborder confusion, ça me va.",
            "C'est un beau sujet, confusion - on continue ?",
            "Merci de me parler de confusion.",
        ],
    },
    "ENCOURAGEMENT_RESPONSES": {
        "en": [
            "You can circle back to encouragement any time - I'll still be here.",
            "I'm always up for talking encouragement whenever you are.",
            "I'm following along on encouragement, keep going.",
            "I'll remember you brought up encouragement.",
        ],
        "sw": [
            "Hakuna haraka - encouragement inaweza kuchukua muda unaohitaji.",
            "Kwa kweli, encouragement ni jambo zuri la kuzungumzia.",
            "Hilo ni wazo zuri kuhusu encouragement, tuendelee?",
        ],
        "fr": [
            "Peu importe comment tu veux aborder encouragement, ça me va.",
            "Je suis toujours partant pour parler de encouragement.",
            "C'est un beau sujet, encouragement - on continue ?",
        ],
    },
    "CONGRATULATIONS_RESPONSES": {
        "en": [
            "Good to know where you stand on congratulations.",
            "I'll remember you brought up congratulations.",
            "I'm following along on congratulations, keep going.",
            "I'm always up for talking congratulations whenever you are.",
        ],
        "sw": [
            "Unaweza kurudi kwenye congratulations wakati wowote - bado nitakuwepo.",
            "Ni vizuri kujua unavyoona congratulations.",
            "Nitakumbuka ulizungumzia congratulations.",
        ],
        "fr": [
            "Ça vaut la peine de s'arrêter un instant sur congratulations.",
            "Merci de me parler de congratulations.",
            "C'est bon de savoir ce que tu penses de congratulations.",
        ],
    },
    "SURPRISE_RESPONSES": {
        "en": [
            "Good to know where you stand on surprise.",
            "Honestly, surprise is a good thing to check in about.",
            "I'm following along on surprise, keep going.",
            "However you want to take surprise from here works for me.",
        ],
        "sw": [
            "Kwa kweli, surprise ni jambo zuri la kuzungumzia.",
            "Nashukuru kunieleza kuhusu surprise.",
            "Unaweza kurudi kwenye surprise wakati wowote - bado nitakuwepo.",
        ],
        "fr": [
            "Tu peux revenir sur surprise quand tu veux, je serai là.",
            "Honnêtement, surprise vaut la peine d'en reparler.",
            "Merci de me parler de surprise.",
        ],
    },
    "SMALL_REQUEST_RESPONSES": {
        "en": [
            "No rush - small request can take as long as you need.",
            "I appreciate you letting me in on small request.",
            "That's a fair way to look at small request.",
            "I'm always up for talking small request whenever you are.",
        ],
        "sw": [
            "Nitakumbuka ulizungumzia small request.",
            "Njia yoyote unayotaka kuchukua kuhusu small request inafaa kwangu.",
            "Niko tayari kuzungumza kuhusu small request wakati wowote.",
        ],
        "fr": [
            "Honnêtement, small request vaut la peine d'en reparler.",
            "Ça vaut la peine de s'arrêter un instant sur small request.",
            "Tu peux revenir sur small request quand tu veux, je serai là.",
        ],
    },
    "BOT_IDENTITY_CURIOSITY_RESPONSES": {
        "en": [
            "Good to know where you stand on bot identity curiosity.",
            "That's a fair way to look at bot identity curiosity.",
            "Worth sitting with for a second - bot identity curiosity, that is.",
            "I'm following along on bot identity curiosity, keep going.",
        ],
        "sw": [
            "Inafaa kutafakari kidogo kuhusu bot identity curiosity.",
            "Kwa kweli, bot identity curiosity ni jambo zuri la kuzungumzia.",
            "Njia yoyote unayotaka kuchukua kuhusu bot identity curiosity inafaa kwangu.",
        ],
        "fr": [
            "Merci de me parler de bot identity curiosity.",
            "C'est un beau sujet, bot identity curiosity - on continue ?",
            "Tu peux revenir sur bot identity curiosity quand tu veux, je serai là.",
        ],
    },
    "GOODNIGHT_RESPONSES": {
        "en": [
            "I'm following along on goodnight, keep going.",
            "That's a fair way to look at goodnight.",
            "Honestly, goodnight is a good thing to check in about.",
            "I appreciate you letting me in on goodnight.",
        ],
        "sw": [
            "Njia yoyote unayotaka kuchukua kuhusu goodnight inafaa kwangu.",
            "Ni vizuri kujua unavyoona goodnight.",
            "Hilo ni wazo zuri kuhusu goodnight, tuendelee?",
        ],
        "fr": [
            "Tu peux revenir sur goodnight quand tu veux, je serai là.",
            "Pas de pression - goodnight peut prendre tout le temps qu'il faut.",
            "Peu importe comment tu veux aborder goodnight, ça me va.",
        ],
    },
    "GOOD_MORNING_RESPONSES": {
        "en": [
            "Honestly, good morning is a good thing to check in about.",
            "That's a nice thread on good morning, want to keep pulling it?",
            "That's a fair way to look at good morning.",
            "I appreciate you letting me in on good morning.",
        ],
        "sw": [
            "Unaweza kurudi kwenye good morning wakati wowote - bado nitakuwepo.",
            "Niko tayari kuzungumza kuhusu good morning wakati wowote.",
            "Njia yoyote unayotaka kuchukua kuhusu good morning inafaa kwangu.",
        ],
        "fr": [
            "Honnêtement, good morning vaut la peine d'en reparler.",
            "C'est bon de savoir ce que tu penses de good morning.",
            "C'est un beau sujet, good morning - on continue ?",
        ],
    },
    "GOOD_EVENING_RESPONSES": {
        "en": [
            "You can circle back to good evening any time - I'll still be here.",
            "I'm following along on good evening, keep going.",
            "I appreciate you letting me in on good evening.",
            "Honestly, good evening is a good thing to check in about.",
        ],
        "sw": [
            "Nashukuru kunieleza kuhusu good evening.",
            "Unaweza kurudi kwenye good evening wakati wowote - bado nitakuwepo.",
            "Njia yoyote unayotaka kuchukua kuhusu good evening inafaa kwangu.",
        ],
        "fr": [
            "Tu peux revenir sur good evening quand tu veux, je serai là.",
            "Honnêtement, good evening vaut la peine d'en reparler.",
            "Pas de pression - good evening peut prendre tout le temps qu'il faut.",
        ],
    },
    "WEEKEND_RESPONSES": {
        "en": [
            "No rush - weekend can take as long as you need.",
            "However you want to take weekend from here works for me.",
            "I'll remember you brought up weekend.",
            "I'm always up for talking weekend whenever you are.",
        ],
        "sw": [
            "Unaweza kurudi kwenye weekend wakati wowote - bado nitakuwepo.",
            "Hilo ni wazo zuri kuhusu weekend, tuendelee?",
            "Inafaa kutafakari kidogo kuhusu weekend.",
        ],
        "fr": [
            "Peu importe comment tu veux aborder weekend, ça me va.",
            "Tu peux revenir sur weekend quand tu veux, je serai là.",
            "Je me souviendrai que tu as mentionné weekend.",
        ],
    },
    "WEATHER_COLD_RESPONSES": {
        "en": [
            "Good to know where you stand on weather cold.",
            "I'm always up for talking weather cold whenever you are.",
            "Worth sitting with for a second - weather cold, that is.",
            "No rush - weather cold can take as long as you need.",
        ],
        "sw": [
            "Unaweza kurudi kwenye weather cold wakati wowote - bado nitakuwepo.",
            "Hilo ni wazo zuri kuhusu weather cold, tuendelee?",
            "Nitakumbuka ulizungumzia weather cold.",
        ],
        "fr": [
            "C'est un beau sujet, weather cold - on continue ?",
            "Je suis toujours partant pour parler de weather cold.",
            "Peu importe comment tu veux aborder weather cold, ça me va.",
        ],
    },
    "WEATHER_HOT_RESPONSES": {
        "en": [
            "Good to know where you stand on weather hot.",
            "That's a nice thread on weather hot, want to keep pulling it?",
            "You can circle back to weather hot any time - I'll still be here.",
            "I'm following along on weather hot, keep going.",
        ],
        "sw": [
            "Nitakumbuka ulizungumzia weather hot.",
            "Hilo ni wazo zuri kuhusu weather hot, tuendelee?",
            "Unaweza kurudi kwenye weather hot wakati wowote - bado nitakuwepo.",
        ],
        "fr": [
            "Merci de me parler de weather hot.",
            "Tu peux revenir sur weather hot quand tu veux, je serai là.",
            "Je suis toujours partant pour parler de weather hot.",
        ],
    },
    "WEATHER_RAIN_RESPONSES": {
        "en": [
            "That's a nice thread on weather rain, want to keep pulling it?",
            "I'm following along on weather rain, keep going.",
            "No rush - weather rain can take as long as you need.",
            "That's a fair way to look at weather rain.",
        ],
        "sw": [
            "Njia yoyote unayotaka kuchukua kuhusu weather rain inafaa kwangu.",
            "Ni vizuri kujua unavyoona weather rain.",
            "Niko tayari kuzungumza kuhusu weather rain wakati wowote.",
        ],
        "fr": [
            "C'est un beau sujet, weather rain - on continue ?",
            "Merci de me parler de weather rain.",
            "Ça vaut la peine de s'arrêter un instant sur weather rain.",
        ],
    },
    "WEATHER_SNOW_RESPONSES": {
        "en": [
            "Good to know where you stand on weather snow.",
            "Worth sitting with for a second - weather snow, that is.",
            "I'll remember you brought up weather snow.",
            "That's a nice thread on weather snow, want to keep pulling it?",
        ],
        "sw": [
            "Niko tayari kuzungumza kuhusu weather snow wakati wowote.",
            "Kwa kweli, weather snow ni jambo zuri la kuzungumzia.",
            "Hakuna haraka - weather snow inaweza kuchukua muda unaohitaji.",
        ],
        "fr": [
            "Peu importe comment tu veux aborder weather snow, ça me va.",
            "Honnêtement, weather snow vaut la peine d'en reparler.",
            "Ça vaut la peine de s'arrêter un instant sur weather snow.",
        ],
    },
    "WEATHER_WINDY_RESPONSES": {
        "en": [
            "That's a nice thread on weather windy, want to keep pulling it?",
            "Honestly, weather windy is a good thing to check in about.",
            "I appreciate you letting me in on weather windy.",
            "You can circle back to weather windy any time - I'll still be here.",
        ],
        "sw": [
            "Nashukuru kunieleza kuhusu weather windy.",
            "Ni vizuri kujua unavyoona weather windy.",
            "Kwa kweli, weather windy ni jambo zuri la kuzungumzia.",
        ],
        "fr": [
            "C'est bon de savoir ce que tu penses de weather windy.",
            "Pas de pression - weather windy peut prendre tout le temps qu'il faut.",
            "Merci de me parler de weather windy.",
        ],
    },
    "HOLIDAY_SMALLTALK_RESPONSES": {
        "en": [
            "That's a nice thread on holiday smalltalk, want to keep pulling it?",
            "Worth sitting with for a second - holiday smalltalk, that is.",
            "I'm always up for talking holiday smalltalk whenever you are.",
            "You can circle back to holiday smalltalk any time - I'll still be here.",
        ],
        "sw": [
            "Inafaa kutafakari kidogo kuhusu holiday smalltalk.",
            "Njia yoyote unayotaka kuchukua kuhusu holiday smalltalk inafaa kwangu.",
            "Unaweza kurudi kwenye holiday smalltalk wakati wowote - bado nitakuwepo.",
        ],
        "fr": [
            "Merci de me parler de holiday smalltalk.",
            "Pas de pression - holiday smalltalk peut prendre tout le temps qu'il faut.",
            "C'est bon de savoir ce que tu penses de holiday smalltalk.",
        ],
    },
    "LEARNING_RESPONSES": {
        "en": [
            "That's a nice thread on learning, want to keep pulling it?",
            "I'll remember you brought up learning.",
            "Honestly, learning is a good thing to check in about.",
            "Good to know where you stand on learning.",
        ],
        "sw": [
            "Inafaa kutafakari kidogo kuhusu learning.",
            "Hilo ni wazo zuri kuhusu learning, tuendelee?",
            "Unaweza kurudi kwenye learning wakati wowote - bado nitakuwepo.",
        ],
        "fr": [
            "C'est bon de savoir ce que tu penses de learning.",
            "Je suis toujours partant pour parler de learning.",
            "Peu importe comment tu veux aborder learning, ça me va.",
        ],
    },
    "MOTIVATION_GOALS_RESPONSES": {
        "en": [
            "Honestly, motivation goals is a good thing to check in about.",
            "Worth sitting with for a second - motivation goals, that is.",
            "That's a fair way to look at motivation goals.",
            "However you want to take motivation goals from here works for me.",
        ],
        "sw": [
            "Hilo ni wazo zuri kuhusu motivation goals, tuendelee?",
            "Hakuna haraka - motivation goals inaweza kuchukua muda unaohitaji.",
            "Unaweza kurudi kwenye motivation goals wakati wowote - bado nitakuwepo.",
        ],
        "fr": [
            "Je suis toujours partant pour parler de motivation goals.",
            "Honnêtement, motivation goals vaut la peine d'en reparler.",
            "Pas de pression - motivation goals peut prendre tout le temps qu'il faut.",
        ],
    },
    "NOSTALGIA_RESPONSES": {
        "en": [
            "You can circle back to nostalgia any time - I'll still be here.",
            "That's a nice thread on nostalgia, want to keep pulling it?",
            "That's a fair way to look at nostalgia.",
            "Worth sitting with for a second - nostalgia, that is.",
        ],
        "sw": [
            "Ni vizuri kujua unavyoona nostalgia.",
            "Nashukuru kunieleza kuhusu nostalgia.",
            "Niko tayari kuzungumza kuhusu nostalgia wakati wowote.",
        ],
        "fr": [
            "Honnêtement, nostalgia vaut la peine d'en reparler.",
            "Peu importe comment tu veux aborder nostalgia, ça me va.",
            "Je suis toujours partant pour parler de nostalgia.",
        ],
    },
    "FUTURE_PLANS_RESPONSES": {
        "en": [
            "That's a fair way to look at future plans.",
            "However you want to take future plans from here works for me.",
            "I'm always up for talking future plans whenever you are.",
            "Worth sitting with for a second - future plans, that is.",
        ],
        "sw": [
            "Nitakumbuka ulizungumzia future plans.",
            "Njia yoyote unayotaka kuchukua kuhusu future plans inafaa kwangu.",
            "Hakuna haraka - future plans inaweza kuchukua muda unaohitaji.",
        ],
        "fr": [
            "Pas de pression - future plans peut prendre tout le temps qu'il faut.",
            "Merci de me parler de future plans.",
            "Ça vaut la peine de s'arrêter un instant sur future plans.",
        ],
    },
    "GAMING_RESPONSES": {
        "en": [
            "I'm following along on gaming, keep going.",
            "Worth sitting with for a second - gaming, that is.",
            "I'm always up for talking gaming whenever you are.",
            "I appreciate you letting me in on gaming.",
        ],
        "sw": [
            "Hakuna haraka - gaming inaweza kuchukua muda unaohitaji.",
            "Hilo ni wazo zuri kuhusu gaming, tuendelee?",
            "Niko tayari kuzungumza kuhusu gaming wakati wowote.",
        ],
        "fr": [
            "Honnêtement, gaming vaut la peine d'en reparler.",
            "C'est un beau sujet, gaming - on continue ?",
            "Merci de me parler de gaming.",
        ],
    },
    "COOKING_RESPONSES": {
        "en": [
            "Worth sitting with for a second - cooking, that is.",
            "Good to know where you stand on cooking.",
            "I'm always up for talking cooking whenever you are.",
            "I appreciate you letting me in on cooking.",
        ],
        "sw": [
            "Nashukuru kunieleza kuhusu cooking.",
            "Hilo ni wazo zuri kuhusu cooking, tuendelee?",
            "Hakuna haraka - cooking inaweza kuchukua muda unaohitaji.",
        ],
        "fr": [
            "Je me souviendrai que tu as mentionné cooking.",
            "C'est bon de savoir ce que tu penses de cooking.",
            "Honnêtement, cooking vaut la peine d'en reparler.",
        ],
    },
    "NATURE_OUTDOORS_RESPONSES": {
        "en": [
            "Good to know where you stand on nature outdoors.",
            "I appreciate you letting me in on nature outdoors.",
            "I'm always up for talking nature outdoors whenever you are.",
            "However you want to take nature outdoors from here works for me.",
        ],
        "sw": [
            "Niko tayari kuzungumza kuhusu nature outdoors wakati wowote.",
            "Kwa kweli, nature outdoors ni jambo zuri la kuzungumzia.",
            "Nashukuru kunieleza kuhusu nature outdoors.",
        ],
        "fr": [
            "Je me souviendrai que tu as mentionné nature outdoors.",
            "C'est bon de savoir ce que tu penses de nature outdoors.",
            "Peu importe comment tu veux aborder nature outdoors, ça me va.",
        ],
    },
    "SLEEP_DREAMS_RESPONSES": {
        "en": [
            "Worth sitting with for a second - sleep dreams, that is.",
            "No rush - sleep dreams can take as long as you need.",
            "That's a nice thread on sleep dreams, want to keep pulling it?",
            "That's a fair way to look at sleep dreams.",
        ],
        "sw": [
            "Niko tayari kuzungumza kuhusu sleep dreams wakati wowote.",
            "Nashukuru kunieleza kuhusu sleep dreams.",
            "Njia yoyote unayotaka kuchukua kuhusu sleep dreams inafaa kwangu.",
        ],
        "fr": [
            "C'est un beau sujet, sleep dreams - on continue ?",
            "Je suis toujours partant pour parler de sleep dreams.",
            "Merci de me parler de sleep dreams.",
        ],
    },
    "HUMOR_APPRECIATION_RESPONSES": {
        "en": [
            "I'll remember you brought up humor appreciation.",
            "I'm following along on humor appreciation, keep going.",
            "Worth sitting with for a second - humor appreciation, that is.",
            "I'm always up for talking humor appreciation whenever you are.",
        ],
        "sw": [
            "Kwa kweli, humor appreciation ni jambo zuri la kuzungumzia.",
            "Ni vizuri kujua unavyoona humor appreciation.",
            "Niko tayari kuzungumza kuhusu humor appreciation wakati wowote.",
        ],
        "fr": [
            "Tu peux revenir sur humor appreciation quand tu veux, je serai là.",
            "Peu importe comment tu veux aborder humor appreciation, ça me va.",
            "C'est un beau sujet, humor appreciation - on continue ?",
        ],
    },
    "SKEPTICISM_RESPONSES": {
        "en": [
            "However you want to take skepticism from here works for me.",
            "That's a fair way to look at skepticism.",
            "Good to know where you stand on skepticism.",
            "Honestly, skepticism is a good thing to check in about.",
        ],
        "sw": [
            "Kwa kweli, skepticism ni jambo zuri la kuzungumzia.",
            "Niko tayari kuzungumza kuhusu skepticism wakati wowote.",
            "Inafaa kutafakari kidogo kuhusu skepticism.",
        ],
        "fr": [
            "C'est un beau sujet, skepticism - on continue ?",
            "C'est bon de savoir ce que tu penses de skepticism.",
            "Je suis toujours partant pour parler de skepticism.",
        ],
    },
    "FILLER_ACKNOWLEDGEMENT_RESPONSES": {
        "en": [
            "Honestly, filler acknowledgement is a good thing to check in about.",
            "However you want to take filler acknowledgement from here works for me.",
            "I appreciate you letting me in on filler acknowledgement.",
            "You can circle back to filler acknowledgement any time - I'll still be here.",
        ],
        "sw": [
            "Unaweza kurudi kwenye filler acknowledgement wakati wowote - bado nitakuwepo.",
            "Nashukuru kunieleza kuhusu filler acknowledgement.",
            "Ni vizuri kujua unavyoona filler acknowledgement.",
        ],
        "fr": [
            "Peu importe comment tu veux aborder filler acknowledgement, ça me va.",
            "Je suis toujours partant pour parler de filler acknowledgement.",
            "Merci de me parler de filler acknowledgement.",
        ],
    },
    "OPINION_REQUEST_RESPONSES": {
        "en": [
            "You can circle back to opinion request any time - I'll still be here.",
            "However you want to take opinion request from here works for me.",
            "That's a fair way to look at opinion request.",
            "I'm always up for talking opinion request whenever you are.",
        ],
        "sw": [
            "Niko tayari kuzungumza kuhusu opinion request wakati wowote.",
            "Nashukuru kunieleza kuhusu opinion request.",
            "Hakuna haraka - opinion request inaweza kuchukua muda unaohitaji.",
        ],
        "fr": [
            "Merci de me parler de opinion request.",
            "Tu peux revenir sur opinion request quand tu veux, je serai là.",
            "C'est bon de savoir ce que tu penses de opinion request.",
        ],
    },
    "ADVICE_REQUEST_RESPONSES": {
        "en": [
            "I'm following along on advice request, keep going.",
            "I'm always up for talking advice request whenever you are.",
            "Honestly, advice request is a good thing to check in about.",
            "That's a fair way to look at advice request.",
        ],
        "sw": [
            "Nashukuru kunieleza kuhusu advice request.",
            "Nitakumbuka ulizungumzia advice request.",
            "Njia yoyote unayotaka kuchukua kuhusu advice request inafaa kwangu.",
        ],
        "fr": [
            "Tu peux revenir sur advice request quand tu veux, je serai là.",
            "Merci de me parler de advice request.",
            "Je me souviendrai que tu as mentionné advice request.",
        ],
    },
    "COMPARISON_RESPONSES": {
        "en": [
            "That's a nice thread on comparison, want to keep pulling it?",
            "No rush - comparison can take as long as you need.",
            "I appreciate you letting me in on comparison.",
            "I'll remember you brought up comparison.",
        ],
        "sw": [
            "Nashukuru kunieleza kuhusu comparison.",
            "Hakuna haraka - comparison inaweza kuchukua muda unaohitaji.",
            "Ni vizuri kujua unavyoona comparison.",
        ],
        "fr": [
            "Tu peux revenir sur comparison quand tu veux, je serai là.",
            "Je me souviendrai que tu as mentionné comparison.",
            "Merci de me parler de comparison.",
        ],
    },
    "FEELINGS_ANGRY_RESPONSES": {
        "en": [
            "You can circle back to feelings angry any time - I'll still be here.",
            "That's a nice thread on feelings angry, want to keep pulling it?",
            "Worth sitting with for a second - feelings angry, that is.",
            "No rush - feelings angry can take as long as you need.",
        ],
        "sw": [
            "Unaweza kurudi kwenye feelings angry wakati wowote - bado nitakuwepo.",
            "Hakuna haraka - feelings angry inaweza kuchukua muda unaohitaji.",
            "Hilo ni wazo zuri kuhusu feelings angry, tuendelee?",
        ],
        "fr": [
            "C'est bon de savoir ce que tu penses de feelings angry.",
            "Ça vaut la peine de s'arrêter un instant sur feelings angry.",
            "Je suis toujours partant pour parler de feelings angry.",
        ],
    },
    "FEELINGS_NERVOUS_RESPONSES": {
        "en": [
            "That's a nice thread on feelings nervous, want to keep pulling it?",
            "No rush - feelings nervous can take as long as you need.",
            "However you want to take feelings nervous from here works for me.",
            "You can circle back to feelings nervous any time - I'll still be here.",
        ],
        "sw": [
            "Ni vizuri kujua unavyoona feelings nervous.",
            "Kwa kweli, feelings nervous ni jambo zuri la kuzungumzia.",
            "Inafaa kutafakari kidogo kuhusu feelings nervous.",
        ],
        "fr": [
            "Peu importe comment tu veux aborder feelings nervous, ça me va.",
            "Je suis toujours partant pour parler de feelings nervous.",
            "Honnêtement, feelings nervous vaut la peine d'en reparler.",
        ],
    },
    "ANXIETY_RESPONSES": {
        "en": [
            "However you want to take anxiety from here works for me.",
            "I'm always up for talking anxiety whenever you are.",
            "I'm following along on anxiety, keep going.",
            "I'll remember you brought up anxiety.",
        ],
        "sw": [
            "Niko tayari kuzungumza kuhusu anxiety wakati wowote.",
            "Ni vizuri kujua unavyoona anxiety.",
            "Kwa kweli, anxiety ni jambo zuri la kuzungumzia.",
        ],
        "fr": [
            "C'est un beau sujet, anxiety - on continue ?",
            "Je suis toujours partant pour parler de anxiety.",
            "C'est bon de savoir ce que tu penses de anxiety.",
        ],
    },
    "FEELINGS_LONELY_RESPONSES": {
        "en": [
            "I appreciate you letting me in on feelings lonely.",
            "That's a nice thread on feelings lonely, want to keep pulling it?",
            "I'm always up for talking feelings lonely whenever you are.",
            "You can circle back to feelings lonely any time - I'll still be here.",
        ],
        "sw": [
            "Nashukuru kunieleza kuhusu feelings lonely.",
            "Ni vizuri kujua unavyoona feelings lonely.",
            "Unaweza kurudi kwenye feelings lonely wakati wowote - bado nitakuwepo.",
        ],
        "fr": [
            "Pas de pression - feelings lonely peut prendre tout le temps qu'il faut.",
            "C'est un beau sujet, feelings lonely - on continue ?",
            "Je suis toujours partant pour parler de feelings lonely.",
        ],
    },
    "FEELINGS_PROUD_RESPONSES": {
        "en": [
            "Good to know where you stand on feelings proud.",
            "I'm always up for talking feelings proud whenever you are.",
            "Worth sitting with for a second - feelings proud, that is.",
            "Honestly, feelings proud is a good thing to check in about.",
        ],
        "sw": [
            "Hilo ni wazo zuri kuhusu feelings proud, tuendelee?",
            "Nashukuru kunieleza kuhusu feelings proud.",
            "Njia yoyote unayotaka kuchukua kuhusu feelings proud inafaa kwangu.",
        ],
        "fr": [
            "Ça vaut la peine de s'arrêter un instant sur feelings proud.",
            "Pas de pression - feelings proud peut prendre tout le temps qu'il faut.",
            "Honnêtement, feelings proud vaut la peine d'en reparler.",
        ],
    },
    "FEELINGS_JEALOUS_RESPONSES": {
        "en": [
            "I'll remember you brought up feelings jealous.",
            "That's a fair way to look at feelings jealous.",
            "I appreciate you letting me in on feelings jealous.",
            "I'm following along on feelings jealous, keep going.",
        ],
        "sw": [
            "Hakuna haraka - feelings jealous inaweza kuchukua muda unaohitaji.",
            "Inafaa kutafakari kidogo kuhusu feelings jealous.",
            "Hilo ni wazo zuri kuhusu feelings jealous, tuendelee?",
        ],
        "fr": [
            "Ça vaut la peine de s'arrêter un instant sur feelings jealous.",
            "Tu peux revenir sur feelings jealous quand tu veux, je serai là.",
            "Honnêtement, feelings jealous vaut la peine d'en reparler.",
        ],
    },
    "FEELINGS_RELIEVED_RESPONSES": {
        "en": [
            "I'm following along on feelings relieved, keep going.",
            "Worth sitting with for a second - feelings relieved, that is.",
            "No rush - feelings relieved can take as long as you need.",
            "That's a nice thread on feelings relieved, want to keep pulling it?",
        ],
        "sw": [
            "Hilo ni wazo zuri kuhusu feelings relieved, tuendelee?",
            "Hakuna haraka - feelings relieved inaweza kuchukua muda unaohitaji.",
            "Njia yoyote unayotaka kuchukua kuhusu feelings relieved inafaa kwangu.",
        ],
        "fr": [
            "Je me souviendrai que tu as mentionné feelings relieved.",
            "Tu peux revenir sur feelings relieved quand tu veux, je serai là.",
            "Ça vaut la peine de s'arrêter un instant sur feelings relieved.",
        ],
    },
    "BOT_CAPABILITY_CURIOSITY_RESPONSES": {
        "en": [
            "No rush - bot capability curiosity can take as long as you need.",
            "You can circle back to bot capability curiosity any time - I'll still be here.",
            "I'm following along on bot capability curiosity, keep going.",
            "Good to know where you stand on bot capability curiosity.",
        ],
        "sw": [
            "Nashukuru kunieleza kuhusu bot capability curiosity.",
            "Kwa kweli, bot capability curiosity ni jambo zuri la kuzungumzia.",
            "Hakuna haraka - bot capability curiosity inaweza kuchukua muda unaohitaji.",
        ],
        "fr": [
            "C'est bon de savoir ce que tu penses de bot capability curiosity.",
            "Ça vaut la peine de s'arrêter un instant sur bot capability curiosity.",
            "Tu peux revenir sur bot capability curiosity quand tu veux, je serai là.",
        ],
    },
    "SMALL_TALK_WEATHER_CHECK_RESPONSES": {
        "en": [
            "You can circle back to small talk weather check any time - I'll still be here.",
            "However you want to take small talk weather check from here works for me.",
            "Honestly, small talk weather check is a good thing to check in about.",
            "I'm always up for talking small talk weather check whenever you are.",
        ],
        "sw": [
            "Hakuna haraka - small talk weather check inaweza kuchukua muda unaohitaji.",
            "Inafaa kutafakari kidogo kuhusu small talk weather check.",
            "Nashukuru kunieleza kuhusu small talk weather check.",
        ],
        "fr": [
            "Ça vaut la peine de s'arrêter un instant sur small talk weather check.",
            "Tu peux revenir sur small talk weather check quand tu veux, je serai là.",
            "C'est bon de savoir ce que tu penses de small talk weather check.",
        ],
    },
    "INTRODUCTION_REQUEST_RESPONSES": {
        "en": [
            "I'm following along on introduction request, keep going.",
            "I'm always up for talking introduction request whenever you are.",
            "No rush - introduction request can take as long as you need.",
            "I appreciate you letting me in on introduction request.",
        ],
        "sw": [
            "Kwa kweli, introduction request ni jambo zuri la kuzungumzia.",
            "Inafaa kutafakari kidogo kuhusu introduction request.",
            "Njia yoyote unayotaka kuchukua kuhusu introduction request inafaa kwangu.",
        ],
        "fr": [
            "C'est un beau sujet, introduction request - on continue ?",
            "Tu peux revenir sur introduction request quand tu veux, je serai là.",
            "Honnêtement, introduction request vaut la peine d'en reparler.",
        ],
    },
    "SMALL_TALK_BUSY_RESPONSES": {
        "en": [
            "You can circle back to small talk busy any time - I'll still be here.",
            "That's a fair way to look at small talk busy.",
            "I'm always up for talking small talk busy whenever you are.",
            "I'll remember you brought up small talk busy.",
        ],
        "sw": [
            "Njia yoyote unayotaka kuchukua kuhusu small talk busy inafaa kwangu.",
            "Ni vizuri kujua unavyoona small talk busy.",
            "Hakuna haraka - small talk busy inaweza kuchukua muda unaohitaji.",
        ],
        "fr": [
            "Ça vaut la peine de s'arrêter un instant sur small talk busy.",
            "Peu importe comment tu veux aborder small talk busy, ça me va.",
            "Merci de me parler de small talk busy.",
        ],
    },
    "POLITENESS_PLEASE_RESPONSES": {
        "en": [
            "I'm always up for talking politeness please whenever you are.",
            "That's a nice thread on politeness please, want to keep pulling it?",
            "Worth sitting with for a second - politeness please, that is.",
            "You can circle back to politeness please any time - I'll still be here.",
        ],
        "sw": [
            "Niko tayari kuzungumza kuhusu politeness please wakati wowote.",
            "Nashukuru kunieleza kuhusu politeness please.",
            "Ni vizuri kujua unavyoona politeness please.",
        ],
        "fr": [
            "Honnêtement, politeness please vaut la peine d'en reparler.",
            "Ça vaut la peine de s'arrêter un instant sur politeness please.",
            "Peu importe comment tu veux aborder politeness please, ça me va.",
        ],
    },
    "EXERCISE_FITNESS_RESPONSES": {
        "en": [
            "Worth sitting with for a second - exercise fitness, that is.",
            "Good to know where you stand on exercise fitness.",
            "That's a nice thread on exercise fitness, want to keep pulling it?",
            "I'm always up for talking exercise fitness whenever you are.",
        ],
        "sw": [
            "Ni vizuri kujua unavyoona exercise fitness.",
            "Nashukuru kunieleza kuhusu exercise fitness.",
            "Hakuna haraka - exercise fitness inaweza kuchukua muda unaohitaji.",
        ],
        "fr": [
            "Peu importe comment tu veux aborder exercise fitness, ça me va.",
            "Tu peux revenir sur exercise fitness quand tu veux, je serai là.",
            "Pas de pression - exercise fitness peut prendre tout le temps qu'il faut.",
        ],
    },
    "MENTAL_HEALTH_CHECKIN_RESPONSES": {
        "en": [
            "That's a fair way to look at mental health checkin.",
            "You can circle back to mental health checkin any time - I'll still be here.",
            "I appreciate you letting me in on mental health checkin.",
            "Honestly, mental health checkin is a good thing to check in about.",
        ],
        "sw": [
            "Hakuna haraka - mental health checkin inaweza kuchukua muda unaohitaji.",
            "Ni vizuri kujua unavyoona mental health checkin.",
            "Nashukuru kunieleza kuhusu mental health checkin.",
        ],
        "fr": [
            "Tu peux revenir sur mental health checkin quand tu veux, je serai là.",
            "C'est un beau sujet, mental health checkin - on continue ?",
            "Peu importe comment tu veux aborder mental health checkin, ça me va.",
        ],
    },
    "GRATITUDE_FOR_BOT_RESPONSES": {
        "en": [
            "No rush - gratitude for bot can take as long as you need.",
            "I'm following along on gratitude for bot, keep going.",
            "You can circle back to gratitude for bot any time - I'll still be here.",
            "I appreciate you letting me in on gratitude for bot.",
        ],
        "sw": [
            "Nashukuru kunieleza kuhusu gratitude for bot.",
            "Njia yoyote unayotaka kuchukua kuhusu gratitude for bot inafaa kwangu.",
            "Hakuna haraka - gratitude for bot inaweza kuchukua muda unaohitaji.",
        ],
        "fr": [
            "Je suis toujours partant pour parler de gratitude for bot.",
            "Ça vaut la peine de s'arrêter un instant sur gratitude for bot.",
            "Honnêtement, gratitude for bot vaut la peine d'en reparler.",
        ],
    },
    "REPEAT_CLARIFY_RESPONSES": {
        "en": [
            "I'll remember you brought up repeat clarify.",
            "That's a nice thread on repeat clarify, want to keep pulling it?",
            "I'm following along on repeat clarify, keep going.",
            "I'm always up for talking repeat clarify whenever you are.",
        ],
        "sw": [
            "Nitakumbuka ulizungumzia repeat clarify.",
            "Nashukuru kunieleza kuhusu repeat clarify.",
            "Hilo ni wazo zuri kuhusu repeat clarify, tuendelee?",
        ],
        "fr": [
            "Pas de pression - repeat clarify peut prendre tout le temps qu'il faut.",
            "Honnêtement, repeat clarify vaut la peine d'en reparler.",
            "Tu peux revenir sur repeat clarify quand tu veux, je serai là.",
        ],
    },
    "SMALL_CELEBRATION_RESPONSES": {
        "en": [
            "I'll remember you brought up small celebration.",
            "I'm always up for talking small celebration whenever you are.",
            "Worth sitting with for a second - small celebration, that is.",
            "No rush - small celebration can take as long as you need.",
        ],
        "sw": [
            "Unaweza kurudi kwenye small celebration wakati wowote - bado nitakuwepo.",
            "Inafaa kutafakari kidogo kuhusu small celebration.",
            "Kwa kweli, small celebration ni jambo zuri la kuzungumzia.",
        ],
        "fr": [
            "Je suis toujours partant pour parler de small celebration.",
            "Honnêtement, small celebration vaut la peine d'en reparler.",
            "C'est un beau sujet, small celebration - on continue ?",
        ],
    },
    "FORECAST_QUESTION_RESPONSES": {
        "en": [
            "I'm following along on forecast question, keep going.",
            "Honestly, forecast question is a good thing to check in about.",
            "I'll remember you brought up forecast question.",
            "That's a nice thread on forecast question, want to keep pulling it?",
        ],
        "sw": [
            "Hakuna haraka - forecast question inaweza kuchukua muda unaohitaji.",
            "Nitakumbuka ulizungumzia forecast question.",
            "Ni vizuri kujua unavyoona forecast question.",
        ],
        "fr": [
            "Honnêtement, forecast question vaut la peine d'en reparler.",
            "C'est un beau sujet, forecast question - on continue ?",
            "C'est bon de savoir ce que tu penses de forecast question.",
        ],
    },
    "LANGUAGE_PRACTICE_RESPONSES": {
        "en": [
            "Good to know where you stand on language practice.",
            "That's a nice thread on language practice, want to keep pulling it?",
            "You can circle back to language practice any time - I'll still be here.",
            "However you want to take language practice from here works for me.",
        ],
        "sw": [
            "Unaweza kurudi kwenye language practice wakati wowote - bado nitakuwepo.",
            "Ni vizuri kujua unavyoona language practice.",
            "Nitakumbuka ulizungumzia language practice.",
        ],
        "fr": [
            "Merci de me parler de language practice.",
            "Honnêtement, language practice vaut la peine d'en reparler.",
            "Pas de pression - language practice peut prendre tout le temps qu'il faut.",
        ],
    },
    "BOT_AGE_LOCATION_RESPONSES": {
        "en": [
            "I appreciate you letting me in on bot age location.",
            "Honestly, bot age location is a good thing to check in about.",
            "That's a fair way to look at bot age location.",
            "That's a nice thread on bot age location, want to keep pulling it?",
        ],
        "sw": [
            "Ni vizuri kujua unavyoona bot age location.",
            "Njia yoyote unayotaka kuchukua kuhusu bot age location inafaa kwangu.",
            "Inafaa kutafakari kidogo kuhusu bot age location.",
        ],
        "fr": [
            "Je me souviendrai que tu as mentionné bot age location.",
            "Tu peux revenir sur bot age location quand tu veux, je serai là.",
            "Merci de me parler de bot age location.",
        ],
    },
    "BOT_NAME_OPINION_RESPONSES": {
        "en": [
            "Good to know where you stand on bot name opinion.",
            "Worth sitting with for a second - bot name opinion, that is.",
            "You can circle back to bot name opinion any time - I'll still be here.",
            "Honestly, bot name opinion is a good thing to check in about.",
        ],
        "sw": [
            "Inafaa kutafakari kidogo kuhusu bot name opinion.",
            "Ni vizuri kujua unavyoona bot name opinion.",
            "Hilo ni wazo zuri kuhusu bot name opinion, tuendelee?",
        ],
        "fr": [
            "Peu importe comment tu veux aborder bot name opinion, ça me va.",
            "Merci de me parler de bot name opinion.",
            "Tu peux revenir sur bot name opinion quand tu veux, je serai là.",
        ],
    },
    "SLOW_DOWN_RESPONSES": {
        "en": [
            "No rush - slow down can take as long as you need.",
            "I appreciate you letting me in on slow down.",
            "I'll remember you brought up slow down.",
            "I'm always up for talking slow down whenever you are.",
        ],
        "sw": [
            "Njia yoyote unayotaka kuchukua kuhusu slow down inafaa kwangu.",
            "Ni vizuri kujua unavyoona slow down.",
            "Nashukuru kunieleza kuhusu slow down.",
        ],
        "fr": [
            "C'est bon de savoir ce que tu penses de slow down.",
            "Merci de me parler de slow down.",
            "Je me souviendrai que tu as mentionné slow down.",
        ],
    },
    "AWKWARD_PAUSE_RESPONSES": {
        "en": [
            "Honestly, awkward pause is a good thing to check in about.",
            "No rush - awkward pause can take as long as you need.",
            "You can circle back to awkward pause any time - I'll still be here.",
            "I'm following along on awkward pause, keep going.",
        ],
        "sw": [
            "Nashukuru kunieleza kuhusu awkward pause.",
            "Hilo ni wazo zuri kuhusu awkward pause, tuendelee?",
            "Unaweza kurudi kwenye awkward pause wakati wowote - bado nitakuwepo.",
        ],
        "fr": [
            "Honnêtement, awkward pause vaut la peine d'en reparler.",
            "Tu peux revenir sur awkward pause quand tu veux, je serai là.",
            "C'est un beau sujet, awkward pause - on continue ?",
        ],
    },
    "COMPLIMENT_RESPONSE_RESPONSES": {
        "en": [
            "I appreciate you letting me in on compliment response.",
            "I'm following along on compliment response, keep going.",
            "Worth sitting with for a second - compliment response, that is.",
            "However you want to take compliment response from here works for me.",
        ],
        "sw": [
            "Inafaa kutafakari kidogo kuhusu compliment response.",
            "Njia yoyote unayotaka kuchukua kuhusu compliment response inafaa kwangu.",
            "Unaweza kurudi kwenye compliment response wakati wowote - bado nitakuwepo.",
        ],
        "fr": [
            "Merci de me parler de compliment response.",
            "Ça vaut la peine de s'arrêter un instant sur compliment response.",
            "Tu peux revenir sur compliment response quand tu veux, je serai là.",
        ],
    },
    "REMEMBER_SPECIFIC_RESPONSES": {
        "en": [
            "Honestly, remember specific is a good thing to check in about.",
            "You can circle back to remember specific any time - I'll still be here.",
            "No rush - remember specific can take as long as you need.",
            "I'll remember you brought up remember specific.",
        ],
        "sw": [
            "Nitakumbuka ulizungumzia remember specific.",
            "Nashukuru kunieleza kuhusu remember specific.",
            "Ni vizuri kujua unavyoona remember specific.",
        ],
        "fr": [
            "Ça vaut la peine de s'arrêter un instant sur remember specific.",
            "Tu peux revenir sur remember specific quand tu veux, je serai là.",
            "C'est bon de savoir ce que tu penses de remember specific.",
        ],
    },
    "TODAY_PLANS_RESPONSES": {
        "en": [
            "Good to know where you stand on today plans.",
            "You can circle back to today plans any time - I'll still be here.",
            "I'm following along on today plans, keep going.",
            "Honestly, today plans is a good thing to check in about.",
        ],
        "sw": [
            "Hakuna haraka - today plans inaweza kuchukua muda unaohitaji.",
            "Njia yoyote unayotaka kuchukua kuhusu today plans inafaa kwangu.",
            "Unaweza kurudi kwenye today plans wakati wowote - bado nitakuwepo.",
        ],
        "fr": [
            "Je me souviendrai que tu as mentionné today plans.",
            "C'est un beau sujet, today plans - on continue ?",
            "Je suis toujours partant pour parler de today plans.",
        ],
    },
    "TECHNOLOGY_COMPLAINT_RESPONSES": {
        "en": [
            "I'm following along on technology complaint, keep going.",
            "However you want to take technology complaint from here works for me.",
            "Worth sitting with for a second - technology complaint, that is.",
            "That's a fair way to look at technology complaint.",
        ],
        "sw": [
            "Hakuna haraka - technology complaint inaweza kuchukua muda unaohitaji.",
            "Inafaa kutafakari kidogo kuhusu technology complaint.",
            "Ni vizuri kujua unavyoona technology complaint.",
        ],
        "fr": [
            "C'est un beau sujet, technology complaint - on continue ?",
            "Je suis toujours partant pour parler de technology complaint.",
            "Pas de pression - technology complaint peut prendre tout le temps qu'il faut.",
        ],
    },
    "ASPIRATIONS_DREAMS_RESPONSES": {
        "en": [
            "That's a nice thread on aspirations dreams, want to keep pulling it?",
            "That's a fair way to look at aspirations dreams.",
            "I'm following along on aspirations dreams, keep going.",
            "However you want to take aspirations dreams from here works for me.",
        ],
        "sw": [
            "Unaweza kurudi kwenye aspirations dreams wakati wowote - bado nitakuwepo.",
            "Hilo ni wazo zuri kuhusu aspirations dreams, tuendelee?",
            "Njia yoyote unayotaka kuchukua kuhusu aspirations dreams inafaa kwangu.",
        ],
        "fr": [
            "C'est un beau sujet, aspirations dreams - on continue ?",
            "Ça vaut la peine de s'arrêter un instant sur aspirations dreams.",
            "Je suis toujours partant pour parler de aspirations dreams.",
        ],
    },
    "MISSING_SOMEONE_RESPONSES": {
        "en": [
            "You can circle back to missing someone any time - I'll still be here.",
            "Honestly, missing someone is a good thing to check in about.",
            "That's a fair way to look at missing someone.",
            "I'm always up for talking missing someone whenever you are.",
        ],
        "sw": [
            "Nitakumbuka ulizungumzia missing someone.",
            "Njia yoyote unayotaka kuchukua kuhusu missing someone inafaa kwangu.",
            "Hilo ni wazo zuri kuhusu missing someone, tuendelee?",
        ],
        "fr": [
            "Merci de me parler de missing someone.",
            "Je me souviendrai que tu as mentionné missing someone.",
            "Ça vaut la peine de s'arrêter un instant sur missing someone.",
        ],
    },
    "EXCITEMENT_EVENT_RESPONSES": {
        "en": [
            "No rush - excitement event can take as long as you need.",
            "Honestly, excitement event is a good thing to check in about.",
            "You can circle back to excitement event any time - I'll still be here.",
            "I'm following along on excitement event, keep going.",
        ],
        "sw": [
            "Njia yoyote unayotaka kuchukua kuhusu excitement event inafaa kwangu.",
            "Ni vizuri kujua unavyoona excitement event.",
            "Inafaa kutafakari kidogo kuhusu excitement event.",
        ],
        "fr": [
            "Merci de me parler de excitement event.",
            "Tu peux revenir sur excitement event quand tu veux, je serai là.",
            "Pas de pression - excitement event peut prendre tout le temps qu'il faut.",
        ],
    },
    "DISAPPOINTMENT_RESPONSES": {
        "en": [
            "I'll remember you brought up disappointment.",
            "Good to know where you stand on disappointment.",
            "Worth sitting with for a second - disappointment, that is.",
            "You can circle back to disappointment any time - I'll still be here.",
        ],
        "sw": [
            "Nitakumbuka ulizungumzia disappointment.",
            "Ni vizuri kujua unavyoona disappointment.",
            "Hakuna haraka - disappointment inaweza kuchukua muda unaohitaji.",
        ],
        "fr": [
            "Tu peux revenir sur disappointment quand tu veux, je serai là.",
            "Je me souviendrai que tu as mentionné disappointment.",
            "Pas de pression - disappointment peut prendre tout le temps qu'il faut.",
        ],
    },
    "CHAT_META_RESPONSES": {
        "en": [
            "Good to know where you stand on chat meta.",
            "I'm following along on chat meta, keep going.",
            "I appreciate you letting me in on chat meta.",
            "No rush - chat meta can take as long as you need.",
        ],
        "sw": [
            "Nitakumbuka ulizungumzia chat meta.",
            "Ni vizuri kujua unavyoona chat meta.",
            "Niko tayari kuzungumza kuhusu chat meta wakati wowote.",
        ],
        "fr": [
            "Je me souviendrai que tu as mentionné chat meta.",
            "Honnêtement, chat meta vaut la peine d'en reparler.",
            "C'est bon de savoir ce que tu penses de chat meta.",
        ],
    },
    "SEASON_SPRING_RESPONSES": {
        "en": [
            "That's a nice thread on season spring, want to keep pulling it?",
            "I'm always up for talking season spring whenever you are.",
            "Worth sitting with for a second - season spring, that is.",
            "I'll remember you brought up season spring.",
        ],
        "sw": [
            "Kwa kweli, season spring ni jambo zuri la kuzungumzia.",
            "Njia yoyote unayotaka kuchukua kuhusu season spring inafaa kwangu.",
            "Hakuna haraka - season spring inaweza kuchukua muda unaohitaji.",
        ],
        "fr": [
            "Ça vaut la peine de s'arrêter un instant sur season spring.",
            "Honnêtement, season spring vaut la peine d'en reparler.",
            "C'est un beau sujet, season spring - on continue ?",
        ],
    },
    "SEASON_SUMMER_RESPONSES": {
        "en": [
            "You can circle back to season summer any time - I'll still be here.",
            "I'm always up for talking season summer whenever you are.",
            "No rush - season summer can take as long as you need.",
            "However you want to take season summer from here works for me.",
        ],
        "sw": [
            "Hakuna haraka - season summer inaweza kuchukua muda unaohitaji.",
            "Kwa kweli, season summer ni jambo zuri la kuzungumzia.",
            "Niko tayari kuzungumza kuhusu season summer wakati wowote.",
        ],
        "fr": [
            "Tu peux revenir sur season summer quand tu veux, je serai là.",
            "C'est un beau sujet, season summer - on continue ?",
            "C'est bon de savoir ce que tu penses de season summer.",
        ],
    },
    "SEASON_AUTUMN_RESPONSES": {
        "en": [
            "That's a nice thread on season autumn, want to keep pulling it?",
            "I appreciate you letting me in on season autumn.",
            "Honestly, season autumn is a good thing to check in about.",
            "Worth sitting with for a second - season autumn, that is.",
        ],
        "sw": [
            "Kwa kweli, season autumn ni jambo zuri la kuzungumzia.",
            "Ni vizuri kujua unavyoona season autumn.",
            "Hilo ni wazo zuri kuhusu season autumn, tuendelee?",
        ],
        "fr": [
            "Honnêtement, season autumn vaut la peine d'en reparler.",
            "C'est un beau sujet, season autumn - on continue ?",
            "Pas de pression - season autumn peut prendre tout le temps qu'il faut.",
        ],
    },
    "SEASON_WINTER_RESPONSES": {
        "en": [
            "Good to know where you stand on season winter.",
            "That's a nice thread on season winter, want to keep pulling it?",
            "That's a fair way to look at season winter.",
            "No rush - season winter can take as long as you need.",
        ],
        "sw": [
            "Kwa kweli, season winter ni jambo zuri la kuzungumzia.",
            "Unaweza kurudi kwenye season winter wakati wowote - bado nitakuwepo.",
            "Nitakumbuka ulizungumzia season winter.",
        ],
        "fr": [
            "Merci de me parler de season winter.",
            "Je me souviendrai que tu as mentionné season winter.",
            "Ça vaut la peine de s'arrêter un instant sur season winter.",
        ],
    },
    "NIGHTMARE_RESPONSES": {
        "en": [
            "Worth sitting with for a second - nightmare, that is.",
            "I'm following along on nightmare, keep going.",
            "That's a fair way to look at nightmare.",
            "That's a nice thread on nightmare, want to keep pulling it?",
        ],
        "sw": [
            "Nashukuru kunieleza kuhusu nightmare.",
            "Kwa kweli, nightmare ni jambo zuri la kuzungumzia.",
            "Nitakumbuka ulizungumzia nightmare.",
        ],
        "fr": [
            "Je suis toujours partant pour parler de nightmare.",
            "Tu peux revenir sur nightmare quand tu veux, je serai là.",
            "Honnêtement, nightmare vaut la peine d'en reparler.",
        ],
    },
    "TRAFFIC_RESPONSES": {
        "en": [
            "That's a nice thread on traffic, want to keep pulling it?",
            "However you want to take traffic from here works for me.",
            "I appreciate you letting me in on traffic.",
            "Worth sitting with for a second - traffic, that is.",
        ],
        "sw": [
            "Inafaa kutafakari kidogo kuhusu traffic.",
            "Unaweza kurudi kwenye traffic wakati wowote - bado nitakuwepo.",
            "Nitakumbuka ulizungumzia traffic.",
        ],
        "fr": [
            "Ça vaut la peine de s'arrêter un instant sur traffic.",
            "Merci de me parler de traffic.",
            "Je me souviendrai que tu as mentionné traffic.",
        ],
    },
    "NEWS_RESPONSES": {
        "en": [
            "That's a fair way to look at news.",
            "I'll remember you brought up news.",
            "Honestly, news is a good thing to check in about.",
            "I'm following along on news, keep going.",
        ],
        "sw": [
            "Kwa kweli, news ni jambo zuri la kuzungumzia.",
            "Nashukuru kunieleza kuhusu news.",
            "Niko tayari kuzungumza kuhusu news wakati wowote.",
        ],
        "fr": [
            "Ça vaut la peine de s'arrêter un instant sur news.",
            "Je suis toujours partant pour parler de news.",
            "Honnêtement, news vaut la peine d'en reparler.",
        ],
    },
    "COLOR_PREFERENCE_RESPONSES": {
        "en": [
            "However you want to take color preference from here works for me.",
            "Worth sitting with for a second - color preference, that is.",
            "Honestly, color preference is a good thing to check in about.",
            "You can circle back to color preference any time - I'll still be here.",
        ],
        "sw": [
            "Inafaa kutafakari kidogo kuhusu color preference.",
            "Ni vizuri kujua unavyoona color preference.",
            "Hakuna haraka - color preference inaweza kuchukua muda unaohitaji.",
        ],
        "fr": [
            "C'est bon de savoir ce que tu penses de color preference.",
            "Ça vaut la peine de s'arrêter un instant sur color preference.",
            "Merci de me parler de color preference.",
        ],
    },
    "STUDYING_EXAM_RESPONSES": {
        "en": [
            "Worth sitting with for a second - studying exam, that is.",
            "I appreciate you letting me in on studying exam.",
            "However you want to take studying exam from here works for me.",
            "You can circle back to studying exam any time - I'll still be here.",
        ],
        "sw": [
            "Ni vizuri kujua unavyoona studying exam.",
            "Hilo ni wazo zuri kuhusu studying exam, tuendelee?",
            "Nashukuru kunieleza kuhusu studying exam.",
        ],
        "fr": [
            "Pas de pression - studying exam peut prendre tout le temps qu'il faut.",
            "Je suis toujours partant pour parler de studying exam.",
            "C'est bon de savoir ce que tu penses de studying exam.",
        ],
    },
    "GARDENING_PLANTS_RESPONSES": {
        "en": [
            "That's a fair way to look at gardening plants.",
            "I'll remember you brought up gardening plants.",
            "I'm always up for talking gardening plants whenever you are.",
            "Good to know where you stand on gardening plants.",
        ],
        "sw": [
            "Hilo ni wazo zuri kuhusu gardening plants, tuendelee?",
            "Niko tayari kuzungumza kuhusu gardening plants wakati wowote.",
            "Inafaa kutafakari kidogo kuhusu gardening plants.",
        ],
        "fr": [
            "Peu importe comment tu veux aborder gardening plants, ça me va.",
            "Ça vaut la peine de s'arrêter un instant sur gardening plants.",
            "C'est un beau sujet, gardening plants - on continue ?",
        ],
    },
    "SHOPPING_RESPONSES": {
        "en": [
            "That's a nice thread on shopping, want to keep pulling it?",
            "Honestly, shopping is a good thing to check in about.",
            "You can circle back to shopping any time - I'll still be here.",
            "No rush - shopping can take as long as you need.",
        ],
        "sw": [
            "Nashukuru kunieleza kuhusu shopping.",
            "Hakuna haraka - shopping inaweza kuchukua muda unaohitaji.",
            "Njia yoyote unayotaka kuchukua kuhusu shopping inafaa kwangu.",
        ],
        "fr": [
            "Tu peux revenir sur shopping quand tu veux, je serai là.",
            "Honnêtement, shopping vaut la peine d'en reparler.",
            "Ça vaut la peine de s'arrêter un instant sur shopping.",
        ],
    },
    "MOVIES_TV_RESPONSES": {
        "en": [
            "Worth sitting with for a second - movies tv, that is.",
            "That's a nice thread on movies tv, want to keep pulling it?",
            "However you want to take movies tv from here works for me.",
            "I appreciate you letting me in on movies tv.",
        ],
        "sw": [
            "Nitakumbuka ulizungumzia movies tv.",
            "Unaweza kurudi kwenye movies tv wakati wowote - bado nitakuwepo.",
            "Hakuna haraka - movies tv inaweza kuchukua muda unaohitaji.",
        ],
        "fr": [
            "C'est bon de savoir ce que tu penses de movies tv.",
            "Honnêtement, movies tv vaut la peine d'en reparler.",
            "Pas de pression - movies tv peut prendre tout le temps qu'il faut.",
        ],
    },
    "COFFEE_TEA_RESPONSES": {
        "en": [
            "You can circle back to coffee tea any time - I'll still be here.",
            "Honestly, coffee tea is a good thing to check in about.",
            "I appreciate you letting me in on coffee tea.",
            "Worth sitting with for a second - coffee tea, that is.",
        ],
        "sw": [
            "Nitakumbuka ulizungumzia coffee tea.",
            "Unaweza kurudi kwenye coffee tea wakati wowote - bado nitakuwepo.",
            "Kwa kweli, coffee tea ni jambo zuri la kuzungumzia.",
        ],
        "fr": [
            "Tu peux revenir sur coffee tea quand tu veux, je serai là.",
            "Merci de me parler de coffee tea.",
            "Ça vaut la peine de s'arrêter un instant sur coffee tea.",
        ],
    },
    "EXAM_RESULTS_RESPONSES": {
        "en": [
            "Good to know where you stand on exam results.",
            "I appreciate you letting me in on exam results.",
            "That's a nice thread on exam results, want to keep pulling it?",
            "Worth sitting with for a second - exam results, that is.",
        ],
        "sw": [
            "Hilo ni wazo zuri kuhusu exam results, tuendelee?",
            "Kwa kweli, exam results ni jambo zuri la kuzungumzia.",
            "Ni vizuri kujua unavyoona exam results.",
        ],
        "fr": [
            "Merci de me parler de exam results.",
            "Peu importe comment tu veux aborder exam results, ça me va.",
            "Je suis toujours partant pour parler de exam results.",
        ],
    },
    "PARTY_EVENT_RESPONSES": {
        "en": [
            "Good to know where you stand on party event.",
            "I'm always up for talking party event whenever you are.",
            "No rush - party event can take as long as you need.",
            "You can circle back to party event any time - I'll still be here.",
        ],
        "sw": [
            "Kwa kweli, party event ni jambo zuri la kuzungumzia.",
            "Hilo ni wazo zuri kuhusu party event, tuendelee?",
            "Inafaa kutafakari kidogo kuhusu party event.",
        ],
        "fr": [
            "Je me souviendrai que tu as mentionné party event.",
            "Peu importe comment tu veux aborder party event, ça me va.",
            "Ça vaut la peine de s'arrêter un instant sur party event.",
        ],
    },
    "SIBLINGS_RESPONSES": {
        "en": [
            "You can circle back to siblings any time - I'll still be here.",
            "Good to know where you stand on siblings.",
            "That's a nice thread on siblings, want to keep pulling it?",
            "That's a fair way to look at siblings.",
        ],
        "sw": [
            "Njia yoyote unayotaka kuchukua kuhusu siblings inafaa kwangu.",
            "Hakuna haraka - siblings inaweza kuchukua muda unaohitaji.",
            "Nitakumbuka ulizungumzia siblings.",
        ],
        "fr": [
            "Merci de me parler de siblings.",
            "Peu importe comment tu veux aborder siblings, ça me va.",
            "C'est un beau sujet, siblings - on continue ?",
        ],
    },
    "CAREER_CHANGE_RESPONSES": {
        "en": [
            "I'll remember you brought up career change.",
            "That's a nice thread on career change, want to keep pulling it?",
            "I appreciate you letting me in on career change.",
            "No rush - career change can take as long as you need.",
        ],
        "sw": [
            "Kwa kweli, career change ni jambo zuri la kuzungumzia.",
            "Hilo ni wazo zuri kuhusu career change, tuendelee?",
            "Inafaa kutafakari kidogo kuhusu career change.",
        ],
        "fr": [
            "Je me souviendrai que tu as mentionné career change.",
            "C'est un beau sujet, career change - on continue ?",
            "Je suis toujours partant pour parler de career change.",
        ],
    },
    "VOLUNTEER_WORK_RESPONSES": {
        "en": [
            "No rush - volunteer work can take as long as you need.",
            "Honestly, volunteer work is a good thing to check in about.",
            "You can circle back to volunteer work any time - I'll still be here.",
            "That's a fair way to look at volunteer work.",
        ],
        "sw": [
            "Hilo ni wazo zuri kuhusu volunteer work, tuendelee?",
            "Nashukuru kunieleza kuhusu volunteer work.",
            "Njia yoyote unayotaka kuchukua kuhusu volunteer work inafaa kwangu.",
        ],
        "fr": [
            "Honnêtement, volunteer work vaut la peine d'en reparler.",
            "Je suis toujours partant pour parler de volunteer work.",
            "Pas de pression - volunteer work peut prendre tout le temps qu'il faut.",
        ],
    },
    "SPIRITUALITY_RESPONSES": {
        "en": [
            "You can circle back to spirituality any time - I'll still be here.",
            "Honestly, spirituality is a good thing to check in about.",
            "That's a nice thread on spirituality, want to keep pulling it?",
            "I'm always up for talking spirituality whenever you are.",
        ],
        "sw": [
            "Niko tayari kuzungumza kuhusu spirituality wakati wowote.",
            "Ni vizuri kujua unavyoona spirituality.",
            "Hakuna haraka - spirituality inaweza kuchukua muda unaohitaji.",
        ],
        "fr": [
            "Je suis toujours partant pour parler de spirituality.",
            "Honnêtement, spirituality vaut la peine d'en reparler.",
            "Merci de me parler de spirituality.",
        ],
    },
    "POLITICS_DEFLECT_RESPONSES": {
        "en": [
            "Worth sitting with for a second - politics deflect, that is.",
            "I'm following along on politics deflect, keep going.",
            "You can circle back to politics deflect any time - I'll still be here.",
            "I'll remember you brought up politics deflect.",
        ],
        "sw": [
            "Njia yoyote unayotaka kuchukua kuhusu politics deflect inafaa kwangu.",
            "Kwa kweli, politics deflect ni jambo zuri la kuzungumzia.",
            "Ni vizuri kujua unavyoona politics deflect.",
        ],
        "fr": [
            "Tu peux revenir sur politics deflect quand tu veux, je serai là.",
            "Je me souviendrai que tu as mentionné politics deflect.",
            "C'est un beau sujet, politics deflect - on continue ?",
        ],
    },
    "SILENCE_FILLER_RESPONSES": {
        "en": [
            "No rush - silence filler can take as long as you need.",
            "I'll remember you brought up silence filler.",
            "Worth sitting with for a second - silence filler, that is.",
            "I'm always up for talking silence filler whenever you are.",
        ],
        "sw": [
            "Inafaa kutafakari kidogo kuhusu silence filler.",
            "Unaweza kurudi kwenye silence filler wakati wowote - bado nitakuwepo.",
            "Nashukuru kunieleza kuhusu silence filler.",
        ],
        "fr": [
            "Merci de me parler de silence filler.",
            "Honnêtement, silence filler vaut la peine d'en reparler.",
            "C'est un beau sujet, silence filler - on continue ?",
        ],
    },
    "DIRECTIONS_RECOMMENDATION_RESPONSES": {
        "en": [
            "That's a fair way to look at directions recommendation.",
            "That's a nice thread on directions recommendation, want to keep pulling it?",
            "Honestly, directions recommendation is a good thing to check in about.",
            "No rush - directions recommendation can take as long as you need.",
        ],
        "sw": [
            "Hakuna haraka - directions recommendation inaweza kuchukua muda unaohitaji.",
            "Inafaa kutafakari kidogo kuhusu directions recommendation.",
            "Hilo ni wazo zuri kuhusu directions recommendation, tuendelee?",
        ],
        "fr": [
            "C'est bon de savoir ce que tu penses de directions recommendation.",
            "Je me souviendrai que tu as mentionné directions recommendation.",
            "Je suis toujours partant pour parler de directions recommendation.",
        ],
    },
    "NAME_RECOGNITION_RESPONSES": {
        "en": [
            "I appreciate you letting me in on name recognition.",
            "No rush - name recognition can take as long as you need.",
            "However you want to take name recognition from here works for me.",
            "That's a nice thread on name recognition, want to keep pulling it?",
        ],
        "sw": [
            "Niko tayari kuzungumza kuhusu name recognition wakati wowote.",
            "Kwa kweli, name recognition ni jambo zuri la kuzungumzia.",
            "Unaweza kurudi kwenye name recognition wakati wowote - bado nitakuwepo.",
        ],
        "fr": [
            "Je me souviendrai que tu as mentionné name recognition.",
            "Je suis toujours partant pour parler de name recognition.",
            "Tu peux revenir sur name recognition quand tu veux, je serai là.",
        ],
    },
    "GENERAL_CURIOSITY_RESPONSES": {
        "en": [
            "That's a nice thread on general curiosity, want to keep pulling it?",
            "You can circle back to general curiosity any time - I'll still be here.",
            "That's a fair way to look at general curiosity.",
            "However you want to take general curiosity from here works for me.",
        ],
        "sw": [
            "Niko tayari kuzungumza kuhusu general curiosity wakati wowote.",
            "Nashukuru kunieleza kuhusu general curiosity.",
            "Ni vizuri kujua unavyoona general curiosity.",
        ],
        "fr": [
            "C'est un beau sujet, general curiosity - on continue ?",
            "C'est bon de savoir ce que tu penses de general curiosity.",
            "Honnêtement, general curiosity vaut la peine d'en reparler.",
        ],
    },
    "LAUGHTER_RESPONSES": {
        "en": [
            "That's a fair way to look at laughter.",
            "Good to know where you stand on laughter.",
            "I'll remember you brought up laughter.",
            "I'm following along on laughter, keep going.",
        ],
        "sw": [
            "Ni vizuri kujua unavyoona laughter.",
            "Nashukuru kunieleza kuhusu laughter.",
            "Hakuna haraka - laughter inaweza kuchukua muda unaohitaji.",
        ],
        "fr": [
            "Pas de pression - laughter peut prendre tout le temps qu'il faut.",
            "Je me souviendrai que tu as mentionné laughter.",
            "Tu peux revenir sur laughter quand tu veux, je serai là.",
        ],
    },
    "CRYING_RESPONSES": {
        "en": [
            "No rush - crying can take as long as you need.",
            "I'll remember you brought up crying.",
            "I'm following along on crying, keep going.",
            "Worth sitting with for a second - crying, that is.",
        ],
        "sw": [
            "Nitakumbuka ulizungumzia crying.",
            "Hilo ni wazo zuri kuhusu crying, tuendelee?",
            "Niko tayari kuzungumza kuhusu crying wakati wowote.",
        ],
        "fr": [
            "Tu peux revenir sur crying quand tu veux, je serai là.",
            "Je suis toujours partant pour parler de crying.",
            "Pas de pression - crying peut prendre tout le temps qu'il faut.",
        ],
    },
    "MILD_FRUSTRATION_RESPONSES": {
        "en": [
            "You can circle back to mild frustration any time - I'll still be here.",
            "Good to know where you stand on mild frustration.",
            "That's a nice thread on mild frustration, want to keep pulling it?",
            "No rush - mild frustration can take as long as you need.",
        ],
        "sw": [
            "Unaweza kurudi kwenye mild frustration wakati wowote - bado nitakuwepo.",
            "Hakuna haraka - mild frustration inaweza kuchukua muda unaohitaji.",
            "Njia yoyote unayotaka kuchukua kuhusu mild frustration inafaa kwangu.",
        ],
        "fr": [
            "Merci de me parler de mild frustration.",
            "Honnêtement, mild frustration vaut la peine d'en reparler.",
            "C'est bon de savoir ce que tu penses de mild frustration.",
        ],
    },
    "BOT_FAVORITE_THINGS_RESPONSES": {
        "en": [
            "However you want to take bot favorite things from here works for me.",
            "You can circle back to bot favorite things any time - I'll still be here.",
            "Worth sitting with for a second - bot favorite things, that is.",
            "Honestly, bot favorite things is a good thing to check in about.",
        ],
        "sw": [
            "Niko tayari kuzungumza kuhusu bot favorite things wakati wowote.",
            "Hilo ni wazo zuri kuhusu bot favorite things, tuendelee?",
            "Nashukuru kunieleza kuhusu bot favorite things.",
        ],
        "fr": [
            "Ça vaut la peine de s'arrêter un instant sur bot favorite things.",
            "Tu peux revenir sur bot favorite things quand tu veux, je serai là.",
            "Pas de pression - bot favorite things peut prendre tout le temps qu'il faut.",
        ],
    },
    "BIRDS_FISH_RESPONSES": {
        "en": [
            "That's a fair way to look at birds fish.",
            "I'll remember you brought up birds fish.",
            "Worth sitting with for a second - birds fish, that is.",
            "I'm following along on birds fish, keep going.",
        ],
        "sw": [
            "Unaweza kurudi kwenye birds fish wakati wowote - bado nitakuwepo.",
            "Inafaa kutafakari kidogo kuhusu birds fish.",
            "Hakuna haraka - birds fish inaweza kuchukua muda unaohitaji.",
        ],
        "fr": [
            "C'est un beau sujet, birds fish - on continue ?",
            "C'est bon de savoir ce que tu penses de birds fish.",
            "Merci de me parler de birds fish.",
        ],
    },
    "COMMUTE_TRANSPORT_RESPONSES": {
        "en": [
            "I appreciate you letting me in on commute transport.",
            "That's a nice thread on commute transport, want to keep pulling it?",
            "Good to know where you stand on commute transport.",
            "No rush - commute transport can take as long as you need.",
        ],
        "sw": [
            "Ni vizuri kujua unavyoona commute transport.",
            "Niko tayari kuzungumza kuhusu commute transport wakati wowote.",
            "Nitakumbuka ulizungumzia commute transport.",
        ],
        "fr": [
            "C'est bon de savoir ce que tu penses de commute transport.",
            "Tu peux revenir sur commute transport quand tu veux, je serai là.",
            "Je me souviendrai que tu as mentionné commute transport.",
        ],
    },
    "ALLERGIES_RESPONSES": {
        "en": [
            "I appreciate you letting me in on allergies.",
            "That's a fair way to look at allergies.",
            "I'm following along on allergies, keep going.",
            "I'll remember you brought up allergies.",
        ],
        "sw": [
            "Unaweza kurudi kwenye allergies wakati wowote - bado nitakuwepo.",
            "Hilo ni wazo zuri kuhusu allergies, tuendelee?",
            "Nashukuru kunieleza kuhusu allergies.",
        ],
        "fr": [
            "Honnêtement, allergies vaut la peine d'en reparler.",
            "Pas de pression - allergies peut prendre tout le temps qu'il faut.",
            "Je me souviendrai que tu as mentionné allergies.",
        ],
    },
    "DIET_NUTRITION_RESPONSES": {
        "en": [
            "I appreciate you letting me in on diet nutrition.",
            "Honestly, diet nutrition is a good thing to check in about.",
            "Worth sitting with for a second - diet nutrition, that is.",
            "That's a fair way to look at diet nutrition.",
        ],
        "sw": [
            "Njia yoyote unayotaka kuchukua kuhusu diet nutrition inafaa kwangu.",
            "Unaweza kurudi kwenye diet nutrition wakati wowote - bado nitakuwepo.",
            "Nashukuru kunieleza kuhusu diet nutrition.",
        ],
        "fr": [
            "Pas de pression - diet nutrition peut prendre tout le temps qu'il faut.",
            "Je suis toujours partant pour parler de diet nutrition.",
            "Tu peux revenir sur diet nutrition quand tu veux, je serai là.",
        ],
    },
    "SLEEP_SCHEDULE_RESPONSES": {
        "en": [
            "However you want to take sleep schedule from here works for me.",
            "No rush - sleep schedule can take as long as you need.",
            "Good to know where you stand on sleep schedule.",
            "You can circle back to sleep schedule any time - I'll still be here.",
        ],
        "sw": [
            "Hakuna haraka - sleep schedule inaweza kuchukua muda unaohitaji.",
            "Inafaa kutafakari kidogo kuhusu sleep schedule.",
            "Hilo ni wazo zuri kuhusu sleep schedule, tuendelee?",
        ],
        "fr": [
            "Tu peux revenir sur sleep schedule quand tu veux, je serai là.",
            "Honnêtement, sleep schedule vaut la peine d'en reparler.",
            "Je suis toujours partant pour parler de sleep schedule.",
        ],
    },
    "PHOTOGRAPHY_ART_RESPONSES": {
        "en": [
            "I'll remember you brought up photography art.",
            "I'm always up for talking photography art whenever you are.",
            "Good to know where you stand on photography art.",
            "However you want to take photography art from here works for me.",
        ],
        "sw": [
            "Nashukuru kunieleza kuhusu photography art.",
            "Hakuna haraka - photography art inaweza kuchukua muda unaohitaji.",
            "Njia yoyote unayotaka kuchukua kuhusu photography art inafaa kwangu.",
        ],
        "fr": [
            "C'est bon de savoir ce que tu penses de photography art.",
            "Pas de pression - photography art peut prendre tout le temps qu'il faut.",
            "Je me souviendrai que tu as mentionné photography art.",
        ],
    },
    "GRAMMAR_QUESTION_RESPONSES": {
        "en": [
            "Honestly, grammar question is a good thing to check in about.",
            "Good to know where you stand on grammar question.",
            "I'm always up for talking grammar question whenever you are.",
            "I'll remember you brought up grammar question.",
        ],
        "sw": [
            "Ni vizuri kujua unavyoona grammar question.",
            "Inafaa kutafakari kidogo kuhusu grammar question.",
            "Hilo ni wazo zuri kuhusu grammar question, tuendelee?",
        ],
        "fr": [
            "Ça vaut la peine de s'arrêter un instant sur grammar question.",
            "C'est bon de savoir ce que tu penses de grammar question.",
            "Je suis toujours partant pour parler de grammar question.",
        ],
    },
    "NAMING_THINGS_RESPONSES": {
        "en": [
            "I'm following along on naming things, keep going.",
            "That's a fair way to look at naming things.",
            "Honestly, naming things is a good thing to check in about.",
            "I'm always up for talking naming things whenever you are.",
        ],
        "sw": [
            "Unaweza kurudi kwenye naming things wakati wowote - bado nitakuwepo.",
            "Hilo ni wazo zuri kuhusu naming things, tuendelee?",
            "Nashukuru kunieleza kuhusu naming things.",
        ],
        "fr": [
            "C'est bon de savoir ce que tu penses de naming things.",
            "C'est un beau sujet, naming things - on continue ?",
            "Pas de pression - naming things peut prendre tout le temps qu'il faut.",
        ],
    },
    "WEATHER_EXTREME_RESPONSES": {
        "en": [
            "Good to know where you stand on weather extreme.",
            "I'll remember you brought up weather extreme.",
            "Honestly, weather extreme is a good thing to check in about.",
            "I appreciate you letting me in on weather extreme.",
        ],
        "sw": [
            "Hilo ni wazo zuri kuhusu weather extreme, tuendelee?",
            "Njia yoyote unayotaka kuchukua kuhusu weather extreme inafaa kwangu.",
            "Nitakumbuka ulizungumzia weather extreme.",
        ],
        "fr": [
            "Merci de me parler de weather extreme.",
            "Honnêtement, weather extreme vaut la peine d'en reparler.",
            "Tu peux revenir sur weather extreme quand tu veux, je serai là.",
        ],
    },
    "HOME_HOUSE_RESPONSES": {
        "en": [
            "That's a nice thread on home house, want to keep pulling it?",
            "Good to know where you stand on home house.",
            "I'm always up for talking home house whenever you are.",
            "That's a fair way to look at home house.",
        ],
        "sw": [
            "Njia yoyote unayotaka kuchukua kuhusu home house inafaa kwangu.",
            "Unaweza kurudi kwenye home house wakati wowote - bado nitakuwepo.",
            "Ni vizuri kujua unavyoona home house.",
        ],
        "fr": [
            "C'est bon de savoir ce que tu penses de home house.",
            "Tu peux revenir sur home house quand tu veux, je serai là.",
            "C'est un beau sujet, home house - on continue ?",
        ],
    },
    "NEIGHBORS_RESPONSES": {
        "en": [
            "Good to know where you stand on neighbors.",
            "However you want to take neighbors from here works for me.",
            "I appreciate you letting me in on neighbors.",
            "I'm always up for talking neighbors whenever you are.",
        ],
        "sw": [
            "Niko tayari kuzungumza kuhusu neighbors wakati wowote.",
            "Ni vizuri kujua unavyoona neighbors.",
            "Inafaa kutafakari kidogo kuhusu neighbors.",
        ],
        "fr": [
            "Je me souviendrai que tu as mentionné neighbors.",
            "Tu peux revenir sur neighbors quand tu veux, je serai là.",
            "C'est un beau sujet, neighbors - on continue ?",
        ],
    },
    "PET_LOSS_RESPONSES": {
        "en": [
            "No rush - pet loss can take as long as you need.",
            "I'm always up for talking pet loss whenever you are.",
            "That's a fair way to look at pet loss.",
            "However you want to take pet loss from here works for me.",
        ],
        "sw": [
            "Hilo ni wazo zuri kuhusu pet loss, tuendelee?",
            "Hakuna haraka - pet loss inaweza kuchukua muda unaohitaji.",
            "Nashukuru kunieleza kuhusu pet loss.",
        ],
        "fr": [
            "Je me souviendrai que tu as mentionné pet loss.",
            "C'est un beau sujet, pet loss - on continue ?",
            "Ça vaut la peine de s'arrêter un instant sur pet loss.",
        ],
    },
    "ACHIEVEMENT_MILESTONE_RESPONSES": {
        "en": [
            "Good to know where you stand on achievement milestone.",
            "However you want to take achievement milestone from here works for me.",
            "I'm following along on achievement milestone, keep going.",
            "Worth sitting with for a second - achievement milestone, that is.",
        ],
        "sw": [
            "Unaweza kurudi kwenye achievement milestone wakati wowote - bado nitakuwepo.",
            "Nitakumbuka ulizungumzia achievement milestone.",
            "Ni vizuri kujua unavyoona achievement milestone.",
        ],
        "fr": [
            "C'est un beau sujet, achievement milestone - on continue ?",
            "Tu peux revenir sur achievement milestone quand tu veux, je serai là.",
            "Peu importe comment tu veux aborder achievement milestone, ça me va.",
        ],
    },
    "WAITING_PATIENCE_RESPONSES": {
        "en": [
            "I'll remember you brought up waiting patience.",
            "I'm following along on waiting patience, keep going.",
            "I appreciate you letting me in on waiting patience.",
            "Worth sitting with for a second - waiting patience, that is.",
        ],
        "sw": [
            "Njia yoyote unayotaka kuchukua kuhusu waiting patience inafaa kwangu.",
            "Inafaa kutafakari kidogo kuhusu waiting patience.",
            "Niko tayari kuzungumza kuhusu waiting patience wakati wowote.",
        ],
        "fr": [
            "C'est bon de savoir ce que tu penses de waiting patience.",
            "Pas de pression - waiting patience peut prendre tout le temps qu'il faut.",
            "Honnêtement, waiting patience vaut la peine d'en reparler.",
        ],
    },
    "POSITIVE_SURPRISE_RESPONSES": {
        "en": [
            "That's a nice thread on positive surprise, want to keep pulling it?",
            "I'll remember you brought up positive surprise.",
            "No rush - positive surprise can take as long as you need.",
            "Good to know where you stand on positive surprise.",
        ],
        "sw": [
            "Kwa kweli, positive surprise ni jambo zuri la kuzungumzia.",
            "Nitakumbuka ulizungumzia positive surprise.",
            "Njia yoyote unayotaka kuchukua kuhusu positive surprise inafaa kwangu.",
        ],
        "fr": [
            "Pas de pression - positive surprise peut prendre tout le temps qu'il faut.",
            "Honnêtement, positive surprise vaut la peine d'en reparler.",
            "C'est un beau sujet, positive surprise - on continue ?",
        ],
    },
    "COMPLIMENT_BACK_REQUEST_RESPONSES": {
        "en": [
            "I'm always up for talking compliment back request whenever you are.",
            "I'll remember you brought up compliment back request.",
            "Good to know where you stand on compliment back request.",
            "However you want to take compliment back request from here works for me.",
        ],
        "sw": [
            "Nitakumbuka ulizungumzia compliment back request.",
            "Kwa kweli, compliment back request ni jambo zuri la kuzungumzia.",
            "Hilo ni wazo zuri kuhusu compliment back request, tuendelee?",
        ],
        "fr": [
            "C'est un beau sujet, compliment back request - on continue ?",
            "Je suis toujours partant pour parler de compliment back request.",
            "C'est bon de savoir ce que tu penses de compliment back request.",
        ],
    },
    "DEADLINE_RESPONSES": {
        "en": [
            "No rush - deadline can take as long as you need.",
            "That's a fair way to look at deadline.",
            "However you want to take deadline from here works for me.",
            "You can circle back to deadline any time - I'll still be here.",
        ],
        "sw": [
            "Unaweza kurudi kwenye deadline wakati wowote - bado nitakuwepo.",
            "Hilo ni wazo zuri kuhusu deadline, tuendelee?",
            "Inafaa kutafakari kidogo kuhusu deadline.",
        ],
        "fr": [
            "Peu importe comment tu veux aborder deadline, ça me va.",
            "Ça vaut la peine de s'arrêter un instant sur deadline.",
            "Je suis toujours partant pour parler de deadline.",
        ],
    },
    "PREGNANCY_BABY_RESPONSES": {
        "en": [
            "Good to know where you stand on pregnancy baby.",
            "I'm following along on pregnancy baby, keep going.",
            "I'll remember you brought up pregnancy baby.",
            "Honestly, pregnancy baby is a good thing to check in about.",
        ],
        "sw": [
            "Hilo ni wazo zuri kuhusu pregnancy baby, tuendelee?",
            "Njia yoyote unayotaka kuchukua kuhusu pregnancy baby inafaa kwangu.",
            "Hakuna haraka - pregnancy baby inaweza kuchukua muda unaohitaji.",
        ],
        "fr": [
            "Tu peux revenir sur pregnancy baby quand tu veux, je serai là.",
            "Honnêtement, pregnancy baby vaut la peine d'en reparler.",
            "Ça vaut la peine de s'arrêter un instant sur pregnancy baby.",
        ],
    },
    "WEDDING_ENGAGEMENT_RESPONSES": {
        "en": [
            "No rush - wedding engagement can take as long as you need.",
            "Worth sitting with for a second - wedding engagement, that is.",
            "That's a nice thread on wedding engagement, want to keep pulling it?",
            "I appreciate you letting me in on wedding engagement.",
        ],
        "sw": [
            "Inafaa kutafakari kidogo kuhusu wedding engagement.",
            "Niko tayari kuzungumza kuhusu wedding engagement wakati wowote.",
            "Hilo ni wazo zuri kuhusu wedding engagement, tuendelee?",
        ],
        "fr": [
            "Je me souviendrai que tu as mentionné wedding engagement.",
            "Merci de me parler de wedding engagement.",
            "C'est bon de savoir ce que tu penses de wedding engagement.",
        ],
    },
    "GRADUATION_RESPONSES": {
        "en": [
            "Worth sitting with for a second - graduation, that is.",
            "Good to know where you stand on graduation.",
            "However you want to take graduation from here works for me.",
            "You can circle back to graduation any time - I'll still be here.",
        ],
        "sw": [
            "Kwa kweli, graduation ni jambo zuri la kuzungumzia.",
            "Niko tayari kuzungumza kuhusu graduation wakati wowote.",
            "Ni vizuri kujua unavyoona graduation.",
        ],
        "fr": [
            "Pas de pression - graduation peut prendre tout le temps qu'il faut.",
            "Ça vaut la peine de s'arrêter un instant sur graduation.",
            "Merci de me parler de graduation.",
        ],
    },
    "MOVING_CITY_RESPONSES": {
        "en": [
            "I'll remember you brought up moving city.",
            "Honestly, moving city is a good thing to check in about.",
            "That's a fair way to look at moving city.",
            "I'm following along on moving city, keep going.",
        ],
        "sw": [
            "Unaweza kurudi kwenye moving city wakati wowote - bado nitakuwepo.",
            "Ni vizuri kujua unavyoona moving city.",
            "Nashukuru kunieleza kuhusu moving city.",
        ],
        "fr": [
            "Peu importe comment tu veux aborder moving city, ça me va.",
            "Ça vaut la peine de s'arrêter un instant sur moving city.",
            "Honnêtement, moving city vaut la peine d'en reparler.",
        ],
    },
    "NEW_PET_RESPONSES": {
        "en": [
            "That's a nice thread on new pet, want to keep pulling it?",
            "That's a fair way to look at new pet.",
            "I appreciate you letting me in on new pet.",
            "I'll remember you brought up new pet.",
        ],
        "sw": [
            "Ni vizuri kujua unavyoona new pet.",
            "Njia yoyote unayotaka kuchukua kuhusu new pet inafaa kwangu.",
            "Kwa kweli, new pet ni jambo zuri la kuzungumzia.",
        ],
        "fr": [
            "C'est un beau sujet, new pet - on continue ?",
            "Je suis toujours partant pour parler de new pet.",
            "Je me souviendrai que tu as mentionné new pet.",
        ],
    },
    "FIRST_DAY_RESPONSES": {
        "en": [
            "No rush - first day can take as long as you need.",
            "You can circle back to first day any time - I'll still be here.",
            "That's a nice thread on first day, want to keep pulling it?",
            "That's a fair way to look at first day.",
        ],
        "sw": [
            "Nitakumbuka ulizungumzia first day.",
            "Inafaa kutafakari kidogo kuhusu first day.",
            "Niko tayari kuzungumza kuhusu first day wakati wowote.",
        ],
        "fr": [
            "Je me souviendrai que tu as mentionné first day.",
            "Pas de pression - first day peut prendre tout le temps qu'il faut.",
            "Je suis toujours partant pour parler de first day.",
        ],
    },
    "REUNION_RESPONSES": {
        "en": [
            "I'll remember you brought up reunion.",
            "Good to know where you stand on reunion.",
            "That's a fair way to look at reunion.",
            "You can circle back to reunion any time - I'll still be here.",
        ],
        "sw": [
            "Kwa kweli, reunion ni jambo zuri la kuzungumzia.",
            "Hakuna haraka - reunion inaweza kuchukua muda unaohitaji.",
            "Unaweza kurudi kwenye reunion wakati wowote - bado nitakuwepo.",
        ],
        "fr": [
            "Peu importe comment tu veux aborder reunion, ça me va.",
            "C'est un beau sujet, reunion - on continue ?",
            "Pas de pression - reunion peut prendre tout le temps qu'il faut.",
        ],
    },
    "FLUENCY_GOALS_RESPONSES": {
        "en": [
            "I appreciate you letting me in on fluency goals.",
            "You can circle back to fluency goals any time - I'll still be here.",
            "That's a fair way to look at fluency goals.",
            "Honestly, fluency goals is a good thing to check in about.",
        ],
        "sw": [
            "Nashukuru kunieleza kuhusu fluency goals.",
            "Ni vizuri kujua unavyoona fluency goals.",
            "Inafaa kutafakari kidogo kuhusu fluency goals.",
        ],
        "fr": [
            "Je me souviendrai que tu as mentionné fluency goals.",
            "C'est un beau sujet, fluency goals - on continue ?",
            "Peu importe comment tu veux aborder fluency goals, ça me va.",
        ],
    },
    "CULTURAL_TRADITIONS_RESPONSES": {
        "en": [
            "I'll remember you brought up cultural traditions.",
            "Good to know where you stand on cultural traditions.",
            "I appreciate you letting me in on cultural traditions.",
            "I'm always up for talking cultural traditions whenever you are.",
        ],
        "sw": [
            "Hakuna haraka - cultural traditions inaweza kuchukua muda unaohitaji.",
            "Nitakumbuka ulizungumzia cultural traditions.",
            "Kwa kweli, cultural traditions ni jambo zuri la kuzungumzia.",
        ],
        "fr": [
            "Ça vaut la peine de s'arrêter un instant sur cultural traditions.",
            "C'est un beau sujet, cultural traditions - on continue ?",
            "Tu peux revenir sur cultural traditions quand tu veux, je serai là.",
        ],
    },
    "SUSTAINABILITY_RESPONSES": {
        "en": [
            "Worth sitting with for a second - sustainability, that is.",
            "Honestly, sustainability is a good thing to check in about.",
            "That's a fair way to look at sustainability.",
            "You can circle back to sustainability any time - I'll still be here.",
        ],
        "sw": [
            "Njia yoyote unayotaka kuchukua kuhusu sustainability inafaa kwangu.",
            "Hakuna haraka - sustainability inaweza kuchukua muda unaohitaji.",
            "Kwa kweli, sustainability ni jambo zuri la kuzungumzia.",
        ],
        "fr": [
            "Ça vaut la peine de s'arrêter un instant sur sustainability.",
            "Pas de pression - sustainability peut prendre tout le temps qu'il faut.",
            "Peu importe comment tu veux aborder sustainability, ça me va.",
        ],
    },
    "FUN_FACT_RESPONSES": {
        "en": [
            "However you want to take fun fact from here works for me.",
            "Worth sitting with for a second - fun fact, that is.",
            "That's a nice thread on fun fact, want to keep pulling it?",
            "I'm always up for talking fun fact whenever you are.",
        ],
        "sw": [
            "Inafaa kutafakari kidogo kuhusu fun fact.",
            "Unaweza kurudi kwenye fun fact wakati wowote - bado nitakuwepo.",
            "Hakuna haraka - fun fact inaweza kuchukua muda unaohitaji.",
        ],
        "fr": [
            "Je suis toujours partant pour parler de fun fact.",
            "Honnêtement, fun fact vaut la peine d'en reparler.",
            "Ça vaut la peine de s'arrêter un instant sur fun fact.",
        ],
    },
    "GIFT_THANKS_RESPONSES": {
        "en": [
            "However you want to take gift thanks from here works for me.",
            "Honestly, gift thanks is a good thing to check in about.",
            "Worth sitting with for a second - gift thanks, that is.",
            "I appreciate you letting me in on gift thanks.",
        ],
        "sw": [
            "Nashukuru kunieleza kuhusu gift thanks.",
            "Unaweza kurudi kwenye gift thanks wakati wowote - bado nitakuwepo.",
            "Niko tayari kuzungumza kuhusu gift thanks wakati wowote.",
        ],
        "fr": [
            "C'est un beau sujet, gift thanks - on continue ?",
            "Honnêtement, gift thanks vaut la peine d'en reparler.",
            "Merci de me parler de gift thanks.",
        ],
    },
    "RUNNING_LATE_RESPONSES": {
        "en": [
            "I'm always up for talking running late whenever you are.",
            "No rush - running late can take as long as you need.",
            "I'm following along on running late, keep going.",
            "However you want to take running late from here works for me.",
        ],
        "sw": [
            "Hakuna haraka - running late inaweza kuchukua muda unaohitaji.",
            "Niko tayari kuzungumza kuhusu running late wakati wowote.",
            "Nashukuru kunieleza kuhusu running late.",
        ],
        "fr": [
            "Pas de pression - running late peut prendre tout le temps qu'il faut.",
            "Je suis toujours partant pour parler de running late.",
            "Je me souviendrai que tu as mentionné running late.",
        ],
    },
    "TIME_MANAGEMENT_RESPONSES": {
        "en": [
            "That's a nice thread on time management, want to keep pulling it?",
            "You can circle back to time management any time - I'll still be here.",
            "That's a fair way to look at time management.",
            "Worth sitting with for a second - time management, that is.",
        ],
        "sw": [
            "Niko tayari kuzungumza kuhusu time management wakati wowote.",
            "Inafaa kutafakari kidogo kuhusu time management.",
            "Nashukuru kunieleza kuhusu time management.",
        ],
        "fr": [
            "Peu importe comment tu veux aborder time management, ça me va.",
            "Je suis toujours partant pour parler de time management.",
            "C'est un beau sujet, time management - on continue ?",
        ],
    },
    "SPORTS_VICTORY_RESPONSES": {
        "en": [
            "Good to know where you stand on sports victory.",
            "I'll remember you brought up sports victory.",
            "You can circle back to sports victory any time - I'll still be here.",
            "Worth sitting with for a second - sports victory, that is.",
        ],
        "sw": [
            "Hakuna haraka - sports victory inaweza kuchukua muda unaohitaji.",
            "Nashukuru kunieleza kuhusu sports victory.",
            "Nitakumbuka ulizungumzia sports victory.",
        ],
        "fr": [
            "Je suis toujours partant pour parler de sports victory.",
            "Honnêtement, sports victory vaut la peine d'en reparler.",
            "Tu peux revenir sur sports victory quand tu veux, je serai là.",
        ],
    },
    "SPORTS_LOSS_RESPONSES": {
        "en": [
            "Good to know where you stand on sports loss.",
            "Honestly, sports loss is a good thing to check in about.",
            "I'm always up for talking sports loss whenever you are.",
            "That's a nice thread on sports loss, want to keep pulling it?",
        ],
        "sw": [
            "Inafaa kutafakari kidogo kuhusu sports loss.",
            "Hakuna haraka - sports loss inaweza kuchukua muda unaohitaji.",
            "Nitakumbuka ulizungumzia sports loss.",
        ],
        "fr": [
            "Pas de pression - sports loss peut prendre tout le temps qu'il faut.",
            "C'est un beau sujet, sports loss - on continue ?",
            "Peu importe comment tu veux aborder sports loss, ça me va.",
        ],
    },
    "UNPREDICTABLE_WEATHER_RESPONSES": {
        "en": [
            "I'm following along on unpredictable weather, keep going.",
            "I'll remember you brought up unpredictable weather.",
            "You can circle back to unpredictable weather any time - I'll still be here.",
            "That's a nice thread on unpredictable weather, want to keep pulling it?",
        ],
        "sw": [
            "Nitakumbuka ulizungumzia unpredictable weather.",
            "Inafaa kutafakari kidogo kuhusu unpredictable weather.",
            "Nashukuru kunieleza kuhusu unpredictable weather.",
        ],
        "fr": [
            "Je me souviendrai que tu as mentionné unpredictable weather.",
            "Je suis toujours partant pour parler de unpredictable weather.",
            "Honnêtement, unpredictable weather vaut la peine d'en reparler.",
        ],
    },
    "NEW_YEAR_RESOLUTION_RESPONSES": {
        "en": [
            "Good to know where you stand on new year resolution.",
            "Honestly, new year resolution is a good thing to check in about.",
            "Worth sitting with for a second - new year resolution, that is.",
            "However you want to take new year resolution from here works for me.",
        ],
        "sw": [
            "Nashukuru kunieleza kuhusu new year resolution.",
            "Hilo ni wazo zuri kuhusu new year resolution, tuendelee?",
            "Ni vizuri kujua unavyoona new year resolution.",
        ],
        "fr": [
            "Merci de me parler de new year resolution.",
            "Je suis toujours partant pour parler de new year resolution.",
            "Tu peux revenir sur new year resolution quand tu veux, je serai là.",
        ],
    },
    "CHILDHOOD_MEMORY_RESPONSES": {
        "en": [
            "Good to know where you stand on childhood memory.",
            "Honestly, childhood memory is a good thing to check in about.",
            "I'm always up for talking childhood memory whenever you are.",
            "Worth sitting with for a second - childhood memory, that is.",
        ],
        "sw": [
            "Ni vizuri kujua unavyoona childhood memory.",
            "Inafaa kutafakari kidogo kuhusu childhood memory.",
            "Hilo ni wazo zuri kuhusu childhood memory, tuendelee?",
        ],
        "fr": [
            "Tu peux revenir sur childhood memory quand tu veux, je serai là.",
            "C'est un beau sujet, childhood memory - on continue ?",
            "Peu importe comment tu veux aborder childhood memory, ça me va.",
        ],
    },
    "ROLE_MODEL_RESPONSES": {
        "en": [
            "You can circle back to role model any time - I'll still be here.",
            "That's a nice thread on role model, want to keep pulling it?",
            "Honestly, role model is a good thing to check in about.",
            "Good to know where you stand on role model.",
        ],
        "sw": [
            "Kwa kweli, role model ni jambo zuri la kuzungumzia.",
            "Inafaa kutafakari kidogo kuhusu role model.",
            "Ni vizuri kujua unavyoona role model.",
        ],
        "fr": [
            "Peu importe comment tu veux aborder role model, ça me va.",
            "Je me souviendrai que tu as mentionné role model.",
            "Merci de me parler de role model.",
        ],
    },
    "FEAR_PHOBIA_RESPONSES": {
        "en": [
            "I'm following along on fear phobia, keep going.",
            "Worth sitting with for a second - fear phobia, that is.",
            "That's a nice thread on fear phobia, want to keep pulling it?",
            "No rush - fear phobia can take as long as you need.",
        ],
        "sw": [
            "Hilo ni wazo zuri kuhusu fear phobia, tuendelee?",
            "Njia yoyote unayotaka kuchukua kuhusu fear phobia inafaa kwangu.",
            "Ni vizuri kujua unavyoona fear phobia.",
        ],
        "fr": [
            "C'est bon de savoir ce que tu penses de fear phobia.",
            "Merci de me parler de fear phobia.",
            "C'est un beau sujet, fear phobia - on continue ?",
        ],
    },
    "DREAM_INTERPRETATION_RESPONSES": {
        "en": [
            "I'm always up for talking dream interpretation whenever you are.",
            "Worth sitting with for a second - dream interpretation, that is.",
            "Honestly, dream interpretation is a good thing to check in about.",
            "Good to know where you stand on dream interpretation.",
        ],
        "sw": [
            "Niko tayari kuzungumza kuhusu dream interpretation wakati wowote.",
            "Ni vizuri kujua unavyoona dream interpretation.",
            "Kwa kweli, dream interpretation ni jambo zuri la kuzungumzia.",
        ],
        "fr": [
            "Peu importe comment tu veux aborder dream interpretation, ça me va.",
            "Tu peux revenir sur dream interpretation quand tu veux, je serai là.",
            "C'est un beau sujet, dream interpretation - on continue ?",
        ],
    },
    "SELF_IMPROVEMENT_RESPONSES": {
        "en": [
            "No rush - self improvement can take as long as you need.",
            "Good to know where you stand on self improvement.",
            "I'm always up for talking self improvement whenever you are.",
            "That's a nice thread on self improvement, want to keep pulling it?",
        ],
        "sw": [
            "Inafaa kutafakari kidogo kuhusu self improvement.",
            "Nitakumbuka ulizungumzia self improvement.",
            "Njia yoyote unayotaka kuchukua kuhusu self improvement inafaa kwangu.",
        ],
        "fr": [
            "Tu peux revenir sur self improvement quand tu veux, je serai là.",
            "Merci de me parler de self improvement.",
            "Peu importe comment tu veux aborder self improvement, ça me va.",
        ],
    },
    "SOCIAL_MEDIA_RESPONSES": {
        "en": [
            "That's a nice thread on social media, want to keep pulling it?",
            "I'll remember you brought up social media.",
            "I appreciate you letting me in on social media.",
            "However you want to take social media from here works for me.",
        ],
        "sw": [
            "Nitakumbuka ulizungumzia social media.",
            "Nashukuru kunieleza kuhusu social media.",
            "Inafaa kutafakari kidogo kuhusu social media.",
        ],
        "fr": [
            "Je me souviendrai que tu as mentionné social media.",
            "Pas de pression - social media peut prendre tout le temps qu'il faut.",
            "C'est un beau sujet, social media - on continue ?",
        ],
    },
    "REMOTE_WORK_RESPONSES": {
        "en": [
            "I'm following along on remote work, keep going.",
            "I'll remember you brought up remote work.",
            "No rush - remote work can take as long as you need.",
            "You can circle back to remote work any time - I'll still be here.",
        ],
        "sw": [
            "Inafaa kutafakari kidogo kuhusu remote work.",
            "Hilo ni wazo zuri kuhusu remote work, tuendelee?",
            "Njia yoyote unayotaka kuchukua kuhusu remote work inafaa kwangu.",
        ],
        "fr": [
            "Merci de me parler de remote work.",
            "Je me souviendrai que tu as mentionné remote work.",
            "C'est bon de savoir ce que tu penses de remote work.",
        ],
    },
    "JOB_INTERVIEW_RESPONSES": {
        "en": [
            "I appreciate you letting me in on job interview.",
            "I'm following along on job interview, keep going.",
            "Worth sitting with for a second - job interview, that is.",
            "That's a nice thread on job interview, want to keep pulling it?",
        ],
        "sw": [
            "Nashukuru kunieleza kuhusu job interview.",
            "Unaweza kurudi kwenye job interview wakati wowote - bado nitakuwepo.",
            "Ni vizuri kujua unavyoona job interview.",
        ],
        "fr": [
            "Je suis toujours partant pour parler de job interview.",
            "Merci de me parler de job interview.",
            "Honnêtement, job interview vaut la peine d'en reparler.",
        ],
    },
    "RECIPE_DISH_RESPONSES": {
        "en": [
            "I appreciate you letting me in on recipe dish.",
            "However you want to take recipe dish from here works for me.",
            "Good to know where you stand on recipe dish.",
            "That's a nice thread on recipe dish, want to keep pulling it?",
        ],
        "sw": [
            "Nitakumbuka ulizungumzia recipe dish.",
            "Niko tayari kuzungumza kuhusu recipe dish wakati wowote.",
            "Njia yoyote unayotaka kuchukua kuhusu recipe dish inafaa kwangu.",
        ],
        "fr": [
            "Tu peux revenir sur recipe dish quand tu veux, je serai là.",
            "Peu importe comment tu veux aborder recipe dish, ça me va.",
            "Je suis toujours partant pour parler de recipe dish.",
        ],
    },
    "INSOMNIA_RESPONSES": {
        "en": [
            "I'll remember you brought up insomnia.",
            "Good to know where you stand on insomnia.",
            "I'm following along on insomnia, keep going.",
            "That's a nice thread on insomnia, want to keep pulling it?",
        ],
        "sw": [
            "Kwa kweli, insomnia ni jambo zuri la kuzungumzia.",
            "Ni vizuri kujua unavyoona insomnia.",
            "Nitakumbuka ulizungumzia insomnia.",
        ],
        "fr": [
            "C'est bon de savoir ce que tu penses de insomnia.",
            "Pas de pression - insomnia peut prendre tout le temps qu'il faut.",
            "C'est un beau sujet, insomnia - on continue ?",
        ],
    },
    "QUITTING_HABIT_RESPONSES": {
        "en": [
            "Honestly, quitting habit is a good thing to check in about.",
            "I'm always up for talking quitting habit whenever you are.",
            "I'm following along on quitting habit, keep going.",
            "Worth sitting with for a second - quitting habit, that is.",
        ],
        "sw": [
            "Nitakumbuka ulizungumzia quitting habit.",
            "Hakuna haraka - quitting habit inaweza kuchukua muda unaohitaji.",
            "Hilo ni wazo zuri kuhusu quitting habit, tuendelee?",
        ],
        "fr": [
            "C'est bon de savoir ce que tu penses de quitting habit.",
            "Merci de me parler de quitting habit.",
            "C'est un beau sujet, quitting habit - on continue ?",
        ],
    },
    "MEDITATION_MINDFULNESS_RESPONSES": {
        "en": [
            "That's a fair way to look at meditation mindfulness.",
            "I appreciate you letting me in on meditation mindfulness.",
            "Worth sitting with for a second - meditation mindfulness, that is.",
            "However you want to take meditation mindfulness from here works for me.",
        ],
        "sw": [
            "Niko tayari kuzungumza kuhusu meditation mindfulness wakati wowote.",
            "Ni vizuri kujua unavyoona meditation mindfulness.",
            "Hakuna haraka - meditation mindfulness inaweza kuchukua muda unaohitaji.",
        ],
        "fr": [
            "Je me souviendrai que tu as mentionné meditation mindfulness.",
            "Tu peux revenir sur meditation mindfulness quand tu veux, je serai là.",
            "C'est un beau sujet, meditation mindfulness - on continue ?",
        ],
    },
    "SIBLING_RIVALRY_RESPONSES": {
        "en": [
            "No rush - sibling rivalry can take as long as you need.",
            "That's a nice thread on sibling rivalry, want to keep pulling it?",
            "Honestly, sibling rivalry is a good thing to check in about.",
            "You can circle back to sibling rivalry any time - I'll still be here.",
        ],
        "sw": [
            "Hakuna haraka - sibling rivalry inaweza kuchukua muda unaohitaji.",
            "Ni vizuri kujua unavyoona sibling rivalry.",
            "Hilo ni wazo zuri kuhusu sibling rivalry, tuendelee?",
        ],
        "fr": [
            "Ça vaut la peine de s'arrêter un instant sur sibling rivalry.",
            "Tu peux revenir sur sibling rivalry quand tu veux, je serai là.",
            "Merci de me parler de sibling rivalry.",
        ],
    },
    "LONG_DISTANCE_RELATIONSHIP_RESPONSES": {
        "en": [
            "You can circle back to long distance relationship any time - I'll still be here.",
            "Honestly, long distance relationship is a good thing to check in about.",
            "Worth sitting with for a second - long distance relationship, that is.",
            "Good to know where you stand on long distance relationship.",
        ],
        "sw": [
            "Nashukuru kunieleza kuhusu long distance relationship.",
            "Niko tayari kuzungumza kuhusu long distance relationship wakati wowote.",
            "Hakuna haraka - long distance relationship inaweza kuchukua muda unaohitaji.",
        ],
        "fr": [
            "C'est un beau sujet, long distance relationship - on continue ?",
            "Pas de pression - long distance relationship peut prendre tout le temps qu'il faut.",
            "Ça vaut la peine de s'arrêter un instant sur long distance relationship.",
        ],
    },
    "PET_PEEVE_RESPONSES": {
        "en": [
            "That's a fair way to look at pet peeve.",
            "I appreciate you letting me in on pet peeve.",
            "However you want to take pet peeve from here works for me.",
            "That's a nice thread on pet peeve, want to keep pulling it?",
        ],
        "sw": [
            "Inafaa kutafakari kidogo kuhusu pet peeve.",
            "Nashukuru kunieleza kuhusu pet peeve.",
            "Njia yoyote unayotaka kuchukua kuhusu pet peeve inafaa kwangu.",
        ],
        "fr": [
            "Merci de me parler de pet peeve.",
            "Pas de pression - pet peeve peut prendre tout le temps qu'il faut.",
            "Je suis toujours partant pour parler de pet peeve.",
        ],
    },
    "KINDNESS_RESPONSES": {
        "en": [
            "Good to know where you stand on kindness.",
            "However you want to take kindness from here works for me.",
            "I'm always up for talking kindness whenever you are.",
            "Worth sitting with for a second - kindness, that is.",
        ],
        "sw": [
            "Ni vizuri kujua unavyoona kindness.",
            "Kwa kweli, kindness ni jambo zuri la kuzungumzia.",
            "Nitakumbuka ulizungumzia kindness.",
        ],
        "fr": [
            "Pas de pression - kindness peut prendre tout le temps qu'il faut.",
            "Je suis toujours partant pour parler de kindness.",
            "Ça vaut la peine de s'arrêter un instant sur kindness.",
        ],
    },
    "PROCRASTINATION_RESPONSES": {
        "en": [
            "You can circle back to procrastination any time - I'll still be here.",
            "I'm following along on procrastination, keep going.",
            "However you want to take procrastination from here works for me.",
            "I'll remember you brought up procrastination.",
        ],
        "sw": [
            "Inafaa kutafakari kidogo kuhusu procrastination.",
            "Niko tayari kuzungumza kuhusu procrastination wakati wowote.",
            "Njia yoyote unayotaka kuchukua kuhusu procrastination inafaa kwangu.",
        ],
        "fr": [
            "Tu peux revenir sur procrastination quand tu veux, je serai là.",
            "Je me souviendrai que tu as mentionné procrastination.",
            "Pas de pression - procrastination peut prendre tout le temps qu'il faut.",
        ],
    },
    "DECLUTTERING_RESPONSES": {
        "en": [
            "However you want to take decluttering from here works for me.",
            "Worth sitting with for a second - decluttering, that is.",
            "I'll remember you brought up decluttering.",
            "I'm following along on decluttering, keep going.",
        ],
        "sw": [
            "Hilo ni wazo zuri kuhusu decluttering, tuendelee?",
            "Nitakumbuka ulizungumzia decluttering.",
            "Nashukuru kunieleza kuhusu decluttering.",
        ],
        "fr": [
            "Je suis toujours partant pour parler de decluttering.",
            "C'est bon de savoir ce que tu penses de decluttering.",
            "Tu peux revenir sur decluttering quand tu veux, je serai là.",
        ],
    },
    "PUBLIC_SPEAKING_RESPONSES": {
        "en": [
            "I'll remember you brought up public speaking.",
            "I appreciate you letting me in on public speaking.",
            "You can circle back to public speaking any time - I'll still be here.",
            "I'm following along on public speaking, keep going.",
        ],
        "sw": [
            "Hakuna haraka - public speaking inaweza kuchukua muda unaohitaji.",
            "Njia yoyote unayotaka kuchukua kuhusu public speaking inafaa kwangu.",
            "Niko tayari kuzungumza kuhusu public speaking wakati wowote.",
        ],
        "fr": [
            "Honnêtement, public speaking vaut la peine d'en reparler.",
            "Merci de me parler de public speaking.",
            "C'est bon de savoir ce que tu penses de public speaking.",
        ],
    },
    "LEARNING_TO_DRIVE_RESPONSES": {
        "en": [
            "Honestly, learning to drive is a good thing to check in about.",
            "I'm always up for talking learning to drive whenever you are.",
            "Good to know where you stand on learning to drive.",
            "I'm following along on learning to drive, keep going.",
        ],
        "sw": [
            "Kwa kweli, learning to drive ni jambo zuri la kuzungumzia.",
            "Njia yoyote unayotaka kuchukua kuhusu learning to drive inafaa kwangu.",
            "Hakuna haraka - learning to drive inaweza kuchukua muda unaohitaji.",
        ],
        "fr": [
            "Merci de me parler de learning to drive.",
            "Ça vaut la peine de s'arrêter un instant sur learning to drive.",
            "Peu importe comment tu veux aborder learning to drive, ça me va.",
        ],
    },
    "RETIREMENT_PLANNING_RESPONSES": {
        "en": [
            "I'm always up for talking retirement planning whenever you are.",
            "No rush - retirement planning can take as long as you need.",
            "You can circle back to retirement planning any time - I'll still be here.",
            "I'll remember you brought up retirement planning.",
        ],
        "sw": [
            "Niko tayari kuzungumza kuhusu retirement planning wakati wowote.",
            "Njia yoyote unayotaka kuchukua kuhusu retirement planning inafaa kwangu.",
            "Nitakumbuka ulizungumzia retirement planning.",
        ],
        "fr": [
            "C'est un beau sujet, retirement planning - on continue ?",
            "Tu peux revenir sur retirement planning quand tu veux, je serai là.",
            "Honnêtement, retirement planning vaut la peine d'en reparler.",
        ],
    },
    "PROGRAMMING_CODING_RESPONSES": {
        "en": [
            "I'll remember you brought up programming coding.",
            "Honestly, programming coding is a good thing to check in about.",
            "I appreciate you letting me in on programming coding.",
            "That's a fair way to look at programming coding.",
        ],
        "sw": [
            "Niko tayari kuzungumza kuhusu programming coding wakati wowote.",
            "Kwa kweli, programming coding ni jambo zuri la kuzungumzia.",
            "Njia yoyote unayotaka kuchukua kuhusu programming coding inafaa kwangu.",
        ],
        "fr": [
            "Tu peux revenir sur programming coding quand tu veux, je serai là.",
            "Honnêtement, programming coding vaut la peine d'en reparler.",
            "Peu importe comment tu veux aborder programming coding, ça me va.",
        ],
    },
    "GYM_INTIMIDATION_RESPONSES": {
        "en": [
            "Good to know where you stand on gym intimidation.",
            "I'm always up for talking gym intimidation whenever you are.",
            "Worth sitting with for a second - gym intimidation, that is.",
            "That's a nice thread on gym intimidation, want to keep pulling it?",
        ],
        "sw": [
            "Hilo ni wazo zuri kuhusu gym intimidation, tuendelee?",
            "Inafaa kutafakari kidogo kuhusu gym intimidation.",
            "Nashukuru kunieleza kuhusu gym intimidation.",
        ],
        "fr": [
            "C'est bon de savoir ce que tu penses de gym intimidation.",
            "Je suis toujours partant pour parler de gym intimidation.",
            "Merci de me parler de gym intimidation.",
        ],
    },
    "COMFORT_FOOD_RESPONSES": {
        "en": [
            "I'm following along on comfort food, keep going.",
            "Honestly, comfort food is a good thing to check in about.",
            "That's a fair way to look at comfort food.",
            "Worth sitting with for a second - comfort food, that is.",
        ],
        "sw": [
            "Unaweza kurudi kwenye comfort food wakati wowote - bado nitakuwepo.",
            "Inafaa kutafakari kidogo kuhusu comfort food.",
            "Kwa kweli, comfort food ni jambo zuri la kuzungumzia.",
        ],
        "fr": [
            "Je me souviendrai que tu as mentionné comfort food.",
            "C'est bon de savoir ce que tu penses de comfort food.",
            "Tu peux revenir sur comfort food quand tu veux, je serai là.",
        ],
    },
    "SINGING_VOICE_RESPONSES": {
        "en": [
            "I'll remember you brought up singing voice.",
            "I'm always up for talking singing voice whenever you are.",
            "That's a fair way to look at singing voice.",
            "Honestly, singing voice is a good thing to check in about.",
        ],
        "sw": [
            "Njia yoyote unayotaka kuchukua kuhusu singing voice inafaa kwangu.",
            "Nashukuru kunieleza kuhusu singing voice.",
            "Unaweza kurudi kwenye singing voice wakati wowote - bado nitakuwepo.",
        ],
        "fr": [
            "Je suis toujours partant pour parler de singing voice.",
            "Je me souviendrai que tu as mentionné singing voice.",
            "Peu importe comment tu veux aborder singing voice, ça me va.",
        ],
    },
    "JOURNALING_RESPONSES": {
        "en": [
            "That's a nice thread on journaling, want to keep pulling it?",
            "Worth sitting with for a second - journaling, that is.",
            "That's a fair way to look at journaling.",
            "Honestly, journaling is a good thing to check in about.",
        ],
        "sw": [
            "Unaweza kurudi kwenye journaling wakati wowote - bado nitakuwepo.",
            "Nashukuru kunieleza kuhusu journaling.",
            "Hilo ni wazo zuri kuhusu journaling, tuendelee?",
        ],
        "fr": [
            "C'est bon de savoir ce que tu penses de journaling.",
            "Peu importe comment tu veux aborder journaling, ça me va.",
            "Honnêtement, journaling vaut la peine d'en reparler.",
        ],
    },
    "BOARD_GAMES_PUZZLES_RESPONSES": {
        "en": [
            "Honestly, board games puzzles is a good thing to check in about.",
            "Good to know where you stand on board games puzzles.",
            "No rush - board games puzzles can take as long as you need.",
            "I'm always up for talking board games puzzles whenever you are.",
        ],
        "sw": [
            "Hakuna haraka - board games puzzles inaweza kuchukua muda unaohitaji.",
            "Inafaa kutafakari kidogo kuhusu board games puzzles.",
            "Kwa kweli, board games puzzles ni jambo zuri la kuzungumzia.",
        ],
        "fr": [
            "Honnêtement, board games puzzles vaut la peine d'en reparler.",
            "Tu peux revenir sur board games puzzles quand tu veux, je serai là.",
            "Ça vaut la peine de s'arrêter un instant sur board games puzzles.",
        ],
    },
    "CAMPING_OUTDOOR_TRIP_RESPONSES": {
        "en": [
            "I appreciate you letting me in on camping outdoor trip.",
            "I'm following along on camping outdoor trip, keep going.",
            "You can circle back to camping outdoor trip any time - I'll still be here.",
            "Worth sitting with for a second - camping outdoor trip, that is.",
        ],
        "sw": [
            "Niko tayari kuzungumza kuhusu camping outdoor trip wakati wowote.",
            "Ni vizuri kujua unavyoona camping outdoor trip.",
            "Unaweza kurudi kwenye camping outdoor trip wakati wowote - bado nitakuwepo.",
        ],
        "fr": [
            "Peu importe comment tu veux aborder camping outdoor trip, ça me va.",
            "Merci de me parler de camping outdoor trip.",
            "C'est un beau sujet, camping outdoor trip - on continue ?",
        ],
    },
    "CAR_TROUBLE_RESPONSES": {
        "en": [
            "That's a fair way to look at car trouble.",
            "No rush - car trouble can take as long as you need.",
            "That's a nice thread on car trouble, want to keep pulling it?",
            "I appreciate you letting me in on car trouble.",
        ],
        "sw": [
            "Nitakumbuka ulizungumzia car trouble.",
            "Hakuna haraka - car trouble inaweza kuchukua muda unaohitaji.",
            "Kwa kweli, car trouble ni jambo zuri la kuzungumzia.",
        ],
        "fr": [
            "Tu peux revenir sur car trouble quand tu veux, je serai là.",
            "Pas de pression - car trouble peut prendre tout le temps qu'il faut.",
            "C'est bon de savoir ce que tu penses de car trouble.",
        ],
    },
    "ROOMMATES_RESPONSES": {
        "en": [
            "However you want to take roommates from here works for me.",
            "I appreciate you letting me in on roommates.",
            "Worth sitting with for a second - roommates, that is.",
            "Honestly, roommates is a good thing to check in about.",
        ],
        "sw": [
            "Njia yoyote unayotaka kuchukua kuhusu roommates inafaa kwangu.",
            "Hakuna haraka - roommates inaweza kuchukua muda unaohitaji.",
            "Unaweza kurudi kwenye roommates wakati wowote - bado nitakuwepo.",
        ],
        "fr": [
            "Pas de pression - roommates peut prendre tout le temps qu'il faut.",
            "Peu importe comment tu veux aborder roommates, ça me va.",
            "C'est bon de savoir ce que tu penses de roommates.",
        ],
    },
    "ONLINE_DATING_RESPONSES": {
        "en": [
            "However you want to take online dating from here works for me.",
            "That's a nice thread on online dating, want to keep pulling it?",
            "I'm always up for talking online dating whenever you are.",
            "You can circle back to online dating any time - I'll still be here.",
        ],
        "sw": [
            "Nashukuru kunieleza kuhusu online dating.",
            "Njia yoyote unayotaka kuchukua kuhusu online dating inafaa kwangu.",
            "Hakuna haraka - online dating inaweza kuchukua muda unaohitaji.",
        ],
        "fr": [
            "Pas de pression - online dating peut prendre tout le temps qu'il faut.",
            "Je suis toujours partant pour parler de online dating.",
            "C'est un beau sujet, online dating - on continue ?",
        ],
    },
    "TATTOOS_PIERCINGS_RESPONSES": {
        "en": [
            "Worth sitting with for a second - tattoos piercings, that is.",
            "However you want to take tattoos piercings from here works for me.",
            "Honestly, tattoos piercings is a good thing to check in about.",
            "I'm always up for talking tattoos piercings whenever you are.",
        ],
        "sw": [
            "Nashukuru kunieleza kuhusu tattoos piercings.",
            "Hilo ni wazo zuri kuhusu tattoos piercings, tuendelee?",
            "Hakuna haraka - tattoos piercings inaweza kuchukua muda unaohitaji.",
        ],
        "fr": [
            "C'est bon de savoir ce que tu penses de tattoos piercings.",
            "Peu importe comment tu veux aborder tattoos piercings, ça me va.",
            "Je me souviendrai que tu as mentionné tattoos piercings.",
        ],
    },
    "FASHION_STYLE_RESPONSES": {
        "en": [
            "No rush - fashion style can take as long as you need.",
            "However you want to take fashion style from here works for me.",
            "Honestly, fashion style is a good thing to check in about.",
            "I'm following along on fashion style, keep going.",
        ],
        "sw": [
            "Hakuna haraka - fashion style inaweza kuchukua muda unaohitaji.",
            "Nashukuru kunieleza kuhusu fashion style.",
            "Hilo ni wazo zuri kuhusu fashion style, tuendelee?",
        ],
        "fr": [
            "Honnêtement, fashion style vaut la peine d'en reparler.",
            "Je suis toujours partant pour parler de fashion style.",
            "Tu peux revenir sur fashion style quand tu veux, je serai là.",
        ],
    },
    "LANGUAGE_BARRIER_RESPONSES": {
        "en": [
            "Honestly, language barrier is a good thing to check in about.",
            "No rush - language barrier can take as long as you need.",
            "Worth sitting with for a second - language barrier, that is.",
            "I'm following along on language barrier, keep going.",
        ],
        "sw": [
            "Inafaa kutafakari kidogo kuhusu language barrier.",
            "Hilo ni wazo zuri kuhusu language barrier, tuendelee?",
            "Nashukuru kunieleza kuhusu language barrier.",
        ],
        "fr": [
            "Peu importe comment tu veux aborder language barrier, ça me va.",
            "C'est un beau sujet, language barrier - on continue ?",
            "Je me souviendrai que tu as mentionné language barrier.",
        ],
    },
    "SCHOOL_VOLUNTEERING_RESPONSES": {
        "en": [
            "That's a nice thread on school volunteering, want to keep pulling it?",
            "Honestly, school volunteering is a good thing to check in about.",
            "You can circle back to school volunteering any time - I'll still be here.",
            "However you want to take school volunteering from here works for me.",
        ],
        "sw": [
            "Niko tayari kuzungumza kuhusu school volunteering wakati wowote.",
            "Hilo ni wazo zuri kuhusu school volunteering, tuendelee?",
            "Nitakumbuka ulizungumzia school volunteering.",
        ],
        "fr": [
            "Ça vaut la peine de s'arrêter un instant sur school volunteering.",
            "C'est un beau sujet, school volunteering - on continue ?",
            "Peu importe comment tu veux aborder school volunteering, ça me va.",
        ],
    },
    "CHARITY_DONATION_RESPONSES": {
        "en": [
            "Worth sitting with for a second - charity donation, that is.",
            "No rush - charity donation can take as long as you need.",
            "However you want to take charity donation from here works for me.",
            "That's a nice thread on charity donation, want to keep pulling it?",
        ],
        "sw": [
            "Unaweza kurudi kwenye charity donation wakati wowote - bado nitakuwepo.",
            "Ni vizuri kujua unavyoona charity donation.",
            "Kwa kweli, charity donation ni jambo zuri la kuzungumzia.",
        ],
        "fr": [
            "Merci de me parler de charity donation.",
            "Je me souviendrai que tu as mentionné charity donation.",
            "C'est bon de savoir ce que tu penses de charity donation.",
        ],
    },
    "HOSTING_GUESTS_RESPONSES": {
        "en": [
            "I'm always up for talking hosting guests whenever you are.",
            "Good to know where you stand on hosting guests.",
            "That's a nice thread on hosting guests, want to keep pulling it?",
            "I appreciate you letting me in on hosting guests.",
        ],
        "sw": [
            "Kwa kweli, hosting guests ni jambo zuri la kuzungumzia.",
            "Hakuna haraka - hosting guests inaweza kuchukua muda unaohitaji.",
            "Hilo ni wazo zuri kuhusu hosting guests, tuendelee?",
        ],
        "fr": [
            "Peu importe comment tu veux aborder hosting guests, ça me va.",
            "C'est un beau sujet, hosting guests - on continue ?",
            "Je suis toujours partant pour parler de hosting guests.",
        ],
    },
    "TIME_ZONES_RESPONSES": {
        "en": [
            "I'll remember you brought up time zones.",
            "That's a nice thread on time zones, want to keep pulling it?",
            "No rush - time zones can take as long as you need.",
            "I'm following along on time zones, keep going.",
        ],
        "sw": [
            "Unaweza kurudi kwenye time zones wakati wowote - bado nitakuwepo.",
            "Niko tayari kuzungumza kuhusu time zones wakati wowote.",
            "Hilo ni wazo zuri kuhusu time zones, tuendelee?",
        ],
        "fr": [
            "Pas de pression - time zones peut prendre tout le temps qu'il faut.",
            "Je me souviendrai que tu as mentionné time zones.",
            "Je suis toujours partant pour parler de time zones.",
        ],
    },
    "PRODUCTIVITY_TOOLS_RESPONSES": {
        "en": [
            "However you want to take productivity tools from here works for me.",
            "That's a nice thread on productivity tools, want to keep pulling it?",
            "Good to know where you stand on productivity tools.",
            "Worth sitting with for a second - productivity tools, that is.",
        ],
        "sw": [
            "Inafaa kutafakari kidogo kuhusu productivity tools.",
            "Nitakumbuka ulizungumzia productivity tools.",
            "Niko tayari kuzungumza kuhusu productivity tools wakati wowote.",
        ],
        "fr": [
            "Je suis toujours partant pour parler de productivity tools.",
            "Tu peux revenir sur productivity tools quand tu veux, je serai là.",
            "Ça vaut la peine de s'arrêter un instant sur productivity tools.",
        ],
    },
    "PARENTING_RESPONSES": {
        "en": [
            "Worth sitting with for a second - parenting, that is.",
            "Honestly, parenting is a good thing to check in about.",
            "I'll remember you brought up parenting.",
            "Good to know where you stand on parenting.",
        ],
        "sw": [
            "Inafaa kutafakari kidogo kuhusu parenting.",
            "Hilo ni wazo zuri kuhusu parenting, tuendelee?",
            "Njia yoyote unayotaka kuchukua kuhusu parenting inafaa kwangu.",
        ],
        "fr": [
            "C'est un beau sujet, parenting - on continue ?",
            "Je me souviendrai que tu as mentionné parenting.",
            "Peu importe comment tu veux aborder parenting, ça me va.",
        ],
    },
    "TEENAGER_STRUGGLE_RESPONSES": {
        "en": [
            "However you want to take teenager struggle from here works for me.",
            "I'm always up for talking teenager struggle whenever you are.",
            "I appreciate you letting me in on teenager struggle.",
            "No rush - teenager struggle can take as long as you need.",
        ],
        "sw": [
            "Niko tayari kuzungumza kuhusu teenager struggle wakati wowote.",
            "Unaweza kurudi kwenye teenager struggle wakati wowote - bado nitakuwepo.",
            "Ni vizuri kujua unavyoona teenager struggle.",
        ],
        "fr": [
            "Je suis toujours partant pour parler de teenager struggle.",
            "Tu peux revenir sur teenager struggle quand tu veux, je serai là.",
            "Ça vaut la peine de s'arrêter un instant sur teenager struggle.",
        ],
    },
    "ELDERLY_PARENT_CARE_RESPONSES": {
        "en": [
            "I'm following along on elderly parent care, keep going.",
            "Worth sitting with for a second - elderly parent care, that is.",
            "Good to know where you stand on elderly parent care.",
            "That's a fair way to look at elderly parent care.",
        ],
        "sw": [
            "Kwa kweli, elderly parent care ni jambo zuri la kuzungumzia.",
            "Inafaa kutafakari kidogo kuhusu elderly parent care.",
            "Niko tayari kuzungumza kuhusu elderly parent care wakati wowote.",
        ],
        "fr": [
            "Tu peux revenir sur elderly parent care quand tu veux, je serai là.",
            "Pas de pression - elderly parent care peut prendre tout le temps qu'il faut.",
            "C'est un beau sujet, elderly parent care - on continue ?",
        ],
    },
    "GRIEF_LOSS_RESPONSES": {
        "en": [
            "That's a nice thread on grief loss, want to keep pulling it?",
            "Honestly, grief loss is a good thing to check in about.",
            "That's a fair way to look at grief loss.",
            "I appreciate you letting me in on grief loss.",
        ],
        "sw": [
            "Nitakumbuka ulizungumzia grief loss.",
            "Njia yoyote unayotaka kuchukua kuhusu grief loss inafaa kwangu.",
            "Unaweza kurudi kwenye grief loss wakati wowote - bado nitakuwepo.",
        ],
        "fr": [
            "Peu importe comment tu veux aborder grief loss, ça me va.",
            "Je me souviendrai que tu as mentionné grief loss.",
            "C'est un beau sujet, grief loss - on continue ?",
        ],
    },
    "THERAPY_COUNSELING_RESPONSES": {
        "en": [
            "I appreciate you letting me in on therapy counseling.",
            "That's a fair way to look at therapy counseling.",
            "I'm following along on therapy counseling, keep going.",
            "I'm always up for talking therapy counseling whenever you are.",
        ],
        "sw": [
            "Kwa kweli, therapy counseling ni jambo zuri la kuzungumzia.",
            "Niko tayari kuzungumza kuhusu therapy counseling wakati wowote.",
            "Hilo ni wazo zuri kuhusu therapy counseling, tuendelee?",
        ],
        "fr": [
            "Je me souviendrai que tu as mentionné therapy counseling.",
            "C'est bon de savoir ce que tu penses de therapy counseling.",
            "Ça vaut la peine de s'arrêter un instant sur therapy counseling.",
        ],
    },
    "ADDICTION_RECOVERY_RESPONSES": {
        "en": [
            "Honestly, addiction recovery is a good thing to check in about.",
            "That's a fair way to look at addiction recovery.",
            "However you want to take addiction recovery from here works for me.",
            "Good to know where you stand on addiction recovery.",
        ],
        "sw": [
            "Kwa kweli, addiction recovery ni jambo zuri la kuzungumzia.",
            "Nashukuru kunieleza kuhusu addiction recovery.",
            "Inafaa kutafakari kidogo kuhusu addiction recovery.",
        ],
        "fr": [
            "Honnêtement, addiction recovery vaut la peine d'en reparler.",
            "Peu importe comment tu veux aborder addiction recovery, ça me va.",
            "Je me souviendrai que tu as mentionné addiction recovery.",
        ],
    },
    "IDENTITY_COMING_OUT_RESPONSES": {
        "en": [
            "That's a nice thread on identity coming out, want to keep pulling it?",
            "I appreciate you letting me in on identity coming out.",
            "However you want to take identity coming out from here works for me.",
            "Worth sitting with for a second - identity coming out, that is.",
        ],
        "sw": [
            "Kwa kweli, identity coming out ni jambo zuri la kuzungumzia.",
            "Unaweza kurudi kwenye identity coming out wakati wowote - bado nitakuwepo.",
            "Nashukuru kunieleza kuhusu identity coming out.",
        ],
        "fr": [
            "Ça vaut la peine de s'arrêter un instant sur identity coming out.",
            "Peu importe comment tu veux aborder identity coming out, ça me va.",
            "Pas de pression - identity coming out peut prendre tout le temps qu'il faut.",
        ],
    },
    "IMMIGRATION_RESPONSES": {
        "en": [
            "You can circle back to immigration any time - I'll still be here.",
            "That's a nice thread on immigration, want to keep pulling it?",
            "However you want to take immigration from here works for me.",
            "I'll remember you brought up immigration.",
        ],
        "sw": [
            "Niko tayari kuzungumza kuhusu immigration wakati wowote.",
            "Inafaa kutafakari kidogo kuhusu immigration.",
            "Njia yoyote unayotaka kuchukua kuhusu immigration inafaa kwangu.",
        ],
        "fr": [
            "Je me souviendrai que tu as mentionné immigration.",
            "Tu peux revenir sur immigration quand tu veux, je serai là.",
            "Ça vaut la peine de s'arrêter un instant sur immigration.",
        ],
    },
    "DISABILITY_ACCESSIBILITY_RESPONSES": {
        "en": [
            "Worth sitting with for a second - disability accessibility, that is.",
            "I'll remember you brought up disability accessibility.",
            "You can circle back to disability accessibility any time - I'll still be here.",
            "Honestly, disability accessibility is a good thing to check in about.",
        ],
        "sw": [
            "Unaweza kurudi kwenye disability accessibility wakati wowote - bado nitakuwepo.",
            "Kwa kweli, disability accessibility ni jambo zuri la kuzungumzia.",
            "Inafaa kutafakari kidogo kuhusu disability accessibility.",
        ],
        "fr": [
            "C'est un beau sujet, disability accessibility - on continue ?",
            "Peu importe comment tu veux aborder disability accessibility, ça me va.",
            "Je suis toujours partant pour parler de disability accessibility.",
        ],
    },
    "MENSTRUAL_HEALTH_RESPONSES": {
        "en": [
            "I appreciate you letting me in on menstrual health.",
            "I'm always up for talking menstrual health whenever you are.",
            "Worth sitting with for a second - menstrual health, that is.",
            "I'm following along on menstrual health, keep going.",
        ],
        "sw": [
            "Niko tayari kuzungumza kuhusu menstrual health wakati wowote.",
            "Kwa kweli, menstrual health ni jambo zuri la kuzungumzia.",
            "Nashukuru kunieleza kuhusu menstrual health.",
        ],
        "fr": [
            "Tu peux revenir sur menstrual health quand tu veux, je serai là.",
            "Merci de me parler de menstrual health.",
            "Pas de pression - menstrual health peut prendre tout le temps qu'il faut.",
        ],
    },
    "CHECKUP_VACCINE_RESPONSES": {
        "en": [
            "I'll remember you brought up checkup vaccine.",
            "I'm always up for talking checkup vaccine whenever you are.",
            "I'm following along on checkup vaccine, keep going.",
            "I appreciate you letting me in on checkup vaccine.",
        ],
        "sw": [
            "Hilo ni wazo zuri kuhusu checkup vaccine, tuendelee?",
            "Njia yoyote unayotaka kuchukua kuhusu checkup vaccine inafaa kwangu.",
            "Kwa kweli, checkup vaccine ni jambo zuri la kuzungumzia.",
        ],
        "fr": [
            "Tu peux revenir sur checkup vaccine quand tu veux, je serai là.",
            "Honnêtement, checkup vaccine vaut la peine d'en reparler.",
            "Ça vaut la peine de s'arrêter un instant sur checkup vaccine.",
        ],
    },
    "CLIMATE_ANXIETY_RESPONSES": {
        "en": [
            "I'll remember you brought up climate anxiety.",
            "You can circle back to climate anxiety any time - I'll still be here.",
            "I'm always up for talking climate anxiety whenever you are.",
            "That's a nice thread on climate anxiety, want to keep pulling it?",
        ],
        "sw": [
            "Kwa kweli, climate anxiety ni jambo zuri la kuzungumzia.",
            "Nitakumbuka ulizungumzia climate anxiety.",
            "Ni vizuri kujua unavyoona climate anxiety.",
        ],
        "fr": [
            "Pas de pression - climate anxiety peut prendre tout le temps qu'il faut.",
            "Tu peux revenir sur climate anxiety quand tu veux, je serai là.",
            "Merci de me parler de climate anxiety.",
        ],
    },
    "AI_TECHNOLOGY_FEAR_RESPONSES": {
        "en": [
            "That's a fair way to look at ai technology fear.",
            "No rush - ai technology fear can take as long as you need.",
            "I'm always up for talking ai technology fear whenever you are.",
            "Honestly, ai technology fear is a good thing to check in about.",
        ],
        "sw": [
            "Niko tayari kuzungumza kuhusu ai technology fear wakati wowote.",
            "Inafaa kutafakari kidogo kuhusu ai technology fear.",
            "Hakuna haraka - ai technology fear inaweza kuchukua muda unaohitaji.",
        ],
        "fr": [
            "Pas de pression - ai technology fear peut prendre tout le temps qu'il faut.",
            "Tu peux revenir sur ai technology fear quand tu veux, je serai là.",
            "C'est un beau sujet, ai technology fear - on continue ?",
        ],
    },
    "REMOTE_LEARNING_RESPONSES": {
        "en": [
            "I appreciate you letting me in on remote learning.",
            "You can circle back to remote learning any time - I'll still be here.",
            "Good to know where you stand on remote learning.",
            "I'm always up for talking remote learning whenever you are.",
        ],
        "sw": [
            "Nashukuru kunieleza kuhusu remote learning.",
            "Nitakumbuka ulizungumzia remote learning.",
            "Kwa kweli, remote learning ni jambo zuri la kuzungumzia.",
        ],
        "fr": [
            "C'est un beau sujet, remote learning - on continue ?",
            "Pas de pression - remote learning peut prendre tout le temps qu'il faut.",
            "Honnêtement, remote learning vaut la peine d'en reparler.",
        ],
    },
    "HOBBY_CLUB_RESPONSES": {
        "en": [
            "No rush - hobby club can take as long as you need.",
            "You can circle back to hobby club any time - I'll still be here.",
            "I'm always up for talking hobby club whenever you are.",
            "Worth sitting with for a second - hobby club, that is.",
        ],
        "sw": [
            "Kwa kweli, hobby club ni jambo zuri la kuzungumzia.",
            "Hilo ni wazo zuri kuhusu hobby club, tuendelee?",
            "Niko tayari kuzungumza kuhusu hobby club wakati wowote.",
        ],
        "fr": [
            "Peu importe comment tu veux aborder hobby club, ça me va.",
            "Honnêtement, hobby club vaut la peine d'en reparler.",
            "Je suis toujours partant pour parler de hobby club.",
        ],
    },
    "SNEEZE_HICCUP_RESPONSES": {
        "en": [
            "Worth sitting with for a second - sneeze hiccup, that is.",
            "However you want to take sneeze hiccup from here works for me.",
            "Honestly, sneeze hiccup is a good thing to check in about.",
            "I'll remember you brought up sneeze hiccup.",
        ],
        "sw": [
            "Niko tayari kuzungumza kuhusu sneeze hiccup wakati wowote.",
            "Nashukuru kunieleza kuhusu sneeze hiccup.",
            "Ni vizuri kujua unavyoona sneeze hiccup.",
        ],
        "fr": [
            "Honnêtement, sneeze hiccup vaut la peine d'en reparler.",
            "Je me souviendrai que tu as mentionné sneeze hiccup.",
            "Je suis toujours partant pour parler de sneeze hiccup.",
        ],
    },
    "HANDEDNESS_RESPONSES": {
        "en": [
            "I'll remember you brought up handedness.",
            "That's a nice thread on handedness, want to keep pulling it?",
            "That's a fair way to look at handedness.",
            "Worth sitting with for a second - handedness, that is.",
        ],
        "sw": [
            "Hilo ni wazo zuri kuhusu handedness, tuendelee?",
            "Unaweza kurudi kwenye handedness wakati wowote - bado nitakuwepo.",
            "Kwa kweli, handedness ni jambo zuri la kuzungumzia.",
        ],
        "fr": [
            "Merci de me parler de handedness.",
            "Pas de pression - handedness peut prendre tout le temps qu'il faut.",
            "C'est un beau sujet, handedness - on continue ?",
        ],
    },
    "ASTROLOGY_ZODIAC_RESPONSES": {
        "en": [
            "You can circle back to astrology zodiac any time - I'll still be here.",
            "That's a fair way to look at astrology zodiac.",
            "I'll remember you brought up astrology zodiac.",
            "Good to know where you stand on astrology zodiac.",
        ],
        "sw": [
            "Hakuna haraka - astrology zodiac inaweza kuchukua muda unaohitaji.",
            "Kwa kweli, astrology zodiac ni jambo zuri la kuzungumzia.",
            "Niko tayari kuzungumza kuhusu astrology zodiac wakati wowote.",
        ],
        "fr": [
            "C'est bon de savoir ce que tu penses de astrology zodiac.",
            "Ça vaut la peine de s'arrêter un instant sur astrology zodiac.",
            "C'est un beau sujet, astrology zodiac - on continue ?",
        ],
    },
    "PERSONALITY_TYPE_RESPONSES": {
        "en": [
            "That's a nice thread on personality type, want to keep pulling it?",
            "Worth sitting with for a second - personality type, that is.",
            "However you want to take personality type from here works for me.",
            "Good to know where you stand on personality type.",
        ],
        "sw": [
            "Hilo ni wazo zuri kuhusu personality type, tuendelee?",
            "Niko tayari kuzungumza kuhusu personality type wakati wowote.",
            "Kwa kweli, personality type ni jambo zuri la kuzungumzia.",
        ],
        "fr": [
            "Pas de pression - personality type peut prendre tout le temps qu'il faut.",
            "Ça vaut la peine de s'arrêter un instant sur personality type.",
            "Je suis toujours partant pour parler de personality type.",
        ],
    },
    "LUCKY_SUPERSTITION_RESPONSES": {
        "en": [
            "Worth sitting with for a second - lucky superstition, that is.",
            "You can circle back to lucky superstition any time - I'll still be here.",
            "No rush - lucky superstition can take as long as you need.",
            "I'm following along on lucky superstition, keep going.",
        ],
        "sw": [
            "Hakuna haraka - lucky superstition inaweza kuchukua muda unaohitaji.",
            "Inafaa kutafakari kidogo kuhusu lucky superstition.",
            "Nashukuru kunieleza kuhusu lucky superstition.",
        ],
        "fr": [
            "C'est bon de savoir ce que tu penses de lucky superstition.",
            "Honnêtement, lucky superstition vaut la peine d'en reparler.",
            "Tu peux revenir sur lucky superstition quand tu veux, je serai là.",
        ],
    },
    "FAVORITE_SEASON_RESPONSES": {
        "en": [
            "That's a nice thread on favorite season, want to keep pulling it?",
            "Honestly, favorite season is a good thing to check in about.",
            "I'm following along on favorite season, keep going.",
            "Worth sitting with for a second - favorite season, that is.",
        ],
        "sw": [
            "Hilo ni wazo zuri kuhusu favorite season, tuendelee?",
            "Hakuna haraka - favorite season inaweza kuchukua muda unaohitaji.",
            "Niko tayari kuzungumza kuhusu favorite season wakati wowote.",
        ],
        "fr": [
            "C'est un beau sujet, favorite season - on continue ?",
            "Peu importe comment tu veux aborder favorite season, ça me va.",
            "Je me souviendrai que tu as mentionné favorite season.",
        ],
    },
    "IDEAL_VACATION_RESPONSES": {
        "en": [
            "I appreciate you letting me in on ideal vacation.",
            "No rush - ideal vacation can take as long as you need.",
            "Worth sitting with for a second - ideal vacation, that is.",
            "I'm following along on ideal vacation, keep going.",
        ],
        "sw": [
            "Nitakumbuka ulizungumzia ideal vacation.",
            "Nashukuru kunieleza kuhusu ideal vacation.",
            "Njia yoyote unayotaka kuchukua kuhusu ideal vacation inafaa kwangu.",
        ],
        "fr": [
            "Je me souviendrai que tu as mentionné ideal vacation.",
            "Pas de pression - ideal vacation peut prendre tout le temps qu'il faut.",
            "Ça vaut la peine de s'arrêter un instant sur ideal vacation.",
        ],
    },
    "FIRST_IMPRESSION_RESPONSES": {
        "en": [
            "That's a fair way to look at first impression.",
            "I appreciate you letting me in on first impression.",
            "Good to know where you stand on first impression.",
            "That's a nice thread on first impression, want to keep pulling it?",
        ],
        "sw": [
            "Hilo ni wazo zuri kuhusu first impression, tuendelee?",
            "Nashukuru kunieleza kuhusu first impression.",
            "Njia yoyote unayotaka kuchukua kuhusu first impression inafaa kwangu.",
        ],
        "fr": [
            "Honnêtement, first impression vaut la peine d'en reparler.",
            "Je me souviendrai que tu as mentionné first impression.",
            "Merci de me parler de first impression.",
        ],
    },
    "BUCKET_LIST_RESPONSES": {
        "en": [
            "However you want to take bucket list from here works for me.",
            "I'll remember you brought up bucket list.",
            "Honestly, bucket list is a good thing to check in about.",
            "You can circle back to bucket list any time - I'll still be here.",
        ],
        "sw": [
            "Nitakumbuka ulizungumzia bucket list.",
            "Hilo ni wazo zuri kuhusu bucket list, tuendelee?",
            "Njia yoyote unayotaka kuchukua kuhusu bucket list inafaa kwangu.",
        ],
        "fr": [
            "Pas de pression - bucket list peut prendre tout le temps qu'il faut.",
            "C'est un beau sujet, bucket list - on continue ?",
            "Je me souviendrai que tu as mentionné bucket list.",
        ],
    },
    "GIVE_COMPLIMENT_TO_BOT_RESPONSES": {
        "en": [
            "No rush - give compliment to bot can take as long as you need.",
            "I appreciate you letting me in on give compliment to bot.",
            "Worth sitting with for a second - give compliment to bot, that is.",
            "However you want to take give compliment to bot from here works for me.",
        ],
        "sw": [
            "Njia yoyote unayotaka kuchukua kuhusu give compliment to bot inafaa kwangu.",
            "Nashukuru kunieleza kuhusu give compliment to bot.",
            "Inafaa kutafakari kidogo kuhusu give compliment to bot.",
        ],
        "fr": [
            "Tu peux revenir sur give compliment to bot quand tu veux, je serai là.",
            "C'est un beau sujet, give compliment to bot - on continue ?",
            "C'est bon de savoir ce que tu penses de give compliment to bot.",
        ],
    },
    "CONVERSATION_STARTER_RESPONSES": {
        "en": [
            "No rush - conversation starter can take as long as you need.",
            "However you want to take conversation starter from here works for me.",
            "I'm following along on conversation starter, keep going.",
            "I'll remember you brought up conversation starter.",
        ],
        "sw": [
            "Ni vizuri kujua unavyoona conversation starter.",
            "Hakuna haraka - conversation starter inaweza kuchukua muda unaohitaji.",
            "Unaweza kurudi kwenye conversation starter wakati wowote - bado nitakuwepo.",
        ],
        "fr": [
            "Je me souviendrai que tu as mentionné conversation starter.",
            "Je suis toujours partant pour parler de conversation starter.",
            "Tu peux revenir sur conversation starter quand tu veux, je serai là.",
        ],
    },
    "CONVERSATIONAL_FILLER_STARTER_RESPONSES": {
        "en": [
            "No rush - conversational filler starter can take as long as you need.",
            "I'll remember you brought up conversational filler starter.",
            "I appreciate you letting me in on conversational filler starter.",
            "I'm always up for talking conversational filler starter whenever you are.",
        ],
        "sw": [
            "Ni vizuri kujua unavyoona conversational filler starter.",
            "Kwa kweli, conversational filler starter ni jambo zuri la kuzungumzia.",
            "Njia yoyote unayotaka kuchukua kuhusu conversational filler starter inafaa kwangu.",
        ],
        "fr": [
            "C'est bon de savoir ce que tu penses de conversational filler starter.",
            "Peu importe comment tu veux aborder conversational filler starter, ça me va.",
            "Je me souviendrai que tu as mentionné conversational filler starter.",
        ],
    },
    "LUCK_FORTUNE_RESPONSES": {
        "en": [
            "No rush - luck fortune can take as long as you need.",
            "Good to know where you stand on luck fortune.",
            "I'll remember you brought up luck fortune.",
            "I'm always up for talking luck fortune whenever you are.",
        ],
        "sw": [
            "Ni vizuri kujua unavyoona luck fortune.",
            "Unaweza kurudi kwenye luck fortune wakati wowote - bado nitakuwepo.",
            "Nashukuru kunieleza kuhusu luck fortune.",
        ],
        "fr": [
            "Je suis toujours partant pour parler de luck fortune.",
            "Pas de pression - luck fortune peut prendre tout le temps qu'il faut.",
            "Tu peux revenir sur luck fortune quand tu veux, je serai là.",
        ],
    },
    "RELAXING_WEEKEND_RESPONSES": {
        "en": [
            "Worth sitting with for a second - relaxing weekend, that is.",
            "I appreciate you letting me in on relaxing weekend.",
            "I'm following along on relaxing weekend, keep going.",
            "That's a nice thread on relaxing weekend, want to keep pulling it?",
        ],
        "sw": [
            "Kwa kweli, relaxing weekend ni jambo zuri la kuzungumzia.",
            "Hilo ni wazo zuri kuhusu relaxing weekend, tuendelee?",
            "Unaweza kurudi kwenye relaxing weekend wakati wowote - bado nitakuwepo.",
        ],
        "fr": [
            "Peu importe comment tu veux aborder relaxing weekend, ça me va.",
            "C'est un beau sujet, relaxing weekend - on continue ?",
            "Ça vaut la peine de s'arrêter un instant sur relaxing weekend.",
        ],
    },
    "PROUD_OF_SOMEONE_RESPONSES": {
        "en": [
            "Worth sitting with for a second - proud of someone, that is.",
            "I'll remember you brought up proud of someone.",
            "Good to know where you stand on proud of someone.",
            "No rush - proud of someone can take as long as you need.",
        ],
        "sw": [
            "Unaweza kurudi kwenye proud of someone wakati wowote - bado nitakuwepo.",
            "Niko tayari kuzungumza kuhusu proud of someone wakati wowote.",
            "Hakuna haraka - proud of someone inaweza kuchukua muda unaohitaji.",
        ],
        "fr": [
            "Peu importe comment tu veux aborder proud of someone, ça me va.",
            "C'est bon de savoir ce que tu penses de proud of someone.",
            "Ça vaut la peine de s'arrêter un instant sur proud of someone.",
        ],
    },
    "FORGIVENESS_RESPONSES": {
        "en": [
            "I appreciate you letting me in on forgiveness.",
            "You can circle back to forgiveness any time - I'll still be here.",
            "Honestly, forgiveness is a good thing to check in about.",
            "However you want to take forgiveness from here works for me.",
        ],
        "sw": [
            "Inafaa kutafakari kidogo kuhusu forgiveness.",
            "Hilo ni wazo zuri kuhusu forgiveness, tuendelee?",
            "Kwa kweli, forgiveness ni jambo zuri la kuzungumzia.",
        ],
        "fr": [
            "Merci de me parler de forgiveness.",
            "Ça vaut la peine de s'arrêter un instant sur forgiveness.",
            "C'est un beau sujet, forgiveness - on continue ?",
        ],
    },
    "MISTAKE_LEARNING_RESPONSES": {
        "en": [
            "Honestly, mistake learning is a good thing to check in about.",
            "I appreciate you letting me in on mistake learning.",
            "You can circle back to mistake learning any time - I'll still be here.",
            "No rush - mistake learning can take as long as you need.",
        ],
        "sw": [
            "Nitakumbuka ulizungumzia mistake learning.",
            "Inafaa kutafakari kidogo kuhusu mistake learning.",
            "Unaweza kurudi kwenye mistake learning wakati wowote - bado nitakuwepo.",
        ],
        "fr": [
            "Je suis toujours partant pour parler de mistake learning.",
            "Je me souviendrai que tu as mentionné mistake learning.",
            "Tu peux revenir sur mistake learning quand tu veux, je serai là.",
        ],
    },
    "TRUST_ISSUES_RESPONSES": {
        "en": [
            "No rush - trust issues can take as long as you need.",
            "You can circle back to trust issues any time - I'll still be here.",
            "I'm always up for talking trust issues whenever you are.",
            "However you want to take trust issues from here works for me.",
        ],
        "sw": [
            "Njia yoyote unayotaka kuchukua kuhusu trust issues inafaa kwangu.",
            "Niko tayari kuzungumza kuhusu trust issues wakati wowote.",
            "Unaweza kurudi kwenye trust issues wakati wowote - bado nitakuwepo.",
        ],
        "fr": [
            "Je suis toujours partant pour parler de trust issues.",
            "Je me souviendrai que tu as mentionné trust issues.",
            "C'est bon de savoir ce que tu penses de trust issues.",
        ],
    },
    "SETTING_BOUNDARIES_RESPONSES": {
        "en": [
            "You can circle back to setting boundaries any time - I'll still be here.",
            "I'll remember you brought up setting boundaries.",
            "No rush - setting boundaries can take as long as you need.",
            "I appreciate you letting me in on setting boundaries.",
        ],
        "sw": [
            "Hakuna haraka - setting boundaries inaweza kuchukua muda unaohitaji.",
            "Nashukuru kunieleza kuhusu setting boundaries.",
            "Njia yoyote unayotaka kuchukua kuhusu setting boundaries inafaa kwangu.",
        ],
        "fr": [
            "Peu importe comment tu veux aborder setting boundaries, ça me va.",
            "Ça vaut la peine de s'arrêter un instant sur setting boundaries.",
            "C'est bon de savoir ce que tu penses de setting boundaries.",
        ],
    },
    "SELF_CARE_ROUTINE_RESPONSES": {
        "en": [
            "That's a nice thread on self care routine, want to keep pulling it?",
            "I'm always up for talking self care routine whenever you are.",
            "You can circle back to self care routine any time - I'll still be here.",
            "I'll remember you brought up self care routine.",
        ],
        "sw": [
            "Hakuna haraka - self care routine inaweza kuchukua muda unaohitaji.",
            "Niko tayari kuzungumza kuhusu self care routine wakati wowote.",
            "Hilo ni wazo zuri kuhusu self care routine, tuendelee?",
        ],
        "fr": [
            "Pas de pression - self care routine peut prendre tout le temps qu'il faut.",
            "C'est un beau sujet, self care routine - on continue ?",
            "Ça vaut la peine de s'arrêter un instant sur self care routine.",
        ],
    },
    "FEELING_STUCK_RESPONSES": {
        "en": [
            "I appreciate you letting me in on feeling stuck.",
            "I'll remember you brought up feeling stuck.",
            "You can circle back to feeling stuck any time - I'll still be here.",
            "I'm following along on feeling stuck, keep going.",
        ],
        "sw": [
            "Hilo ni wazo zuri kuhusu feeling stuck, tuendelee?",
            "Hakuna haraka - feeling stuck inaweza kuchukua muda unaohitaji.",
            "Nitakumbuka ulizungumzia feeling stuck.",
        ],
        "fr": [
            "Je me souviendrai que tu as mentionné feeling stuck.",
            "Ça vaut la peine de s'arrêter un instant sur feeling stuck.",
            "Honnêtement, feeling stuck vaut la peine d'en reparler.",
        ],
    },
    "LIFE_TRANSITION_RESPONSES": {
        "en": [
            "I appreciate you letting me in on life transition.",
            "That's a nice thread on life transition, want to keep pulling it?",
            "I'm always up for talking life transition whenever you are.",
            "However you want to take life transition from here works for me.",
        ],
        "sw": [
            "Niko tayari kuzungumza kuhusu life transition wakati wowote.",
            "Unaweza kurudi kwenye life transition wakati wowote - bado nitakuwepo.",
            "Njia yoyote unayotaka kuchukua kuhusu life transition inafaa kwangu.",
        ],
        "fr": [
            "Je suis toujours partant pour parler de life transition.",
            "C'est un beau sujet, life transition - on continue ?",
            "Je me souviendrai que tu as mentionné life transition.",
        ],
    },
    "HOPE_FUTURE_RESPONSES": {
        "en": [
            "However you want to take hope future from here works for me.",
            "No rush - hope future can take as long as you need.",
            "I appreciate you letting me in on hope future.",
            "Honestly, hope future is a good thing to check in about.",
        ],
        "sw": [
            "Hakuna haraka - hope future inaweza kuchukua muda unaohitaji.",
            "Hilo ni wazo zuri kuhusu hope future, tuendelee?",
            "Nitakumbuka ulizungumzia hope future.",
        ],
        "fr": [
            "Je suis toujours partant pour parler de hope future.",
            "Tu peux revenir sur hope future quand tu veux, je serai là.",
            "Pas de pression - hope future peut prendre tout le temps qu'il faut.",
        ],
    },
    "GRATITUDE_PRACTICE_RESPONSES": {
        "en": [
            "I'm always up for talking gratitude practice whenever you are.",
            "No rush - gratitude practice can take as long as you need.",
            "Good to know where you stand on gratitude practice.",
            "That's a nice thread on gratitude practice, want to keep pulling it?",
        ],
        "sw": [
            "Unaweza kurudi kwenye gratitude practice wakati wowote - bado nitakuwepo.",
            "Nashukuru kunieleza kuhusu gratitude practice.",
            "Hakuna haraka - gratitude practice inaweza kuchukua muda unaohitaji.",
        ],
        "fr": [
            "C'est bon de savoir ce que tu penses de gratitude practice.",
            "Ça vaut la peine de s'arrêter un instant sur gratitude practice.",
            "Honnêtement, gratitude practice vaut la peine d'en reparler.",
        ],
    },
}

for _bank_name, _extra_langs in _EXTRA_RESPONSE_PHRASES_2.items():
    _bank = globals().get(_bank_name)
    if isinstance(_bank, dict):
        for _lang, _phrases in _extra_langs.items():
            _bank.setdefault(_lang, []).extend(_phrases)

# ==============================================================================
