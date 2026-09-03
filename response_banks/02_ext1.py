"""Section 8-EXT: expanded response variety (auto-templated)
Part of the response-bank data set - see chatbot_modules/13_response_banks_loader.py.
"""

# SECTION 8-EXT: EXPANDED RESPONSE VARIETY (auto-templated supplementary phrasing)
# ==============================================================================
#
# The banks above this point (Section 8) are individually hand-written, one
# line at a time. This block is different and is labeled as such: it's a
# programmatically generated SUPPLEMENT that adds a handful of extra, more
# generic phrasings to every single response bank above, purely to widen reply
# variety further without hand-typing thousands more one-off lines. Nothing
# here is learned or fetched at runtime - it's fixed, deterministic template
# text (seeded RNG, same output every run), merged into the existing banks
# once at import time by the loop at the bottom of this section.
_EXTRA_RESPONSE_PHRASES = {
    "GREETING_RESPONSES": {
        "en": [
            "There's always more to say about greeting.",
            "I don't think we've fully covered greeting yet - what else is on your mind?",
            "I like where this greeting conversation is headed.",
        ],
        "sw": [
            "Hilo ni jambo zuri kuhusu greeting.",
            "Kuna mengi zaidi ya kusema kuhusu greeting.",
        ],
        "fr": [
            "Content que tu aies parlé de greeting - continue, j'écoute.",
            "N'hésite pas à m'en dire plus sur greeting quand tu veux.",
        ],
    },
    "FAREWELL_RESPONSES": {
        "en": [
            "There's always more to say about farewell.",
            "Noted - I'll keep that in mind as we talk about farewell.",
            "That's interesting, tell me a bit more about farewell.",
        ],
        "sw": [
            "Ningeweza kuendelea kuzungumza kuhusu farewell kwa muda.",
            "Bado hatujamaliza kuzungumza kuhusu farewell - kuna nini kingine?",
        ],
        "fr": [
            "On n'a pas encore tout dit sur farewell - quoi d'autre ?",
            "Merci d'avoir partagé ça - farewell mérite qu'on en parle.",
        ],
    },
    "THANKS_RESPONSES": {
        "en": [
            "That's a good angle on thanks, honestly.",
            "That's interesting, tell me a bit more about thanks.",
            "I don't think we've fully covered thanks yet - what else is on your mind?",
        ],
        "sw": [
            "Hilo ni jambo zuri kuhusu thanks.",
            "Jisikie huru kunieleza zaidi kuhusu thanks wakati wowote.",
        ],
        "fr": [
            "Je pourrais continuer à parler de thanks un moment.",
            "Il y a toujours plus à dire sur thanks.",
        ],
    },
    "HOW_ARE_YOU_RESPONSES": {
        "en": [
            "Thanks for sharing that - how are you is worth talking through.",
            "I like where this how are you conversation is headed.",
            "I don't think we've fully covered how are you yet - what else is on your mind?",
        ],
        "sw": [
            "Nafurahi umetaja how are you - endelea, nasikiliza.",
            "Jisikie huru kunieleza zaidi kuhusu how are you wakati wowote.",
        ],
        "fr": [
            "Je pourrais continuer à parler de how are you un moment.",
            "Content que tu aies parlé de how are you - continue, j'écoute.",
        ],
    },
    "UNKNOWN_RESPONSES": {
        "en": [
            "I like where this unknown conversation is headed.",
            "Glad you brought unknown up - keep going, I'm listening.",
            "That's a good angle on unknown, honestly.",
        ],
        "sw": [
            "Jisikie huru kunieleza zaidi kuhusu unknown wakati wowote.",
            "Bado hatujamaliza kuzungumza kuhusu unknown - kuna nini kingine?",
        ],
        "fr": [
            "Il y a toujours plus à dire sur unknown.",
            "C'est un bon point de vue sur unknown.",
        ],
    },
    "COMPLIMENT_RESPONSES": {
        "en": [
            "There's always more to say about compliment.",
            "Feel free to tell me more about compliment whenever you like.",
            "Noted - I'll keep that in mind as we talk about compliment.",
        ],
        "sw": [
            "Napenda mwelekeo wa mazungumzo haya kuhusu compliment.",
            "Ningeweza kuendelea kuzungumza kuhusu compliment kwa muda.",
        ],
        "fr": [
            "On n'a pas encore tout dit sur compliment - quoi d'autre ?",
            "N'hésite pas à m'en dire plus sur compliment quand tu veux.",
        ],
    },
    "WEATHER_SMALLTALK_RESPONSES": {
        "en": [
            "Thanks for sharing that - weather smalltalk is worth talking through.",
            "Noted - I'll keep that in mind as we talk about weather smalltalk.",
            "There's always more to say about weather smalltalk.",
        ],
        "sw": [
            "Ningeweza kuendelea kuzungumza kuhusu weather smalltalk kwa muda.",
            "Bado hatujamaliza kuzungumza kuhusu weather smalltalk - kuna nini kingine?",
        ],
        "fr": [
            "J'aime la direction que prend cette discussion sur weather smalltalk.",
            "Je pourrais continuer à parler de weather smalltalk un moment.",
        ],
    },
    "FEELINGS_HAPPY_RESPONSES": {
        "en": [
            "That's interesting, tell me a bit more about feelings happy.",
            "Feel free to tell me more about feelings happy whenever you like.",
            "That's a good angle on feelings happy, honestly.",
        ],
        "sw": [
            "Kuna mengi zaidi ya kusema kuhusu feelings happy.",
            "Bado hatujamaliza kuzungumza kuhusu feelings happy - kuna nini kingine?",
        ],
        "fr": [
            "C'est un bon point de vue sur feelings happy.",
            "Je pourrais continuer à parler de feelings happy un moment.",
        ],
    },
    "FEELINGS_SAD_RESPONSES": {
        "en": [
            "I like where this feelings sad conversation is headed.",
            "There's always more to say about feelings sad.",
            "That's a good angle on feelings sad, honestly.",
        ],
        "sw": [
            "Kuna mengi zaidi ya kusema kuhusu feelings sad.",
            "Hilo ni jambo zuri kuhusu feelings sad.",
        ],
        "fr": [
            "J'aime la direction que prend cette discussion sur feelings sad.",
            "C'est un bon point de vue sur feelings sad.",
        ],
    },
    "FEELINGS_TIRED_RESPONSES": {
        "en": [
            "Feel free to tell me more about feelings tired whenever you like.",
            "Glad you brought feelings tired up - keep going, I'm listening.",
            "That's interesting, tell me a bit more about feelings tired.",
        ],
        "sw": [
            "Jisikie huru kunieleza zaidi kuhusu feelings tired wakati wowote.",
            "Kuna mengi zaidi ya kusema kuhusu feelings tired.",
        ],
        "fr": [
            "J'aime la direction que prend cette discussion sur feelings tired.",
            "N'hésite pas à m'en dire plus sur feelings tired quand tu veux.",
        ],
    },
    "FOOD_HUNGRY_RESPONSES": {
        "en": [
            "There's always more to say about food hungry.",
            "Glad you brought food hungry up - keep going, I'm listening.",
            "That's a good angle on food hungry, honestly.",
        ],
        "sw": [
            "Nafurahi umetaja food hungry - endelea, nasikiliza.",
            "Hilo ni jambo zuri kuhusu food hungry.",
        ],
        "fr": [
            "Je pourrais continuer à parler de food hungry un moment.",
            "Content que tu aies parlé de food hungry - continue, j'écoute.",
        ],
    },
    "FOOD_THIRSTY_RESPONSES": {
        "en": [
            "Noted - I'll keep that in mind as we talk about food thirsty.",
            "That's a good angle on food thirsty, honestly.",
            "Feel free to tell me more about food thirsty whenever you like.",
        ],
        "sw": [
            "Bado hatujamaliza kuzungumza kuhusu food thirsty - kuna nini kingine?",
            "Kuna mengi zaidi ya kusema kuhusu food thirsty.",
        ],
        "fr": [
            "On n'a pas encore tout dit sur food thirsty - quoi d'autre ?",
            "Je pourrais continuer à parler de food thirsty un moment.",
        ],
    },
    "HOBBIES_RESPONSES": {
        "en": [
            "Feel free to tell me more about hobbies whenever you like.",
            "I could keep chatting about hobbies for a while.",
            "I like where this hobbies conversation is headed.",
        ],
        "sw": [
            "Kuna mengi zaidi ya kusema kuhusu hobbies.",
            "Asante kwa kushiriki - hobbies inafaa kuzungumziwa.",
        ],
        "fr": [
            "N'hésite pas à m'en dire plus sur hobbies quand tu veux.",
            "Il y a toujours plus à dire sur hobbies.",
        ],
    },
    "FAMILY_RESPONSES": {
        "en": [
            "Thanks for sharing that - family is worth talking through.",
            "I could keep chatting about family for a while.",
            "That's interesting, tell me a bit more about family.",
        ],
        "sw": [
            "Nafurahi umetaja family - endelea, nasikiliza.",
            "Asante kwa kushiriki - family inafaa kuzungumziwa.",
        ],
        "fr": [
            "Content que tu aies parlé de family - continue, j'écoute.",
            "Il y a toujours plus à dire sur family.",
        ],
    },
    "WORK_SCHOOL_RESPONSES": {
        "en": [
            "Noted - I'll keep that in mind as we talk about work school.",
            "That's interesting, tell me a bit more about work school.",
            "I like where this work school conversation is headed.",
        ],
        "sw": [
            "Ningeweza kuendelea kuzungumza kuhusu work school kwa muda.",
            "Napenda mwelekeo wa mazungumzo haya kuhusu work school.",
        ],
        "fr": [
            "Je pourrais continuer à parler de work school un moment.",
            "Content que tu aies parlé de work school - continue, j'écoute.",
        ],
    },
    "AGREEMENT_RESPONSES": {
        "en": [
            "That's a good angle on agreement, honestly.",
            "Glad you brought agreement up - keep going, I'm listening.",
            "Thanks for sharing that - agreement is worth talking through.",
        ],
        "sw": [
            "Kuna mengi zaidi ya kusema kuhusu agreement.",
            "Ningeweza kuendelea kuzungumza kuhusu agreement kwa muda.",
        ],
        "fr": [
            "On n'a pas encore tout dit sur agreement - quoi d'autre ?",
            "Je pourrais continuer à parler de agreement un moment.",
        ],
    },
    "DISAGREEMENT_RESPONSES": {
        "en": [
            "There's always more to say about disagreement.",
            "Glad you brought disagreement up - keep going, I'm listening.",
            "Noted - I'll keep that in mind as we talk about disagreement.",
        ],
        "sw": [
            "Ningeweza kuendelea kuzungumza kuhusu disagreement kwa muda.",
            "Napenda mwelekeo wa mazungumzo haya kuhusu disagreement.",
        ],
        "fr": [
            "Il y a toujours plus à dire sur disagreement.",
            "C'est un bon point de vue sur disagreement.",
        ],
    },
    "APOLOGY_RESPONSES": {
        "en": [
            "I could keep chatting about apology for a while.",
            "Thanks for sharing that - apology is worth talking through.",
            "I like where this apology conversation is headed.",
        ],
        "sw": [
            "Bado hatujamaliza kuzungumza kuhusu apology - kuna nini kingine?",
            "Jisikie huru kunieleza zaidi kuhusu apology wakati wowote.",
        ],
        "fr": [
            "Il y a toujours plus à dire sur apology.",
            "N'hésite pas à m'en dire plus sur apology quand tu veux.",
        ],
    },
    "BOREDOM_RESPONSES": {
        "en": [
            "Noted - I'll keep that in mind as we talk about boredom.",
            "I like where this boredom conversation is headed.",
            "Feel free to tell me more about boredom whenever you like.",
        ],
        "sw": [
            "Kuna mengi zaidi ya kusema kuhusu boredom.",
            "Nafurahi umetaja boredom - endelea, nasikiliza.",
        ],
        "fr": [
            "Je pourrais continuer à parler de boredom un moment.",
            "Il y a toujours plus à dire sur boredom.",
        ],
    },
    "LOVE_RELATIONSHIPS_RESPONSES": {
        "en": [
            "Thanks for sharing that - love relationships is worth talking through.",
            "I don't think we've fully covered love relationships yet - what else is on your mind?",
            "I like where this love relationships conversation is headed.",
        ],
        "sw": [
            "Nafurahi umetaja love relationships - endelea, nasikiliza.",
            "Napenda mwelekeo wa mazungumzo haya kuhusu love relationships.",
        ],
        "fr": [
            "Il y a toujours plus à dire sur love relationships.",
            "Je pourrais continuer à parler de love relationships un moment.",
        ],
    },
    "MUSIC_RESPONSES": {
        "en": [
            "I like where this music conversation is headed.",
            "Noted - I'll keep that in mind as we talk about music.",
            "That's a good angle on music, honestly.",
        ],
        "sw": [
            "Nafurahi umetaja music - endelea, nasikiliza.",
            "Asante kwa kushiriki - music inafaa kuzungumziwa.",
        ],
        "fr": [
            "Content que tu aies parlé de music - continue, j'écoute.",
            "J'aime la direction que prend cette discussion sur music.",
        ],
    },
    "SPORTS_RESPONSES": {
        "en": [
            "Noted - I'll keep that in mind as we talk about sports.",
            "I don't think we've fully covered sports yet - what else is on your mind?",
            "Feel free to tell me more about sports whenever you like.",
        ],
        "sw": [
            "Asante kwa kushiriki - sports inafaa kuzungumziwa.",
            "Bado hatujamaliza kuzungumza kuhusu sports - kuna nini kingine?",
        ],
        "fr": [
            "Il y a toujours plus à dire sur sports.",
            "Content que tu aies parlé de sports - continue, j'écoute.",
        ],
    },
    "BOOKS_RESPONSES": {
        "en": [
            "I like where this books conversation is headed.",
            "That's a good angle on books, honestly.",
            "I don't think we've fully covered books yet - what else is on your mind?",
        ],
        "sw": [
            "Hilo ni jambo zuri kuhusu books.",
            "Napenda mwelekeo wa mazungumzo haya kuhusu books.",
        ],
        "fr": [
            "Il y a toujours plus à dire sur books.",
            "On n'a pas encore tout dit sur books - quoi d'autre ?",
        ],
    },
    "TECHNOLOGY_RESPONSES": {
        "en": [
            "Thanks for sharing that - technology is worth talking through.",
            "There's always more to say about technology.",
            "Glad you brought technology up - keep going, I'm listening.",
        ],
        "sw": [
            "Nafurahi umetaja technology - endelea, nasikiliza.",
            "Jisikie huru kunieleza zaidi kuhusu technology wakati wowote.",
        ],
        "fr": [
            "Merci d'avoir partagé ça - technology mérite qu'on en parle.",
            "J'aime la direction que prend cette discussion sur technology.",
        ],
    },
    "PETS_ANIMALS_RESPONSES": {
        "en": [
            "Glad you brought pets animals up - keep going, I'm listening.",
            "I like where this pets animals conversation is headed.",
            "I could keep chatting about pets animals for a while.",
        ],
        "sw": [
            "Hilo ni jambo zuri kuhusu pets animals.",
            "Napenda mwelekeo wa mazungumzo haya kuhusu pets animals.",
        ],
        "fr": [
            "C'est un bon point de vue sur pets animals.",
            "N'hésite pas à m'en dire plus sur pets animals quand tu veux.",
        ],
    },
    "TRAVEL_RESPONSES": {
        "en": [
            "I like where this travel conversation is headed.",
            "I could keep chatting about travel for a while.",
            "Feel free to tell me more about travel whenever you like.",
        ],
        "sw": [
            "Asante kwa kushiriki - travel inafaa kuzungumziwa.",
            "Napenda mwelekeo wa mazungumzo haya kuhusu travel.",
        ],
        "fr": [
            "Merci d'avoir partagé ça - travel mérite qu'on en parle.",
            "On n'a pas encore tout dit sur travel - quoi d'autre ?",
        ],
    },
    "HEALTH_RESPONSES": {
        "en": [
            "That's a good angle on health, honestly.",
            "That's interesting, tell me a bit more about health.",
            "There's always more to say about health.",
        ],
        "sw": [
            "Jisikie huru kunieleza zaidi kuhusu health wakati wowote.",
            "Bado hatujamaliza kuzungumza kuhusu health - kuna nini kingine?",
        ],
        "fr": [
            "C'est un bon point de vue sur health.",
            "J'aime la direction que prend cette discussion sur health.",
        ],
    },
    "MONEY_RESPONSES": {
        "en": [
            "That's a good angle on money, honestly.",
            "I don't think we've fully covered money yet - what else is on your mind?",
            "There's always more to say about money.",
        ],
        "sw": [
            "Bado hatujamaliza kuzungumza kuhusu money - kuna nini kingine?",
            "Kuna mengi zaidi ya kusema kuhusu money.",
        ],
        "fr": [
            "Il y a toujours plus à dire sur money.",
            "On n'a pas encore tout dit sur money - quoi d'autre ?",
        ],
    },
    "BIRTHDAY_RESPONSES": {
        "en": [
            "Feel free to tell me more about birthday whenever you like.",
            "There's always more to say about birthday.",
            "That's a good angle on birthday, honestly.",
        ],
        "sw": [
            "Napenda mwelekeo wa mazungumzo haya kuhusu birthday.",
            "Jisikie huru kunieleza zaidi kuhusu birthday wakati wowote.",
        ],
        "fr": [
            "Merci d'avoir partagé ça - birthday mérite qu'on en parle.",
            "Il y a toujours plus à dire sur birthday.",
        ],
    },
    "CONFUSION_RESPONSES": {
        "en": [
            "Noted - I'll keep that in mind as we talk about confusion.",
            "Glad you brought confusion up - keep going, I'm listening.",
            "Thanks for sharing that - confusion is worth talking through.",
        ],
        "sw": [
            "Hilo ni jambo zuri kuhusu confusion.",
            "Ningeweza kuendelea kuzungumza kuhusu confusion kwa muda.",
        ],
        "fr": [
            "Merci d'avoir partagé ça - confusion mérite qu'on en parle.",
            "Je pourrais continuer à parler de confusion un moment.",
        ],
    },
    "ENCOURAGEMENT_RESPONSES": {
        "en": [
            "I could keep chatting about encouragement for a while.",
            "That's a good angle on encouragement, honestly.",
            "There's always more to say about encouragement.",
        ],
        "sw": [
            "Kuna mengi zaidi ya kusema kuhusu encouragement.",
            "Jisikie huru kunieleza zaidi kuhusu encouragement wakati wowote.",
        ],
        "fr": [
            "Je pourrais continuer à parler de encouragement un moment.",
            "Content que tu aies parlé de encouragement - continue, j'écoute.",
        ],
    },
    "CONGRATULATIONS_RESPONSES": {
        "en": [
            "I could keep chatting about congratulations for a while.",
            "That's interesting, tell me a bit more about congratulations.",
            "Thanks for sharing that - congratulations is worth talking through.",
        ],
        "sw": [
            "Bado hatujamaliza kuzungumza kuhusu congratulations - kuna nini kingine?",
            "Jisikie huru kunieleza zaidi kuhusu congratulations wakati wowote.",
        ],
        "fr": [
            "Il y a toujours plus à dire sur congratulations.",
            "On n'a pas encore tout dit sur congratulations - quoi d'autre ?",
        ],
    },
    "SURPRISE_RESPONSES": {
        "en": [
            "I could keep chatting about surprise for a while.",
            "Feel free to tell me more about surprise whenever you like.",
            "There's always more to say about surprise.",
        ],
        "sw": [
            "Hilo ni jambo zuri kuhusu surprise.",
            "Kuna mengi zaidi ya kusema kuhusu surprise.",
        ],
        "fr": [
            "C'est un bon point de vue sur surprise.",
            "J'aime la direction que prend cette discussion sur surprise.",
        ],
    },
    "SMALL_REQUEST_RESPONSES": {
        "en": [
            "Thanks for sharing that - small request is worth talking through.",
            "Glad you brought small request up - keep going, I'm listening.",
            "I could keep chatting about small request for a while.",
        ],
        "sw": [
            "Nafurahi umetaja small request - endelea, nasikiliza.",
            "Asante kwa kushiriki - small request inafaa kuzungumziwa.",
        ],
        "fr": [
            "Merci d'avoir partagé ça - small request mérite qu'on en parle.",
            "Il y a toujours plus à dire sur small request.",
        ],
    },
    "BOT_IDENTITY_CURIOSITY_RESPONSES": {
        "en": [
            "There's always more to say about bot identity curiosity.",
            "Thanks for sharing that - bot identity curiosity is worth talking through.",
            "That's interesting, tell me a bit more about bot identity curiosity.",
        ],
        "sw": [
            "Bado hatujamaliza kuzungumza kuhusu bot identity curiosity - kuna nini kingine?",
            "Jisikie huru kunieleza zaidi kuhusu bot identity curiosity wakati wowote.",
        ],
        "fr": [
            "On n'a pas encore tout dit sur bot identity curiosity - quoi d'autre ?",
            "Merci d'avoir partagé ça - bot identity curiosity mérite qu'on en parle.",
        ],
    },
    "GOODNIGHT_RESPONSES": {
        "en": [
            "That's a good angle on goodnight, honestly.",
            "Glad you brought goodnight up - keep going, I'm listening.",
            "I could keep chatting about goodnight for a while.",
        ],
        "sw": [
            "Asante kwa kushiriki - goodnight inafaa kuzungumziwa.",
            "Hilo ni jambo zuri kuhusu goodnight.",
        ],
        "fr": [
            "C'est un bon point de vue sur goodnight.",
            "Je pourrais continuer à parler de goodnight un moment.",
        ],
    },
    "GOOD_MORNING_RESPONSES": {
        "en": [
            "I could keep chatting about good morning for a while.",
            "I don't think we've fully covered good morning yet - what else is on your mind?",
            "Glad you brought good morning up - keep going, I'm listening.",
        ],
        "sw": [
            "Ningeweza kuendelea kuzungumza kuhusu good morning kwa muda.",
            "Bado hatujamaliza kuzungumza kuhusu good morning - kuna nini kingine?",
        ],
        "fr": [
            "Je pourrais continuer à parler de good morning un moment.",
            "Content que tu aies parlé de good morning - continue, j'écoute.",
        ],
    },
    "GOOD_EVENING_RESPONSES": {
        "en": [
            "Thanks for sharing that - good evening is worth talking through.",
            "I like where this good evening conversation is headed.",
            "I could keep chatting about good evening for a while.",
        ],
        "sw": [
            "Asante kwa kushiriki - good evening inafaa kuzungumziwa.",
            "Kuna mengi zaidi ya kusema kuhusu good evening.",
        ],
        "fr": [
            "C'est un bon point de vue sur good evening.",
            "Content que tu aies parlé de good evening - continue, j'écoute.",
        ],
    },
    "WEEKEND_RESPONSES": {
        "en": [
            "That's a good angle on weekend, honestly.",
            "I don't think we've fully covered weekend yet - what else is on your mind?",
            "Noted - I'll keep that in mind as we talk about weekend.",
        ],
        "sw": [
            "Jisikie huru kunieleza zaidi kuhusu weekend wakati wowote.",
            "Bado hatujamaliza kuzungumza kuhusu weekend - kuna nini kingine?",
        ],
        "fr": [
            "On n'a pas encore tout dit sur weekend - quoi d'autre ?",
            "J'aime la direction que prend cette discussion sur weekend.",
        ],
    },
    "WEATHER_COLD_RESPONSES": {
        "en": [
            "Thanks for sharing that - weather cold is worth talking through.",
            "Noted - I'll keep that in mind as we talk about weather cold.",
            "Glad you brought weather cold up - keep going, I'm listening.",
        ],
        "sw": [
            "Bado hatujamaliza kuzungumza kuhusu weather cold - kuna nini kingine?",
            "Napenda mwelekeo wa mazungumzo haya kuhusu weather cold.",
        ],
        "fr": [
            "Il y a toujours plus à dire sur weather cold.",
            "Je pourrais continuer à parler de weather cold un moment.",
        ],
    },
    "WEATHER_HOT_RESPONSES": {
        "en": [
            "Glad you brought weather hot up - keep going, I'm listening.",
            "There's always more to say about weather hot.",
            "Noted - I'll keep that in mind as we talk about weather hot.",
        ],
        "sw": [
            "Hilo ni jambo zuri kuhusu weather hot.",
            "Asante kwa kushiriki - weather hot inafaa kuzungumziwa.",
        ],
        "fr": [
            "Il y a toujours plus à dire sur weather hot.",
            "J'aime la direction que prend cette discussion sur weather hot.",
        ],
    },
    "WEATHER_RAIN_RESPONSES": {
        "en": [
            "That's a good angle on weather rain, honestly.",
            "I don't think we've fully covered weather rain yet - what else is on your mind?",
            "There's always more to say about weather rain.",
        ],
        "sw": [
            "Ningeweza kuendelea kuzungumza kuhusu weather rain kwa muda.",
            "Jisikie huru kunieleza zaidi kuhusu weather rain wakati wowote.",
        ],
        "fr": [
            "N'hésite pas à m'en dire plus sur weather rain quand tu veux.",
            "Content que tu aies parlé de weather rain - continue, j'écoute.",
        ],
    },
    "WEATHER_SNOW_RESPONSES": {
        "en": [
            "That's a good angle on weather snow, honestly.",
            "Feel free to tell me more about weather snow whenever you like.",
            "That's interesting, tell me a bit more about weather snow.",
        ],
        "sw": [
            "Napenda mwelekeo wa mazungumzo haya kuhusu weather snow.",
            "Hilo ni jambo zuri kuhusu weather snow.",
        ],
        "fr": [
            "Content que tu aies parlé de weather snow - continue, j'écoute.",
            "N'hésite pas à m'en dire plus sur weather snow quand tu veux.",
        ],
    },
    "WEATHER_WINDY_RESPONSES": {
        "en": [
            "I like where this weather windy conversation is headed.",
            "Thanks for sharing that - weather windy is worth talking through.",
            "Feel free to tell me more about weather windy whenever you like.",
        ],
        "sw": [
            "Kuna mengi zaidi ya kusema kuhusu weather windy.",
            "Bado hatujamaliza kuzungumza kuhusu weather windy - kuna nini kingine?",
        ],
        "fr": [
            "Merci d'avoir partagé ça - weather windy mérite qu'on en parle.",
            "J'aime la direction que prend cette discussion sur weather windy.",
        ],
    },
    "HOLIDAY_SMALLTALK_RESPONSES": {
        "en": [
            "That's interesting, tell me a bit more about holiday smalltalk.",
            "There's always more to say about holiday smalltalk.",
            "Noted - I'll keep that in mind as we talk about holiday smalltalk.",
        ],
        "sw": [
            "Hilo ni jambo zuri kuhusu holiday smalltalk.",
            "Napenda mwelekeo wa mazungumzo haya kuhusu holiday smalltalk.",
        ],
        "fr": [
            "J'aime la direction que prend cette discussion sur holiday smalltalk.",
            "Il y a toujours plus à dire sur holiday smalltalk.",
        ],
    },
    "LEARNING_RESPONSES": {
        "en": [
            "Feel free to tell me more about learning whenever you like.",
            "There's always more to say about learning.",
            "That's a good angle on learning, honestly.",
        ],
        "sw": [
            "Jisikie huru kunieleza zaidi kuhusu learning wakati wowote.",
            "Nafurahi umetaja learning - endelea, nasikiliza.",
        ],
        "fr": [
            "Content que tu aies parlé de learning - continue, j'écoute.",
            "C'est un bon point de vue sur learning.",
        ],
    },
    "MOTIVATION_GOALS_RESPONSES": {
        "en": [
            "Noted - I'll keep that in mind as we talk about motivation goals.",
            "I like where this motivation goals conversation is headed.",
            "I don't think we've fully covered motivation goals yet - what else is on your mind?",
        ],
        "sw": [
            "Napenda mwelekeo wa mazungumzo haya kuhusu motivation goals.",
            "Jisikie huru kunieleza zaidi kuhusu motivation goals wakati wowote.",
        ],
        "fr": [
            "Il y a toujours plus à dire sur motivation goals.",
            "Merci d'avoir partagé ça - motivation goals mérite qu'on en parle.",
        ],
    },
    "NOSTALGIA_RESPONSES": {
        "en": [
            "I like where this nostalgia conversation is headed.",
            "There's always more to say about nostalgia.",
            "Noted - I'll keep that in mind as we talk about nostalgia.",
        ],
        "sw": [
            "Nafurahi umetaja nostalgia - endelea, nasikiliza.",
            "Asante kwa kushiriki - nostalgia inafaa kuzungumziwa.",
        ],
        "fr": [
            "J'aime la direction que prend cette discussion sur nostalgia.",
            "Merci d'avoir partagé ça - nostalgia mérite qu'on en parle.",
        ],
    },
    "FUTURE_PLANS_RESPONSES": {
        "en": [
            "That's a good angle on future plans, honestly.",
            "Feel free to tell me more about future plans whenever you like.",
            "That's interesting, tell me a bit more about future plans.",
        ],
        "sw": [
            "Napenda mwelekeo wa mazungumzo haya kuhusu future plans.",
            "Asante kwa kushiriki - future plans inafaa kuzungumziwa.",
        ],
        "fr": [
            "Merci d'avoir partagé ça - future plans mérite qu'on en parle.",
            "Content que tu aies parlé de future plans - continue, j'écoute.",
        ],
    },
    "GAMING_RESPONSES": {
        "en": [
            "I don't think we've fully covered gaming yet - what else is on your mind?",
            "There's always more to say about gaming.",
            "I could keep chatting about gaming for a while.",
        ],
        "sw": [
            "Napenda mwelekeo wa mazungumzo haya kuhusu gaming.",
            "Bado hatujamaliza kuzungumza kuhusu gaming - kuna nini kingine?",
        ],
        "fr": [
            "On n'a pas encore tout dit sur gaming - quoi d'autre ?",
            "Content que tu aies parlé de gaming - continue, j'écoute.",
        ],
    },
    "COOKING_RESPONSES": {
        "en": [
            "Glad you brought cooking up - keep going, I'm listening.",
            "I like where this cooking conversation is headed.",
            "That's interesting, tell me a bit more about cooking.",
        ],
        "sw": [
            "Asante kwa kushiriki - cooking inafaa kuzungumziwa.",
            "Napenda mwelekeo wa mazungumzo haya kuhusu cooking.",
        ],
        "fr": [
            "Je pourrais continuer à parler de cooking un moment.",
            "J'aime la direction que prend cette discussion sur cooking.",
        ],
    },
    "NATURE_OUTDOORS_RESPONSES": {
        "en": [
            "I don't think we've fully covered nature outdoors yet - what else is on your mind?",
            "There's always more to say about nature outdoors.",
            "Noted - I'll keep that in mind as we talk about nature outdoors.",
        ],
        "sw": [
            "Nafurahi umetaja nature outdoors - endelea, nasikiliza.",
            "Napenda mwelekeo wa mazungumzo haya kuhusu nature outdoors.",
        ],
        "fr": [
            "On n'a pas encore tout dit sur nature outdoors - quoi d'autre ?",
            "Je pourrais continuer à parler de nature outdoors un moment.",
        ],
    },
    "SLEEP_DREAMS_RESPONSES": {
        "en": [
            "Feel free to tell me more about sleep dreams whenever you like.",
            "Noted - I'll keep that in mind as we talk about sleep dreams.",
            "Glad you brought sleep dreams up - keep going, I'm listening.",
        ],
        "sw": [
            "Ningeweza kuendelea kuzungumza kuhusu sleep dreams kwa muda.",
            "Kuna mengi zaidi ya kusema kuhusu sleep dreams.",
        ],
        "fr": [
            "On n'a pas encore tout dit sur sleep dreams - quoi d'autre ?",
            "Content que tu aies parlé de sleep dreams - continue, j'écoute.",
        ],
    },
    "HUMOR_APPRECIATION_RESPONSES": {
        "en": [
            "Feel free to tell me more about humor appreciation whenever you like.",
            "I don't think we've fully covered humor appreciation yet - what else is on your mind?",
            "That's interesting, tell me a bit more about humor appreciation.",
        ],
        "sw": [
            "Hilo ni jambo zuri kuhusu humor appreciation.",
            "Jisikie huru kunieleza zaidi kuhusu humor appreciation wakati wowote.",
        ],
        "fr": [
            "C'est un bon point de vue sur humor appreciation.",
            "N'hésite pas à m'en dire plus sur humor appreciation quand tu veux.",
        ],
    },
    "SKEPTICISM_RESPONSES": {
        "en": [
            "There's always more to say about skepticism.",
            "Feel free to tell me more about skepticism whenever you like.",
            "I could keep chatting about skepticism for a while.",
        ],
        "sw": [
            "Nafurahi umetaja skepticism - endelea, nasikiliza.",
            "Kuna mengi zaidi ya kusema kuhusu skepticism.",
        ],
        "fr": [
            "Content que tu aies parlé de skepticism - continue, j'écoute.",
            "Je pourrais continuer à parler de skepticism un moment.",
        ],
    },
    "FILLER_ACKNOWLEDGEMENT_RESPONSES": {
        "en": [
            "Glad you brought filler acknowledgement up - keep going, I'm listening.",
            "I could keep chatting about filler acknowledgement for a while.",
            "I don't think we've fully covered filler acknowledgement yet - what else is on your mind?",
        ],
        "sw": [
            "Nafurahi umetaja filler acknowledgement - endelea, nasikiliza.",
            "Jisikie huru kunieleza zaidi kuhusu filler acknowledgement wakati wowote.",
        ],
        "fr": [
            "N'hésite pas à m'en dire plus sur filler acknowledgement quand tu veux.",
            "Je pourrais continuer à parler de filler acknowledgement un moment.",
        ],
    },
    "OPINION_REQUEST_RESPONSES": {
        "en": [
            "I could keep chatting about opinion request for a while.",
            "That's a good angle on opinion request, honestly.",
            "I like where this opinion request conversation is headed.",
        ],
        "sw": [
            "Nafurahi umetaja opinion request - endelea, nasikiliza.",
            "Ningeweza kuendelea kuzungumza kuhusu opinion request kwa muda.",
        ],
        "fr": [
            "Il y a toujours plus à dire sur opinion request.",
            "C'est un bon point de vue sur opinion request.",
        ],
    },
    "ADVICE_REQUEST_RESPONSES": {
        "en": [
            "I don't think we've fully covered advice request yet - what else is on your mind?",
            "Thanks for sharing that - advice request is worth talking through.",
            "That's a good angle on advice request, honestly.",
        ],
        "sw": [
            "Hilo ni jambo zuri kuhusu advice request.",
            "Ningeweza kuendelea kuzungumza kuhusu advice request kwa muda.",
        ],
        "fr": [
            "Merci d'avoir partagé ça - advice request mérite qu'on en parle.",
            "Content que tu aies parlé de advice request - continue, j'écoute.",
        ],
    },
    "COMPARISON_RESPONSES": {
        "en": [
            "I like where this comparison conversation is headed.",
            "That's a good angle on comparison, honestly.",
            "Noted - I'll keep that in mind as we talk about comparison.",
        ],
        "sw": [
            "Bado hatujamaliza kuzungumza kuhusu comparison - kuna nini kingine?",
            "Jisikie huru kunieleza zaidi kuhusu comparison wakati wowote.",
        ],
        "fr": [
            "C'est un bon point de vue sur comparison.",
            "Merci d'avoir partagé ça - comparison mérite qu'on en parle.",
        ],
    },
    "FEELINGS_ANGRY_RESPONSES": {
        "en": [
            "Feel free to tell me more about feelings angry whenever you like.",
            "I like where this feelings angry conversation is headed.",
            "There's always more to say about feelings angry.",
        ],
        "sw": [
            "Napenda mwelekeo wa mazungumzo haya kuhusu feelings angry.",
            "Nafurahi umetaja feelings angry - endelea, nasikiliza.",
        ],
        "fr": [
            "Je pourrais continuer à parler de feelings angry un moment.",
            "N'hésite pas à m'en dire plus sur feelings angry quand tu veux.",
        ],
    },
    "FEELINGS_NERVOUS_RESPONSES": {
        "en": [
            "Noted - I'll keep that in mind as we talk about feelings nervous.",
            "Feel free to tell me more about feelings nervous whenever you like.",
            "I don't think we've fully covered feelings nervous yet - what else is on your mind?",
        ],
        "sw": [
            "Kuna mengi zaidi ya kusema kuhusu feelings nervous.",
            "Nafurahi umetaja feelings nervous - endelea, nasikiliza.",
        ],
        "fr": [
            "Content que tu aies parlé de feelings nervous - continue, j'écoute.",
            "J'aime la direction que prend cette discussion sur feelings nervous.",
        ],
    },
    "ANXIETY_RESPONSES": {
        "en": [
            "I like where this anxiety conversation is headed.",
            "I don't think we've fully covered anxiety yet - what else is on your mind?",
            "There's always more to say about anxiety.",
        ],
        "sw": [
            "Ningeweza kuendelea kuzungumza kuhusu anxiety kwa muda.",
            "Nafurahi umetaja anxiety - endelea, nasikiliza.",
        ],
        "fr": [
            "N'hésite pas à m'en dire plus sur anxiety quand tu veux.",
            "C'est un bon point de vue sur anxiety.",
        ],
    },
    "FEELINGS_LONELY_RESPONSES": {
        "en": [
            "That's interesting, tell me a bit more about feelings lonely.",
            "Noted - I'll keep that in mind as we talk about feelings lonely.",
            "There's always more to say about feelings lonely.",
        ],
        "sw": [
            "Ningeweza kuendelea kuzungumza kuhusu feelings lonely kwa muda.",
            "Napenda mwelekeo wa mazungumzo haya kuhusu feelings lonely.",
        ],
        "fr": [
            "C'est un bon point de vue sur feelings lonely.",
            "Content que tu aies parlé de feelings lonely - continue, j'écoute.",
        ],
    },
    "FEELINGS_PROUD_RESPONSES": {
        "en": [
            "I don't think we've fully covered feelings proud yet - what else is on your mind?",
            "I could keep chatting about feelings proud for a while.",
            "That's interesting, tell me a bit more about feelings proud.",
        ],
        "sw": [
            "Hilo ni jambo zuri kuhusu feelings proud.",
            "Nafurahi umetaja feelings proud - endelea, nasikiliza.",
        ],
        "fr": [
            "Je pourrais continuer à parler de feelings proud un moment.",
            "On n'a pas encore tout dit sur feelings proud - quoi d'autre ?",
        ],
    },
    "FEELINGS_JEALOUS_RESPONSES": {
        "en": [
            "Feel free to tell me more about feelings jealous whenever you like.",
            "That's interesting, tell me a bit more about feelings jealous.",
            "There's always more to say about feelings jealous.",
        ],
        "sw": [
            "Napenda mwelekeo wa mazungumzo haya kuhusu feelings jealous.",
            "Asante kwa kushiriki - feelings jealous inafaa kuzungumziwa.",
        ],
        "fr": [
            "J'aime la direction que prend cette discussion sur feelings jealous.",
            "N'hésite pas à m'en dire plus sur feelings jealous quand tu veux.",
        ],
    },
    "FEELINGS_RELIEVED_RESPONSES": {
        "en": [
            "I could keep chatting about feelings relieved for a while.",
            "Feel free to tell me more about feelings relieved whenever you like.",
            "That's interesting, tell me a bit more about feelings relieved.",
        ],
        "sw": [
            "Napenda mwelekeo wa mazungumzo haya kuhusu feelings relieved.",
            "Asante kwa kushiriki - feelings relieved inafaa kuzungumziwa.",
        ],
        "fr": [
            "Content que tu aies parlé de feelings relieved - continue, j'écoute.",
            "Il y a toujours plus à dire sur feelings relieved.",
        ],
    },
    "BOT_CAPABILITY_CURIOSITY_RESPONSES": {
        "en": [
            "I could keep chatting about bot capability curiosity for a while.",
            "That's interesting, tell me a bit more about bot capability curiosity.",
            "Glad you brought bot capability curiosity up - keep going, I'm listening.",
        ],
        "sw": [
            "Napenda mwelekeo wa mazungumzo haya kuhusu bot capability curiosity.",
            "Hilo ni jambo zuri kuhusu bot capability curiosity.",
        ],
        "fr": [
            "On n'a pas encore tout dit sur bot capability curiosity - quoi d'autre ?",
            "Content que tu aies parlé de bot capability curiosity - continue, j'écoute.",
        ],
    },
    "SMALL_TALK_WEATHER_CHECK_RESPONSES": {
        "en": [
            "I like where this small talk weather check conversation is headed.",
            "That's a good angle on small talk weather check, honestly.",
            "I could keep chatting about small talk weather check for a while.",
        ],
        "sw": [
            "Jisikie huru kunieleza zaidi kuhusu small talk weather check wakati wowote.",
            "Hilo ni jambo zuri kuhusu small talk weather check.",
        ],
        "fr": [
            "Merci d'avoir partagé ça - small talk weather check mérite qu'on en parle.",
            "C'est un bon point de vue sur small talk weather check.",
        ],
    },
    "INTRODUCTION_REQUEST_RESPONSES": {
        "en": [
            "That's a good angle on introduction request, honestly.",
            "Noted - I'll keep that in mind as we talk about introduction request.",
            "Thanks for sharing that - introduction request is worth talking through.",
        ],
        "sw": [
            "Nafurahi umetaja introduction request - endelea, nasikiliza.",
            "Jisikie huru kunieleza zaidi kuhusu introduction request wakati wowote.",
        ],
        "fr": [
            "Il y a toujours plus à dire sur introduction request.",
            "Content que tu aies parlé de introduction request - continue, j'écoute.",
        ],
    },
    "SMALL_TALK_BUSY_RESPONSES": {
        "en": [
            "Noted - I'll keep that in mind as we talk about small talk busy.",
            "Feel free to tell me more about small talk busy whenever you like.",
            "There's always more to say about small talk busy.",
        ],
        "sw": [
            "Hilo ni jambo zuri kuhusu small talk busy.",
            "Jisikie huru kunieleza zaidi kuhusu small talk busy wakati wowote.",
        ],
        "fr": [
            "J'aime la direction que prend cette discussion sur small talk busy.",
            "Il y a toujours plus à dire sur small talk busy.",
        ],
    },
    "POLITENESS_PLEASE_RESPONSES": {
        "en": [
            "That's a good angle on politeness please, honestly.",
            "Glad you brought politeness please up - keep going, I'm listening.",
            "I don't think we've fully covered politeness please yet - what else is on your mind?",
        ],
        "sw": [
            "Bado hatujamaliza kuzungumza kuhusu politeness please - kuna nini kingine?",
            "Kuna mengi zaidi ya kusema kuhusu politeness please.",
        ],
        "fr": [
            "Merci d'avoir partagé ça - politeness please mérite qu'on en parle.",
            "J'aime la direction que prend cette discussion sur politeness please.",
        ],
    },
    "EXERCISE_FITNESS_RESPONSES": {
        "en": [
            "There's always more to say about exercise fitness.",
            "Thanks for sharing that - exercise fitness is worth talking through.",
            "I could keep chatting about exercise fitness for a while.",
        ],
        "sw": [
            "Hilo ni jambo zuri kuhusu exercise fitness.",
            "Jisikie huru kunieleza zaidi kuhusu exercise fitness wakati wowote.",
        ],
        "fr": [
            "Je pourrais continuer à parler de exercise fitness un moment.",
            "C'est un bon point de vue sur exercise fitness.",
        ],
    },
    "MENTAL_HEALTH_CHECKIN_RESPONSES": {
        "en": [
            "I could keep chatting about mental health checkin for a while.",
            "That's a good angle on mental health checkin, honestly.",
            "Glad you brought mental health checkin up - keep going, I'm listening.",
        ],
        "sw": [
            "Bado hatujamaliza kuzungumza kuhusu mental health checkin - kuna nini kingine?",
            "Ningeweza kuendelea kuzungumza kuhusu mental health checkin kwa muda.",
        ],
        "fr": [
            "Il y a toujours plus à dire sur mental health checkin.",
            "Je pourrais continuer à parler de mental health checkin un moment.",
        ],
    },
    "GRATITUDE_FOR_BOT_RESPONSES": {
        "en": [
            "I could keep chatting about gratitude for bot for a while.",
            "That's a good angle on gratitude for bot, honestly.",
            "Glad you brought gratitude for bot up - keep going, I'm listening.",
        ],
        "sw": [
            "Asante kwa kushiriki - gratitude for bot inafaa kuzungumziwa.",
            "Bado hatujamaliza kuzungumza kuhusu gratitude for bot - kuna nini kingine?",
        ],
        "fr": [
            "C'est un bon point de vue sur gratitude for bot.",
            "Je pourrais continuer à parler de gratitude for bot un moment.",
        ],
    },
    "REPEAT_CLARIFY_RESPONSES": {
        "en": [
            "There's always more to say about repeat clarify.",
            "Thanks for sharing that - repeat clarify is worth talking through.",
            "Glad you brought repeat clarify up - keep going, I'm listening.",
        ],
        "sw": [
            "Asante kwa kushiriki - repeat clarify inafaa kuzungumziwa.",
            "Jisikie huru kunieleza zaidi kuhusu repeat clarify wakati wowote.",
        ],
        "fr": [
            "N'hésite pas à m'en dire plus sur repeat clarify quand tu veux.",
            "Je pourrais continuer à parler de repeat clarify un moment.",
        ],
    },
    "SMALL_CELEBRATION_RESPONSES": {
        "en": [
            "Thanks for sharing that - small celebration is worth talking through.",
            "Noted - I'll keep that in mind as we talk about small celebration.",
            "I could keep chatting about small celebration for a while.",
        ],
        "sw": [
            "Asante kwa kushiriki - small celebration inafaa kuzungumziwa.",
            "Kuna mengi zaidi ya kusema kuhusu small celebration.",
        ],
        "fr": [
            "Merci d'avoir partagé ça - small celebration mérite qu'on en parle.",
            "C'est un bon point de vue sur small celebration.",
        ],
    },
    "FORECAST_QUESTION_RESPONSES": {
        "en": [
            "I like where this forecast question conversation is headed.",
            "That's a good angle on forecast question, honestly.",
            "That's interesting, tell me a bit more about forecast question.",
        ],
        "sw": [
            "Asante kwa kushiriki - forecast question inafaa kuzungumziwa.",
            "Jisikie huru kunieleza zaidi kuhusu forecast question wakati wowote.",
        ],
        "fr": [
            "C'est un bon point de vue sur forecast question.",
            "Content que tu aies parlé de forecast question - continue, j'écoute.",
        ],
    },
    "LANGUAGE_PRACTICE_RESPONSES": {
        "en": [
            "Thanks for sharing that - language practice is worth talking through.",
            "There's always more to say about language practice.",
            "I like where this language practice conversation is headed.",
        ],
        "sw": [
            "Hilo ni jambo zuri kuhusu language practice.",
            "Nafurahi umetaja language practice - endelea, nasikiliza.",
        ],
        "fr": [
            "N'hésite pas à m'en dire plus sur language practice quand tu veux.",
            "Content que tu aies parlé de language practice - continue, j'écoute.",
        ],
    },
    "BOT_AGE_LOCATION_RESPONSES": {
        "en": [
            "Noted - I'll keep that in mind as we talk about bot age location.",
            "There's always more to say about bot age location.",
            "Glad you brought bot age location up - keep going, I'm listening.",
        ],
        "sw": [
            "Nafurahi umetaja bot age location - endelea, nasikiliza.",
            "Kuna mengi zaidi ya kusema kuhusu bot age location.",
        ],
        "fr": [
            "Je pourrais continuer à parler de bot age location un moment.",
            "N'hésite pas à m'en dire plus sur bot age location quand tu veux.",
        ],
    },
    "BOT_NAME_OPINION_RESPONSES": {
        "en": [
            "Glad you brought bot name opinion up - keep going, I'm listening.",
            "That's a good angle on bot name opinion, honestly.",
            "There's always more to say about bot name opinion.",
        ],
        "sw": [
            "Ningeweza kuendelea kuzungumza kuhusu bot name opinion kwa muda.",
            "Hilo ni jambo zuri kuhusu bot name opinion.",
        ],
        "fr": [
            "N'hésite pas à m'en dire plus sur bot name opinion quand tu veux.",
            "J'aime la direction que prend cette discussion sur bot name opinion.",
        ],
    },
    "SLOW_DOWN_RESPONSES": {
        "en": [
            "Thanks for sharing that - slow down is worth talking through.",
            "I could keep chatting about slow down for a while.",
            "I don't think we've fully covered slow down yet - what else is on your mind?",
        ],
        "sw": [
            "Hilo ni jambo zuri kuhusu slow down.",
            "Ningeweza kuendelea kuzungumza kuhusu slow down kwa muda.",
        ],
        "fr": [
            "Je pourrais continuer à parler de slow down un moment.",
            "C'est un bon point de vue sur slow down.",
        ],
    },
    "AWKWARD_PAUSE_RESPONSES": {
        "en": [
            "That's interesting, tell me a bit more about awkward pause.",
            "I don't think we've fully covered awkward pause yet - what else is on your mind?",
            "I could keep chatting about awkward pause for a while.",
        ],
        "sw": [
            "Asante kwa kushiriki - awkward pause inafaa kuzungumziwa.",
            "Bado hatujamaliza kuzungumza kuhusu awkward pause - kuna nini kingine?",
        ],
        "fr": [
            "N'hésite pas à m'en dire plus sur awkward pause quand tu veux.",
            "Content que tu aies parlé de awkward pause - continue, j'écoute.",
        ],
    },
    "COMPLIMENT_RESPONSE_RESPONSES": {
        "en": [
            "I could keep chatting about compliment response for a while.",
            "That's interesting, tell me a bit more about compliment response.",
            "That's a good angle on compliment response, honestly.",
        ],
        "sw": [
            "Asante kwa kushiriki - compliment response inafaa kuzungumziwa.",
            "Kuna mengi zaidi ya kusema kuhusu compliment response.",
        ],
        "fr": [
            "J'aime la direction que prend cette discussion sur compliment response.",
            "C'est un bon point de vue sur compliment response.",
        ],
    },
    "REMEMBER_SPECIFIC_RESPONSES": {
        "en": [
            "Thanks for sharing that - remember specific is worth talking through.",
            "I don't think we've fully covered remember specific yet - what else is on your mind?",
            "I could keep chatting about remember specific for a while.",
        ],
        "sw": [
            "Jisikie huru kunieleza zaidi kuhusu remember specific wakati wowote.",
            "Asante kwa kushiriki - remember specific inafaa kuzungumziwa.",
        ],
        "fr": [
            "Je pourrais continuer à parler de remember specific un moment.",
            "N'hésite pas à m'en dire plus sur remember specific quand tu veux.",
        ],
    },
    "TODAY_PLANS_RESPONSES": {
        "en": [
            "Glad you brought today plans up - keep going, I'm listening.",
            "Thanks for sharing that - today plans is worth talking through.",
            "That's interesting, tell me a bit more about today plans.",
        ],
        "sw": [
            "Bado hatujamaliza kuzungumza kuhusu today plans - kuna nini kingine?",
            "Hilo ni jambo zuri kuhusu today plans.",
        ],
        "fr": [
            "On n'a pas encore tout dit sur today plans - quoi d'autre ?",
            "Merci d'avoir partagé ça - today plans mérite qu'on en parle.",
        ],
    },
    "TECHNOLOGY_COMPLAINT_RESPONSES": {
        "en": [
            "I could keep chatting about technology complaint for a while.",
            "Glad you brought technology complaint up - keep going, I'm listening.",
            "Thanks for sharing that - technology complaint is worth talking through.",
        ],
        "sw": [
            "Nafurahi umetaja technology complaint - endelea, nasikiliza.",
            "Bado hatujamaliza kuzungumza kuhusu technology complaint - kuna nini kingine?",
        ],
        "fr": [
            "J'aime la direction que prend cette discussion sur technology complaint.",
            "C'est un bon point de vue sur technology complaint.",
        ],
    },
    "ASPIRATIONS_DREAMS_RESPONSES": {
        "en": [
            "Feel free to tell me more about aspirations dreams whenever you like.",
            "That's a good angle on aspirations dreams, honestly.",
            "Thanks for sharing that - aspirations dreams is worth talking through.",
        ],
        "sw": [
            "Jisikie huru kunieleza zaidi kuhusu aspirations dreams wakati wowote.",
            "Nafurahi umetaja aspirations dreams - endelea, nasikiliza.",
        ],
        "fr": [
            "Je pourrais continuer à parler de aspirations dreams un moment.",
            "Content que tu aies parlé de aspirations dreams - continue, j'écoute.",
        ],
    },
    "MISSING_SOMEONE_RESPONSES": {
        "en": [
            "I could keep chatting about missing someone for a while.",
            "I like where this missing someone conversation is headed.",
            "There's always more to say about missing someone.",
        ],
        "sw": [
            "Asante kwa kushiriki - missing someone inafaa kuzungumziwa.",
            "Bado hatujamaliza kuzungumza kuhusu missing someone - kuna nini kingine?",
        ],
        "fr": [
            "On n'a pas encore tout dit sur missing someone - quoi d'autre ?",
            "Content que tu aies parlé de missing someone - continue, j'écoute.",
        ],
    },
    "EXCITEMENT_EVENT_RESPONSES": {
        "en": [
            "That's a good angle on excitement event, honestly.",
            "There's always more to say about excitement event.",
            "I don't think we've fully covered excitement event yet - what else is on your mind?",
        ],
        "sw": [
            "Bado hatujamaliza kuzungumza kuhusu excitement event - kuna nini kingine?",
            "Kuna mengi zaidi ya kusema kuhusu excitement event.",
        ],
        "fr": [
            "C'est un bon point de vue sur excitement event.",
            "Je pourrais continuer à parler de excitement event un moment.",
        ],
    },
    "DISAPPOINTMENT_RESPONSES": {
        "en": [
            "I don't think we've fully covered disappointment yet - what else is on your mind?",
            "Glad you brought disappointment up - keep going, I'm listening.",
            "That's a good angle on disappointment, honestly.",
        ],
        "sw": [
            "Nafurahi umetaja disappointment - endelea, nasikiliza.",
            "Hilo ni jambo zuri kuhusu disappointment.",
        ],
        "fr": [
            "Il y a toujours plus à dire sur disappointment.",
            "J'aime la direction que prend cette discussion sur disappointment.",
        ],
    },
    "CHAT_META_RESPONSES": {
        "en": [
            "That's a good angle on chat meta, honestly.",
            "Thanks for sharing that - chat meta is worth talking through.",
            "I like where this chat meta conversation is headed.",
        ],
        "sw": [
            "Jisikie huru kunieleza zaidi kuhusu chat meta wakati wowote.",
            "Kuna mengi zaidi ya kusema kuhusu chat meta.",
        ],
        "fr": [
            "Il y a toujours plus à dire sur chat meta.",
            "Je pourrais continuer à parler de chat meta un moment.",
        ],
    },
    "SEASON_SPRING_RESPONSES": {
        "en": [
            "Glad you brought season spring up - keep going, I'm listening.",
            "I like where this season spring conversation is headed.",
            "There's always more to say about season spring.",
        ],
        "sw": [
            "Bado hatujamaliza kuzungumza kuhusu season spring - kuna nini kingine?",
            "Nafurahi umetaja season spring - endelea, nasikiliza.",
        ],
        "fr": [
            "Je pourrais continuer à parler de season spring un moment.",
            "C'est un bon point de vue sur season spring.",
        ],
    },
    "SEASON_SUMMER_RESPONSES": {
        "en": [
            "That's a good angle on season summer, honestly.",
            "There's always more to say about season summer.",
            "That's interesting, tell me a bit more about season summer.",
        ],
        "sw": [
            "Kuna mengi zaidi ya kusema kuhusu season summer.",
            "Jisikie huru kunieleza zaidi kuhusu season summer wakati wowote.",
        ],
        "fr": [
            "J'aime la direction que prend cette discussion sur season summer.",
            "Je pourrais continuer à parler de season summer un moment.",
        ],
    },
    "SEASON_AUTUMN_RESPONSES": {
        "en": [
            "That's interesting, tell me a bit more about season autumn.",
            "There's always more to say about season autumn.",
            "I don't think we've fully covered season autumn yet - what else is on your mind?",
        ],
        "sw": [
            "Jisikie huru kunieleza zaidi kuhusu season autumn wakati wowote.",
            "Napenda mwelekeo wa mazungumzo haya kuhusu season autumn.",
        ],
        "fr": [
            "Je pourrais continuer à parler de season autumn un moment.",
            "N'hésite pas à m'en dire plus sur season autumn quand tu veux.",
        ],
    },
    "SEASON_WINTER_RESPONSES": {
        "en": [
            "Feel free to tell me more about season winter whenever you like.",
            "There's always more to say about season winter.",
            "That's interesting, tell me a bit more about season winter.",
        ],
        "sw": [
            "Bado hatujamaliza kuzungumza kuhusu season winter - kuna nini kingine?",
            "Ningeweza kuendelea kuzungumza kuhusu season winter kwa muda.",
        ],
        "fr": [
            "Je pourrais continuer à parler de season winter un moment.",
            "Merci d'avoir partagé ça - season winter mérite qu'on en parle.",
        ],
    },
    "NIGHTMARE_RESPONSES": {
        "en": [
            "Thanks for sharing that - nightmare is worth talking through.",
            "There's always more to say about nightmare.",
            "I could keep chatting about nightmare for a while.",
        ],
        "sw": [
            "Jisikie huru kunieleza zaidi kuhusu nightmare wakati wowote.",
            "Asante kwa kushiriki - nightmare inafaa kuzungumziwa.",
        ],
        "fr": [
            "Merci d'avoir partagé ça - nightmare mérite qu'on en parle.",
            "N'hésite pas à m'en dire plus sur nightmare quand tu veux.",
        ],
    },
    "TRAFFIC_RESPONSES": {
        "en": [
            "Glad you brought traffic up - keep going, I'm listening.",
            "I could keep chatting about traffic for a while.",
            "That's interesting, tell me a bit more about traffic.",
        ],
        "sw": [
            "Napenda mwelekeo wa mazungumzo haya kuhusu traffic.",
            "Asante kwa kushiriki - traffic inafaa kuzungumziwa.",
        ],
        "fr": [
            "Merci d'avoir partagé ça - traffic mérite qu'on en parle.",
            "C'est un bon point de vue sur traffic.",
        ],
    },
    "NEWS_RESPONSES": {
        "en": [
            "I could keep chatting about news for a while.",
            "I like where this news conversation is headed.",
            "Feel free to tell me more about news whenever you like.",
        ],
        "sw": [
            "Hilo ni jambo zuri kuhusu news.",
            "Ningeweza kuendelea kuzungumza kuhusu news kwa muda.",
        ],
        "fr": [
            "Il y a toujours plus à dire sur news.",
            "Content que tu aies parlé de news - continue, j'écoute.",
        ],
    },
    "COLOR_PREFERENCE_RESPONSES": {
        "en": [
            "Thanks for sharing that - color preference is worth talking through.",
            "That's a good angle on color preference, honestly.",
            "That's interesting, tell me a bit more about color preference.",
        ],
        "sw": [
            "Ningeweza kuendelea kuzungumza kuhusu color preference kwa muda.",
            "Nafurahi umetaja color preference - endelea, nasikiliza.",
        ],
        "fr": [
            "On n'a pas encore tout dit sur color preference - quoi d'autre ?",
            "C'est un bon point de vue sur color preference.",
        ],
    },
    "STUDYING_EXAM_RESPONSES": {
        "en": [
            "Feel free to tell me more about studying exam whenever you like.",
            "Glad you brought studying exam up - keep going, I'm listening.",
            "Thanks for sharing that - studying exam is worth talking through.",
        ],
        "sw": [
            "Hilo ni jambo zuri kuhusu studying exam.",
            "Nafurahi umetaja studying exam - endelea, nasikiliza.",
        ],
        "fr": [
            "J'aime la direction que prend cette discussion sur studying exam.",
            "Content que tu aies parlé de studying exam - continue, j'écoute.",
        ],
    },
    "GARDENING_PLANTS_RESPONSES": {
        "en": [
            "I like where this gardening plants conversation is headed.",
            "That's interesting, tell me a bit more about gardening plants.",
            "I don't think we've fully covered gardening plants yet - what else is on your mind?",
        ],
        "sw": [
            "Hilo ni jambo zuri kuhusu gardening plants.",
            "Bado hatujamaliza kuzungumza kuhusu gardening plants - kuna nini kingine?",
        ],
        "fr": [
            "C'est un bon point de vue sur gardening plants.",
            "N'hésite pas à m'en dire plus sur gardening plants quand tu veux.",
        ],
    },
    "SHOPPING_RESPONSES": {
        "en": [
            "I could keep chatting about shopping for a while.",
            "Thanks for sharing that - shopping is worth talking through.",
            "That's a good angle on shopping, honestly.",
        ],
        "sw": [
            "Asante kwa kushiriki - shopping inafaa kuzungumziwa.",
            "Jisikie huru kunieleza zaidi kuhusu shopping wakati wowote.",
        ],
        "fr": [
            "Merci d'avoir partagé ça - shopping mérite qu'on en parle.",
            "C'est un bon point de vue sur shopping.",
        ],
    },
    "MOVIES_TV_RESPONSES": {
        "en": [
            "I don't think we've fully covered movies tv yet - what else is on your mind?",
            "There's always more to say about movies tv.",
            "I like where this movies tv conversation is headed.",
        ],
        "sw": [
            "Hilo ni jambo zuri kuhusu movies tv.",
            "Asante kwa kushiriki - movies tv inafaa kuzungumziwa.",
        ],
        "fr": [
            "C'est un bon point de vue sur movies tv.",
            "Content que tu aies parlé de movies tv - continue, j'écoute.",
        ],
    },
    "COFFEE_TEA_RESPONSES": {
        "en": [
            "That's interesting, tell me a bit more about coffee tea.",
            "Feel free to tell me more about coffee tea whenever you like.",
            "Thanks for sharing that - coffee tea is worth talking through.",
        ],
        "sw": [
            "Jisikie huru kunieleza zaidi kuhusu coffee tea wakati wowote.",
            "Hilo ni jambo zuri kuhusu coffee tea.",
        ],
        "fr": [
            "N'hésite pas à m'en dire plus sur coffee tea quand tu veux.",
            "Content que tu aies parlé de coffee tea - continue, j'écoute.",
        ],
    },
    "EXAM_RESULTS_RESPONSES": {
        "en": [
            "Thanks for sharing that - exam results is worth talking through.",
            "I like where this exam results conversation is headed.",
            "Noted - I'll keep that in mind as we talk about exam results.",
        ],
        "sw": [
            "Napenda mwelekeo wa mazungumzo haya kuhusu exam results.",
            "Kuna mengi zaidi ya kusema kuhusu exam results.",
        ],
        "fr": [
            "Il y a toujours plus à dire sur exam results.",
            "N'hésite pas à m'en dire plus sur exam results quand tu veux.",
        ],
    },
    "PARTY_EVENT_RESPONSES": {
        "en": [
            "That's a good angle on party event, honestly.",
            "Feel free to tell me more about party event whenever you like.",
            "There's always more to say about party event.",
        ],
        "sw": [
            "Nafurahi umetaja party event - endelea, nasikiliza.",
            "Kuna mengi zaidi ya kusema kuhusu party event.",
        ],
        "fr": [
            "C'est un bon point de vue sur party event.",
            "N'hésite pas à m'en dire plus sur party event quand tu veux.",
        ],
    },
    "SIBLINGS_RESPONSES": {
        "en": [
            "Thanks for sharing that - siblings is worth talking through.",
            "I like where this siblings conversation is headed.",
            "Noted - I'll keep that in mind as we talk about siblings.",
        ],
        "sw": [
            "Kuna mengi zaidi ya kusema kuhusu siblings.",
            "Ningeweza kuendelea kuzungumza kuhusu siblings kwa muda.",
        ],
        "fr": [
            "C'est un bon point de vue sur siblings.",
            "Content que tu aies parlé de siblings - continue, j'écoute.",
        ],
    },
    "CAREER_CHANGE_RESPONSES": {
        "en": [
            "That's a good angle on career change, honestly.",
            "Feel free to tell me more about career change whenever you like.",
            "Glad you brought career change up - keep going, I'm listening.",
        ],
        "sw": [
            "Napenda mwelekeo wa mazungumzo haya kuhusu career change.",
            "Bado hatujamaliza kuzungumza kuhusu career change - kuna nini kingine?",
        ],
        "fr": [
            "Content que tu aies parlé de career change - continue, j'écoute.",
            "Merci d'avoir partagé ça - career change mérite qu'on en parle.",
        ],
    },
    "VOLUNTEER_WORK_RESPONSES": {
        "en": [
            "I don't think we've fully covered volunteer work yet - what else is on your mind?",
            "That's interesting, tell me a bit more about volunteer work.",
            "I like where this volunteer work conversation is headed.",
        ],
        "sw": [
            "Nafurahi umetaja volunteer work - endelea, nasikiliza.",
            "Jisikie huru kunieleza zaidi kuhusu volunteer work wakati wowote.",
        ],
        "fr": [
            "Merci d'avoir partagé ça - volunteer work mérite qu'on en parle.",
            "On n'a pas encore tout dit sur volunteer work - quoi d'autre ?",
        ],
    },
    "SPIRITUALITY_RESPONSES": {
        "en": [
            "I don't think we've fully covered spirituality yet - what else is on your mind?",
            "I like where this spirituality conversation is headed.",
            "Thanks for sharing that - spirituality is worth talking through.",
        ],
        "sw": [
            "Asante kwa kushiriki - spirituality inafaa kuzungumziwa.",
            "Hilo ni jambo zuri kuhusu spirituality.",
        ],
        "fr": [
            "N'hésite pas à m'en dire plus sur spirituality quand tu veux.",
            "Il y a toujours plus à dire sur spirituality.",
        ],
    },
    "POLITICS_DEFLECT_RESPONSES": {
        "en": [
            "I don't think we've fully covered politics deflect yet - what else is on your mind?",
            "I like where this politics deflect conversation is headed.",
            "Thanks for sharing that - politics deflect is worth talking through.",
        ],
        "sw": [
            "Kuna mengi zaidi ya kusema kuhusu politics deflect.",
            "Ningeweza kuendelea kuzungumza kuhusu politics deflect kwa muda.",
        ],
        "fr": [
            "Il y a toujours plus à dire sur politics deflect.",
            "C'est un bon point de vue sur politics deflect.",
        ],
    },
    "SILENCE_FILLER_RESPONSES": {
        "en": [
            "Thanks for sharing that - silence filler is worth talking through.",
            "There's always more to say about silence filler.",
            "I don't think we've fully covered silence filler yet - what else is on your mind?",
        ],
        "sw": [
            "Nafurahi umetaja silence filler - endelea, nasikiliza.",
            "Kuna mengi zaidi ya kusema kuhusu silence filler.",
        ],
        "fr": [
            "J'aime la direction que prend cette discussion sur silence filler.",
            "On n'a pas encore tout dit sur silence filler - quoi d'autre ?",
        ],
    },
    "DIRECTIONS_RECOMMENDATION_RESPONSES": {
        "en": [
            "That's a good angle on directions recommendation, honestly.",
            "There's always more to say about directions recommendation.",
            "I could keep chatting about directions recommendation for a while.",
        ],
        "sw": [
            "Hilo ni jambo zuri kuhusu directions recommendation.",
            "Ningeweza kuendelea kuzungumza kuhusu directions recommendation kwa muda.",
        ],
        "fr": [
            "Je pourrais continuer à parler de directions recommendation un moment.",
            "C'est un bon point de vue sur directions recommendation.",
        ],
    },
    "NAME_RECOGNITION_RESPONSES": {
        "en": [
            "Thanks for sharing that - name recognition is worth talking through.",
            "I like where this name recognition conversation is headed.",
            "I could keep chatting about name recognition for a while.",
        ],
        "sw": [
            "Napenda mwelekeo wa mazungumzo haya kuhusu name recognition.",
            "Asante kwa kushiriki - name recognition inafaa kuzungumziwa.",
        ],
        "fr": [
            "On n'a pas encore tout dit sur name recognition - quoi d'autre ?",
            "J'aime la direction que prend cette discussion sur name recognition.",
        ],
    },
    "GENERAL_CURIOSITY_RESPONSES": {
        "en": [
            "There's always more to say about general curiosity.",
            "That's a good angle on general curiosity, honestly.",
            "Noted - I'll keep that in mind as we talk about general curiosity.",
        ],
        "sw": [
            "Napenda mwelekeo wa mazungumzo haya kuhusu general curiosity.",
            "Jisikie huru kunieleza zaidi kuhusu general curiosity wakati wowote.",
        ],
        "fr": [
            "Il y a toujours plus à dire sur general curiosity.",
            "Merci d'avoir partagé ça - general curiosity mérite qu'on en parle.",
        ],
    },
    "LAUGHTER_RESPONSES": {
        "en": [
            "That's a good angle on laughter, honestly.",
            "Glad you brought laughter up - keep going, I'm listening.",
            "There's always more to say about laughter.",
        ],
        "sw": [
            "Nafurahi umetaja laughter - endelea, nasikiliza.",
            "Bado hatujamaliza kuzungumza kuhusu laughter - kuna nini kingine?",
        ],
        "fr": [
            "Je pourrais continuer à parler de laughter un moment.",
            "C'est un bon point de vue sur laughter.",
        ],
    },
    "CRYING_RESPONSES": {
        "en": [
            "That's interesting, tell me a bit more about crying.",
            "Thanks for sharing that - crying is worth talking through.",
            "I like where this crying conversation is headed.",
        ],
        "sw": [
            "Bado hatujamaliza kuzungumza kuhusu crying - kuna nini kingine?",
            "Kuna mengi zaidi ya kusema kuhusu crying.",
        ],
        "fr": [
            "J'aime la direction que prend cette discussion sur crying.",
            "N'hésite pas à m'en dire plus sur crying quand tu veux.",
        ],
    },
    "MILD_FRUSTRATION_RESPONSES": {
        "en": [
            "I like where this mild frustration conversation is headed.",
            "Thanks for sharing that - mild frustration is worth talking through.",
            "There's always more to say about mild frustration.",
        ],
        "sw": [
            "Hilo ni jambo zuri kuhusu mild frustration.",
            "Nafurahi umetaja mild frustration - endelea, nasikiliza.",
        ],
        "fr": [
            "C'est un bon point de vue sur mild frustration.",
            "Merci d'avoir partagé ça - mild frustration mérite qu'on en parle.",
        ],
    },
    "BOT_FAVORITE_THINGS_RESPONSES": {
        "en": [
            "There's always more to say about bot favorite things.",
            "Noted - I'll keep that in mind as we talk about bot favorite things.",
            "That's a good angle on bot favorite things, honestly.",
        ],
        "sw": [
            "Nafurahi umetaja bot favorite things - endelea, nasikiliza.",
            "Asante kwa kushiriki - bot favorite things inafaa kuzungumziwa.",
        ],
        "fr": [
            "Content que tu aies parlé de bot favorite things - continue, j'écoute.",
            "On n'a pas encore tout dit sur bot favorite things - quoi d'autre ?",
        ],
    },
    "BIRDS_FISH_RESPONSES": {
        "en": [
            "I don't think we've fully covered birds fish yet - what else is on your mind?",
            "Glad you brought birds fish up - keep going, I'm listening.",
            "I like where this birds fish conversation is headed.",
        ],
        "sw": [
            "Napenda mwelekeo wa mazungumzo haya kuhusu birds fish.",
            "Hilo ni jambo zuri kuhusu birds fish.",
        ],
        "fr": [
            "Il y a toujours plus à dire sur birds fish.",
            "C'est un bon point de vue sur birds fish.",
        ],
    },
    "COMMUTE_TRANSPORT_RESPONSES": {
        "en": [
            "I like where this commute transport conversation is headed.",
            "I could keep chatting about commute transport for a while.",
            "That's interesting, tell me a bit more about commute transport.",
        ],
        "sw": [
            "Asante kwa kushiriki - commute transport inafaa kuzungumziwa.",
            "Hilo ni jambo zuri kuhusu commute transport.",
        ],
        "fr": [
            "Il y a toujours plus à dire sur commute transport.",
            "J'aime la direction que prend cette discussion sur commute transport.",
        ],
    },
    "ALLERGIES_RESPONSES": {
        "en": [
            "I don't think we've fully covered allergies yet - what else is on your mind?",
            "I could keep chatting about allergies for a while.",
            "Feel free to tell me more about allergies whenever you like.",
        ],
        "sw": [
            "Napenda mwelekeo wa mazungumzo haya kuhusu allergies.",
            "Bado hatujamaliza kuzungumza kuhusu allergies - kuna nini kingine?",
        ],
        "fr": [
            "Il y a toujours plus à dire sur allergies.",
            "Merci d'avoir partagé ça - allergies mérite qu'on en parle.",
        ],
    },
    "DIET_NUTRITION_RESPONSES": {
        "en": [
            "That's interesting, tell me a bit more about diet nutrition.",
            "I don't think we've fully covered diet nutrition yet - what else is on your mind?",
            "I like where this diet nutrition conversation is headed.",
        ],
        "sw": [
            "Bado hatujamaliza kuzungumza kuhusu diet nutrition - kuna nini kingine?",
            "Ningeweza kuendelea kuzungumza kuhusu diet nutrition kwa muda.",
        ],
        "fr": [
            "Content que tu aies parlé de diet nutrition - continue, j'écoute.",
            "C'est un bon point de vue sur diet nutrition.",
        ],
    },
    "SLEEP_SCHEDULE_RESPONSES": {
        "en": [
            "Noted - I'll keep that in mind as we talk about sleep schedule.",
            "Thanks for sharing that - sleep schedule is worth talking through.",
            "I like where this sleep schedule conversation is headed.",
        ],
        "sw": [
            "Nafurahi umetaja sleep schedule - endelea, nasikiliza.",
            "Napenda mwelekeo wa mazungumzo haya kuhusu sleep schedule.",
        ],
        "fr": [
            "Je pourrais continuer à parler de sleep schedule un moment.",
            "N'hésite pas à m'en dire plus sur sleep schedule quand tu veux.",
        ],
    },
    "PHOTOGRAPHY_ART_RESPONSES": {
        "en": [
            "Thanks for sharing that - photography art is worth talking through.",
            "There's always more to say about photography art.",
            "That's interesting, tell me a bit more about photography art.",
        ],
        "sw": [
            "Jisikie huru kunieleza zaidi kuhusu photography art wakati wowote.",
            "Hilo ni jambo zuri kuhusu photography art.",
        ],
        "fr": [
            "N'hésite pas à m'en dire plus sur photography art quand tu veux.",
            "Content que tu aies parlé de photography art - continue, j'écoute.",
        ],
    },
    "GRAMMAR_QUESTION_RESPONSES": {
        "en": [
            "There's always more to say about grammar question.",
            "Glad you brought grammar question up - keep going, I'm listening.",
            "Feel free to tell me more about grammar question whenever you like.",
        ],
        "sw": [
            "Ningeweza kuendelea kuzungumza kuhusu grammar question kwa muda.",
            "Jisikie huru kunieleza zaidi kuhusu grammar question wakati wowote.",
        ],
        "fr": [
            "Merci d'avoir partagé ça - grammar question mérite qu'on en parle.",
            "Content que tu aies parlé de grammar question - continue, j'écoute.",
        ],
    },
    "NAMING_THINGS_RESPONSES": {
        "en": [
            "I could keep chatting about naming things for a while.",
            "Noted - I'll keep that in mind as we talk about naming things.",
            "I don't think we've fully covered naming things yet - what else is on your mind?",
        ],
        "sw": [
            "Asante kwa kushiriki - naming things inafaa kuzungumziwa.",
            "Bado hatujamaliza kuzungumza kuhusu naming things - kuna nini kingine?",
        ],
        "fr": [
            "N'hésite pas à m'en dire plus sur naming things quand tu veux.",
            "Content que tu aies parlé de naming things - continue, j'écoute.",
        ],
    },
    "WEATHER_EXTREME_RESPONSES": {
        "en": [
            "Feel free to tell me more about weather extreme whenever you like.",
            "There's always more to say about weather extreme.",
            "I could keep chatting about weather extreme for a while.",
        ],
        "sw": [
            "Bado hatujamaliza kuzungumza kuhusu weather extreme - kuna nini kingine?",
            "Jisikie huru kunieleza zaidi kuhusu weather extreme wakati wowote.",
        ],
        "fr": [
            "Merci d'avoir partagé ça - weather extreme mérite qu'on en parle.",
            "C'est un bon point de vue sur weather extreme.",
        ],
    },
    "HOME_HOUSE_RESPONSES": {
        "en": [
            "I don't think we've fully covered home house yet - what else is on your mind?",
            "That's a good angle on home house, honestly.",
            "Feel free to tell me more about home house whenever you like.",
        ],
        "sw": [
            "Asante kwa kushiriki - home house inafaa kuzungumziwa.",
            "Jisikie huru kunieleza zaidi kuhusu home house wakati wowote.",
        ],
        "fr": [
            "Merci d'avoir partagé ça - home house mérite qu'on en parle.",
            "Je pourrais continuer à parler de home house un moment.",
        ],
    },
    "NEIGHBORS_RESPONSES": {
        "en": [
            "I don't think we've fully covered neighbors yet - what else is on your mind?",
            "That's a good angle on neighbors, honestly.",
            "I like where this neighbors conversation is headed.",
        ],
        "sw": [
            "Nafurahi umetaja neighbors - endelea, nasikiliza.",
            "Asante kwa kushiriki - neighbors inafaa kuzungumziwa.",
        ],
        "fr": [
            "Merci d'avoir partagé ça - neighbors mérite qu'on en parle.",
            "N'hésite pas à m'en dire plus sur neighbors quand tu veux.",
        ],
    },
    "PET_LOSS_RESPONSES": {
        "en": [
            "Thanks for sharing that - pet loss is worth talking through.",
            "There's always more to say about pet loss.",
            "I don't think we've fully covered pet loss yet - what else is on your mind?",
        ],
        "sw": [
            "Hilo ni jambo zuri kuhusu pet loss.",
            "Jisikie huru kunieleza zaidi kuhusu pet loss wakati wowote.",
        ],
        "fr": [
            "Content que tu aies parlé de pet loss - continue, j'écoute.",
            "Merci d'avoir partagé ça - pet loss mérite qu'on en parle.",
        ],
    },
    "ACHIEVEMENT_MILESTONE_RESPONSES": {
        "en": [
            "Noted - I'll keep that in mind as we talk about achievement milestone.",
            "I don't think we've fully covered achievement milestone yet - what else is on your mind?",
            "I could keep chatting about achievement milestone for a while.",
        ],
        "sw": [
            "Kuna mengi zaidi ya kusema kuhusu achievement milestone.",
            "Asante kwa kushiriki - achievement milestone inafaa kuzungumziwa.",
        ],
        "fr": [
            "Il y a toujours plus à dire sur achievement milestone.",
            "C'est un bon point de vue sur achievement milestone.",
        ],
    },
    "WAITING_PATIENCE_RESPONSES": {
        "en": [
            "There's always more to say about waiting patience.",
            "Glad you brought waiting patience up - keep going, I'm listening.",
            "Thanks for sharing that - waiting patience is worth talking through.",
        ],
        "sw": [
            "Napenda mwelekeo wa mazungumzo haya kuhusu waiting patience.",
            "Asante kwa kushiriki - waiting patience inafaa kuzungumziwa.",
        ],
        "fr": [
            "J'aime la direction que prend cette discussion sur waiting patience.",
            "C'est un bon point de vue sur waiting patience.",
        ],
    },
    "POSITIVE_SURPRISE_RESPONSES": {
        "en": [
            "Thanks for sharing that - positive surprise is worth talking through.",
            "That's interesting, tell me a bit more about positive surprise.",
            "That's a good angle on positive surprise, honestly.",
        ],
        "sw": [
            "Asante kwa kushiriki - positive surprise inafaa kuzungumziwa.",
            "Napenda mwelekeo wa mazungumzo haya kuhusu positive surprise.",
        ],
        "fr": [
            "Content que tu aies parlé de positive surprise - continue, j'écoute.",
            "C'est un bon point de vue sur positive surprise.",
        ],
    },
    "COMPLIMENT_BACK_REQUEST_RESPONSES": {
        "en": [
            "That's a good angle on compliment back request, honestly.",
            "Noted - I'll keep that in mind as we talk about compliment back request.",
            "Glad you brought compliment back request up - keep going, I'm listening.",
        ],
        "sw": [
            "Kuna mengi zaidi ya kusema kuhusu compliment back request.",
            "Nafurahi umetaja compliment back request - endelea, nasikiliza.",
        ],
        "fr": [
            "Je pourrais continuer à parler de compliment back request un moment.",
            "Content que tu aies parlé de compliment back request - continue, j'écoute.",
        ],
    },
    "DEADLINE_RESPONSES": {
        "en": [
            "Noted - I'll keep that in mind as we talk about deadline.",
            "I like where this deadline conversation is headed.",
            "I don't think we've fully covered deadline yet - what else is on your mind?",
        ],
        "sw": [
            "Napenda mwelekeo wa mazungumzo haya kuhusu deadline.",
            "Jisikie huru kunieleza zaidi kuhusu deadline wakati wowote.",
        ],
        "fr": [
            "J'aime la direction que prend cette discussion sur deadline.",
            "Je pourrais continuer à parler de deadline un moment.",
        ],
    },
    "PREGNANCY_BABY_RESPONSES": {
        "en": [
            "That's interesting, tell me a bit more about pregnancy baby.",
            "Thanks for sharing that - pregnancy baby is worth talking through.",
            "Glad you brought pregnancy baby up - keep going, I'm listening.",
        ],
        "sw": [
            "Asante kwa kushiriki - pregnancy baby inafaa kuzungumziwa.",
            "Napenda mwelekeo wa mazungumzo haya kuhusu pregnancy baby.",
        ],
        "fr": [
            "Merci d'avoir partagé ça - pregnancy baby mérite qu'on en parle.",
            "Content que tu aies parlé de pregnancy baby - continue, j'écoute.",
        ],
    },
    "WEDDING_ENGAGEMENT_RESPONSES": {
        "en": [
            "Feel free to tell me more about wedding engagement whenever you like.",
            "Noted - I'll keep that in mind as we talk about wedding engagement.",
            "I could keep chatting about wedding engagement for a while.",
        ],
        "sw": [
            "Asante kwa kushiriki - wedding engagement inafaa kuzungumziwa.",
            "Nafurahi umetaja wedding engagement - endelea, nasikiliza.",
        ],
        "fr": [
            "C'est un bon point de vue sur wedding engagement.",
            "N'hésite pas à m'en dire plus sur wedding engagement quand tu veux.",
        ],
    },
    "GRADUATION_RESPONSES": {
        "en": [
            "That's a good angle on graduation, honestly.",
            "I could keep chatting about graduation for a while.",
            "That's interesting, tell me a bit more about graduation.",
        ],
        "sw": [
            "Ningeweza kuendelea kuzungumza kuhusu graduation kwa muda.",
            "Bado hatujamaliza kuzungumza kuhusu graduation - kuna nini kingine?",
        ],
        "fr": [
            "N'hésite pas à m'en dire plus sur graduation quand tu veux.",
            "Merci d'avoir partagé ça - graduation mérite qu'on en parle.",
        ],
    },
    "MOVING_CITY_RESPONSES": {
        "en": [
            "Thanks for sharing that - moving city is worth talking through.",
            "I could keep chatting about moving city for a while.",
            "Noted - I'll keep that in mind as we talk about moving city.",
        ],
        "sw": [
            "Nafurahi umetaja moving city - endelea, nasikiliza.",
            "Hilo ni jambo zuri kuhusu moving city.",
        ],
        "fr": [
            "On n'a pas encore tout dit sur moving city - quoi d'autre ?",
            "Il y a toujours plus à dire sur moving city.",
        ],
    },
    "NEW_PET_RESPONSES": {
        "en": [
            "Noted - I'll keep that in mind as we talk about new pet.",
            "Feel free to tell me more about new pet whenever you like.",
            "There's always more to say about new pet.",
        ],
        "sw": [
            "Asante kwa kushiriki - new pet inafaa kuzungumziwa.",
            "Bado hatujamaliza kuzungumza kuhusu new pet - kuna nini kingine?",
        ],
        "fr": [
            "Merci d'avoir partagé ça - new pet mérite qu'on en parle.",
            "On n'a pas encore tout dit sur new pet - quoi d'autre ?",
        ],
    },
    "FIRST_DAY_RESPONSES": {
        "en": [
            "Glad you brought first day up - keep going, I'm listening.",
            "I could keep chatting about first day for a while.",
            "That's interesting, tell me a bit more about first day.",
        ],
        "sw": [
            "Kuna mengi zaidi ya kusema kuhusu first day.",
            "Hilo ni jambo zuri kuhusu first day.",
        ],
        "fr": [
            "J'aime la direction que prend cette discussion sur first day.",
            "Content que tu aies parlé de first day - continue, j'écoute.",
        ],
    },
    "REUNION_RESPONSES": {
        "en": [
            "That's interesting, tell me a bit more about reunion.",
            "I could keep chatting about reunion for a while.",
            "There's always more to say about reunion.",
        ],
        "sw": [
            "Jisikie huru kunieleza zaidi kuhusu reunion wakati wowote.",
            "Ningeweza kuendelea kuzungumza kuhusu reunion kwa muda.",
        ],
        "fr": [
            "Je pourrais continuer à parler de reunion un moment.",
            "Content que tu aies parlé de reunion - continue, j'écoute.",
        ],
    },
    "FLUENCY_GOALS_RESPONSES": {
        "en": [
            "Thanks for sharing that - fluency goals is worth talking through.",
            "Noted - I'll keep that in mind as we talk about fluency goals.",
            "I don't think we've fully covered fluency goals yet - what else is on your mind?",
        ],
        "sw": [
            "Kuna mengi zaidi ya kusema kuhusu fluency goals.",
            "Asante kwa kushiriki - fluency goals inafaa kuzungumziwa.",
        ],
        "fr": [
            "J'aime la direction que prend cette discussion sur fluency goals.",
            "Il y a toujours plus à dire sur fluency goals.",
        ],
    },
    "CULTURAL_TRADITIONS_RESPONSES": {
        "en": [
            "There's always more to say about cultural traditions.",
            "I could keep chatting about cultural traditions for a while.",
            "That's interesting, tell me a bit more about cultural traditions.",
        ],
        "sw": [
            "Kuna mengi zaidi ya kusema kuhusu cultural traditions.",
            "Hilo ni jambo zuri kuhusu cultural traditions.",
        ],
        "fr": [
            "Content que tu aies parlé de cultural traditions - continue, j'écoute.",
            "N'hésite pas à m'en dire plus sur cultural traditions quand tu veux.",
        ],
    },
    "SUSTAINABILITY_RESPONSES": {
        "en": [
            "I like where this sustainability conversation is headed.",
            "I don't think we've fully covered sustainability yet - what else is on your mind?",
            "Noted - I'll keep that in mind as we talk about sustainability.",
        ],
        "sw": [
            "Jisikie huru kunieleza zaidi kuhusu sustainability wakati wowote.",
            "Ningeweza kuendelea kuzungumza kuhusu sustainability kwa muda.",
        ],
        "fr": [
            "On n'a pas encore tout dit sur sustainability - quoi d'autre ?",
            "Content que tu aies parlé de sustainability - continue, j'écoute.",
        ],
    },
    "FUN_FACT_RESPONSES": {
        "en": [
            "Feel free to tell me more about fun fact whenever you like.",
            "That's interesting, tell me a bit more about fun fact.",
            "I could keep chatting about fun fact for a while.",
        ],
        "sw": [
            "Nafurahi umetaja fun fact - endelea, nasikiliza.",
            "Kuna mengi zaidi ya kusema kuhusu fun fact.",
        ],
        "fr": [
            "Je pourrais continuer à parler de fun fact un moment.",
            "J'aime la direction que prend cette discussion sur fun fact.",
        ],
    },
    "GIFT_THANKS_RESPONSES": {
        "en": [
            "Glad you brought gift thanks up - keep going, I'm listening.",
            "That's interesting, tell me a bit more about gift thanks.",
            "Noted - I'll keep that in mind as we talk about gift thanks.",
        ],
        "sw": [
            "Kuna mengi zaidi ya kusema kuhusu gift thanks.",
            "Napenda mwelekeo wa mazungumzo haya kuhusu gift thanks.",
        ],
        "fr": [
            "Je pourrais continuer à parler de gift thanks un moment.",
            "J'aime la direction que prend cette discussion sur gift thanks.",
        ],
    },
    "RUNNING_LATE_RESPONSES": {
        "en": [
            "That's a good angle on running late, honestly.",
            "Thanks for sharing that - running late is worth talking through.",
            "Glad you brought running late up - keep going, I'm listening.",
        ],
        "sw": [
            "Hilo ni jambo zuri kuhusu running late.",
            "Asante kwa kushiriki - running late inafaa kuzungumziwa.",
        ],
        "fr": [
            "J'aime la direction que prend cette discussion sur running late.",
            "C'est un bon point de vue sur running late.",
        ],
    },
    "TIME_MANAGEMENT_RESPONSES": {
        "en": [
            "I like where this time management conversation is headed.",
            "I don't think we've fully covered time management yet - what else is on your mind?",
            "Thanks for sharing that - time management is worth talking through.",
        ],
        "sw": [
            "Napenda mwelekeo wa mazungumzo haya kuhusu time management.",
            "Jisikie huru kunieleza zaidi kuhusu time management wakati wowote.",
        ],
        "fr": [
            "Content que tu aies parlé de time management - continue, j'écoute.",
            "On n'a pas encore tout dit sur time management - quoi d'autre ?",
        ],
    },
    "SPORTS_VICTORY_RESPONSES": {
        "en": [
            "Thanks for sharing that - sports victory is worth talking through.",
            "Feel free to tell me more about sports victory whenever you like.",
            "I like where this sports victory conversation is headed.",
        ],
        "sw": [
            "Ningeweza kuendelea kuzungumza kuhusu sports victory kwa muda.",
            "Jisikie huru kunieleza zaidi kuhusu sports victory wakati wowote.",
        ],
        "fr": [
            "J'aime la direction que prend cette discussion sur sports victory.",
            "C'est un bon point de vue sur sports victory.",
        ],
    },
    "SPORTS_LOSS_RESPONSES": {
        "en": [
            "I like where this sports loss conversation is headed.",
            "That's a good angle on sports loss, honestly.",
            "I could keep chatting about sports loss for a while.",
        ],
        "sw": [
            "Asante kwa kushiriki - sports loss inafaa kuzungumziwa.",
            "Bado hatujamaliza kuzungumza kuhusu sports loss - kuna nini kingine?",
        ],
        "fr": [
            "C'est un bon point de vue sur sports loss.",
            "Merci d'avoir partagé ça - sports loss mérite qu'on en parle.",
        ],
    },
    "UNPREDICTABLE_WEATHER_RESPONSES": {
        "en": [
            "That's interesting, tell me a bit more about unpredictable weather.",
            "Feel free to tell me more about unpredictable weather whenever you like.",
            "I like where this unpredictable weather conversation is headed.",
        ],
        "sw": [
            "Napenda mwelekeo wa mazungumzo haya kuhusu unpredictable weather.",
            "Bado hatujamaliza kuzungumza kuhusu unpredictable weather - kuna nini kingine?",
        ],
        "fr": [
            "Je pourrais continuer à parler de unpredictable weather un moment.",
            "Content que tu aies parlé de unpredictable weather - continue, j'écoute.",
        ],
    },
    "NEW_YEAR_RESOLUTION_RESPONSES": {
        "en": [
            "I don't think we've fully covered new year resolution yet - what else is on your mind?",
            "That's interesting, tell me a bit more about new year resolution.",
            "Thanks for sharing that - new year resolution is worth talking through.",
        ],
        "sw": [
            "Napenda mwelekeo wa mazungumzo haya kuhusu new year resolution.",
            "Ningeweza kuendelea kuzungumza kuhusu new year resolution kwa muda.",
        ],
        "fr": [
            "C'est un bon point de vue sur new year resolution.",
            "J'aime la direction que prend cette discussion sur new year resolution.",
        ],
    },
    "CHILDHOOD_MEMORY_RESPONSES": {
        "en": [
            "Feel free to tell me more about childhood memory whenever you like.",
            "That's a good angle on childhood memory, honestly.",
            "Noted - I'll keep that in mind as we talk about childhood memory.",
        ],
        "sw": [
            "Napenda mwelekeo wa mazungumzo haya kuhusu childhood memory.",
            "Jisikie huru kunieleza zaidi kuhusu childhood memory wakati wowote.",
        ],
        "fr": [
            "Content que tu aies parlé de childhood memory - continue, j'écoute.",
            "N'hésite pas à m'en dire plus sur childhood memory quand tu veux.",
        ],
    },
    "ROLE_MODEL_RESPONSES": {
        "en": [
            "There's always more to say about role model.",
            "I don't think we've fully covered role model yet - what else is on your mind?",
            "I like where this role model conversation is headed.",
        ],
        "sw": [
            "Asante kwa kushiriki - role model inafaa kuzungumziwa.",
            "Bado hatujamaliza kuzungumza kuhusu role model - kuna nini kingine?",
        ],
        "fr": [
            "N'hésite pas à m'en dire plus sur role model quand tu veux.",
            "Merci d'avoir partagé ça - role model mérite qu'on en parle.",
        ],
    },
    "FEAR_PHOBIA_RESPONSES": {
        "en": [
            "Glad you brought fear phobia up - keep going, I'm listening.",
            "There's always more to say about fear phobia.",
            "I like where this fear phobia conversation is headed.",
        ],
        "sw": [
            "Jisikie huru kunieleza zaidi kuhusu fear phobia wakati wowote.",
            "Asante kwa kushiriki - fear phobia inafaa kuzungumziwa.",
        ],
        "fr": [
            "Je pourrais continuer à parler de fear phobia un moment.",
            "Il y a toujours plus à dire sur fear phobia.",
        ],
    },
    "DREAM_INTERPRETATION_RESPONSES": {
        "en": [
            "That's a good angle on dream interpretation, honestly.",
            "Glad you brought dream interpretation up - keep going, I'm listening.",
            "Feel free to tell me more about dream interpretation whenever you like.",
        ],
        "sw": [
            "Napenda mwelekeo wa mazungumzo haya kuhusu dream interpretation.",
            "Ningeweza kuendelea kuzungumza kuhusu dream interpretation kwa muda.",
        ],
        "fr": [
            "Content que tu aies parlé de dream interpretation - continue, j'écoute.",
            "Merci d'avoir partagé ça - dream interpretation mérite qu'on en parle.",
        ],
    },
    "SELF_IMPROVEMENT_RESPONSES": {
        "en": [
            "Thanks for sharing that - self improvement is worth talking through.",
            "I like where this self improvement conversation is headed.",
            "Feel free to tell me more about self improvement whenever you like.",
        ],
        "sw": [
            "Kuna mengi zaidi ya kusema kuhusu self improvement.",
            "Hilo ni jambo zuri kuhusu self improvement.",
        ],
        "fr": [
            "Il y a toujours plus à dire sur self improvement.",
            "Merci d'avoir partagé ça - self improvement mérite qu'on en parle.",
        ],
    },
    "SOCIAL_MEDIA_RESPONSES": {
        "en": [
            "That's a good angle on social media, honestly.",
            "I could keep chatting about social media for a while.",
            "Feel free to tell me more about social media whenever you like.",
        ],
        "sw": [
            "Kuna mengi zaidi ya kusema kuhusu social media.",
            "Ningeweza kuendelea kuzungumza kuhusu social media kwa muda.",
        ],
        "fr": [
            "Je pourrais continuer à parler de social media un moment.",
            "On n'a pas encore tout dit sur social media - quoi d'autre ?",
        ],
    },
    "REMOTE_WORK_RESPONSES": {
        "en": [
            "I like where this remote work conversation is headed.",
            "Noted - I'll keep that in mind as we talk about remote work.",
            "There's always more to say about remote work.",
        ],
        "sw": [
            "Asante kwa kushiriki - remote work inafaa kuzungumziwa.",
            "Nafurahi umetaja remote work - endelea, nasikiliza.",
        ],
        "fr": [
            "J'aime la direction que prend cette discussion sur remote work.",
            "Merci d'avoir partagé ça - remote work mérite qu'on en parle.",
        ],
    },
    "JOB_INTERVIEW_RESPONSES": {
        "en": [
            "I could keep chatting about job interview for a while.",
            "Feel free to tell me more about job interview whenever you like.",
            "There's always more to say about job interview.",
        ],
        "sw": [
            "Hilo ni jambo zuri kuhusu job interview.",
            "Asante kwa kushiriki - job interview inafaa kuzungumziwa.",
        ],
        "fr": [
            "On n'a pas encore tout dit sur job interview - quoi d'autre ?",
            "J'aime la direction que prend cette discussion sur job interview.",
        ],
    },
    "RECIPE_DISH_RESPONSES": {
        "en": [
            "Noted - I'll keep that in mind as we talk about recipe dish.",
            "Feel free to tell me more about recipe dish whenever you like.",
            "That's a good angle on recipe dish, honestly.",
        ],
        "sw": [
            "Kuna mengi zaidi ya kusema kuhusu recipe dish.",
            "Jisikie huru kunieleza zaidi kuhusu recipe dish wakati wowote.",
        ],
        "fr": [
            "Merci d'avoir partagé ça - recipe dish mérite qu'on en parle.",
            "N'hésite pas à m'en dire plus sur recipe dish quand tu veux.",
        ],
    },
    "INSOMNIA_RESPONSES": {
        "en": [
            "I like where this insomnia conversation is headed.",
            "I could keep chatting about insomnia for a while.",
            "There's always more to say about insomnia.",
        ],
        "sw": [
            "Nafurahi umetaja insomnia - endelea, nasikiliza.",
            "Bado hatujamaliza kuzungumza kuhusu insomnia - kuna nini kingine?",
        ],
        "fr": [
            "On n'a pas encore tout dit sur insomnia - quoi d'autre ?",
            "Content que tu aies parlé de insomnia - continue, j'écoute.",
        ],
    },
    "QUITTING_HABIT_RESPONSES": {
        "en": [
            "Thanks for sharing that - quitting habit is worth talking through.",
            "There's always more to say about quitting habit.",
            "Noted - I'll keep that in mind as we talk about quitting habit.",
        ],
        "sw": [
            "Hilo ni jambo zuri kuhusu quitting habit.",
            "Napenda mwelekeo wa mazungumzo haya kuhusu quitting habit.",
        ],
        "fr": [
            "Content que tu aies parlé de quitting habit - continue, j'écoute.",
            "C'est un bon point de vue sur quitting habit.",
        ],
    },
    "MEDITATION_MINDFULNESS_RESPONSES": {
        "en": [
            "Thanks for sharing that - meditation mindfulness is worth talking through.",
            "Feel free to tell me more about meditation mindfulness whenever you like.",
            "I could keep chatting about meditation mindfulness for a while.",
        ],
        "sw": [
            "Nafurahi umetaja meditation mindfulness - endelea, nasikiliza.",
            "Hilo ni jambo zuri kuhusu meditation mindfulness.",
        ],
        "fr": [
            "Il y a toujours plus à dire sur meditation mindfulness.",
            "Je pourrais continuer à parler de meditation mindfulness un moment.",
        ],
    },
    "SIBLING_RIVALRY_RESPONSES": {
        "en": [
            "Thanks for sharing that - sibling rivalry is worth talking through.",
            "I could keep chatting about sibling rivalry for a while.",
            "I like where this sibling rivalry conversation is headed.",
        ],
        "sw": [
            "Bado hatujamaliza kuzungumza kuhusu sibling rivalry - kuna nini kingine?",
            "Jisikie huru kunieleza zaidi kuhusu sibling rivalry wakati wowote.",
        ],
        "fr": [
            "N'hésite pas à m'en dire plus sur sibling rivalry quand tu veux.",
            "Il y a toujours plus à dire sur sibling rivalry.",
        ],
    },
    "LONG_DISTANCE_RELATIONSHIP_RESPONSES": {
        "en": [
            "Thanks for sharing that - long distance relationship is worth talking through.",
            "That's interesting, tell me a bit more about long distance relationship.",
            "That's a good angle on long distance relationship, honestly.",
        ],
        "sw": [
            "Jisikie huru kunieleza zaidi kuhusu long distance relationship wakati wowote.",
            "Bado hatujamaliza kuzungumza kuhusu long distance relationship - kuna nini kingine?",
        ],
        "fr": [
            "N'hésite pas à m'en dire plus sur long distance relationship quand tu veux.",
            "J'aime la direction que prend cette discussion sur long distance relationship.",
        ],
    },
    "PET_PEEVE_RESPONSES": {
        "en": [
            "Feel free to tell me more about pet peeve whenever you like.",
            "I don't think we've fully covered pet peeve yet - what else is on your mind?",
            "I could keep chatting about pet peeve for a while.",
        ],
        "sw": [
            "Napenda mwelekeo wa mazungumzo haya kuhusu pet peeve.",
            "Kuna mengi zaidi ya kusema kuhusu pet peeve.",
        ],
        "fr": [
            "Il y a toujours plus à dire sur pet peeve.",
            "Je pourrais continuer à parler de pet peeve un moment.",
        ],
    },
    "KINDNESS_RESPONSES": {
        "en": [
            "Thanks for sharing that - kindness is worth talking through.",
            "There's always more to say about kindness.",
            "That's a good angle on kindness, honestly.",
        ],
        "sw": [
            "Bado hatujamaliza kuzungumza kuhusu kindness - kuna nini kingine?",
            "Asante kwa kushiriki - kindness inafaa kuzungumziwa.",
        ],
        "fr": [
            "N'hésite pas à m'en dire plus sur kindness quand tu veux.",
            "Il y a toujours plus à dire sur kindness.",
        ],
    },
    "PROCRASTINATION_RESPONSES": {
        "en": [
            "Glad you brought procrastination up - keep going, I'm listening.",
            "That's a good angle on procrastination, honestly.",
            "There's always more to say about procrastination.",
        ],
        "sw": [
            "Hilo ni jambo zuri kuhusu procrastination.",
            "Napenda mwelekeo wa mazungumzo haya kuhusu procrastination.",
        ],
        "fr": [
            "C'est un bon point de vue sur procrastination.",
            "Je pourrais continuer à parler de procrastination un moment.",
        ],
    },
    "DECLUTTERING_RESPONSES": {
        "en": [
            "That's a good angle on decluttering, honestly.",
            "Feel free to tell me more about decluttering whenever you like.",
            "Glad you brought decluttering up - keep going, I'm listening.",
        ],
        "sw": [
            "Bado hatujamaliza kuzungumza kuhusu decluttering - kuna nini kingine?",
            "Nafurahi umetaja decluttering - endelea, nasikiliza.",
        ],
        "fr": [
            "Content que tu aies parlé de decluttering - continue, j'écoute.",
            "Il y a toujours plus à dire sur decluttering.",
        ],
    },
    "PUBLIC_SPEAKING_RESPONSES": {
        "en": [
            "Noted - I'll keep that in mind as we talk about public speaking.",
            "I like where this public speaking conversation is headed.",
            "Glad you brought public speaking up - keep going, I'm listening.",
        ],
        "sw": [
            "Kuna mengi zaidi ya kusema kuhusu public speaking.",
            "Jisikie huru kunieleza zaidi kuhusu public speaking wakati wowote.",
        ],
        "fr": [
            "On n'a pas encore tout dit sur public speaking - quoi d'autre ?",
            "Il y a toujours plus à dire sur public speaking.",
        ],
    },
    "LEARNING_TO_DRIVE_RESPONSES": {
        "en": [
            "I don't think we've fully covered learning to drive yet - what else is on your mind?",
            "Feel free to tell me more about learning to drive whenever you like.",
            "That's a good angle on learning to drive, honestly.",
        ],
        "sw": [
            "Jisikie huru kunieleza zaidi kuhusu learning to drive wakati wowote.",
            "Bado hatujamaliza kuzungumza kuhusu learning to drive - kuna nini kingine?",
        ],
        "fr": [
            "Content que tu aies parlé de learning to drive - continue, j'écoute.",
            "Merci d'avoir partagé ça - learning to drive mérite qu'on en parle.",
        ],
    },
    "RETIREMENT_PLANNING_RESPONSES": {
        "en": [
            "I don't think we've fully covered retirement planning yet - what else is on your mind?",
            "Glad you brought retirement planning up - keep going, I'm listening.",
            "I could keep chatting about retirement planning for a while.",
        ],
        "sw": [
            "Kuna mengi zaidi ya kusema kuhusu retirement planning.",
            "Jisikie huru kunieleza zaidi kuhusu retirement planning wakati wowote.",
        ],
        "fr": [
            "Il y a toujours plus à dire sur retirement planning.",
            "C'est un bon point de vue sur retirement planning.",
        ],
    },
    "PROGRAMMING_CODING_RESPONSES": {
        "en": [
            "Thanks for sharing that - programming coding is worth talking through.",
            "Feel free to tell me more about programming coding whenever you like.",
            "There's always more to say about programming coding.",
        ],
        "sw": [
            "Asante kwa kushiriki - programming coding inafaa kuzungumziwa.",
            "Napenda mwelekeo wa mazungumzo haya kuhusu programming coding.",
        ],
        "fr": [
            "C'est un bon point de vue sur programming coding.",
            "J'aime la direction que prend cette discussion sur programming coding.",
        ],
    },
    "GYM_INTIMIDATION_RESPONSES": {
        "en": [
            "I don't think we've fully covered gym intimidation yet - what else is on your mind?",
            "Noted - I'll keep that in mind as we talk about gym intimidation.",
            "I like where this gym intimidation conversation is headed.",
        ],
        "sw": [
            "Asante kwa kushiriki - gym intimidation inafaa kuzungumziwa.",
            "Jisikie huru kunieleza zaidi kuhusu gym intimidation wakati wowote.",
        ],
        "fr": [
            "On n'a pas encore tout dit sur gym intimidation - quoi d'autre ?",
            "Merci d'avoir partagé ça - gym intimidation mérite qu'on en parle.",
        ],
    },
    "COMFORT_FOOD_RESPONSES": {
        "en": [
            "Thanks for sharing that - comfort food is worth talking through.",
            "I could keep chatting about comfort food for a while.",
            "Noted - I'll keep that in mind as we talk about comfort food.",
        ],
        "sw": [
            "Kuna mengi zaidi ya kusema kuhusu comfort food.",
            "Hilo ni jambo zuri kuhusu comfort food.",
        ],
        "fr": [
            "Merci d'avoir partagé ça - comfort food mérite qu'on en parle.",
            "On n'a pas encore tout dit sur comfort food - quoi d'autre ?",
        ],
    },
    "SINGING_VOICE_RESPONSES": {
        "en": [
            "There's always more to say about singing voice.",
            "Feel free to tell me more about singing voice whenever you like.",
            "Glad you brought singing voice up - keep going, I'm listening.",
        ],
        "sw": [
            "Kuna mengi zaidi ya kusema kuhusu singing voice.",
            "Asante kwa kushiriki - singing voice inafaa kuzungumziwa.",
        ],
        "fr": [
            "J'aime la direction que prend cette discussion sur singing voice.",
            "Merci d'avoir partagé ça - singing voice mérite qu'on en parle.",
        ],
    },
    "JOURNALING_RESPONSES": {
        "en": [
            "That's interesting, tell me a bit more about journaling.",
            "Noted - I'll keep that in mind as we talk about journaling.",
            "Feel free to tell me more about journaling whenever you like.",
        ],
        "sw": [
            "Ningeweza kuendelea kuzungumza kuhusu journaling kwa muda.",
            "Napenda mwelekeo wa mazungumzo haya kuhusu journaling.",
        ],
        "fr": [
            "J'aime la direction que prend cette discussion sur journaling.",
            "C'est un bon point de vue sur journaling.",
        ],
    },
    "BOARD_GAMES_PUZZLES_RESPONSES": {
        "en": [
            "Noted - I'll keep that in mind as we talk about board games puzzles.",
            "I could keep chatting about board games puzzles for a while.",
            "There's always more to say about board games puzzles.",
        ],
        "sw": [
            "Kuna mengi zaidi ya kusema kuhusu board games puzzles.",
            "Ningeweza kuendelea kuzungumza kuhusu board games puzzles kwa muda.",
        ],
        "fr": [
            "C'est un bon point de vue sur board games puzzles.",
            "Merci d'avoir partagé ça - board games puzzles mérite qu'on en parle.",
        ],
    },
    "CAMPING_OUTDOOR_TRIP_RESPONSES": {
        "en": [
            "Thanks for sharing that - camping outdoor trip is worth talking through.",
            "That's a good angle on camping outdoor trip, honestly.",
            "I could keep chatting about camping outdoor trip for a while.",
        ],
        "sw": [
            "Jisikie huru kunieleza zaidi kuhusu camping outdoor trip wakati wowote.",
            "Ningeweza kuendelea kuzungumza kuhusu camping outdoor trip kwa muda.",
        ],
        "fr": [
            "Merci d'avoir partagé ça - camping outdoor trip mérite qu'on en parle.",
            "C'est un bon point de vue sur camping outdoor trip.",
        ],
    },
    "CAR_TROUBLE_RESPONSES": {
        "en": [
            "I could keep chatting about car trouble for a while.",
            "There's always more to say about car trouble.",
            "Feel free to tell me more about car trouble whenever you like.",
        ],
        "sw": [
            "Ningeweza kuendelea kuzungumza kuhusu car trouble kwa muda.",
            "Nafurahi umetaja car trouble - endelea, nasikiliza.",
        ],
        "fr": [
            "J'aime la direction que prend cette discussion sur car trouble.",
            "Content que tu aies parlé de car trouble - continue, j'écoute.",
        ],
    },
    "ROOMMATES_RESPONSES": {
        "en": [
            "Glad you brought roommates up - keep going, I'm listening.",
            "Thanks for sharing that - roommates is worth talking through.",
            "There's always more to say about roommates.",
        ],
        "sw": [
            "Kuna mengi zaidi ya kusema kuhusu roommates.",
            "Ningeweza kuendelea kuzungumza kuhusu roommates kwa muda.",
        ],
        "fr": [
            "Il y a toujours plus à dire sur roommates.",
            "On n'a pas encore tout dit sur roommates - quoi d'autre ?",
        ],
    },
    "ONLINE_DATING_RESPONSES": {
        "en": [
            "I could keep chatting about online dating for a while.",
            "There's always more to say about online dating.",
            "Feel free to tell me more about online dating whenever you like.",
        ],
        "sw": [
            "Nafurahi umetaja online dating - endelea, nasikiliza.",
            "Napenda mwelekeo wa mazungumzo haya kuhusu online dating.",
        ],
        "fr": [
            "On n'a pas encore tout dit sur online dating - quoi d'autre ?",
            "J'aime la direction que prend cette discussion sur online dating.",
        ],
    },
    "TATTOOS_PIERCINGS_RESPONSES": {
        "en": [
            "Noted - I'll keep that in mind as we talk about tattoos piercings.",
            "That's interesting, tell me a bit more about tattoos piercings.",
            "Feel free to tell me more about tattoos piercings whenever you like.",
        ],
        "sw": [
            "Kuna mengi zaidi ya kusema kuhusu tattoos piercings.",
            "Hilo ni jambo zuri kuhusu tattoos piercings.",
        ],
        "fr": [
            "N'hésite pas à m'en dire plus sur tattoos piercings quand tu veux.",
            "Je pourrais continuer à parler de tattoos piercings un moment.",
        ],
    },
    "FASHION_STYLE_RESPONSES": {
        "en": [
            "I could keep chatting about fashion style for a while.",
            "I don't think we've fully covered fashion style yet - what else is on your mind?",
            "I like where this fashion style conversation is headed.",
        ],
        "sw": [
            "Napenda mwelekeo wa mazungumzo haya kuhusu fashion style.",
            "Nafurahi umetaja fashion style - endelea, nasikiliza.",
        ],
        "fr": [
            "Il y a toujours plus à dire sur fashion style.",
            "J'aime la direction que prend cette discussion sur fashion style.",
        ],
    },
    "LANGUAGE_BARRIER_RESPONSES": {
        "en": [
            "Noted - I'll keep that in mind as we talk about language barrier.",
            "That's a good angle on language barrier, honestly.",
            "Glad you brought language barrier up - keep going, I'm listening.",
        ],
        "sw": [
            "Asante kwa kushiriki - language barrier inafaa kuzungumziwa.",
            "Kuna mengi zaidi ya kusema kuhusu language barrier.",
        ],
        "fr": [
            "Il y a toujours plus à dire sur language barrier.",
            "Content que tu aies parlé de language barrier - continue, j'écoute.",
        ],
    },
    "SCHOOL_VOLUNTEERING_RESPONSES": {
        "en": [
            "Noted - I'll keep that in mind as we talk about school volunteering.",
            "Feel free to tell me more about school volunteering whenever you like.",
            "There's always more to say about school volunteering.",
        ],
        "sw": [
            "Napenda mwelekeo wa mazungumzo haya kuhusu school volunteering.",
            "Asante kwa kushiriki - school volunteering inafaa kuzungumziwa.",
        ],
        "fr": [
            "C'est un bon point de vue sur school volunteering.",
            "Je pourrais continuer à parler de school volunteering un moment.",
        ],
    },
    "CHARITY_DONATION_RESPONSES": {
        "en": [
            "I could keep chatting about charity donation for a while.",
            "Noted - I'll keep that in mind as we talk about charity donation.",
            "I don't think we've fully covered charity donation yet - what else is on your mind?",
        ],
        "sw": [
            "Napenda mwelekeo wa mazungumzo haya kuhusu charity donation.",
            "Bado hatujamaliza kuzungumza kuhusu charity donation - kuna nini kingine?",
        ],
        "fr": [
            "Content que tu aies parlé de charity donation - continue, j'écoute.",
            "Merci d'avoir partagé ça - charity donation mérite qu'on en parle.",
        ],
    },
    "HOSTING_GUESTS_RESPONSES": {
        "en": [
            "I like where this hosting guests conversation is headed.",
            "Feel free to tell me more about hosting guests whenever you like.",
            "Noted - I'll keep that in mind as we talk about hosting guests.",
        ],
        "sw": [
            "Bado hatujamaliza kuzungumza kuhusu hosting guests - kuna nini kingine?",
            "Kuna mengi zaidi ya kusema kuhusu hosting guests.",
        ],
        "fr": [
            "Content que tu aies parlé de hosting guests - continue, j'écoute.",
            "J'aime la direction que prend cette discussion sur hosting guests.",
        ],
    },
    "TIME_ZONES_RESPONSES": {
        "en": [
            "I could keep chatting about time zones for a while.",
            "There's always more to say about time zones.",
            "Glad you brought time zones up - keep going, I'm listening.",
        ],
        "sw": [
            "Bado hatujamaliza kuzungumza kuhusu time zones - kuna nini kingine?",
            "Asante kwa kushiriki - time zones inafaa kuzungumziwa.",
        ],
        "fr": [
            "C'est un bon point de vue sur time zones.",
            "Merci d'avoir partagé ça - time zones mérite qu'on en parle.",
        ],
    },
    "PRODUCTIVITY_TOOLS_RESPONSES": {
        "en": [
            "I could keep chatting about productivity tools for a while.",
            "Thanks for sharing that - productivity tools is worth talking through.",
            "Feel free to tell me more about productivity tools whenever you like.",
        ],
        "sw": [
            "Nafurahi umetaja productivity tools - endelea, nasikiliza.",
            "Asante kwa kushiriki - productivity tools inafaa kuzungumziwa.",
        ],
        "fr": [
            "J'aime la direction que prend cette discussion sur productivity tools.",
            "N'hésite pas à m'en dire plus sur productivity tools quand tu veux.",
        ],
    },
    "PARENTING_RESPONSES": {
        "en": [
            "Feel free to tell me more about parenting whenever you like.",
            "There's always more to say about parenting.",
            "I don't think we've fully covered parenting yet - what else is on your mind?",
        ],
        "sw": [
            "Nafurahi umetaja parenting - endelea, nasikiliza.",
            "Kuna mengi zaidi ya kusema kuhusu parenting.",
        ],
        "fr": [
            "On n'a pas encore tout dit sur parenting - quoi d'autre ?",
            "N'hésite pas à m'en dire plus sur parenting quand tu veux.",
        ],
    },
    "TEENAGER_STRUGGLE_RESPONSES": {
        "en": [
            "There's always more to say about teenager struggle.",
            "I like where this teenager struggle conversation is headed.",
            "Thanks for sharing that - teenager struggle is worth talking through.",
        ],
        "sw": [
            "Ningeweza kuendelea kuzungumza kuhusu teenager struggle kwa muda.",
            "Hilo ni jambo zuri kuhusu teenager struggle.",
        ],
        "fr": [
            "Merci d'avoir partagé ça - teenager struggle mérite qu'on en parle.",
            "C'est un bon point de vue sur teenager struggle.",
        ],
    },
    "ELDERLY_PARENT_CARE_RESPONSES": {
        "en": [
            "I like where this elderly parent care conversation is headed.",
            "That's a good angle on elderly parent care, honestly.",
            "There's always more to say about elderly parent care.",
        ],
        "sw": [
            "Jisikie huru kunieleza zaidi kuhusu elderly parent care wakati wowote.",
            "Hilo ni jambo zuri kuhusu elderly parent care.",
        ],
        "fr": [
            "Il y a toujours plus à dire sur elderly parent care.",
            "Content que tu aies parlé de elderly parent care - continue, j'écoute.",
        ],
    },
    "GRIEF_LOSS_RESPONSES": {
        "en": [
            "That's interesting, tell me a bit more about grief loss.",
            "Thanks for sharing that - grief loss is worth talking through.",
            "I like where this grief loss conversation is headed.",
        ],
        "sw": [
            "Bado hatujamaliza kuzungumza kuhusu grief loss - kuna nini kingine?",
            "Kuna mengi zaidi ya kusema kuhusu grief loss.",
        ],
        "fr": [
            "Je pourrais continuer à parler de grief loss un moment.",
            "J'aime la direction que prend cette discussion sur grief loss.",
        ],
    },
    "THERAPY_COUNSELING_RESPONSES": {
        "en": [
            "I don't think we've fully covered therapy counseling yet - what else is on your mind?",
            "That's interesting, tell me a bit more about therapy counseling.",
            "That's a good angle on therapy counseling, honestly.",
        ],
        "sw": [
            "Napenda mwelekeo wa mazungumzo haya kuhusu therapy counseling.",
            "Kuna mengi zaidi ya kusema kuhusu therapy counseling.",
        ],
        "fr": [
            "Content que tu aies parlé de therapy counseling - continue, j'écoute.",
            "Je pourrais continuer à parler de therapy counseling un moment.",
        ],
    },
    "ADDICTION_RECOVERY_RESPONSES": {
        "en": [
            "I like where this addiction recovery conversation is headed.",
            "That's interesting, tell me a bit more about addiction recovery.",
            "Feel free to tell me more about addiction recovery whenever you like.",
        ],
        "sw": [
            "Kuna mengi zaidi ya kusema kuhusu addiction recovery.",
            "Bado hatujamaliza kuzungumza kuhusu addiction recovery - kuna nini kingine?",
        ],
        "fr": [
            "Merci d'avoir partagé ça - addiction recovery mérite qu'on en parle.",
            "N'hésite pas à m'en dire plus sur addiction recovery quand tu veux.",
        ],
    },
    "IDENTITY_COMING_OUT_RESPONSES": {
        "en": [
            "I could keep chatting about identity coming out for a while.",
            "Glad you brought identity coming out up - keep going, I'm listening.",
            "Noted - I'll keep that in mind as we talk about identity coming out.",
        ],
        "sw": [
            "Ningeweza kuendelea kuzungumza kuhusu identity coming out kwa muda.",
            "Napenda mwelekeo wa mazungumzo haya kuhusu identity coming out.",
        ],
        "fr": [
            "C'est un bon point de vue sur identity coming out.",
            "J'aime la direction que prend cette discussion sur identity coming out.",
        ],
    },
    "IMMIGRATION_RESPONSES": {
        "en": [
            "Noted - I'll keep that in mind as we talk about immigration.",
            "Feel free to tell me more about immigration whenever you like.",
            "There's always more to say about immigration.",
        ],
        "sw": [
            "Ningeweza kuendelea kuzungumza kuhusu immigration kwa muda.",
            "Asante kwa kushiriki - immigration inafaa kuzungumziwa.",
        ],
        "fr": [
            "On n'a pas encore tout dit sur immigration - quoi d'autre ?",
            "C'est un bon point de vue sur immigration.",
        ],
    },
    "DISABILITY_ACCESSIBILITY_RESPONSES": {
        "en": [
            "I don't think we've fully covered disability accessibility yet - what else is on your mind?",
            "Thanks for sharing that - disability accessibility is worth talking through.",
            "There's always more to say about disability accessibility.",
        ],
        "sw": [
            "Jisikie huru kunieleza zaidi kuhusu disability accessibility wakati wowote.",
            "Napenda mwelekeo wa mazungumzo haya kuhusu disability accessibility.",
        ],
        "fr": [
            "Je pourrais continuer à parler de disability accessibility un moment.",
            "J'aime la direction que prend cette discussion sur disability accessibility.",
        ],
    },
    "MENSTRUAL_HEALTH_RESPONSES": {
        "en": [
            "I could keep chatting about menstrual health for a while.",
            "That's interesting, tell me a bit more about menstrual health.",
            "I like where this menstrual health conversation is headed.",
        ],
        "sw": [
            "Kuna mengi zaidi ya kusema kuhusu menstrual health.",
            "Hilo ni jambo zuri kuhusu menstrual health.",
        ],
        "fr": [
            "On n'a pas encore tout dit sur menstrual health - quoi d'autre ?",
            "Content que tu aies parlé de menstrual health - continue, j'écoute.",
        ],
    },
    "CHECKUP_VACCINE_RESPONSES": {
        "en": [
            "Glad you brought checkup vaccine up - keep going, I'm listening.",
            "Thanks for sharing that - checkup vaccine is worth talking through.",
            "Feel free to tell me more about checkup vaccine whenever you like.",
        ],
        "sw": [
            "Kuna mengi zaidi ya kusema kuhusu checkup vaccine.",
            "Hilo ni jambo zuri kuhusu checkup vaccine.",
        ],
        "fr": [
            "Il y a toujours plus à dire sur checkup vaccine.",
            "Merci d'avoir partagé ça - checkup vaccine mérite qu'on en parle.",
        ],
    },
    "CLIMATE_ANXIETY_RESPONSES": {
        "en": [
            "I could keep chatting about climate anxiety for a while.",
            "That's interesting, tell me a bit more about climate anxiety.",
            "There's always more to say about climate anxiety.",
        ],
        "sw": [
            "Ningeweza kuendelea kuzungumza kuhusu climate anxiety kwa muda.",
            "Asante kwa kushiriki - climate anxiety inafaa kuzungumziwa.",
        ],
        "fr": [
            "J'aime la direction que prend cette discussion sur climate anxiety.",
            "N'hésite pas à m'en dire plus sur climate anxiety quand tu veux.",
        ],
    },
    "AI_TECHNOLOGY_FEAR_RESPONSES": {
        "en": [
            "Feel free to tell me more about ai technology fear whenever you like.",
            "That's a good angle on ai technology fear, honestly.",
            "That's interesting, tell me a bit more about ai technology fear.",
        ],
        "sw": [
            "Nafurahi umetaja ai technology fear - endelea, nasikiliza.",
            "Bado hatujamaliza kuzungumza kuhusu ai technology fear - kuna nini kingine?",
        ],
        "fr": [
            "Il y a toujours plus à dire sur ai technology fear.",
            "J'aime la direction que prend cette discussion sur ai technology fear.",
        ],
    },
    "REMOTE_LEARNING_RESPONSES": {
        "en": [
            "Noted - I'll keep that in mind as we talk about remote learning.",
            "That's a good angle on remote learning, honestly.",
            "Feel free to tell me more about remote learning whenever you like.",
        ],
        "sw": [
            "Jisikie huru kunieleza zaidi kuhusu remote learning wakati wowote.",
            "Asante kwa kushiriki - remote learning inafaa kuzungumziwa.",
        ],
        "fr": [
            "Content que tu aies parlé de remote learning - continue, j'écoute.",
            "Il y a toujours plus à dire sur remote learning.",
        ],
    },
    "HOBBY_CLUB_RESPONSES": {
        "en": [
            "There's always more to say about hobby club.",
            "Glad you brought hobby club up - keep going, I'm listening.",
            "I like where this hobby club conversation is headed.",
        ],
        "sw": [
            "Hilo ni jambo zuri kuhusu hobby club.",
            "Kuna mengi zaidi ya kusema kuhusu hobby club.",
        ],
        "fr": [
            "Content que tu aies parlé de hobby club - continue, j'écoute.",
            "Je pourrais continuer à parler de hobby club un moment.",
        ],
    },
    "SNEEZE_HICCUP_RESPONSES": {
        "en": [
            "There's always more to say about sneeze hiccup.",
            "Glad you brought sneeze hiccup up - keep going, I'm listening.",
            "Thanks for sharing that - sneeze hiccup is worth talking through.",
        ],
        "sw": [
            "Asante kwa kushiriki - sneeze hiccup inafaa kuzungumziwa.",
            "Ningeweza kuendelea kuzungumza kuhusu sneeze hiccup kwa muda.",
        ],
        "fr": [
            "Merci d'avoir partagé ça - sneeze hiccup mérite qu'on en parle.",
            "N'hésite pas à m'en dire plus sur sneeze hiccup quand tu veux.",
        ],
    },
    "HANDEDNESS_RESPONSES": {
        "en": [
            "That's interesting, tell me a bit more about handedness.",
            "Feel free to tell me more about handedness whenever you like.",
            "Noted - I'll keep that in mind as we talk about handedness.",
        ],
        "sw": [
            "Nafurahi umetaja handedness - endelea, nasikiliza.",
            "Hilo ni jambo zuri kuhusu handedness.",
        ],
        "fr": [
            "Il y a toujours plus à dire sur handedness.",
            "C'est un bon point de vue sur handedness.",
        ],
    },
    "ASTROLOGY_ZODIAC_RESPONSES": {
        "en": [
            "Thanks for sharing that - astrology zodiac is worth talking through.",
            "I like where this astrology zodiac conversation is headed.",
            "Noted - I'll keep that in mind as we talk about astrology zodiac.",
        ],
        "sw": [
            "Bado hatujamaliza kuzungumza kuhusu astrology zodiac - kuna nini kingine?",
            "Nafurahi umetaja astrology zodiac - endelea, nasikiliza.",
        ],
        "fr": [
            "Il y a toujours plus à dire sur astrology zodiac.",
            "Content que tu aies parlé de astrology zodiac - continue, j'écoute.",
        ],
    },
    "PERSONALITY_TYPE_RESPONSES": {
        "en": [
            "Thanks for sharing that - personality type is worth talking through.",
            "That's interesting, tell me a bit more about personality type.",
            "I don't think we've fully covered personality type yet - what else is on your mind?",
        ],
        "sw": [
            "Bado hatujamaliza kuzungumza kuhusu personality type - kuna nini kingine?",
            "Nafurahi umetaja personality type - endelea, nasikiliza.",
        ],
        "fr": [
            "J'aime la direction que prend cette discussion sur personality type.",
            "On n'a pas encore tout dit sur personality type - quoi d'autre ?",
        ],
    },
    "LUCKY_SUPERSTITION_RESPONSES": {
        "en": [
            "There's always more to say about lucky superstition.",
            "Noted - I'll keep that in mind as we talk about lucky superstition.",
            "I could keep chatting about lucky superstition for a while.",
        ],
        "sw": [
            "Asante kwa kushiriki - lucky superstition inafaa kuzungumziwa.",
            "Napenda mwelekeo wa mazungumzo haya kuhusu lucky superstition.",
        ],
        "fr": [
            "On n'a pas encore tout dit sur lucky superstition - quoi d'autre ?",
            "C'est un bon point de vue sur lucky superstition.",
        ],
    },
    "FAVORITE_SEASON_RESPONSES": {
        "en": [
            "That's interesting, tell me a bit more about favorite season.",
            "That's a good angle on favorite season, honestly.",
            "Feel free to tell me more about favorite season whenever you like.",
        ],
        "sw": [
            "Asante kwa kushiriki - favorite season inafaa kuzungumziwa.",
            "Napenda mwelekeo wa mazungumzo haya kuhusu favorite season.",
        ],
        "fr": [
            "Content que tu aies parlé de favorite season - continue, j'écoute.",
            "On n'a pas encore tout dit sur favorite season - quoi d'autre ?",
        ],
    },
    "IDEAL_VACATION_RESPONSES": {
        "en": [
            "Thanks for sharing that - ideal vacation is worth talking through.",
            "There's always more to say about ideal vacation.",
            "Feel free to tell me more about ideal vacation whenever you like.",
        ],
        "sw": [
            "Kuna mengi zaidi ya kusema kuhusu ideal vacation.",
            "Napenda mwelekeo wa mazungumzo haya kuhusu ideal vacation.",
        ],
        "fr": [
            "Content que tu aies parlé de ideal vacation - continue, j'écoute.",
            "On n'a pas encore tout dit sur ideal vacation - quoi d'autre ?",
        ],
    },
    "FIRST_IMPRESSION_RESPONSES": {
        "en": [
            "That's a good angle on first impression, honestly.",
            "Thanks for sharing that - first impression is worth talking through.",
            "Noted - I'll keep that in mind as we talk about first impression.",
        ],
        "sw": [
            "Nafurahi umetaja first impression - endelea, nasikiliza.",
            "Asante kwa kushiriki - first impression inafaa kuzungumziwa.",
        ],
        "fr": [
            "N'hésite pas à m'en dire plus sur first impression quand tu veux.",
            "Content que tu aies parlé de first impression - continue, j'écoute.",
        ],
    },
    "BUCKET_LIST_RESPONSES": {
        "en": [
            "I could keep chatting about bucket list for a while.",
            "That's interesting, tell me a bit more about bucket list.",
            "Feel free to tell me more about bucket list whenever you like.",
        ],
        "sw": [
            "Bado hatujamaliza kuzungumza kuhusu bucket list - kuna nini kingine?",
            "Ningeweza kuendelea kuzungumza kuhusu bucket list kwa muda.",
        ],
        "fr": [
            "N'hésite pas à m'en dire plus sur bucket list quand tu veux.",
            "On n'a pas encore tout dit sur bucket list - quoi d'autre ?",
        ],
    },
    "GIVE_COMPLIMENT_TO_BOT_RESPONSES": {
        "en": [
            "Feel free to tell me more about give compliment to bot whenever you like.",
            "There's always more to say about give compliment to bot.",
            "I could keep chatting about give compliment to bot for a while.",
        ],
        "sw": [
            "Napenda mwelekeo wa mazungumzo haya kuhusu give compliment to bot.",
            "Nafurahi umetaja give compliment to bot - endelea, nasikiliza.",
        ],
        "fr": [
            "Content que tu aies parlé de give compliment to bot - continue, j'écoute.",
            "Merci d'avoir partagé ça - give compliment to bot mérite qu'on en parle.",
        ],
    },
    "CONVERSATION_STARTER_RESPONSES": {
        "en": [
            "There's always more to say about conversation starter.",
            "Glad you brought conversation starter up - keep going, I'm listening.",
            "Feel free to tell me more about conversation starter whenever you like.",
        ],
        "sw": [
            "Napenda mwelekeo wa mazungumzo haya kuhusu conversation starter.",
            "Jisikie huru kunieleza zaidi kuhusu conversation starter wakati wowote.",
        ],
        "fr": [
            "Je pourrais continuer à parler de conversation starter un moment.",
            "Il y a toujours plus à dire sur conversation starter.",
        ],
    },
    "CONVERSATIONAL_FILLER_STARTER_RESPONSES": {
        "en": [
            "That's interesting, tell me a bit more about conversational filler starter.",
            "There's always more to say about conversational filler starter.",
            "I like where this conversational filler starter conversation is headed.",
        ],
        "sw": [
            "Ningeweza kuendelea kuzungumza kuhusu conversational filler starter kwa muda.",
            "Jisikie huru kunieleza zaidi kuhusu conversational filler starter wakati wowote.",
        ],
        "fr": [
            "N'hésite pas à m'en dire plus sur conversational filler starter quand tu veux.",
            "Je pourrais continuer à parler de conversational filler starter un moment.",
        ],
    },
    "LUCK_FORTUNE_RESPONSES": {
        "en": [
            "Glad you brought luck fortune up - keep going, I'm listening.",
            "Noted - I'll keep that in mind as we talk about luck fortune.",
            "There's always more to say about luck fortune.",
        ],
        "sw": [
            "Ningeweza kuendelea kuzungumza kuhusu luck fortune kwa muda.",
            "Napenda mwelekeo wa mazungumzo haya kuhusu luck fortune.",
        ],
        "fr": [
            "N'hésite pas à m'en dire plus sur luck fortune quand tu veux.",
            "On n'a pas encore tout dit sur luck fortune - quoi d'autre ?",
        ],
    },
    "RELAXING_WEEKEND_RESPONSES": {
        "en": [
            "Feel free to tell me more about relaxing weekend whenever you like.",
            "I like where this relaxing weekend conversation is headed.",
            "Glad you brought relaxing weekend up - keep going, I'm listening.",
        ],
        "sw": [
            "Hilo ni jambo zuri kuhusu relaxing weekend.",
            "Nafurahi umetaja relaxing weekend - endelea, nasikiliza.",
        ],
        "fr": [
            "Merci d'avoir partagé ça - relaxing weekend mérite qu'on en parle.",
            "Il y a toujours plus à dire sur relaxing weekend.",
        ],
    },
    "PROUD_OF_SOMEONE_RESPONSES": {
        "en": [
            "That's a good angle on proud of someone, honestly.",
            "Glad you brought proud of someone up - keep going, I'm listening.",
            "Noted - I'll keep that in mind as we talk about proud of someone.",
        ],
        "sw": [
            "Kuna mengi zaidi ya kusema kuhusu proud of someone.",
            "Nafurahi umetaja proud of someone - endelea, nasikiliza.",
        ],
        "fr": [
            "Il y a toujours plus à dire sur proud of someone.",
            "J'aime la direction que prend cette discussion sur proud of someone.",
        ],
    },
    "FORGIVENESS_RESPONSES": {
        "en": [
            "Noted - I'll keep that in mind as we talk about forgiveness.",
            "That's interesting, tell me a bit more about forgiveness.",
            "I don't think we've fully covered forgiveness yet - what else is on your mind?",
        ],
        "sw": [
            "Jisikie huru kunieleza zaidi kuhusu forgiveness wakati wowote.",
            "Ningeweza kuendelea kuzungumza kuhusu forgiveness kwa muda.",
        ],
        "fr": [
            "Content que tu aies parlé de forgiveness - continue, j'écoute.",
            "J'aime la direction que prend cette discussion sur forgiveness.",
        ],
    },
    "MISTAKE_LEARNING_RESPONSES": {
        "en": [
            "I could keep chatting about mistake learning for a while.",
            "Glad you brought mistake learning up - keep going, I'm listening.",
            "Noted - I'll keep that in mind as we talk about mistake learning.",
        ],
        "sw": [
            "Nafurahi umetaja mistake learning - endelea, nasikiliza.",
            "Ningeweza kuendelea kuzungumza kuhusu mistake learning kwa muda.",
        ],
        "fr": [
            "Content que tu aies parlé de mistake learning - continue, j'écoute.",
            "N'hésite pas à m'en dire plus sur mistake learning quand tu veux.",
        ],
    },
    "TRUST_ISSUES_RESPONSES": {
        "en": [
            "Thanks for sharing that - trust issues is worth talking through.",
            "I don't think we've fully covered trust issues yet - what else is on your mind?",
            "I could keep chatting about trust issues for a while.",
        ],
        "sw": [
            "Jisikie huru kunieleza zaidi kuhusu trust issues wakati wowote.",
            "Asante kwa kushiriki - trust issues inafaa kuzungumziwa.",
        ],
        "fr": [
            "C'est un bon point de vue sur trust issues.",
            "Merci d'avoir partagé ça - trust issues mérite qu'on en parle.",
        ],
    },
    "SETTING_BOUNDARIES_RESPONSES": {
        "en": [
            "That's interesting, tell me a bit more about setting boundaries.",
            "I like where this setting boundaries conversation is headed.",
            "Thanks for sharing that - setting boundaries is worth talking through.",
        ],
        "sw": [
            "Hilo ni jambo zuri kuhusu setting boundaries.",
            "Napenda mwelekeo wa mazungumzo haya kuhusu setting boundaries.",
        ],
        "fr": [
            "C'est un bon point de vue sur setting boundaries.",
            "Content que tu aies parlé de setting boundaries - continue, j'écoute.",
        ],
    },
    "SELF_CARE_ROUTINE_RESPONSES": {
        "en": [
            "Thanks for sharing that - self care routine is worth talking through.",
            "That's a good angle on self care routine, honestly.",
            "Feel free to tell me more about self care routine whenever you like.",
        ],
        "sw": [
            "Asante kwa kushiriki - self care routine inafaa kuzungumziwa.",
            "Hilo ni jambo zuri kuhusu self care routine.",
        ],
        "fr": [
            "J'aime la direction que prend cette discussion sur self care routine.",
            "Je pourrais continuer à parler de self care routine un moment.",
        ],
    },
    "FEELING_STUCK_RESPONSES": {
        "en": [
            "I could keep chatting about feeling stuck for a while.",
            "Noted - I'll keep that in mind as we talk about feeling stuck.",
            "That's interesting, tell me a bit more about feeling stuck.",
        ],
        "sw": [
            "Nafurahi umetaja feeling stuck - endelea, nasikiliza.",
            "Ningeweza kuendelea kuzungumza kuhusu feeling stuck kwa muda.",
        ],
        "fr": [
            "C'est un bon point de vue sur feeling stuck.",
            "Je pourrais continuer à parler de feeling stuck un moment.",
        ],
    },
    "LIFE_TRANSITION_RESPONSES": {
        "en": [
            "That's interesting, tell me a bit more about life transition.",
            "Glad you brought life transition up - keep going, I'm listening.",
            "I like where this life transition conversation is headed.",
        ],
        "sw": [
            "Bado hatujamaliza kuzungumza kuhusu life transition - kuna nini kingine?",
            "Jisikie huru kunieleza zaidi kuhusu life transition wakati wowote.",
        ],
        "fr": [
            "Merci d'avoir partagé ça - life transition mérite qu'on en parle.",
            "Je pourrais continuer à parler de life transition un moment.",
        ],
    },
    "HOPE_FUTURE_RESPONSES": {
        "en": [
            "Feel free to tell me more about hope future whenever you like.",
            "Noted - I'll keep that in mind as we talk about hope future.",
            "There's always more to say about hope future.",
        ],
        "sw": [
            "Kuna mengi zaidi ya kusema kuhusu hope future.",
            "Nafurahi umetaja hope future - endelea, nasikiliza.",
        ],
        "fr": [
            "Il y a toujours plus à dire sur hope future.",
            "Je pourrais continuer à parler de hope future un moment.",
        ],
    },
    "GRATITUDE_PRACTICE_RESPONSES": {
        "en": [
            "Glad you brought gratitude practice up - keep going, I'm listening.",
            "I like where this gratitude practice conversation is headed.",
            "Thanks for sharing that - gratitude practice is worth talking through.",
        ],
        "sw": [
            "Nafurahi umetaja gratitude practice - endelea, nasikiliza.",
            "Ningeweza kuendelea kuzungumza kuhusu gratitude practice kwa muda.",
        ],
        "fr": [
            "Je pourrais continuer à parler de gratitude practice un moment.",
            "On n'a pas encore tout dit sur gratitude practice - quoi d'autre ?",
        ],
    },
}

# Merge the supplementary phrasing above into each corresponding bank. This
# runs once, at import time, appending rather than replacing, so every
# hand-written line from Section 8 is kept exactly as-is.
for _bank_name, _extra_langs in _EXTRA_RESPONSE_PHRASES.items():
    _bank = globals().get(_bank_name)
    if isinstance(_bank, dict):
        for _lang, _phrases in _extra_langs.items():
            _bank.setdefault(_lang, []).extend(_phrases)


# ==============================================================================
