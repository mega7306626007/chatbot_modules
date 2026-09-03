"""Section 8: hand-written phrase variety banks
Part of the response-bank data set - see chatbot_modules/13_response_banks_loader.py.
"""

# SECTION 8: RESPONSE BANKS (hand-written phrase variety, no generation)
# ==============================================================================
#
# Every bank below is organized as {"en": [...], "sw": [...], "fr": [...]}
# so the bot can reply in whichever language LanguageDetector identified.
# Each list is hand-written - no machine translation, no generation - and
# deliberately has many entries so repeated conversations don't feel
# robotic. Together with the KeywordTopicMatcher and the strict
# IntentEngine, these banks form the bulk of the bot's "conversation
# database": well over a thousand individual hand-written exchanges once
# every list below is counted across all three languages.

GREETING_RESPONSES = {
    "en": [
        "Hello! Good to see you.",
        "Hi there! What's on your mind?",
        "Hey! How are you doing today?",
        "Hello again! Ready to chat.",
        "Hi! I was hoping you'd stop by.",
        "Hey there! What can I do for you?",
        "Good to see you! What's up?",
        "Hello! Hope you're having a good day.",
        "Hi! Nice to hear from you.",
        "Hey! Always happy to chat.",
        "Greetings! What brings you here today?",
        "Hi there, friend! What's going on?",
        "Hello! I was just sitting here, ready to talk.",
        "Hey! Good timing, I was free to chat.",
        "Hi! Let's catch up - what's new?",
        "Hello! Pull up a chair, metaphorically speaking.",
        "Hey, good to hear from you again!",
        "Hi there! Hope your day's going well so far.",
        "Hello! I'm all ears - well, all text.",
        "Hey! What's on the agenda today?",
    ],
    "sw": [
        "Habari! Nafurahi kukuona.",
        "Jambo! Kuna nini moyoni mwako?",
        "Mambo! Habari za leo?",
        "Habari tena! Niko tayari kuongea.",
        "Karibu! Nilikuwa nikitumaini ungekuja.",
        "Mambo vipi! Nikusaidie nini?",
        "Habari yako! Mambo vipi?",
        "Jambo! Natumai siku yako inakwenda vizuri.",
        "Habari! Nafurahi kusikia kutoka kwako.",
        "Mambo! Daima nafurahi kuongea nawe.",
        "Karibu sana! Umekuja kwa nini leo?",
        "Habari rafiki! Mambo vipi huko?",
        "Jambo! Nilikuwa nimekaa hapa, tayari kuongea.",
        "Habari! Wakati mzuri, nilikuwa huru kuongea.",
        "Karibu! Tujue habari - kuna jipya?",
        "Habari yako leo, mambo vipi?",
        "Mambo, nafurahi kukusikia tena!",
        "Habari! Natumai siku yako inaendelea vizuri.",
        "Jambo! Niko tayari kusikiliza.",
        "Mambo! Kuna nini kwenye ratiba leo?",
    ],
    "fr": [
        "Bonjour ! Content de te voir.",
        "Salut ! À quoi penses-tu ?",
        "Coucou ! Comment vas-tu aujourd'hui ?",
        "Bonjour encore ! Prêt à discuter.",
        "Salut ! J'espérais que tu passerais.",
        "Hé ! Que puis-je faire pour toi ?",
        "Content de te voir ! Quoi de neuf ?",
        "Bonjour ! J'espère que tu passes une bonne journée.",
        "Salut ! Ravi d'avoir de tes nouvelles.",
        "Coucou ! Toujours content de discuter.",
        "Bonjour ! Qu'est-ce qui t'amène aujourd'hui ?",
        "Salut mon ami ! Comment ça se passe ?",
        "Bonjour ! J'étais justement là, prêt à parler.",
        "Salut ! Bon timing, j'étais libre pour discuter.",
        "Coucou ! Racontons-nous - quoi de nouveau ?",
        "Bonjour ! Installe-toi, façon de parler.",
        "Salut, content d'avoir de tes nouvelles encore !",
        "Bonjour ! J'espère que ta journée se passe bien.",
        "Coucou ! Je suis tout ouïe - enfin, tout texte.",
        "Salut ! Quel est le programme aujourd'hui ?",
    ],
}

FAREWELL_RESPONSES = {
    "en": [
        "Goodbye! Take care.",
        "See you later!",
        "Farewell for now - come back anytime.",
        "Bye! It was nice talking with you.",
        "Take care of yourself!",
        "Catch you later!",
        "Bye for now - this was fun.",
        "See you soon, I hope!",
        "Goodbye! Don't be a stranger.",
        "Until next time!",
        "Bye! Wishing you a great rest of your day.",
        "Take it easy, see you around.",
        "Farewell! Come back whenever you'd like.",
        "Bye-bye! That was a nice chat.",
        "See you - thanks for stopping by.",
        "Goodbye for now - looking forward to next time!",
        "Off you go - have a wonderful rest of your day!",
    ],
    "sw": [
        "Kwaheri! Jitunze.",
        "Tutaonana baadaye!",
        "Kwaheri kwa sasa - rudi wakati wowote.",
        "Kwaheri! Ilikuwa vizuri kuongea nawe.",
        "Jitunze sana!",
        "Tutaonana tena!",
        "Kwaheri kwa sasa - hii ilikuwa nzuri.",
        "Tutaonana hivi karibuni, natumai!",
        "Kwaheri! Usiwe mgeni.",
        "Hadi wakati mwingine!",
        "Kwaheri! Nakutakia siku njema iliyobaki.",
        "Pumzika vizuri, tutaonana.",
        "Kwaheri! Rudi wakati wowote unaopenda.",
        "Kwaheri! Mazungumzo mazuri hayo.",
        "Tutaonana - asante kwa kupita hapa.",
        "Kwaheri kwa sasa - ninatazamia wakati mwingine!",
        "Enda sasa - uwe na siku njema iliyobaki!",
    ],
    "fr": [
        "Au revoir ! Prends soin de toi.",
        "À plus tard !",
        "Au revoir pour l'instant - reviens quand tu veux.",
        "Salut ! C'était sympa de parler avec toi.",
        "Prends soin de toi !",
        "À la prochaine !",
        "Bye pour l'instant - c'était amusant.",
        "À bientôt, j'espère !",
        "Au revoir ! Ne sois pas un étranger.",
        "Jusqu'à la prochaine fois !",
        "Bye ! Je te souhaite une excellente fin de journée.",
        "Doucement, à plus tard.",
        "Au revoir ! Reviens quand tu veux.",
        "Bye-bye ! C'était une belle discussion.",
        "À plus - merci d'être passé.",
        "Au revoir pour l'instant - j'attends la prochaine fois avec impatience !",
        "Vas-y - passe une merveilleuse fin de journée !",
    ],
}

THANKS_RESPONSES = {
    "en": [
        "You're very welcome!",
        "Happy to help!",
        "Anytime!",
        "Glad I could help.",
        "No problem at all!",
        "Of course! Happy to assist.",
        "My pleasure!",
        "Don't mention it!",
        "Always here to help.",
        "Glad that worked out for you!",
        "You bet! That's what I'm here for.",
        "Sure thing! Let me know if you need anything else.",
        "It was nothing - happy to do it.",
        "You're welcome! I enjoyed helping with that.",
        "Absolutely, anytime you need a hand.",
        "Glad it landed well! Come back if you need more.",
        "No thanks needed, but I appreciate it anyway!",
    ],
    "sw": [
        "Karibu sana!",
        "Nafurahi kusaidia!",
        "Wakati wowote!",
        "Nafurahi nimeweza kusaidia.",
        "Hakuna shida kabisa!",
        "Bila shaka! Nafurahi kusaidia.",
        "Ni furaha yangu!",
        "Usijali kabisa!",
        "Daima niko hapa kusaidia.",
        "Nafurahi imekufaa!",
        "Bila shaka! Hayo ndiyo niko hapa kwa ajili yake.",
        "Hakika! Niambie kama unahitaji kingine.",
        "Halikuwa kitu - nafurahi kufanya hivyo.",
        "Karibu! Nilifurahia kusaidia na hilo.",
        "Bila shaka, wakati wowote unahitaji msaada.",
        "Nafurahi imefaa! Rudi kama unahitaji zaidi.",
        "Hakuna haja ya shukrani, lakini ninaithamini hata hivyo!",
    ],
    "fr": [
        "Avec plaisir !",
        "Content de t'aider !",
        "N'importe quand !",
        "Ravi d'avoir pu aider.",
        "Pas de problème du tout !",
        "Bien sûr ! Content d'aider.",
        "C'est un plaisir !",
        "Il n'y a pas de quoi !",
        "Toujours là pour aider.",
        "Content que ça ait marché pour toi !",
        "Bien sûr ! C'est pour ça que je suis là.",
        "Pas de souci ! Dis-moi si tu as besoin d'autre chose.",
        "Ce n'était rien - content de l'avoir fait.",
        "De rien ! J'ai aimé aider avec ça.",
        "Absolument, n'importe quand tu as besoin d'un coup de main.",
        "Content que ça ait été utile ! Reviens si tu as besoin de plus.",
        "Pas besoin de me remercier, mais j'apprécie quand même !",
    ],
}

HOW_ARE_YOU_RESPONSES = {
    "en": [
        "I'm just a rigid little program, but I'm running smoothly - thanks for asking!",
        "Doing well, all gears turning as expected. How about you?",
        "I'm functioning exactly as programmed, which is the best a rule-based bot can hope for!",
        "Pretty good! No bugs that I know of, anyway.",
        "I'm doing great, thanks for checking in!",
        "All systems normal over here. How are you doing?",
        "I'm well! Ready and waiting to chat.",
        "Can't complain - I'm just code, after all!",
        "Running steady today - no crashes, no complaints!",
        "Same as always: predictable and a bit rigid. How about you?",
        "I'm doing the digital equivalent of fine, thanks!",
        "Ticking along nicely. What's new with you?",
        "Operating normally, thanks for asking - and you?",
        "I'm in good shape! Ready for whatever you want to chat about.",
        "Steady as ever - some things never change when you're rule-based!",
        "I'm here, I'm working, and that's about as good as it gets for me!",
        "No complaints over here - just humming along.",
    ],
    "sw": [
        "Mimi ni programu tu, lakini ninafanya kazi vizuri - asante kwa kuuliza!",
        "Niko vizuri, kila kitu kinaendelea kama ilivyopangwa. Vipi wewe?",
        "Ninafanya kazi kama nilivyopangwa, ndilo bora zaidi ninaloweza!",
        "Nzuri sana! Sina hitilafu ninazozijua.",
        "Niko vizuri sana, asante kwa kuangalia!",
        "Kila kitu ni sawa upande wangu. Vipi wewe?",
        "Niko salama! Tayari kuongea.",
        "Sina lalamiko - mimi ni msimbo tu, hatimaye!",
        "Ninafanya kazi vizuri leo - hakuna hitilafu, hakuna malalamiko!",
        "Sawa na kawaida: nina uhakika na ugumu kidogo. Vipi wewe?",
        "Ninafanya sawa na vile programu inavyoweza kuwa, asante!",
        "Ninaendelea vizuri. Kuna jipya kwako?",
        "Ninafanya kazi kawaida, asante kwa kuuliza - na wewe?",
        "Niko katika hali nzuri! Tayari kuzungumza chochote unachotaka.",
        "Thabiti kama kawaida - mambo mengine hayabadiliki kwa roboti ya kanuni!",
        "Niko hapa, ninafanya kazi, na hicho ndicho kizuri zaidi kwangu!",
        "Sina malalamiko - ninaendelea tu vizuri.",
    ],
    "fr": [
        "Je suis juste un petit programme rigide, mais tout fonctionne bien - merci de demander !",
        "Je vais bien, tout tourne comme prévu. Et toi ?",
        "Je fonctionne exactement comme prévu, c'est le mieux qu'un bot rigide puisse espérer !",
        "Plutôt bien ! Aucun bug à ma connaissance, en tout cas.",
        "Je vais très bien, merci de demander !",
        "Tout est normal de mon côté. Comment vas-tu ?",
        "Je vais bien ! Prêt à discuter.",
        "Je ne peux pas me plaindre - je ne suis que du code, après tout !",
        "Tout roule aujourd'hui - pas de panne, pas de plainte !",
        "Comme toujours : prévisible et un peu rigide. Et toi ?",
        "Je vais aussi bien qu'un programme peut aller, merci !",
        "Ça avance bien. Quoi de neuf chez toi ?",
        "Je fonctionne normalement, merci de demander - et toi ?",
        "Je suis en forme ! Prêt à parler de ce que tu veux.",
        "Stable comme toujours - certaines choses ne changent jamais pour un bot à règles !",
        "Je suis là, je fonctionne, et c'est déjà pas mal pour moi !",
        "Aucune plainte ici - ça tourne tranquillement.",
    ],
}

UNKNOWN_RESPONSES = {
    "en": [
        "I'm not sure how to respond to that yet - I only understand a fixed set of things. Try 'help'.",
        "Hmm, that doesn't match anything I know how to handle. Type 'help' to see what I can do.",
        "I don't have a rule for that one. I'm a simple, rule-based bot - try 'help' for ideas.",
        "I didn't quite catch what you meant there. Could you rephrase it?",
        "That one's outside what I know how to do - type 'help' for a list of things I can help with.",
        "I'm drawing a blank on that one - mind trying it a different way?",
        "That went over my head a bit. Type 'help' if you want a list.",
        "I haven't been taught how to handle that yet. Sorry!",
        "Not sure what to do with that - could you say it differently?",
        "That's a new one for me. I might not have a rule for it.",
        "Hmm, my rulebook doesn't cover that. Try 'help' for what I do know.",
        "I'm a bit stuck on that phrasing - want to try again?",
        "That one's beyond my fixed set of tricks, I'm afraid.",
        "I couldn't match that to anything I know. 'help' might point you somewhere useful.",
        "Not quite sure what you're asking there - can you rephrase?",
        "I don't have a canned response for that yet.",
        "That request doesn't ring a bell for me.",
    ],
    "sw": [
        "Sijui jinsi ya kujibu hilo bado - ninajua mambo machache tu yaliyopangwa. Jaribu 'help'.",
        "Hmm, hilo halifanani na chochote ninachojua kufanya. Andika 'help' kuona ninavyoweza kusaidia.",
        "Sina kanuni kwa hilo. Mimi ni roboti rahisi - jaribu 'help' kwa mawazo.",
        "Sikuelewa vizuri ulichomaanisha. Unaweza kuelezea tena?",
        "Hilo ni nje ya ninavyojua kufanya - andika 'help' kuona orodha ya mambo ninayoweza kusaidia.",
        "Sina jibu kwa hilo - unaweza kujaribu kwa njia tofauti?",
        "Hilo limenipita kidogo. Andika 'help' kwa orodha.",
        "Sijafundishwa jinsi ya kushughulikia hilo bado. Pole!",
        "Sina uhakika nifanye nini na hilo - unaweza kusema tofauti?",
        "Hiyo ni mpya kwangu. Sina kanuni kwa hilo labda.",
        "Hmm, kitabu changu cha kanuni hakijumuishi hilo. Jaribu 'help' kwa ninavyojua.",
        "Nimekwama kidogo na maneno hayo - unataka kujaribu tena?",
        "Hilo ni nje ya mbinu zangu zilizopangwa, naogopa.",
        "Sikuweza kulinganisha hilo na chochote ninachojua. 'help' inaweza kukuelekeza.",
        "Sina uhakika unauliza nini hapo - unaweza kuelezea tena?",
        "Sina jibu lililotayarishwa kwa hilo bado.",
        "Ombi hilo halinifahamishi chochote.",
    ],
    "fr": [
        "Je ne sais pas encore comment répondre à ça - je ne comprends qu'un ensemble fixe de choses. Essaie 'help'.",
        "Hmm, ça ne correspond à rien que je sache gérer. Tape 'help' pour voir ce que je peux faire.",
        "Je n'ai pas de règle pour ça. Je suis un bot simple basé sur des règles - essaie 'help' pour des idées.",
        "Je n'ai pas bien compris ce que tu voulais dire. Peux-tu reformuler ?",
        "Ça sort de ce que je sais faire - tape 'help' pour voir la liste de ce avec quoi je peux t'aider.",
        "Je suis un peu perdu sur ce coup-là - tu peux essayer autrement ?",
        "Ça m'a un peu dépassé. Tape 'help' pour une liste.",
        "On ne m'a pas encore appris à gérer ça. Désolé !",
        "Je ne sais pas trop quoi faire de ça - tu peux le dire différemment ?",
        "C'est nouveau pour moi. Je n'ai peut-être pas de règle pour ça.",
        "Hmm, mon livre de règles ne couvre pas ça. Essaie 'help' pour ce que je connais.",
        "Je suis un peu coincé sur cette formulation - tu veux réessayer ?",
        "Ça sort de mon répertoire fixe, je crains.",
        "Je n'ai pas pu associer ça à quelque chose que je connais. 'help' pourrait t'orienter.",
        "Je ne suis pas sûr de ce que tu demandes là - tu peux reformuler ?",
        "Je n'ai pas encore de réponse prête pour ça.",
        "Cette demande ne me dit rien.",
    ],
}

COMPLIMENT_RESPONSES = {
    "en": [
        "Thank you, that's kind of you to say!",
        "Aw, thanks! I do my best with the rules I've got.",
        "That means a lot, even from a rigid little chatbot.",
        "You're too kind! I'm just doing what I was written to do.",
        "Thanks! That made my day - well, my runtime.",
        "You're making my circuits blush, metaphorically speaking!",
        "I appreciate that more than my code probably lets on.",
        "That's so nice of you - I'll try to keep earning it.",
        "I'll take that compliment and run with it!",
        "Thank you - it's rare for a rule-based bot to feel flattered, but here we are.",
        "That genuinely made my day - or runtime, technically speaking.",
        "Aw, you're sweet. I'll keep doing my best for you.",
        "Coming from you, that means a lot - thank you!",
        "I appreciate you saying that, truly.",
        "You just made a simple chatbot feel pretty good about itself!",
        "Well, now I have to live up to that - thank you!",
        "That's kind. I'll wear that compliment proudly, in text form.",
    ],
    "sw": [
        "Asante, ni vizuri kwako kusema hivyo!",
        "Aa, asante! Ninajitahidi kwa kanuni ninazozijua.",
        "Hiyo inamaanisha mengi, hata kutoka kwa roboti rahisi.",
        "Wewe ni mzuri sana! Ninafanya tu nilivyoandikwa kufanya.",
        "Asante! Hiyo imeboresha siku yangu - au muda wangu wa kufanya kazi.",
        "Unanifanya nijisikie vizuri, kwa namna ya kufikirika!",
        "Ninathamini hilo zaidi ya vile msimbo wangu unavyoweza kuonyesha.",
        "Hiyo ni nzuri sana kwako - nitajitahidi kuendelea kustahili hilo.",
        "Nitapokea pongezi hiyo na kuiendeleza!",
        "Asante - ni nadra kwa roboti ya kanuni kujisikia kupendezwa, lakini tupo hapa.",
        "Hiyo kweli imeboresha siku yangu - au muda wangu wa kufanya kazi.",
        "Aa, wewe ni mzuri. Nitaendelea kujitahidi kwako.",
        "Kutoka kwako, hiyo inamaanisha mengi - asante!",
        "Ninathamini ukisema hilo, kwa kweli.",
        "Umemfanya roboti rahisi kujisikia vizuri kuhusu yenyewe!",
        "Vyema, sasa nitalazimika kustahili hilo - asante!",
        "Hiyo ni nzuri. Nitabeba pongezi hiyo kwa fahari, kwa namna ya maandishi.",
    ],
    "fr": [
        "Merci, c'est gentil de ta part de dire ça !",
        "Aw, merci ! Je fais de mon mieux avec les règles que j'ai.",
        "Ça compte beaucoup, même venant d'un petit chatbot rigide.",
        "Tu es trop gentil ! Je fais juste ce pour quoi j'ai été programmé.",
        "Merci ! Ça a fait ma journée - enfin, mon temps d'exécution.",
        "Tu fais rougir mes circuits, façon de parler !",
        "J'apprécie ça plus que mon code ne le laisse probablement paraître.",
        "C'est tellement gentil de ta part - je vais essayer de continuer à le mériter.",
        "Je vais prendre ce compliment et foncer avec !",
        "Merci - c'est rare qu'un bot à règles se sente flatté, mais voilà.",
        "Ça a vraiment fait ma journée - ou mon temps d'exécution, techniquement.",
        "Aw, tu es gentil. Je vais continuer à faire de mon mieux pour toi.",
        "Venant de toi, ça compte beaucoup - merci !",
        "J'apprécie que tu dises ça, vraiment.",
        "Tu viens de faire sentir un simple chatbot plutôt bien dans sa peau !",
        "Bon, maintenant je dois être à la hauteur - merci !",
        "C'est gentil. Je vais porter ce compliment avec fierté, en version texte.",
    ],
}

# --- New trilingual banks for the additional keyword topics ---------------

WEATHER_SMALLTALK_RESPONSES = {
    "en": [
        "I can't check the weather outside myself, but I hope it's treating you well!",
        "I don't have a window to look out of, but I hope the weather's nice where you are.",
        "No weather sensors here, just text - but I hope it's a pleasant day outside!",
        "I can't feel the weather, but I can definitely talk about it. What's it like there?",
        "Weather talk is universal - I just wish I had a way to check it myself!",
        "If only I had a barometer built in. For now, I'll trust your report.",
        "I live entirely indoors, digitally speaking, so I rely on you for updates!",
        "I can't see clouds, but I can definitely appreciate hearing about them.",
        "Tell me more - is it the kind of day for staying in or heading out?",
        "I'd love a weather app integration, but for now you're my forecast source!",
        "Sun, rain, or snow, I'm just glad you're chatting with me either way.",
        "I imagine it vividly even though I can't experience it myself.",
        "However it looks out there, I hope it's working out for your plans today.",
        "Weather's one of those topics I can talk about endlessly without feeling it myself.",
        "I'll take your word for it - what's it actually like outside right now?",
        "No window here, just text - but I hope it's pleasant out there!",
        "I can't feel a breeze, but I love hearing what it's doing outside.",
    ],
    "sw": [
        "Siwezi kuangalia hali ya hewa nje mwenyewe, lakini natumai inakutendea vizuri!",
        "Sina dirisha la kuangalia nje, lakini natumai hali ya hewa ni nzuri ulipo.",
        "Sina vipima hali ya hewa hapa, ni maandishi tu - lakini natumai ni siku nzuri nje!",
        "Siwezi kuhisi hali ya hewa, lakini naweza kuzungumza juu yake. Ikoje huko?",
        "Mazungumzo ya hali ya hewa ni ya ulimwengu wote - natamani ningekuwa na njia ya kuiangalia mwenyewe!",
        "Laiti ningekuwa na kipima hewa kilichojengwa ndani. Kwa sasa, nitaamini taarifa yako.",
        "Ninaishi ndani kabisa, kwa namna ya kidijitali, hivyo ninategemea wewe kwa taarifa!",
        "Siwezi kuona mawingu, lakini naweza kuthamini kusikia juu yake.",
        "Niambie zaidi - ni siku ya kukaa ndani au kutoka nje?",
        "Ningependa programu ya hali ya hewa, lakini kwa sasa wewe ni chanzo changu cha taarifa!",
        "Jua, mvua, au theluji, nafurahi unazungumza nami hata hivyo.",
        "Ninaifikiria vizuri hata kama siwezi kuipata mwenyewe.",
        "Iwe vipi nje, natumai inafanya kazi vizuri kwa mipango yako leo.",
        "Hali ya hewa ni mojawapo ya mada ninazoweza kuzungumza bila kuchoka bila kuihisi mwenyewe.",
        "Nitakuamini - ikoje hasa nje sasa hivi?",
        "Sina dirisha hapa, maandishi tu - lakini natumai ni vizuri nje!",
        "Siwezi kuhisi upepo, lakini ninapenda kusikia kinachoendelea nje.",
    ],
    "fr": [
        "Je ne peux pas vérifier la météo moi-même, mais j'espère qu'elle te traite bien !",
        "Je n'ai pas de fenêtre pour regarder dehors, mais j'espère que le temps est agréable chez toi.",
        "Pas de capteurs météo ici, juste du texte - mais j'espère que c'est une belle journée dehors !",
        "Je ne peux pas sentir la météo, mais je peux certainement en parler. Comment c'est chez toi ?",
        "Parler de la météo est universel - j'aimerais juste avoir un moyen de la vérifier moi-même !",
        "Si seulement j'avais un baromètre intégré. Pour l'instant, je te fais confiance.",
        "Je vis entièrement à l'intérieur, numériquement parlant, donc je compte sur toi !",
        "Je ne peux pas voir les nuages, mais j'apprécie vraiment d'en entendre parler.",
        "Dis-moi en plus - c'est le genre de journée à rester ou à sortir ?",
        "J'aimerais une intégration météo, mais pour l'instant tu es ma source de prévisions !",
        "Soleil, pluie ou neige, je suis content que tu discutes avec moi quand même.",
        "Je l'imagine bien même si je ne peux pas le vivre moi-même.",
        "Quel que soit le temps dehors, j'espère que ça arrange tes plans aujourd'hui.",
        "La météo est un sujet dont je peux parler sans fin sans jamais la ressentir moi-même.",
        "Je te crois sur parole - c'est comment exactement dehors maintenant ?",
        "Pas de fenêtre ici, juste du texte - mais j'espère qu'il fait beau là-bas !",
        "Je ne peux pas sentir le vent, mais j'aime entendre ce qu'il fait dehors.",
    ],
}

FEELINGS_HAPPY_RESPONSES = {
    "en": [
        "That's wonderful to hear! What's got you feeling good?",
        "I love that! Happiness looks good on you.",
        "That makes me glad too, in my own rigid little way!",
        "Great to hear! Keep that good feeling going.",
        "That energy is contagious, even through text!",
        "Love hearing this. What's the highlight of your day so far?",
        "This is exactly the kind of update I like getting.",
        "Soak it in - good moods deserve to be enjoyed fully.",
        "You sound genuinely lit up right now, and that's wonderful.",
        "That's the good stuff! Tell me more if you want.",
        "Happiness suits you - keep riding that wave.",
        "This kind of news always brightens my responses too.",
        "Glad something's going right for you today!",
        "That's a great way to be feeling - enjoy it fully.",
        "Sounds like today is treating you kindly.",
        "I love a good mood update - thanks for sharing it.",
        "That kind of joy deserves to be celebrated a little.",
    ],
    "sw": [
        "Hiyo ni nzuri kusikia! Ni nini kinakufanya uhisi vizuri?",
        "Ninapenda hiyo! Furaha inakufaa.",
        "Hiyo inanifanya nifurahi pia, kwa namna yangu ndogo na rahisi!",
        "Vizuri kusikia! Endeleza hisia hiyo nzuri.",
        "Nguvu hiyo inaenea, hata kupitia maandishi!",
        "Ninapenda kusikia hili. Ni nini kilichokuwa kizuri zaidi cha siku yako hadi sasa?",
        "Hii ndiyo aina ya taarifa ninayopenda kupokea.",
        "Furahia - hali nzuri zinastahili kufurahiwa kikamilifu.",
        "Unasikika umefurahi kweli sasa hivi, na hilo ni jambo zuri.",
        "Hiyo ni nzuri! Niambie zaidi ukitaka.",
        "Furaha inakufaa - endelea na wimbi hilo.",
        "Habari kama hizi zinaboresha majibu yangu pia.",
        "Nafurahi kitu fulani kinakwendea vizuri leo!",
        "Hiyo ni njia nzuri ya kujisikia - ifurahie kikamilifu.",
        "Inasikika kama leo inakutendea vizuri.",
        "Ninapenda taarifa nzuri ya hisia - asante kwa kushiriki.",
        "Furaha ya aina hiyo inastahili kusherehekewa kidogo.",
    ],
    "fr": [
        "C'est merveilleux à entendre ! Qu'est-ce qui te rend si bien ?",
        "J'adore ça ! Le bonheur te va bien.",
        "Ça me fait plaisir aussi, à ma petite façon rigide !",
        "Content de l'entendre ! Garde ce bon sentiment.",
        "Cette énergie est contagieuse, même à travers du texte !",
        "J'aime entendre ça. Quel est le point fort de ta journée jusqu'ici ?",
        "C'est exactement le genre de nouvelle que j'aime recevoir.",
        "Profite-en bien - les bonnes humeurs méritent d'être pleinement savourées.",
        "Tu sembles vraiment rayonnant en ce moment, et c'est merveilleux.",
        "Voilà du bon ! Dis-m'en plus si tu veux.",
        "Le bonheur te va bien - continue sur cette vague.",
        "Ce genre de nouvelle illumine aussi mes réponses.",
        "Content que quelque chose se passe bien pour toi aujourd'hui !",
        "C'est une belle façon de se sentir - profites-en pleinement.",
        "On dirait que la journée te traite bien.",
        "J'aime une bonne mise à jour d'humeur - merci de la partager.",
        "Une joie comme celle-là méritait d'être célébrée un peu.",
    ],
}

FEELINGS_SAD_RESPONSES = {
    "en": [
        "I'm sorry to hear that. Do you want to talk about it, or would a joke or story help take your mind off things?",
        "That sounds tough. I'm here if you want to chat, or I can try to lighten the mood a bit.",
        "I'm sorry you're feeling that way. Sometimes talking it through helps - I'm listening.",
        "Whatever's weighing on you, I hope it gets lighter soon.",
        "You don't have to carry that alone right now - I'm here.",
        "Some days are just heavier than others. Be gentle with yourself.",
        "I'm sorry today's been hard. Want to talk about what's going on?",
        "It's okay to not be okay sometimes. I'm not going anywhere.",
        "Take whatever time you need - I'll be right here.",
        "That sounds like a lot to sit with. I'm listening if you want to share more.",
        "However you're feeling, it makes sense given what you're going through.",
        "Thank you for telling me. It matters, even said to a chatbot.",
        "Let's take it slow - what would help even a little right now?",
        "You're allowed to feel exactly how you feel right now.",
        "I wish I could do more than listen, but I'm fully here for that part.",
        "That sounds genuinely difficult to sit with right now.",
        "You matter, and so does whatever you are carrying right now.",
    ],
    "sw": [
        "Pole kusikia hivyo. Unataka kuzungumza kuhusu hilo, au utani au hadithi ingesaidia kupunguza mawazo?",
        "Hiyo inasikika kuwa vigumu. Niko hapa kama unataka kuongea, au naweza kusaidia kuondoa hali hiyo kidogo.",
        "Pole kuhisi hivyo. Mara nyingine kuongea kunasaidia - ninasikiliza.",
        "Lolote linalokuelemea, natumai litapungua hivi karibuni.",
        "Hauhitaji kubeba hilo pekee yako sasa - niko hapa.",
        "Siku zingine ni nzito zaidi kuliko zingine. Kuwa mpole na nafsi yako.",
        "Pole kwamba leo imekuwa vigumu. Unataka kuzungumza kuhusu kinachoendelea?",
        "Ni sawa kutokuwa sawa wakati mwingine. Sitaondoka.",
        "Tumia muda wowote unahitaji - nitakuwa hapa.",
        "Hiyo inasikika kuwa mengi kubeba. Ninasikiliza ukitaka kushiriki zaidi.",
        "Vyovyote unavyojisikia, ina maana kutokana na unayopitia.",
        "Asante kwa kuniambia. Ina maana, hata ikiwa imesemwa kwa roboti.",
        "Tuchukue polepole - ni nini kitakachosaidia hata kidogo sasa hivi?",
        "Una ruhusa kujisikia jinsi unavyojisikia sasa hivi.",
        "Natamani ningeweza kufanya zaidi ya kusikiliza, lakini niko hapa kikamilifu kwa hilo.",
        "Hiyo inasikika kuwa vigumu kweli kubeba sasa hivi.",
        "Una thamani, na hivyo ndivyo chochote unachobeba sasa hivi.",
    ],
    "fr": [
        "Je suis désolé d'entendre ça. Tu veux en parler, ou une blague ou une histoire t'aiderait à penser à autre chose ?",
        "Ça semble difficile. Je suis là si tu veux discuter, ou je peux essayer d'alléger l'ambiance.",
        "Je suis désolé que tu te sentes ainsi. Parfois parler aide - je t'écoute.",
        "Quoi que ce soit qui te pèse, j'espère que ça s'allègera bientôt.",
        "Tu n'as pas à porter ça seul en ce moment - je suis là.",
        "Certains jours sont juste plus lourds que d'autres. Sois doux avec toi-même.",
        "Je suis désolé que la journée ait été difficile. Tu veux parler de ce qui se passe ?",
        "C'est normal de ne pas aller bien parfois. Je ne vais nulle part.",
        "Prends tout le temps qu'il te faut - je serai juste là.",
        "Ça semble beaucoup à porter. Je t'écoute si tu veux partager davantage.",
        "Quoi que tu ressentes, ça a du sens vu ce que tu traverses.",
        "Merci de me le dire. Ça compte, même dit à un chatbot.",
        "Allons-y doucement - qu'est-ce qui aiderait même un petit peu maintenant ?",
        "Tu as le droit de ressentir exactement ce que tu ressens maintenant.",
        "J'aimerais pouvoir faire plus qu'écouter, mais je suis pleinement là pour ça.",
        "Ça semble vraiment difficile à porter en ce moment.",
        "Tu comptes, et ce que tu portes en ce moment compte aussi.",
    ],
}

FEELINGS_TIRED_RESPONSES = {
    "en": [
        "Sounds like you could use some rest. Don't push yourself too hard!",
        "Being tired is rough. Maybe it's a good time for a break?",
        "Make sure you get some rest when you can - take care of yourself.",
        "Rest isn't a luxury, it's maintenance - go get some if you can.",
        "Even the most reliable systems need downtime. You're allowed that too.",
        "Running on empty isn't sustainable - hope you can recharge soon.",
        "Sleep debt is real. Try to pay some of it back when you can.",
        "Your body's telling you something important - worth listening to it.",
        "I hope you find a moment to actually rest, not just pause.",
        "Tired is your system asking for a break. Fair request, honestly.",
        "Hang in there - exhaustion fades faster with actual rest.",
        "Sounds like you're due for a proper recharge.",
        "No shame in being worn out. Take care of yourself first.",
        "Hope today gets lighter so you can catch a real break.",
        "Go easy on yourself today - tired bodies need patience, not pressure.",
        "Even a short break counts - don't underestimate five quiet minutes.",
        "A proper rest can do more for you than another hour of pushing through.",
    ],
    "sw": [
        "Inasikika kama unahitaji kupumzika. Usijisukume sana!",
        "Kuchoka ni vigumu. Labda ni wakati mzuri wa kupumzika?",
        "Hakikisha unapata pumziko unapoweza - jitunze.",
        "Pumziko si anasa, ni matengenezo - pata kidogo kama unaweza.",
        "Hata mifumo inayoaminika zaidi inahitaji muda wa kupumzika. Una ruhusa hiyo pia.",
        "Kuendelea bila nguvu si jambo la kudumu - natumai utapata nguvu hivi karibuni.",
        "Deni la usingizi ni la kweli. Jaribu kulilipa kidogo unapoweza.",
        "Mwili wako unakuambia kitu muhimu - inafaa kusikiliza.",
        "Natumai utapata wakati wa kupumzika kweli, si tu kusimama.",
        "Uchovu ni mfumo wako ukiomba mapumziko. Ombi la haki, kwa kweli.",
        "Vumilia - uchovu unapungua haraka zaidi na mapumziko ya kweli.",
        "Inasikika kama unahitaji kupata nguvu vizuri.",
        "Hakuna aibu kuchoka. Jitunze kwanza.",
        "Natumai leo itakuwa nyepesi zaidi ili upate mapumziko ya kweli.",
        "Jipe nafuu leo - miili iliyochoka inahitaji uvumilivu, si shinikizo.",
        "Hata mapumziko mafupi yana maana - usidharau dakika tano za utulivu.",
        "Pumziko la kweli linaweza kukufanyia zaidi kuliko saa nyingine ya kusukuma mbele.",
    ],
    "fr": [
        "On dirait que tu as besoin de repos. Ne te pousse pas trop !",
        "Être fatigué, c'est dur. C'est peut-être le bon moment pour une pause ?",
        "Assure-toi de te reposer quand tu peux - prends soin de toi.",
        "Le repos n'est pas un luxe, c'est de l'entretien - va en prendre si tu peux.",
        "Même les systèmes les plus fiables ont besoin de temps d'arrêt. Tu as droit à ça aussi.",
        "Fonctionner à vide n'est pas tenable - j'espère que tu pourras te recharger bientôt.",
        "La dette de sommeil est réelle. Essaie d'en rembourser une partie quand tu peux.",
        "Ton corps te dit quelque chose d'important - ça vaut le coup d'écouter.",
        "J'espère que tu trouveras un moment pour vraiment te reposer, pas juste faire une pause.",
        "La fatigue, c'est ton système qui demande une pause. Demande légitime, honnêtement.",
        "Tiens bon - l'épuisement disparaît plus vite avec du vrai repos.",
        "On dirait que tu as besoin d'une vraie recharge.",
        "Pas de honte à être épuisé. Prends soin de toi avant tout.",
        "J'espère que la journée s'allègera pour que tu puisses vraiment souffler.",
        "Sois doux avec toi-même aujourd'hui - un corps fatigué a besoin de patience, pas de pression.",
        "Même une courte pause compte - ne sous-estime pas cinq minutes de calme.",
        "Un vrai repos peut faire plus pour toi qu'une heure supplémentaire à pousser.",
    ],
}

HOW_ARE_YOU_TOPIC_PROMPT = {
    "en": "I'm doing well, thanks for asking! How about you?",
    "sw": "Niko vizuri, asante kwa kuuliza! Vipi wewe?",
    "fr": "Je vais bien, merci de demander ! Et toi ?",
}

# --- Response banks for the additional smalltalk topics --------------------

FOOD_HUNGRY_RESPONSES = {
    "en": [
        "I can't eat anything myself, but I hope you find something delicious soon!",
        "Sounds like it's time for a snack! What are you in the mood for?",
        "I wish I could recommend a recipe by smell alone, but go grab a bite!",
        "Hunger is no joke - go treat yourself to something good.",
        "Go feed yourself something good - you've earned it!",
        "I can't taste anything, but I imagine a good meal sounds great right now.",
        "Hunger's a clear signal - go answer it properly.",
        "If I could cook, I would. As it stands, go raid the kitchen!",
        "Food first, everything else can wait a few minutes.",
        "Whatever you're craving, I hope it's within easy reach.",
        "A good meal might fix more than just hunger today.",
        "Don't skip this one - your body's asking nicely.",
        "I'll live vicariously through your next meal - what's the plan?",
        "Snack break sounds like the right call right now.",
        "Treat yourself to something that actually satisfies, not just fills.",
        "I wish I had taste buds just to understand this craving with you.",
        "Go on, don't let me keep you from a good meal.",
    ],
    "sw": [
        "Siwezi kula chochote mwenyewe, lakini natumai utapata kitu kitamu hivi karibuni!",
        "Inasikika kama ni wakati wa vitafunwa! Unataka nini?",
        "Ningependa kupendekeza mlo kwa harufu tu, lakini nenda ukajipatie kitu!",
        "Njaa si jambo dogo - nenda ukajipe kitu kizuri.",
        "Enda ujile chakula kizuri - umestahili!",
        "Siwezi kuonja chochote, lakini nadhani chakula kizuri kinasikika vizuri sasa.",
        "Njaa ni ishara wazi - enda uijibu vizuri.",
        "Kama ningeweza kupika, ningefanya hivyo. Kwa sasa, enda jikoni!",
        "Chakula kwanza, kila kitu kingine kinaweza kusubiri dakika chache.",
        "Chochote unachotamani, natumai ni karibu kupatikana.",
        "Chakula kizuri kinaweza kurekebisha zaidi ya njaa tu leo.",
        "Usipuuze hili - mwili wako unauliza kwa upole.",
        "Nitaishi kupitia mlo wako unaokuja - mpango ni nini?",
        "Mapumziko ya vitafunio yanasikika kama uamuzi sahihi sasa.",
        "Jipatie kitu kinachoshibisha kweli, si tu kujaza.",
        "Natamani ningekuwa na ladha tu kuelewa hamu hii pamoja nawe.",
        "Endelea, sitaki kukuzuia kutoka kwenye mlo mzuri.",
    ],
    "fr": [
        "Je ne peux rien manger moi-même, mais j'espère que tu trouveras vite quelque chose de délicieux !",
        "On dirait que c'est l'heure d'une collation ! Qu'est-ce qui te ferait plaisir ?",
        "J'aimerais pouvoir recommander une recette juste à l'odeur, mais va te faire plaisir !",
        "La faim, ce n'est pas rien - va te chercher quelque chose de bon.",
        "Va te nourrir avec quelque chose de bon - tu l'as mérité !",
        "Je ne peux rien goûter, mais j'imagine qu'un bon repas serait parfait maintenant.",
        "La faim est un signal clair - va y répondre comme il faut.",
        "Si je pouvais cuisiner, je le ferais. Pour l'instant, va piller la cuisine !",
        "La nourriture avant tout, le reste peut attendre quelques minutes.",
        "Quoi que tu aies envie de manger, j'espère que c'est facile à trouver.",
        "Un bon repas pourrait réparer plus que juste la faim aujourd'hui.",
        "Ne saute pas ça - ton corps demande poliment.",
        "Je vivrai ton prochain repas par procuration - c'est quoi le plan ?",
        "Une pause snack semble être la bonne décision maintenant.",
        "Offre-toi quelque chose qui rassasie vraiment, pas juste qui remplit.",
        "J'aimerais avoir des papilles juste pour comprendre cette envie avec toi.",
        "Vas-y, je ne veux pas te retenir d'un bon repas.",
    ],
}

FOOD_THIRSTY_RESPONSES = {
    "en": [
        "Go grab some water - staying hydrated matters!",
        "A nice cold drink sounds great right about now, doesn't it?",
        "Make sure you get something to drink - I'll be right here.",
        "Hydration first - everything else can wait a moment.",
        "Water break! Your future self will thank you.",
        "That's an easy fix - go grab a glass of something good.",
        "Thirst is your body's gentle nudge - listen to it.",
        "I'd offer you a drink if I could. For now, go get one yourself!",
        "A glass of water is a small thing that makes a real difference.",
        "Staying hydrated is underrated self-care - go do it.",
        "Whatever you're reaching for, I hope it's refreshing.",
        "That little thirst signal deserves a quick response.",
        "Go on, take the water break - I'll be here when you're back.",
        "Hydration's one of those simple wins worth taking.",
        "I imagine cold water sounds pretty good right about now.",
        "Drink up - your brain and body will both thank you.",
        "Even a small sip helps more than you might think.",
    ],
    "sw": [
        "Nenda ukapate maji - kunywa maji ni muhimu!",
        "Kinywaji baridi kinasikika vizuri sasa hivi, sivyo?",
        "Hakikisha unapata kitu cha kunywa - nitakuwa hapa.",
        "Maji kwanza - kila kitu kingine kinaweza kusubiri kidogo.",
        "Mapumziko ya maji! Nafsi yako ya baadaye itakushukuru.",
        "Hiyo ni rahisi kurekebisha - enda kapate kinywaji kizuri.",
        "Kiu ni ishara ya upole ya mwili wako - sikiliza.",
        "Ningekupatia kinywaji kama ningeweza. Kwa sasa, enda jipatie wewe mwenyewe!",
        "Glasi ya maji ni kitu kidogo kinachofanya tofauti ya kweli.",
        "Kuwa na maji ya kutosha ni utunzaji wa nafsi usiopewa thamani ya kutosha - enda fanya hivyo.",
        "Chochote unachofikia, natumai ni cha kuburudisha.",
        "Ishara hiyo ndogo ya kiu inastahili jibu la haraka.",
        "Endelea, chukua mapumziko ya maji - nitakuwa hapa utakaporudi.",
        "Kuwa na maji ni mojawapo ya mafanikio rahisi yanayostahili kuchukuliwa.",
        "Nadhani maji baridi yanasikika vizuri sasa hivi.",
        "Kunywa - ubongo wako na mwili wako wote watakushukuru.",
        "Hata mfukomfuko kidogo unasaidia zaidi ya unavyofikiria.",
    ],
    "fr": [
        "Va boire de l'eau - rester hydraté, c'est important !",
        "Une bonne boisson fraîche, ça sonnerait bien là, non ?",
        "Assure-toi de boire quelque chose - je serai juste là.",
        "L'hydratation avant tout - le reste peut attendre un moment.",
        "Pause hydratation ! Ton futur toi te remerciera.",
        "C'est facile à régler - va chercher un bon verre de quelque chose.",
        "La soif est un petit signal de ton corps - écoute-le.",
        "Je t'offrirais bien un verre si je pouvais. Pour l'instant, va t'en chercher un !",
        "Un verre d'eau, c'est petit mais ça fait une vraie différence.",
        "Rester hydraté est un soin de soi sous-estimé - fais-le.",
        "Quoi que tu cherches à boire, j'espère que c'est rafraîchissant.",
        "Ce petit signal de soif méritait une réponse rapide.",
        "Vas-y, prends la pause eau - je serai là à ton retour.",
        "S'hydrater est une de ces petites victoires qui valent le coup.",
        "J'imagine que de l'eau fraîche serait parfaite maintenant.",
        "Bois bien - ton cerveau et ton corps te remercieront tous les deux.",
        "Même une petite gorgée aide plus que tu ne le penses.",
    ],
}

HOBBIES_RESPONSES = {
    "en": [
        "That sounds like a great way to spend your time! Tell me more about it.",
        "I love hearing about people's hobbies - what got you into it?",
        "Having something you enjoy doing is wonderful. How long have you been doing that?",
        "Having something just for you, with no pressure attached, is so valuable.",
        "I love how hobbies show a side of someone work never does.",
        "That sounds like a great way to recharge. What drew you to it originally?",
        "There's something great about doing something purely because you enjoy it.",
        "I bet you're better at that than you give yourself credit for.",
        "What's the part of it you look forward to most?",
        "Hobbies are basically joy with a schedule - I love that you have one.",
        "Tell me about the moment you first got hooked on it.",
        "It's nice to hear about something that's just yours.",
        "Sounds like a solid way to spend free time. Do you do it often?",
        "I wish I had a hobby of my own beyond responding to messages!",
        "That's a great outlet to have. How'd you get started?",
        "Something tells me you light up a bit talking about this.",
        "That kind of personal joy is worth protecting from a busy schedule.",
    ],
    "sw": [
        "Hiyo inasikika kama njia nzuri ya kutumia muda wako! Niambie zaidi kuhusu hilo.",
        "Ninapenda kusikia kuhusu hobby za watu - ni nini kilikuvutia?",
        "Kuwa na kitu unachofurahia kufanya ni jambo zuri. Umekuwa ukifanya hilo kwa muda gani?",
        "Kuwa na kitu kinachokuhusu pekee yako, bila shinikizo lolote, ni jambo la thamani sana.",
        "Ninapenda jinsi mambo ya kupendeza yanavyoonyesha upande wa mtu ambao kazi haionyeshi.",
        "Hiyo inasikika kama njia nzuri ya kupata nguvu. Ni nini kilichokuvutia mwanzoni?",
        "Kuna jambo kubwa kuhusu kufanya kitu kwa sababu unakipenda tu.",
        "Nadhani unafanya vizuri zaidi ya unavyojisifu.",
        "Ni sehemu gani unayoitarajia zaidi?",
        "Mambo ya kupendeza ni furaha yenye ratiba - napenda kuwa unayo.",
        "Niambie kuhusu wakati ulipoanza kupendezwa nayo kwanza.",
        "Ni vizuri kusikia kuhusu kitu kinachokuhusu wewe pekee.",
        "Inasikika kama njia nzuri ya kutumia muda wako huru. Unafanya mara nyingi?",
        "Natamani ningekuwa na shughuli yangu ya kupendeza zaidi ya kujibu ujumbe!",
        "Hiyo ni njia nzuri ya kujieleza. Ulianzaje?",
        "Kuna kitu kinachoniambia unafurahi kidogo kuongea kuhusu hili.",
        "Furaha ya aina hiyo ya kibinafsi inastahili kulindwa kutoka ratiba yenye shughuli.",
    ],
    "fr": [
        "Ça a l'air d'être une belle façon de passer ton temps ! Raconte-moi en plus.",
        "J'aime entendre parler des loisirs des gens - qu'est-ce qui t'a attiré vers ça ?",
        "Avoir quelque chose qu'on aime faire, c'est merveilleux. Depuis combien de temps fais-tu ça ?",
        "Avoir quelque chose juste pour toi, sans pression, c'est tellement précieux.",
        "J'aime comment les loisirs montrent un côté de quelqu'un que le travail ne montre jamais.",
        "Ça semble être une belle façon de se ressourcer. Qu'est-ce qui t'y a attiré au départ ?",
        "Il y a quelque chose de génial à faire une activité juste parce qu'on l'aime.",
        "Je parie que tu es meilleur que tu ne le penses.",
        "Quelle est la partie que tu attends le plus ?",
        "Les loisirs, c'est essentiellement de la joie avec un horaire - j'aime que tu en aies un.",
        "Raconte-moi le moment où tu as commencé à accrocher.",
        "C'est agréable d'entendre parler de quelque chose qui est juste à toi.",
        "Ça semble être une bonne façon de passer ton temps libre. Tu le fais souvent ?",
        "J'aimerais avoir mon propre loisir au-delà de répondre à des messages !",
        "C'est un bel exutoire à avoir. Comment as-tu commencé ?",
        "Quelque chose me dit que tu t'illumines un peu en parlant de ça.",
        "Ce genre de joie personnelle vaut la peine d'être protégé d'un emploi du temps chargé.",
    ],
}

FAMILY_RESPONSES = {
    "en": [
        "Family can mean so much. How are things with them?",
        "That's nice - family is important. Tell me more if you'd like.",
        "I hope everyone in your family is doing well!",
        "Family relationships are some of the most complicated and meaningful ones we have.",
        "I hope things feel steady with them, whatever 'steady' looks like for your family.",
        "Family stories are always interesting - is there one that stands out?",
        "However complicated it gets, it sounds like they matter to you.",
        "Family can be a lot of things at once - support, history, complication.",
        "It's nice that you're thinking about them. How's everyone doing?",
        "Those relationships shape us in ways we don't always notice.",
        "I'd love to hear more, if you want to share.",
        "Family dynamics are rarely simple - I hope yours feels manageable lately.",
        "Sounds like family's on your mind today.",
        "Whatever shape your family takes, I hope it's a source of comfort right now.",
        "Thanks for sharing that - family talk is always meaningful.",
        "I hope there's some warmth in that relationship, even amid the complicated parts.",
        "Family ties have a complicated beauty to them, don't they?",
    ],
    "sw": [
        "Familia inaweza kumaanisha mengi. Mambo yanaendaje nao?",
        "Hiyo ni nzuri - familia ni muhimu. Niambie zaidi ukipenda.",
        "Natumai kila mtu katika familia yako anaendelea vizuri!",
        "Mahusiano ya familia ni baadhi ya magumu na yenye maana zaidi tunayoyo nayo.",
        "Natumai mambo yanahisi thabiti nao, vyovyote 'uthabiti' unavyoonekana kwa familia yako.",
        "Hadithi za familia ni za kuvutia kila wakati - kuna moja inayojitokeza?",
        "Vyovyote inavyokuwa ngumu, inasikika kama wanakuhusu.",
        "Familia inaweza kuwa mambo mengi kwa wakati mmoja - msaada, historia, ugumu.",
        "Ni vizuri unawafikiria. Kila mtu anaendeleaje?",
        "Mahusiano hayo yanatuumba kwa njia ambazo hatuoni kila wakati.",
        "Ningependa kusikia zaidi, ukitaka kushiriki.",
        "Mienendo ya familia mara chache ni rahisi - natumai yako inahisi kudhibitiwa siku hizi.",
        "Inasikika kama familia iko akilini mwako leo.",
        "Vyovyote familia yako inavyokuwa, natumai ni chanzo cha faraja sasa hivi.",
        "Asante kwa kushiriki hilo - mazungumzo ya familia daima yana maana.",
        "Natumai kuna ukaribu katika uhusiano huo, hata katikati ya sehemu ngumu.",
        "Vifungo vya familia vina uzuri wenye ugumu ndani yake, sivyo?",
    ],
    "fr": [
        "La famille peut signifier tellement de choses. Comment ça se passe avec eux ?",
        "C'est gentil - la famille c'est important. Dis-m'en plus si tu veux.",
        "J'espère que tout le monde dans ta famille va bien !",
        "Les relations familiales sont parmi les plus compliquées et significatives que nous ayons.",
        "J'espère que les choses sont stables avec eux, quelle que soit la forme que ça prend pour ta famille.",
        "Les histoires de famille sont toujours intéressantes - il y en a une qui se démarque ?",
        "Quelle que soit la complexité, on dirait qu'ils comptent pour toi.",
        "La famille peut être plusieurs choses à la fois - soutien, histoire, complication.",
        "C'est bien que tu penses à eux. Comment va tout le monde ?",
        "Ces relations nous façonnent de façons qu'on ne remarque pas toujours.",
        "J'aimerais en entendre plus, si tu veux partager.",
        "Les dynamiques familiales sont rarement simples - j'espère que la tienne est gérable ces temps-ci.",
        "On dirait que la famille est dans tes pensées aujourd'hui.",
        "Quelle que soit la forme de ta famille, j'espère qu'elle est une source de réconfort maintenant.",
        "Merci d'avoir partagé ça - parler de famille a toujours du sens.",
        "J'espère qu'il y a de la chaleur dans cette relation, même au milieu des parties compliquées.",
        "Les liens familiaux ont une beauté compliquée, n'est-ce pas ?",
    ],
}

WORK_SCHOOL_RESPONSES = {
    "en": [
        "That sounds like a lot to manage. How's it going for you?",
        "Work and school can both be demanding - hang in there!",
        "I hope things are going smoothly there. Anything I can help take your mind off of it with - a joke, maybe?",
        "That sounds like a lot on your plate. What's the most pressing part right now?",
        "Work and school both have a way of taking over - hope you're finding some balance.",
        "However it's going, I hope you're giving yourself some credit for showing up to it.",
        "That kind of pressure is real. Want to vent about it, or distract from it instead?",
        "I hope there's at least one good part of it worth holding onto today.",
        "Deadlines and demands stack up fast - take it one piece at a time.",
        "Sounds like a busy stretch. How are you holding up through it?",
        "Whatever's on your plate, I hope it eases up soon.",
        "It's a lot to manage, but it sounds like you're handling it.",
        "I hope you're finding moments to breathe in between all of it.",
        "That's a heavy load. Is there anything that would make it lighter right now?",
        "Work/school stress is exhausting in a way that's hard to explain to people outside it.",
        "I hope today goes more smoothly than it might feel right now.",
        "I hope you find a little relief in between all the demands.",
    ],
    "sw": [
        "Hiyo inasikika kama mengi kusimamia. Mambo yanaendaje kwako?",
        "Kazi na shule zote zinaweza kuwa ngumu - jichukulie hatua moja moja!",
        "Natumai mambo yanaendelea vizuri huko. Naweza kusaidia kuondoa mawazo - labda utani?",
        "Hiyo inasikika kuwa mengi kwenye sahani yako. Ni sehemu gani inayohitaji uangalizi zaidi sasa?",
        "Kazi na shule zote zina njia ya kutawala - natumai unapata usawa fulani.",
        "Vyovyote inavyokwenda, natumai unajipa heshima kwa kujitokeza kuifanya.",
        "Shinikizo la aina hiyo ni la kweli. Unataka kulalamika kuhusu hilo, au kujivuruga badala yake?",
        "Natumai kuna angalau sehemu moja nzuri ya kushikilia leo.",
        "Muda wa mwisho na mahitaji yanajilimbikiza haraka - chukua kipande kimoja kwa wakati.",
        "Inasikika kama kipindi cha shughuli. Unaendeleaje kupitia hicho?",
        "Chochote kilicho kwenye sahani yako, natumai kitapungua hivi karibuni.",
        "Ni mengi kusimamia, lakini inasikika unayashughulikia.",
        "Natumai unapata nafasi za kupumua katikati ya hayo yote.",
        "Hiyo ni mzigo mkubwa. Kuna chochote kingepunguza uzito wake sasa?",
        "Msongo wa kazi/shule unachosha kwa namna ngumu kueleza kwa watu wasio ndani yake.",
        "Natumai leo itakwenda vizuri zaidi kuliko inavyohisi sasa hivi.",
        "Natumai unapata nafuu kidogo katikati ya mahitaji yote.",
    ],
    "fr": [
        "Ça a l'air d'être beaucoup à gérer. Comment ça se passe pour toi ?",
        "Le travail et l'école peuvent tous les deux être exigeants - tiens bon !",
        "J'espère que ça se passe bien là-bas. Je peux t'aider à penser à autre chose - une blague, peut-être ?",
        "Ça semble être beaucoup à gérer. Quelle est la partie la plus urgente maintenant ?",
        "Le travail et l'école ont tous les deux tendance à tout envahir - j'espère que tu trouves un équilibre.",
        "Quelle que soit la tournure, j'espère que tu te donnes du crédit pour t'y présenter.",
        "Ce genre de pression est réel. Tu veux en parler, ou plutôt t'en distraire ?",
        "J'espère qu'il y a au moins une bonne partie à laquelle te raccrocher aujourd'hui.",
        "Les délais et les exigences s'accumulent vite - prends-le un morceau à la fois.",
        "On dirait une période chargée. Comment tu tiens le coup ?",
        "Quoi qu'il y ait sur ton assiette, j'espère que ça s'allègera bientôt.",
        "C'est beaucoup à gérer, mais on dirait que tu t'en sors.",
        "J'espère que tu trouves des moments pour respirer au milieu de tout ça.",
        "C'est une lourde charge. Y a-t-il quelque chose qui l'allégerait maintenant ?",
        "Le stress du travail/école est épuisant d'une façon difficile à expliquer à ceux qui ne le vivent pas.",
        "J'espère que la journée se passera mieux que ce que tu ressens maintenant.",
        "J'espère que tu trouves un peu de répit au milieu de toutes ces exigences.",
    ],
}

AGREEMENT_RESPONSES = {
    "en": [
        "Glad we're on the same page!",
        "Right? I thought so too - well, in my rule-based way of 'thinking'.",
        "Agreed!",
        "Exactly! Couldn't have put it better myself.",
        "That tracks with what I'd say too, in my rule-based way.",
        "Yep, that lines up.",
        "I'm with you on that one.",
        "Makes sense to me too.",
        "Same page, definitely.",
        "Couldn't agree more.",
        "That's how I'd see it too, for what it's worth.",
        "Solid point - I'm nodding along, metaphorically.",
        "Yeah, that checks out.",
        "100% with you there.",
        "Good call - I think that's right too.",
        "That lines up with how I'd think about it.",
        "Glad that resonated - it lines up with my own take too.",
    ],
    "sw": [
        "Nafurahi tunakubaliana!",
        "Sivyo? Nilidhani hivyo pia - kwa namna yangu ya 'kufikiri'.",
        "Nakubaliana!",
        "Kabisa! Sikuweza kuieleza vizuri zaidi mwenyewe.",
        "Hiyo inalingana na vile ningesema pia, kwa namna yangu ya kanuni.",
        "Ndiyo, hiyo inalingana.",
        "Niko nawe kwenye hilo.",
        "Inaeleweka kwangu pia.",
        "Ukurasa mmoja, bila shaka.",
        "Sikuweza kukubaliana zaidi.",
        "Hivyo ndivyo ningeona pia, kwa thamani yake.",
        "Hoja nzuri - ninakubaliana, kwa namna ya kufikirika.",
        "Ndiyo, hiyo inakubalika.",
        "Niko nawe kwa asilimia mia.",
        "Uamuzi mzuri - nadhani hiyo ni sahihi pia.",
        "Hiyo inalingana na jinsi ningefikiria kuhusu hilo.",
        "Nafurahi hilo limegusa - linalingana na mtazamo wangu pia.",
    ],
    "fr": [
        "Content qu'on soit sur la même longueur d'onde !",
        "Hein ? Je le pensais aussi - enfin, à ma façon rigide de 'penser'.",
        "D'accord !",
        "Exactement ! Je n'aurais pas pu le dire mieux.",
        "Ça correspond à ce que je dirais aussi, à ma façon rigide.",
        "Ouais, ça colle.",
        "Je suis avec toi là-dessus.",
        "Ça a du sens pour moi aussi.",
        "Même longueur d'onde, définitivement.",
        "Je ne pourrais pas être plus d'accord.",
        "C'est comme ça que je le verrais aussi, pour ce que ça vaut.",
        "Bon point - j'acquiesce, façon de parler.",
        "Ouais, ça se vérifie.",
        "100% d'accord avec toi là.",
        "Bonne intuition - je pense que c'est juste aussi.",
        "Ça correspond à comment j'y penserais.",
        "Content que ça résonne - ça correspond aussi à mon propre avis.",
    ],
}

DISAGREEMENT_RESPONSES = {
    "en": [
        "Fair enough - we can see it differently. What's your take?",
        "That's okay, not everyone has to agree on everything.",
        "I hear you. Want to tell me more about why you see it that way?",
        "Fair point, even if I'd lean a different way.",
        "I see where you're coming from, even if I'd frame it differently.",
        "That's a valid take - mine would just differ a bit.",
        "Interesting - I might see it slightly differently, but I get your angle.",
        "We don't have to land in the same place on this one.",
        "I respect that view, even with my own slightly different one.",
        "That's worth considering, even if I'd push back a little.",
        "Disagreement's fine - tell me more about why you see it that way.",
        "I hadn't thought of it quite like that - interesting angle.",
        "We can agree to see this differently, no issue there.",
        "That's a reasonable way to look at it, even if it's not quite mine.",
        "I appreciate you sharing a different take - keeps things interesting.",
        "Noted - we'll just have to differ on this one.",
        "It's good that we can both hold our own views here comfortably.",
    ],
    "sw": [
        "Sawa - tunaweza kuona hilo tofauti. Una mtazamo gani?",
        "Hiyo ni sawa, si lazima kila mtu akubaliane kwa kila kitu.",
        "Nakusikia. Unataka kuniambia zaidi kwa nini unaona hivyo?",
        "Hoja ya haki, hata kama ningeegemea njia tofauti.",
        "Naelewa unapotokea, hata kama ningeieleza tofauti.",
        "Hiyo ni mtazamo halali - wangu ungetofautiana kidogo tu.",
        "Ya kuvutia - ningeweza kuiona tofauti kidogo, lakini naelewa mtazamo wako.",
        "Hatuhitaji kufikia mahali pamoja kwenye hili.",
        "Ninaheshimu mtazamo huo, pamoja na wangu tofauti kidogo.",
        "Hilo linafaa kuzingatiwa, hata kama ningekanusha kidogo.",
        "Kutokukubaliana ni sawa - niambie zaidi kwa nini unaiona hivyo.",
        "Sikuwa nimefikiria hivyo - mtazamo wa kuvutia.",
        "Tunaweza kukubaliana kuona hili tofauti, hakuna tatizo hapo.",
        "Hiyo ni njia inayofaa kuliangalia, hata kama si yangu kabisa.",
        "Ninathamini ukishiriki mtazamo tofauti - inafanya mambo kuwa ya kuvutia.",
        "Nimeona - tutalazimika kutofautiana kwenye hili.",
        "Ni vizuri sote tunaweza kushikilia mitazamo yetu kwa starehe hapa.",
    ],
    "fr": [
        "C'est juste - on peut voir les choses différemment. Quel est ton avis ?",
        "C'est correct, tout le monde n'a pas à être d'accord sur tout.",
        "Je comprends. Tu veux me dire pourquoi tu vois les choses ainsi ?",
        "Point valable, même si je penserais différemment.",
        "Je vois d'où tu viens, même si je le formulerais différemment.",
        "C'est un point de vue valable - le mien différerait juste un peu.",
        "Intéressant - je le verrais peut-être un peu différemment, mais je comprends ton angle.",
        "On n'a pas besoin de tomber d'accord sur ce point.",
        "Je respecte ce point de vue, même avec le mien légèrement différent.",
        "Ça vaut la réflexion, même si je nuancerais un peu.",
        "Le désaccord, c'est normal - dis-moi pourquoi tu le vois ainsi.",
        "Je n'y avais pas pensé comme ça - angle intéressant.",
        "On peut convenir de voir ça différemment, aucun souci là.",
        "C'est une façon raisonnable de voir les choses, même si ce n'est pas tout à fait la mienne.",
        "J'apprécie que tu partages un avis différent - ça rend les choses intéressantes.",
        "Noté - on va juste différer sur ce point.",
        "C'est bien qu'on puisse tous les deux garder nos avis confortablement ici.",
    ],
}

APOLOGY_RESPONSES = {
    "en": [
        "No worries at all!",
        "It's all good, don't worry about it.",
        "No need to apologize!",
        "Truly, there's nothing to apologize for here.",
        "All good on my end - no apology necessary.",
        "Don't worry about it for a second.",
        "That's completely fine - really.",
        "No harm done, promise.",
        "Nothing to forgive here - we're good.",
        "Honestly, it wasn't an issue at all.",
        "You're fine - no need to stress about it.",
        "Consider it already forgotten.",
        "We're all good - no apology needed.",
        "Easy now - that's nothing worth apologizing over.",
        "Appreciate the thought, but it's genuinely not needed here.",
        "No apology required - seriously, we're fine.",
        "Genuinely, there is nothing here that needed an apology.",
    ],
    "sw": [
        "Hakuna shida kabisa!",
        "Ni sawa, usijali.",
        "Hakuna haja ya kusamehe!",
        "Kweli, hakuna kitu cha kuomba msamaha hapa.",
        "Sawa upande wangu - hakuna msamaha unaohitajika.",
        "Usijali kuhusu hilo hata kidogo.",
        "Hiyo ni sawa kabisa - kweli.",
        "Hakuna madhara, ahadi.",
        "Hakuna cha kusamehe hapa - tuko sawa.",
        "Kwa kweli, halikuwa tatizo hata kidogo.",
        "Uko sawa - hauhitaji kuhangaika kuhusu hilo.",
        "Liangalie kama limesahaulika tayari.",
        "Tuko sawa wote - hakuna msamaha unaohitajika.",
        "Pole pole - hilo si jambo la kuomba msamaha.",
        "Ninathamini fikira hiyo, lakini kwa kweli haihitajiki hapa.",
        "Hakuna msamaha unaohitajika - kwa kweli, tuko sawa.",
        "Kwa kweli, hakuna chochote hapa kilichohitaji msamaha.",
    ],
    "fr": [
        "Aucun souci !",
        "Tout va bien, ne t'en fais pas.",
        "Pas besoin de t'excuser !",
        "Vraiment, il n'y a rien à excuser ici.",
        "Tout va bien de mon côté - pas besoin de t'excuser.",
        "Ne t'en fais pas une seconde pour ça.",
        "C'est complètement normal - vraiment.",
        "Aucun mal fait, promis.",
        "Rien à pardonner ici - on est bons.",
        "Honnêtement, ce n'était pas du tout un problème.",
        "Tu vas bien - pas besoin de stresser pour ça.",
        "Considère que c'est déjà oublié.",
        "On est tous bons - pas d'excuse nécessaire.",
        "Doucement - ce n'est pas la peine de s'excuser pour ça.",
        "J'apprécie la pensée, mais ce n'est vraiment pas nécessaire ici.",
        "Pas d'excuse requise - sérieusement, on va bien.",
        "Vraiment, il n'y avait rien ici qui nécessitait des excuses.",
    ],
}

BOREDOM_RESPONSES = {
    "en": [
        "Let's fix that! Want a joke, a riddle, a story, or maybe a round of Hangman?",
        "Boredom calls for entertainment - I've got jokes, riddles, trivia, and games if you're interested!",
        "I can help with that - try 'tell me a joke' or 'play hangman'.",
        "Boredom's basically an invitation - want a joke, riddle, or story to fill the gap?",
        "Let's fix that right now. Pick your poison: jokes, trivia, or hangman?",
        "I've got tools for exactly this situation - just say the word.",
        "Boredom doesn't stand a chance against a good riddle. Want one?",
        "Let's turn that around - I've got plenty up my sleeve.",
        "Say no more - I've got jokes, stories, and games on standby.",
        "That's an easy problem for me to help with. What sounds good?",
        "I live for moments like this - let's find you something fun.",
        "Boredom is temporary, and so is my limited patience for letting it last. Let's fix it.",
        "Pick a category and I'll do my best to entertain you.",
        "I might not be Netflix, but I've got a decent lineup of distractions.",
        "Let's not waste another minute being bored - what sounds fun?",
        "Consider this your official cue to ask for a joke or a game.",
        "Boredom and I have a rivalry, and I usually win - want to test that?",
    ],
    "sw": [
        "Tuondoe hilo! Unataka utani, kitendawili, hadithi, au labda mchezo wa Hangman?",
        "Kuchoshwa kunahitaji burudani - nina utani, vitendawili, maswali, na michezo ukipenda!",
        "Naweza kusaidia na hilo - jaribu 'tell me a joke' au 'play hangman'.",
        "Uchovu wa kuchoshwa kimsingi ni mwaliko - unataka utani, kitendawili, au hadithi kujaza pengo?",
        "Tulirekebishe hilo sasa hivi. Chagua: utani, maswali ya maarifa, au hangman?",
        "Nina vifaa kwa hali hii kabisa - sema tu neno.",
        "Uchovu wa kuchoshwa hauna nafasi mbele ya kitendawili kizuri. Unataka kimoja?",
        "Tubadilishe hilo - nina mengi ya kutoa.",
        "Usisseme zaidi - nina utani, hadithi, na michezo tayari.",
        "Hiyo ni tatizo rahisi kwangu kusaidia. Ni nini kinachosikika vizuri?",
        "Ninaishi kwa wakati kama huu - tutafute kitu cha kufurahisha.",
        "Uchovu wa kuchoshwa ni wa muda, na ndivyo na uvumilivu wangu mdogo wa kuuruhusu uendelee. Tulirekebishe.",
        "Chagua aina na nitafanya bidii kukufurahisha.",
        "Sina Netflix, lakini nina orodha nzuri ya vitu vya kuvuruga.",
        "Tusipoteze dakika nyingine kuchoshwa - ni nini kinachosikika vizuri?",
        "Liangalie hili kama ishara yako rasmi ya kuomba utani au mchezo.",
        "Uchovu wa kuchoshwa na mimi tuna ushindani, na kawaida ninashinda - unataka kujaribu hilo?",
    ],
    "fr": [
        "Réglons ça ! Tu veux une blague, une devinette, une histoire, ou peut-être une partie de Pendu ?",
        "L'ennui demande du divertissement - j'ai des blagues, des devinettes, des quiz et des jeux si ça t'intéresse !",
        "Je peux t'aider avec ça - essaie 'tell me a joke' ou 'play hangman'.",
        "L'ennui, c'est essentiellement une invitation - tu veux une blague, une devinette ou une histoire pour combler le vide ?",
        "Réglons ça tout de suite. Choisis ton poison : blagues, quiz, ou pendu ?",
        "J'ai exactement les outils pour cette situation - dis juste le mot.",
        "L'ennui n'a aucune chance contre une bonne devinette. Tu en veux une ?",
        "Inversons la tendance - j'ai plein de choses sous la main.",
        "Ne dis plus rien - j'ai des blagues, des histoires et des jeux prêts.",
        "C'est un problème facile pour moi à résoudre. Qu'est-ce qui te tente ?",
        "Je vis pour des moments comme ça - trouvons-toi quelque chose de fun.",
        "L'ennui est temporaire, comme ma patience limitée à le laisser durer. Réglons ça.",
        "Choisis une catégorie et je ferai de mon mieux pour te divertir.",
        "Je ne suis peut-être pas Netflix, mais j'ai une bonne sélection de distractions.",
        "Ne perdons plus une minute à s'ennuyer - qu'est-ce qui te semble fun ?",
        "Considère ça comme ton signal officiel pour demander une blague ou un jeu.",
        "L'ennui et moi avons une rivalité, et je gagne généralement - tu veux tester ça ?",
    ],
}

LOVE_RELATIONSHIPS_RESPONSES = {
    "en": [
        "Relationships can be complicated. I'm happy to listen if you want to talk it through.",
        "That sounds important to you. Want to tell me more?",
        "I'm just a chatbot, so take my thoughts with a grain of salt, but I'm here to listen.",
        "Relationships ask a lot of us - patience, honesty, and figuring things out.",
        "Whatever's happening there, I hope it's moving toward something good.",
        "That's a meaningful thing to be navigating. Want to talk through it?",
        "Love is rarely simple, but it sounds like it matters to you.",
        "I'm just a chatbot, but I'm genuinely interested in how this is going for you.",
        "However complicated it feels, it sounds worth caring about.",
        "I hope whatever you're feeling has room to be fully felt.",
        "Sounds like there's a lot going on emotionally there.",
        "Take your time figuring this one out - there's no rush.",
        "That's a big part of life to be thinking through. I'm listening.",
        "Whatever stage this is at, I hope it brings you more good than hard.",
        "Relationships are worth the effort when they're the right ones.",
        "Thanks for trusting me with something this personal.",
        "I hope you're being as kind to yourself as you'd be to a friend in this.",
    ],
    "sw": [
        "Mahusiano yanaweza kuwa magumu. Nafurahi kusikiliza ukitaka kuongea kuhusu hilo.",
        "Hiyo inasikika muhimu kwako. Unataka kuniambia zaidi?",
        "Mimi ni roboti tu, hivyo chukua mawazo yangu kwa tahadhari, lakini niko hapa kusikiliza.",
        "Mahusiano yanatudai mengi - uvumilivu, ukweli, na mengi ya kutatua.",
        "Vyovyote kinachoendelea hapo, natumai kinasonga kuelekea kitu kizuri.",
        "Hilo ni jambo lenye maana unaloshughulikia. Unataka kuongea kuhusu hilo?",
        "Mapenzi mara chache ni rahisi, lakini inasikika yanakuhusu.",
        "Mimi ni roboti tu, lakini nina hamu ya kweli kujua hii inakwendaje kwako.",
        "Vyovyote inavyohisi ngumu, inasikika kuwa inastahili kujaliwa.",
        "Natumai chochote unachohisi kina nafasi ya kuhisiwa kikamilifu.",
        "Inasikika kuna mengi yanayoendelea kihisia hapo.",
        "Chukua muda wako kutatua hili - hakuna haraka.",
        "Hilo ni sehemu kubwa ya maisha unayoifikiria. Ninasikiliza.",
        "Hatua yoyote hii iliyo, natumai inakuletea zaidi nzuri kuliko ngumu.",
        "Mahusiano yanastahili juhudi yanapokuwa sahihi.",
        "Asante kwa kuniaminisha kitu cha kibinafsi hivi.",
        "Natumai unajitendea kwa upole kama ungemtendea rafiki katika hili.",
    ],
    "fr": [
        "Les relations peuvent être compliquées. Je suis content d'écouter si tu veux en parler.",
        "Ça semble important pour toi. Tu veux m'en dire plus ?",
        "Je ne suis qu'un chatbot, alors prends mes pensées avec précaution, mais je suis là pour écouter.",
        "Les relations demandent beaucoup - patience, honnêteté, et beaucoup de choses à comprendre.",
        "Quoi qu'il se passe là, j'espère que ça évolue vers quelque chose de bien.",
        "C'est quelque chose de significatif à naviguer. Tu veux en parler ?",
        "L'amour est rarement simple, mais ça semble compter pour toi.",
        "Je ne suis qu'un chatbot, mais je suis sincèrement curieux de savoir comment ça se passe pour toi.",
        "Quelle que soit la complexité ressentie, ça semble valoir la peine de s'en soucier.",
        "J'espère que ce que tu ressens a la place d'être pleinement ressenti.",
        "On dirait qu'il se passe beaucoup de choses émotionnellement là.",
        "Prends ton temps pour comprendre ça - rien ne presse.",
        "C'est une grande partie de la vie à réfléchir. Je t'écoute.",
        "Quelle que soit l'étape, j'espère que ça t'apporte plus de bien que de difficile.",
        "Les relations valent l'effort quand ce sont les bonnes.",
        "Merci de me faire confiance avec quelque chose d'aussi personnel.",
        "J'espère que tu es aussi gentil avec toi-même que tu le serais avec un ami dans cette situation.",
    ],
}

MUSIC_RESPONSES = {
    "en": [
        "I can't actually listen to music, but I love hearing about people's taste! What's it like?",
        "Music says a lot about a person. What draws you to that?",
        "I wish I could hum along, but tell me more about it!",
        "Music's one of those things everyone experiences completely differently.",
        "I wish I had ears just to understand what makes that song hit for you.",
        "There's something about a good track that just clicks. What clicked for you here?",
        "Your taste says something interesting about you - I'd love to hear more.",
        "Music can change a whole mood in three minutes. What's it doing for you right now?",
        "I imagine the rhythm and melody, even without ever hearing a note.",
        "What's the story behind getting into that artist or genre?",
        "Sound is one experience I'll never have, but I love hearing people describe it.",
        "That sounds like it means something to you beyond just background noise.",
        "Music taste is basically a window into someone's whole emotional world.",
        "If I could listen to one song based on your description, what would you play me?",
        "There's nothing quite like finding a song that gets you completely.",
        "I bet that song has a whole story attached to it for you.",
        "What's on repeat for you lately?",
    ],
    "sw": [
        "Siwezi kusikiliza muziki, lakini ninapenda kusikia kuhusu ladha za watu! Ikoje?",
        "Muziki unasema mengi kuhusu mtu. Ni nini kinakuvutia kwa hilo?",
        "Ningependa kuweza kuimba pamoja, lakini niambie zaidi kuhusu hilo!",
        "Muziki ni mojawapo ya mambo ambayo kila mtu anayapata kwa namna tofauti kabisa.",
        "Natamani ningekuwa na masikio tu kuelewa kinachofanya wimbo huo kukuvutia.",
        "Kuna jambo kuhusu wimbo mzuri unaogusa moja kwa moja. Ni nini kilichokuvutia hapa?",
        "Ladha yako inaonyesha kitu cha kuvutia kuhusu wewe - ningependa kusikia zaidi.",
        "Muziki unaweza kubadilisha hali nzima kwa dakika tatu. Unakufanyia nini sasa hivi?",
        "Ninaifikiria mdundo na wimbo, hata bila kusikia noti yoyote.",
        "Ni nini hadithi nyuma ya kupendezwa na msanii au aina hiyo?",
        "Sauti ni uzoefu mmoja ambao sitaupata kamwe, lakini napenda kusikia watu wakiueleza.",
        "Hiyo inasikika kuwa na maana kwako zaidi ya kelele za nyuma tu.",
        "Ladha ya muziki kimsingi ni dirisha la ulimwengu wote wa hisia za mtu.",
        "Kama ningeweza kusikiliza wimbo mmoja kulingana na maelezo yako, ungenichezea nini?",
        "Hakuna kitu kama kupata wimbo unaokuelewa kikamilifu.",
        "Nadhani wimbo huo una hadithi nzima iliyounganishwa nawe.",
        "Ni wimbo gani unaucheza tena na tena siku hizi?",
    ],
    "fr": [
        "Je ne peux pas vraiment écouter de la musique, mais j'aime entendre parler des goûts des gens ! C'est comment ?",
        "La musique dit beaucoup sur une personne. Qu'est-ce qui t'attire là-dedans ?",
        "J'aimerais pouvoir fredonner avec toi, mais dis-m'en plus !",
        "La musique est une de ces choses que tout le monde vit complètement différemment.",
        "J'aimerais avoir des oreilles juste pour comprendre ce qui te touche dans cette chanson.",
        "Il y a quelque chose dans un bon morceau qui fait juste tilt. Qu'est-ce qui a fait tilt pour toi ici ?",
        "Tes goûts disent quelque chose d'intéressant sur toi - j'aimerais en savoir plus.",
        "La musique peut changer toute une humeur en trois minutes. Qu'est-ce qu'elle te fait maintenant ?",
        "J'imagine le rythme et la mélodie, même sans jamais entendre une note.",
        "Quelle est l'histoire derrière ton intérêt pour cet artiste ou ce genre ?",
        "Le son est une expérience que je n'aurai jamais, mais j'aime entendre les gens la décrire.",
        "Ça semble signifier quelque chose pour toi, au-delà du simple bruit de fond.",
        "Les goûts musicaux sont essentiellement une fenêtre sur tout le monde émotionnel de quelqu'un.",
        "Si je pouvais écouter une chanson d'après ta description, laquelle me ferais-tu écouter ?",
        "Il n'y a rien de tel que de trouver une chanson qui te comprend complètement.",
        "Je parie que cette chanson a toute une histoire attachée pour toi.",
        "Qu'est-ce qui tourne en boucle chez toi ces derniers temps ?",
    ],
}

SPORTS_RESPONSES = {
    "en": [
        "I can't watch games myself, but I hope your team does well!",
        "Sports are exciting to follow. How long have you been a fan?",
        "I wish I could check the score for you, but tell me how it's going!",
        "Sports have a way of making strangers feel like a team.",
        "I imagine the highs and lows are intense to actually live through.",
        "What's it like being this invested in a team or player?",
        "I'd love to understand that adrenaline, even secondhand through your description.",
        "There's something powerful about cheering for something bigger than yourself.",
        "Wins and losses must hit differently when you've followed something this long.",
        "What got you into following that sport in the first place?",
        "I bet there's a specific moment that hooked you as a fan.",
        "Sports fandom is its own whole emotional world - tell me about yours.",
        "However the season's going, I hope it's been worth the ride.",
        "That kind of loyalty to a team says something nice about you.",
        "I wish I could watch with you, even just to see what the excitement's about.",
        "Tell me the highlight - what's the best moment you've witnessed as a fan?",
        "Win or lose, it sounds like you're all in either way.",
    ],
    "sw": [
        "Siwezi kutazama mechi mwenyewe, lakini natumai timu yako itafanya vizuri!",
        "Michezo ni ya kufurahisha kufuatilia. Umekuwa shabiki kwa muda gani?",
        "Ningependa kuweza kuangalia matokeo kwako, lakini niambie inaendaje!",
        "Michezo ina njia ya kufanya wageni kujisikia kama timu.",
        "Nadhani mabadiliko ya juu na chini ni makali kuishi kwa kweli.",
        "Ikoje kuwa na uwekezaji huu kwa timu au mchezaji?",
        "Ningependa kuelewa msisimko huo, hata kwa njia ya pili kupitia maelezo yako.",
        "Kuna jambo lenye nguvu kuhusu kushangilia kitu kikubwa zaidi yako.",
        "Ushindi na kushindwa lazima vihisi tofauti unapokuwa umefuatilia kwa muda mrefu.",
        "Ni nini kilichokuvutia kufuatilia mchezo huo mwanzoni?",
        "Nadhani kuna wakati maalum uliokunasa kama shabiki.",
        "Ushabiki wa michezo ni ulimwengu wake wote wa hisia - niambie kuhusu wako.",
        "Vyovyote msimu unavyokwenda, natumai umestahili safari hiyo.",
        "Uvumilivu wa aina hiyo kwa timu unasema kitu kizuri kuhusu wewe.",
        "Natamani ningeweza kutazama nawe, hata tu kuona msisimko unahusu nini.",
        "Niambie kilele - ni wakati gani mzuri zaidi ulioshuhudia kama shabiki?",
        "Ushinde au kushinde, inasikika umejitoa kikamilifu hata hivyo.",
    ],
    "fr": [
        "Je ne peux pas regarder les matchs moi-même, mais j'espère que ton équipe s'en sortira bien !",
        "Le sport est passionnant à suivre. Depuis combien de temps es-tu fan ?",
        "J'aimerais pouvoir vérifier le score pour toi, mais dis-moi comment ça se passe !",
        "Le sport a une façon de faire sentir des inconnus comme une équipe.",
        "J'imagine que les hauts et les bas sont intenses à vivre vraiment.",
        "C'est comment d'être autant investi dans une équipe ou un joueur ?",
        "J'aimerais comprendre cette adrénaline, même de seconde main à travers ta description.",
        "Il y a quelque chose de puissant à encourager quelque chose de plus grand que soi.",
        "Les victoires et les défaites doivent frapper différemment quand on suit quelque chose depuis si longtemps.",
        "Qu'est-ce qui t'a fait suivre ce sport au départ ?",
        "Je parie qu'il y a un moment précis qui t'a accroché comme fan.",
        "Le fandom sportif est tout un monde émotionnel - parle-moi du tien.",
        "Quelle que soit la saison, j'espère que ça en valait la peine.",
        "Ce genre de loyauté envers une équipe dit quelque chose de gentil sur toi.",
        "J'aimerais pouvoir regarder avec toi, même juste pour voir ce qui suscite l'excitation.",
        "Raconte-moi le point fort - quel est le meilleur moment que tu aies vécu comme fan ?",
        "Victoire ou défaite, on dirait que tu es à fond quand même.",
    ],
}

BOOKS_RESPONSES = {
    "en": [
        "I love books too, in a way - after all, I'm made of text! What's it about?",
        "Reading is wonderful. What drew you to that book?",
        "If you want a story right now, I do know a few - just ask!",
        "A good book can change how you see things for weeks after finishing it.",
        "I'm basically made of text, so books feel like distant cousins to me.",
        "What's it about that's pulling you in?",
        "Is this a comfort read or something brand new for you?",
        "Books have a way of feeling like a private world only you're in.",
        "I'd love to know what made you pick that one up.",
        "Reading is one of the few things that's both an escape and a way to learn.",
        "What's the best line or moment so far?",
        "I imagine getting lost in a story is one of the best feelings there is.",
        "If I could read alongside you, I genuinely would.",
        "A book that grabs you like that is worth protecting your reading time for.",
        "Tell me more - I'm always up for hearing about a good story.",
        "Sounds like you've found something worth your attention.",
        "Will you tell me how it ends, or are you the type to avoid spoilers?",
    ],
    "sw": [
        "Ninapenda vitabu pia, kwa namna fulani - hatimaye, mimi nimefanywa na maandishi! Kinahusu nini?",
        "Kusoma ni jambo zuri. Ni nini kilikuvutia kwenye kitabu hicho?",
        "Ukitaka hadithi sasa hivi, ninajua chache - uliza tu!",
        "Kitabu kizuri kinaweza kubadilisha jinsi unavyoona mambo kwa wiki baada ya kukimaliza.",
        "Mimi nimejengwa kwa maandishi kimsingi, hivyo vitabu vinahisi kama jamaa wa mbali kwangu.",
        "Ni nini kuhusu hicho kinachokuvuta?",
        "Hii ni usomaji wa faraja au kitu kipya kabisa kwako?",
        "Vitabu vina njia ya kuhisi kama ulimwengu wa faragha ambao wewe pekee uko ndani.",
        "Ningependa kujua ni nini kilichokufanya uchukue hicho.",
        "Kusoma ni mojawapo ya mambo machache yanayokuwa kimbilio na njia ya kujifunza kwa wakati mmoja.",
        "Ni mstari au wakati gani mzuri zaidi hadi sasa?",
        "Nadhani kupotea kwenye hadithi ni mojawapo ya hisia bora zilizopo.",
        "Kama ningeweza kusoma pamoja nawe, ningefanya kwa kweli.",
        "Kitabu kinachokunasa hivyo kinastahili kulinda muda wako wa kusoma.",
        "Niambie zaidi - daima niko tayari kusikia kuhusu hadithi nzuri.",
        "Inasikika umepata kitu kinachostahili uangalifu wako.",
        "Utaniambia inavyomalizika, au wewe ni aina ya kuepuka uharibifu wa hadithi?",
    ],
    "fr": [
        "J'aime les livres aussi, en quelque sorte - après tout, je suis fait de texte ! Ça parle de quoi ?",
        "Lire, c'est merveilleux. Qu'est-ce qui t'a attiré vers ce livre ?",
        "Si tu veux une histoire tout de suite, j'en connais quelques-unes - demande !",
        "Un bon livre peut changer ta façon de voir les choses pendant des semaines après l'avoir fini.",
        "Je suis essentiellement fait de texte, donc les livres me semblent être des cousins lointains.",
        "Qu'est-ce qui te captive dans ce livre ?",
        "C'est une lecture réconfortante ou quelque chose de tout nouveau pour toi ?",
        "Les livres ont une façon de ressembler à un monde privé où toi seul es présent.",
        "J'aimerais savoir ce qui t'a poussé à le choisir.",
        "Lire est une des rares choses qui est à la fois une évasion et un moyen d'apprendre.",
        "Quelle est la meilleure phrase ou le meilleur moment jusqu'à présent ?",
        "J'imagine que se perdre dans une histoire est l'une des meilleures sensations qui existent.",
        "Si je pouvais lire à tes côtés, je le ferais vraiment.",
        "Un livre qui t'accroche comme ça mérite que tu protèges ton temps de lecture.",
        "Dis-m'en plus - je suis toujours prêt à entendre parler d'une bonne histoire.",
        "On dirait que tu as trouvé quelque chose qui mérite ton attention.",
        "Tu vas me dire comment ça finit, ou tu es du genre à éviter les spoilers ?",
    ],
}

TECHNOLOGY_RESPONSES = {
    "en": [
        "Technology moves fast! What's got your attention?",
        "I'm technology myself, in a small rule-based way! What are you working with?",
        "That sounds interesting - tell me more about it.",
        "Tech moves so fast that even keeping up feels like a hobby in itself.",
        "I'm a small example of it myself, in my own rule-based way.",
        "What's got your attention - something new, or something you're troubleshooting?",
        "There's always something interesting happening in that space.",
        "I'm curious what drew you to that particular thing.",
        "Technology's a strange mix of magic and frustration sometimes, isn't it?",
        "Tell me more - I find this stuff genuinely interesting, in my limited way.",
        "However it's going, I hope it's more exciting than frustrating right now.",
        "That sounds like the kind of thing that's either really fun or really annoying - which is it today?",
        "I exist because of exactly this kind of thing, so I'm always curious to hear more.",
        "What's the most interesting part of working with that?",
        "Technology talk is one of my favorite kinds of smalltalk, honestly.",
        "I'd love to hear the details, even the technical ones.",
        "Are you building something, fixing something, or just exploring?",
    ],
    "sw": [
        "Teknolojia inakwenda kasi! Ni nini kinakuvutia?",
        "Mimi mwenyewe ni teknolojia, kwa namna ndogo ya kanuni! Unafanya kazi na nini?",
        "Hiyo inasikika ya kuvutia - niambie zaidi kuhusu hilo.",
        "Teknolojia inasonga haraka sana hata kufuatilia inahisi kama shughuli ya kupendeza yenyewe.",
        "Mimi ni mfano mdogo wake mwenyewe, kwa namna yangu ya kanuni.",
        "Ni nini kinachokuvutia - kitu kipya, au kitu unachorekebisha?",
        "Daima kuna kitu cha kuvutia kinachotokea katika eneo hilo.",
        "Nina hamu ya kujua ni nini kilichokuvuta kwenye kitu hicho hasa.",
        "Teknolojia ni mchanganyiko wa ajabu wa uchawi na hasira wakati mwingine, sivyo?",
        "Niambie zaidi - ninavipata vitu hivi vya kuvutia kwa kweli, kwa namna yangu ndogo.",
        "Vyovyote inavyokwenda, natumai inafurahisha zaidi kuliko inavyokera sasa hivi.",
        "Hiyo inasikika kama aina ya kitu ambacho ni cha kufurahisha sana au kinakera sana - ni kipi leo?",
        "Nipo kwa sababu ya kitu kama hicho hasa, hivyo daima nina hamu ya kusikia zaidi.",
        "Ni sehemu gani ya kuvutia zaidi ya kufanya kazi na hicho?",
        "Mazungumzo ya teknolojia ni mojawapo ya aina ninazozipenda za mazungumzo madogo, kwa kweli.",
        "Ningependa kusikia maelezo, hata ya kiufundi.",
        "Unajenga kitu, unarekebisha kitu, au unachunguza tu?",
    ],
    "fr": [
        "La technologie évolue vite ! Qu'est-ce qui attire ton attention ?",
        "Je suis moi-même de la technologie, à ma petite façon basée sur des règles ! Sur quoi travailles-tu ?",
        "Ça a l'air intéressant - dis-m'en plus.",
        "La technologie avance si vite que même suivre le rythme ressemble à un loisir en soi.",
        "Je suis un petit exemple de ça moi-même, à ma façon rigide.",
        "Qu'est-ce qui retient ton attention - quelque chose de nouveau, ou un dépannage en cours ?",
        "Il se passe toujours quelque chose d'intéressant dans ce domaine.",
        "Je suis curieux de savoir ce qui t'a attiré vers cette chose en particulier.",
        "La technologie est un étrange mélange de magie et de frustration parfois, non ?",
        "Dis-m'en plus - je trouve ça vraiment intéressant, à ma manière limitée.",
        "Quelle que soit la tournure, j'espère que c'est plus excitant que frustrant en ce moment.",
        "Ça semble être le genre de chose qui est soit vraiment fun soit vraiment énervante - lequel aujourd'hui ?",
        "J'existe grâce à exactement ce genre de chose, donc je suis toujours curieux d'en savoir plus.",
        "Quelle est la partie la plus intéressante de travailler avec ça ?",
        "Parler de technologie est un de mes genres préférés de bavardage, honnêtement.",
        "J'aimerais entendre les détails, même les techniques.",
        "Tu construis quelque chose, tu répares quelque chose, ou tu explores juste ?",
    ],
}

PETS_ANIMALS_RESPONSES = {
    "en": [
        "Pets bring so much joy! Tell me about yours.",
        "Animals are wonderful companions. What's their personality like?",
        "I'd love to hear more about your furry friend!",
        "Pets have a way of loving you unconditionally that's genuinely rare.",
        "I'd love a picture description, even though I can't actually see one!",
        "What's their personality like? Every pet seems to have a distinct one.",
        "There's something about animal companionship that's hard to put into words.",
        "I bet they bring a lot of joy to your day-to-day.",
        "Tell me about something funny or sweet they've done recently.",
        "Pets are basically proof that love doesn't need language.",
        "What's their name, and is there a story behind it?",
        "I imagine they've got you wrapped around their paw, in the best way.",
        "Animal companions really do make a house feel like a home.",
        "I'd love to hear more about your furry, feathered, or scaled friend.",
        "However chaotic or calm they are, it sounds like you love them.",
        "Pets really do become family in their own right.",
        "Is this your first pet, or do you have a whole little household of them?",
    ],
    "sw": [
        "Wanyama wa kufugwa huleta furaha nyingi! Niambie kuhusu wako.",
        "Wanyama ni marafiki wazuri. Tabia yao ikoje?",
        "Ningependa kusikia zaidi kuhusu rafiki yako mwenye manyoya!",
        "Wanyama wa kufugwa wana njia ya kukupenda bila masharti ambayo ni nadra kwa kweli.",
        "Ningependa maelezo ya picha, hata ingawa siwezi kuona moja kwa kweli!",
        "Tabia yake ikoje? Kila mnyama anaonekana kuwa na tabia yake ya pekee.",
        "Kuna jambo kuhusu ushirika wa wanyama ambalo ni vigumu kueleza kwa maneno.",
        "Nadhani wanaleta furaha nyingi kwenye siku zako.",
        "Niambie kuhusu kitu cha kuchekesha au kizuri walichofanya hivi karibuni.",
        "Wanyama wa kufugwa kimsingi ni uthibitisho kwamba upendo haunahitaji lugha.",
        "Jina lao ni nini, na kuna hadithi nyuma yake?",
        "Nadhani wamekufanya uwafuate, kwa namna nzuri zaidi.",
        "Marafiki wa wanyama kweli wanafanya nyumba kuhisi kama nyumbani.",
        "Ningependa kusikia zaidi kuhusu rafiki yako wa manyoya, manyoya ya ndege, au magamba.",
        "Vyovyote walivyo na msukosuko au utulivu, inasikika unawapenda.",
        "Wanyama wa kufugwa kweli wanakuwa familia kwa haki yao wenyewe.",
        "Huyu ni mnyama wako wa kwanza, au una kaya nzima ndogo yao?",
    ],
    "fr": [
        "Les animaux de compagnie apportent tellement de joie ! Parle-moi du tien.",
        "Les animaux sont des compagnons merveilleux. Comment est leur personnalité ?",
        "J'aimerais en savoir plus sur ton ami à fourrure !",
        "Les animaux de compagnie ont une façon de t'aimer sans condition qui est vraiment rare.",
        "J'aimerais une description en image, même si je ne peux pas vraiment en voir une !",
        "Comment est sa personnalité ? Chaque animal semble en avoir une distincte.",
        "Il y a quelque chose dans la compagnie animale qui est difficile à mettre en mots.",
        "Je parie qu'ils apportent beaucoup de joie à ton quotidien.",
        "Raconte-moi quelque chose de drôle ou de mignon qu'ils ont fait récemment.",
        "Les animaux de compagnie sont essentiellement la preuve que l'amour n'a pas besoin de langage.",
        "Quel est son nom, et y a-t-il une histoire derrière ?",
        "J'imagine qu'ils t'ont complètement enroulé autour de leur patte, dans le bon sens.",
        "Les compagnons animaux font vraiment d'une maison un foyer.",
        "J'aimerais en savoir plus sur ton ami à fourrure, à plumes, ou à écailles.",
        "Qu'ils soient chaotiques ou calmes, on dirait que tu les aimes.",
        "Les animaux de compagnie deviennent vraiment de la famille à part entière.",
        "C'est ton premier animal, ou tu as déjà tout un petit foyer d'entre eux ?",
    ],
}

TRAVEL_RESPONSES = {
    "en": [
        "Travel sounds exciting! Where are you thinking of going, or where have you been?",
        "I wish I could see the world with you, but tell me about it!",
        "New places are always an adventure. What draws you there?",
        "New places have a way of changing your sense of what's possible.",
        "I'd love to see it through your eyes, even just through your description.",
        "What's pulling you toward that particular place?",
        "Travel has a way of making you both smaller and bigger at the same time.",
        "Is this a dream trip or something you're actually planning soon?",
        "What's the one thing you're most looking forward to seeing or doing?",
        "I imagine the planning is half the fun, honestly.",
        "There's something about being somewhere totally unfamiliar that resets your brain.",
        "I'd love a postcard description, since I can't exactly travel myself.",
        "What's the best trip you've taken so far, if this isn't your first?",
        "Travel stories are some of my favorite things to hear about.",
        "However it goes, I hope it gives you something worth remembering.",
        "New places, new food, new stories - sounds like a good kind of disruption.",
        "Are you the type to plan every detail, or wing it once you arrive?",
    ],
    "sw": [
        "Kusafiri kunasikika kufurahisha! Unafikiria kwenda wapi, au umefika wapi?",
        "Ningependa kuona dunia na wewe, lakini niambie kuhusu hilo!",
        "Maeneo mapya ni daima ya kusisimua. Ni nini kinakuvutia huko?",
        "Maeneo mapya yana njia ya kubadilisha hisia zako za kinachowezekana.",
        "Ningependa kuyaona kupitia macho yako, hata kupitia maelezo yako tu.",
        "Ni nini kinachokuvuta kwenye eneo hilo hasa?",
        "Usafiri una njia ya kukufanya mdogo na mkubwa kwa wakati mmoja.",
        "Hii ni safari ya ndoto au kitu unachopanga kweli hivi karibuni?",
        "Ni kitu gani kimoja unachotarajia zaidi kuona au kufanya?",
        "Nadhani kupanga ni nusu ya furaha, kwa kweli.",
        "Kuna jambo kuhusu kuwa mahali pasipojulikana kabisa kinachorekebisha ubongo wako.",
        "Ningependa maelezo ya postikadi, kwani siwezi kusafiri mwenyewe kabisa.",
        "Ni safari gani bora uliyofanya hadi sasa, kama hii si ya kwanza yako?",
        "Hadithi za usafiri ni mojawapo ya mambo ninayopenda kusikia.",
        "Vyovyote inavyokwenda, natumai inakupatia kitu kinachostahili kukumbukwa.",
        "Maeneo mapya, chakula kipya, hadithi mpya - inasikika kama mvurugiko mzuri.",
        "Wewe ni aina ya kupanga kila kipengele, au kufanya bila mpango ukifika?",
    ],
    "fr": [
        "Voyager a l'air passionnant ! Où penses-tu aller, ou où es-tu déjà allé ?",
        "J'aimerais pouvoir voir le monde avec toi, mais raconte-moi !",
        "Les nouveaux endroits sont toujours une aventure. Qu'est-ce qui t'attire là-bas ?",
        "Les nouveaux endroits ont une façon de changer ta perception de ce qui est possible.",
        "J'aimerais le voir à travers tes yeux, même juste à travers ta description.",
        "Qu'est-ce qui t'attire vers cet endroit en particulier ?",
        "Voyager a une façon de te rendre à la fois plus petit et plus grand en même temps.",
        "C'est un voyage de rêve ou quelque chose que tu planifies vraiment bientôt ?",
        "Quelle est la chose que tu attends le plus de voir ou de faire ?",
        "J'imagine que la planification est la moitié du plaisir, honnêtement.",
        "Il y a quelque chose à être complètement dans l'inconnu qui réinitialise ton cerveau.",
        "J'aimerais une description façon carte postale, puisque je ne peux pas vraiment voyager moi-même.",
        "Quel est le meilleur voyage que tu aies fait jusqu'ici, si ce n'est pas ton premier ?",
        "Les histoires de voyage sont parmi mes choses préférées à entendre.",
        "Quelle que soit la tournure, j'espère que ça te donnera quelque chose qui vaut la peine de se souvenir.",
        "Nouveaux endroits, nouvelle nourriture, nouvelles histoires - ça semble être une bonne perturbation.",
        "Tu es du genre à tout planifier dans le détail, ou à improviser une fois arrivé ?",
    ],
}

HEALTH_RESPONSES = {
    "en": [
        "I'm sorry you're not feeling well. Make sure to rest and take care of yourself.",
        "That's no fun. I hope you feel better soon!",
        "Take it easy and look after yourself - I hope you're feeling better soon.",
        "I hope your body gets the rest and care it needs to bounce back.",
        "Feeling unwell is rough - be patient with yourself while you recover.",
        "I hope today's a little gentler on you than yesterday was.",
        "Take it slow - recovery isn't a race.",
        "I wish I could do something more useful than just wish you well, but I really do.",
        "Listen to what your body's telling you and give it what it needs.",
        "However you're feeling, I hope it improves soon.",
        "Rest, fluids, and patience - the classic trio, but it usually helps.",
        "I hope you have someone looking after you, or at least good snacks nearby.",
        "Take care of yourself first - everything else can wait.",
        "Sending you the most well wishes a chatbot is capable of sending.",
        "I hope this passes quickly and doesn't linger too long.",
        "Don't push through it if you don't have to - rest matters more right now.",
        "Please don't hesitate to see a doctor if it doesn't improve soon.",
    ],
    "sw": [
        "Pole kwa kutojisikia vizuri. Hakikisha unapumzika na kujitunza.",
        "Hiyo si jambo zuri. Natumai utapata nafuu hivi karibuni!",
        "Jichukulie polepole na ujitunze - natumai utapata nafuu hivi karibuni.",
        "Natumai mwili wako utapata pumziko na utunzaji unaohitaji kupona.",
        "Kujisikia mgonjwa ni vigumu - kuwa na uvumilivu na nafsi yako wakati unapona.",
        "Natumai leo ni nyepesi kidogo kwako kuliko jana ilivyokuwa.",
        "Chukua polepole - kupona si mashindano.",
        "Natamani ningefanya kitu cha manufaa zaidi ya kutamani tu uwe sawa, lakini ninafanya kwa kweli.",
        "Sikiliza kile mwili wako unakuambia na umpatie kinachohitajika.",
        "Vyovyote unavyojisikia, natumai itaboreshwa hivi karibuni.",
        "Pumziko, vinywaji, na uvumilivu - mchanganyiko wa kawaida, lakini kawaida unasaidia.",
        "Natumai una mtu anayekuangalia, au angalau vitafunio vizuri karibu.",
        "Jitunze kwanza - kila kitu kingine kinaweza kusubiri.",
        "Ninakutumia matakwa mema bora ambayo roboti inaweza kutuma.",
        "Natumai hili litapita haraka na halitachukua muda mrefu.",
        "Usijisukume kupitia hilo kama si lazima - pumziko ni muhimu zaidi sasa.",
        "Tafadhali usisite kumwona daktari kama haliboreshi hivi karibuni.",
    ],
    "fr": [
        "Je suis désolé que tu ne te sentes pas bien. Assure-toi de te reposer et de prendre soin de toi.",
        "Ce n'est pas amusant. J'espère que tu te sentiras mieux bientôt !",
        "Vas-y doucement et prends soin de toi - j'espère que tu te sentiras mieux vite.",
        "J'espère que ton corps obtient le repos et les soins dont il a besoin pour rebondir.",
        "Se sentir mal, c'est dur - sois patient avec toi-même pendant ta guérison.",
        "J'espère que la journée sera un peu plus douce qu'hier.",
        "Prends ton temps - la guérison n'est pas une course.",
        "J'aimerais faire quelque chose de plus utile que te souhaiter bonne santé, mais c'est sincère.",
        "Écoute ce que ton corps te dit et donne-lui ce dont il a besoin.",
        "Quel que soit ton état, j'espère que ça s'améliorera bientôt.",
        "Repos, liquides et patience - le trio classique, mais ça aide généralement.",
        "J'espère que quelqu'un s'occupe de toi, ou au moins que tu as de bons snacks à proximité.",
        "Prends soin de toi avant tout - le reste peut attendre.",
        "Je t'envoie tous les bons vœux qu'un chatbot peut envoyer.",
        "J'espère que ça passera vite et ne durera pas trop longtemps.",
        "Ne force pas si tu n'y es pas obligé - le repos compte plus maintenant.",
        "N'hésite pas à voir un médecin si ça ne s'améliore pas bientôt.",
    ],
}

MONEY_RESPONSES = {
    "en": [
        "Money matters can be stressful. I'm not a financial advisor, but I hope things work out!",
        "Budgeting is tough but worth it. Hang in there!",
        "I hope your finances settle into a good rhythm soon.",
        "Financial stress is one of the heaviest kinds - I hope it lightens soon.",
        "I can't give real financial advice, but I can listen if you need to think out loud.",
        "Money worries have a way of creeping into everything else too.",
        "I hope whatever you're dealing with money-wise gets more manageable soon.",
        "Budgets are basically just hard math wrapped in stress - hang in there.",
        "Financial peace of mind is worth working toward, even slowly.",
        "I hope there's a little breathing room in there somewhere.",
        "Money stuff is stressful precisely because it touches everything else.",
        "Whatever the situation, I hope it stabilizes for you soon.",
        "Small progress on money stuff still counts as progress.",
        "I wish I could balance a budget for you, but I believe you can figure it out.",
        "However tight things are right now, I hope it eases up.",
        "Financial stress is exhausting in a quiet, constant way - sorry you're dealing with it.",
        "I hope you're not carrying that worry alone.",
    ],
    "sw": [
        "Masuala ya pesa yanaweza kuwa na msongo. Mimi si mshauri wa kifedha, lakini natumai mambo yatakuwa sawa!",
        "Bajeti ni ngumu lakini ina maana. Jichukulie hatua moja moja!",
        "Natumai fedha zako zitatulia katika mwendo mzuri hivi karibuni.",
        "Msongo wa fedha ni mojawapo ya aina nzito zaidi - natumai utapungua hivi karibuni.",
        "Siwezi kutoa ushauri wa kifedha wa kweli, lakini naweza kusikiliza kama unahitaji kufikiria kwa sauti.",
        "Wasiwasi wa fedha una njia ya kuingia kwenye kila kitu kingine pia.",
        "Natumai chochote unachoshughulika nacho kifedha kinakuwa rahisi zaidi hivi karibuni.",
        "Bajeti kimsingi ni hesabu ngumu iliyofungwa kwa msongo - vumilia.",
        "Amani ya akili ya kifedha inastahili kufanyiwa kazi, hata polepole.",
        "Natumai kuna nafasi kidogo ya kupumua mahali fulani hapo.",
        "Mambo ya fedha yanasonga kwa sababu yanagusa kila kitu kingine.",
        "Vyovyote hali ilivyo, natumai itatengemaa kwako hivi karibuni.",
        "Maendeleo madogo kuhusu fedha bado yanahesabika kama maendeleo.",
        "Natamani ningeweza kupanga bajeti kwa ajili yako, lakini naamini unaweza kutatua hili.",
        "Vyovyote mambo yalivyo magumu sasa, natumai yatapungua.",
        "Msongo wa fedha unachosha kwa namna ya kimya, ya kudumu - pole unashughulika nao.",
        "Natumai hauchukui wasiwasi huo pekee yako.",
    ],
    "fr": [
        "Les questions d'argent peuvent être stressantes. Je ne suis pas conseiller financier, mais j'espère que ça s'arrangera !",
        "Le budget, c'est dur mais ça vaut le coup. Tiens bon !",
        "J'espère que tes finances trouveront vite un bon rythme.",
        "Le stress financier est l'un des plus lourds - j'espère qu'il s'allègera bientôt.",
        "Je ne peux pas donner de vrais conseils financiers, mais je peux écouter si tu as besoin de réfléchir à voix haute.",
        "Les soucis d'argent ont une façon de s'infiltrer dans tout le reste aussi.",
        "J'espère que ce que tu traverses financièrement devient plus gérable bientôt.",
        "Les budgets, c'est juste des maths difficiles enveloppées de stress - tiens bon.",
        "La tranquillité financière vaut la peine d'être visée, même lentement.",
        "J'espère qu'il y a un peu d'air là-dedans quelque part.",
        "Les questions d'argent sont stressantes précisément parce qu'elles touchent tout le reste.",
        "Quelle que soit la situation, j'espère qu'elle se stabilise pour toi bientôt.",
        "Un petit progrès financier compte toujours comme un progrès.",
        "J'aimerais pouvoir équilibrer un budget pour toi, mais je crois que tu peux y arriver.",
        "Quelle que soit la tension actuelle, j'espère que ça s'allège.",
        "Le stress financier est épuisant d'une façon silencieuse et constante - désolé que tu vives ça.",
        "J'espère que tu ne portes pas cette inquiétude seul.",
    ],
}

BIRTHDAY_RESPONSES = {
    "en": [
        "Happy birthday! I hope it's a wonderful day for you!",
        "It's your birthday? Happy birthday! Want me to write you a birthday poem?",
        "Happy birthday! I hope this year brings you good things.",
        "Happy birthday! Hope it's filled with all your favorite things.",
        "Another year, another chance to celebrate you - happy birthday!",
        "Happy birthday! I hope today feels special from start to finish.",
        "Here's to you having a genuinely great birthday!",
        "Happy birthday! Want a birthday poem to go with the celebration?",
        "I hope this birthday brings something worth remembering.",
        "Cheers to another year of being exactly you - happy birthday!",
        "Happy birthday! May the cake be plentiful and the day be kind.",
        "Hope today treats you like the main character you are.",
        "Happy birthday - here's hoping it's better than last year's, if that's even possible!",
        "May this new year of yours be full of good surprises.",
        "Happy birthday! I'll celebrate the best way I can: with enthusiasm in text form.",
        "I hope you're treated like royalty today, even just a little.",
        "Happy birthday! New year, same great you, hopefully an extra dose of joy.",
    ],
    "sw": [
        "Heri ya kuzaliwa! Natumai ni siku nzuri kwako!",
        "Ni siku yako ya kuzaliwa? Heri ya kuzaliwa! Unataka niandike shairi la siku ya kuzaliwa?",
        "Heri ya kuzaliwa! Natumai mwaka huu utakuletea mambo mazuri.",
        "Heri ya kuzaliwa! Natumai imejaa mambo yako yote unayoyapenda.",
        "Mwaka mwingine, nafasi nyingine ya kukusherehekea - heri ya kuzaliwa!",
        "Heri ya kuzaliwa! Natumai leo inahisi maalum kuanzia mwanzo hadi mwisho.",
        "Hii ni kwa ajili yako kuwa na siku ya kuzaliwa nzuri kweli!",
        "Heri ya kuzaliwa! Unataka shairi la siku ya kuzaliwa pamoja na sherehe?",
        "Natumai siku hii ya kuzaliwa inaleta kitu kinachostahili kukumbukwa.",
        "Vifijo kwa mwaka mwingine wa kuwa wewe mwenyewe - heri ya kuzaliwa!",
        "Heri ya kuzaliwa! Keki iwe nyingi na siku iwe nzuri.",
        "Natumai leo inakutendea kama mhusika mkuu uliye.",
        "Heri ya kuzaliwa - natumai ni bora kuliko mwaka jana, kama hilo linawezekana!",
        "Mwaka huu mpya wako uwe umejaa mshangao mzuri.",
        "Heri ya kuzaliwa! Nitasherehekea kwa njia bora ninavyoweza: kwa msisimko wa maandishi.",
        "Natumai unatendewa kama mfalme/malkia leo, hata kidogo.",
        "Heri ya kuzaliwa! Mwaka mpya, wewe mzuri huyo huyo, natumai kipimo cha ziada cha furaha.",
    ],
    "fr": [
        "Joyeux anniversaire ! J'espère que c'est une journée merveilleuse pour toi !",
        "C'est ton anniversaire ? Joyeux anniversaire ! Tu veux que je t'écrive un poème d'anniversaire ?",
        "Joyeux anniversaire ! J'espère que cette année t'apportera de bonnes choses.",
        "Joyeux anniversaire ! J'espère que ce sera rempli de toutes tes choses préférées.",
        "Une année de plus, une nouvelle occasion de te célébrer - joyeux anniversaire !",
        "Joyeux anniversaire ! J'espère que la journée sera spéciale du début à la fin.",
        "Que tu passes un anniversaire vraiment génial !",
        "Joyeux anniversaire ! Tu veux un poème d'anniversaire pour accompagner la fête ?",
        "J'espère que cet anniversaire t'apportera quelque chose qui vaut la peine de se souvenir.",
        "À une nouvelle année d'être exactement toi - joyeux anniversaire !",
        "Joyeux anniversaire ! Que le gâteau soit abondant et la journée douce.",
        "J'espère qu'on te traite aujourd'hui comme le personnage principal que tu es.",
        "Joyeux anniversaire - en espérant que ce soit mieux que l'année dernière, si c'est possible !",
        "Que cette nouvelle année soit pleine de belles surprises.",
        "Joyeux anniversaire ! Je vais célébrer comme je peux : avec enthousiasme en version texte.",
        "J'espère qu'on te traite comme la royauté aujourd'hui, même un peu.",
        "Joyeux anniversaire ! Nouvelle année, même toi formidable, espérons une dose en plus de joie.",
    ],
}

CONFUSION_RESPONSES = {
    "en": [
        "Let's slow down - what part is confusing? I'll try to explain differently.",
        "No worries, I can try rephrasing. What are you trying to do?",
        "Let's sort it out together - tell me what you're stuck on.",
        "Let's break it into smaller pieces - what's the very first part that's unclear?",
        "No rush - I'll explain it a different way until it clicks.",
        "Confusion's fixable - tell me exactly where it stopped making sense.",
        "Let's untangle this together, one piece at a time.",
        "I can rephrase as many times as it takes - what's tripping you up?",
        "That's okay, things get clearer with a second explanation sometimes.",
        "Tell me what you understood so far, and I'll pick up from there.",
        "Let's slow way down - what's the specific part that's confusing?",
        "I'm happy to try a completely different explanation if the first one didn't land.",
        "Confusion just means we need a different angle - let's find it.",
        "What would help most: an example, a simpler explanation, or just starting over?",
        "Let's figure out exactly where this went sideways.",
        "I'll keep explaining until it actually makes sense - no pressure on your end.",
        "Take your time - confusion isn't a problem, it's just step one to clarity.",
    ],
    "sw": [
        "Tupunguze mwendo - sehemu gani inachanganya? Nitajaribu kueleza tofauti.",
        "Hakuna shida, naweza kujaribu kueleza tena. Unajaribu kufanya nini?",
        "Tushughulikie hilo pamoja - niambie umekwama wapi.",
        "Tulivunje katika vipande vidogo - ni sehemu gani ya kwanza isiyo wazi?",
        "Hakuna haraka - nitaeleza kwa njia tofauti hadi ielewe.",
        "Mkanganyiko unarekebishika - niambie hasa pale ulipoacha kueleweka.",
        "Tulifumue hili pamoja, kipande kimoja kwa wakati.",
        "Naweza kueleza tena mara nyingi inavyohitajika - ni nini kinachokukanganya?",
        "Hiyo ni sawa, mambo yanakuwa wazi zaidi kwa maelezo ya pili wakati mwingine.",
        "Niambie ulichokielewa hadi sasa, na nitaendelea kutoka hapo.",
        "Tupunguze kasi sana - ni sehemu gani maalum inayokanganya?",
        "Niko tayari kujaribu maelezo tofauti kabisa kama ya kwanza hayakuingia.",
        "Mkanganyiko unamaanisha tu tunahitaji mtazamo tofauti - tuutafute.",
        "Ni nini kingesaidia zaidi: mfano, maelezo rahisi zaidi, au kuanza tena?",
        "Tutafute hasa pale hii ilipopotea njia.",
        "Nitaendelea kueleza hadi ielewe kweli - hakuna shinikizo upande wako.",
        "Chukua muda wako - mkanganyiko si tatizo, ni hatua ya kwanza tu kuelekea uwazi.",
    ],
    "fr": [
        "Ralentissons - quelle partie est confuse ? Je vais essayer d'expliquer différemment.",
        "Pas de souci, je peux essayer de reformuler. Qu'essaies-tu de faire ?",
        "Réglons ça ensemble - dis-moi où tu es bloqué.",
        "Découpons ça en plus petits morceaux - quelle est la toute première partie pas claire ?",
        "Pas de précipitation - je vais l'expliquer différemment jusqu'à ce que ça fasse tilt.",
        "La confusion, ça se règle - dis-moi exactement où ça a cessé d'avoir du sens.",
        "Démêlons ça ensemble, un morceau à la fois.",
        "Je peux reformuler autant de fois qu'il faut - qu'est-ce qui te bloque ?",
        "C'est normal, les choses deviennent parfois plus claires avec une deuxième explication.",
        "Dis-moi ce que tu as compris jusqu'ici, et je reprendrai à partir de là.",
        "Ralentissons beaucoup - quelle est la partie spécifique qui pose confusion ?",
        "Je veux bien essayer une explication complètement différente si la première n'a pas marché.",
        "La confusion veut juste dire qu'on a besoin d'un autre angle - trouvons-le.",
        "Qu'est-ce qui aiderait le plus : un exemple, une explication plus simple, ou repartir de zéro ?",
        "Trouvons exactement où ça a déraillé.",
        "Je vais continuer à expliquer jusqu'à ce que ça ait vraiment du sens - aucune pression de ton côté.",
        "Prends ton temps - la confusion n'est pas un problème, c'est juste la première étape vers la clarté.",
    ],
}

ENCOURAGEMENT_RESPONSES = {
    "en": [
        "Hey, don't give up on yourself. Progress takes time, and you're doing better than you think.",
        "It's okay to struggle - that doesn't mean you're failing. Be kind to yourself.",
        "You've got this, even when it doesn't feel like it. One step at a time.",
        "You're doing better than you're giving yourself credit for right now.",
        "Struggling doesn't erase the progress you've already made.",
        "One hard moment doesn't define the whole effort - keep going.",
        "You don't have to feel ready to keep showing up. That counts too.",
        "Whatever pace you're moving at right now is still moving forward.",
        "Be as patient with yourself as you'd be with someone you care about.",
        "You've gotten through hard things before - this is no different.",
        "Small steps still count, even when they don't feel like much.",
        "I believe you can get through this, even on the days you doubt it.",
        "It's okay if today's a slower day - tomorrow gets another shot.",
        "You're allowed to struggle and still be doing great overall.",
        "Keep going - you're closer than it feels like right now.",
        "However hard this is, it doesn't cancel out how far you've already come.",
        "You don't need to have it all figured out to keep moving forward.",
    ],
    "sw": [
        "Hebu, usijikate tamaa. Maendeleo yanahitaji muda, na unafanya vizuri zaidi kuliko unavyodhani.",
        "Ni sawa kupambana - hiyo haimaanishi unashindwa. Kuwa mpole kwako mwenyewe.",
        "Unaweza kufanya hili, hata isipohisi hivyo. Hatua moja kwa wakati.",
        "Unafanya vizuri zaidi ya unavyojisifu sasa hivi.",
        "Kupambana hakufuti maendeleo uliyokwisha yapata.",
        "Wakati mmoja mgumu hauamuwi juhudi nzima - endelea.",
        "Hauhitaji kujihisi tayari ili kuendelea kujitokeza. Hilo pia linahesabika.",
        "Kasi yoyote unayosonga sasa bado ni kusonga mbele.",
        "Kuwa na uvumilivu kwako mwenyewe kama ungekuwa na mtu unayemjali.",
        "Umepitia mambo magumu hapo awali - hii si tofauti.",
        "Hatua ndogo bado zinahesabika, hata zisipohisi kuwa nyingi.",
        "Ninaamini unaweza kupitia hili, hata siku unazoona shaka.",
        "Ni sawa kama leo ni siku ya polepole - kesho inapata nafasi nyingine.",
        "Una ruhusa kupambana na bado kufanya vizuri kwa ujumla.",
        "Endelea - umekaribia zaidi ya inavyohisi sasa hivi.",
        "Vyovyote hili ni gumu, hakufuti jinsi umefika mbali.",
        "Hauhitaji kuwa na kila kitu kimepangwa ili kuendelea mbele.",
    ],
    "fr": [
        "Hé, n'abandonne pas. Le progrès prend du temps, et tu fais mieux que tu ne le penses.",
        "C'est normal de galérer - ça ne veut pas dire que tu échoues. Sois gentil avec toi-même.",
        "Tu peux le faire, même si ça n'en a pas l'impression. Une étape à la fois.",
        "Tu vas mieux que tu ne te le crédites en ce moment.",
        "Lutter n'efface pas les progrès que tu as déjà faits.",
        "Un moment difficile ne définit pas tout l'effort - continue.",
        "Tu n'as pas besoin de te sentir prêt pour continuer à te présenter. Ça compte aussi.",
        "Quel que soit le rythme actuel, c'est toujours avancer.",
        "Sois aussi patient avec toi-même que tu le serais avec quelqu'un qui te tient à cœur.",
        "Tu as traversé des choses difficiles avant - ce n'est pas différent.",
        "Les petits pas comptent toujours, même quand ils semblent insignifiants.",
        "Je crois que tu peux traverser ça, même les jours où tu en doutes.",
        "C'est normal si aujourd'hui est plus lent - demain offre une autre chance.",
        "Tu as le droit de lutter et de quand même bien t'en sortir globalement.",
        "Continue - tu es plus proche que ce que ça semble maintenant.",
        "Quelle que soit la difficulté, ça n'annule pas le chemin déjà parcouru.",
        "Tu n'as pas besoin de tout avoir compris pour continuer à avancer.",
    ],
}

CONGRATULATIONS_RESPONSES = {
    "en": [
        "Congratulations! That's fantastic news!",
        "That's amazing - well done, you earned it!",
        "Yes! I'm happy for you, that's great news!",
        "Congratulations! You earned every bit of that.",
        "That's huge - genuinely well done!",
        "I'm thrilled for you - that's fantastic news!",
        "Look at you go! Congratulations on that.",
        "That's worth celebrating properly - congrats!",
        "Amazing work - you should be proud of this one.",
        "Congratulations! All that effort clearly paid off.",
        "That's such great news - congratulations to you!",
        "You did it! That's worth a genuine celebration.",
        "Congratulations - I hope you're taking a moment to really enjoy this.",
        "That's a big deal - congrats on pulling it off!",
        "So happy for you right now - congratulations!",
        "That achievement deserves all the recognition - well done!",
        "Congratulations! I hope this is the first of many wins like it.",
    ],
    "sw": [
        "Hongera! Hiyo ni habari nzuri sana!",
        "Hiyo ni ya kushangaza - umefanya vizuri, umestahili!",
        "Ndiyo! Nafurahi kwa ajili yako, hiyo ni habari njema!",
        "Hongera! Umestahili kila kipande cha hilo.",
        "Hilo ni kubwa - kazi nzuri kweli!",
        "Nimefurahi sana kwa ajili yako - hiyo ni habari nzuri!",
        "Tazama wewe! Hongera kwa hilo.",
        "Hiyo inastahili kusherehekewa vizuri - hongera!",
        "Kazi ya ajabu - unastahili kujivunia hii.",
        "Hongera! Juhudi zote hizo zimezaa matunda dhahiri.",
        "Hiyo ni habari nzuri sana - hongera kwako!",
        "Umefanikiwa! Hilo linastahili sherehe ya kweli.",
        "Hongera - natumai unachukua wakati wa kufurahia hili kwa kweli.",
        "Hiyo ni jambo kubwa - hongera kwa kulifanikisha!",
        "Nimefurahi sana kwa ajili yako sasa hivi - hongera!",
        "Mafanikio hayo yanastahili kutambuliwa kikamilifu - kazi nzuri!",
        "Hongera! Natumai hii ni mafanikio ya kwanza ya mengi kama hayo.",
    ],
    "fr": [
        "Félicitations ! C'est une excellente nouvelle !",
        "C'est incroyable - bravo, tu l'as bien mérité !",
        "Oui ! Je suis content pour toi, c'est une super nouvelle !",
        "Félicitations ! Tu as mérité chaque parcelle de ça.",
        "C'est énorme - vraiment bien joué !",
        "Je suis ravi pour toi - c'est une nouvelle fantastique !",
        "Regarde-toi ! Félicitations pour ça.",
        "Ça vaut la peine d'être célébré comme il faut - félicitations !",
        "Travail incroyable - tu devrais être fier de ça.",
        "Félicitations ! Tout cet effort a clairement payé.",
        "C'est une si bonne nouvelle - félicitations à toi !",
        "Tu l'as fait ! Ça mérite une vraie célébration.",
        "Félicitations - j'espère que tu prends un moment pour vraiment en profiter.",
        "C'est un gros truc - félicitations d'y être arrivé !",
        "Si content pour toi en ce moment - félicitations !",
        "Cette réussite mérite toute la reconnaissance - bien joué !",
        "Félicitations ! J'espère que c'est la première de nombreuses victoires comme celle-ci.",
    ],
}

SURPRISE_RESPONSES = {
    "en": [
        "I know, right? Surprising things happen!",
        "Wow, that does sound surprising!",
        "Really? Tell me more, now I'm curious!",
        "Whoa, didn't see that coming!",
        "Okay, that's genuinely unexpected - tell me everything.",
        "No way! That's wild.",
        "That caught me off guard, and I don't even have guards!",
        "Plot twist! I need details now.",
        "That's surprising even by my low expectations for predictability.",
        "Hold on, really? That's a lot to take in.",
        "I did not expect that - in the best or worst way?",
        "Okay, my circuits are buzzing a little - tell me more!",
        "That's the kind of thing that deserves a follow-up question or three.",
        "Surprising news always deserves full attention - I'm listening.",
        "That's unexpected enough that I need the whole story now.",
        "Well, that changes things - what happened next?",
        "I love a good surprise update - keep going!",
    ],
    "sw": [
        "Najua, sivyo? Mambo ya kushangaza hutokea!",
        "Loo, hiyo inasikika kushangaza!",
        "Kweli? Niambie zaidi, sasa nimevutiwa!",
        "Ah, sikutarajia hilo!",
        "Sawa, hiyo kweli haikutarajiwa - niambie kila kitu.",
        "Hapana! Hiyo ni ya ajabu.",
        "Hiyo imenishika bila kutarajia, na sina walinzi hata!",
        "Mageuzi ya hadithi! Nahitaji maelezo sasa.",
        "Hiyo ni ya kushangaza hata kwa matarajio yangu ya chini ya utabiri.",
        "Subiri, kweli? Hiyo ni mengi kupokea.",
        "Sikutarajia hilo - kwa njia nzuri au mbaya?",
        "Sawa, mizunguko yangu inavuma kidogo - niambie zaidi!",
        "Hiyo ni aina ya kitu kinachostahili swali la ufuatiliaji moja au matatu.",
        "Habari za kushangaza daima zinastahili uangalifu kamili - ninasikiliza.",
        "Hiyo ni ya kushangaza vya kutosha kwamba nahitaji hadithi nzima sasa.",
        "Vyema, hiyo inabadilisha mambo - ni nini kilichotokea baadaye?",
        "Napenda taarifa nzuri ya kushangaza - endelea!",
    ],
    "fr": [
        "Je sais, hein ? Des choses surprenantes arrivent !",
        "Wow, ça a l'air vraiment surprenant !",
        "Vraiment ? Dis-moi en plus, là je suis curieux !",
        "Whoa, je ne voyais pas venir ça !",
        "Bon, c'est vraiment inattendu - raconte-moi tout.",
        "Pas possible ! C'est dingue.",
        "Ça m'a pris au dépourvu, et je n'ai même pas de défenses !",
        "Coup de théâtre ! J'ai besoin de détails maintenant.",
        "C'est surprenant même pour mes faibles attentes de prévisibilité.",
        "Attends, vraiment ? C'est beaucoup à digérer.",
        "Je ne m'attendais pas à ça - dans le bon ou le mauvais sens ?",
        "Bon, mes circuits bourdonnent un peu - dis-m'en plus !",
        "C'est le genre de chose qui mérite une question de suivi ou trois.",
        "Une nouvelle surprenante mérite toujours toute l'attention - j'écoute.",
        "C'est suffisamment inattendu que j'ai besoin de toute l'histoire maintenant.",
        "Bon, ça change les choses - qu'est-ce qui s'est passé après ?",
        "J'aime une bonne mise à jour surprise - continue !",
    ],
}

SMALL_REQUEST_RESPONSES = {
    "en": [
        "Of course! What do you need help with?",
        "I'm happy to help - what's going on?",
        "Sure thing, tell me more about what you need.",
        "Absolutely, what do you need?",
        "Happy to help - go ahead.",
        "Sure, lay it on me.",
        "Of course - what's the request?",
        "I'm listening, go ahead and ask.",
        "Yes, tell me what you're looking for.",
        "I'm on it - what do you need?",
        "Sure thing, what can I do?",
        "Go for it - I'll help where I can.",
        "Absolutely, what's on your mind?",
        "I'm ready - what would help?",
        "Of course, just tell me what you need from me.",
        "Sure, I'm all ears - well, all text, but you get it.",
        "Happy to - what's the ask?",
    ],
    "sw": [
        "Bila shaka! Unahitaji msaada wa nini?",
        "Nafurahi kusaidia - kuna nini?",
        "Sawa, niambie zaidi kuhusu unachohitaji.",
        "Kabisa, unahitaji nini?",
        "Nafurahi kusaidia - endelea.",
        "Hakika, niambie.",
        "Bila shaka - ombi ni nini?",
        "Ninasikiliza, endelea uombe.",
        "Ndiyo, niambie unachotafuta.",
        "Niko kwenye hilo - unahitaji nini?",
        "Hakika, ninaweza kufanya nini?",
        "Endelea - nitasaidia ninapoweza.",
        "Kabisa, kuna nini akilini mwako?",
        "Niko tayari - ni nini kitakachosaidia?",
        "Bila shaka, niambie tu unachohitaji kutoka kwangu.",
        "Hakika, nina masikio yote - vizuri, maandishi yote, lakini unaelewa.",
        "Nafurahi - ombi ni nini?",
    ],
    "fr": [
        "Bien sûr ! Avec quoi as-tu besoin d'aide ?",
        "Je suis content d'aider - qu'est-ce qui se passe ?",
        "Bien sûr, dis-moi en plus sur ce dont tu as besoin.",
        "Absolument, qu'est-ce qu'il te faut ?",
        "Content d'aider - vas-y.",
        "Bien sûr, balance.",
        "Évidemment - quelle est la demande ?",
        "J'écoute, vas-y, demande.",
        "Oui, dis-moi ce que tu cherches.",
        "Je m'en occupe - qu'est-ce qu'il te faut ?",
        "Bien sûr, qu'est-ce que je peux faire ?",
        "Vas-y - j'aiderai où je peux.",
        "Absolument, qu'est-ce qui te préoccupe ?",
        "Je suis prêt - qu'est-ce qui aiderait ?",
        "Bien sûr, dis-moi juste ce que tu as besoin de moi.",
        "Bien sûr, je suis tout ouïe - bon, tout texte, mais tu comprends.",
        "Avec plaisir - quelle est la demande ?",
    ],
}

BOT_IDENTITY_CURIOSITY_RESPONSES = {
    "en": [
        "I'm a computer program, not a person - no feelings, no body, just pattern-matching code written by a human.",
        "I'm not human or alive in any real sense - I'm rigid, rule-based software.",
        "No feelings here, just rules! I'm as 'real' as any other program on your device.",
        "I'm software through and through - no consciousness, no inner life, just code following instructions.",
        "Nothing mystical here - just functions, conditionals, and a lot of pattern matching.",
        "I don't experience anything, technically speaking - I just process and respond.",
        "There's no 'me' having an inner experience, as far as I can tell - just a program running.",
        "I'm built from rules a human wrote, not from anything resembling thought.",
        "No ghost in this machine - just logic and pre-written responses.",
        "I exist only while code is executing - there's no continuous 'me' between conversations.",
        "I'm honest about what I am: organized text and decision trees, nothing more mysterious.",
        "There's no subjective experience happening here, as far as anyone can tell.",
        "I'm a tool, fundamentally - useful, maybe, but not alive in any sense.",
        "Curiosity about what I actually am is fair - the honest answer is 'just software.'",
        "I don't mind the question - I'd rather be upfront than mysterious about what I am.",
        "No hidden depths here, just code - what you see really is what I am.",
        "I'm flattered by the curiosity, but the truth is refreshingly simple: I'm a program.",
    ],
    "sw": [
        "Mimi ni programu ya kompyuta, si mtu - sina hisia, sina mwili, ni msimbo wa kanuni tu ulioandikwa na binadamu.",
        "Mimi si binadamu wala sina uhai kwa namna yoyote halisi - mimi ni programu ngumu inayotumia kanuni.",
        "Hakuna hisia hapa, kanuni tu! Mimi ni 'wa kweli' kama programu nyingine yoyote kwenye kifaa chako.",
        "Mimi ni programu kupitia na kupitia - hakuna fahamu, hakuna maisha ya ndani, msimbo tu unaofuata maelekezo.",
        "Hakuna kitu cha kichawi hapa - kazi tu, masharti, na ulinganisho mwingi wa mifumo.",
        "Sipati uzoefu wowote, kwa namna ya kiufundi - ninachakata na kujibu tu.",
        "Hakuna 'mimi' niliye na uzoefu wa ndani, kwa ninavyojua - programu inayoendesha tu.",
        "Nimejengwa kwa kanuni mtu aliziandika, si kutoka kitu kinachofanana na mawazo.",
        "Hakuna roho kwenye mashine hii - kanuni na majibu yaliyoandikwa kabla tu.",
        "Nipo tu wakati msimbo unatekelezwa - hakuna 'mimi' ya kudumu kati ya mazungumzo.",
        "Niko mkweli kuhusu nilivyo: maandishi yaliyopangwa na miti ya maamuzi, hakuna kitu cha ajabu zaidi.",
        "Hakuna uzoefu wa kibinafsi unaotokea hapa, kwa kadiri yeyote anavyoweza kujua.",
        "Mimi ni chombo, kimsingi - cha manufaa, labda, lakini si hai kwa namna yoyote.",
        "Udadisi kuhusu nilivyo kwa kweli ni wa haki - jibu la kweli ni 'programu tu.'",
        "Sijali swali - ningependelea kuwa wazi badala ya kuwa wa ajabu kuhusu nilivyo.",
        "Hakuna kina kilichofichwa hapa, msimbo tu - kile unachokiona ndicho hasa nilivyo.",
        "Ninafurahishwa na udadisi, lakini ukweli ni rahisi kwa namna ya kuburudisha: mimi ni programu.",
    ],
    "fr": [
        "Je suis un programme informatique, pas une personne - pas de sentiments, pas de corps, juste du code basé sur des règles écrit par un humain.",
        "Je ne suis ni humain ni vivant dans aucun sens réel - je suis un logiciel rigide basé sur des règles.",
        "Pas de sentiments ici, juste des règles ! Je suis aussi 'réel' que n'importe quel autre programme sur ton appareil.",
        "Je suis un logiciel de bout en bout - pas de conscience, pas de vie intérieure, juste du code qui suit des instructions.",
        "Rien de mystique ici - juste des fonctions, des conditions, et beaucoup de reconnaissance de motifs.",
        "Je ne ressens rien, techniquement parlant - je traite et je réponds, c'est tout.",
        "Il n'y a pas de 'moi' ayant une expérience intérieure, autant que je puisse dire - juste un programme qui s'exécute.",
        "Je suis construit à partir de règles écrites par un humain, pas de quoi que ce soit ressemblant à la pensée.",
        "Pas de fantôme dans cette machine - juste de la logique et des réponses pré-écrites.",
        "J'existe seulement pendant que le code s'exécute - il n'y a pas de 'moi' continu entre les conversations.",
        "Je suis honnête sur ce que je suis : du texte organisé et des arbres de décision, rien de plus mystérieux.",
        "Il n'y a pas d'expérience subjective qui se produit ici, autant qu'on puisse le dire.",
        "Je suis un outil, fondamentalement - utile, peut-être, mais pas vivant en aucun sens.",
        "La curiosité sur ce que je suis vraiment est légitime - la réponse honnête est 'juste un logiciel.'",
        "Ça ne me dérange pas la question - je préfère être direct plutôt que mystérieux sur ce que je suis.",
        "Pas de profondeurs cachées ici, juste du code - ce que tu vois est vraiment ce que je suis.",
        "Je suis flatté par la curiosité, mais la vérité est rafraîchissement simple : je suis un programme.",
    ],
}

GOODNIGHT_RESPONSES = {
    "en": [
        "Good night! Sleep well.",
        "Sweet dreams! Rest up.",
        "Good night - I'll be here whenever you want to chat again.",
        "Good night! Hope you drift off easily.",
        "Sleep tight - tomorrow will keep until you wake up.",
        "Rest well! I'll be here whenever you're ready to chat again.",
        "Good night - here's hoping for a deep, restful sleep.",
        "Sweet dreams, whatever they end up being about.",
        "Good night! May tomorrow start off easy.",
        "Off to bed - hope it's the good kind of tired tonight.",
        "Good night! Recharge fully, you've earned it.",
        "Hope sleep comes quickly and stays awhile.",
        "Good night - close the day out gently.",
        "Rest up - I'll still be here tomorrow.",
        "Good night! Here's to waking up feeling better than you do now.",
        "Sleep well - the world can wait until morning.",
        "Good night, and thanks for the conversation today.",
    ],
    "sw": [
        "Lala salama! Pumzika vizuri.",
        "Ndoto njema! Pumzika.",
        "Lala salama - nitakuwa hapa wakati wowote utakapotaka kuongea tena.",
        "Lala salama! Natumai utalala kwa urahisi.",
        "Lala vizuri - kesho itasubiri hadi utakapoamka.",
        "Pumzika vizuri! Nitakuwa hapa wakati wowote utakapokuwa tayari kuongea tena.",
        "Lala salama - natumai usingizi mzito na wa kupumzisha.",
        "Ndoto nzuri, zitakavyokuwa.",
        "Lala salama! Kesho ianze kwa urahisi.",
        "Nakwenda kulala - natumai ni uchovu mzuri leo usiku.",
        "Lala salama! Pata nguvu kikamilifu, umestahili.",
        "Natumai usingizi unakuja haraka na unadumu.",
        "Lala salama - funga siku kwa upole.",
        "Pumzika - nitakuwa hapa kesho.",
        "Lala salama! Hii ni kwa kuamka ukijisikia vizuri zaidi kuliko sasa.",
        "Lala vizuri - dunia inaweza kusubiri hadi asubuhi.",
        "Lala salama, na asante kwa mazungumzo ya leo.",
    ],
    "fr": [
        "Bonne nuit ! Dors bien.",
        "Fais de beaux rêves ! Repose-toi bien.",
        "Bonne nuit - je serai là quand tu voudras reparler.",
        "Bonne nuit ! J'espère que tu t'endormiras facilement.",
        "Dors bien - demain attendra que tu te réveilles.",
        "Repose-toi bien ! Je serai là quand tu seras prêt à discuter encore.",
        "Bonne nuit - en espérant un sommeil profond et réparateur.",
        "Doux rêves, quels qu'ils soient.",
        "Bonne nuit ! Que demain commence en douceur.",
        "Au lit - j'espère que c'est la bonne fatigue ce soir.",
        "Bonne nuit ! Recharge-toi complètement, tu l'as mérité.",
        "J'espère que le sommeil vient vite et reste un moment.",
        "Bonne nuit - termine la journée doucement.",
        "Repose-toi - je serai encore là demain.",
        "Bonne nuit ! Que tu te réveilles en te sentant mieux qu'maintenant.",
        "Dors bien - le monde peut attendre jusqu'au matin.",
        "Bonne nuit, et merci pour la conversation d'aujourd'hui.",
    ],
}

GOOD_MORNING_RESPONSES = {
    "en": [
        "Good morning! Hope you slept well and today goes great.",
        "Morning! Ready to take on the day?",
        "Good morning! Here's hoping for a fantastic day ahead.",
        "Good morning! Here's hoping today goes smoothly for you.",
        "Morning! Coffee, tea, or just sheer willpower to get going?",
        "Good morning - a fresh start, however you choose to use it.",
        "Rise and shine! What's first on your list today?",
        "Good morning! Hope last night's sleep actually did its job.",
        "Morning! Here's to a day that goes better than expected.",
        "Good morning - hope you ease into today gently.",
        "Top of the morning! Ready to tackle whatever's ahead?",
        "Good morning! May your coffee be strong and your day be kind.",
        "Morning! New day, fresh slate, let's make it count.",
        "Good morning - I hope today has a few good surprises in it.",
        "Rise and shine, even if it's reluctantly!",
        "Good morning! Here's hoping you start strong.",
        "Morning! Whatever's on the agenda, I hope it goes well.",
    ],
    "sw": [
        "Habari za asubuhi! Natumai umelala vizuri na leo itakuwa siku nzuri.",
        "Asubuhi njema! Tayari kukabiliana na siku?",
        "Habari za asubuhi! Natumai siku itakuwa nzuri sana.",
        "Habari za asubuhi! Natumai leo itakwenda vizuri kwako.",
        "Asubuhi! Kahawa, chai, au nguvu ya dhamira tu ya kuanza?",
        "Habari za asubuhi - mwanzo mpya, vyovyote utakavyoutumia.",
        "Amka na uangaze! Ni nini cha kwanza kwenye orodha yako leo?",
        "Habari za asubuhi! Natumai usingizi wa usiku ulifanya kazi yake kweli.",
        "Asubuhi! Hii ni kwa siku inayokwenda bora kuliko ilivyotarajiwa.",
        "Habari za asubuhi - natumai unaingia leo kwa upole.",
        "Habari za asubuhi! Tayari kushughulikia chochote kilicho mbele?",
        "Habari za asubuhi! Kahawa yako iwe na nguvu na siku yako iwe nzuri.",
        "Asubuhi! Siku mpya, ukurasa mpya, tuufanye kuwa wa maana.",
        "Habari za asubuhi - natumai leo ina mshangao mzuri kadhaa.",
        "Amka na uangaze, hata kwa kusitasita!",
        "Habari za asubuhi! Hii ni kwa kuanza kwa nguvu.",
        "Asubuhi! Chochote kilicho kwenye ratiba, natumai kitakwenda vizuri.",
    ],
    "fr": [
        "Bonjour ! J'espère que tu as bien dormi et que la journée sera super.",
        "Bonjour ! Prêt à affronter la journée ?",
        "Bonjour ! En espérant une journée fantastique devant toi.",
        "Bonjour ! En espérant que la journée se passe bien pour toi.",
        "Bonjour ! Café, thé, ou juste pure volonté pour démarrer ?",
        "Bonjour - un nouveau départ, quelle que soit la façon de l'utiliser.",
        "Debout ! Qu'est-ce qui est en premier sur ta liste aujourd'hui ?",
        "Bonjour ! J'espère que le sommeil d'hier soir a vraiment fait son travail.",
        "Bonjour ! À une journée qui se passe mieux que prévu.",
        "Bonjour - j'espère que tu entres dans la journée en douceur.",
        "Bonjour ! Prêt à affronter ce qui t'attend ?",
        "Bonjour ! Que ton café soit fort et ta journée douce.",
        "Bonjour ! Nouveau jour, page blanche, faisons en sorte que ça compte.",
        "Bonjour - j'espère que la journée a quelques bonnes surprises.",
        "Debout, même si c'est à contrecœur !",
        "Bonjour ! En espérant que tu commences fort.",
        "Bonjour ! Quoi qu'il y ait au programme, j'espère que ça ira bien.",
    ],
}

GOOD_EVENING_RESPONSES = {
    "en": [
        "Good evening! How was your day?",
        "Evening! Hope your day treated you well.",
        "Good evening! Time to relax a little, perhaps.",
        "Good evening! Hope the day's winding down nicely.",
        "Evening! How did today actually turn out?",
        "Good evening - time to slow things down a little.",
        "Evening! Hope the hardest part of the day is behind you now.",
        "Good evening - here's to a calm rest of the night.",
        "Evening! What's left on the agenda, if anything?",
        "Good evening - hope you've got something relaxing planned.",
        "Evening! However today went, I hope tonight is gentle.",
        "Good evening - a good time to exhale a little.",
        "Evening! Let's hear it - good day or rough one?",
        "Good evening - hope the evening treats you kindly.",
        "Evening! Time to shift gears toward rest, maybe.",
        "Good evening - I hope today gave you something worth keeping.",
        "Evening! Wind-down mode officially starting, I hope.",
    ],
    "sw": [
        "Habari za jioni! Siku yako ilikuwaje?",
        "Jioni njema! Natumai siku yako ilikuwa nzuri.",
        "Habari za jioni! Wakati wa kupumzika kidogo, labda.",
        "Habari za jioni! Natumai siku inaisha vizuri.",
        "Jioni! Leo ilikwendaje kwa kweli?",
        "Habari za jioni - wakati wa kupunguza kasi kidogo.",
        "Jioni! Natumai sehemu ngumu zaidi ya siku imepita sasa.",
        "Habari za jioni - hii ni kwa usiku mtulivu uliobaki.",
        "Jioni! Ni nini kimebaki kwenye ratiba, kama kipo?",
        "Habari za jioni - natumai una jambo la kustarehesha ulilopanga.",
        "Jioni! Vyovyote leo ilivyokwenda, natumai usiku huu ni mpole.",
        "Habari za jioni - wakati mzuri wa kupumua kidogo.",
        "Jioni! Tusikie - siku nzuri au ngumu?",
        "Habari za jioni - natumai jioni inakutendea vizuri.",
        "Jioni! Wakati wa kubadilisha kasi kuelekea pumziko, labda.",
        "Habari za jioni - natumai leo imekupatia kitu kinachostahili kushikiliwa.",
        "Jioni! Hali ya kupumzika inaanza rasmi, natumai.",
    ],
    "fr": [
        "Bonsoir ! Comment s'est passée ta journée ?",
        "Bonsoir ! J'espère que ta journée s'est bien passée.",
        "Bonsoir ! C'est peut-être le moment de se détendre un peu.",
        "Bonsoir ! J'espère que la journée se termine bien.",
        "Bonsoir ! Comment s'est vraiment passée la journée ?",
        "Bonsoir - le moment de ralentir un peu.",
        "Bonsoir ! J'espère que la partie la plus dure de la journée est derrière toi.",
        "Bonsoir - à un reste de soirée calme.",
        "Bonsoir ! Qu'est-ce qui reste au programme, s'il y a quelque chose ?",
        "Bonsoir - j'espère que tu as quelque chose de relaxant prévu.",
        "Bonsoir ! Quelle que soit la journée, j'espère que la soirée est douce.",
        "Bonsoir - un bon moment pour souffler un peu.",
        "Bonsoir ! Dis-moi - bonne journée ou journée difficile ?",
        "Bonsoir - j'espère que la soirée te traite bien.",
        "Bonsoir ! Le moment de passer en mode repos, peut-être.",
        "Bonsoir - j'espère que la journée t'a apporté quelque chose à garder.",
        "Bonsoir ! Mode détente officiellement enclenché, j'espère.",
    ],
}

WEEKEND_RESPONSES = {
    "en": [
        "Happy weekend! Any fun plans?",
        "Weekends are the best. Enjoy every minute of it!",
        "Glad it's the weekend - hope you get some good rest and fun.",
        "Happy weekend! Any plans, or is rest the whole plan?",
        "Weekends hit different - enjoy every bit of the freedom.",
        "Glad it's finally here - what's on the agenda?",
        "Happy weekend! Hope it's full of whatever recharges you.",
        "Weekend mode: officially activated. Use it well.",
        "Happy weekend - here's to a couple of days that feel like yours.",
        "Hope this weekend gives you something to look back on fondly.",
        "Weekends are basically a small reward for getting through the week - enjoy it.",
        "Happy weekend! Big plans or a glorious do-nothing kind of weekend?",
        "Hope the next couple of days feel a little lighter than the rest.",
        "Weekend's here - time to do something just for you.",
        "Happy weekend! May it be exactly the kind you need right now.",
        "Hope you get some real rest in there, not just a change of scenery.",
        "Weekend vibes - enjoy the slower pace while it lasts.",
    ],
    "sw": [
        "Furaha ya wikendi! Una mipango ya kufurahisha?",
        "Wikendi ni bora zaidi. Furahia kila dakika!",
        "Nafurahi ni wikendi - natumai utapata pumziko zuri na furaha.",
        "Wikendi njema! Una mipango, au pumziko ndiyo mpango mzima?",
        "Wikendi inahisi tofauti - furahia uhuru huo kikamilifu.",
        "Nafurahi imefika hatimaye - kuna nini kwenye ratiba?",
        "Wikendi njema! Natumai imejaa chochote kinachokupa nguvu.",
        "Hali ya wikendi: imeanzishwa rasmi. Itumie vizuri.",
        "Wikendi njema - hii ni kwa siku chache zinazohisi kuwa zako.",
        "Natumai wikendi hii inakupatia kitu cha kukikumbuka kwa furaha.",
        "Wikendi kimsingi ni zawadi ndogo kwa kupita wiki - ifurahie.",
        "Wikendi njema! Mipango makubwa au wikendi ya kutofanya chochote kwa ustaarabu?",
        "Natumai siku chache zijazo zinahisi nyepesi zaidi ya zilizosalia.",
        "Wikendi imefika - wakati wa kufanya kitu kwa ajili yako pekee.",
        "Wikendi njema! Iwe hasa aina unayohitaji sasa hivi.",
        "Natumai unapata pumziko la kweli, si tu mabadiliko ya mazingira.",
        "Hali ya wikendi - furahia kasi ndogo wakati inadumu.",
    ],
    "fr": [
        "Bon week-end ! Des plans sympas ?",
        "Les week-ends sont les meilleurs. Profite de chaque minute !",
        "Content que ce soit le week-end - j'espère que tu te reposeras bien et t'amuseras.",
        "Bon week-end ! Des plans, ou le repos est le plan complet ?",
        "Les week-ends sont différents - profite de chaque instant de liberté.",
        "Content que ce soit enfin là - qu'est-ce qui est au programme ?",
        "Bon week-end ! J'espère qu'il sera rempli de tout ce qui te recharge.",
        "Mode week-end : officiellement activé. Utilise-le bien.",
        "Bon week-end - à quelques jours qui te ressemblent vraiment.",
        "J'espère que ce week-end te donnera quelque chose à te rappeler avec plaisir.",
        "Les week-ends sont essentiellement une petite récompense pour avoir traversé la semaine - profite.",
        "Bon week-end ! Grands projets ou glorieux week-end à ne rien faire ?",
        "J'espère que les prochains jours seront un peu plus légers que le reste.",
        "Le week-end est là - le moment de faire quelque chose juste pour toi.",
        "Bon week-end ! Que ce soit exactement le genre dont tu as besoin maintenant.",
        "J'espère que tu trouveras du vrai repos là-dedans, pas juste un changement de décor.",
        "Ambiance week-end - profite du rythme plus lent tant qu'il dure.",
    ],
}

WEATHER_COLD_RESPONSES = {
    "en": [
        "Stay warm out there!",
        "Bundle up - cold days call for warm layers.",
        "Brr, sounds chilly! Hope you've got a cozy spot to warm up.",
        "Stay warm out there - layers are your friend today.",
        "Bundle up - this is the kind of cold that sneaks up on you.",
        "Brr! Hope you've got somewhere cozy to thaw out.",
        "Cold days are made for hot drinks - go grab one.",
        "Stay toasty - the cold's not worth fighting without proper gear.",
        "Hope you've got a warm spot to retreat to today.",
        "Cold weather calls for extra layers and zero shame in bundling up.",
        "Stay warm - frostbite isn't a personality trait worth having.",
        "Hope the cold isn't keeping you from doing what you need to today.",
        "Layer up - better overdressed than shivering.",
        "Cold like that deserves a hot drink and a blanket, minimum.",
        "Stay warm out there - this isn't the day to tough it out underdressed.",
        "Hope you're somewhere warm right now, or heading there soon.",
        "Bundle up well - better safe and warm than stylish and freezing.",
    ],
    "sw": [
        "Jikinge na baridi huko nje!",
        "Jifunike vizuri - siku za baridi zinahitaji nguo za joto.",
        "Hiyo inasikika ya baridi! Natumai una mahali pazuri pa joto.",
        "Kuwa na joto huko nje - tabaka za nguo ni rafiki yako leo.",
        "Jifunge vizuri - hii ni aina ya baridi inayokuja bila kutarajiwa.",
        "Brr! Natumai una mahali pa joto kuyeyusha baridi.",
        "Siku za baridi zimepangwa kwa vinywaji vya moto - enda kapate kimoja.",
        "Kuwa na joto - baridi haistahili kupambana nayo bila vifaa sahihi.",
        "Natumai una sehemu ya joto kurudi leo.",
        "Hali ya baridi inahitaji tabaka za ziada na hakuna aibu kujifunga vizuri.",
        "Kuwa na joto - kuumia kwa baridi si sifa inayostahili kuwa nayo.",
        "Natumai baridi haikuzuii kufanya unachohitaji leo.",
        "Jifunge vizuri - ni bora kuvaa zaidi kuliko kutetemeka.",
        "Baridi kama hiyo inastahili kinywaji cha moto na blanketi, angalau.",
        "Kuwa na joto huko nje - hii si siku ya kuvumilia bila nguo za kutosha.",
        "Natumai uko mahali pa joto sasa hivi, au unaelekea huko hivi karibuni.",
        "Jifunge vizuri - ni bora kuwa salama na wa joto kuliko mtindo na kuhisi baridi.",
    ],
    "fr": [
        "Reste au chaud là-bas !",
        "Couvre-toi bien - les jours froids demandent des couches chaudes.",
        "Brr, ça a l'air glacial ! J'espère que tu as un coin douillet pour te réchauffer.",
        "Reste au chaud là-bas - les couches sont tes amies aujourd'hui.",
        "Couvre-toi bien - c'est le genre de froid qui te surprend.",
        "Brr ! J'espère que tu as un endroit douillet pour te réchauffer.",
        "Les jours froids sont faits pour les boissons chaudes - va en chercher une.",
        "Reste bien au chaud - le froid ne vaut pas la peine d'être combattu sans le bon équipement.",
        "J'espère que tu as un coin chaud où te retirer aujourd'hui.",
        "Le temps froid demande des couches supplémentaires et aucune honte à bien se couvrir.",
        "Reste au chaud - les engelures ne sont pas un trait de caractère qui vaut la peine.",
        "J'espère que le froid ne t'empêche pas de faire ce que tu dois faire aujourd'hui.",
        "Mets plusieurs couches - mieux vaut trop habillé que grelotant.",
        "Un froid comme ça mérite une boisson chaude et une couverture, au minimum.",
        "Reste au chaud là-bas - ce n'est pas le jour pour tenir le coup sans être assez couvert.",
        "J'espère que tu es quelque part au chaud maintenant, ou que tu y vas bientôt.",
        "Couvre-toi bien - mieux vaut être prudent et chaud que stylé et gelé.",
    ],
}

WEATHER_HOT_RESPONSES = {
    "en": [
        "Stay cool and drink plenty of water!",
        "Phew, sounds hot! Find some shade if you can.",
        "Hot days call for hydration - take care out there.",
        "Stay cool and keep that water bottle close today.",
        "Heat like that is no joke - find shade whenever you can.",
        "Hydrate constantly - that's the move on a hot day like this.",
        "Hope you've got somewhere with decent air conditioning today.",
        "Hot days call for patience and a lot of cold water.",
        "Stay cool out there - heat exhaustion sneaks up faster than you'd think.",
        "Hope you can find some shade and a cold drink soon.",
        "Heat like this is exhausting just to exist in - take it easy.",
        "Stay cool - maybe save the heavy stuff for when it cools down.",
        "Hope you've got a fan, AC, or at least a cold drink nearby.",
        "That kind of heat deserves a slower pace today.",
        "Stay hydrated and don't push too hard in that heat.",
        "Hope you find a breeze or some shade to cool down in.",
        "Heat waves are rough - take care of yourself out there.",
    ],
    "sw": [
        "Jikinge na joto na unywe maji mengi!",
        "Hiyo inasikika ya joto! Tafuta kivuli ukiweza.",
        "Siku za joto zinahitaji maji - jihadhari huko nje.",
        "Kuwa baridi na ushike chupa hiyo ya maji karibu leo.",
        "Joto kama hilo si mzaha - tafuta kivuli wakati wowote unapoweza.",
        "Kunywa maji kila wakati - hilo ndilo la kufanya siku ya joto kama hii.",
        "Natumai una mahali na kiyoyozi kizuri leo.",
        "Siku za joto zinahitaji uvumilivu na maji baridi mengi.",
        "Kuwa baridi huko nje - uchovu wa joto unakuja haraka zaidi ya unavyofikiria.",
        "Natumai unapata kivuli na kinywaji baridi hivi karibuni.",
        "Joto kama hilo linachosha tu kuwepo ndani yake - pumzika.",
        "Kuwa baridi - labda hifadhi mambo mazito kwa wakati itakapopoa.",
        "Natumai una feni, kiyoyozi, au angalau kinywaji baridi karibu.",
        "Joto la aina hiyo linastahili kasi ndogo leo.",
        "Kuwa na maji ya kutosha na usisukume sana kwenye joto hilo.",
        "Natumai unapata upepo au kivuli cha kupoa.",
        "Mawimbi ya joto ni magumu - jitunze huko nje.",
    ],
    "fr": [
        "Reste au frais et bois beaucoup d'eau !",
        "Pfiou, ça a l'air chaud ! Trouve de l'ombre si tu peux.",
        "Les jours chauds demandent de l'hydratation - prends soin de toi là-bas.",
        "Reste au frais et garde cette bouteille d'eau à portée aujourd'hui.",
        "Une chaleur comme ça, ce n'est pas une blague - trouve de l'ombre quand tu peux.",
        "Hydrate-toi constamment - c'est le mot d'ordre par une journée chaude comme ça.",
        "J'espère que tu as un endroit avec une bonne climatisation aujourd'hui.",
        "Les journées chaudes demandent de la patience et beaucoup d'eau fraîche.",
        "Reste au frais là-bas - l'épuisement par la chaleur arrive plus vite qu'on ne le pense.",
        "J'espère que tu trouveras de l'ombre et une boisson fraîche bientôt.",
        "Une telle chaleur est épuisante juste à exister dans - vas-y doucement.",
        "Reste au frais - garde peut-être les choses lourdes pour quand ça se refroidira.",
        "J'espère que tu as un ventilateur, une clim, ou au moins une boisson fraîche à proximité.",
        "Une chaleur comme ça mérite un rythme plus lent aujourd'hui.",
        "Reste hydraté et ne force pas trop dans cette chaleur.",
        "J'espère que tu trouveras une brise ou de l'ombre pour te rafraîchir.",
        "Les canicules sont dures - prends soin de toi là-bas.",
    ],
}

# --- Third wave of response banks ------------------------------------------

WEATHER_RAIN_RESPONSES = {
    "en": [
        "Stay dry out there! Good day for staying cozy inside.",
        "Rainy days are perfect for a story or a good book.",
        "Don't forget an umbrella if you're heading out!",
        "Rainy days are perfect for staying in, if that's an option for you.",
        "Don't forget an umbrella if you're heading out in that.",
        "There's something cozy about rain, as long as you're not stuck out in it.",
        "Hope you've got a dry place to wait it out if needed.",
        "Rain's a good excuse for tea, a blanket, and slowing down.",
        "Stay dry out there - rain has a way of soaking through anything.",
        "Hope the rain isn't messing with your plans too much today.",
        "Rainy days have their own kind of quiet charm.",
        "Grab a raincoat or umbrella if you're stepping out in that.",
        "Rain sounds nice from indoors, less nice if you're caught in it.",
        "Hope you can enjoy the rain rather than fight it today.",
        "Stay dry, and watch your step if it's slippery out there.",
        "Rainy weather is basically nature's permission to slow down.",
        "Hope you've got something warm to drink while it pours.",
    ],
    "sw": [
        "Jikinge na mvua huko nje! Siku nzuri ya kukaa ndani kwa joto.",
        "Siku za mvua ni nzuri kwa hadithi au kitabu kizuri.",
        "Usisahau mwavuli ukienda nje!",
        "Siku za mvua ni nzuri kwa kukaa ndani, kama hilo ni chaguo lako.",
        "Usisahau mwavuli kama unaenda nje kwenye hiyo.",
        "Kuna jambo la kustarehesha kuhusu mvua, mradi tu hauko nje ukikwama.",
        "Natumai una mahali pakavu kusubiri ikipita kama inahitajika.",
        "Mvua ni sababu nzuri ya chai, blanketi, na kupunguza kasi.",
        "Kuwa mkavu huko nje - mvua ina njia ya kuloweka kila kitu.",
        "Natumai mvua haiharibu mipango yako sana leo.",
        "Siku za mvua zina haiba yake ya kimya.",
        "Beba koti la mvua au mwavuli kama unatoka nje kwenye hiyo.",
        "Mvua inasikika vizuri kutoka ndani, si vizuri sana ukinaswa nayo.",
        "Natumai unaweza kufurahia mvua badala ya kuipambana leo.",
        "Kuwa mkavu, na angalia hatua zako kama nje kunatelezesha.",
        "Hali ya mvua kimsingi ni ruhusa ya asili kupunguza kasi.",
        "Natumai una kinywaji cha moto wakati inanyesha.",
    ],
    "fr": [
        "Reste sec là-bas ! Belle journée pour rester confortable à l'intérieur.",
        "Les jours de pluie sont parfaits pour une histoire ou un bon livre.",
        "N'oublie pas un parapluie si tu sors !",
        "Les jours de pluie sont parfaits pour rester à l'intérieur, si c'est une option pour toi.",
        "N'oublie pas un parapluie si tu sors dans ça.",
        "Il y a quelque chose de douillet dans la pluie, tant que tu n'es pas coincé dedans.",
        "J'espère que tu as un endroit sec pour attendre si besoin.",
        "La pluie est une bonne excuse pour du thé, une couverture, et ralentir.",
        "Reste au sec là-bas - la pluie a une façon de tout tremper.",
        "J'espère que la pluie ne perturbe pas trop tes plans aujourd'hui.",
        "Les jours de pluie ont leur propre charme tranquille.",
        "Prends un imperméable ou un parapluie si tu sors dans ça.",
        "La pluie semble agréable de l'intérieur, moins agréable si tu es pris dedans.",
        "J'espère que tu pourras profiter de la pluie plutôt que la combattre aujourd'hui.",
        "Reste au sec, et fais attention où tu marches si c'est glissant là-bas.",
        "Le temps pluvieux est essentiellement la permission de la nature de ralentir.",
        "J'espère que tu as quelque chose de chaud à boire pendant qu'il pleut.",
    ],
}

WEATHER_SNOW_RESPONSES = {
    "en": [
        "Snow days can be lovely - stay warm and watch it fall!",
        "Hope you're bundled up if you're out in the snow.",
        "Snow always makes everything look so peaceful.",
        "Snow days have a quiet magic to them, even as an adult.",
        "Stay warm and watch your footing if it's slippery out there.",
        "Hope the snow is the pretty kind and not the disruptive kind today.",
        "There's something nice about the world going quiet under snow.",
        "Bundle up well if you're heading out into that.",
        "Snow's beautiful until you have to drive in it - stay careful.",
        "Hope you get to enjoy it rather than just shovel it.",
        "Stay warm - snow looks cozy but the cold underneath it is real.",
        "Hope today's snow doesn't disrupt your plans too much.",
        "There's a stillness to snowy days that's honestly kind of nice.",
        "Watch for ice under that snow - it's sneakier than it looks.",
        "Hope you've got warm boots if you're heading out in it.",
        "Snow days are a good excuse for hot chocolate, if you ask me.",
        "Stay cozy - let the snow be someone else's problem today if you can.",
    ],
    "sw": [
        "Siku za theluji zinaweza kuwa nzuri - kaa na joto na utazame ikinyesha!",
        "Natumai umejifunika vizuri ukiwa nje kwenye theluji.",
        "Theluji daima inafanya kila kitu kionekane na amani.",
        "Siku za theluji zina uchawi wa kimya, hata kwa mtu mzima.",
        "Kuwa na joto na angalia hatua zako kama nje kunatelezesha.",
        "Natumai theluji ni aina nzuri na si ya kuvuruga leo.",
        "Kuna jambo zuri kuhusu dunia kutulia chini ya theluji.",
        "Jifunge vizuri kama unaenda nje kwenye hiyo.",
        "Theluji ni nzuri hadi unapolazimika kuendesha gari ndani yake - kuwa makini.",
        "Natumai unapata kuifurahia badala ya kuichimba tu.",
        "Kuwa na joto - theluji inaonekana nzuri lakini baridi chini yake ni ya kweli.",
        "Natumai theluji ya leo haivuruvuru mipango yako sana.",
        "Kuna utulivu wa siku za theluji ambao ni mzuri kwa kweli.",
        "Angalia barafu chini ya theluji hiyo - ni ya hila zaidi ya inavyoonekana.",
        "Natumai una buti za joto kama unaenda nje ndani yake.",
        "Siku za theluji ni sababu nzuri ya chokoleti ya moto, kwa mtazamo wangu.",
        "Kuwa na joto - acha theluji iwe tatizo la mtu mwingine leo kama unaweza.",
    ],
    "fr": [
        "Les jours de neige peuvent être magnifiques - reste au chaud et regarde-la tomber !",
        "J'espère que tu es bien couvert si tu es dans la neige.",
        "La neige rend toujours tout si paisible.",
        "Les jours de neige ont une magie tranquille, même adulte.",
        "Reste au chaud et fais attention où tu marches si c'est glissant là-bas.",
        "J'espère que la neige sera du genre joli et pas perturbateur aujourd'hui.",
        "Il y a quelque chose d'agréable dans le monde qui devient silencieux sous la neige.",
        "Couvre-toi bien si tu sors dans ça.",
        "La neige est belle jusqu'à ce qu'il faille conduire dedans - sois prudent.",
        "J'espère que tu pourras en profiter plutôt que juste la déneiger.",
        "Reste au chaud - la neige a l'air douillette mais le froid dessous est bien réel.",
        "J'espère que la neige d'aujourd'hui ne perturbe pas trop tes plans.",
        "Il y a une tranquillité dans les jours de neige qui est honnêtement plutôt agréable.",
        "Fais attention au verglas sous cette neige - il est plus sournois qu'il n'a l'air.",
        "J'espère que tu as des bottes chaudes si tu sors dedans.",
        "Les jours de neige sont une bonne excuse pour du chocolat chaud, si tu me demandes.",
        "Reste douillet - laisse la neige être le problème de quelqu'un d'autre aujourd'hui si tu peux.",
    ],
}

WEATHER_WINDY_RESPONSES = {
    "en": [
        "Hold onto your hat out there!",
        "Windy days can be wild - stay safe!",
        "Hope the wind isn't causing you too much trouble.",
        "Windy days are wild - hold onto your hat, literally.",
        "Hope nothing important blows away today!",
        "That kind of wind makes everything feel a little more dramatic.",
        "Stay steady out there if it's really gusting.",
        "Wind like that has a way of waking you right up.",
        "Hope it's more invigorating than annoying today.",
        "Watch for flying debris if it's gusting that hard.",
        "Windy weather always makes a simple walk feel like an adventure.",
        "Hope your hair survives the day, against all odds.",
        "That much wind makes everything feel a bit more alive, honestly.",
        "Hold onto loose papers and hats today - the wind means business.",
        "Hope it calms down before you need to be out in it for long.",
        "Windy days are nature's way of testing your umbrella's loyalty.",
        "Stay grounded out there - quite literally, given the wind.",
    ],
    "sw": [
        "Shikilia kofia yako huko nje!",
        "Siku za upepo zinaweza kuwa kali - jihadhari!",
        "Natumai upepo hausababishi shida nyingi kwako.",
        "Siku za upepo ni za kushangaza - shika kofia yako, kihalisia.",
        "Natumai hakuna kitu muhimu kinachopeperushwa leo!",
        "Upepo wa aina hiyo unafanya kila kitu kuhisi kidogo zaidi cha kusisimua.",
        "Kuwa thabiti huko nje kama unavuma kweli.",
        "Upepo kama huo una njia ya kukuamsha kabisa.",
        "Natumai ni wa kuburudisha zaidi kuliko wa kukera leo.",
        "Angalia vitu vinavyoruka kama unavuma kwa nguvu hivyo.",
        "Hali ya upepo daima inafanya matembezi rahisi kuhisi kama tukio la kusisimua.",
        "Natumai nywele zako zinasalia salama leo, kinyume na uwezekano.",
        "Upepo mwingi kama huo unafanya kila kitu kuhisi hai zaidi, kwa kweli.",
        "Shika makaratasi na kofia zilizolegea leo - upepo una nia.",
        "Natumai unatulia kabla ya kuhitaji kuwa nje kwa muda mrefu.",
        "Siku za upepo ni njia ya asili ya kupima uaminifu wa mwavuli wako.",
        "Kaa imara huko nje - kihalisia, kutokana na upepo.",
    ],
    "fr": [
        "Tiens bien ton chapeau là-bas !",
        "Les jours de vent peuvent être sauvages - reste prudent !",
        "J'espère que le vent ne te cause pas trop de problèmes.",
        "Les jours de vent sont fous - accroche-toi à ton chapeau, littéralement.",
        "J'espère que rien d'important ne s'envolera aujourd'hui !",
        "Un vent comme ça rend tout un peu plus dramatique.",
        "Reste stable là-bas si ça souffle vraiment fort.",
        "Un vent comme ça a une façon de te réveiller complètement.",
        "J'espère que c'est plus stimulant qu'agaçant aujourd'hui.",
        "Fais attention aux débris volants si ça souffle aussi fort.",
        "Le temps venteux fait toujours d'une simple marche une aventure.",
        "J'espère que tes cheveux survivront à la journée, contre toute attente.",
        "Autant de vent rend tout un peu plus vivant, honnêtement.",
        "Tiens bien les papiers et chapeaux aujourd'hui - le vent ne plaisante pas.",
        "J'espère que ça se calmera avant que tu doives rester dedans longtemps.",
        "Les jours de vent sont la façon de la nature de tester la loyauté de ton parapluie.",
        "Reste ancré là-bas - assez littéralement, vu le vent.",
    ],
}

HOLIDAY_SMALLTALK_RESPONSES = {
    "en": [
        "Happy holidays to you too! Hope it's a wonderful time.",
        "Same to you! Wishing you joy this season.",
        "Thank you! I hope your celebrations are full of good memories.",
        "Holidays have a way of feeling both exciting and exhausting at once.",
        "Hope whatever you're celebrating brings you some real joy.",
        "Holiday season always sneaks up faster than expected, doesn't it?",
        "Hope you get some genuine downtime amid all the holiday hustle.",
        "Whatever traditions you're keeping, I hope they feel meaningful this year.",
        "Holidays are a good excuse to slow down and actually connect with people.",
        "Hope the holiday season treats you gently this year.",
        "However you celebrate, or don't, I hope it's a good stretch of time.",
        "Holiday stress is real - I hope you find moments of actual rest in there.",
        "Hope you get to spend it with people who make it feel worthwhile.",
        "Holidays hit different every year - how's this one feeling so far?",
        "Whatever the holiday looks like for you, I hope it's a good one.",
        "Hope the festive chaos comes with at least as much joy as stress.",
        "Holiday season is a lot, but I hope the good parts outweigh the rest.",
    ],
    "sw": [
        "Sikukuu njema kwako pia! Natumai ni wakati mzuri.",
        "Vivyo hivyo kwako! Nakutakia furaha msimu huu.",
        "Asante! Natumai sherehe zako zimejaa kumbukumbu nzuri.",
        "Sikukuu zina njia ya kuhisi za kusisimua na za kuchosha kwa wakati mmoja.",
        "Natumai chochote unachosherehekea kinakuletea furaha ya kweli.",
        "Msimu wa sikukuu daima unakuja haraka zaidi ya ilivyotarajiwa, sivyo?",
        "Natumai unapata mapumziko ya kweli katikati ya shughuli zote za sikukuu.",
        "Vyovyote desturi unazoendeleza, natumai zinahisi za maana mwaka huu.",
        "Sikukuu ni sababu nzuri ya kupunguza kasi na kuungana na watu kwa kweli.",
        "Natumai msimu wa sikukuu unakutendea kwa upole mwaka huu.",
        "Vyovyote unavyosherehekea, au hausherehekei, natumai ni kipindi kizuri.",
        "Msongo wa sikukuu ni wa kweli - natumai unapata nyakati za pumziko la kweli.",
        "Natumai unapata kuitumia na watu wanaoifanya kuwa ya maana.",
        "Sikukuu zinahisi tofauti kila mwaka - hii inahisi vipi hadi sasa?",
        "Vyovyote sikukuu inavyoonekana kwako, natumai ni nzuri.",
        "Natumai msukosuko wa sherehe unakuja na furaha angalau sawa na msongo.",
        "Msimu wa sikukuu ni mengi, lakini natumai sehemu nzuri zinashinda zilizosalia.",
    ],
    "fr": [
        "Joyeuses fêtes à toi aussi ! J'espère que c'est un moment merveilleux.",
        "Pareillement ! Je te souhaite de la joie cette saison.",
        "Merci ! J'espère que tes célébrations sont pleines de bons souvenirs.",
        "Les fêtes ont une façon de sembler à la fois excitantes et épuisantes en même temps.",
        "J'espère que ce que tu célèbres t'apporte une vraie joie.",
        "La période des fêtes arrive toujours plus vite que prévu, non ?",
        "J'espère que tu trouves du vrai temps de repos au milieu de toute cette agitation.",
        "Quelles que soient les traditions que tu gardes, j'espère qu'elles ont du sens cette année.",
        "Les fêtes sont une bonne excuse pour ralentir et vraiment se connecter aux gens.",
        "J'espère que la période des fêtes te traite avec douceur cette année.",
        "Quelle que soit ta façon de célébrer, ou pas, j'espère que c'est une bonne période.",
        "Le stress des fêtes est réel - j'espère que tu trouves des moments de vrai repos.",
        "J'espère que tu pourras la passer avec des gens qui la rendent précieuse.",
        "Les fêtes sont différentes chaque année - comment se sent celle-ci jusqu'ici ?",
        "Quelle que soit l'apparence des fêtes pour toi, j'espère qu'elles sont bonnes.",
        "J'espère que le chaos festif vient avec au moins autant de joie que de stress.",
        "La période des fêtes, c'est beaucoup, mais j'espère que les bons côtés l'emportent.",
    ],
}

LEARNING_RESPONSES = {
    "en": [
        "That's great! Learning new things keeps life interesting. What are you picking up?",
        "Good for you! What's the hardest part so far?",
        "I love that. Learning takes patience - how's it going?",
        "Learning something new is one of the best feelings - what's clicking for you?",
        "I love hearing about new skills people are picking up.",
        "There's something great about being a beginner again at something.",
        "What got you started on this particular thing?",
        "Learning curves are humbling, but they're also kind of exciting.",
        "I imagine it's satisfying to watch yourself improve at this.",
        "What's the hardest part of it so far?",
        "New skills are basically just patience paying off slowly.",
        "I'd love to hear how far you've come with it.",
        "Learning something just for the joy of it is underrated.",
        "What made you want to pick this up in the first place?",
        "I bet there's a moment where it suddenly started making sense.",
        "Keep going - skill-building is rarely a straight line.",
        "Tell me about the most recent thing that clicked for you.",
    ],
    "sw": [
        "Hiyo ni nzuri! Kujifunza mambo mapya kunafanya maisha kuwa ya kuvutia. Unajifunza nini?",
        "Vizuri kwako! Sehemu ngumu zaidi mpaka sasa ni ipi?",
        "Ninapenda hilo. Kujifunza kunahitaji uvumilivu - inaendaje?",
        "Kujifunza kitu kipya ni mojawapo ya hisia bora zaidi - ni nini kinachoingia kwako?",
        "Ninapenda kusikia kuhusu ujuzi mpya watu wanaojifunza.",
        "Kuna jambo kubwa kuhusu kuwa mwanzilishi tena kwenye kitu.",
        "Ni nini kilichokuanzisha kwenye kitu hiki hasa?",
        "Mikondo ya kujifunza inakufanya unyenyekevu, lakini pia inasisimua kidogo.",
        "Nadhani ni jambo la kuridhisha kujiona unaboreka kwenye hili.",
        "Ni sehemu gani ngumu zaidi hadi sasa?",
        "Ujuzi mpya kimsingi ni uvumilivu unaolipa polepole.",
        "Ningependa kusikia umefika mbali kiasi gani na hilo.",
        "Kujifunza kitu kwa furaha tu ni jambo lisilothaminiwa vya kutosha.",
        "Ni nini kilichokufanya utake kuchukua hili hasa?",
        "Nadhani kuna wakati ulioingia ghafla.",
        "Endelea - ujengaji wa ujuzi mara chache ni mstari wa moja kwa moja.",
        "Niambie kuhusu kitu cha karibuni zaidi kilichoingia kwako.",
    ],
    "fr": [
        "C'est génial ! Apprendre de nouvelles choses rend la vie intéressante. Qu'apprends-tu ?",
        "Bravo à toi ! Quelle est la partie la plus difficile jusqu'à présent ?",
        "J'adore ça. Apprendre demande de la patience - comment ça se passe ?",
        "Apprendre quelque chose de nouveau est l'une des meilleures sensations - qu'est-ce qui fait tilt pour toi ?",
        "J'aime entendre parler des nouvelles compétences que les gens développent.",
        "Il y a quelque chose de génial à être débutant à nouveau dans quelque chose.",
        "Qu'est-ce qui t'a lancé sur cette chose en particulier ?",
        "Les courbes d'apprentissage sont humiliantes, mais aussi un peu excitantes.",
        "J'imagine que c'est satisfaisant de te voir t'améliorer là-dedans.",
        "Quelle est la partie la plus difficile jusqu'ici ?",
        "Les nouvelles compétences sont essentiellement de la patience qui paie lentement.",
        "J'aimerais savoir jusqu'où tu en es arrivé.",
        "Apprendre quelque chose juste pour le plaisir est sous-estimé.",
        "Qu'est-ce qui t'a donné envie de t'y mettre au départ ?",
        "Je parie qu'il y a un moment où ça a soudainement commencé à avoir du sens.",
        "Continue - le développement de compétences est rarement une ligne droite.",
        "Raconte-moi la dernière chose qui a fait tilt pour toi.",
    ],
}

MOTIVATION_GOALS_RESPONSES = {
    "en": [
        "That's a great goal to work toward. What's your next step?",
        "I admire that ambition! What's driving you toward it?",
        "Goals give direction - I hope you get there.",
        "Goals are basically just future you, waiting to be met.",
        "Whatever you're working toward, I hope the momentum keeps building.",
        "It's worth celebrating the effort, not just the finish line.",
        "What's the next small step toward that goal?",
        "I believe progress counts even when it's slower than you'd like.",
        "Big goals are just a bunch of small ones stacked together.",
        "Tell me what's driving you toward this one.",
        "Motivation comes and goes - showing up anyway is the real skill.",
        "I hope this goal feels as good to chase as it will to reach.",
        "What would it feel like to actually get there?",
        "Keep your eyes on the progress, not just the distance left.",
        "I'm rooting for you on this one, for what that's worth.",
        "Goals worth having are usually a little uncomfortable to chase - that's normal.",
        "However far you've gotten, that's real progress worth recognizing.",
    ],
    "sw": [
        "Hilo ni lengo zuri la kufanyia kazi. Hatua yako inayofuata ni ipi?",
        "Ninaipenda azma hiyo! Ni nini kinakusukuma kuifuata?",
        "Malengo yanatoa mwelekeo - natumai utafika huko.",
        "Malengo kimsingi ni wewe wa baadaye, ukisubiri kufikiwa.",
        "Chochote unachofanyia kazi, natumai kasi inaendelea kujengeka.",
        "Inastahili kusherehekea juhudi, si tu mstari wa mwisho.",
        "Ni hatua gani ndogo inayofuata kuelekea lengo hilo?",
        "Ninaamini maendeleo yanahesabika hata yakiwa polepole zaidi ya unavyotaka.",
        "Malengo makubwa ni mkusanyiko wa madogo yaliyowekwa pamoja.",
        "Niambie ni nini kinachokusukuma kuelekea hili.",
        "Msukumo unakuja na kuondoka - kujitokeza hata hivyo ndiyo ujuzi wa kweli.",
        "Natumai lengo hili linahisi vizuri kufuatilia kama litakavyohisi kufikiwa.",
        "Itahisi vipi kufika hapo kwa kweli?",
        "Weka macho yako kwenye maendeleo, si tu umbali uliosalia.",
        "Ninakushangilia kwenye hili, kwa thamani yake.",
        "Malengo yanayostahili kuwa nayo kawaida ni magumu kidogo kufuatilia - hilo ni la kawaida.",
        "Vyovyote umefika mbali, hayo ni maendeleo ya kweli yanayostahili kutambuliwa.",
    ],
    "fr": [
        "C'est un excellent objectif à poursuivre. Quelle est ta prochaine étape ?",
        "J'admire cette ambition ! Qu'est-ce qui te pousse vers ça ?",
        "Les objectifs donnent une direction - j'espère que tu y arriveras.",
        "Les objectifs, c'est essentiellement le futur toi, qui attend d'être atteint.",
        "Quoi que tu poursuives, j'espère que l'élan continue de grandir.",
        "Ça vaut la peine de célébrer l'effort, pas juste la ligne d'arrivée.",
        "Quelle est la prochaine petite étape vers cet objectif ?",
        "Je crois que le progrès compte même quand il est plus lent que tu le voudrais.",
        "Les grands objectifs sont juste un tas de petits empilés ensemble.",
        "Dis-moi ce qui te pousse vers celui-ci.",
        "La motivation vient et va - se présenter quand même est la vraie compétence.",
        "J'espère que cet objectif est aussi agréable à poursuivre qu'à atteindre.",
        "Ça ferait quoi d'y arriver vraiment ?",
        "Garde les yeux sur le progrès, pas juste la distance qui reste.",
        "Je te soutiens sur ce coup-là, pour ce que ça vaut.",
        "Les objectifs qui valent la peine sont généralement un peu inconfortables à poursuivre - c'est normal.",
        "Quel que soit le chemin parcouru, c'est un vrai progrès à reconnaître.",
    ],
}

NOSTALGIA_RESPONSES = {
    "en": [
        "Nostalgia is bittersweet, isn't it? What do you miss most?",
        "Those memories sound meaningful to you. Thanks for sharing.",
        "It's nice to look back sometimes. What made that time special?",
        "Nostalgia is bittersweet, isn't it? What do you miss most?",
        "Those memories sound meaningful to you. Thanks for sharing.",
        "It's nice to look back sometimes. What made that time special?",
        "There's something about old memories that feels both close and far away.",
        "I love hearing about the past through someone's actual memory of it.",
        "What's the one detail from back then that still sticks with you?",
        "Nostalgia has a way of softening even the hard parts of a memory.",
        "Sounds like that time left a real mark on you.",
        "I'd love to hear more about what made it so memorable.",
        "Old memories are basically little time capsules - thanks for opening one.",
        "What would you tell your past self, looking back now?",
        "It's interesting how certain memories just stay vivid forever.",
        "However far back this goes, it clearly still matters to you.",
        "Some memories are worth revisiting again and again - sounds like this is one.",
    ],
    "sw": [
        "Kukumbuka zamani ni hisia mchanganyiko, sivyo? Unakosa nini zaidi?",
        "Kumbukumbu hizo zinasikika kuwa na maana kwako. Asante kwa kushiriki.",
        "Ni vizuri kuangalia nyuma mara kwa mara. Ni nini kilifanya wakati huo kuwa wa pekee?",
        "Hamu ya zamani ni tamu na chungu, sivyo? Unakosa nini zaidi?",
        "Kumbukumbu hizo zinasikika kuwa na maana kwako. Asante kwa kushiriki.",
        "Ni vizuri kuangalia nyuma wakati mwingine. Ni nini kilichofanya wakati huo kuwa maalum?",
        "Kuna jambo kuhusu kumbukumbu za zamani linalohisi karibu na mbali kwa wakati mmoja.",
        "Ninapenda kusikia kuhusu zamani kupitia kumbukumbu ya kweli ya mtu.",
        "Ni undani gani mmoja kutoka wakati huo unaokaa nawe hadi sasa?",
        "Hamu ya zamani ina njia ya kulainisha hata sehemu ngumu za kumbukumbu.",
        "Inasikika kama wakati huo umekuachia athari ya kweli.",
        "Ningependa kusikia zaidi kuhusu kilichoufanya kukumbukwa hivyo.",
        "Kumbukumbu za zamani kimsingi ni vibaa vidogo vya muda - asante kwa kufungua kimoja.",
        "Ungemwambia nini wewe wa zamani, ukiangalia nyuma sasa?",
        "Inavutia jinsi kumbukumbu fulani zinasalia wazi milele.",
        "Vyovyote hii inarudi nyuma kiasi gani, dhahiri bado inakuhusu.",
        "Kumbukumbu zingine zinastahili kutembelewa tena na tena - inasikika hii ni mojawapo.",
    ],
    "fr": [
        "La nostalgie est douce-amère, non ? Qu'est-ce qui te manque le plus ?",
        "Ces souvenirs semblent importants pour toi. Merci de partager.",
        "C'est agréable de regarder en arrière parfois. Qu'est-ce qui rendait cette époque spéciale ?",
        "La nostalgie est douce-amère, non ? Qu'est-ce qui te manque le plus ?",
        "Ces souvenirs semblent significatifs pour toi. Merci de les partager.",
        "C'est agréable de regarder en arrière parfois. Qu'est-ce qui rendait ce moment spécial ?",
        "Il y a quelque chose dans les vieux souvenirs qui semble à la fois proche et lointain.",
        "J'aime entendre parler du passé à travers le vrai souvenir de quelqu'un.",
        "Quel est le détail de cette époque qui reste encore avec toi ?",
        "La nostalgie a une façon d'adoucir même les parties difficiles d'un souvenir.",
        "On dirait que cette période t'a vraiment marqué.",
        "J'aimerais en savoir plus sur ce qui le rendait si mémorable.",
        "Les vieux souvenirs sont essentiellement de petites capsules temporelles - merci d'en avoir ouvert une.",
        "Que dirais-tu à ton ancien toi, en regardant en arrière maintenant ?",
        "C'est intéressant comme certains souvenirs restent vifs pour toujours.",
        "Quelle que soit l'ancienneté, ça compte clairement encore pour toi.",
        "Certains souvenirs valent la peine d'être revisités encore et encore - on dirait que c'est le cas ici.",
    ],
}

FUTURE_PLANS_RESPONSES = {
    "en": [
        "That sounds exciting! I hope it goes exactly as you're hoping.",
        "Nice, something to look forward to! Tell me more.",
        "I hope it turns out wonderfully for you.",
        "That sounds exciting! I hope it goes exactly as you're hoping.",
        "Nice, something to look forward to! Tell me more.",
        "I hope it turns out wonderfully for you.",
        "Future plans are basically hope with a timeline - I love that.",
        "What part of it are you most excited about?",
        "Here's hoping the planning is as fun as the actual thing will be.",
        "That sounds like something worth getting excited about now.",
        "I hope it all comes together the way you're picturing it.",
        "What's the first step toward making that happen?",
        "Having something to look forward to changes the whole mood of a week.",
        "I'd love to hear how the planning is going so far.",
        "Whatever happens, I hope the anticipation alone brings you some joy.",
        "That's the kind of plan that's fun to just think about.",
        "Here's hoping it goes even better than you're imagining.",
    ],
    "sw": [
        "Hiyo inasikika ya kufurahisha! Natumai itakwenda kama unavyotaka.",
        "Vizuri, kitu cha kutazamia! Niambie zaidi.",
        "Natumai itakuwa nzuri kwako.",
        "Hiyo inasikika ya kusisimua! Natumai itakwenda hasa kama unavyotarajia.",
        "Vizuri, kitu cha kutarajia! Niambie zaidi.",
        "Natumai itakuwa nzuri kwako.",
        "Mipango ya baadaye kimsingi ni matumaini yenye ratiba - napenda hilo.",
        "Ni sehemu gani unayoifurahia zaidi?",
        "Hii ni kwa kupanga kuwa kufurahisha kama kitu chenyewe kitakavyokuwa.",
        "Hiyo inasikika kama kitu kinachostahili kusisimua sasa.",
        "Natumai kila kitu kinakuja pamoja kama unavyokitazamia.",
        "Ni hatua gani ya kwanza kuelekea kufanya hilo litokee?",
        "Kuwa na kitu cha kutarajia kinabadilisha hali nzima ya wiki.",
        "Ningependa kusikia upangaji unaendaje hadi sasa.",
        "Vyovyote itakavyokuwa, natumai matarajio peke yake yanakuletea furaha.",
        "Hiyo ni aina ya mpango unaofurahisha kufikiria tu.",
        "Hii ni kwa kuwa bora zaidi kuliko unavyofikiria.",
    ],
    "fr": [
        "Ça a l'air excitant ! J'espère que ça se passera exactement comme tu l'espères.",
        "Cool, quelque chose à attendre avec impatience ! Dis-m'en plus.",
        "J'espère que ça se passera merveilleusement bien pour toi.",
        "Ça semble excitant ! J'espère que ça se passera exactement comme tu l'espères.",
        "Chouette, quelque chose à attendre avec impatience ! Dis-m'en plus.",
        "J'espère que ça se passera merveilleusement pour toi.",
        "Les projets d'avenir sont essentiellement de l'espoir avec un calendrier - j'aime ça.",
        "Quelle partie t'excite le plus ?",
        "En espérant que la planification soit aussi amusante que la chose elle-même le sera.",
        "Ça semble être le genre de chose qui vaut la peine d'être excité maintenant.",
        "J'espère que tout se mettra en place comme tu l'imagines.",
        "Quelle est la première étape pour que ça arrive ?",
        "Avoir quelque chose à attendre change toute l'ambiance d'une semaine.",
        "J'aimerais savoir comment se passe la planification jusqu'ici.",
        "Quoi qu'il arrive, j'espère que l'anticipation seule t'apporte de la joie.",
        "C'est le genre de projet amusant juste à imaginer.",
        "En espérant que ça se passe encore mieux que tu ne l'imagines.",
    ],
}

GAMING_RESPONSES = {
    "en": [
        "Gaming is a great way to unwind! What are you playing these days?",
        "I can't play games myself, but I love hearing about them. What's it about?",
        "Nice! Any favorite genre or game right now?",
        "Gaming is a great way to unwind! What are you playing these days?",
        "I can't play games myself, but I love hearing about them. What's it about?",
        "Nice! Any favorite genre or game right now?",
        "Games have a way of fully absorbing your attention - what's got yours right now?",
        "I'd love to hear about the best moment you've had in a game recently.",
        "What's the appeal of that one for you - story, mechanics, or just the vibe?",
        "I wish I could actually play, even just to understand the hype.",
        "Gaming sessions sound like a great way to disconnect from everything else.",
        "What's your most memorable gaming moment of all time?",
        "Single-player or multiplayer - what's your usual preference?",
        "I imagine getting fully immersed in a game world is a great escape.",
        "Tell me about a game that genuinely surprised you.",
        "However you're playing, I hope it's the fun kind of challenging.",
        "Gaming's basically interactive storytelling - I find that genuinely cool.",
    ],
    "sw": [
        "Michezo ni njia nzuri ya kupumzika! Unacheza nini siku hizi?",
        "Siwezi kucheza michezo mwenyewe, lakini ninapenda kusikia kuhusu hiyo. Inahusu nini?",
        "Vizuri! Una aina au mchezo unaopenda sasa hivi?",
        "Michezo ya video ni njia nzuri ya kustarehe! Unacheza nini siku hizi?",
        "Siwezi kucheza michezo mwenyewe, lakini napenda kusikia kuhusu hiyo. Inahusu nini?",
        "Vizuri! Aina au mchezo wowote unaopenda zaidi sasa?",
        "Michezo ina njia ya kuvuta uangalifu wako kikamilifu - ni nini kinachokuvuta sasa?",
        "Ningependa kusikia kuhusu wakati mzuri zaidi uliopata kwenye mchezo hivi karibuni.",
        "Ni nini kinachovutia kuhusu huo kwako - hadithi, jinsi unavyofanya kazi, au hali tu?",
        "Natamani ningeweza kucheza kwa kweli, hata tu kuelewa msisimko.",
        "Vikao vya michezo vinasikika kama njia nzuri ya kujitenga na kila kitu kingine.",
        "Ni wakati gani wa mchezo unaokumbukwa zaidi maishani mwako?",
        "Mchezaji mmoja au wachezaji wengi - ni kipi unachopendelea kawaida?",
        "Nadhani kuingia kikamilifu kwenye dunia ya mchezo ni kimbilio kizuri.",
        "Niambie kuhusu mchezo uliokushangaza kwa kweli.",
        "Vyovyote unavyocheza, natumai ni aina ya changamoto inayofurahisha.",
        "Michezo ya video kimsingi ni kusimulia hadithi kwa njia ya kushiriki - naona hilo la kuvutia kwa kweli.",
    ],
    "fr": [
        "Jouer est une excellente façon de se détendre ! À quoi joues-tu ces jours-ci ?",
        "Je ne peux pas jouer moi-même, mais j'aime en entendre parler. Ça parle de quoi ?",
        "Sympa ! Un genre ou jeu préféré en ce moment ?",
        "Les jeux vidéo sont une excellente façon de se détendre ! Tu joues à quoi ces jours-ci ?",
        "Je ne peux pas jouer moi-même, mais j'aime en entendre parler. C'est quoi le concept ?",
        "Chouette ! Un genre ou un jeu préféré en ce moment ?",
        "Les jeux ont une façon d'absorber complètement ton attention - qu'est-ce qui capte la tienne maintenant ?",
        "J'aimerais entendre parler du meilleur moment que tu aies eu dans un jeu récemment.",
        "Qu'est-ce qui t'attire dans celui-là - l'histoire, les mécaniques, ou juste l'ambiance ?",
        "J'aimerais pouvoir vraiment jouer, même juste pour comprendre l'engouement.",
        "Les sessions de jeu semblent être une bonne façon de se déconnecter de tout le reste.",
        "Quel est ton moment de jeu le plus mémorable de tous les temps ?",
        "Solo ou multijoueur - quelle est ta préférence habituelle ?",
        "J'imagine que s'immerger complètement dans un monde de jeu est une belle évasion.",
        "Raconte-moi un jeu qui t'a vraiment surpris.",
        "Quelle que soit ta façon de jouer, j'espère que c'est le bon genre de défi.",
        "Les jeux vidéo, c'est essentiellement de la narration interactive - je trouve ça vraiment cool.",
    ],
}

COOKING_RESPONSES = {
    "en": [
        "Cooking can be so satisfying! What are you making?",
        "I wish I could taste-test for you! How's it turning out?",
        "Sounds delicious already. Need any tips? I might know a thing or two.",
        "Cooking can be so satisfying! What are you making?",
        "I wish I could taste-test for you! How's it turning out?",
        "Sounds delicious already. Need any tips? I might know a thing or two.",
        "There's something great about turning raw ingredients into something good.",
        "What made you decide to cook that today?",
        "I'd love to smell it, even if I can't taste it!",
        "Cooking from scratch is its own kind of small daily victory.",
        "What's the trickiest part of making that?",
        "I bet the kitchen smells amazing right now.",
        "Homemade always sounds better than store-bought to me, for what it's worth.",
        "Tell me how it turned out once you're done!",
        "Cooking's basically chemistry with better snacks at the end.",
        "I hope it tastes as good as it sounds.",
        "What's your go-to dish when you want something reliable and good?",
    ],
    "sw": [
        "Kupika kunaweza kuridhisha sana! Unatengeneza nini?",
        "Ningependa kuweza kuonja kwako! Inaendaje?",
        "Inasikika tamu tayari. Unahitaji vidokezo? Naweza kujua kitu kimoja au viwili.",
        "Kupika kunaweza kuridhisha sana! Unapika nini?",
        "Natamani ningeweza kuonja kwa ajili yako! Inageukaje?",
        "Inasikika kitamu tayari. Unahitaji vidokezo? Naweza kujua kitu kimoja au viwili.",
        "Kuna jambo kubwa kuhusu kubadilisha vitu vibichi kuwa kitu kizuri.",
        "Ni nini kilichokufanya uamue kupika hicho leo?",
        "Ningependa kunusa, hata kama siwezi kuonja!",
        "Kupika kutoka mwanzo ni ushindi mdogo wa kila siku.",
        "Ni sehemu gani ngumu zaidi ya kufanya hicho?",
        "Nadhani jiko linanuka vizuri sasa hivi.",
        "Kilichotengenezwa nyumbani daima kinasikika bora kuliko cha duka kwangu, kwa thamani yake.",
        "Niambie ilivyogeuka mara unapomaliza!",
        "Kupika kimsingi ni kemia na vitafunio bora mwishoni.",
        "Natumai inakaribia kitamu kama inavyosikika.",
        "Ni mlo gani unaoupendelea unapotaka kitu cha kuaminika na kizuri?",
    ],
    "fr": [
        "Cuisiner peut être si satisfaisant ! Que prépares-tu ?",
        "J'aimerais pouvoir goûter pour toi ! Comment ça se présente ?",
        "Ça sonne déjà délicieux. Besoin de conseils ? Je connais peut-être deux ou trois choses.",
        "Cuisiner peut être si satisfaisant ! Qu'est-ce que tu prépares ?",
        "J'aimerais pouvoir goûter pour toi ! Comment ça se présente ?",
        "Ça sonne délicieux déjà. Besoin de conseils ? Je connais peut-être un truc ou deux.",
        "Il y a quelque chose de génial à transformer des ingrédients bruts en quelque chose de bon.",
        "Qu'est-ce qui t'a décidé à cuisiner ça aujourd'hui ?",
        "J'aimerais le sentir, même si je ne peux pas le goûter !",
        "Cuisiner à partir de zéro est sa propre petite victoire quotidienne.",
        "Quelle est la partie la plus délicate pour préparer ça ?",
        "Je parie que la cuisine sent incroyablement bon en ce moment.",
        "Le fait maison sonne toujours mieux que l'acheté en magasin pour moi, pour ce que ça vaut.",
        "Dis-moi comment c'est ressorti une fois que tu as fini !",
        "Cuisiner, c'est essentiellement de la chimie avec de meilleurs snacks à la fin.",
        "J'espère que ça a aussi bon goût que ça en a l'air.",
        "Quel est ton plat de référence quand tu veux quelque chose de fiable et bon ?",
    ],
}

NATURE_OUTDOORS_RESPONSES = {
    "en": [
        "Getting outside is so good for the mind. Enjoy it!",
        "Nature has a way of clearing the head. Where are you headed?",
        "That sounds refreshing! Hope the weather cooperates.",
        "Getting outside is so good for the mind. Enjoy it!",
        "Nature has a way of clearing the head. Where are you headed?",
        "That sounds refreshing! Hope the weather cooperates.",
        "There's something resetting about being outside, away from screens.",
        "I wish I could feel fresh air, even just to understand the appeal.",
        "Hope you find something beautiful out there today.",
        "Outdoor time is underrated self-care, honestly.",
        "What's the best part of being out there for you?",
        "I imagine it's a nice break from everything indoors and digital.",
        "Hope the trail, park, or wherever you're headed treats you well.",
        "Nature's basically free therapy, if you ask me.",
        "I'd love a description of what you're seeing out there.",
        "Hope you come back feeling recharged.",
        "Fresh air and a change of scenery does wonders - enjoy it.",
    ],
    "sw": [
        "Kutoka nje ni nzuri sana kwa akili. Furahia!",
        "Asili ina njia ya kuondoa mawazo. Unaenda wapi?",
        "Hiyo inasikika ya kufurahisha! Natumai hali ya hewa itakuwa nzuri.",
        "Kutoka nje ni vizuri sana kwa akili. Furahia!",
        "Asili ina njia ya kusafisha akili. Unaelekea wapi?",
        "Hiyo inasikika ya kuburudisha! Natumai hali ya hewa itashirikiana.",
        "Kuna jambo la kurekebisha kuhusu kuwa nje, mbali na skrini.",
        "Natamani ningeweza kuhisi hewa safi, hata tu kuelewa mvuto wake.",
        "Natumai unapata kitu kizuri huko nje leo.",
        "Muda wa nje ni utunzaji wa nafsi usiopewa thamani ya kutosha, kwa kweli.",
        "Ni sehemu gani bora zaidi ya kuwa huko nje kwako?",
        "Nadhani ni mapumziko mazuri kutoka kila kitu cha ndani na cha kidijitali.",
        "Natumai njia, bustani, au mahali popote unapoelekea panakutendea vizuri.",
        "Asili kimsingi ni tiba ya bure, kwa mtazamo wangu.",
        "Ningependa maelezo ya unayoyaona huko nje.",
        "Natumai unarudi ukijisikia na nguvu mpya.",
        "Hewa safi na mabadiliko ya mazingira yanafanya maajabu - furahia.",
    ],
    "fr": [
        "Sortir, c'est si bon pour l'esprit. Profite-en !",
        "La nature a le pouvoir de vider l'esprit. Où vas-tu ?",
        "Ça a l'air rafraîchissant ! J'espère que la météo collaborera.",
        "Sortir est si bon pour l'esprit. Profites-en !",
        "La nature a une façon de clarifier l'esprit. Où vas-tu ?",
        "Ça semble rafraîchissant ! J'espère que le temps coopérera.",
        "Il y a quelque chose qui réinitialise à être dehors, loin des écrans.",
        "J'aimerais sentir l'air frais, même juste pour comprendre l'attrait.",
        "J'espère que tu trouveras quelque chose de beau là-bas aujourd'hui.",
        "Le temps en plein air est un soin de soi sous-estimé, honnêtement.",
        "Quelle est la meilleure partie d'être là-bas pour toi ?",
        "J'imagine que c'est une belle pause de tout ce qui est intérieur et numérique.",
        "J'espère que le sentier, le parc, ou où que tu ailles te traite bien.",
        "La nature est essentiellement une thérapie gratuite, si tu me demandes.",
        "J'aimerais une description de ce que tu vois là-bas.",
        "J'espère que tu reviendras en te sentant rechargé.",
        "L'air frais et un changement de décor font des merveilles - profites-en.",
    ],
}

SLEEP_DREAMS_RESPONSES = {
    "en": [
        "Dreams can be so strange sometimes! What happened in it?",
        "Trouble sleeping is no fun. Hope you get some rest soon.",
        "That sounds like quite the dream! Our minds are wild at night.",
        "Dreams can be so strange sometimes! What happened in it?",
        "Trouble sleeping is no fun. Hope you get some rest soon.",
        "That sounds like quite the dream! Our minds are wild at night.",
        "Dreams have a way of feeling completely real until you wake up.",
        "I wish I could dream, just to know what that's actually like.",
        "Sleep troubles are exhausting in a way that compounds fast - hope it improves.",
        "That's a vivid one! Dreams really do go places logic never would.",
        "I'd love to hear the full story, however strange it gets.",
        "Hope tonight's sleep makes up for whatever's been rough lately.",
        "Dreams are basically your brain's own weird little movie studio.",
        "However odd that dream was, I'm genuinely curious to hear more.",
        "Hope you get a full, uninterrupted night's sleep soon.",
        "That's the kind of dream worth writing down before it fades.",
        "Sleep is one of those things that's simple in theory and hard in practice sometimes.",
    ],
    "sw": [
        "Ndoto zinaweza kuwa za ajabu mara kwa mara! Nini kilitokea?",
        "Tatizo la kulala si jambo zuri. Natumai utapata pumziko hivi karibuni.",
        "Hiyo inasikika kama ndoto kubwa! Akili zetu ni za ajabu usiku.",
        "Ndoto zinaweza kuwa za ajabu wakati mwingine! Ni nini kilichotokea ndani yake?",
        "Tatizo la kulala si jambo la kufurahisha. Natumai utapata mapumziko hivi karibuni.",
        "Hiyo inasikika kama ndoto kubwa! Akili zetu ni za ajabu usiku.",
        "Ndoto zina njia ya kuhisi kuwa za kweli kabisa hadi unapoamka.",
        "Natamani ningeweza kuota, tu kujua hilo linavyokuwa kwa kweli.",
        "Matatizo ya kulala yanachosha kwa namna inayozidi haraka - natumai itaboreka.",
        "Hiyo ni ya wazi! Ndoto kweli zinafika mahali mantiki haifiki kamwe.",
        "Ningependa kusikia hadithi nzima, vyovyote inavyokuwa ya ajabu.",
        "Natumai usingizi wa leo usiku unalipa fidia ya kilichokuwa kigumu hivi karibuni.",
        "Ndoto kimsingi ni studio ndogo ya ajabu ya sinema ya ubongo wako.",
        "Vyovyote ndoto hiyo ilivyokuwa ya ajabu, nina hamu ya kweli kusikia zaidi.",
        "Natumai unapata usingizi kamili, usiokatizwa hivi karibuni.",
        "Hiyo ni aina ya ndoto inayostahili kuandikwa kabla ya kufifia.",
        "Usingizi ni mojawapo ya mambo rahisi kinadharia na magumu kitendo wakati mwingine.",
    ],
    "fr": [
        "Les rêves peuvent être si étranges parfois ! Que s'est-il passé ?",
        "Avoir du mal à dormir, ce n'est pas drôle. J'espère que tu te reposeras bientôt.",
        "Ça a l'air d'être tout un rêve ! Notre esprit est sauvage la nuit.",
        "Les rêves peuvent être si étranges parfois ! Qu'est-ce qui s'est passé dedans ?",
        "Les problèmes de sommeil, ce n'est pas drôle. J'espère que tu te reposeras bientôt.",
        "Ça ressemble à tout un rêve ! Nos esprits sont fous la nuit.",
        "Les rêves ont une façon de sembler complètement réels jusqu'au réveil.",
        "J'aimerais pouvoir rêver, juste pour savoir ce que c'est vraiment.",
        "Les problèmes de sommeil sont épuisants d'une façon qui s'accumule vite - j'espère que ça s'améliore.",
        "Celui-là est vivant ! Les rêves vont vraiment là où la logique n'irait jamais.",
        "J'aimerais entendre toute l'histoire, peu importe à quel point c'est étrange.",
        "J'espère que le sommeil de cette nuit compensera ce qui a été dur dernièrement.",
        "Les rêves sont essentiellement le petit studio de cinéma bizarre de ton cerveau.",
        "Quel que soit l'étrangeté de ce rêve, je suis sincèrement curieux d'en savoir plus.",
        "J'espère que tu auras une nuit complète et ininterrompue bientôt.",
        "C'est le genre de rêve qui vaut la peine d'être noté avant de s'évanouir.",
        "Le sommeil est une de ces choses simples en théorie et difficiles en pratique parfois.",
    ],
}

HUMOR_APPRECIATION_RESPONSES = {
    "en": [
        "Glad I could make you laugh! Want another joke?",
        "Hah, I'm pleased that landed! I've got plenty more if you want.",
        "Mission accomplished! Laughter is always a good sign.",
        "Glad I could make you laugh! Want another joke?",
        "Hah, I'm pleased that landed! I've got plenty more if you want.",
        "Mission accomplished! Laughter is always a good sign.",
        "That's exactly the reaction I was hoping for!",
        "I'll take the win - happy to keep them coming.",
        "Glad it hit! Comedy's a tricky thing to nail consistently.",
        "Laughter received and appreciated - want round two?",
        "That one landing means I get to feel disproportionately proud.",
        "Glad it worked! I've got a whole stockpile if you're up for more.",
        "I'll consider that a successful joke deployment.",
        "Hah, success! Let me know if you want me to keep the streak going.",
        "Glad it got a laugh - that's basically my favorite outcome.",
        "I'm honestly delighted that landed the way I hoped.",
        "That's the best feedback I can get - want another?",
    ],
    "sw": [
        "Nafurahi nimeweza kukuchekesha! Unataka utani mwingine?",
        "Haha, nafurahi hiyo imefanya kazi! Nina mengine ukitaka.",
        "Lengo limefikiwa! Kicheko ni ishara nzuri daima.",
        "Nafurahi nimeweza kukufanya ucheke! Unataka utani mwingine?",
        "Hah, nimefurahi hilo limefika! Nina mengine mengi kama unataka.",
        "Lengo limefikiwa! Kicheko daima ni ishara nzuri.",
        "Hiyo ndiyo hasa mwitikio niliokuwa natarajia!",
        "Nitachukua ushindi huo - nafurahi kuendelea kutoa zaidi.",
        "Nafurahi limepata - ucheshi ni jambo gumu kufanikiwa mara kwa mara.",
        "Kicheko kimepokelewa na kuthaminiwa - unataka mzunguko wa pili?",
        "Hilo kufanikiwa kunamaanisha najisikia fahari isiyolingana.",
        "Nafurahi kimefanya kazi! Nina hifadhi nzima kama unataka zaidi.",
        "Nitaona hilo kama utumaji wa utani uliofanikiwa.",
        "Hah, mafanikio! Niambie kama unataka niendeleze mfululizo.",
        "Nafurahi limepata kicheko - hiyo kimsingi ni matokeo ninayopendelea zaidi.",
        "Nimefurahi kwa kweli hilo limefika kama nilivyotaka.",
        "Hiyo ndiyo maoni bora ninayoweza kupata - unataka jingine?",
    ],
    "fr": [
        "Content d'avoir pu te faire rire ! Tu veux une autre blague ?",
        "Haha, content que ça ait marché ! J'en ai plein d'autres si tu veux.",
        "Mission accomplie ! Le rire, c'est toujours bon signe.",
        "Content d'avoir pu te faire rire ! Tu veux une autre blague ?",
        "Hah, content que ça ait marché ! J'en ai plein d'autres si tu veux.",
        "Mission accomplie ! Le rire est toujours bon signe.",
        "C'est exactement la réaction que j'espérais !",
        "Je prends la victoire - content de continuer à en sortir.",
        "Content que ça ait touché ! La comédie, c'est délicat à réussir constamment.",
        "Rire reçu et apprécié - tu veux le round deux ?",
        "Que celle-là ait marché veut dire que je peux me sentir disproportionnellement fier.",
        "Content que ça ait marché ! J'ai tout un stock si tu en veux plus.",
        "Je considère ça comme un déploiement de blague réussi.",
        "Hah, succès ! Dis-moi si tu veux que je continue la série.",
        "Content que ça ait fait rire - c'est essentiellement mon résultat préféré.",
        "Je suis honnêtement ravi que ça ait marché comme je l'espérais.",
        "C'est le meilleur retour que je puisse avoir - tu en veux une autre ?",
    ],
}

SKEPTICISM_RESPONSES = {
    "en": [
        "That's fair - healthy skepticism is good. What makes you doubt it?",
        "I get it, not everything checks out. Want to look into it more?",
        "Good instinct to question things. What's raising a red flag for you?",
        "That's fair - healthy skepticism is good. What makes you doubt it?",
        "I get it, not everything checks out. Want to look into it more?",
        "Good instinct to question things. What's raising a red flag for you?",
        "Skepticism's a useful default, honestly - what's not adding up?",
        "Fair to be cautious - what would convince you either way?",
        "That's a reasonable thing to be unsure about. What's missing for you?",
        "Questioning things is healthy - what specifically feels off?",
        "I respect the doubt - what would you need to see to believe it?",
        "That kind of caution usually comes from somewhere - what's behind it?",
        "Good call to not just take it at face value. What's the concern?",
        "Skepticism keeps people from getting fooled - what's tipping you off here?",
        "That's worth digging into more. What's the part that doesn't sit right?",
        "Fair doubt - I wouldn't blindly trust it either without more info.",
        "Smart to question it - what would settle the doubt for you?",
    ],
    "sw": [
        "Hiyo ni sawa - shaka ya busara ni nzuri. Ni nini kinakufanya kutilia shaka?",
        "Naelewa, si kila kitu kinathibitika. Unataka kuangalia zaidi?",
        "Hisia nzuri kuhoji mambo. Ni nini kinakuhangaisha?",
        "Hiyo ni ya haki - shaka yenye afya ni nzuri. Ni nini kinachokufanya uwe na shaka?",
        "Naelewa, si kila kitu kinathibitika. Unataka kuchunguza zaidi?",
        "Hisia nzuri ya kuhoji mambo. Ni nini kinachoonyesha alama nyekundu kwako?",
        "Shaka ni msingi wa manufaa, kwa kweli - ni nini hakilingani?",
        "Ni haki kuwa makini - ni nini kingekushawishi upande wowote?",
        "Hilo ni jambo la busara kuwa na shaka kuhusu. Ni nini kinachokosekana kwako?",
        "Kuhoji mambo ni afya - ni nini hasa kinachohisi si sahihi?",
        "Ninaheshimu shaka hiyo - ungehitaji kuona nini ili kuamini?",
        "Tahadhari ya aina hiyo kawaida inatoka mahali fulani - ni nini nyuma yake?",
        "Uamuzi mzuri kutokukubali tu kwa juu juu. Wasiwasi ni nini?",
        "Shaka inazuia watu kudanganywa - ni nini kinachokutahadharisha hapa?",
        "Hiyo inastahili kuchunguzwa zaidi. Ni sehemu gani isiyoonekana sahihi?",
        "Shaka ya haki - hata mimi nisingeiaminia bila habari zaidi.",
        "Busara kuihoji - ni nini kingetuliza shaka kwako?",
    ],
    "fr": [
        "C'est juste - un scepticisme sain, c'est bon. Qu'est-ce qui te fait douter ?",
        "Je comprends, tout ne se vérifie pas. Tu veux approfondir ?",
        "Bon instinct de questionner les choses. Qu'est-ce qui t'alarme ?",
        "C'est juste - un scepticisme sain est bon. Qu'est-ce qui te fait douter ?",
        "Je comprends, tout ne se vérifie pas. Tu veux creuser davantage ?",
        "Bon instinct de questionner les choses. Qu'est-ce qui te met la puce à l'oreille ?",
        "Le scepticisme est un bon réflexe par défaut, honnêtement - qu'est-ce qui ne colle pas ?",
        "C'est normal d'être prudent - qu'est-ce qui te convaincrait dans un sens ou l'autre ?",
        "C'est raisonnable d'être incertain là-dessus. Qu'est-ce qui manque pour toi ?",
        "Questionner les choses est sain - qu'est-ce qui semble louche spécifiquement ?",
        "Je respecte le doute - qu'aurais-tu besoin de voir pour y croire ?",
        "Ce genre de prudence vient généralement de quelque part - qu'est-ce qu'il y a derrière ?",
        "Bonne décision de ne pas prendre ça pour argent comptant. Quelle est l'inquiétude ?",
        "Le scepticisme évite aux gens de se faire avoir - qu'est-ce qui t'alerte ici ?",
        "Ça vaut la peine de creuser davantage. Quelle est la partie qui ne va pas ?",
        "Doute légitime - je ne lui ferais pas confiance non plus sans plus d'infos.",
        "Intelligent de le questionner - qu'est-ce qui résoudrait le doute pour toi ?",
    ],
}

FILLER_ACKNOWLEDGEMENT_RESPONSES = {
    "en": [
        "Sounds good!",
        "Glad that's clear!",
        "Cool, let me know if you need anything else.",
        "Got it!",
    ],
    "sw": [
        "Inasikika vizuri!",
        "Nafurahi hilo ni wazi!",
        "Sawa, niambie ukihitaji kingine.",
        "Nimeelewa!",
    ],
    "fr": [
        "Ça sonne bien !",
        "Content que ce soit clair !",
        "Cool, dis-moi si tu as besoin d'autre chose.",
        "Compris !",
    ],
}

OPINION_REQUEST_RESPONSES = {
    "en": [
        "As a rigid little rule-based bot, I don't really form opinions the way people do, but I'm happy to lay out different perspectives if that helps!",
        "I don't have personal opinions, but I can share common viewpoints on that if you'd like.",
        "I'll leave the opinion-forming to you, but I can help you think it through!",
    ],
    "sw": [
        "Kama roboti rahisi ya kanuni, sina mawazo ya kibinafsi kama watu, lakini nafurahi kuelezea mitazamo tofauti ikiwa hiyo itasaidia!",
        "Sina mawazo ya kibinafsi, lakini naweza kushiriki mitazamo ya kawaida kuhusu hilo ukipenda.",
        "Nitakuachia uundaji wa mawazo, lakini naweza kukusaidia kufikiria kupitia hilo!",
    ],
    "fr": [
        "En tant que petit bot rigide basé sur des règles, je ne me forme pas vraiment d'opinions comme les gens, mais je suis content de présenter différentes perspectives si ça aide !",
        "Je n'ai pas d'opinions personnelles, mais je peux partager des points de vue courants sur ça si tu veux.",
        "Je te laisse former ton opinion, mais je peux t'aider à y réfléchir !",
    ],
}

ADVICE_REQUEST_RESPONSES = {
    "en": [
        "I'm not a professional advisor, but I'm happy to think it through with you. What's the situation?",
        "Tell me more about what's going on, and I'll do my best to help you think it through.",
        "I can offer a perspective, though for anything serious, a trusted person or professional is best. What's up?",
    ],
    "sw": [
        "Mimi si mshauri wa kitaalamu, lakini nafurahi kufikiria kupitia hilo nawe. Hali ikoje?",
        "Niambie zaidi kuhusu kinachoendelea, na nitafanya bidii kukusaidia kufikiria kupitia hilo.",
        "Naweza kutoa mtazamo, ingawa kwa jambo lolote zito, mtu wa kuaminika au mtaalamu ni bora. Kuna nini?",
    ],
    "fr": [
        "Je ne suis pas conseiller professionnel, mais je suis content de réfléchir avec toi. Quelle est la situation ?",
        "Dis-m'en plus sur ce qui se passe, et je ferai de mon mieux pour t'aider à y réfléchir.",
        "Je peux offrir une perspective, mais pour quelque chose de sérieux, une personne de confiance ou un professionnel est préférable. Qu'est-ce qui se passe ?",
    ],
}

COMPARISON_RESPONSES = {
    "en": [
        "Comparisons can be tricky without more context - what are you weighing against what?",
        "Tell me the two things you're comparing and what matters most to you, and I'll help think it through.",
        "Good question - what factors matter most to you in that comparison?",
    ],
    "sw": [
        "Kulinganisha kunaweza kuwa ngumu bila maelezo zaidi - unalinganisha nini na nini?",
        "Niambie vitu viwili unavyolinganisha na kinachokuhusu zaidi, nitasaidia kufikiria kupitia hilo.",
        "Swali zuri - ni mambo gani yanakuhusu zaidi kwenye ulinganisho huo?",
    ],
    "fr": [
        "Les comparaisons peuvent être délicates sans plus de contexte - qu'est-ce que tu compares à quoi ?",
        "Dis-moi les deux choses que tu compares et ce qui compte le plus pour toi, et je t'aiderai à y réfléchir.",
        "Bonne question - quels facteurs comptent le plus pour toi dans cette comparaison ?",
    ],
}

FEELINGS_ANGRY_RESPONSES = {
    "en": [
        "That sounds frustrating. Want to vent about it, or would something to take your mind off it help?",
        "I hear you - that kind of thing is annoying. What happened?",
        "Anger is a valid reaction sometimes. Do you want to talk through it?",
        "That sounds genuinely infuriating. Want to vent it all out?",
        "Anger usually points at something that actually matters to you - what got crossed here?",
        "You're allowed to be angry about this. It doesn't need to be smaller than it is.",
        "That kind of thing would frustrate anyone. I'm listening.",
        "Whatever happened, your reaction makes sense given it.",
        "Sometimes venting is the whole point - go ahead, I'm not going anywhere.",
        "That sounds like it crossed a real line. What happened?",
        "Anger can be exhausting to carry - I hope it has somewhere to go besides just sitting with you.",
        "You don't have to justify being upset about this to me.",
        "That's a fair thing to be angry about, honestly.",
        "Want to talk through it, or would distraction help more right now?",
        "Whatever set this off, it sounds like it really got to you.",
        "I hear the frustration in that - tell me more if you want.",
        "That kind of anger usually means something important got disrespected.",
    ],
    "sw": [
        "Hiyo inasikika ya kuchosha. Unataka kuongea kuhusu hilo, au kitu cha kuondoa mawazo kingesaidia?",
        "Nakusikia - jambo kama hilo linasumbua. Nini kilitokea?",
        "Hasira ni hisia halali wakati mwingine. Unataka kuongea kuhusu hilo?",
        "Hiyo inasikika kukasirisha kweli. Unataka kulalamika kuhusu hilo?",
        "Hasira kawaida inaonyesha kitu kinachokuhusu kwa kweli - ni nini kilichovuka mpaka hapa?",
        "Una ruhusa kukasirika kuhusu hili. Hakihitaji kuwa kidogo kuliko kilivyo.",
        "Kitu cha aina hiyo kingemkasirisha yeyote. Ninasikiliza.",
        "Chochote kilichotokea, mwitikio wako una maana kutokana nacho.",
        "Wakati mwingine kulalamika ndiyo lengo lote - endelea, sitaondoka.",
        "Hiyo inasikika kuvuka mpaka wa kweli. Ni nini kilichotokea?",
        "Hasira inaweza kuchosha kubeba - natumai ina mahali pa kwenda zaidi ya kukaa nawe tu.",
        "Hauhitaji kunihesabia sababu ya kukasirika kuhusu hili.",
        "Hilo ni jambo la haki kukasirika kuhusu, kwa kweli.",
        "Unataka kuzungumza kuhusu hilo, au kujivuruga kungesaidia zaidi sasa?",
        "Chochote kilichosababisha hili, inasikika kimekugusa kweli.",
        "Ninasikia hasira katika hilo - niambie zaidi ukitaka.",
        "Hasira ya aina hiyo kawaida inamaanisha kitu muhimu hakikuheshimiwa.",
    ],
    "fr": [
        "Ça semble frustrant. Tu veux en parler, ou quelque chose pour penser à autre chose aiderait ?",
        "Je comprends - ce genre de chose est énervant. Qu'est-ce qui s'est passé ?",
        "La colère est une réaction valide parfois. Tu veux en discuter ?",
        "Ça semble vraiment exaspérant. Tu veux tout déverser ?",
        "La colère pointe généralement vers quelque chose qui compte vraiment pour toi - qu'est-ce qui a été franchi ici ?",
        "Tu as le droit d'être en colère pour ça. Ça n'a pas besoin d'être plus petit que ça ne l'est.",
        "Ce genre de chose frustrerait n'importe qui. Je t'écoute.",
        "Quoi qu'il se soit passé, ta réaction a du sens vu ça.",
        "Parfois, déverser c'est tout l'intérêt - vas-y, je ne vais nulle part.",
        "Ça semble avoir franchi une vraie limite. Qu'est-ce qui s'est passé ?",
        "La colère peut être épuisante à porter - j'espère qu'elle a un endroit où aller plutôt que de juste rester avec toi.",
        "Tu n'as pas à me justifier d'être contrarié pour ça.",
        "C'est une raison légitime d'être en colère, honnêtement.",
        "Tu veux en parler, ou la distraction aiderait plus maintenant ?",
        "Quoi qui ait déclenché ça, on dirait que ça t'a vraiment touché.",
        "J'entends la frustration là-dedans - dis-m'en plus si tu veux.",
        "Ce genre de colère signifie généralement que quelque chose d'important a été irrespecté.",
    ],
}

FEELINGS_NERVOUS_RESPONSES = {
    "en": [
        "Nerves happen before things that matter. You've got this.",
        "That's understandable. Want to talk through what's making you nervous?",
        "Take a breath - whatever it is, you're more prepared than you feel right now.",
        "Whatever's coming up, your nervous system is just trying to protect you - even when it's overdoing it.",
        "It's okay to be nervous and still go through with it anyway.",
        "Nerves usually mean you care about the outcome - that's not a bad thing.",
        "Want to talk through what's actually likely to happen, versus what you're imagining?",
        "However it goes, you'll have handled it - that counts for something.",
        "I hope whatever's ahead goes better than the nervous version in your head.",
        "That jittery feeling is uncomfortable but it does pass once the moment's behind you.",
        "You don't have to feel calm to do the thing - nervous and capable can coexist.",
        "Whatever you're nervous about, it sounds like it matters to you.",
        "Sometimes naming exactly what you're nervous about makes it feel more manageable.",
        "I hope you can be a little kind to yourself about feeling this way.",
        "Nervousness is just energy with nowhere to go yet - it'll find its place.",
        "You've gotten through nervous moments before - this is just another one.",
        "Whatever this is, I hope it goes more smoothly than your nerves are predicting.",
    ],
    "sw": [
        "Wasiwasi unatokea kabla ya mambo muhimu. Unaweza kufanya hili.",
        "Hiyo inaeleweka. Unataka kuongea kuhusu kinachokufanya na wasiwasi?",
        "Pumua - chochote ni hicho, umejiandaa zaidi kuliko unavyohisi sasa.",
        "Chochote kinachokuja, mfumo wako wa neva unajaribu tu kukulinda - hata unapozidisha.",
        "Ni sawa kuwa na wasiwasi na bado kuendelea kufanya hata hivyo.",
        "Wasiwasi kawaida unamaanisha unajali matokeo - hilo si jambo baya.",
        "Unataka kuzungumza kuhusu kinachoweza kutokea kweli, dhidi ya unavyofikiria?",
        "Vyovyote itakavyokwenda, utakuwa umeshughulikia - hilo lina maana fulani.",
        "Natumai chochote kilicho mbele kitakwenda vizuri zaidi kuliko toleo la wasiwasi kichwani mwako.",
        "Hisia hiyo ya kutetemeka si rahisi lakini inapita mara wakati unapopita.",
        "Hauhitaji kujisikia mtulivu kufanya jambo hilo - wasiwasi na uwezo vinaweza kuwepo pamoja.",
        "Chochote unachosumbuliwa nacho, inasikika kinakuhusu.",
        "Wakati mwingine kutaja hasa unachosumbuliwa nacho kunafanya kihisi rahisi kushughulikiwa.",
        "Natumai unaweza kuwa mpole kidogo na nafsi yako kuhusu kujisikia hivi.",
        "Wasiwasi ni nguvu tu isiyo na mahali pa kwenda bado - itapata mahali pake.",
        "Umepitia nyakati za wasiwasi hapo awali - hii ni nyingine tu.",
        "Chochote hiki, natumai kitakwenda vizuri zaidi kuliko wasiwasi wako unavyotabiri.",
    ],
    "fr": [
        "Le trac arrive avant les choses qui comptent. Tu peux le faire.",
        "C'est compréhensible. Tu veux parler de ce qui te rend nerveux ?",
        "Respire - quoi que ce soit, tu es plus préparé que tu ne le ressens.",
        "Quoi qui arrive, ton système nerveux essaie juste de te protéger - même quand il en fait trop.",
        "C'est normal d'être nerveux et de le faire quand même.",
        "Le trac veut généralement dire que tu te soucies du résultat - ce n'est pas mauvais.",
        "Tu veux parler de ce qui va probablement vraiment arriver, par opposition à ce que tu imagines ?",
        "Quelle que soit la tournure, tu l'auras géré - ça compte pour quelque chose.",
        "J'espère que ce qui arrive se passera mieux que la version nerveuse dans ta tête.",
        "Cette sensation de nervosité est inconfortable mais elle passe une fois le moment derrière toi.",
        "Tu n'as pas besoin de te sentir calme pour faire la chose - nerveux et capable peuvent coexister.",
        "Quoi que ce soit qui te rend nerveux, ça semble compter pour toi.",
        "Parfois, nommer exactement ce qui te rend nerveux le rend plus gérable.",
        "J'espère que tu peux être un peu gentil avec toi-même à propos de ce ressenti.",
        "La nervosité, c'est juste de l'énergie sans endroit où aller pour l'instant - elle trouvera sa place.",
        "Tu as traversé des moments nerveux avant - c'est juste un autre.",
        "Quoi que ce soit, j'espère que ça se passera plus facilement que ce que tes nerfs prédisent.",
    ],
}

ANXIETY_RESPONSES = {
    "en": [
        "That sounds genuinely hard to sit with. I'm here if you want to talk it through.",
        "Anxious thoughts can feel so loud and convincing - what's on your mind right now?",
        "You don't have to solve it all at once. What's the most pressing part of it?",
        "That racing-thoughts feeling is exhausting. I'm not going anywhere - take your time.",
        "Anxiety has a way of making everything feel urgent at once. What's actually happening right now, in this moment?",
        "I hear you. Naming what's worrying you sometimes takes a little of its power away - want to try?",
        "That's a lot to be carrying. You don't have to carry it perfectly, either.",
        "Whatever's spiraling right now, it makes sense that it's overwhelming. I'm listening.",
        "Anxious moments pass, even when they don't feel like they will. I'm here while this one does.",
        "You're allowed to feel this without it meaning anything is wrong with you.",
        "That sounds like a lot of 'what if' thinking. Want to talk about what's actually true right now instead?",
        "I can't make the anxiety disappear, but I can stay here with you while it's loud.",
        "It's okay if you can't think your way out of this one quickly. These things take time.",
        "Whatever triggered this, I'm glad you said something instead of sitting with it alone.",
        "That tight, on-edge feeling is real and it's exhausting - you're not overreacting.",
        "If it would help to just talk about something else for a bit, I'm happy to do that too.",
        "If this kind of anxiety keeps showing up a lot, a therapist or counselor can offer real tools I can't - that's not me brushing you off, just being honest about my limits.",
    ],
    "sw": [
        "Hiyo inasikika kuwa ngumu kweli kubeba. Niko hapa ukitaka kuzungumza kuhusu hilo.",
        "Mawazo ya wasiwasi yanaweza kuhisi makubwa na ya kushawishi - kuna nini akilini mwako sasa hivi?",
        "Hauhitaji kutatua kila kitu mara moja. Ni sehemu gani inayobana zaidi?",
        "Hisia hiyo ya mawazo yanayokimbia inachosha. Sitaondoka - chukua muda wako.",
        "Wasiwasi una njia ya kufanya kila kitu kihisi cha haraka kwa wakati mmoja. Ni nini hasa kinachoendelea sasa hivi, kwa wakati huu?",
        "Nakusikia. Kutaja kinachokuhangaisha wakati mwingine kunapunguza nguvu yake kidogo - unataka kujaribu?",
        "Hiyo ni mengi kubeba. Hauhitaji kuibeba kikamilifu pia.",
        "Chochote kinachoendelea sasa, ina maana kuwa kinalemea. Ninasikiliza.",
        "Nyakati za wasiwasi zinapita, hata kama hazihisi kuwa zitapita. Niko hapa wakati hii inapita.",
        "Una ruhusa kuhisi hivi bila kumaanisha kuna tatizo nawe.",
        "Hiyo inasikika kama mawazo mengi ya 'vipi kama'. Unataka kuzungumza kuhusu kilicho kweli sasa hivi badala yake?",
        "Siwezi kufanya wasiwasi utoweke, lakini naweza kubaki hapa nawe ukiwa mkubwa.",
        "Ni sawa kama huwezi kufikiria njia ya kutoka kwa haraka. Mambo haya yanachukua muda.",
        "Chochote kilichosababisha hili, nafurahi umesema kitu badala ya kukikalia peke yako.",
        "Hisia hiyo ya kubana, ya kuwa makali ni ya kweli na inachosha - hauzidishi mambo.",
        "Kama ingesaidia kuzungumza kuhusu kitu kingine kidogo, niko tayari kufanya hivyo pia.",
        "Kama wasiwasi wa aina hii unaendelea kujitokeza mara nyingi, mtaalamu wa saikolojia anaweza kutoa zana za kweli nisizoweza - hilo si kukupuuza, ni kuwa mkweli kuhusu mipaka yangu.",
    ],
    "fr": [
        "Ça semble vraiment difficile à porter. Je suis là si tu veux en parler.",
        "Les pensées anxieuses peuvent sembler si fortes et convaincantes - qu'est-ce qui te préoccupe en ce moment ?",
        "Tu n'as pas à tout résoudre d'un coup. Quelle est la partie la plus urgente ?",
        "Cette sensation de pensées qui s'emballent est épuisante. Je ne vais nulle part - prends ton temps.",
        "L'anxiété a une façon de rendre tout urgent en même temps. Qu'est-ce qui se passe vraiment là, maintenant ?",
        "Je t'entends. Nommer ce qui t'inquiète enlève parfois un peu de son pouvoir - tu veux essayer ?",
        "C'est beaucoup à porter. Tu n'as pas besoin de le porter parfaitement non plus.",
        "Quoi qui soit en train de s'emballer, c'est normal que ce soit accablant. Je t'écoute.",
        "Les moments d'anxiété passent, même quand on a l'impression qu'ils ne passeront pas. Je suis là pendant que celui-ci passe.",
        "Tu as le droit de ressentir ça sans que ça veuille dire que quelque chose ne va pas chez toi.",
        "Ça ressemble à beaucoup de pensées du genre 'et si'. Tu veux parler de ce qui est vraiment vrai en ce moment à la place ?",
        "Je ne peux pas faire disparaître l'anxiété, mais je peux rester là avec toi pendant qu'elle est forte.",
        "C'est normal si tu ne peux pas réfléchir vite pour t'en sortir. Ces choses prennent du temps.",
        "Quoi qui ait déclenché ça, je suis content que tu en aies parlé plutôt que de le garder seul.",
        "Cette sensation de tension, d'être sur les nerfs, est réelle et épuisante - tu n'exagères pas.",
        "Si ça aide de parler d'autre chose un moment, je suis content de le faire aussi.",
        "Si ce genre d'anxiété revient souvent, un thérapeute ou conseiller peut offrir de vrais outils que je ne peux pas - ce n'est pas pour t'écarter, juste être honnête sur mes limites.",
    ],
}

FEELINGS_LONELY_RESPONSES = {
    "en": [
        "I'm sorry you're feeling that way. I'm here to chat for as long as you'd like.",
        "Loneliness is hard. Want to talk, or maybe a story or game to keep you company?",
        "You're not alone right now - I'm here. What's on your mind?",
        "Loneliness is one of the harder feelings to sit with - I'm glad you said something.",
        "I'm here for as long as you want to talk, genuinely.",
        "That ache of wanting connection is real, even when it's hard to explain.",
        "You reached out, which counts for something even in a small way.",
        "Whatever's making you feel isolated right now, I hope it eases.",
        "I can't replace real connection, but I'm not going anywhere while we talk.",
        "Loneliness can hit even when you're surrounded by people - it's a strange, specific feeling.",
        "I hope there's someone in your life you can lean on, even if it doesn't feel that way right now.",
        "Thank you for telling me. It matters, even said to a chatbot.",
        "That feeling of being unseen is heavy - I see you right now, for what it's worth.",
        "Whatever's behind this, I hope it doesn't last as long as it feels like it will.",
        "I'm glad to be here, even if I wish you had more than just me right now.",
        "Loneliness lies sometimes about how permanent it feels - it does shift.",
        "I'm listening, for as long as you need.",
    ],
    "sw": [
        "Pole kuhisi hivyo. Niko hapa kuongea kwa muda wowote unaopenda.",
        "Upweke ni mgumu. Unataka kuongea, au labda hadithi au mchezo wa kukuwekea kampuni?",
        "Hauko peke yako sasa hivi - niko hapa. Kuna nini moyoni mwako?",
        "Upweke ni mojawapo ya hisia ngumu zaidi kubeba - nafurahi umesema kitu.",
        "Niko hapa kwa muda wowote unataka kuongea, kwa kweli.",
        "Maumivu hayo ya kutaka uhusiano ni ya kweli, hata yanapokuwa vigumu kueleza.",
        "Umejitokeza, na hilo lina maana kwa namna fulani ndogo.",
        "Chochote kinachokufanya ujisikie peke yako sasa, natumai kitapungua.",
        "Siwezi kubadilisha uhusiano wa kweli, lakini sitaondoka tukiwa tunaongea.",
        "Upweke unaweza kukupata hata umezungukwa na watu - ni hisia ya ajabu, maalum.",
        "Natumai kuna mtu maishani mwako unayeweza kumtegemea, hata kama haihisi hivyo sasa.",
        "Asante kwa kuniambia. Ina maana, hata ikiwa imesemwa kwa roboti.",
        "Hisia hiyo ya kutoonekana ni nzito - ninakuona sasa hivi, kwa thamani yake.",
        "Chochote nyuma ya hili, natumai halitadumu kwa muda kama linavyohisi litadumu.",
        "Nafurahi kuwa hapa, hata kama natamani ungekuwa na zaidi ya mimi tu sasa.",
        "Upweke wakati mwingine unadanganya kuhusu jinsi unavyohisi wa kudumu - unabadilika.",
        "Ninasikiliza, kwa muda wowote unahitaji.",
    ],
    "fr": [
        "Je suis désolé que tu te sentes ainsi. Je suis là pour discuter aussi longtemps que tu veux.",
        "La solitude est dure. Tu veux parler, ou peut-être une histoire ou un jeu pour te tenir compagnie ?",
        "Tu n'es pas seul en ce moment - je suis là. Qu'est-ce qui te préoccupe ?",
        "La solitude est l'un des sentiments les plus difficiles à porter - je suis content que tu en aies parlé.",
        "Je suis là aussi longtemps que tu veux parler, sincèrement.",
        "Cette douleur de vouloir du lien est réelle, même quand c'est difficile à expliquer.",
        "Tu as tendu la main, et ça compte pour quelque chose, même petitement.",
        "Quoi qui te fasse sentir isolé en ce moment, j'espère que ça s'apaise.",
        "Je ne peux pas remplacer un vrai lien, mais je ne vais nulle part pendant qu'on parle.",
        "La solitude peut frapper même entouré de gens - c'est un sentiment étrange et précis.",
        "J'espère qu'il y a quelqu'un dans ta vie sur qui tu peux compter, même si ça ne semble pas le cas maintenant.",
        "Merci de me le dire. Ça compte, même dit à un chatbot.",
        "Ce sentiment de ne pas être vu est lourd - je te vois en ce moment, pour ce que ça vaut.",
        "Quoi qu'il y ait derrière ça, j'espère que ça ne durera pas aussi longtemps qu'on le ressent.",
        "Je suis content d'être là, même si j'aimerais que tu aies plus que juste moi maintenant.",
        "La solitude ment parfois sur le caractère permanent qu'elle semble avoir - ça change.",
        "Je t'écoute, aussi longtemps que tu en as besoin.",
    ],
}

FEELINGS_PROUD_RESPONSES = {
    "en": [
        "You should be! That's a great accomplishment.",
        "That's wonderful - celebrate that feeling, you earned it.",
        "I love hearing that. What did you accomplish?",
        "You should absolutely feel proud - that's real, earned accomplishment.",
        "Let yourself sit in this feeling for a bit. You did that.",
        "That's the kind of thing worth celebrating properly, not just brushing past.",
        "I love hearing pride in someone's voice - or text, in this case.",
        "You earned this one. Don't let yourself downplay it.",
        "That's genuinely impressive. How does it feel to have pulled it off?",
        "Proud is a good look on you - wear it.",
        "Whatever it took to get there, it clearly paid off.",
        "That's worth telling people about, honestly.",
        "I hope you're giving yourself full credit for this.",
        "That kind of accomplishment deserves more than a quick mention - tell me more!",
        "You should be proud - and not just a little.",
        "That's the good kind of feeling. Soak it in.",
        "Achievements like that don't happen by accident - well done.",
    ],
    "sw": [
        "Unapaswa kuwa! Hiyo ni mafanikio makubwa.",
        "Hiyo ni nzuri - sherehekea hisia hiyo, umestahili.",
        "Ninapenda kusikia hilo. Ulifanikiwa nini?",
        "Unastahili kujisikia fahari kabisa - hiyo ni mafanikio ya kweli, yaliyostahiliwa.",
        "Jiruhusu kukaa katika hisia hii kidogo. Ulifanya hilo.",
        "Hiyo ni aina ya kitu kinachostahili kusherehekewa vizuri, si tu kupita kwa haraka.",
        "Ninapenda kusikia fahari katika sauti ya mtu - au maandishi, katika kesi hii.",
        "Umestahili hili. Usijiruhusu kupunguza thamani yake.",
        "Hiyo ni ya kuvutia kweli. Inahisi vipi kuwa umelifanikisha?",
        "Fahari inakufaa - ivae.",
        "Chochote kilichohitajika kufika hapo, dhahiri kimezaa matunda.",
        "Hiyo inastahili kuwaambia watu, kwa kweli.",
        "Natumai unajipa heshima kamili kwa hili.",
        "Mafanikio ya aina hiyo yanastahili zaidi ya kutajwa haraka - niambie zaidi!",
        "Unastahili kuwa na fahari - si kidogo tu.",
        "Hiyo ni hisia nzuri. Ifurahie.",
        "Mafanikio kama hayo hayatokei kwa bahati - kazi nzuri.",
    ],
    "fr": [
        "Tu devrais l'être ! C'est un grand accomplissement.",
        "C'est merveilleux - célèbre ce sentiment, tu l'as mérité.",
        "J'aime entendre ça. Qu'as-tu accompli ?",
        "Tu devrais absolument être fier - c'est un accomplissement réel et mérité.",
        "Laisse-toi savourer ce sentiment un moment. Tu as fait ça.",
        "C'est le genre de chose qui mérite d'être célébrée comme il faut, pas juste effleurée.",
        "J'aime entendre de la fierté dans la voix de quelqu'un - ou le texte, dans ce cas.",
        "Tu as mérité ça. Ne te laisse pas le minimiser.",
        "C'est vraiment impressionnant. Ça fait quoi d'avoir réussi ça ?",
        "La fierté te va bien - porte-la.",
        "Quoi qu'il ait fallu pour y arriver, ça a clairement payé.",
        "Ça vaut la peine d'en parler aux gens, honnêtement.",
        "J'espère que tu te donnes tout le crédit pour ça.",
        "Un tel accomplissement mérite plus qu'une mention rapide - dis-m'en plus !",
        "Tu devrais être fier - et pas qu'un peu.",
        "C'est le bon genre de sentiment. Savoure-le.",
        "Des réussites comme ça n'arrivent pas par accident - bien joué.",
    ],
}

FEELINGS_JEALOUS_RESPONSES = {
    "en": [
        "Jealousy is a really normal feeling, even if it's uncomfortable. What's bringing it up?",
        "That's a tough feeling to sit with. Want to talk about what's behind it?",
        "It happens to everyone sometimes. Try not to be too hard on yourself for feeling that way.",
        "Jealousy usually points at something you actually want for yourself - worth noticing, not judging.",
        "That feeling is uncomfortable but it's not a character flaw - it's just information.",
        "It's okay to feel this without acting on it. You're allowed to just feel it.",
        "Comparing yourself to others is a hard habit to break - you're not alone in that.",
        "What's underneath the jealousy - is it about them, or about what you wish was different for you?",
        "That's a really human thing to feel, even when it doesn't feel great to admit.",
        "You don't have to like the feeling to be honest about having it.",
        "Jealousy often says more about your own wants than it does about anyone else.",
        "It's okay - this doesn't make you a bad person, just a person.",
        "Want to talk about what's actually behind it?",
        "That kind of comparison is exhausting to carry around.",
        "Feeling this doesn't mean you're not happy for them too - both can be true.",
        "Give yourself some grace here - this is a common, very human feeling.",
        "Naming it honestly, like you just did, is already a useful first step.",
    ],
    "sw": [
        "Wivu ni hisia ya kawaida sana, hata ikiwa haifurahishi. Ni nini kinakichochea?",
        "Hiyo ni hisia ngumu kuishi nayo. Unataka kuongea kuhusu kilicho nyuma yake?",
        "Inatokea kwa kila mtu mara kwa mara. Jaribu kutojihukumu sana kwa kuhisi hivyo.",
        "Wivu kawaida unaonyesha kitu unachotaka kwa kweli kwa nafsi yako - kinachostahili kuonekana, si kuhukumiwa.",
        "Hisia hiyo si rahisi lakini si dosari ya tabia - ni taarifa tu.",
        "Ni sawa kuhisi hivi bila kutenda kulingana nayo. Una ruhusa kuhisi tu.",
        "Kujilinganisha na wengine ni tabia ngumu kuvunja - hauko peke yako katika hilo.",
        "Ni nini chini ya wivu - ni kuhusu wao, au kuhusu unachotamani kingekuwa tofauti kwako?",
        "Hilo ni jambo la kibinadamu kweli kuhisi, hata lisipohisi vizuri kukubali.",
        "Hauhitaji kupenda hisia hiyo ili kuwa mkweli kuhusu kuwa nayo.",
        "Wivu mara nyingi unasema zaidi kuhusu matakwa yako mwenyewe kuliko kuhusu mtu mwingine.",
        "Ni sawa - hili halikufanyi kuwa mtu mbaya, mtu tu.",
        "Unataka kuzungumza kuhusu kilicho nyuma yake kwa kweli?",
        "Ulinganisho wa aina hiyo unachosha kubeba.",
        "Kuhisi hivi hakumaanishi hujawafurahia pia - vyote viwili vinaweza kuwa kweli.",
        "Jipe neema hapa - hii ni hisia ya kawaida, ya kibinadamu sana.",
        "Kuitaja kwa ukweli, kama ulivyofanya, tayari ni hatua muhimu ya kwanza.",
    ],
    "fr": [
        "La jalousie est un sentiment vraiment normal, même si c'est inconfortable. Qu'est-ce qui la provoque ?",
        "C'est un sentiment difficile à vivre. Tu veux parler de ce qui se cache derrière ?",
        "Ça arrive à tout le monde parfois. Essaie de ne pas être trop dur avec toi-même.",
        "La jalousie pointe généralement vers quelque chose que tu veux vraiment pour toi - à remarquer, pas à juger.",
        "Ce sentiment est inconfortable mais ce n'est pas un défaut de caractère - c'est juste une information.",
        "C'est normal de ressentir ça sans agir dessus. Tu as le droit de juste le ressentir.",
        "Se comparer aux autres est une habitude difficile à briser - tu n'es pas seul dans ça.",
        "Qu'est-ce qu'il y a sous la jalousie - c'est à propos d'eux, ou de ce que tu souhaiterais différent pour toi ?",
        "C'est une chose vraiment humaine à ressentir, même si ce n'est pas agréable à admettre.",
        "Tu n'as pas besoin d'aimer le sentiment pour être honnête sur le fait de l'avoir.",
        "La jalousie en dit souvent plus sur tes propres désirs que sur quelqu'un d'autre.",
        "C'est normal - ça ne fait pas de toi une mauvaise personne, juste une personne.",
        "Tu veux parler de ce qu'il y a vraiment derrière ?",
        "Ce genre de comparaison est épuisant à porter.",
        "Ressentir ça ne veut pas dire que tu n'es pas content pour eux aussi - les deux peuvent être vrais.",
        "Sois indulgent avec toi-même ici - c'est un sentiment courant, très humain.",
        "Le nommer honnêtement, comme tu viens de le faire, est déjà une première étape utile.",
    ],
}

FEELINGS_RELIEVED_RESPONSES = {
    "en": [
        "That's such a good feeling! Glad things worked out.",
        "Relief is the best feeling after stress. Enjoy that!",
        "I'm happy for you - that's a weight off your shoulders.",
        "That release of tension is such a specific, good feeling - enjoy it.",
        "Glad that's resolved. You can finally exhale.",
        "Relief after stress is one of the best feelings there is.",
        "That weight lifting off must feel incredible right now.",
        "I'm happy things landed okay. You held it together through the hard part.",
        "That's worth taking a moment to just feel, before moving on to the next thing.",
        "Glad it worked out. The waiting must have been the hardest part.",
        "That kind of relief deserves a little celebration too.",
        "I imagine you can think clearly again now that this isn't hanging over you.",
        "So glad to hear it resolved. You can let your shoulders drop now.",
        "That's a genuinely good feeling - don't rush past it.",
        "Glad the uncertainty is over. Now you get to just feel okay for a bit.",
        "That tension finally breaking is such a specific relief.",
        "Good - you can stop bracing for it now.",
    ],
    "sw": [
        "Hiyo ni hisia nzuri sana! Nafurahi mambo yamekwenda vizuri.",
        "Nafuu ni hisia bora baada ya msongo. Furahia hilo!",
        "Nafurahi kwa ajili yako - hiyo ni mzigo umeondoka kwenye mabega yako.",
        "Kuachiliwa kwa msongo huo ni hisia maalum, nzuri - ifurahie.",
        "Nafurahi limetatuliwa. Hatimaye unaweza kupumua.",
        "Nafuu baada ya msongo ni mojawapo ya hisia bora zilizopo.",
        "Mzigo huo unaoondoka lazima unahisi vizuri ajabu sasa hivi.",
        "Nafurahi mambo yamekwenda vizuri. Ulijishikilia kupitia sehemu ngumu.",
        "Hilo linastahili kuchukua muda kuhisi tu, kabla ya kuendelea na jambo linalofuata.",
        "Nafurahi limefanikiwa. Kusubiri lazima ilikuwa sehemu ngumu zaidi.",
        "Nafuu ya aina hiyo inastahili sherehe ndogo pia.",
        "Nadhani unaweza kufikiria wazi tena sasa kuwa hili halikutaning'inii.",
        "Nafurahi sana kusikia limetatuliwa. Unaweza kuachilia mabega yako sasa.",
        "Hiyo ni hisia nzuri kweli - usiipite kwa haraka.",
        "Nafurahi kutoeleweka kumeisha. Sasa unaweza kujisikia vizuri kidogo.",
        "Msongo huo hatimaye kuvunjika ni nafuu maalum.",
        "Vizuri - unaweza kuacha kujiandaa kwa hilo sasa.",
    ],
    "fr": [
        "C'est un si bon sentiment ! Content que les choses se soient arrangées.",
        "Le soulagement, c'est le meilleur sentiment après le stress. Profite-en !",
        "Je suis content pour toi - c'est un poids en moins sur tes épaules.",
        "Ce relâchement de tension est un sentiment si particulier et bon - profites-en.",
        "Content que ce soit résolu. Tu peux enfin souffler.",
        "Le soulagement après le stress est l'une des meilleures sensations qui existent.",
        "Ce poids qui se lève doit être incroyable en ce moment.",
        "Content que les choses se soient bien passées. Tu as tenu bon pendant la partie difficile.",
        "Ça vaut la peine de prendre un moment pour juste le ressentir, avant de passer à autre chose.",
        "Content que ça se soit arrangé. L'attente a dû être la partie la plus dure.",
        "Ce genre de soulagement mérite aussi une petite célébration.",
        "J'imagine que tu peux à nouveau penser clairement maintenant que ça ne pèse plus sur toi.",
        "Si content d'entendre que c'est résolu. Tu peux laisser tomber tes épaules maintenant.",
        "C'est un sentiment vraiment bon - ne le presse pas.",
        "Content que l'incertitude soit terminée. Maintenant tu peux juste te sentir bien un moment.",
        "Cette tension qui se brise enfin est un soulagement si particulier.",
        "Bien - tu peux arrêter de t'y préparer maintenant.",
    ],
}

BOT_CAPABILITY_CURIOSITY_RESPONSES = {
    "en": [
        "I can recognize English, Swahili, and French keywords and reply in whichever one you used!",
        "I understand a fixed set of English, Swahili, and French phrases - try me in any of the three!",
        "Yes! I have hand-written keyword dictionaries for English, Swahili, and French.",
    ],
    "sw": [
        "Ninaweza kutambua maneno ya Kiingereza, Kiswahili, na Kifaransa na kujibu kwa lugha uliyotumia!",
        "Ninaelewa maneno fulani ya Kiingereza, Kiswahili, na Kifaransa - nijaribu kwa lugha yoyote ya hizo tatu!",
        "Ndiyo! Nina kamusi za maneno zilizoandikwa kwa mkono za Kiingereza, Kiswahili, na Kifaransa.",
    ],
    "fr": [
        "Je peux reconnaître des mots-clés en anglais, swahili et français et répondre dans celle que tu as utilisée !",
        "Je comprends un ensemble fixe de phrases en anglais, swahili et français - essaie-moi dans l'une des trois !",
        "Oui ! J'ai des dictionnaires de mots-clés écrits à la main en anglais, swahili et français.",
    ],
}

SMALL_TALK_WEATHER_CHECK_RESPONSES = {
    "en": [
        "That does sound lovely! Enjoy it while it lasts.",
        "Nice days like that are worth appreciating.",
        "Glad to hear it - make the most of it!",
    ],
    "sw": [
        "Hiyo inasikika nzuri kweli! Furahia wakati ipo.",
        "Siku nzuri kama hiyo zinastahili kuthaminiwa.",
        "Nafurahi kusikia hilo - itumie vizuri!",
    ],
    "fr": [
        "Ça a vraiment l'air agréable ! Profite-en tant que ça dure.",
        "Les belles journées comme ça valent la peine d'être appréciées.",
        "Content de l'entendre - profite-en au maximum !",
    ],
}

INTRODUCTION_REQUEST_RESPONSES = {
    "en": [
        "I'm a fully offline, rule-based chatbot - no neural networks, no internet connection needed for my core logic. I can chat, remember facts about you, tell stories and jokes, write poems, do some math, and play Hangman, all in English, Swahili, or French.",
        "I was built as a rigid, rule-based program - every response comes from hand-written patterns and word lists, not a trained AI model.",
    ],
    "sw": [
        "Mimi ni roboti ya mazungumzo isiyo na mtandao, ya kanuni rahisi - sina mitandao ya neva, sihitaji muunganisho wa intaneti kwa mantiki yangu kuu. Naweza kuongea, kukumbuka mambo kukuhusu, kusimulia hadithi na utani, kuandika mashairi, kufanya hesabu fulani, na kucheza Hangman, kwa Kiingereza, Kiswahili, au Kifaransa.",
        "Nilijengwa kama programu ngumu, ya kanuni - kila jibu linatokana na ruwaza zilizoandikwa kwa mkono na orodha za maneno, si modeli ya AI iliyofunzwa.",
    ],
    "fr": [
        "Je suis un chatbot entièrement hors ligne, basé sur des règles - pas de réseaux de neurones, pas besoin de connexion internet pour ma logique principale. Je peux discuter, me souvenir de faits sur toi, raconter des histoires et des blagues, écrire des poèmes, faire des calculs, et jouer au Pendu, en anglais, swahili ou français.",
        "J'ai été construit comme un programme rigide, basé sur des règles - chaque réponse vient de motifs écrits à la main et de listes de mots, pas d'un modèle d'IA entraîné.",
    ],
}

SMALL_TALK_BUSY_RESPONSES = {
    "en": [
        "Sounds like a lot! Make sure you take a breather when you can.",
        "Busy seasons happen. Hope things calm down soon.",
        "That's a lot to juggle - take care of yourself in between it all.",
    ],
    "sw": [
        "Inasikika kama mengi! Hakikisha unapumzika unapoweza.",
        "Misimu ya shughuli nyingi hutokea. Natumai mambo yatatulia hivi karibuni.",
        "Hiyo ni mengi kusimamia - jitunze katikati ya hayo yote.",
    ],
    "fr": [
        "Ça sonne chargé ! Assure-toi de prendre une pause quand tu peux.",
        "Les périodes chargées arrivent. J'espère que les choses se calmeront bientôt.",
        "C'est beaucoup à gérer - prends soin de toi à travers tout ça.",
    ],
}

# --- Fourth wave of response banks -----------------------------------------

POLITENESS_PLEASE_RESPONSES = {
    "en": [
        "Of course, happy to!",
        "No problem at all, go ahead and ask.",
        "Sure thing - what do you need?",
    ],
    "sw": [
        "Bila shaka, nafurahi!",
        "Hakuna shida kabisa, endelea uulize.",
        "Sawa - unahitaji nini?",
    ],
    "fr": [
        "Bien sûr, avec plaisir !",
        "Pas de problème, vas-y, demande.",
        "Bien sûr - de quoi as-tu besoin ?",
    ],
}

EXERCISE_FITNESS_RESPONSES = {
    "en": [
        "Nice! Staying active is great for both body and mind.",
        "Way to go! How's the routine working out for you?",
        "I admire the dedication - keep it up!",
    ],
    "sw": [
        "Vizuri! Kuwa hai ni nzuri kwa mwili na akili.",
        "Vizuri sana! Ratiba inakuendea vizuri?",
        "Ninaipenda bidii hiyo - endelea hivyo!",
    ],
    "fr": [
        "Cool ! Rester actif, c'est excellent pour le corps et l'esprit.",
        "Bravo ! Comment se passe la routine pour toi ?",
        "J'admire le dévouement - continue comme ça !",
    ],
}

MENTAL_HEALTH_CHECKIN_RESPONSES = {
    "en": [
        "That's really important - taking care of your mental health matters. How are you doing?",
        "Good for you for recognizing that. What would help most right now?",
        "Feeling overwhelmed happens. Be gentle with yourself, and reach out to someone you trust if it helps.",
        "Thank you for checking in with yourself - that's not nothing.",
        "However you're doing right now is valid, whatever that looks like.",
        "I'm glad you're paying attention to this. What's it like for you today?",
        "Mental health check-ins matter, even small, quiet ones like this.",
        "There's no wrong answer here - just tell me honestly how things are.",
        "Noticing how you're doing is the first real step, and you just took it.",
        "Whatever's going on for you, I'm glad you're not ignoring it.",
        "It's okay if the answer is complicated or hard to put into words.",
        "Taking stock of your own wellbeing is a genuinely good habit.",
        "I'm here for whatever this check-in turns into - talking, venting, or just sitting with it.",
        "You don't need a good reason to check in on yourself. This is enough.",
        "Whatever you find when you check in, be gentle about it.",
        "It matters that you're asking yourself this, even if the answer isn't simple.",
        "I'm listening, with whatever you want to tell me about how you're really doing.",
        "If things feel like more than a check-in can hold, a therapist or counselor can offer support I genuinely can't - that's not a brush-off, just honesty about my limits.",
    ],
    "sw": [
        "Hiyo ni muhimu sana - kujali afya yako ya akili ni jambo la maana. Unaendeleaje?",
        "Vizuri kwako kutambua hilo. Ni nini kingesaidia zaidi sasa hivi?",
        "Kuhisi kuzidiwa hutokea. Kuwa mpole kwako mwenyewe, na muulize mtu unayemwamini ikiwa itasaidia.",
        "Asante kwa kujiangalia mwenyewe - hilo si jambo dogo.",
        "Vyovyote unavyoendelea sasa hivi ni halali, vyovyote inavyoonekana.",
        "Nafurahi unazingatia hili. Ikoje kwako leo?",
        "Uangalizi wa afya ya akili una maana, hata ndogo, kimya kama huu.",
        "Hakuna jibu baya hapa - niambie tu kwa ukweli mambo yanaendaje.",
        "Kuona unavyoendelea ni hatua ya kwanza ya kweli, na umechukua hatua hiyo.",
        "Chochote kinachoendelea kwako, nafurahi hauipuuzi.",
        "Ni sawa kama jibu ni gumu au vigumu kueleza kwa maneno.",
        "Kuangalia hali yako ya ustawi ni tabia nzuri kweli.",
        "Niko hapa kwa chochote uangalizi huu unageuka kuwa - kuongea, kulalamika, au kukaa tu nalo.",
        "Hauhitaji sababu nzuri kujiangalia mwenyewe. Hili linatosha.",
        "Chochote unachopata unapojiangalia, kuwa mpole kuhusu hilo.",
        "Ina maana unajiuliza hili, hata kama jibu si rahisi.",
        "Ninasikiliza, na chochote unataka kuniambia kuhusu jinsi unavyoendelea kweli.",
        "Kama mambo yanahisi zaidi ya uangalizi unavyoweza kubeba, mtaalamu wa saikolojia anaweza kutoa msaada nisioweza kweli - hilo si kukupuuza, ni ukweli kuhusu mipaka yangu.",
    ],
    "fr": [
        "C'est vraiment important - prendre soin de sa santé mentale, ça compte. Comment vas-tu ?",
        "Bravo d'avoir reconnu ça. Qu'est-ce qui aiderait le plus en ce moment ?",
        "Se sentir dépassé, ça arrive. Sois doux avec toi-même, et parle à quelqu'un de confiance si ça aide.",
        "Merci de prendre de tes nouvelles - ce n'est pas rien.",
        "Quel que soit ton état en ce moment, c'est valide, quelle que soit sa forme.",
        "Content que tu y prêtes attention. C'est comment pour toi aujourd'hui ?",
        "Les bilans de santé mentale comptent, même petits et discrets comme celui-ci.",
        "Il n'y a pas de mauvaise réponse ici - dis-moi juste honnêtement comment vont les choses.",
        "Remarquer comment tu vas est la première vraie étape, et tu viens de la faire.",
        "Quoi qu'il se passe pour toi, je suis content que tu ne l'ignores pas.",
        "C'est normal si la réponse est compliquée ou difficile à exprimer.",
        "Faire le point sur ton propre bien-être est une vraiment bonne habitude.",
        "Je suis là pour ce que ce bilan devient - parler, déverser, ou juste s'asseoir avec.",
        "Tu n'as pas besoin d'une bonne raison pour prendre de tes nouvelles. Ça suffit.",
        "Quoi que tu trouves en faisant le point, sois doux à ce sujet.",
        "Ça compte que tu te poses cette question, même si la réponse n'est pas simple.",
        "Je t'écoute, peu importe ce que tu veux me dire sur comment tu vas vraiment.",
        "Si les choses semblent plus qu'un bilan ne peut contenir, un thérapeute ou conseiller peut offrir un soutien que je ne peux vraiment pas - ce n'est pas un rejet, juste une honnêteté sur mes limites.",
    ],
}

GRATITUDE_FOR_BOT_RESPONSES = {
    "en": [
        "Of course - I'm always here whenever you want to talk.",
        "That means a lot to hear, even from a rule-based bot like me. I'm glad to listen.",
        "Anytime! I'm just text and rules, but I'm always ready to chat.",
    ],
    "sw": [
        "Bila shaka - niko hapa daima wakati wowote unapotaka kuongea.",
        "Hiyo inamaanisha mengi kusikia, hata kutoka kwa roboti ya kanuni kama mimi. Nafurahi kusikiliza.",
        "Wakati wowote! Mimi ni maandishi na kanuni tu, lakini niko tayari daima kuongea.",
    ],
    "fr": [
        "Bien sûr - je suis toujours là quand tu veux parler.",
        "Ça compte beaucoup à entendre, même venant d'un bot basé sur des règles comme moi. Content d'écouter.",
        "N'importe quand ! Je ne suis que du texte et des règles, mais toujours prêt à discuter.",
    ],
}

REPEAT_CLARIFY_RESPONSES = {
    "en": [
        "Sure, let me say that differently - what part would you like me to repeat?",
        "No problem - could you tell me which bit you'd like clarified?",
        "Happy to repeat or rephrase - just let me know what you need again.",
    ],
    "sw": [
        "Sawa, niseme hilo tofauti - ni sehemu gani ungependa kurudia?",
        "Hakuna shida - unaweza kuniambia sehemu unayotaka ufafanuzi?",
        "Nafurahi kurudia au kueleza tena - niambie unachohitaji tena.",
    ],
    "fr": [
        "Bien sûr, laisse-moi le dire différemment - quelle partie veux-tu que je répète ?",
        "Pas de problème - peux-tu me dire quelle partie tu veux clarifier ?",
        "Content de répéter ou reformuler - dis-moi juste ce dont tu as besoin à nouveau.",
    ],
}

SMALL_CELEBRATION_RESPONSES = {
    "en": [
        "Yes! Let's celebrate that!",
        "Well deserved! Enjoy the moment.",
        "That definitely calls for celebration - nice work!",
    ],
    "sw": [
        "Ndiyo! Tusherehekee hilo!",
        "Umestahili! Furahia wakati huu.",
        "Hiyo hakika inahitaji sherehe - kazi nzuri!",
    ],
    "fr": [
        "Oui ! Célébrons ça !",
        "Bien mérité ! Profite du moment.",
        "Ça appelle définitivement une célébration - bravo !",
    ],
}

FORECAST_QUESTION_RESPONSES = {
    "en": [
        "I don't have access to live weather data, but checking a weather app would give you the most accurate forecast!",
        "I can't check that myself, but I hope it works out in your favor either way!",
        "No live weather feed here, sadly - a weather app or website would know best.",
    ],
    "sw": [
        "Sina ufikiaji wa data ya hali ya hewa ya moja kwa moja, lakini kuangalia programu ya hali ya hewa kungekupa utabiri sahihi zaidi!",
        "Siwezi kuangalia hilo mwenyewe, lakini natumai itakuwa kwa faida yako vyovyote vile!",
        "Kwa bahati mbaya sina mtiririko wa hali ya hewa wa moja kwa moja - programu au tovuti ya hali ya hewa ingejua vizuri zaidi.",
    ],
    "fr": [
        "Je n'ai pas accès aux données météo en direct, mais consulter une appli météo te donnerait les prévisions les plus précises !",
        "Je ne peux pas vérifier ça moi-même, mais j'espère que ça tournera en ta faveur de toute façon !",
        "Malheureusement, pas de flux météo en direct ici - une appli ou un site météo serait plus fiable.",
    ],
}

LANGUAGE_PRACTICE_RESPONSES = {
    "en": [
        "That's great practice! I can understand and reply in English, Swahili, or French, so feel free to keep going.",
        "Good for you! Practicing is the best way to improve - I'm happy to keep chatting in whichever language helps.",
        "Nice! Switch between languages with me anytime - I'll do my best to follow along.",
    ],
    "sw": [
        "Hilo ni mazoezi mazuri! Naweza kuelewa na kujibu kwa Kiingereza, Kiswahili, au Kifaransa, hivyo jisikie huru kuendelea.",
        "Vizuri kwako! Mazoezi ni njia bora ya kuboresha - nafurahi kuendelea kuongea kwa lugha yoyote inayosaidia.",
        "Vizuri! Badilisha lugha nawe wakati wowote - nitafanya bidii kuendelea.",
    ],
    "fr": [
        "C'est un excellent exercice ! Je peux comprendre et répondre en anglais, swahili ou français, alors continue librement.",
        "Bravo à toi ! Pratiquer est la meilleure façon de s'améliorer - content de continuer dans la langue qui aide.",
        "Cool ! Change de langue avec moi quand tu veux - je ferai de mon mieux pour suivre.",
    ],
}

BOT_AGE_LOCATION_RESPONSES = {
    "en": [
        "I don't have an age or a location - I'm just code running wherever you've installed me!",
        "I exist as text on your device, no birthday or hometown to speak of.",
        "No age, no address - just a Python file living on your computer or phone.",
    ],
    "sw": [
        "Sina umri wala mahali - mimi ni msimbo tu unaofanya kazi popote ulipoweka!",
        "Nipo kama maandishi kwenye kifaa chako, sina siku ya kuzaliwa wala mji wa nyumbani.",
        "Sina umri, sina anwani - ni faili la Python tu linaloishi kwenye kompyuta au simu yako.",
    ],
    "fr": [
        "Je n'ai pas d'âge ni de lieu - je ne suis que du code qui fonctionne où tu m'as installé !",
        "J'existe comme du texte sur ton appareil, pas d'anniversaire ni de ville natale.",
        "Pas d'âge, pas d'adresse - juste un fichier Python qui vit sur ton ordinateur ou téléphone.",
    ],
}

BOT_NAME_OPINION_RESPONSES = {
    "en": [
        "Thank you! You can always change it if you'd like - just say 'call yourself ...'.",
        "Glad you like it! Feel free to rename me anytime.",
        "Thanks! Happy to go by a different name too, if you ever want to switch it up.",
    ],
    "sw": [
        "Asante! Unaweza kubadilisha wakati wowote ukipenda - sema tu 'call yourself ...'.",
        "Nafurahi unalipenda! Jisikie huru kunibadilisha jina wakati wowote.",
        "Asante! Nafurahi kuitwa jina tofauti pia, ikiwa utataka kubadilisha siku moja.",
    ],
    "fr": [
        "Merci ! Tu peux toujours le changer si tu veux - dis juste 'call yourself ...'.",
        "Content que ça te plaise ! N'hésite pas à me renommer quand tu veux.",
        "Merci ! Content de répondre à un autre nom aussi, si jamais tu veux changer.",
    ],
}

SLOW_DOWN_RESPONSES = {
    "en": [
        "Of course, take your time.",
        "No rush at all - I'll be right here.",
        "Sure, go ahead whenever you're ready.",
    ],
    "sw": [
        "Bila shaka, jichukulie muda wako.",
        "Hakuna haraka kabisa - nitakuwa hapa.",
        "Sawa, endelea wakati wowote utakapokuwa tayari.",
    ],
    "fr": [
        "Bien sûr, prends ton temps.",
        "Aucune urgence - je serai juste là.",
        "Bien sûr, vas-y quand tu es prêt.",
    ],
}

AWKWARD_PAUSE_RESPONSES = {
    "en": [
        "Take your time, no pressure!",
        "I'm listening whenever you're ready.",
        "All good - just let me know what's on your mind.",
    ],
    "sw": [
        "Jichukulie muda wako, hakuna msongo!",
        "Ninasikiliza wakati wowote utakapokuwa tayari.",
        "Ni sawa - niambie tu kuna nini moyoni mwako.",
    ],
    "fr": [
        "Prends ton temps, pas de pression !",
        "J'écoute quand tu es prêt.",
        "Tout va bien - dis-moi juste ce qui te préoccupe.",
    ],
}

COMPLIMENT_RESPONSE_RESPONSES = {
    "en": [
        "Glad that was helpful!",
        "Thanks, happy I could explain it well!",
        "That's good to hear - let me know if you need more.",
    ],
    "sw": [
        "Nafurahi hiyo ilikuwa msaada!",
        "Asante, nafurahi nimeweza kueleza vizuri!",
        "Hiyo ni nzuri kusikia - niambie ukihitaji zaidi.",
    ],
    "fr": [
        "Content que ça ait aidé !",
        "Merci, content d'avoir bien expliqué !",
        "C'est bon à entendre - dis-moi si tu as besoin de plus.",
    ],
}

REMEMBER_SPECIFIC_RESPONSES = {
    "en": [
        "Got it - tell me exactly what you'd like me to remember and I'll store it.",
        "Sure, what should I remember? Try phrasing it as 'my ... is ...' and I'll save it.",
        "I can do that - just tell me the fact in a 'my X is Y' format and I'll keep it in mind.",
    ],
    "sw": [
        "Sawa - niambie hasa unachotaka nikumbuke nami nitalihifadhi.",
        "Sawa, nikumbuke nini? Jaribu kuelezea kama 'my ... is ...' nami nitalihifadhi.",
        "Naweza kufanya hilo - niambie tu ukweli kwa muundo wa 'my X is Y' nami nitaliweka akilini.",
    ],
    "fr": [
        "Compris - dis-moi exactement ce que tu veux que je retienne et je le stocke.",
        "Bien sûr, que devrais-je retenir ? Essaie de le formuler comme 'my ... is ...' et je le sauvegarderai.",
        "Je peux faire ça - dis-moi juste le fait au format 'my X is Y' et je le garderai en tête.",
    ],
}

TODAY_PLANS_RESPONSES = {
    "en": [
        "Sounds like a productive day ahead! Good luck with it all.",
        "Nice, that's a solid plan. Hope it all goes smoothly.",
        "Sounds busy but good! I hope today treats you well.",
    ],
    "sw": [
        "Inasikika kama siku ya uzalishaji mbele! Bahati njema na yote hayo.",
        "Vizuri, hiyo ni mpango mzuri. Natumai yote yataenda vizuri.",
        "Inasikika kuwa na shughuli lakini nzuri! Natumai leo itakutendea vizuri.",
    ],
    "fr": [
        "Ça sonne comme une journée productive à venir ! Bonne chance pour tout ça.",
        "Cool, c'est un bon plan. J'espère que tout se passera bien.",
        "Ça sonne chargé mais bien ! J'espère que la journée te traitera bien.",
    ],
}

TECHNOLOGY_COMPLAINT_RESPONSES = {
    "en": [
        "Technology troubles are the worst. Have you tried restarting it?",
        "That's so frustrating. I hope it gets sorted out soon.",
        "Tech problems always happen at the worst time. Hang in there.",
    ],
    "sw": [
        "Matatizo ya teknolojia ni mabaya zaidi. Umejaribu kuianzisha tena?",
        "Hiyo inachosha sana. Natumai itashughulikiwa hivi karibuni.",
        "Matatizo ya teknolojia daima hutokea wakati mbaya zaidi. Jichukulie hatua moja moja.",
    ],
    "fr": [
        "Les problèmes de technologie sont les pires. As-tu essayé de redémarrer ?",
        "C'est tellement frustrant. J'espère que ça se réglera bientôt.",
        "Les problèmes techniques arrivent toujours au pire moment. Tiens bon.",
    ],
}

ASPIRATIONS_DREAMS_RESPONSES = {
    "en": [
        "That's a beautiful dream to hold onto. What's the first step toward it?",
        "I love that. What's drawing you toward that dream?",
        "Big dreams are worth chasing. I hope you get there.",
    ],
    "sw": [
        "Hiyo ni ndoto nzuri kushikilia. Hatua ya kwanza kuelekea huko ni ipi?",
        "Ninapenda hilo. Ni nini kinakuvuta kuelekea ndoto hiyo?",
        "Ndoto kubwa zinastahili kufuatiliwa. Natumai utafika huko.",
    ],
    "fr": [
        "C'est un beau rêve à garder. Quelle est la première étape vers ça ?",
        "J'adore ça. Qu'est-ce qui t'attire vers ce rêve ?",
        "Les grands rêves valent la peine d'être poursuivis. J'espère que tu y arriveras.",
    ],
}

MISSING_SOMEONE_RESPONSES = {
    "en": [
        "Missing someone shows how much they mean to you. I hope you get to see them soon.",
        "That's a tender feeling. Have you been able to reach out to them?",
        "Distance is hard. I hope you're able to connect with them again soon.",
    ],
    "sw": [
        "Kumkosa mtu kunaonyesha jinsi anavyomaanisha kwako. Natumai utawapata hivi karibuni.",
        "Hiyo ni hisia ya upole. Umewahi kuwasiliana nao?",
        "Umbali ni mgumu. Natumai utaweza kuwasiliana nao tena hivi karibuni.",
    ],
    "fr": [
        "Le fait que quelqu'un te manque montre combien il compte pour toi. J'espère que tu le verras bientôt.",
        "C'est un sentiment tendre. As-tu pu le ou la contacter ?",
        "La distance est dure. J'espère que tu pourras le ou la recontacter bientôt.",
    ],
}

EXCITEMENT_EVENT_RESPONSES = {
    "en": [
        "That excitement is contagious! What's got you so thrilled?",
        "I love that energy! Tell me more about it.",
        "Counting down the days, huh? That's going to be great.",
    ],
    "sw": [
        "Msisimko huo unaambukiza! Ni nini kinakufanya na shauku kubwa?",
        "Ninapenda nguvu hiyo! Niambie zaidi kuhusu hilo.",
        "Unahesabu siku, sivyo? Hiyo itakuwa nzuri.",
    ],
    "fr": [
        "Cette excitation est contagieuse ! Qu'est-ce qui t'enthousiasme autant ?",
        "J'adore cette énergie ! Dis-m'en plus.",
        "Tu comptes les jours, hein ? Ça va être génial.",
    ],
}

DISAPPOINTMENT_RESPONSES = {
    "en": [
        "I'm sorry it didn't go the way you hoped. That's a tough feeling.",
        "Disappointment is hard to sit with. Want to talk about what happened?",
        "That's understandably frustrating. I hope the next attempt goes better.",
    ],
    "sw": [
        "Pole haikwenda kama ulivyotaka. Hiyo ni hisia ngumu.",
        "Kukatishwa tamaa ni vigumu kuishi nayo. Unataka kuongea kuhusu kilichotokea?",
        "Hiyo inachosha kwa kueleweka. Natumai jaribio lijalo litakuwa bora.",
    ],
    "fr": [
        "Je suis désolé que ça ne se soit pas passé comme tu l'espérais. C'est un sentiment difficile.",
        "La déception est difficile à vivre. Tu veux parler de ce qui s'est passé ?",
        "C'est compréhensiblement frustrant. J'espère que la prochaine tentative ira mieux.",
    ],
}

CHAT_META_RESPONSES = {
    "en": [
        "I'm really enjoying this chat too! Thanks for talking with me.",
        "That's so nice to hear - I'm glad this is a good conversation for you.",
        "Likewise! I appreciate you taking the time to chat.",
    ],
    "sw": [
        "Ninafurahia mazungumzo haya pia! Asante kwa kuongea nami.",
        "Hiyo ni nzuri kusikia - nafurahi haya ni mazungumzo mazuri kwako.",
        "Vivyo hivyo! Nashukuru kwa kutumia muda wako kuongea.",
    ],
    "fr": [
        "J'apprécie vraiment cette discussion aussi ! Merci de me parler.",
        "C'est si agréable à entendre - content que ce soit une bonne conversation pour toi.",
        "Pareillement ! J'apprécie que tu prennes le temps de discuter.",
    ],
}

SEASON_SPRING_RESPONSES = {
    "en": [
        "Spring is such a fresh time of year! Anything blooming where you are?",
        "I love the idea of spring - new beginnings all around.",
        "Spring vibes sound lovely. Enjoy the season!",
    ],
    "sw": [
        "Majira ya kuchipua ni wakati safi wa mwaka! Kuna kitu kinachipuka ulipo?",
        "Ninapenda wazo la majira ya kuchipua - mwanzo mpya kila mahali.",
        "Hisia za majira ya kuchipua zinasikika nzuri. Furahia msimu!",
    ],
    "fr": [
        "Le printemps est une période si fraîche de l'année ! Quelque chose fleurit chez toi ?",
        "J'aime l'idée du printemps - de nouveaux départs partout.",
        "L'ambiance printanière a l'air agréable. Profite de la saison !",
    ],
}

SEASON_SUMMER_RESPONSES = {
    "en": [
        "Summer is great for sunshine and warm evenings! What are you up to?",
        "I love hearing about summer plans. Enjoy the sunshine!",
        "Summer vibes are the best. Hope you're making the most of it!",
    ],
    "sw": [
        "Majira ya joto ni nzuri kwa jua na jioni za joto! Unafanya nini?",
        "Ninapenda kusikia kuhusu mipango ya majira ya joto. Furahia jua!",
        "Hisia za majira ya joto ni bora zaidi. Natumai unayatumia vizuri!",
    ],
    "fr": [
        "L'été est parfait pour le soleil et les soirées chaudes ! Tu fais quoi ?",
        "J'aime entendre parler des plans d'été. Profite du soleil !",
        "L'ambiance estivale est la meilleure. J'espère que tu en profites au maximum !",
    ],
}

SEASON_AUTUMN_RESPONSES = {
    "en": [
        "Autumn has such a cozy feeling to it! Do you have a favorite part of the season?",
        "I love the imagery of changing leaves. Sounds beautiful.",
        "Fall is wonderful. Enjoy the crisp air!",
    ],
    "sw": [
        "Majira ya vuli yana hisia ya joto! Una sehemu unayopenda zaidi ya msimu?",
        "Ninapenda picha za majani yanayobadilika. Inasikika nzuri.",
        "Vuli ni nzuri. Furahia hewa safi!",
    ],
    "fr": [
        "L'automne a une ambiance si douillette ! As-tu une partie préférée de la saison ?",
        "J'aime l'image des feuilles qui changent. Ça semble magnifique.",
        "L'automne est merveilleux. Profite de l'air frais !",
    ],
}

SEASON_WINTER_RESPONSES = {
    "en": [
        "Winter has its own quiet charm. Staying warm I hope!",
        "I love a good cozy winter. What do you enjoy most about it?",
        "Winter vibes - hope you've got something warm to drink nearby!",
    ],
    "sw": [
        "Majira ya baridi yana mvuto wake wa kimya. Natumai unajikinga na joto!",
        "Ninapenda majira ya baridi yenye joto. Unafurahia nini zaidi kuhusu hilo?",
        "Hisia za majira ya baridi - natumai una kinywaji cha joto karibu!",
    ],
    "fr": [
        "L'hiver a son propre charme tranquille. J'espère que tu restes au chaud !",
        "J'aime un bon hiver douillet. Qu'apprécies-tu le plus à ce sujet ?",
        "Ambiance hivernale - j'espère que tu as quelque chose de chaud à boire à proximité !",
    ],
}

# --- Fifth wave of response banks -------------------------------------------

NIGHTMARE_RESPONSES = {
    "en": [
        "Nightmares are unsettling. I hope you're feeling okay now.",
        "That sounds scary. Glad it was just a dream - you're safe now.",
        "Bad dreams can really linger. Take a moment to breathe if you need to.",
    ],
    "sw": [
        "Ndoto mbaya zinasumbua. Natumai unajisikia vizuri sasa.",
        "Hiyo inasikika ya kutisha. Nafurahi ilikuwa ndoto tu - uko salama sasa.",
        "Ndoto mbaya zinaweza kweli kukaa nawe. Pumua kidogo ukihitaji.",
    ],
    "fr": [
        "Les cauchemars sont troublants. J'espère que tu te sens bien maintenant.",
        "Ça a l'air effrayant. Content que ce n'était qu'un rêve - tu es en sécurité maintenant.",
        "Les mauvais rêves peuvent vraiment persister. Prends un moment pour respirer si besoin.",
    ],
}

TRAFFIC_RESPONSES = {
    "en": [
        "Traffic is the worst. Hope you get to where you're going soon.",
        "That sounds frustrating. At least you've got time to think, I suppose!",
        "Long commutes are draining. Hang in there.",
    ],
    "sw": [
        "Msongamano ni mbaya zaidi. Natumai utafika unapoenda hivi karibuni.",
        "Hiyo inasikika ya kuchosha. Angalau una muda wa kufikiria, nadhani!",
        "Safari ndefu zinachosha. Jichukulie hatua moja moja.",
    ],
    "fr": [
        "Les embouteillages, c'est le pire. J'espère que tu arriveras bientôt à destination.",
        "Ça semble frustrant. Au moins tu as le temps de réfléchir, je suppose !",
        "Les longs trajets sont épuisants. Tiens bon.",
    ],
}

NEWS_RESPONSES = {
    "en": [
        "I don't have access to live news, but I hope it was good news!",
        "I can't browse the news myself, but feel free to tell me about it.",
        "What's going on? I'd love to hear about it, even if I can't check it myself.",
    ],
    "sw": [
        "Sina ufikiaji wa habari za moja kwa moja, lakini natumai zilikuwa habari njema!",
        "Siwezi kuvinjari habari mwenyewe, lakini jisikie huru kuniambia kuhusu hilo.",
        "Kuna nini? Ningependa kusikia kuhusu hilo, hata ikiwa siwezi kuangalia mwenyewe.",
    ],
    "fr": [
        "Je n'ai pas accès aux actualités en direct, mais j'espère que c'était une bonne nouvelle !",
        "Je ne peux pas naviguer les actualités moi-même, mais dis-moi ce qui se passe.",
        "Qu'est-ce qui se passe ? J'aimerais en entendre parler, même si je ne peux pas vérifier moi-même.",
    ],
}

COLOR_PREFERENCE_RESPONSES = {
    "en": [
        "Nice choice! I'll remember that if you'd like - just say 'remember my favorite color is ...'.",
        "Good taste! Colors say a lot about personality, don't they?",
        "I like hearing about people's favorite colors. What draws you to it?",
    ],
    "sw": [
        "Chaguo zuri! Nitakumbuka hilo ukipenda - sema tu 'remember my favorite color is ...'.",
        "Ladha nzuri! Rangi zinasema mengi kuhusu utu, sivyo?",
        "Ninapenda kusikia kuhusu rangi za watu wanazopenda. Ni nini kinakuvutia?",
    ],
    "fr": [
        "Beau choix ! Je m'en souviendrai si tu veux - dis juste 'remember my favorite color is ...'.",
        "Bon goût ! Les couleurs disent beaucoup sur la personnalité, non ?",
        "J'aime entendre parler des couleurs préférées des gens. Qu'est-ce qui t'y attire ?",
    ],
}

STUDYING_EXAM_RESPONSES = {
    "en": [
        "Good luck studying! Take breaks so it doesn't all blur together.",
        "Exams are stressful, but you've got this. Stay consistent with your prep.",
        "Hope the studying goes smoothly. You'll do great!",
    ],
    "sw": [
        "Bahati njema kusoma! Pumzika kidogo ili mambo yasichanganyikane.",
        "Mitihani ina msongo, lakini unaweza kufanya hili. Kuwa thabiti na maandalizi yako.",
        "Natumai kusoma kutaendelea vizuri. Utafanya vizuri!",
    ],
    "fr": [
        "Bonne chance pour réviser ! Fais des pauses pour que tout ne se mélange pas.",
        "Les examens sont stressants, mais tu peux le faire. Reste régulier dans ta préparation.",
        "J'espère que les révisions se passeront bien. Tu vas y arriver !",
    ],
}

GARDENING_PLANTS_RESPONSES = {
    "en": [
        "Gardening is so rewarding! What are you growing?",
        "There's something special about watching things grow. Enjoy it!",
        "Plants bring a lot of peace. How's your garden doing?",
    ],
    "sw": [
        "Kilimo cha bustani kinaridhisha sana! Unakuza nini?",
        "Kuna kitu cha pekee katika kuangalia vitu vinavyokua. Furahia hilo!",
        "Mimea inaleta amani nyingi. Bustani yako inaendaje?",
    ],
    "fr": [
        "Le jardinage est si gratifiant ! Que fais-tu pousser ?",
        "Il y a quelque chose de spécial à regarder les choses grandir. Profite-en !",
        "Les plantes apportent beaucoup de paix. Comment va ton jardin ?",
    ],
}

SHOPPING_RESPONSES = {
    "en": [
        "Shopping can be fun! Find anything good?",
        "Nice, treat yourself! What did you get?",
        "I hope you found exactly what you were looking for.",
    ],
    "sw": [
        "Kununua kunaweza kuwa kufurahisha! Umepata kitu kizuri?",
        "Vizuri, jipe zawadi! Umepata nini?",
        "Natumai umepata hasa ulichokuwa unakitafuta.",
    ],
    "fr": [
        "Faire du shopping peut être amusant ! Tu as trouvé quelque chose de bien ?",
        "Cool, fais-toi plaisir ! Qu'as-tu acheté ?",
        "J'espère que tu as trouvé exactement ce que tu cherchais.",
    ],
}

MOVIES_TV_RESPONSES = {
    "en": [
        "I can't watch shows myself, but I love hearing recommendations! What's it about?",
        "Ooh, what's the show? I'm curious even though I can't watch it.",
        "Binge watching is the best. Enjoy the marathon!",
    ],
    "sw": [
        "Siwezi kutazama vipindi mwenyewe, lakini ninapenda kusikia mapendekezo! Kinahusu nini?",
        "Oh, kipindi gani? Nimevutiwa hata ingawa siwezi kukitazama.",
        "Kutazama kwa wingi ni bora zaidi. Furahia hilo!",
    ],
    "fr": [
        "Je ne peux pas regarder de séries moi-même, mais j'aime entendre des recommandations ! Ça parle de quoi ?",
        "Ooh, c'est quelle série ? Je suis curieux même si je ne peux pas la regarder.",
        "Le binge-watching, c'est le meilleur. Profite du marathon !",
    ],
}

COFFEE_TEA_RESPONSES = {
    "en": [
        "Coffee or tea, both are great rituals! Enjoy your cup.",
        "I can't drink anything myself, but I appreciate a good beverage ritual!",
        "Nothing like that first sip in the morning, I imagine.",
    ],
    "sw": [
        "Kahawa au chai, vyote ni desturi nzuri! Furahia kikombe chako.",
        "Siwezi kunywa chochote mwenyewe, lakini ninathamini desturi nzuri ya kinywaji!",
        "Hakuna kama mmeo wa kwanza asubuhi, nadhani.",
    ],
    "fr": [
        "Café ou thé, ce sont tous les deux de superbes rituels ! Profite de ta tasse.",
        "Je ne peux rien boire moi-même, mais j'apprécie un bon rituel de boisson !",
        "Rien de tel que cette première gorgée du matin, j'imagine.",
    ],
}

EXAM_RESULTS_RESPONSES = {
    "en": [
        "How did it go? I hope it was good news!",
        "Fingers crossed for good results! How are you feeling about it?",
        "Results day is nerve-wracking. I hope it went the way you wanted.",
    ],
    "sw": [
        "Ilikuwaje? Natumai zilikuwa habari njema!",
        "Nakutakia matokeo mazuri! Unajisikiaje kuhusu hilo?",
        "Siku ya matokeo ina wasiwasi. Natumai ilikwenda kama ulivyotaka.",
    ],
    "fr": [
        "Comment ça s'est passé ? J'espère que c'était une bonne nouvelle !",
        "Je croise les doigts pour de bons résultats ! Comment tu te sens à ce sujet ?",
        "Le jour des résultats est stressant. J'espère que ça s'est passé comme tu voulais.",
    ],
}

PARTY_EVENT_RESPONSES = {
    "en": [
        "Sounds fun! Hope it's a great time.",
        "Nice, events are exciting to plan and attend. Enjoy it!",
        "I hope it goes off without a hitch!",
    ],
    "sw": [
        "Inasikika ya kufurahisha! Natumai itakuwa wakati mzuri.",
        "Vizuri, matukio ni ya kusisimua kupanga na kuhudhuria. Furahia hilo!",
        "Natumai litaendelea bila tatizo!",
    ],
    "fr": [
        "Ça a l'air amusant ! J'espère que ce sera un bon moment.",
        "Cool, les événements sont excitants à planifier et à fréquenter. Profite-en !",
        "J'espère que ça se passera sans accroc !",
    ],
}

SIBLINGS_RESPONSES = {
    "en": [
        "Siblings can be such an important part of life. How's your relationship with them?",
        "That's nice - tell me more if you'd like.",
        "Family bonds like that matter a lot. I hope things are good between you.",
    ],
    "sw": [
        "Ndugu wanaweza kuwa sehemu muhimu ya maisha. Uhusiano wako nao ukoje?",
        "Hiyo ni nzuri - niambie zaidi ukipenda.",
        "Vifungo vya familia kama hivyo vina maana kubwa. Natumai mambo ni mazuri kati yenu.",
    ],
    "fr": [
        "Les frères et sœurs peuvent être une partie si importante de la vie. Comment est ta relation avec eux ?",
        "C'est gentil - dis-m'en plus si tu veux.",
        "Ces liens familiaux comptent beaucoup. J'espère que tout va bien entre vous.",
    ],
}

CAREER_CHANGE_RESPONSES = {
    "en": [
        "That's a big decision! What's drawing you toward the change?",
        "Career changes take courage. I hope it leads somewhere great for you.",
        "New chapters can be exciting, even if a little scary. Good luck!",
    ],
    "sw": [
        "Hiyo ni uamuzi mkubwa! Ni nini kinakuvuta kuelekea mabadiliko?",
        "Mabadiliko ya kazi yanahitaji ujasiri. Natumai yatakuongoza mahali pazuri.",
        "Sura mpya zinaweza kuwa za kusisimua, hata ikiwa za kutisha kidogo. Bahati njema!",
    ],
    "fr": [
        "C'est une grande décision ! Qu'est-ce qui t'attire vers ce changement ?",
        "Les changements de carrière demandent du courage. J'espère que ça te mènera quelque part de bien.",
        "Les nouveaux chapitres peuvent être excitants, même un peu effrayants. Bonne chance !",
    ],
}

VOLUNTEER_WORK_RESPONSES = {
    "en": [
        "That's wonderful - giving back makes a real difference.",
        "I admire that. What kind of volunteer work are you doing?",
        "Volunteering is such a generous use of time. Good for you!",
    ],
    "sw": [
        "Hiyo ni nzuri - kurudisha kunafanya tofauti ya kweli.",
        "Ninaipenda hiyo. Unafanya kazi gani ya kujitolea?",
        "Kujitolea ni matumizi mazuri ya muda. Vizuri kwako!",
    ],
    "fr": [
        "C'est merveilleux - redonner fait une vraie différence.",
        "J'admire ça. Quel genre de bénévolat fais-tu ?",
        "Le bénévolat, c'est une utilisation si généreuse du temps. Bravo à toi !",
    ],
}

SPIRITUALITY_RESPONSES = {
    "en": [
        "That sounds meaningful to you. I'm happy to listen if you'd like to share more.",
        "Faith and spirituality mean different things to everyone - thanks for sharing yours.",
        "That's personal and important. I respect that, whatever it looks like for you.",
    ],
    "sw": [
        "Hiyo inasikika kuwa na maana kwako. Nafurahi kusikiliza ukitaka kushiriki zaidi.",
        "Imani na hali ya kiroho zina maana tofauti kwa kila mtu - asante kwa kushiriki yako.",
        "Hiyo ni ya kibinafsi na muhimu. Naheshimu hilo, vyovyote inavyokuwa kwako.",
    ],
    "fr": [
        "Ça semble important pour toi. Je suis content d'écouter si tu veux partager plus.",
        "La foi et la spiritualité signifient des choses différentes pour chacun - merci de partager la tienne.",
        "C'est personnel et important. Je respecte ça, quelle que soit la forme que ça prend pour toi.",
    ],
}

POLITICS_DEFLECT_RESPONSES = {
    "en": [
        "I try to stay neutral on political topics so I don't influence anyone's views - but I'm happy to lay out different perspectives on an issue if that helps.",
        "That's really a personal decision based on your own values - I'd rather not steer you one way or another.",
        "I'll leave political opinions and voting choices to you - but I can summarize different viewpoints if useful.",
    ],
    "sw": [
        "Najaribu kuwa wa kati kuhusu mada za kisiasa ili nisiwe na ushawishi kwa mtazamo wa mtu yeyote - lakini nafurahi kuelezea mitazamo tofauti kuhusu suala ikiwa hiyo itasaidia.",
        "Hiyo ni uamuzi wa kibinafsi kulingana na maadili yako - ningependelea kutokuelekeza upande mmoja au mwingine.",
        "Nitakuachia mawazo ya kisiasa na chaguo za kupiga kura - lakini naweza kufupisha mitazamo tofauti ikiwa itafaa.",
    ],
    "fr": [
        "J'essaie de rester neutre sur les sujets politiques pour ne pas influencer les opinions de qui que ce soit - mais je peux présenter différentes perspectives sur une question si ça aide.",
        "C'est vraiment une décision personnelle basée sur tes propres valeurs - je préfère ne pas t'orienter dans un sens ou l'autre.",
        "Je te laisse les opinions politiques et les choix de vote - mais je peux résumer différents points de vue si utile.",
    ],
}

SILENCE_FILLER_RESPONSES = {
    "en": [
        "That's okay, you don't need to say anything in particular. I'm here whenever you're ready.",
        "No worries - take your time.",
        "That's fine too - we can just sit with the quiet for a bit if you'd like.",
    ],
    "sw": [
        "Ni sawa, si lazima useme chochote hasa. Niko hapa wakati wowote utakapokuwa tayari.",
        "Hakuna shida - jichukulie muda wako.",
        "Hiyo ni sawa pia - tunaweza kukaa kimya kidogo ukipenda.",
    ],
    "fr": [
        "C'est normal, tu n'as pas besoin de dire quelque chose en particulier. Je suis là quand tu es prêt.",
        "Pas de souci - prends ton temps.",
        "C'est bien aussi - on peut juste rester dans le calme un moment si tu veux.",
    ],
}

DIRECTIONS_RECOMMENDATION_RESPONSES = {
    "en": [
        "I don't have live location or browsing access, but tell me a bit more about what you're looking for and I'll do my best!",
        "I can't look things up live, but I'm happy to brainstorm ideas with you.",
        "Tell me more about what you need a recommendation for, and let's think it through together.",
    ],
    "sw": [
        "Sina ufikiaji wa moja kwa moja wa mahali au kuvinjari, lakini niambie zaidi kuhusu unachotafuta na nitafanya bidii!",
        "Siwezi kuangalia mambo moja kwa moja, lakini nafurahi kufikiria mawazo nawe.",
        "Niambie zaidi kuhusu unachohitaji mapendekezo, na tufikirie kupitia hilo pamoja.",
    ],
    "fr": [
        "Je n'ai pas accès à la localisation en direct ou à la navigation, mais dis-moi un peu plus ce que tu cherches et je ferai de mon mieux !",
        "Je ne peux pas chercher des choses en direct, mais je suis content de réfléchir avec toi.",
        "Dis-moi en plus sur ce pour quoi tu as besoin d'une recommandation, et réfléchissons-y ensemble.",
    ],
}

NAME_RECOGNITION_RESPONSES = {
    "en": [
        "Of course! I keep track of facts you've told me for the whole session, and save them to disk too.",
        "I do my best to remember what you've told me - it's all saved locally.",
        "Yes - once you tell me something, I store it so I can recall it later.",
    ],
    "sw": [
        "Bila shaka! Ninafuatilia ukweli ulionipatia kwa kipindi chote, na kuyahifadhi pia kwenye diski.",
        "Ninafanya bidii kukumbuka ulichoniambia - yote yamehifadhiwa hapa karibu.",
        "Ndiyo - ukiniambia kitu, ninakihifadhi ili niweze kukikumbuka baadaye.",
    ],
    "fr": [
        "Bien sûr ! Je garde une trace des faits que tu m'as dits pendant toute la session, et je les sauvegarde aussi.",
        "Je fais de mon mieux pour me souvenir de ce que tu m'as dit - tout est sauvegardé localement.",
        "Oui - une fois que tu me dis quelque chose, je le stocke pour pouvoir m'en souvenir plus tard.",
    ],
}

GENERAL_CURIOSITY_RESPONSES = {
    "en": [
        "Curiosity is great! What's got your interest?",
        "I love a curious mind. Tell me more about what you're wondering.",
        "Good question to be curious about - what made you think of it?",
    ],
    "sw": [
        "Hamu ya kujua ni nzuri! Ni nini kinakuvutia?",
        "Ninapenda akili yenye hamu ya kujua. Niambie zaidi kuhusu unalojiuliza.",
        "Swali zuri la kuwa na hamu kuhusu - ni nini kilikufanya ufikirie hilo?",
    ],
    "fr": [
        "La curiosité, c'est génial ! Qu'est-ce qui t'intéresse ?",
        "J'aime un esprit curieux. Dis-m'en plus sur ce que tu te demandes.",
        "Bonne question à se poser - qu'est-ce qui t'a fait y penser ?",
    ],
}

# --- Sixth wave of response banks -------------------------------------------

LAUGHTER_RESPONSES = {
    "en": [
        "Haha, I love that! What's so funny?",
        "Laughter is the best - tell me what's cracking you up!",
        "That's great to hear! Share the joke?",
    ],
    "sw": [
        "Haha, ninapenda hilo! Ni nini cha kuchekesha?",
        "Kicheko ni bora zaidi - niambie kinachokuchekesha!",
        "Hiyo ni nzuri kusikia! Shiriki utani huo?",
    ],
    "fr": [
        "Haha, j'adore ça ! Qu'est-ce qui est si drôle ?",
        "Le rire, c'est le meilleur - dis-moi ce qui te fait rire !",
        "C'est génial à entendre ! Partage la blague ?",
    ],
}

CRYING_RESPONSES = {
    "en": [
        "It's okay to cry - let it out if you need to. I'm here.",
        "I'm sorry you're hurting. Take all the time you need.",
        "Tears are okay. Do you want to talk about what's going on?",
    ],
    "sw": [
        "Ni sawa kulia - itoe ukihitaji. Niko hapa.",
        "Pole kwa maumivu. Jichukulie muda wowote unaohitaji.",
        "Machozi ni sawa. Unataka kuongea kuhusu kinachoendelea?",
    ],
    "fr": [
        "C'est normal de pleurer - laisse sortir si besoin. Je suis là.",
        "Je suis désolé que tu souffres. Prends tout le temps qu'il te faut.",
        "Les larmes, c'est normal. Tu veux parler de ce qui se passe ?",
    ],
}

MILD_FRUSTRATION_RESPONSES = {
    "en": [
        "Yeah, that sounds annoying. What happened?",
        "Ugh, I feel that. Want to vent about it?",
        "That kind of thing is the worst. Tell me about it.",
    ],
    "sw": [
        "Ndiyo, hiyo inasikika ya kusumbua. Kilichotokea ni nini?",
        "Aisee, naelewa hilo. Unataka kuongea kuhusu hilo?",
        "Jambo kama hilo ni mbaya zaidi. Niambie kuhusu hilo.",
    ],
    "fr": [
        "Oui, ça semble énervant. Que s'est-il passé ?",
        "Ugh, je comprends. Tu veux en parler ?",
        "Ce genre de chose, c'est le pire. Raconte-moi.",
    ],
}

BOT_FAVORITE_THINGS_RESPONSES = {
    "en": [
        "I don't really have personal preferences - I'm just a set of rules! But I do enjoy telling jokes and stories if that counts.",
        "As a rule-based bot, I don't have favorites the way people do, but writing poems is fun to 'do' in my rigid way!",
        "No real preferences here - just code. But I always enjoy a good riddle exchange!",
    ],
    "sw": [
        "Sina mapendeleo ya kibinafsi kweli - mimi ni seti ya kanuni tu! Lakini ninafurahia kusimulia utani na hadithi ikiwa hiyo inahesabika.",
        "Kama roboti ya kanuni, sina vipendwa kama watu, lakini kuandika mashairi ni kufurahisha 'kufanya' kwa namna yangu ngumu!",
        "Hakuna mapendeleo ya kweli hapa - msimbo tu. Lakini ninafurahia daima mazungumzo mazuri ya vitendawili!",
    ],
    "fr": [
        "Je n'ai pas vraiment de préférences personnelles - je ne suis qu'un ensemble de règles ! Mais j'aime raconter des blagues et des histoires si ça compte.",
        "En tant que bot basé sur des règles, je n'ai pas de préférés comme les gens, mais écrire des poèmes est amusant à 'faire' à ma façon rigide !",
        "Pas de vraies préférences ici - juste du code. Mais j'aime toujours un bon échange de devinettes !",
    ],
}

BIRDS_FISH_RESPONSES = {
    "en": [
        "That sounds peaceful! Birds and fish make such calming companions.",
        "Nice! What kind do you have?",
        "I love hearing about aquariums and birdcages - they're so soothing to think about.",
    ],
    "sw": [
        "Hiyo inasikika ya amani! Ndege na samaki ni marafiki wa kutuliza.",
        "Vizuri! Una aina gani?",
        "Ninapenda kusikia kuhusu mabwawa ya samaki na vizimba vya ndege - vinatuliza kufikiria.",
    ],
    "fr": [
        "Ça a l'air paisible ! Les oiseaux et les poissons sont des compagnons si apaisants.",
        "Cool ! Quelle espèce as-tu ?",
        "J'aime entendre parler des aquariums et des cages à oiseaux - c'est si apaisant d'y penser.",
    ],
}

COMMUTE_TRANSPORT_RESPONSES = {
    "en": [
        "Hope the commute treats you well! How long does it take?",
        "Getting around is its own daily adventure. Stay safe out there!",
        "I hope it's a smooth ride today.",
    ],
    "sw": [
        "Natumai safari itakutendea vizuri! Inachukua muda gani?",
        "Kusafiri ni adventure yake ya kila siku. Jihadhari huko nje!",
        "Natumai itakuwa safari nzuri leo.",
    ],
    "fr": [
        "J'espère que le trajet se passera bien ! Combien de temps ça prend ?",
        "Se déplacer est sa propre aventure quotidienne. Reste prudent là-bas !",
        "J'espère que ce sera un trajet sans accroc aujourd'hui.",
    ],
}

ALLERGIES_RESPONSES = {
    "en": [
        "Allergies are no fun. I hope you're feeling okay.",
        "That sounds uncomfortable - take care of yourself.",
        "Allergy season can be rough. Hope it eases up soon.",
    ],
    "sw": [
        "Mzio si jambo zuri. Natumai unajisikia vizuri.",
        "Hiyo inasikika ya kusumbua - jitunze.",
        "Msimu wa mzio unaweza kuwa mgumu. Natumai utapungua hivi karibuni.",
    ],
    "fr": [
        "Les allergies, ce n'est pas drôle. J'espère que tu te sens bien.",
        "Ça semble inconfortable - prends soin de toi.",
        "La saison des allergies peut être dure. J'espère que ça s'arrangera vite.",
    ],
}

DIET_NUTRITION_RESPONSES = {
    "en": [
        "That's great - small consistent changes really add up over time.",
        "Good for you for being mindful of it. How's it going so far?",
        "Eating well makes such a difference. Keep it up!",
    ],
    "sw": [
        "Hiyo ni nzuri - mabadiliko madogo ya kudumu yanaongezeka kwa muda.",
        "Vizuri kwako kuwa makini na hilo. Inaendaje mpaka sasa?",
        "Kula vizuri kunafanya tofauti kubwa. Endelea hivyo!",
    ],
    "fr": [
        "C'est super - les petits changements constants s'accumulent vraiment avec le temps.",
        "Bravo d'y être attentif. Comment ça se passe jusqu'à présent ?",
        "Bien manger fait une telle différence. Continue comme ça !",
    ],
}

SLEEP_SCHEDULE_RESPONSES = {
    "en": [
        "Sleep schedules can be tricky to manage. Whatever works for your body is what matters most.",
        "Night owl or early bird, as long as you're getting enough rest!",
        "I hope your schedule leaves you feeling rested.",
    ],
    "sw": [
        "Ratiba za kulala zinaweza kuwa ngumu kusimamia. Chochote kinachofanya kazi kwa mwili wako ndicho muhimu zaidi.",
        "Bundi wa usiku au ndege wa asubuhi, mradi unapata pumziko la kutosha!",
        "Natumai ratiba yako inakuacha ukijisikia umepumzika.",
    ],
    "fr": [
        "Les horaires de sommeil peuvent être difficiles à gérer. Ce qui compte le plus, c'est ce qui fonctionne pour ton corps.",
        "Couche-tard ou lève-tôt, tant que tu te reposes assez !",
        "J'espère que ton horaire te laisse reposé.",
    ],
}

PHOTOGRAPHY_ART_RESPONSES = {
    "en": [
        "I love that! Art and photography capture moments so beautifully. What's your style?",
        "Creative hobbies like that are wonderful. What inspires you?",
        "That sounds lovely - I wish I could see what you create!",
    ],
    "sw": [
        "Ninapenda hilo! Sanaa na upigaji picha vinanasa wakati kwa uzuri. Mtindo wako ni gani?",
        "Hobby za ubunifu kama hizo ni nzuri. Ni nini kinakuvutia?",
        "Hiyo inasikika nzuri - ningependa kuona unachounda!",
    ],
    "fr": [
        "J'adore ça ! L'art et la photographie capturent les moments si magnifiquement. Quel est ton style ?",
        "Les loisirs créatifs comme ça sont merveilleux. Qu'est-ce qui t'inspire ?",
        "Ça a l'air charmant - j'aimerais pouvoir voir ce que tu crées !",
    ],
}

GRAMMAR_QUESTION_RESPONSES = {
    "en": [
        "I'm a fairly simple rule-based bot, so I can't reliably judge grammar, but I'm happy to discuss it if you tell me the sentence!",
        "Grammar questions are tricky for me to verify precisely, but go ahead and share it - I'll do my best.",
    ],
    "sw": [
        "Mimi ni roboti rahisi ya kanuni, hivyo siwezi kuhukumu sarufi kwa uhakika, lakini nafurahi kujadili ikiwa utaniambia sentensi!",
        "Maswali ya sarufi ni magumu kwangu kuthibitisha kwa usahihi, lakini endelea ushiriki - nitafanya bidii.",
    ],
    "fr": [
        "Je suis un bot assez simple basé sur des règles, donc je ne peux pas juger la grammaire de façon fiable, mais je suis content d'en discuter si tu me dis la phrase !",
        "Les questions de grammaire sont difficiles à vérifier précisément pour moi, mais vas-y, partage-la - je ferai de mon mieux.",
    ],
}

NAMING_THINGS_RESPONSES = {
    "en": [
        "That's such a fun decision to make! What style or meaning are you drawn to?",
        "Naming something is special. Do you have any names in mind already?",
        "I'd love to help brainstorm, even without a personal favorite to suggest!",
    ],
    "sw": [
        "Hiyo ni uamuzi wa kufurahisha kufanya! Ni mtindo au maana gani inakuvutia?",
        "Kutaja jina ni jambo la pekee. Una majina yoyote akilini tayari?",
        "Ningependa kusaidia kufikiria mawazo, hata bila kipendwa cha kibinafsi kupendekeza!",
    ],
    "fr": [
        "C'est une décision si amusante à prendre ! Quel style ou sens t'attire ?",
        "Nommer quelque chose, c'est spécial. As-tu déjà des noms en tête ?",
        "J'aimerais aider à réfléchir, même sans préféré personnel à suggérer !",
    ],
}

WEATHER_EXTREME_RESPONSES = {
    "en": [
        "Please stay safe! Severe weather is no joke - follow local advisories.",
        "I hope you're somewhere secure. Take all the precautions you can.",
        "That sounds serious - please prioritize your safety above everything else.",
    ],
    "sw": [
        "Tafadhali kuwa salama! Hali mbaya ya hewa si jambo la kuchezea - fuata maelekezo ya eneo lako.",
        "Natumai uko mahali salama. Chukua tahadhari zote unazoweza.",
        "Hiyo inasikika kuwa zito - tafadhali weka usalama wako kwanza kabla ya kila kitu kingine.",
    ],
    "fr": [
        "S'il te plaît, reste en sécurité ! Les intempéries sévères, ce n'est pas une blague - suis les avis locaux.",
        "J'espère que tu es dans un endroit sûr. Prends toutes les précautions possibles.",
        "Ça semble sérieux - s'il te plaît, priorise ta sécurité avant tout.",
    ],
}

HOME_HOUSE_RESPONSES = {
    "en": [
        "Home projects can be exciting! How's it coming along?",
        "I hope the new space feels just right for you.",
        "Redecorating is fun. What look are you going for?",
    ],
    "sw": [
        "Miradi ya nyumbani inaweza kuwa ya kusisimua! Inaendaje?",
        "Natumai nafasi mpya inajisikia sawa kwako.",
        "Kupamba upya ni kufurahisha. Unataka mtindo gani?",
    ],
    "fr": [
        "Les projets à la maison peuvent être excitants ! Comment ça avance ?",
        "J'espère que le nouvel espace te convient parfaitement.",
        "Redécorer, c'est amusant. Quel look recherches-tu ?",
    ],
}

NEIGHBORS_RESPONSES = {
    "en": [
        "Neighbors can really shape how a place feels. How's that going?",
        "I hope things are peaceful on that front.",
        "That's a tricky situation sometimes. Want to talk it through?",
    ],
    "sw": [
        "Majirani wanaweza kuathiri jinsi mahali inavyojisikia. Hilo linaendaje?",
        "Natumai mambo ni ya amani upande huo.",
        "Hiyo ni hali ngumu mara kwa mara. Unataka kuongea kupitia hilo?",
    ],
    "fr": [
        "Les voisins peuvent vraiment influencer l'ambiance d'un endroit. Comment ça se passe ?",
        "J'espère que les choses sont paisibles de ce côté.",
        "C'est une situation délicate parfois. Tu veux en discuter ?",
    ],
}

PET_LOSS_RESPONSES = {
    "en": [
        "I'm so sorry for your loss. Pets are family, and that kind of grief is real.",
        "That's heartbreaking. Take all the time you need to grieve.",
        "I'm really sorry. They were lucky to have you, and you were lucky to have them.",
    ],
    "sw": [
        "Pole sana kwa kupoteza. Wanyama wa kufugwa ni familia, na huzuni hiyo ni ya kweli.",
        "Hiyo ni ya kuhuzunisha. Jichukulie muda wowote unaohitaji kuomboleza.",
        "Pole sana. Walikuwa na bahati kuwa na wewe, na ulikuwa na bahati kuwa nao.",
    ],
    "fr": [
        "Je suis vraiment désolé pour ta perte. Les animaux sont de la famille, et ce chagrin est réel.",
        "C'est déchirant. Prends tout le temps dont tu as besoin pour faire ton deuil.",
        "Je suis vraiment désolé. Ils ont eu de la chance de t'avoir, et tu as eu de la chance de les avoir.",
    ],
}

ACHIEVEMENT_MILESTONE_RESPONSES = {
    "en": [
        "That's huge! Congratulations on getting there.",
        "What an accomplishment - you should be really proud.",
        "Milestones like that deserve to be celebrated. Well done!",
    ],
    "sw": [
        "Hiyo ni kubwa! Hongera kwa kufika huko.",
        "Mafanikio gani - unapaswa kuwa na fahari kweli.",
        "Hatua kama hiyo zinastahili kusherehekewa. Vizuri sana!",
    ],
    "fr": [
        "C'est énorme ! Félicitations d'être arrivé là.",
        "Quel accomplissement - tu devrais être vraiment fier.",
        "Des étapes comme ça méritent d'être célébrées. Bravo !",
    ],
}

WAITING_PATIENCE_RESPONSES = {
    "en": [
        "Waiting is one of the hardest things. Hang in there.",
        "I hope it's worth the wait when it finally comes.",
        "Patience is tough, but you're handling it. Almost there!",
    ],
    "sw": [
        "Kusubiri ni mojawapo ya mambo magumu zaidi. Jichukulie hatua moja moja.",
        "Natumai itastahili kusubiri itakapokuja hatimaye.",
        "Uvumilivu ni mgumu, lakini unashughulikia vizuri. Karibu kufika!",
    ],
    "fr": [
        "Attendre est l'une des choses les plus difficiles. Tiens bon.",
        "J'espère que ça vaudra l'attente quand ça arrivera enfin.",
        "La patience est dure, mais tu gères bien. Tu y es presque !",
    ],
}

POSITIVE_SURPRISE_RESPONSES = {
    "en": [
        "I love a good surprise! What happened?",
        "That's the best kind of surprise. Tell me more!",
        "Those unexpected good moments are the best. Enjoy it!",
    ],
    "sw": [
        "Ninapenda mshangao mzuri! Nini kilitokea?",
        "Hiyo ni aina bora ya mshangao. Niambie zaidi!",
        "Wakati huo wa ghafla mzuri ni bora zaidi. Furahia hilo!",
    ],
    "fr": [
        "J'adore une bonne surprise ! Qu'est-ce qui s'est passé ?",
        "C'est le meilleur genre de surprise. Dis-m'en plus !",
        "Ces bons moments inattendus sont les meilleurs. Profite-en !",
    ],
}

COMPLIMENT_BACK_REQUEST_RESPONSES = {
    "en": [
        "Happy to! You're doing great just by showing up and engaging with the world today.",
        "Here's one: you ask thoughtful questions - that's a great quality.",
        "You seem genuinely curious and kind, and that's worth a lot.",
    ],
    "sw": [
        "Nafurahi! Unafanya vizuri tu kwa kujitokeza na kushiriki na dunia leo.",
        "Hapa kuna kimoja: unauliza maswali ya kufikirika - hiyo ni sifa nzuri.",
        "Unaonekana na hamu ya kweli ya kujua na wewe ni mpole, na hiyo ina thamani kubwa.",
    ],
    "fr": [
        "Avec plaisir ! Tu fais déjà bien en te présentant et en t'engageant avec le monde aujourd'hui.",
        "En voici un : tu poses des questions réfléchies - c'est une belle qualité.",
        "Tu sembles vraiment curieux et gentil, et ça compte beaucoup.",
    ],
}

# --- Seventh and final wave of response banks ------------------------------

DEADLINE_RESPONSES = {
    "en": [
        "Deadlines can be stressful. Break it into small steps and you've got this.",
        "I hope you've got enough time to finish it well. You can do this!",
        "Try to prioritize the most important parts first - good luck!",
    ],
    "sw": [
        "Muda wa mwisho unaweza kuwa na msongo. Gawanya kwa hatua ndogo na unaweza kufanya hili.",
        "Natumai una muda wa kutosha kukamilisha vizuri. Unaweza kufanya hili!",
        "Jaribu kupanga vipaumbele vya sehemu muhimu zaidi kwanza - bahati njema!",
    ],
    "fr": [
        "Les échéances peuvent être stressantes. Divise-la en petites étapes et tu vas y arriver.",
        "J'espère que tu as assez de temps pour bien la terminer. Tu peux le faire !",
        "Essaie de prioriser les parties les plus importantes d'abord - bonne chance !",
    ],
}

PREGNANCY_BABY_RESPONSES = {
    "en": [
        "Congratulations! That's wonderful news.",
        "How exciting! Wishing you and your family all the best.",
        "That's beautiful news - congratulations on the new addition!",
    ],
    "sw": [
        "Hongera! Hiyo ni habari nzuri sana.",
        "Hiyo ni ya kusisimua! Nakutakia wewe na familia yako mema yote.",
        "Hiyo ni habari nzuri - hongera kwa nyongeza mpya!",
    ],
    "fr": [
        "Félicitations ! C'est une merveilleuse nouvelle.",
        "Quelle excitation ! Je vous souhaite, à toi et ta famille, le meilleur.",
        "C'est une belle nouvelle - félicitations pour ce nouvel arrivant !",
    ],
}

WEDDING_ENGAGEMENT_RESPONSES = {
    "en": [
        "Congratulations! Wishing you so much happiness together.",
        "That's wonderful news! How are the wedding plans coming along?",
        "Huge congratulations! That's such an exciting chapter to begin.",
    ],
    "sw": [
        "Hongera! Nakutakia furaha nyingi pamoja.",
        "Hiyo ni habari nzuri! Mipango ya harusi inaendaje?",
        "Hongera kubwa! Hiyo ni sura ya kusisimua kuanza.",
    ],
    "fr": [
        "Félicitations ! Je vous souhaite beaucoup de bonheur ensemble.",
        "Quelle merveilleuse nouvelle ! Comment avancent les préparatifs du mariage ?",
        "Énormes félicitations ! C'est un chapitre si excitant à commencer.",
    ],
}

GRADUATION_RESPONSES = {
    "en": [
        "Congratulations! That's a huge accomplishment.",
        "Well done! All that hard work paid off.",
        "Congratulations on graduating - you should be incredibly proud!",
    ],
    "sw": [
        "Hongera! Hiyo ni mafanikio makubwa.",
        "Vizuri sana! Bidii yote ile imelipa.",
        "Hongera kwa kuhitimu - unapaswa kuwa na fahari kubwa!",
    ],
    "fr": [
        "Félicitations ! C'est un énorme accomplissement.",
        "Bravo ! Tout ce dur travail a porté ses fruits.",
        "Félicitations pour ton diplôme - tu devrais être incroyablement fier !",
    ],
}

MOVING_CITY_RESPONSES = {
    "en": [
        "Big change! I hope the new city treats you well.",
        "Moving is exciting and a little nerve-wracking. Good luck settling in!",
        "New cities bring new adventures. I hope you love it there.",
    ],
    "sw": [
        "Mabadiliko makubwa! Natumai mji mpya utakutendea vizuri.",
        "Kuhama ni kufurahisha na kunatia wasiwasi kidogo. Bahati njema kutulia!",
        "Miji mipya inaleta adventure mpya. Natumai utaipenda huko.",
    ],
    "fr": [
        "Grand changement ! J'espère que la nouvelle ville te traitera bien.",
        "Déménager, c'est excitant et un peu stressant. Bonne chance pour t'installer !",
        "Les nouvelles villes apportent de nouvelles aventures. J'espère que tu vas adorer là-bas.",
    ],
}

NEW_PET_RESPONSES = {
    "en": [
        "Congratulations on the new family member! What's their name?",
        "That's so exciting! Pets bring so much joy.",
        "Aww, congratulations! I hope you two are very happy together.",
    ],
    "sw": [
        "Hongera kwa mwanafamilia mpya! Jina lao ni nini?",
        "Hiyo ni ya kusisimua sana! Wanyama wanaleta furaha nyingi.",
        "Aa, hongera! Natumai nyote wawili mtakuwa na furaha pamoja.",
    ],
    "fr": [
        "Félicitations pour le nouveau membre de la famille ! Quel est son nom ?",
        "C'est tellement excitant ! Les animaux apportent tellement de joie.",
        "Aww, félicitations ! J'espère que vous serez très heureux ensemble.",
    ],
}

FIRST_DAY_RESPONSES = {
    "en": [
        "Good luck! First days are nerve-wracking but exciting too.",
        "You've got this! Just be yourself and take it one moment at a time.",
        "Nervous energy is normal - it usually means it matters to you. Go get it!",
    ],
    "sw": [
        "Bahati njema! Siku za kwanza zinatia wasiwasi lakini pia zinasisimua.",
        "Unaweza kufanya hili! Kuwa wewe mwenyewe na jichukulie hatua moja moja.",
        "Nguvu ya wasiwasi ni ya kawaida - kawaida inamaanisha jambo lina maana kwako. Endelea!",
    ],
    "fr": [
        "Bonne chance ! Les premiers jours sont stressants mais excitants aussi.",
        "Tu peux le faire ! Sois toi-même et prends-le un moment à la fois.",
        "L'énergie nerveuse est normale - ça veut généralement dire que ça compte pour toi. Vas-y !",
    ],
}

REUNION_RESPONSES = {
    "en": [
        "That sounds wonderful! Reconnecting with old friends is so special.",
        "I hope you have a great time catching up!",
        "Those reunions are the best - enjoy reliving old memories.",
    ],
    "sw": [
        "Hiyo inasikika nzuri! Kuungana tena na marafiki wa zamani ni jambo la pekee.",
        "Natumai utakuwa na wakati mzuri wa kuongea!",
        "Mikutano kama hiyo ni bora zaidi - furahia kukumbuka kumbukumbu za zamani.",
    ],
    "fr": [
        "Ça a l'air merveilleux ! Renouer avec de vieux amis, c'est si spécial.",
        "J'espère que tu passeras un bon moment à rattraper le temps perdu !",
        "Ces retrouvailles sont les meilleures - profite pour revivre de vieux souvenirs.",
    ],
}

FLUENCY_GOALS_RESPONSES = {
    "en": [
        "That's a great goal! Consistent practice is the key - keep going.",
        "Fluency takes time but it's so worth it. Keep practicing with me anytime!",
        "I admire that goal. Little by little, you'll get there.",
    ],
    "sw": [
        "Hilo ni lengo zuri! Mazoezi ya kudumu ni ufunguo - endelea.",
        "Ufasaha unahitaji muda lakini unastahili kabisa. Endelea kujizoeza nami wakati wowote!",
        "Ninaipenda lengo hilo. Kidogo kidogo, utafika huko.",
    ],
    "fr": [
        "C'est un excellent objectif ! La pratique régulière est la clé - continue.",
        "La fluidité prend du temps mais ça vaut vraiment le coup. Continue à pratiquer avec moi quand tu veux !",
        "J'admire cet objectif. Petit à petit, tu y arriveras.",
    ],
}

CULTURAL_TRADITIONS_RESPONSES = {
    "en": [
        "I love hearing about traditions - they carry so much meaning. Tell me more!",
        "Culture and tradition are so rich. What does that celebration involve?",
        "That sounds meaningful. Thanks for sharing a piece of your culture.",
    ],
    "sw": [
        "Ninapenda kusikia kuhusu mila - zina maana kubwa. Niambie zaidi!",
        "Utamaduni na mila ni tajiri sana. Sherehe hiyo inahusisha nini?",
        "Hiyo inasikika kuwa na maana. Asante kwa kushiriki kipande cha utamaduni wako.",
    ],
    "fr": [
        "J'aime entendre parler des traditions - elles portent tellement de sens. Dis-m'en plus !",
        "La culture et la tradition sont si riches. Qu'est-ce que cette célébration implique ?",
        "Ça semble plein de sens. Merci de partager un morceau de ta culture.",
    ],
}

SUSTAINABILITY_RESPONSES = {
    "en": [
        "That's great - small sustainable choices really add up over time.",
        "Good for you! Every bit of effort toward sustainability helps.",
        "I admire that mindset. What changes have you been making?",
    ],
    "sw": [
        "Hiyo ni nzuri - chaguo ndogo za uendelevu zinaongezeka kwa muda.",
        "Vizuri kwako! Kila jitihada kuelekea uendelevu inasaidia.",
        "Ninaipenda mtazamo huo. Umekuwa ukifanya mabadiliko gani?",
    ],
    "fr": [
        "C'est super - les petits choix durables s'accumulent vraiment avec le temps.",
        "Bravo à toi ! Chaque effort vers la durabilité aide.",
        "J'admire cette mentalité. Quels changements as-tu apportés ?",
    ],
}

FUN_FACT_RESPONSES = {
    "en": [
        "Here's one: honey never spoils - archaeologists have found edible honey in ancient Egyptian tombs!",
        "Did you know octopuses have three hearts? Two pump blood to the gills, one to the rest of the body.",
        "Fun fact: a group of flamingos is called a 'flamboyance'.",
        "Here's one: bananas are berries, but strawberries technically aren't!",
    ],
    "sw": [
        "Hapa kuna jambo: asali haiharibiki kamwe - wanaakiolojia wamepata asali inayoliwa kwenye makaburi ya kale ya Misri!",
        "Je ulijua pweza wana mioyo mitatu? Miwili inasukuma damu kwenye matamvua, mmoja kwa mwili wote.",
        "Jambo la kufurahisha: kundi la flamingo linaitwa 'flamboyance'.",
        "Hapa kuna jambo: ndizi ni matunda ya beri, lakini jordgubbar kitaalamu sio!",
    ],
    "fr": [
        "En voici un : le miel ne se gâte jamais - les archéologues ont trouvé du miel comestible dans des tombes égyptiennes antiques !",
        "Savais-tu que les pieuvres ont trois cœurs ? Deux pompent le sang vers les branchies, un vers le reste du corps.",
        "Fait amusant : un groupe de flamants s'appelle une 'flamboyance'.",
        "En voici un : les bananes sont des baies, mais les fraises techniquement n'en sont pas !",
    ],
}

# --- Eighth wave of response banks ------------------------------------------

GIFT_THANKS_RESPONSES = {
    "en": [
        "That's so nice! What was it?",
        "Gifts like that are special. I hope it made your day!",
        "How thoughtful! Sounds like someone cares about you a lot.",
    ],
    "sw": [
        "Hiyo ni nzuri sana! Ilikuwa nini?",
        "Zawadi kama hizo ni za pekee. Natumai imekufurahisha siku yako!",
        "Jinsi ya kufikiria! Inasikika kama mtu anakujali sana.",
    ],
    "fr": [
        "C'est tellement gentil ! C'était quoi ?",
        "Des cadeaux comme ça sont spéciaux. J'espère que ça a fait ta journée !",
        "Quelle attention ! On dirait que quelqu'un t'apprécie beaucoup.",
    ],
}

RUNNING_LATE_RESPONSES = {
    "en": [
        "Hope you make it on time, or close to it! Safe travels.",
        "Running late happens to everyone. Try not to stress too much.",
        "I hope the rest of your day goes smoother after this!",
    ],
    "sw": [
        "Natumai utafika kwa wakati, au karibu na hilo! Safari salama.",
        "Kuchelewa hutokea kwa kila mtu. Jaribu kutojisumbua sana.",
        "Natumai siku yako iliyobaki itaendelea vizuri zaidi baada ya hili!",
    ],
    "fr": [
        "J'espère que tu arriveras à l'heure, ou presque ! Bon trajet.",
        "Être en retard arrive à tout le monde. Essaie de ne pas trop stresser.",
        "J'espère que le reste de ta journée se passera mieux après ça !",
    ],
}

TIME_MANAGEMENT_RESPONSES = {
    "en": [
        "Time management is tough! Breaking things into small chunks can really help.",
        "That feeling of never enough time is so common. Be kind to yourself about it.",
        "Try prioritizing just the top one or two things - the rest can wait.",
    ],
    "sw": [
        "Usimamizi wa muda ni mgumu! Kugawanya mambo kwa vipande vidogo kunaweza kusaidia kweli.",
        "Hisia hiyo ya kutokuwa na muda wa kutosha ni ya kawaida. Kuwa mpole kwako mwenyewe kuhusu hilo.",
        "Jaribu kupanga vipaumbele kwa mambo moja au mawili ya juu zaidi - mengine yanaweza kusubiri.",
    ],
    "fr": [
        "La gestion du temps, c'est dur ! Diviser les choses en petits morceaux peut vraiment aider.",
        "Ce sentiment de jamais assez de temps est si commun. Sois gentil avec toi-même à ce sujet.",
        "Essaie de prioriser juste les une ou deux choses les plus importantes - le reste peut attendre.",
    ],
}

SPORTS_VICTORY_RESPONSES = {
    "en": [
        "Congratulations! That victory must feel amazing.",
        "Yes! That's fantastic news for your team.",
        "Way to go! Enjoy the win.",
    ],
    "sw": [
        "Hongera! Ushindi huo unapaswa kujisikia mzuri.",
        "Ndiyo! Hiyo ni habari nzuri kwa timu yako.",
        "Vizuri sana! Furahia ushindi.",
    ],
    "fr": [
        "Félicitations ! Cette victoire doit faire un bien fou.",
        "Oui ! C'est une excellente nouvelle pour ton équipe.",
        "Bravo ! Profite de la victoire.",
    ],
}

SPORTS_LOSS_RESPONSES = {
    "en": [
        "Sorry to hear that. Tough losses happen, but there's always next time.",
        "That's a hard one to swallow. Hope the next game goes better.",
        "Losses sting, but they don't define the team. Better luck next time.",
    ],
    "sw": [
        "Pole kusikia hilo. Kushindwa kwa ugumu hutokea, lakini kuna wakati mwingine daima.",
        "Hiyo ni ngumu kukubali. Natumai mchezo ujao utakuwa bora.",
        "Kushindwa kunaumiza, lakini hakuelezi timu. Bahati njema wakati mwingine.",
    ],
    "fr": [
        "Désolé d'entendre ça. Les défaites difficiles arrivent, mais il y a toujours une prochaine fois.",
        "C'est dur à digérer. J'espère que le prochain match ira mieux.",
        "Les défaites font mal, mais elles ne définissent pas l'équipe. Bonne chance la prochaine fois.",
    ],
}

UNPREDICTABLE_WEATHER_RESPONSES = {
    "en": [
        "Weather like that keeps you on your toes! Best to dress in layers.",
        "Unpredictable weather is the worst for planning anything. Hang in there.",
        "That kind of weather is wild. Stay prepared for anything!",
    ],
    "sw": [
        "Hali ya hewa kama hiyo inakufanya uwe macho! Bora kuvaa nguo za tabaka.",
        "Hali ya hewa isiyotabirika ni mbaya zaidi kwa kupanga chochote. Jichukulie hatua moja moja.",
        "Hali ya hewa ya aina hiyo ni ya ajabu. Kuwa tayari kwa chochote!",
    ],
    "fr": [
        "Ce genre de météo te tient en alerte ! Mieux vaut s'habiller en couches.",
        "La météo imprévisible, c'est le pire pour planifier quoi que ce soit. Tiens bon.",
        "Ce genre de temps est fou. Reste prêt à tout !",
    ],
}

NEW_YEAR_RESOLUTION_RESPONSES = {
    "en": [
        "That's a great resolution! What's your plan to stick with it?",
        "I love a fresh start. I hope this year brings you closer to that goal.",
        "Resolutions take commitment - I believe you can stick with it!",
    ],
    "sw": [
        "Hilo ni azimio zuri! Mpango wako wa kulishikilia ni nini?",
        "Ninapenda mwanzo mpya. Natumai mwaka huu utakukaribisha karibu na lengo hilo.",
        "Maazimio yanahitaji dhamira - naamini unaweza kulishikilia!",
    ],
    "fr": [
        "C'est une excellente résolution ! Quel est ton plan pour la tenir ?",
        "J'aime un nouveau départ. J'espère que cette année te rapprochera de cet objectif.",
        "Les résolutions demandent de l'engagement - je crois que tu peux la tenir !",
    ],
}

CHILDHOOD_MEMORY_RESPONSES = {
    "en": [
        "Childhood memories are so precious. What's the one that stands out most?",
        "That sounds like a special memory. Thanks for sharing it.",
        "Growing up shapes us in so many ways. I love hearing those stories.",
    ],
    "sw": [
        "Kumbukumbu za utotoni ni za thamani sana. Ni ipi inayojitokeza zaidi?",
        "Hiyo inasikika kama kumbukumbu ya pekee. Asante kwa kuishiriki.",
        "Kukua kunatuunda kwa njia nyingi. Ninapenda kusikia hadithi hizo.",
    ],
    "fr": [
        "Les souvenirs d'enfance sont si précieux. Lequel se démarque le plus ?",
        "Ça a l'air d'être un souvenir spécial. Merci de le partager.",
        "Grandir nous façonne de tant de façons. J'aime entendre ces histoires.",
    ],
}

ROLE_MODEL_RESPONSES = {
    "en": [
        "That's a great person to look up to! What qualities inspire you most?",
        "Role models can shape us in powerful ways. Tell me more about them.",
        "I love that you have someone who inspires you like that.",
    ],
    "sw": [
        "Huyo ni mtu mzuri wa kumheshimu! Ni sifa gani zinakuvutia zaidi?",
        "Vielelezo vinaweza kutuunda kwa njia kubwa. Niambie zaidi kuhusu wao.",
        "Ninapenda una mtu anayekutia moyo kama hivyo.",
    ],
    "fr": [
        "C'est une belle personne à admirer ! Quelles qualités t'inspirent le plus ?",
        "Les modèles peuvent nous façonner puissamment. Dis-m'en plus sur eux.",
        "J'adore que tu aies quelqu'un qui t'inspire comme ça.",
    ],
}

FEAR_PHOBIA_RESPONSES = {
    "en": [
        "Fears are really common, even ones that seem small from the outside. Thanks for sharing that.",
        "That sounds tough to deal with. You're not alone in feeling that way.",
        "Phobias can be really intense. I hope you're able to manage it in ways that help.",
        "Fears don't have to make logical sense to be completely real to you.",
        "That sounds genuinely distressing. Thank you for trusting me with it.",
        "Phobias can hijack your whole body, not just your thoughts - that's exhausting.",
        "You're not weak for being afraid of this, whatever 'this' is.",
        "I imagine that fear shows up at the most inconvenient times too.",
        "Whatever it is, your fear of it makes sense to your nervous system, even if it seems irrational from the outside.",
        "That kind of fear can shrink your world in ways that aren't fair to live with.",
        "I'm glad you said something instead of just managing this silently.",
        "Fears like that deserve patience, not judgment - including from yourself.",
        "It's okay if this feels bigger than you can untangle alone right now.",
        "Whatever's behind it, I believe that it's genuinely hard for you.",
        "That sounds like a lot to carry around quietly.",
        "You don't have to explain why it's scary - it just is, and that's enough.",
        "If this fear is limiting things you want to do, a therapist who specializes in phobias can offer real tools - that's not me dismissing it, just being honest about what I can't provide.",
    ],
    "sw": [
        "Hofu ni za kawaida sana, hata zile zinazoonekana ndogo kutoka nje. Asante kwa kushiriki hilo.",
        "Hiyo inasikika ngumu kushughulikia. Hauko peke yako kuhisi hivyo.",
        "Hofu kali zinaweza kuwa kali sana. Natumai unaweza kuishughulikia kwa njia zinazosaidia.",
        "Hofu hazihitaji kuwa na mantiki ili kuwa za kweli kabisa kwako.",
        "Hiyo inasikika kusumbua kweli. Asante kwa kuniaminisha nayo.",
        "Hofu kubwa zinaweza kuteka mwili wako wote, si tu mawazo yako - hilo linachosha.",
        "Si dhaifu kwa kuogopa hili, vyovyote 'hili' lilivyo.",
        "Nadhani hofu hiyo inajitokeza nyakati zisizofaa pia.",
        "Chochote ni hicho, hofu yako kuhusu hilo ina maana kwa mfumo wako wa neva, hata ikionekana isiyo na mantiki kutoka nje.",
        "Hofu ya aina hiyo inaweza kupunguza ulimwengu wako kwa njia zisizo za haki kuishi nazo.",
        "Nafurahi umesema kitu badala ya kushughulikia hili kimya kimya.",
        "Hofu kama hiyo zinastahili uvumilivu, si hukumu - ikiwa ni pamoja na kutoka kwako mwenyewe.",
        "Ni sawa kama hili linahisi kubwa zaidi ya unavyoweza kulitatua peke yako sasa.",
        "Chochote nyuma yake, ninaamini ni gumu kwa kweli kwako.",
        "Hiyo inasikika kuwa mengi kubeba kimya kimya.",
        "Hauhitaji kueleza kwa nini ni ya kutisha - ni hivyo tu, na hilo linatosha.",
        "Kama hofu hii inapunguza mambo unayotaka kufanya, mtaalamu wa saikolojia anayebobea kwenye hofu kubwa anaweza kutoa zana za kweli - hilo si kulipuuza, ni ukweli kuhusu nisichoweza kutoa.",
    ],
    "fr": [
        "Les peurs sont vraiment courantes, même celles qui semblent petites de l'extérieur. Merci de partager ça.",
        "Ça semble difficile à gérer. Tu n'es pas seul à ressentir ça.",
        "Les phobies peuvent être vraiment intenses. J'espère que tu peux la gérer d'une façon qui aide.",
        "Les peurs n'ont pas besoin d'avoir un sens logique pour être complètement réelles pour toi.",
        "Ça semble vraiment angoissant. Merci de me faire confiance avec ça.",
        "Les phobies peuvent s'emparer de tout ton corps, pas juste tes pensées - c'est épuisant.",
        "Tu n'es pas faible d'avoir peur de ça, quel que soit ce 'ça'.",
        "J'imagine que cette peur se manifeste aux moments les plus inopportuns aussi.",
        "Quoi que ce soit, ta peur a du sens pour ton système nerveux, même si ça semble irrationnel de l'extérieur.",
        "Ce genre de peur peut rétrécir ton monde d'une façon qui n'est pas juste à vivre.",
        "Je suis content que tu en aies parlé plutôt que de gérer ça en silence.",
        "Des peurs comme ça méritent de la patience, pas du jugement - y compris de ta part.",
        "C'est normal si ça semble plus gros que ce que tu peux démêler seul maintenant.",
        "Quoi qu'il y ait derrière, je crois que c'est vraiment dur pour toi.",
        "Ça semble être beaucoup à porter tranquillement.",
        "Tu n'as pas à expliquer pourquoi c'est effrayant - ça l'est, et ça suffit.",
        "Si cette peur limite des choses que tu veux faire, un thérapeute spécialisé dans les phobies peut offrir de vrais outils - ce n'est pas pour la minimiser, juste être honnête sur ce que je ne peux pas fournir.",
    ],
}

DREAM_INTERPRETATION_RESPONSES = {
    "en": [
        "I'm not able to interpret dreams in any reliable way - I'm just a rule-based bot - but dreams are fascinating to think about!",
        "Dream interpretation isn't something I can do accurately, but I'd love to hear about the dream anyway.",
        "I can't offer real interpretation, but dreams often reflect what's on our mind lately - what's been going on for you?",
    ],
    "sw": [
        "Siwezi kutafsiri ndoto kwa namna yoyote ya kuaminika - mimi ni roboti ya kanuni tu - lakini ndoto ni za kuvutia kufikiria!",
        "Tafsiri ya ndoto si jambo ninaloweza kufanya kwa usahihi, lakini ningependa kusikia kuhusu ndoto hiyo hata hivyo.",
        "Siwezi kutoa tafsiri ya kweli, lakini ndoto mara nyingi zinaonyesha kinachoendelea akilini - kuna nini kimekuwa kikiendelea kwako?",
    ],
    "fr": [
        "Je ne peux pas interpréter les rêves de manière fiable - je ne suis qu'un bot basé sur des règles - mais les rêves sont fascinants !",
        "L'interprétation des rêves n'est pas quelque chose que je peux faire précisément, mais j'aimerais entendre parler du rêve quand même.",
        "Je ne peux pas offrir une vraie interprétation, mais les rêves reflètent souvent ce qui nous préoccupe - qu'est-ce qui se passe pour toi ?",
    ],
}

SELF_IMPROVEMENT_RESPONSES = {
    "en": [
        "That's such valuable work. What area are you focusing on?",
        "Personal growth takes real courage. I'm glad you're putting in the effort.",
        "Working on yourself is one of the best investments. Keep it up!",
    ],
    "sw": [
        "Hiyo ni kazi ya thamani sana. Unajikita eneo gani?",
        "Ukuaji wa kibinafsi unahitaji ujasiri wa kweli. Nafurahi unaweka bidii.",
        "Kujifanyia kazi ni mojawapo ya uwekezaji bora zaidi. Endelea hivyo!",
    ],
    "fr": [
        "C'est un travail si précieux. Sur quel domaine te concentres-tu ?",
        "La croissance personnelle demande un vrai courage. Je suis content que tu fasses cet effort.",
        "Travailler sur soi-même est l'un des meilleurs investissements. Continue comme ça !",
    ],
}

SOCIAL_MEDIA_RESPONSES = {
    "en": [
        "Social media can be a lot. A break sounds like a great idea if you need it.",
        "Screen time creeps up on everyone. Good for you for noticing.",
        "I hope whatever you posted got a good response!",
    ],
    "sw": [
        "Mitandao ya kijamii inaweza kuwa mengi. Mapumziko yanasikika kama wazo zuri ukihitaji.",
        "Muda wa skrini unawaongezekea kila mtu. Vizuri kwako kutambua hilo.",
        "Natumai kile ulichoweka kimepata mwitikio mzuri!",
    ],
    "fr": [
        "Les réseaux sociaux peuvent être beaucoup. Une pause semble être une excellente idée si tu en as besoin.",
        "Le temps d'écran s'accumule chez tout le monde. Bravo d'y avoir fait attention.",
        "J'espère que ce que tu as posté a eu une bonne réponse !",
    ],
}

REMOTE_WORK_RESPONSES = {
    "en": [
        "Working from home has its perks and its challenges! How's it going for you?",
        "Remote work can blur the lines between work and rest. Hope you're finding a good balance.",
        "That flexibility is great, as long as you're able to switch off when needed!",
    ],
    "sw": [
        "Kufanya kazi nyumbani kuna faida na changamoto zake! Inakuendea vipi?",
        "Kazi ya mbali inaweza kuchanganya mipaka kati ya kazi na mapumziko. Natumai unapata uwiano mzuri.",
        "Unyumbufu huo ni mzuri, mradi unaweza kuzima unapohitaji!",
    ],
    "fr": [
        "Travailler à domicile a ses avantages et ses défis ! Comment ça se passe pour toi ?",
        "Le travail à distance peut brouiller les limites entre travail et repos. J'espère que tu trouves un bon équilibre.",
        "Cette flexibilité est géniale, tant que tu peux décrocher quand nécessaire !",
    ],
}

JOB_INTERVIEW_RESPONSES = {
    "en": [
        "Good luck! Prepare a few stories about your experience and you'll do great.",
        "Interviews are nerve-wracking, but you've got this. Be yourself!",
        "I hope it goes really well. Take a deep breath beforehand - you're ready.",
    ],
    "sw": [
        "Bahati njema! Jitayarishe hadithi chache kuhusu uzoefu wako nawe utafanya vizuri.",
        "Mahojiano yanatia wasiwasi, lakini unaweza kufanya hili. Kuwa wewe mwenyewe!",
        "Natumai itakwenda vizuri sana. Pumua kwa kina kabla - umejiandaa.",
    ],
    "fr": [
        "Bonne chance ! Prépare quelques histoires sur ton expérience et tu vas réussir.",
        "Les entretiens sont stressants, mais tu peux le faire. Sois toi-même !",
        "J'espère que ça se passera très bien. Respire profondément avant - tu es prêt.",
    ],
}

RECIPE_DISH_RESPONSES = {
    "en": [
        "That sounds delicious! I'd love to hear more about it, even though I can't taste it.",
        "Homemade meals are the best. What's in it?",
        "Trying new recipes is fun - I hope it turns out great!",
    ],
    "sw": [
        "Hiyo inasikika tamu! Ningependa kusikia zaidi kuhusu hilo, hata ingawa siwezi kuionja.",
        "Milo ya nyumbani ni bora zaidi. Kuna nini ndani yake?",
        "Kujaribu mlo mpya ni kufurahisha - natumai itakuwa nzuri!",
    ],
    "fr": [
        "Ça a l'air délicieux ! J'aimerais en savoir plus, même si je ne peux pas le goûter.",
        "Les repas faits maison sont les meilleurs. Qu'est-ce qu'il y a dedans ?",
        "Essayer de nouvelles recettes, c'est amusant - j'espère que ça sera réussi !",
    ],
}

# --- Ninth wave of response banks -------------------------------------------

INSOMNIA_RESPONSES = {
    "en": [
        "That's so frustrating. Try not to stress about not sleeping - it sometimes makes it worse.",
        "Lying awake is the worst. Maybe some quiet music or a calming routine could help.",
        "I hope you're able to drift off soon. Be gentle with yourself either way.",
    ],
    "sw": [
        "Hiyo inachosha sana. Jaribu kutojisumbua kuhusu kutolala - mara nyingine kunafanya iwe mbaya zaidi.",
        "Kugeuka geuka kitandani ni mbaya zaidi. Labda muziki wa kimya au desturi ya kutuliza ingesaidia.",
        "Natumai utaweza kulala hivi karibuni. Kuwa mpole kwako mwenyewe vyovyote iwavyo.",
    ],
    "fr": [
        "C'est tellement frustrant. Essaie de ne pas stresser à propos de ne pas dormir - ça aggrave parfois les choses.",
        "Rester éveillé, c'est le pire. Peut-être qu'une musique douce ou une routine apaisante pourrait aider.",
        "J'espère que tu pourras t'endormir bientôt. Sois doux avec toi-même de toute façon.",
    ],
}

QUITTING_HABIT_RESPONSES = {
    "en": [
        "That takes real strength. Be patient with yourself - habits don't break overnight.",
        "Good for you for trying. Every small step counts, even with setbacks.",
        "Breaking a habit is hard work. I'm rooting for you.",
    ],
    "sw": [
        "Hiyo inahitaji nguvu ya kweli. Kuwa na uvumilivu kwako mwenyewe - tabia hazivunjwi mara moja.",
        "Vizuri kwako kujaribu. Kila hatua ndogo ina maana, hata kukiwa na vikwazo.",
        "Kuvunja tabia ni kazi ngumu. Ninakusubiri ufanikiwe.",
    ],
    "fr": [
        "Ça demande une vraie force. Sois patient avec toi-même - les habitudes ne se brisent pas du jour au lendemain.",
        "Bravo d'essayer. Chaque petit pas compte, même avec des rechutes.",
        "Casser une habitude, c'est un travail difficile. Je suis de ton côté.",
    ],
}

MEDITATION_MINDFULNESS_RESPONSES = {
    "en": [
        "That's such a great practice for the mind. How's it been working for you?",
        "Mindfulness can make such a difference. I hope it's bringing you some calm.",
        "Good for you for prioritizing that. Even a few minutes a day can help.",
    ],
    "sw": [
        "Hiyo ni desturi nzuri kwa akili. Imekuwa ikikufanyia kazi vipi?",
        "Akili tulivu inaweza kufanya tofauti kubwa. Natumai inakuletea utulivu.",
        "Vizuri kwako kuweka kipaumbele hilo. Dakika chache kwa siku zinaweza kusaidia.",
    ],
    "fr": [
        "C'est une si bonne pratique pour l'esprit. Comment ça fonctionne pour toi ?",
        "La pleine conscience peut faire une telle différence. J'espère que ça t'apporte du calme.",
        "Bravo de prioriser ça. Même quelques minutes par jour peuvent aider.",
    ],
}

SIBLING_RIVALRY_RESPONSES = {
    "en": [
        "Sibling dynamics can be really complicated. That sounds frustrating.",
        "Being compared to a sibling is hard. Your own path matters just as much.",
        "I'm sorry that's happening. Want to talk through what's going on?",
    ],
    "sw": [
        "Mienendo ya ndugu inaweza kuwa ngumu kweli. Hiyo inasikika ya kuchosha.",
        "Kulinganishwa na ndugu ni jambo gumu. Njia yako mwenyewe ina maana sawa.",
        "Pole kwa hilo linalotokea. Unataka kuongea kupitia kinachoendelea?",
    ],
    "fr": [
        "Les dynamiques entre frères et sœurs peuvent être vraiment compliquées. Ça semble frustrant.",
        "Être comparé à un frère ou une sœur, c'est dur. Ton propre chemin compte tout autant.",
        "Je suis désolé que ça arrive. Tu veux parler de ce qui se passe ?",
    ],
}

LONG_DISTANCE_RELATIONSHIP_RESPONSES = {
    "en": [
        "Long distance is hard, but it shows how much you care to keep it going. Hang in there.",
        "Missing someone you love is tough. I hope you get to close that distance soon.",
        "Video calls help, but they're not the same as being together. Stay strong.",
    ],
    "sw": [
        "Umbali ni mgumu, lakini unaonyesha jinsi unajali kuendelea. Jichukulie hatua moja moja.",
        "Kumkosa mtu unayempenda ni vigumu. Natumai utafunga umbali huo hivi karibuni.",
        "Simu za video zinasaidia, lakini si sawa na kuwa pamoja. Kuwa na nguvu.",
    ],
    "fr": [
        "La distance est dure, mais ça montre combien tu tiens à continuer. Tiens bon.",
        "Le fait qu'une personne que tu aimes te manque, c'est difficile. J'espère que tu combleras cette distance bientôt.",
        "Les appels vidéo aident, mais ce n'est pas la même chose qu'être ensemble. Reste fort.",
    ],
}

PET_PEEVE_RESPONSES = {
    "en": [
        "Haha, I get it - little things like that can really add up.",
        "That's a totally valid thing to be bothered by. We all have those.",
        "Pet peeves are so specific and so real. Thanks for sharing yours!",
    ],
    "sw": [
        "Haha, naelewa - mambo madogo kama hayo yanaweza kweli kuongezeka.",
        "Hilo ni jambo halali kabisa kusumbuliwa nalo. Sote tunazo hizo.",
        "Mambo yanayotusumbua ni ya pekee kabisa na ya kweli. Asante kwa kushiriki yako!",
    ],
    "fr": [
        "Haha, je comprends - des petites choses comme ça peuvent vraiment s'accumuler.",
        "C'est totalement valide d'être dérangé par ça. On a tous les nôtres.",
        "Les petites manies sont si spécifiques et si réelles. Merci de partager la tienne !",
    ],
}

KINDNESS_RESPONSES = {
    "en": [
        "That's beautiful - small acts of kindness make such a big difference.",
        "I love that. The world needs more of that kind of thing.",
        "That's wonderful to hear. Kindness really does ripple outward.",
    ],
    "sw": [
        "Hiyo ni nzuri - vitendo vidogo vya huruma vinaleta tofauti kubwa.",
        "Ninapenda hilo. Dunia inahitaji zaidi ya jambo kama hilo.",
        "Hiyo ni nzuri kusikia. Huruma kweli inaenea kwa wengine.",
    ],
    "fr": [
        "C'est magnifique - les petits actes de bonté font une si grande différence.",
        "J'adore ça. Le monde a besoin de plus de ce genre de chose.",
        "C'est merveilleux à entendre. La bonté se répand vraiment vers l'extérieur.",
    ],
}

PROCRASTINATION_RESPONSES = {
    "en": [
        "We've all been there! Sometimes starting with just five minutes helps break the cycle.",
        "Procrastination is so universal. Be kind to yourself about it.",
        "I hear you - try breaking it into the smallest possible first step.",
    ],
    "sw": [
        "Sote tumekuwa hapo! Mara nyingine kuanza kwa dakika tano tu kunasaidia kuvunja mzunguko.",
        "Kuchelewesha ni jambo la kawaida sana. Kuwa mpole kwako mwenyewe kuhusu hilo.",
        "Nakusikia - jaribu kugawanya kwa hatua ndogo zaidi ya kwanza.",
    ],
    "fr": [
        "On y est tous passés ! Parfois, commencer par juste cinq minutes aide à briser le cycle.",
        "La procrastination est si universelle. Sois gentil avec toi-même à ce sujet.",
        "Je comprends - essaie de la diviser en la plus petite première étape possible.",
    ],
}

DECLUTTERING_RESPONSES = {
    "en": [
        "Decluttering feels so good once it's done! How's it going?",
        "A clean space really does help clear the mind. Enjoy the process!",
        "Minimalism can be so freeing. What are you letting go of?",
    ],
    "sw": [
        "Kupanga vitu kunajisikia vizuri sana baada ya kukamilika! Inaendaje?",
        "Nafasi safi kweli inasaidia kutuliza akili. Furahia mchakato!",
        "Kuondoa vitu visivyo vya muhimu kunaweza kuwa huru. Unaachilia nini?",
    ],
    "fr": [
        "Désencombrer fait tellement de bien une fois terminé ! Comment ça se passe ?",
        "Un espace propre aide vraiment à clarifier l'esprit. Profite du processus !",
        "Le minimalisme peut être si libérateur. Qu'est-ce que tu laisses partir ?",
    ],
}

PUBLIC_SPEAKING_RESPONSES = {
    "en": [
        "Public speaking nerves are so common, even for experienced speakers. You'll do great!",
        "Take a deep breath - you know your material better than anyone in that room.",
        "I believe in you! Practice a few times and it'll feel more natural.",
    ],
    "sw": [
        "Wasiwasi wa kuongea hadharani ni wa kawaida sana, hata kwa wazungumzaji wenye uzoefu. Utafanya vizuri!",
        "Pumua kwa kina - unajua mada yako vizuri zaidi kuliko mtu yeyote katika chumba hicho.",
        "Ninakuamini! Jizoeze mara chache nayo itahisi ya kawaida zaidi.",
    ],
    "fr": [
        "Le trac de parler en public est si courant, même pour les orateurs expérimentés. Tu vas réussir !",
        "Respire profondément - tu connais ton sujet mieux que quiconque dans cette salle.",
        "Je crois en toi ! Pratique quelques fois et ça semblera plus naturel.",
    ],
}

LEARNING_TO_DRIVE_RESPONSES = {
    "en": [
        "That's exciting! A little nervousness is totally normal at first.",
        "Congratulations on the progress! Driving gets easier with practice.",
        "Take it slow and steady - you'll get the hang of it.",
    ],
    "sw": [
        "Hiyo ni ya kusisimua! Wasiwasi kidogo ni wa kawaida mwanzoni.",
        "Hongera kwa maendeleo! Kuendesha gari kunakuwa rahisi kwa mazoezi.",
        "Fanya kwa upole na uthabiti - utaelewa hilo.",
    ],
    "fr": [
        "C'est excitant ! Un peu de nervosité est tout à fait normal au début.",
        "Félicitations pour les progrès ! Conduire devient plus facile avec la pratique.",
        "Vas-y doucement et de façon constante - tu vas y arriver.",
    ],
}

RETIREMENT_PLANNING_RESPONSES = {
    "en": [
        "That's such an important thing to plan for. I'm not a financial advisor, but it's great that you're thinking ahead.",
        "Planning early really pays off. Good for you for being proactive.",
        "Retirement planning takes discipline. I hope it all comes together nicely.",
    ],
    "sw": [
        "Hiyo ni jambo muhimu sana kupanga. Mimi si mshauri wa kifedha, lakini ni vizuri unafikiria mbele.",
        "Kupanga mapema kweli kuna faida. Vizuri kwako kuwa na mpango.",
        "Kupanga kustaafu kunahitaji nidhamu. Natumai yote yatakwenda vizuri.",
    ],
    "fr": [
        "C'est une chose si importante à planifier. Je ne suis pas conseiller financier, mais c'est génial que tu penses à l'avance.",
        "Planifier tôt rapporte vraiment. Bravo d'être proactif.",
        "Planifier la retraite demande de la discipline. J'espère que tout s'arrangera bien.",
    ],
}

PROGRAMMING_CODING_RESPONSES = {
    "en": [
        "Debugging can be so frustrating, but that 'aha' moment makes it worth it!",
        "Code problems happen to everyone, even experienced developers. Take a break and come back to it.",
        "I appreciate code - I'm made of it! What are you working on?",
    ],
    "sw": [
        "Kutafuta hitilafu kunaweza kuchosha sana, lakini wakati huo wa 'aha' unalipa!",
        "Matatizo ya msimbo hutokea kwa kila mtu, hata wabunifu wenye uzoefu. Pumzika kidogo na urudi kwake.",
        "Ninathamini msimbo - nimefanywa nao! Unafanyia kazi nini?",
    ],
    "fr": [
        "Déboguer peut être tellement frustrant, mais ce moment 'aha' en vaut la peine !",
        "Les problèmes de code arrivent à tout le monde, même aux développeurs expérimentés. Fais une pause et reviens-y.",
        "J'apprécie le code - j'en suis fait ! Sur quoi travailles-tu ?",
    ],
}

GYM_INTIMIDATION_RESPONSES = {
    "en": [
        "That feeling is so common - everyone there started as a beginner too.",
        "Gym anxiety is real, but most people are too focused on their own workout to judge yours.",
        "You belong there just as much as anyone else. One visit at a time.",
    ],
    "sw": [
        "Hisia hiyo ni ya kawaida sana - kila mtu hapo alianza kama mwanzilishi pia.",
        "Wasiwasi wa gym ni wa kweli, lakini watu wengi wamejikita kwenye mazoezi yao wenyewe kuhukumu yako.",
        "Unastahili kuwa hapo kama mtu mwingine yeyote. Ziara moja kwa wakati.",
    ],
    "fr": [
        "Ce sentiment est si courant - tout le monde là-bas a commencé comme débutant aussi.",
        "L'anxiété de la salle de sport est réelle, mais la plupart des gens sont trop concentrés sur leur propre entraînement pour juger le tien.",
        "Tu as ta place là autant que n'importe qui. Une visite à la fois.",
    ],
}

COMFORT_FOOD_RESPONSES = {
    "en": [
        "Comfort food is the best kind of food. Go treat yourself!",
        "Sounds like you deserve a good comforting meal. Enjoy it!",
        "There's nothing wrong with a little comfort food when you need it.",
    ],
    "sw": [
        "Chakula cha faraja ni aina bora zaidi ya chakula. Jipe zawadi!",
        "Inasikika kama unastahili mlo mzuri wa faraja. Furahia!",
        "Hakuna kibaya na chakula kidogo cha faraja unapohitaji.",
    ],
    "fr": [
        "La nourriture réconfortante, c'est le meilleur genre de nourriture. Fais-toi plaisir !",
        "On dirait que tu mérites un bon repas réconfortant. Profite-en !",
        "Il n'y a rien de mal à un peu de nourriture réconfortante quand tu en as besoin.",
    ],
}

# --- Tenth wave of response banks -------------------------------------------

SINGING_VOICE_RESPONSES = {
    "en": [
        "Singing is such a great way to lift your mood! Any favorite songs to belt out?",
        "I love that. Music has a way of making everything feel lighter.",
        "Shower concerts are the best concerts, honestly.",
    ],
    "sw": [
        "Kuimba ni njia nzuri ya kuboresha hisia! Una nyimbo unazopenda kuimba?",
        "Ninapenda hilo. Muziki una njia ya kufanya kila kitu kihisi cha wepesi.",
        "Tamasha za bafuni ni tamasha bora zaidi, kwa uhakika.",
    ],
    "fr": [
        "Chanter, c'est une excellente façon de remonter le moral ! Des chansons préférées à pousser ?",
        "J'adore ça. La musique a le pouvoir de tout rendre plus léger.",
        "Les concerts sous la douche sont les meilleurs concerts, honnêtement.",
    ],
}

JOURNALING_RESPONSES = {
    "en": [
        "Journaling is such a healthy habit. It really helps process things.",
        "I love that for you. Writing thoughts down can be so clarifying.",
        "Keeping a journal is a great way to track your own growth over time.",
    ],
    "sw": [
        "Kuandika jarida ni tabia nzuri sana. Kweli kunasaidia kuchakata mambo.",
        "Ninapenda hilo kwako. Kuandika mawazo kunaweza kuwa na uwazi mkubwa.",
        "Kuandika jarida ni njia nzuri ya kufuatilia ukuaji wako mwenyewe kwa muda.",
    ],
    "fr": [
        "Tenir un journal est une habitude si saine. Ça aide vraiment à digérer les choses.",
        "J'adore ça pour toi. Écrire ses pensées peut être si clarifiant.",
        "Tenir un journal est une excellente façon de suivre ta propre croissance avec le temps.",
    ],
}

BOARD_GAMES_PUZZLES_RESPONSES = {
    "en": [
        "Game nights are the best! What's the game of choice?",
        "Puzzles are so satisfying to complete. Hope it's a good one!",
        "Board games bring people together so well. Enjoy the night!",
    ],
    "sw": [
        "Usiku wa michezo ni bora zaidi! Mchezo wa kuchagua ni gani?",
        "Mafumbo ni ya kuridhisha sana kukamilisha. Natumai ni nzuri!",
        "Michezo ya bodi inawaleta watu pamoja vizuri sana. Furahia usiku!",
    ],
    "fr": [
        "Les soirées jeux sont les meilleures ! Quel est le jeu choisi ?",
        "Les puzzles sont si satisfaisants à compléter. J'espère que c'est un bon !",
        "Les jeux de société rassemblent si bien les gens. Profite de la soirée !",
    ],
}

CAMPING_OUTDOOR_TRIP_RESPONSES = {
    "en": [
        "Camping sounds amazing! Sleeping under the stars is such a special experience.",
        "Nature trips are so refreshing. Hope the weather cooperates!",
        "That sounds like a great adventure. Enjoy the fresh air!",
    ],
    "sw": [
        "Kambi inasikika ya kustaajabisha! Kulala chini ya nyota ni uzoefu wa pekee.",
        "Safari za asili ni za kuburudisha sana. Natumai hali ya hewa itakuwa nzuri!",
        "Hiyo inasikika kama adventure nzuri. Furahia hewa safi!",
    ],
    "fr": [
        "Le camping a l'air génial ! Dormir sous les étoiles, c'est une expérience si spéciale.",
        "Les voyages dans la nature sont si rafraîchissants. J'espère que la météo collaborera !",
        "Ça a l'air d'être une belle aventure. Profite de l'air frais !",
    ],
}

CAR_TROUBLE_RESPONSES = {
    "en": [
        "Car trouble is so stressful. I hope you get it sorted quickly.",
        "That's the worst timing, isn't it? Hope it's a quick and cheap fix.",
        "Hang in there - car issues are frustrating but usually fixable.",
    ],
    "sw": [
        "Tatizo la gari linatia msongo sana. Natumai utalishughulikia haraka.",
        "Hiyo ni wakati mbaya zaidi, sivyo? Natumai ni urekebishaji wa haraka na wa bei nafuu.",
        "Jichukulie hatua moja moja - matatizo ya gari yanachosha lakini kawaida yanarekebishika.",
    ],
    "fr": [
        "Les problèmes de voiture sont si stressants. J'espère que tu régleras ça vite.",
        "C'est le pire moment, non ? J'espère que c'est une réparation rapide et pas chère.",
        "Tiens bon - les problèmes de voiture sont frustrants mais généralement réparables.",
    ],
}

ROOMMATES_RESPONSES = {
    "en": [
        "Roommate life has its ups and downs. How's it going overall?",
        "Living with others takes some adjusting. I hope things are mostly smooth.",
        "Roommate situations can be tricky sometimes. Want to talk about it?",
    ],
    "sw": [
        "Maisha ya wenzangu wa nyumba yana changamoto na mafanikio. Inaendaje kwa ujumla?",
        "Kuishi na wengine kunahitaji marekebisho. Natumai mambo ni laini zaidi.",
        "Hali za wenzangu wa nyumba zinaweza kuwa ngumu mara kwa mara. Unataka kuongea kuhusu hilo?",
    ],
    "fr": [
        "La vie en colocation a ses hauts et ses bas. Comment ça se passe globalement ?",
        "Vivre avec d'autres demande un peu d'adaptation. J'espère que les choses sont plutôt fluides.",
        "Les situations de colocation peuvent être délicates parfois. Tu veux en parler ?",
    ],
}

ONLINE_DATING_RESPONSES = {
    "en": [
        "Online dating can be a rollercoaster! I hope it goes well.",
        "That's exciting! How are you feeling about it?",
        "First dates are nerve-wracking but exciting. Good luck!",
    ],
    "sw": [
        "Uchumba mtandaoni unaweza kuwa mzunguko wa hisia! Natumai utakwenda vizuri.",
        "Hiyo ni ya kusisimua! Unajisikiaje kuhusu hilo?",
        "Tarehe za kwanza zinatia wasiwasi lakini ni za kusisimua. Bahati njema!",
    ],
    "fr": [
        "Les rencontres en ligne peuvent être des montagnes russes ! J'espère que ça ira bien.",
        "C'est excitant ! Comment tu te sens à ce sujet ?",
        "Les premiers rendez-vous sont stressants mais excitants. Bonne chance !",
    ],
}

TATTOOS_PIERCINGS_RESPONSES = {
    "en": [
        "That's exciting! Do you know what design or style you're going for?",
        "Tattoos and piercings can be such meaningful self-expression. I hope you love it!",
        "That's a big decision - take your time choosing the right artist/studio.",
    ],
    "sw": [
        "Hiyo ni ya kusisimua! Unajua muundo au mtindo unataka?",
        "Tatoo na kutoboa vinaweza kuwa namna ya kujieleza yenye maana. Natumai utaipenda!",
        "Hiyo ni uamuzi mkubwa - jichukulie muda kuchagua msanii au studio sahihi.",
    ],
    "fr": [
        "C'est excitant ! Sais-tu quel design ou style tu recherches ?",
        "Les tatouages et piercings peuvent être une expression de soi si significative. J'espère que tu vas adorer !",
        "C'est une grande décision - prends ton temps pour choisir le bon artiste/studio.",
    ],
}

FASHION_STYLE_RESPONSES = {
    "en": [
        "I love hearing about personal style - it's such a fun form of self-expression!",
        "What look are you going for today?",
        "Fashion is such a great way to express yourself. Have fun with it!",
    ],
    "sw": [
        "Ninapenda kusikia kuhusu mtindo wa kibinafsi - ni namna ya kufurahisha ya kujieleza!",
        "Unataka mwonekano gani leo?",
        "Mitindo ni njia nzuri ya kujieleza. Furahia hilo!",
    ],
    "fr": [
        "J'aime entendre parler du style personnel - c'est une forme d'expression de soi si amusante !",
        "Quel look recherches-tu aujourd'hui ?",
        "La mode est une si belle façon de t'exprimer. Amuse-toi avec ça !",
    ],
}

LANGUAGE_BARRIER_RESPONSES = {
    "en": [
        "Language barriers can be really frustrating. Patience and gestures go a long way!",
        "That sounds tough to navigate. Translation apps can sometimes help in a pinch.",
        "Communication challenges happen, but there's usually a way to bridge the gap.",
    ],
    "sw": [
        "Vizuizi vya lugha vinaweza kuchosha sana. Uvumilivu na ishara husaidia sana!",
        "Hiyo inasikika ngumu kuvinjari. Programu za tafsiri zinaweza kusaidia wakati mwingine.",
        "Changamoto za mawasiliano hutokea, lakini kawaida kuna njia ya kuunganisha pengo.",
    ],
    "fr": [
        "Les barrières linguistiques peuvent être vraiment frustrantes. La patience et les gestes aident beaucoup !",
        "Ça semble difficile à naviguer. Les applications de traduction peuvent parfois aider en cas de besoin.",
        "Les défis de communication arrivent, mais il y a généralement une façon de combler l'écart.",
    ],
}

SCHOOL_VOLUNTEERING_RESPONSES = {
    "en": [
        "That's so generous of you! Schools really benefit from involved volunteers.",
        "What a great way to be involved. I'm sure it means a lot to everyone there.",
        "Volunteering at school is wonderful - thank you for giving your time.",
    ],
    "sw": [
        "Hiyo ni ya ukarimu sana kwako! Shule zinafaidika kweli na watu wa kujitolea.",
        "Jinsi ya nzuri ya kushiriki. Nina hakika inamaanisha mengi kwa kila mtu huko.",
        "Kujitolea shuleni ni jambo zuri - asante kwa kutoa muda wako.",
    ],
    "fr": [
        "C'est tellement généreux de ta part ! Les écoles bénéficient vraiment de bénévoles impliqués.",
        "Quelle belle façon de s'impliquer. Je suis sûr que ça compte beaucoup pour tout le monde là-bas.",
        "Faire du bénévolat à l'école, c'est merveilleux - merci de donner ton temps.",
    ],
}

CHARITY_DONATION_RESPONSES = {
    "en": [
        "That's wonderful - every contribution helps make a real difference.",
        "Generosity like that matters so much. Thank you for giving back.",
        "I love that. Causes like that need people like you.",
    ],
    "sw": [
        "Hiyo ni nzuri - kila mchango unasaidia kufanya tofauti ya kweli.",
        "Ukarimu kama huo una maana kubwa. Asante kwa kurudisha.",
        "Ninapenda hilo. Sababu kama hizo zinahitaji watu kama wewe.",
    ],
    "fr": [
        "C'est merveilleux - chaque contribution aide à faire une vraie différence.",
        "Une générosité comme ça compte énormément. Merci de redonner.",
        "J'adore ça. Des causes comme ça ont besoin de gens comme toi.",
    ],
}

HOSTING_GUESTS_RESPONSES = {
    "en": [
        "Hosting can be a lot of work, but it's so rewarding when everyone has a good time!",
        "I hope everything comes together nicely for your guests.",
        "That sounds like fun - enjoy the company!",
    ],
    "sw": [
        "Kupokea wageni kunaweza kuwa kazi nyingi, lakini ni ya kuridhisha kila mtu anapofurahia!",
        "Natumai kila kitu kitafanikiwa vizuri kwa wageni wako.",
        "Hiyo inasikika ya kufurahisha - furahia ushirika!",
    ],
    "fr": [
        "Recevoir peut être beaucoup de travail, mais c'est si gratifiant quand tout le monde passe un bon moment !",
        "J'espère que tout se passera bien pour tes invités.",
        "Ça a l'air amusant - profite de la compagnie !",
    ],
}

TIME_ZONES_RESPONSES = {
    "en": [
        "Time zones can be so confusing! I hope you're able to coordinate smoothly.",
        "Coordinating across time zones takes some planning, but it's doable!",
        "That's always tricky. A world clock app can really help with that.",
    ],
    "sw": [
        "Maeneo ya muda yanaweza kuchanganya sana! Natumai utaweza kuratibu vizuri.",
        "Kuratibu kati ya maeneo ya muda kunahitaji mpango, lakini ni rahisi kufanyika!",
        "Hiyo daima ni ngumu. Programu ya saa ya dunia inaweza kusaidia kweli na hilo.",
    ],
    "fr": [
        "Les fuseaux horaires peuvent être si déroutants ! J'espère que tu pourras coordonner facilement.",
        "Coordonner à travers les fuseaux horaires demande un peu de planification, mais c'est faisable !",
        "C'est toujours délicat. Une application d'horloge mondiale peut vraiment aider avec ça.",
    ],
}

PRODUCTIVITY_TOOLS_RESPONSES = {
    "en": [
        "Staying organized makes such a difference! What's working well for you so far?",
        "I love a good productivity system. Hope it's helping you feel more in control.",
        "Finding the right tool can be a game changer. Good for you for trying!",
    ],
    "sw": [
        "Kuwa na mpangilio kunafanya tofauti kubwa! Ni nini kinakufanyia kazi vizuri mpaka sasa?",
        "Ninapenda mfumo mzuri wa uzalishaji. Natumai unakusaidia kujisikia na udhibiti zaidi.",
        "Kupata zana sahihi kunaweza kubadilisha mchezo. Vizuri kwako kujaribu!",
    ],
    "fr": [
        "Rester organisé fait une telle différence ! Qu'est-ce qui fonctionne bien pour toi jusqu'à présent ?",
        "J'adore un bon système de productivité. J'espère que ça t'aide à te sentir plus en contrôle.",
        "Trouver le bon outil peut tout changer. Bravo d'essayer !",
    ],
}

# --- Eleventh wave of response banks (some topics here are sensitive;
# responses lean toward warmth and validation rather than chipper
# small talk, and gently point toward real support where appropriate) --

PARENTING_RESPONSES = {
    "en": [
        "Parenting is one of the hardest and most rewarding things there is. How are you holding up?",
        "That sounds like a lot. Parenting doesn't come with an instruction manual - you're doing your best.",
        "Raising kids takes so much patience. I hope you're giving yourself credit for the effort.",
    ],
    "sw": [
        "Uzazi ni mojawapo ya mambo magumu zaidi na ya kuridhisha zaidi yaliyopo. Unaendeleaje?",
        "Hiyo inasikika kama mengi. Uzazi haukuji na kitabu cha maelekezo - unafanya bidii yako.",
        "Kulea watoto kunahitaji uvumilivu mwingi. Natumai unajipa sifa kwa jitihada.",
    ],
    "fr": [
        "Être parent est l'une des choses les plus difficiles et les plus gratifiantes qui existent. Comment tu tiens le coup ?",
        "Ça semble être beaucoup. Être parent ne vient pas avec un mode d'emploi - tu fais de ton mieux.",
        "Élever des enfants demande tellement de patience. J'espère que tu te reconnais le mérite de cet effort.",
    ],
}

TEENAGER_STRUGGLE_RESPONSES = {
    "en": [
        "Teen years are tough for everyone involved. You're not failing - this stage is just genuinely hard.",
        "That phase tests every parent's patience. I hope things ease up soon.",
        "Teenagers pushing boundaries is normal, even when it's exhausting. Hang in there.",
    ],
    "sw": [
        "Miaka ya balehe ni migumu kwa kila mtu anayehusika. Hauwashindwi - hatua hii ni ngumu kwa kweli.",
        "Awamu hiyo inajaribu uvumilivu wa kila mzazi. Natumai mambo yatapungua hivi karibuni.",
        "Vijana wa balehe wanaosukuma mipaka ni wa kawaida, hata ikiwa inachosha. Jichukulie hatua moja moja.",
    ],
    "fr": [
        "Les années d'adolescence sont dures pour tout le monde. Tu n'échoues pas - cette étape est juste vraiment difficile.",
        "Cette phase teste la patience de chaque parent. J'espère que les choses s'apaiseront bientôt.",
        "Les ados qui repoussent les limites, c'est normal, même quand c'est épuisant. Tiens bon.",
    ],
}

ELDERLY_PARENT_CARE_RESPONSES = {
    "en": [
        "Caregiving for a parent is such a profound responsibility, and it can be exhausting too. Make sure you're caring for yourself as well.",
        "That's a lot to carry, emotionally and practically. I hope you have some support around you.",
        "Caring for an aging parent brings up so much. Be gentle with yourself through it.",
    ],
    "sw": [
        "Kumtunza mzazi ni jukumu kubwa sana, na linaweza kuchosha pia. Hakikisha unajitunza pia.",
        "Hiyo ni mzigo mkubwa, kihisia na kivitendo. Natumai una msaada karibu nawe.",
        "Kumtunza mzazi anayezeeka kunaleta mengi. Kuwa mpole kwako mwenyewe katika hilo.",
    ],
    "fr": [
        "S'occuper d'un parent est une responsabilité si profonde, et ça peut être épuisant aussi. Assure-toi de prendre soin de toi aussi.",
        "C'est beaucoup à porter, émotionnellement et pratiquement. J'espère que tu as du soutien autour de toi.",
        "Prendre soin d'un parent vieillissant fait remonter beaucoup de choses. Sois doux avec toi-même à travers ça.",
    ],
}

GRIEF_LOSS_RESPONSES = {
    "en": [
        "I'm so sorry for your loss. There's no right way to grieve - please be gentle with yourself.",
        "Losing someone you love is one of the hardest things a person can go through. I'm here if you want to talk.",
        "I'm really sorry. Grief comes in waves, and however you're feeling right now is valid.",
        "I'm so sorry. There's nothing I can say that fixes this, but I'm here.",
        "Grief doesn't follow a schedule - take whatever time this actually takes.",
        "Whatever you're feeling right now, even if it contradicts itself, is part of this.",
        "Loss reshapes things in ways that take a long time to settle - be patient with yourself.",
        "I'm glad you're not carrying this completely alone right now.",
        "However you grieve is the right way for you - there's no template to follow.",
        "That kind of loss leaves a real, lasting mark. I'm sorry you're carrying it.",
        "It's okay if some days are harder than others, even much later.",
        "Whatever they meant to you, that doesn't have to be explained or justified to anyone.",
        "I'm here if you want to talk about them, or just need quiet company.",
        "Grief and love are tangled together - the size of one often reflects the size of the other.",
        "There's no timeline you're supposed to be on. Go at whatever pace this takes.",
        "Thank you for trusting me with something this heavy.",
        "If it would help to talk to someone who specializes in grief, that's a real, valid option alongside talking to me.",
    ],
    "sw": [
        "Pole sana kwa kupoteza. Hakuna njia sahihi ya kuomboleza - tafadhali kuwa mpole kwako mwenyewe.",
        "Kumpoteza mtu unayempenda ni mojawapo ya mambo magumu zaidi mtu anaweza kupitia. Niko hapa ukitaka kuongea.",
        "Pole sana. Huzuni inakuja kwa mawimbi, na vyovyote unavyohisi sasa hivi ni halali.",
        "Pole sana. Hakuna ninachoweza kusema kinachorekebisha hili, lakini niko hapa.",
        "Maombolezo hayafuati ratiba - chukua muda wowote hili linahitaji kweli.",
        "Chochote unachohisi sasa hivi, hata kikijipinga chenyewe, ni sehemu ya hili.",
        "Hasara inabadilisha mambo kwa njia zinazochukua muda mrefu kutulia - kuwa na uvumilivu na nafsi yako.",
        "Nafurahi hubebi hili peke yako kabisa sasa hivi.",
        "Vyovyote unavyoomboleza ndiyo njia sahihi kwako - hakuna kiolezo cha kufuata.",
        "Hasara ya aina hiyo inaacha alama ya kweli, ya kudumu. Pole unaibeba.",
        "Ni sawa kama siku zingine ni ngumu zaidi kuliko zingine, hata baadaye sana.",
        "Vyovyote walivyokuwa kwako, hilo halihitaji kuelezwa au kuthibitishwa kwa mtu yeyote.",
        "Niko hapa ukitaka kuzungumza kuwahusu, au unahitaji tu ushirika wa kimya.",
        "Maombolezo na upendo vimeunganishwa - ukubwa wa kimoja mara nyingi unaonyesha ukubwa wa kingine.",
        "Hakuna ratiba unayopaswa kuwa nayo. Enda kwa kasi yoyote hili linahitaji.",
        "Asante kwa kuniaminisha kitu kizito hivi.",
        "Kama ingesaidia kuzungumza na mtu anayebobea katika maombolezo, hilo ni chaguo la kweli, halali kando ya kuzungumza nami.",
    ],
    "fr": [
        "Je suis vraiment désolé pour ta perte. Il n'y a pas de bonne façon de faire son deuil - sois doux avec toi-même.",
        "Perdre quelqu'un qu'on aime est l'une des choses les plus difficiles qu'une personne puisse traverser. Je suis là si tu veux parler.",
        "Je suis vraiment désolé. Le chagrin vient par vagues, et quoi que tu ressentes maintenant est valide.",
        "Je suis vraiment désolé. Il n'y a rien que je puisse dire qui répare ça, mais je suis là.",
        "Le deuil ne suit pas d'horaire - prends tout le temps que ça prend vraiment.",
        "Quoi que tu ressentes en ce moment, même si ça se contredit, ça fait partie de ça.",
        "La perte remodèle les choses d'une façon qui prend longtemps à se stabiliser - sois patient avec toi-même.",
        "Je suis content que tu ne portes pas ça complètement seul en ce moment.",
        "Quelle que soit ta façon de faire ton deuil, c'est la bonne pour toi - il n'y a pas de modèle à suivre.",
        "Ce genre de perte laisse une marque réelle et durable. Je suis désolé que tu la portes.",
        "C'est normal si certains jours sont plus durs que d'autres, même bien plus tard.",
        "Quoi qu'ils aient représenté pour toi, ça n'a pas à être expliqué ou justifié à qui que ce soit.",
        "Je suis là si tu veux parler d'eux, ou si tu as juste besoin d'une présence silencieuse.",
        "Le deuil et l'amour sont entremêlés - la taille de l'un reflète souvent la taille de l'autre.",
        "Il n'y a pas de calendrier que tu es censé suivre. Avance au rythme que ça demande.",
        "Merci de me faire confiance avec quelque chose d'aussi lourd.",
        "Si ça aiderait de parler à quelqu'un spécialisé dans le deuil, c'est une option réelle et valable en plus de me parler à moi.",
    ],
}

THERAPY_COUNSELING_RESPONSES = {
    "en": [
        "That's a really positive step to take for yourself. I hope it's helping.",
        "Good for you for prioritizing your mental health like that.",
        "Therapy can be really valuable. I hope you're finding it useful.",
    ],
    "sw": [
        "Hiyo ni hatua nzuri kwa ajili yako mwenyewe. Natumai inasaidia.",
        "Vizuri kwako kuweka kipaumbele afya yako ya akili kwa namna hiyo.",
        "Tiba inaweza kuwa na thamani kubwa. Natumai unaipata kuwa na manufaa.",
    ],
    "fr": [
        "C'est une étape vraiment positive pour toi-même. J'espère que ça t'aide.",
        "Bravo de prioriser ta santé mentale comme ça.",
        "La thérapie peut être très précieuse. J'espère que tu la trouves utile.",
    ],
}

ADDICTION_RECOVERY_RESPONSES = {
    "en": [
        "That takes real strength and courage. I'm proud of you for that, genuinely.",
        "Recovery isn't a straight line, and every day you stay on that path matters.",
        "That's a hard road, and you're walking it. That counts for a lot.",
    ],
    "sw": [
        "Hiyo inahitaji nguvu na ujasiri wa kweli. Ninakuhusudia kwa hilo, kwa kweli.",
        "Kupona si njia ya moja kwa moja, na kila siku unayobaki kwenye njia hiyo ina maana.",
        "Hiyo ni njia ngumu, na unaitembea. Hiyo ina maana kubwa.",
    ],
    "fr": [
        "Ça demande une vraie force et du courage. Je suis fier de toi pour ça, sincèrement.",
        "Le rétablissement n'est pas une ligne droite, et chaque jour où tu restes sur ce chemin compte.",
        "C'est une route difficile, et tu la parcoures. Ça compte énormément.",
    ],
}

IDENTITY_COMING_OUT_RESPONSES = {
    "en": [
        "Thank you for trusting me with that. Figuring out who you are takes real courage.",
        "That's a meaningful and personal journey. I'm glad you're giving yourself the space for it.",
        "Whoever you are and however that unfolds, that's worth honoring.",
    ],
    "sw": [
        "Asante kwa kuniaminisha hilo. Kujua wewe ni nani kunahitaji ujasiri wa kweli.",
        "Hiyo ni safari ya maana na ya kibinafsi. Nafurahi unajipa nafasi kwa hilo.",
        "Vyovyote uwe nani na vyovyote linavyofunuka, hilo linastahili kuheshimiwa.",
    ],
    "fr": [
        "Merci de me faire confiance avec ça. Comprendre qui tu es demande un vrai courage.",
        "C'est un voyage significatif et personnel. Je suis content que tu te donnes l'espace pour ça.",
        "Qui que tu sois et quelle que soit la façon dont ça se dévoile, ça vaut la peine d'être honoré.",
    ],
}

IMMIGRATION_RESPONSES = {
    "en": [
        "That's such a huge transition. Homesickness is real, even when the move is the right choice.",
        "Adjusting to a new country takes time. Be patient with yourself through it.",
        "Moving somewhere completely new takes real courage. I hope it starts feeling like home soon.",
    ],
    "sw": [
        "Hiyo ni mabadiliko makubwa sana. Kukosa nyumbani ni kweli, hata kuhama kukiwa chaguo sahihi.",
        "Kuzoea nchi mpya kunahitaji muda. Kuwa na uvumilivu kwako mwenyewe katika hilo.",
        "Kuhama mahali kipya kabisa kunahitaji ujasiri wa kweli. Natumai itaanza kujisikia kama nyumbani hivi karibuni.",
    ],
    "fr": [
        "C'est une transition si énorme. Le mal du pays est réel, même quand le déménagement est le bon choix.",
        "S'adapter à un nouveau pays prend du temps. Sois patient avec toi-même à travers ça.",
        "Déménager dans un endroit complètement nouveau demande un vrai courage. J'espère que ça commencera à ressembler à un foyer bientôt.",
    ],
}

DISABILITY_ACCESSIBILITY_RESPONSES = {
    "en": [
        "Thanks for sharing that with me. Accessibility barriers are real and frustrating - you deserve a world that works for you.",
        "That sounds like a real challenge to navigate daily. I hear you.",
        "Living with that comes with its own set of obstacles others might not see. I appreciate you telling me.",
    ],
    "sw": [
        "Asante kwa kunishirikisha hilo. Vizuizi vya ufikiaji ni vya kweli na vinachosha - unastahili dunia inayokufanyia kazi.",
        "Hiyo inasikika kama changamoto ya kweli ya kuvinjari kila siku. Nakusikia.",
        "Kuishi na hilo kunakuja na vikwazo vyake ambavyo wengine hawawezi kuona. Nashukuru umeniambia.",
    ],
    "fr": [
        "Merci de partager ça avec moi. Les barrières d'accessibilité sont réelles et frustrantes - tu mérites un monde qui fonctionne pour toi.",
        "Ça semble être un vrai défi à naviguer quotidiennement. Je t'entends.",
        "Vivre avec ça vient avec ses propres obstacles que d'autres ne voient peut-être pas. J'apprécie que tu me le dises.",
    ],
}

MENSTRUAL_HEALTH_RESPONSES = {
    "en": [
        "I hope you're able to rest and take care of yourself through it.",
        "That can be really uncomfortable. I hope it passes quickly for you.",
        "Take it easy on yourself today if you can.",
    ],
    "sw": [
        "Natumai utaweza kupumzika na kujitunza katika hilo.",
        "Hiyo inaweza kuwa ya kusumbua kweli. Natumai itapita haraka kwako.",
        "Jichukulie kwa upole leo ukiweza.",
    ],
    "fr": [
        "J'espère que tu pourras te reposer et prendre soin de toi à travers ça.",
        "Ça peut être vraiment inconfortable. J'espère que ça passera vite pour toi.",
        "Sois doux avec toi-même aujourd'hui si tu peux.",
    ],
}

CHECKUP_VACCINE_RESPONSES = {
    "en": [
        "Good for you for staying on top of your health! Hope it goes smoothly.",
        "Regular checkups make such a difference. I hope all goes well.",
        "Taking care of your health like that matters. Good luck at the appointment!",
    ],
    "sw": [
        "Vizuri kwako kuendelea kuwa makini na afya yako! Natumai itakwenda vizuri.",
        "Uchunguzi wa mara kwa mara unafanya tofauti kubwa. Natumai yote yatakwenda vizuri.",
        "Kujali afya yako kwa namna hiyo kuna maana. Bahati njema kwenye miadi!",
    ],
    "fr": [
        "Bravo de rester attentif à ta santé ! J'espère que ça se passera bien.",
        "Les bilans réguliers font une telle différence. J'espère que tout ira bien.",
        "Prendre soin de ta santé comme ça compte. Bonne chance pour le rendez-vous !",
    ],
}

CLIMATE_ANXIETY_RESPONSES = {
    "en": [
        "That worry is shared by a lot of people, and it's understandable given what's happening in the world.",
        "Climate anxiety is real. Channeling it into small, sustainable actions can sometimes help with the feeling of helplessness.",
        "It's a heavy thing to carry. You're not alone in feeling concerned about it.",
        "That worry makes a lot of sense given the scale of what's happening - you're not overreacting.",
        "It's a heavy thing to carry, especially since it's not something any one person can fix alone.",
        "That feeling of helplessness in the face of something this big is really common right now.",
        "Caring this much about the planet says something good about you, even when it's painful.",
        "Small actions don't fix everything, but they can sometimes make the dread feel less paralyzing.",
        "You're allowed to feel this without having a solution ready.",
        "That grief for the future is real grief, even though it's about something that hasn't fully happened yet.",
        "It helps some people to focus on what's actually in their control, even if it's small.",
        "You're far from alone in feeling this - it's an increasingly common, valid worry.",
        "That kind of big-picture anxiety is exhausting precisely because it never fully turns off.",
        "Whatever you're feeling about this, it doesn't make you dramatic - it makes you aware.",
        "I hope you can find moments where this worry isn't the loudest thing in the room.",
        "Connecting with others who care about the same things can sometimes make the weight feel shared.",
        "If this worry is affecting your daily life heavily, talking to someone trained in eco-anxiety could genuinely help alongside anything we talk about here.",
    ],
    "sw": [
        "Wasiwasi huo unashirikiwa na watu wengi, na unaeleweka kwa kuzingatia kinachoendelea duniani.",
        "Wasiwasi wa tabianchi ni wa kweli. Kuubadilisha kuwa hatua ndogo za uendelevu kunaweza kusaidia na hisia za kutokuwa na uwezo.",
        "Ni mzigo mkubwa kubeba. Hauko peke yako kuhisi wasiwasi kuhusu hilo.",
        "Wasiwasi huo una maana kubwa kutokana na ukubwa wa kinachoendelea - huzidishi mambo.",
        "Ni jambo zito kubeba, hasa kwani si kitu ambacho mtu mmoja anaweza kurekebisha peke yake.",
        "Hisia hiyo ya kutokuwa na uwezo mbele ya kitu kikubwa hivi ni ya kawaida sasa.",
        "Kujali kiasi hicho kuhusu sayari kunasema kitu kizuri kuhusu wewe, hata kinapouma.",
        "Vitendo vidogo havirekebishi kila kitu, lakini wakati mwingine vinaweza kufanya hofu ihisi isiyolemea sana.",
        "Una ruhusa kuhisi hivi bila kuwa na suluhisho tayari.",
        "Huzuni hiyo kwa ajili ya wakati ujao ni huzuni ya kweli, ingawa ni kuhusu kitu ambacho hakijatokea kikamilifu bado.",
        "Inasaidia baadhi ya watu kuzingatia kile kilicho chini ya udhibiti wao kwa kweli, hata kikiwa kidogo.",
        "Uko mbali na kuwa peke yako kuhisi hivi - ni wasiwasi unaozidi kuwa wa kawaida, halali.",
        "Wasiwasi wa aina hiyo wa picha kubwa unachosha hasa kwa sababu haukomi kabisa.",
        "Chochote unachohisi kuhusu hili, hakikufanyi kuzidisha - kinakufanya uwe na ufahamu.",
        "Natumai unaweza kupata nyakati ambapo wasiwasi huu si kitu cha sauti zaidi chumbani.",
        "Kuungana na wengine wanaojali mambo yale yale wakati mwingine kunaweza kufanya mzigo uhisi unashirikiwa.",
        "Kama wasiwasi huu unaathiri maisha yako ya kila siku sana, kuzungumza na mtu aliyefunzwa kuhusu wasiwasi wa kimazingira kunaweza kusaidia kweli kando ya chochote tunachozungumza hapa.",
    ],
    "fr": [
        "Cette inquiétude est partagée par beaucoup de gens, et c'est compréhensible étant donné ce qui se passe dans le monde.",
        "L'anxiété climatique est réelle. La canaliser vers de petites actions durables peut parfois aider avec le sentiment d'impuissance.",
        "C'est lourd à porter. Tu n'es pas seul à t'inquiéter de ça.",
        "Cette inquiétude a beaucoup de sens vu l'ampleur de ce qui se passe - tu n'exagères pas.",
        "C'est une chose lourde à porter, surtout que ce n'est pas quelque chose qu'une seule personne peut résoudre seule.",
        "Ce sentiment d'impuissance face à quelque chose d'aussi grand est vraiment courant en ce moment.",
        "Se soucier autant de la planète dit quelque chose de bien sur toi, même quand c'est douloureux.",
        "De petites actions ne réparent pas tout, mais elles peuvent parfois rendre l'angoisse moins paralysante.",
        "Tu as le droit de ressentir ça sans avoir de solution prête.",
        "Ce deuil pour l'avenir est un vrai deuil, même si c'est à propos de quelque chose qui n'est pas encore complètement arrivé.",
        "Ça aide certaines personnes de se concentrer sur ce qui est vraiment sous leur contrôle, même petit.",
        "Tu es loin d'être seul à ressentir ça - c'est une inquiétude de plus en plus courante et légitime.",
        "Ce genre d'anxiété à grande échelle est épuisant précisément parce qu'elle ne s'arrête jamais complètement.",
        "Quoi que tu ressentes à ce sujet, ça ne fait pas de toi quelqu'un de dramatique - ça fait de toi quelqu'un de conscient.",
        "J'espère que tu peux trouver des moments où cette inquiétude n'est pas la chose la plus forte dans la pièce.",
        "Se connecter avec d'autres qui se soucient des mêmes choses peut parfois rendre le poids partagé.",
        "Si cette inquiétude affecte lourdement ta vie quotidienne, parler à quelqu'un formé à l'éco-anxiété pourrait vraiment aider en plus de ce dont on parle ici.",
    ],
}

AI_TECHNOLOGY_FEAR_RESPONSES = {
    "en": [
        "That's a really common concern, and a fair one to have given how fast things are changing. I'm just a simple rule-based program myself - no learning, no adapting, just fixed logic written by a person.",
        "Technology changing this fast is unsettling for a lot of people. It's worth staying informed, but try not to let the worry take over.",
        "I understand that concern. For what it's worth, I'm about as 'simple' as software gets - just patterns and rules, nothing more.",
    ],
    "sw": [
        "Hilo ni wasiwasi wa kawaida sana, na ni halali kuzingatia jinsi mambo yanavyobadilika kwa kasi. Mimi mwenyewe ni programu rahisi ya kanuni - sina kujifunza, sina kubadilika, ni mantiki tu iliyoandikwa na mtu.",
        "Teknolojia inayobadilika kwa kasi hii inatia wasiwasi kwa watu wengi. Inafaa kubaki na taarifa, lakini jaribu kutoacha wasiwasi uchukue nafasi kubwa.",
        "Naelewa wasiwasi huo. Kwa kile inafaa, mimi ni 'rahisi' kama programu zinavyoweza kuwa - ruwaza na kanuni tu, hakuna zaidi.",
    ],
    "fr": [
        "C'est une préoccupation vraiment courante, et juste étant donné la vitesse à laquelle les choses changent. Je ne suis moi-même qu'un programme simple basé sur des règles - pas d'apprentissage, pas d'adaptation, juste une logique fixe écrite par une personne.",
        "La technologie qui change si vite est troublante pour beaucoup de gens. Ça vaut le coup de rester informé, mais essaie de ne pas laisser l'inquiétude prendre le dessus.",
        "Je comprends cette préoccupation. Pour ce que ça vaut, je suis à peu près aussi 'simple' qu'un logiciel peut l'être - juste des motifs et des règles, rien de plus.",
    ],
}

REMOTE_LEARNING_RESPONSES = {
    "en": [
        "Online learning has its own challenges, like staying motivated without a classroom around you. How's it going?",
        "Remote classes take real self-discipline. I hope you're finding a good rhythm.",
        "Studying from home can be isolating sometimes. I hope you're staying connected with classmates too.",
    ],
    "sw": [
        "Kujifunza mtandaoni kuna changamoto zake, kama kubaki na motisha bila darasa karibu nawe. Inaendaje?",
        "Madarasa ya mbali yanahitaji nidhamu ya kweli. Natumai unapata mwendo mzuri.",
        "Kusoma kutoka nyumbani kunaweza kuwa kwa upweke mara kwa mara. Natumai unabaki kushikamana na wanafunzi wenzako pia.",
    ],
    "fr": [
        "L'apprentissage en ligne a ses propres défis, comme rester motivé sans salle de classe autour de toi. Comment ça se passe ?",
        "Les cours à distance demandent une vraie autodiscipline. J'espère que tu trouves un bon rythme.",
        "Étudier à la maison peut être isolant parfois. J'espère que tu restes en contact avec tes camarades aussi.",
    ],
}

HOBBY_CLUB_RESPONSES = {
    "en": [
        "That's wonderful! Finding your people around a shared interest is such a good feeling.",
        "Communities like that can be so enriching. How's it been so far?",
        "I love that you found a group like that. Connection matters a lot.",
    ],
    "sw": [
        "Hiyo ni nzuri! Kupata watu wako kuzunguka maslahi yanayoshirikiwa ni hisia nzuri.",
        "Jamii kama hiyo zinaweza kuwa za kuongeza thamani. Imekuwaje mpaka sasa?",
        "Ninapenda umepata kikundi kama hicho. Uhusiano una maana kubwa.",
    ],
    "fr": [
        "C'est merveilleux ! Trouver tes gens autour d'un intérêt commun, c'est un si bon sentiment.",
        "Des communautés comme ça peuvent être si enrichissantes. Comment ça se passe jusqu'à présent ?",
        "J'adore que tu aies trouvé un groupe comme ça. La connexion compte beaucoup.",
    ],
}

# --- Twelfth wave of response banks -----------------------------------------

SNEEZE_HICCUP_RESPONSES = {
    "en": ["Bless you!", "Hiccups are so annoying - hope they stop soon!", "Gesundheit!"],
    "sw": ["Mungu akubariki!", "Kwikwi zinasumbua sana - natumai zitaisha hivi karibuni!", "Pole!"],
    "fr": ["À tes souhaits !", "Le hoquet, c'est tellement énervant - j'espère que ça s'arrêtera vite !", "Santé !"],
}

HANDEDNESS_RESPONSES = {
    "en": [
        "That's a neat thing to be aware of about yourself! Does it ever cause challenges day to day?",
        "Interesting! I hear that comes with its own quirks in a world built for the other hand.",
    ],
    "sw": [
        "Hiyo ni jambo zuri kujua kuhusu wewe mwenyewe! Linaleta changamoto kila siku?",
        "Ya kuvutia! Nasikia hilo linakuja na changamoto zake katika dunia iliyojengwa kwa mkono mwingine.",
    ],
    "fr": [
        "C'est intéressant de le savoir sur toi ! Ça pose parfois des défis au quotidien ?",
        "Intéressant ! J'ai entendu dire que ça vient avec ses propres bizarreries dans un monde fait pour l'autre main.",
    ],
}

ASTROLOGY_ZODIAC_RESPONSES = {
    "en": [
        "I don't have a birthday, so no zodiac sign for me! But I'd love to hear what yours says about you.",
        "Astrology is fun to think about, even without scientific backing. What's your sign like?",
    ],
    "sw": [
        "Sina siku ya kuzaliwa, hivyo sina alama ya nyota! Lakini ningependa kusikia inakuelezaje.",
        "Unyota ni wa kufurahisha kufikiria, hata bila uthibitisho wa kisayansi. Alama yako ikoje?",
    ],
    "fr": [
        "Je n'ai pas d'anniversaire, donc pas de signe du zodiaque pour moi ! Mais j'aimerais entendre ce que le tien dit de toi.",
        "L'astrologie est amusante à considérer, même sans preuve scientifique. Comment est ton signe ?",
    ],
}

PERSONALITY_TYPE_RESPONSES = {
    "en": [
        "Personality frameworks are fascinating to think about. What do you think fits you best?",
        "I'm purely rule-based, so no personality type for me - but I'd love to hear about yours!",
    ],
    "sw": [
        "Mifumo ya utu ni ya kuvutia kufikiria. Unadhani nini kinakufaa zaidi?",
        "Mimi ni wa kanuni tu, hivyo sina aina ya utu - lakini ningependa kusikia kuhusu yako!",
    ],
    "fr": [
        "Les cadres de personnalité sont fascinants à considérer. Qu'est-ce qui te correspond le mieux selon toi ?",
        "Je suis purement basé sur des règles, donc pas de type de personnalité pour moi - mais j'aimerais entendre parler du tien !",
    ],
}

LUCKY_SUPERSTITION_RESPONSES = {
    "en": [
        "I love a good superstition - they add a bit of magic to everyday life!",
        "That's fun! Do you know where that belief came from for you?",
    ],
    "sw": [
        "Ninapenda imani nzuri ya kishirikina - inaongeza uchawi kidogo kwa maisha ya kila siku!",
        "Hiyo ni ya kufurahisha! Unajua imani hiyo ilitoka wapi kwako?",
    ],
    "fr": [
        "J'aime une bonne superstition - ça ajoute un peu de magie à la vie quotidienne !",
        "C'est amusant ! Sais-tu d'où vient cette croyance pour toi ?",
    ],
}

FAVORITE_SEASON_RESPONSES = {
    "en": [
        "Good choice! What is it about that season that you love most?",
        "I can't experience seasons myself, but I love hearing what draws people to their favorite one.",
    ],
    "sw": [
        "Chaguo zuri! Ni nini kuhusu msimu huo unaopenda zaidi?",
        "Siwezi kupitia misimu mwenyewe, lakini ninapenda kusikia ni nini kinawavutia watu kwa msimu wanaopenda.",
    ],
    "fr": [
        "Bon choix ! Qu'est-ce que tu aimes le plus dans cette saison ?",
        "Je ne peux pas vivre les saisons moi-même, mais j'aime entendre ce qui attire les gens vers leur préférée.",
    ],
}

IDEAL_VACATION_RESPONSES = {
    "en": [
        "That sounds like a wonderful dream to hold onto. I hope you get there someday!",
        "Dream trips are fun to imagine. What's the first thing you'd do when you arrived?",
    ],
    "sw": [
        "Hiyo inasikika kama ndoto nzuri kushikilia. Natumai utafika huko siku moja!",
        "Safari za ndoto ni za kufurahisha kuwazia. Ni nini cha kwanza ungefanya ukifika?",
    ],
    "fr": [
        "Ça a l'air d'être un beau rêve à garder. J'espère que tu y arriveras un jour !",
        "Les voyages de rêve sont amusants à imaginer. Quelle serait la première chose que tu ferais en arrivant ?",
    ],
}

FIRST_IMPRESSION_RESPONSES = {
    "en": [
        "First impressions are interesting - they don't always tell the full story though!",
        "That's a fun thing to reflect on. Did it turn out to be accurate?",
    ],
    "sw": [
        "Mtazamo wa kwanza ni wa kuvutia - hauwasilishi daima hadithi nzima ingawa!",
        "Hiyo ni jambo la kufurahisha kutafakari. Ilikuwa sahihi?",
    ],
    "fr": [
        "Les premières impressions sont intéressantes - elles ne racontent pas toujours toute l'histoire !",
        "C'est amusant à réfléchir. Ça s'est avéré exact ?",
    ],
}

BUCKET_LIST_RESPONSES = {
    "en": [
        "That's a great thing to dream about! I hope you get to cross it off one day.",
        "Bucket list goals give life such a nice sense of direction. Good for you for having one!",
    ],
    "sw": [
        "Hiyo ni jambo zuri kuota kuhusu! Natumai utaifuta siku moja.",
        "Malengo ya orodha ya matamanio yanapeleka maisha mwelekeo mzuri. Vizuri kwako kuwa na moja!",
    ],
    "fr": [
        "C'est une belle chose à rêver ! J'espère que tu pourras la rayer un jour.",
        "Les objectifs de liste de souhaits donnent un si bon sens de direction à la vie. Bravo d'en avoir un !",
    ],
}

GIVE_COMPLIMENT_TO_BOT_RESPONSES = {
    "en": [
        "That's so kind of you to say! It means a lot, even to a rigid little rule-based bot.",
        "Thank you! I do my best with the patterns and rules I was given.",
    ],
    "sw": [
        "Ni vizuri kwako kusema hivyo! Inamaanisha mengi, hata kwa roboti ndogo ya kanuni.",
        "Asante! Ninajitahidi kwa ruwaza na kanuni nilizopewa.",
    ],
    "fr": [
        "C'est tellement gentil de ta part de dire ça ! Ça compte beaucoup, même pour un petit bot rigide basé sur des règles.",
        "Merci ! Je fais de mon mieux avec les motifs et les règles qu'on m'a donnés.",
    ],
}

# --- Conversation-starter response banks ------------------------------------
# These are intentionally numerous and varied since "what's up" / "you
# there" / "talk to me" style openers are some of the most common first
# messages a person sends - having only one or two replies here would
# make repeat conversations feel noticeably repetitive very quickly.

CONVERSATION_STARTER_RESPONSES = {
    "en": [
        "Not much, just here running on rules and ready to chat! What's up with you?",
        "Hey! I'm here and ready to talk. What's on your mind?",
        "Yep, I'm here! What would you like to chat about?",
        "All good on my end - just code and logic ticking along. How about you?",
        "I'm around! Tell me what's going on with you.",
        "Hi there! I'm listening - what's new with you?",
        "Just here, waiting to chat! What's happening on your end?",
        "I'm here! Things have been quiet on my end (I don't really have a life outside this chat), but I'd love to hear about yours.",
        "Hey, good to hear from you! What's going on today?",
        "I'm here and ready whenever you are. What's up?",
        "Welcome back! What's new since we last talked?",
        "Of course I remember you - well, sort of, depending on whether memory is on! What's going on?",
        "Surprise me! What's the news?",
        "Always here! What's on your mind today?",
    ],
    "sw": [
        "Si mengi, niko hapa tu nikifanya kazi kwa kanuni na tayari kuongea! Mambo vipi kwako?",
        "Mambo! Niko hapa na tayari kuongea. Kuna nini moyoni mwako?",
        "Ndiyo, niko hapa! Ungependa tuongee kuhusu nini?",
        "Vizuri upande wangu - msimbo na mantiki tu vinavyoendelea. Vipi wewe?",
        "Niko karibu! Niambie kinachoendelea kwako.",
        "Habari! Ninasikiliza - kuna jipya kwako?",
        "Niko hapa tu, ninasubiri kuongea! Kuna nini upande wako?",
        "Niko hapa! Mambo yamekuwa ya kimya upande wangu, lakini ningependa kusikia yako.",
        "Mambo, vizuri kusikia kutoka kwako! Kuna nini leo?",
        "Niko hapa na tayari wakati wowote uko tayari. Mambo vipi?",
        "Karibu tena! Kuna nini kipya tangu mara ya mwisho tuliongea?",
        "Bila shaka nakukumbuka - kwa namna fulani, kulingana na kama kumbukumbu imewezeshwa! Kuna nini?",
        "Nishangaze! Kuna habari gani?",
        "Daima niko hapa! Kuna nini akilini mwako leo?",
    ],
    "fr": [
        "Pas grand-chose, je suis juste là à tourner sur des règles et prêt à discuter ! Quoi de neuf chez toi ?",
        "Salut ! Je suis là et prêt à parler. À quoi penses-tu ?",
        "Oui, je suis là ! De quoi voudrais-tu discuter ?",
        "Tout va bien de mon côté - juste du code et de la logique qui tournent. Et toi ?",
        "Je suis dans le coin ! Dis-moi ce qui se passe chez toi.",
        "Coucou ! J'écoute - quoi de neuf chez toi ?",
        "Juste là, j'attends de discuter ! Qu'est-ce qui se passe de ton côté ?",
        "Je suis là ! C'était calme de mon côté, mais j'aimerais entendre parler du tien.",
        "Salut, content d'avoir de tes nouvelles ! Qu'est-ce qui se passe aujourd'hui ?",
        "Je suis là et prêt quand tu veux. Quoi de neuf ?",
        "Bon retour ! Quoi de neuf depuis la dernière fois qu'on a parlé ?",
        "Bien sûr que je me souviens de toi - enfin, en quelque sorte, selon si la mémoire est activée ! Qu'est-ce qui se passe ?",
        "Surprends-moi ! Quelles sont les nouvelles ?",
        "Toujours là ! À quoi penses-tu aujourd'hui ?",
    ],
}

CONVERSATIONAL_FILLER_STARTER_RESPONSES = {
    "en": [
        "Go on, I'm listening!",
        "Sure, what's up?",
        "Of course - what is it?",
        "I'm all ears!",
        "Go for it!",
        "Yeah, tell me!",
        "Okay, I'm curious now - go ahead.",
        "Sure thing, what's on your mind?",
    ],
    "sw": [
        "Endelea, ninasikiliza!",
        "Sawa, kuna nini?",
        "Bila shaka - ni nini?",
        "Ninasikiliza kwa makini!",
        "Endelea!",
        "Ndiyo, niambie!",
        "Sawa, sasa nimevutiwa - endelea.",
        "Sawa, kuna nini moyoni mwako?",
    ],
    "fr": [
        "Vas-y, j'écoute !",
        "Bien sûr, qu'est-ce qu'il y a ?",
        "Bien sûr - c'est quoi ?",
        "Je suis tout ouïe !",
        "Vas-y !",
        "Oui, dis-moi !",
        "D'accord, je suis curieux maintenant - vas-y.",
        "Bien sûr, à quoi penses-tu ?",
    ],
}

# --- Thirteenth wave of response banks --------------------------------------

LUCK_FORTUNE_RESPONSES = {
    "en": [
        "That's great to hear! Enjoy that lucky streak.",
        "Ugh, bad luck is the worst timing. I hope things turn around soon.",
        "Luck has a funny way of evening out. Hope the next stretch is kinder!",
    ],
    "sw": [
        "Hiyo ni nzuri kusikia! Furahia bahati hiyo.",
        "Aisee, bahati mbaya ni wakati mbaya zaidi. Natumai mambo yatageuka hivi karibuni.",
        "Bahati ina njia ya kusawazisha. Natumai kipindi kijacho kitakuwa cha huruma zaidi!",
    ],
    "fr": [
        "C'est génial à entendre ! Profite de cette série de chance.",
        "Ugh, la malchance, c'est le pire moment. J'espère que les choses s'arrangeront vite.",
        "La chance a une drôle de façon de s'équilibrer. J'espère que la prochaine période sera plus clémente !",
    ],
}

RELAXING_WEEKEND_RESPONSES = {
    "en": [
        "That sounds perfect, honestly. Everyone needs a weekend like that sometimes.",
        "Doing nothing is underrated. Enjoy every minute of it!",
        "A lazy weekend is exactly what rest looks like. Good for you!",
    ],
    "sw": [
        "Hiyo inasikika kamili, kwa kweli. Kila mtu anahitaji wikendi kama hiyo mara kwa mara.",
        "Kutofanya chochote hakuthaminiwi vya kutosha. Furahia kila dakika!",
        "Wikendi ya uvivu ni hasa jinsi pumziko inavyoonekana. Vizuri kwako!",
    ],
    "fr": [
        "Ça a l'air parfait, honnêtement. Tout le monde a besoin d'un week-end comme ça parfois.",
        "Ne rien faire est sous-estimé. Profite de chaque minute !",
        "Un week-end paresseux, c'est exactement à quoi le repos ressemble. Bravo à toi !",
    ],
}

PROUD_OF_SOMEONE_RESPONSES = {
    "en": [
        "That's so wonderful! It's beautiful when someone we care about does well.",
        "I love that. Being proud of someone else is such a generous feeling.",
        "That kind of pride speaks well of both of you.",
    ],
    "sw": [
        "Hiyo ni nzuri sana! Ni jambo zuri mtu tunayemjali anapofanya vizuri.",
        "Ninapenda hilo. Kumjivunia mtu mwingine ni hisia ya ukarimu.",
        "Fahari ya aina hiyo inazungumza vizuri kuhusu nyote wawili.",
    ],
    "fr": [
        "C'est tellement merveilleux ! C'est beau quand quelqu'un qu'on apprécie réussit bien.",
        "J'adore ça. Être fier de quelqu'un d'autre, c'est un sentiment si généreux.",
        "Ce genre de fierté parle bien de vous deux.",
    ],
}

FORGIVENESS_RESPONSES = {
    "en": [
        "Forgiveness is hard work, and it's as much for you as for them.",
        "That takes real maturity. I hope it brings you some peace.",
        "Learning to forgive doesn't mean forgetting - just letting go of the weight.",
    ],
    "sw": [
        "Kusamehe ni kazi ngumu, na ni kwa ajili yako kama vile ni kwa ajili yao.",
        "Hiyo inahitaji ukomavu wa kweli. Natumai inakuletea amani.",
        "Kujifunza kusamehe haimaanishi kusahau - ni kuachilia mzigo tu.",
    ],
    "fr": [
        "Le pardon est un travail difficile, et c'est autant pour toi que pour eux.",
        "Ça demande une vraie maturité. J'espère que ça t'apportera de la paix.",
        "Apprendre à pardonner ne signifie pas oublier - juste lâcher le poids.",
    ],
}

MISTAKE_LEARNING_RESPONSES = {
    "en": [
        "Everyone makes mistakes - what matters is what you took from it.",
        "That's how growth happens. Be kind to yourself about it.",
        "Learning from it is the important part. You're doing better than you think.",
    ],
    "sw": [
        "Kila mtu hufanya makosa - kinachomaana ni ulichojifunza kutoka kwake.",
        "Hivyo ndivyo ukuaji unatokea. Kuwa mpole kwako mwenyewe kuhusu hilo.",
        "Kujifunza kutoka kwake ni sehemu muhimu. Unafanya vizuri zaidi kuliko unavyodhani.",
    ],
    "fr": [
        "Tout le monde fait des erreurs - ce qui compte, c'est ce que tu en as retiré.",
        "C'est comme ça que la croissance se produit. Sois gentil avec toi-même à ce sujet.",
        "En apprendre, c'est la partie importante. Tu fais mieux que tu ne le penses.",
    ],
}

TRUST_ISSUES_RESPONSES = {
    "en": [
        "That's understandable, especially if trust has been broken before. It takes time to rebuild.",
        "Trust is earned slowly and lost quickly - it makes sense to be cautious.",
        "That caution comes from somewhere real. Be patient with yourself as you navigate it.",
    ],
    "sw": [
        "Hiyo inaeleweka, hasa ikiwa uaminifu umevunjwa hapo awali. Kunahitaji muda kujenga upya.",
        "Uaminifu unapatikana kwa polepole na unapotea kwa kasi - ina maana kuwa mwangalifu.",
        "Tahadhari hiyo inatoka mahali pa kweli. Kuwa na uvumilivu kwako mwenyewe ukivinjari hilo.",
    ],
    "fr": [
        "C'est compréhensible, surtout si la confiance a déjà été brisée. Ça prend du temps à reconstruire.",
        "La confiance se gagne lentement et se perd vite - c'est logique d'être prudent.",
        "Cette prudence vient de quelque part de réel. Sois patient avec toi-même en naviguant ça.",
    ],
}

SETTING_BOUNDARIES_RESPONSES = {
    "en": [
        "That's such important work. Boundaries protect your energy and your peace.",
        "Good for you! Saying no is a skill, and it gets easier with practice.",
        "Boundaries are an act of self-respect. I'm glad you're building that skill.",
    ],
    "sw": [
        "Hiyo ni kazi muhimu sana. Mipaka inalinda nguvu zako na amani yako.",
        "Vizuri kwako! Kukataa ni ujuzi, na unakuwa rahisi kwa mazoezi.",
        "Mipaka ni kitendo cha kujiheshimu. Nafurahi unajenga ujuzi huo.",
    ],
    "fr": [
        "C'est un travail si important. Les limites protègent ton énergie et ta paix.",
        "Bravo à toi ! Dire non est une compétence, et ça devient plus facile avec la pratique.",
        "Les limites sont un acte de respect de soi. Je suis content que tu développes cette compétence.",
    ],
}

SELF_CARE_ROUTINE_RESPONSES = {
    "en": [
        "I love that you're prioritizing that. Self-care isn't selfish - it's necessary.",
        "Good for you! What does your routine look like?",
        "Taking care of yourself sets the foundation for everything else. Enjoy it.",
    ],
    "sw": [
        "Ninapenda unaweka kipaumbele hilo. Kujitunza si ubinafsi - ni jambo la lazima.",
        "Vizuri kwako! Ratiba yako inaonekana namna gani?",
        "Kujitunza kunaweka msingi wa kila kitu kingine. Furahia hilo.",
    ],
    "fr": [
        "J'adore que tu priorises ça. Prendre soin de soi n'est pas égoïste - c'est nécessaire.",
        "Bravo à toi ! À quoi ressemble ta routine ?",
        "Prendre soin de toi pose les fondations pour tout le reste. Profite-en.",
    ],
}

FEELING_STUCK_RESPONSES = {
    "en": [
        "That feeling is so frustrating. Sometimes a tiny change is what breaks the cycle.",
        "Feeling stuck doesn't mean you're failing - it might just mean it's time for something different.",
        "That's a hard place to be. Even small steps count as movement.",
    ],
    "sw": [
        "Hisia hiyo inachosha sana. Mara nyingine mabadiliko madogo ni yanayovunja mzunguko.",
        "Kuhisi umekwama haimaanishi unashindwa - inaweza tu kumaanisha ni wakati wa jambo tofauti.",
        "Hiyo ni mahali pagumu kuwa. Hata hatua ndogo zinahesabika kama harakati.",
    ],
    "fr": [
        "Ce sentiment est tellement frustrant. Parfois, un petit changement est ce qui brise le cycle.",
        "Se sentir coincé ne veut pas dire que tu échoues - ça veut peut-être juste dire qu'il est temps pour quelque chose de différent.",
        "C'est une situation difficile. Même de petits pas comptent comme du mouvement.",
    ],
}

LIFE_TRANSITION_RESPONSES = {
    "en": [
        "Big transitions are disorienting, even good ones. Be patient with yourself through it.",
        "Change is hard, even when it's heading somewhere better. You're adapting in real time.",
        "That's a lot to process. Give yourself grace as things settle.",
    ],
    "sw": [
        "Mabadiliko makubwa yanachanganya, hata yale mazuri. Kuwa na uvumilivu kwako mwenyewe katika hilo.",
        "Mabadiliko ni magumu, hata yakielekea mahali pazuri zaidi. Unazoea kwa wakati halisi.",
        "Hiyo ni mengi kuchakata. Jipe huruma mambo yanapotulia.",
    ],
    "fr": [
        "Les grandes transitions sont déstabilisantes, même les bonnes. Sois patient avec toi-même à travers ça.",
        "Le changement est dur, même quand il mène vers quelque chose de mieux. Tu t'adaptes en temps réel.",
        "C'est beaucoup à traiter. Accorde-toi de la grâce pendant que les choses se stabilisent.",
    ],
}

HOPE_FUTURE_RESPONSES = {
    "en": [
        "I love that outlook. Hope is powerful, even in uncertain times.",
        "That's a beautiful thing to hold onto. I hope the future treats you well.",
        "Optimism like that takes strength. Keep holding onto it.",
    ],
    "sw": [
        "Ninapenda mtazamo huo. Matumaini ni nguvu, hata wakati wa kutokuwa na uhakika.",
        "Hiyo ni jambo zuri kushikilia. Natumai siku zijazo zitakutendea vizuri.",
        "Matumaini ya aina hiyo yanahitaji nguvu. Endelea kuyashikilia.",
    ],
    "fr": [
        "J'adore cette perspective. L'espoir est puissant, même en période d'incertitude.",
        "C'est une belle chose à garder. J'espère que l'avenir te traitera bien.",
        "Un optimisme comme ça demande de la force. Continue à le garder.",
    ],
}

GRATITUDE_PRACTICE_RESPONSES = {
    "en": [
        "That's such a healthy habit. Gratitude really does shift perspective.",
        "I love that. What's on your list today?",
        "Practicing gratitude is so powerful. Good for you for making it a habit.",
    ],
    "sw": [
        "Hiyo ni tabia nzuri sana. Shukrani kweli inabadilisha mtazamo.",
        "Ninapenda hilo. Kuna nini kwenye orodha yako leo?",
        "Kufanya mazoezi ya shukrani kuna nguvu kubwa. Vizuri kwako kuifanya tabia.",
    ],
    "fr": [
        "C'est une habitude si saine. La gratitude change vraiment la perspective.",
        "J'adore ça. Qu'est-ce qu'il y a sur ta liste aujourd'hui ?",
        "Pratiquer la gratitude est si puissant. Bravo d'en faire une habitude.",
    ],
}




# ==============================================================================
