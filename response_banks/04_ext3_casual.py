"""Section 8-EXT3: casual human-tone supplement (hand-written)
Part of the response-bank data set - see chatbot_modules/13_response_banks_loader.py.
"""

# SECTION 8-EXT3: CASUAL, HUMAN-TONE SUPPLEMENT (hand-written, not templated)
# ==============================================================================
#
# Unlike the two templated supplements above (8-EXT/8-EXT2), every line
# here is hand-written, one at a time, specifically to sound like an
# actual casual text conversation rather than a polished assistant
# reply: shorter, looser punctuation, occasional lowercase starts,
# more reactive ("lol", "wait really?", trailing "...") - the
# register real people actually text in, versus the more composed
# tone of the original Section 8 banks. Written after reviewing (and
# NOT copying - these are original lines in a similar style, not
# reproductions of anyone's actual messages) the casual, code-switched
# conversational rhythm that also shaped Section 14's n-gram model.
_CASUAL_TONE_PHRASES = {
    "GREETING_RESPONSES": {
        "en": [
            "heyyy what's up",
            "oh hey! didn't see you there",
            "hii how's it going",
            "yo! what's new",
            "hey hey, good timing",
            "ayy there you are",
            "hi hi, what's good",
        ],
    },
    "FAREWELL_RESPONSES": {
        "en": [
            "aight, later!",
            "okay bye byeee",
            "see ya, take care",
            "alright, catch you later",
            "bye for now!",
            "okay okay, go on then, bye",
        ],
    },
    "THANKS_RESPONSES": {
        "en": [
            "aww no worries at all",
            "haha anytime",
            "of course, don't even worry about it",
            "yeah yeah, all good",
            "np np",
        ],
    },
    "HOW_ARE_YOU_RESPONSES": {
        "en": [
            "eh, can't complain",
            "surviving lol, you?",
            "pretty good actually, you?",
            "same old same old, how about you",
            "not bad not bad",
        ],
    },
    "UNKNOWN_RESPONSES": {
        "en": [
            "wait what do you mean",
            "hmm not sure I follow, say more?",
            "lol what",
            "okay that lost me a bit",
            "huh, come again?",
        ],
    },
}

for _bank_name, _extra_langs in _CASUAL_TONE_PHRASES.items():
    _bank = globals().get(_bank_name)
    if isinstance(_bank, dict):
        for _lang, _phrases in _extra_langs.items():
            _bank.setdefault(_lang, []).extend(_phrases)


# ==============================================================================
