"""Section 8-EXT4: Sheng supplement (merged into Swahili)
Part of the response-bank data set - see chatbot_modules/13_response_banks_loader.py.
"""

# SECTION 8-EXT4: SHENG SUPPLEMENT (Nairobi urban slang, merged into "sw")
# ==============================================================================
#
# Sheng is a real, living urban vernacular spoken mainly by younger
# people in Nairobi and other Kenyan cities - a fluid mix of Swahili,
# English, and other local languages with its own slang vocabulary
# ("poa", "niaje", "buda", "manzi", "noma"), NOT a separate standardized
# language with its own grammar rules the way Swahili/English/French
# are. Because of that, it's added here as a SUPPLEMENT merged into the
# existing "sw" bank (same mechanism as the casual-tone supplement
# above) rather than as a fourth top-level language - a message
# entirely in heavy Sheng would still be detected as Swahili by
# LanguageDetector (Section 7B), since Sheng vocabulary overlaps
# Swahili more than English or French. Every line here is hand-written
# and kept to common, widely-recognized Sheng terms rather than
# hyper-local slang that shifts estate to estate and year to year.
_SHENG_PHRASES = {
    "GREETING_RESPONSES": {
        "sw": [
            "Niaje!",
            "Sasa! Uko aje?",
            "Mambo vipi buda",
            "Fiti sana, wewe je?",
            "Vipi msee, freshi?",
            "Sasa je, story yako?",
            "Niaje mrembo/buda, mambo?",
        ],
    },
    "FAREWELL_RESPONSES": {
        "sw": [
            "Sawa buda, tuonane!",
            "Poa, baadaye msee",
            "Niko out, tuonane hivi punde",
            "Sasa tutaongea baadaye, chill",
            "Ok sawa, kesho tena",
        ],
    },
    "THANKS_RESPONSES": {
        "sw": [
            "Asante sana buda",
            "Poa sana, niko grateful",
            "Eh, asante kabisa msee",
            "Sawa tu, si stress",
        ],
    },
    "HOW_ARE_YOU_RESPONSES": {
        "sw": [
            "Poa tu msee",
            "Fiti kabisa, freshi",
            "Niko sawa tu, wewe je?",
            "Noma kidogo lakini poa",
            "Chill tu, story yangu iko sawa",
        ],
    },
    "UNKNOWN_RESPONSES": {
        "sw": [
            "Aiii sijaelewa vizuri msee",
            "Eh sijapata, sema tena",
            "Si nimeget vibaya, explain kidogo",
            "Wacha nifikirie, sijamake sense yake",
        ],
    },
}

for _bank_name, _extra_langs in _SHENG_PHRASES.items():
    _bank = globals().get(_bank_name)
    if isinstance(_bank, dict):
        for _lang, _phrases in _extra_langs.items():
            _bank.setdefault(_lang, []).extend(_phrases)




# ==============================================================================
