"""10 real trained models: intent/sentiment classifiers, suggestion engine, mood forecaster, semantic memory (Sections 6G,6H,6H2,6H3), plus urgency/politeness/question-type/text-complexity/emoji networks (Section 6H4, in 32_deep_networks.py)
Auto-split from the original single-file chatbot.py - see main.py for load order.
"""

# SECTION 6G: NEURAL NETWORKS (real PyTorch models, sklearn fallback)
# ==============================================================================
#
# This section holds TWO genuinely trained neural networks:
#
#   1. NeuralIntentClassifier - classifies free-form user text into an
#      intent (both ordinary conversation and bot commands).
#   2. SentimentClassifier - classifies free-form user text into a
#      coarse mood (positive / negative / neutral), used to make the
#      bot's tone adapt to how the user seems to be feeling.
#
# Both follow the same backend strategy:
#   - If PyTorch is installed, build and train a hand-written nn.Module
#     with a learned nn.Embedding layer (NOT TF-IDF) so the network can
#     generalize across semantically similar words it wasn't shown in
#     that exact combination, mean-pooling token embeddings into a
#     sentence vector, then passing that through BatchNorm1d, GELU,
#     Dropout, and Linear layers, trained with Adam + a StepLR
#     scheduler, an explicit train/validation split, and early stopping
#     on validation accuracy.
#   - If PyTorch is NOT installed, fall back automatically to
#     scikit-learn's MLPClassifier over TF-IDF features - a different
#     (sparser) feature representation, but still a real backprop
#     network, so nothing crashes and the feature still works.
#
# Both classifiers report real held-out validation accuracy after every
# fit - not just "trained on N examples" - so confidence claims are
# backed by an actual evaluation, not vibes.
#
# Online learning is from USER-VERIFIED corrections only (see
# add_correction/retrain) - never from the model's own predictions,
# which would let confidently-wrong guesses compound with no ground
# truth to correct them.

# ---- Intent classifier training data (see disambiguation notes below) -----
#
# Every class has at least 6 examples (most have 7-14): with only ~2-3
# examples per class, a held-out validation split is nearly meaningless
# (a class's only example can land entirely in validation with nothing
# to learn it from), so the original ~100-example set was expanded to
# ~260 examples with extra disambiguating phrasings for the pairs that
# were empirically confused in testing (greeting/farewell/how_are_you,
# the four feelings_* classes, and the joke/quote/riddle/story quartet).
NN_INTENT_EXAMPLES = [
    # --- greeting ---
    ("hello", "greeting"),
    ("hi there", "greeting"),
    ("hey", "greeting"),
    ("good morning", "greeting"),
    ("good evening", "greeting"),
    ("yo what's up", "greeting"),
    ("hiya", "greeting"),
    ("howdy", "greeting"),
    ("greetings", "greeting"),
    ("hey there how's it going", "greeting"),
    ("good afternoon", "greeting"),
    ("what's good", "greeting"),
    ("hello there friend", "greeting"),
    ("hey i'm back", "greeting"),
    ("hi, it's me again", "greeting"),
    ("hey hey", "greeting"),
    ("oh hi", "greeting"),
    ("good to see you", "greeting"),
    ("hello hello", "greeting"),
    ("sup", "greeting"),
    ("hey, what's happening", "greeting"),
    ("good day to you", "greeting"),
    ("hi, how's everything", "greeting"),
    ("yo", "greeting"),
    ("hi again", "greeting"),
    ("evening", "greeting"),

    # --- farewell ---
    ("bye", "farewell"),
    ("goodbye", "farewell"),
    ("see you later", "farewell"),
    ("talk to you soon", "farewell"),
    ("i'm heading out", "farewell"),
    ("gotta go now", "farewell"),
    ("catch you later", "farewell"),
    ("night night", "farewell"),
    ("see ya", "farewell"),
    ("i'm off, take care", "farewell"),
    ("alright i'm done for now", "farewell"),
    ("i have to go now, bye", "farewell"),
    ("signing off for tonight", "farewell"),
    ("okay, bye for now", "farewell"),
    ("that's all for today, goodbye", "farewell"),
    ("i'll talk to you later", "farewell"),
    ("time for me to go", "farewell"),
    ("until next time", "farewell"),
    ("logging off now", "farewell"),
    ("i'm done chatting for today", "farewell"),
    ("farewell for now", "farewell"),
    ("i'm exiting now, goodbye", "farewell"),
    ("see you next time", "farewell"),
    ("peace out", "farewell"),
    ("take care, bye", "farewell"),

    # --- thanks ---
    ("thanks a lot", "thanks"),
    ("thank you so much", "thanks"),
    ("appreciate it", "thanks"),
    ("thanks for the help", "thanks"),
    ("that's very kind of you", "thanks"),
    ("much appreciated", "thanks"),
    ("thanks a bunch", "thanks"),
    ("you're a lifesaver, thank you", "thanks"),
    ("i really appreciate your help", "thanks"),
    ("thank you, that helped a lot", "thanks"),
    ("you're the best, thanks", "thanks"),
    ("cheers for that", "thanks"),
    ("thanks so much for this", "thanks"),
    ("that was very helpful, thank you", "thanks"),
    ("i owe you one, thanks", "thanks"),
    ("appreciate the quick help", "thanks"),

    # --- how_are_you ---
    ("how are you", "how_are_you"),
    ("how are you doing", "how_are_you"),
    ("how's it going", "how_are_you"),
    ("how have you been", "how_are_you"),
    ("you alright", "how_are_you"),
    ("how do you feel today", "how_are_you"),
    ("are you doing okay", "how_are_you"),
    ("how's your day been", "how_are_you"),
    ("how's life treating you", "how_are_you"),
    ("everything good with you", "how_are_you"),
    ("how have things been lately", "how_are_you"),
    ("how was your day", "how_are_you"),
    ("you doing well today", "how_are_you"),
    ("hows everything going for you", "how_are_you"),
    ("how's everything been with you", "how_are_you"),
    ("are you having a good day", "how_are_you"),
    ("how's your week been going", "how_are_you"),
    ("how are things on your end", "how_are_you"),
    ("doing alright today", "how_are_you"),

    # --- feelings_happy ---
    ("i'm feeling great today", "feelings_happy"),
    ("i am so happy right now", "feelings_happy"),
    ("today has been amazing", "feelings_happy"),
    ("i feel wonderful", "feelings_happy"),
    ("i'm in such a good mood", "feelings_happy"),
    ("everything is going great for me", "feelings_happy"),
    ("i feel fantastic", "feelings_happy"),
    ("i'm overjoyed right now", "feelings_happy"),
    ("life is good today", "feelings_happy"),
    ("i'm on top of the world today", "feelings_happy"),
    ("i can't stop smiling today", "feelings_happy"),
    ("today turned out really great", "feelings_happy"),
    ("i'm in a really good mood right now", "feelings_happy"),
    ("things are going so well for me lately", "feelings_happy"),
    ("i feel really upbeat today", "feelings_happy"),
    ("i'm just really content right now", "feelings_happy"),
    ("i'm bursting with joy today", "feelings_happy"),
    ("i feel cheerful and bright today", "feelings_happy"),
    ("everything feels wonderful right now", "feelings_happy"),
    ("i'm delighted with how today went", "feelings_happy"),
    ("i feel so joyful and excited", "feelings_happy"),
    ("today has been a joyful, happy day", "feelings_happy"),

    # --- feelings_sad ---
    ("i'm feeling kind of down", "feelings_sad"),
    ("i am sad today", "feelings_sad"),
    ("not having a great day", "feelings_sad"),
    ("i feel pretty low right now", "feelings_sad"),
    ("today has been rough", "feelings_sad"),
    ("i'm feeling a bit blue", "feelings_sad"),
    ("things aren't going well for me", "feelings_sad"),
    ("i feel really upset today", "feelings_sad"),
    ("i'm heartbroken right now", "feelings_sad"),
    ("i've been feeling down lately", "feelings_sad"),
    ("i'm having a hard time today", "feelings_sad"),
    ("i feel kind of empty right now", "feelings_sad"),
    ("nothing has gone right for me today", "feelings_sad"),
    ("i'm struggling a bit emotionally today", "feelings_sad"),
    ("i just feel really down right now", "feelings_sad"),
    ("today's been a sad one for me", "feelings_sad"),
    ("i feel like crying right now", "feelings_sad"),
    ("i'm grieving and it hurts a lot", "feelings_sad"),
    ("i feel miserable and gloomy today", "feelings_sad"),
    ("i've been crying on and off today", "feelings_sad"),
    ("i feel so lonely and sad lately", "feelings_sad"),
    ("everything makes me want to cry today", "feelings_sad"),

    # --- feelings_tired ---
    ("i'm exhausted", "feelings_tired"),
    ("i'm so tired", "feelings_tired"),
    ("i barely slept last night", "feelings_tired"),
    ("i need a nap", "feelings_tired"),
    ("i'm running on no sleep", "feelings_tired"),
    ("i feel drained today", "feelings_tired"),
    ("i could really use some rest", "feelings_tired"),
    ("i'm completely worn out", "feelings_tired"),
    ("i can barely keep my eyes open", "feelings_tired"),
    ("i'm so sleepy right now", "feelings_tired"),
    ("i didn't get enough sleep last night", "feelings_tired"),
    ("i feel completely burned out today", "feelings_tired"),
    ("my energy is totally gone today", "feelings_tired"),
    ("i'm dragging today, so tired", "feelings_tired"),
    ("i need to lie down, i'm exhausted", "feelings_tired"),
    ("i'm yawning nonstop, so sleepy", "feelings_tired"),
    ("i could sleep for a whole week", "feelings_tired"),
    ("my eyelids feel so heavy right now", "feelings_tired"),
    ("i stayed up way too late and i'm groggy", "feelings_tired"),
    ("i'm sleep deprived and sluggish today", "feelings_tired"),
    ("all i want to do is sleep right now", "feelings_tired"),

    # --- weather_smalltalk ---
    ("what's the weather like", "weather_smalltalk"),
    ("is it sunny outside", "weather_smalltalk"),
    ("nice weather today", "weather_smalltalk"),
    ("is it raining out there", "weather_smalltalk"),
    ("how's the weather where you are", "weather_smalltalk"),
    ("it's pretty cold outside today", "weather_smalltalk"),
    ("is it windy today", "weather_smalltalk"),
    ("what's it like outside right now", "weather_smalltalk"),
    ("is it snowing where you are", "weather_smalltalk"),
    ("the weather has been crazy lately", "weather_smalltalk"),

    # --- bot_capabilities_joke ---
    ("are you an ai", "bot_capabilities_joke"),
    ("are you a robot", "bot_capabilities_joke"),
    ("what are you", "bot_capabilities_joke"),
    ("are you human", "bot_capabilities_joke"),
    ("are you a real person", "bot_capabilities_joke"),
    ("are you sentient", "bot_capabilities_joke"),
    ("are you actually intelligent", "bot_capabilities_joke"),
    ("do you have real feelings", "bot_capabilities_joke"),
    ("are you conscious", "bot_capabilities_joke"),
    ("are you alive", "bot_capabilities_joke"),
    ("can you actually think", "bot_capabilities_joke"),

    # --- ask_bot_name ---
    ("what's your name", "ask_bot_name"),
    ("who are you", "ask_bot_name"),
    ("do you have a name", "ask_bot_name"),
    ("what should i call you", "ask_bot_name"),
    ("tell me your name", "ask_bot_name"),
    ("what is this bot's name", "ask_bot_name"),
    ("what's your name again", "ask_bot_name"),
    ("do you go by a name", "ask_bot_name"),
    ("what's this assistant called", "ask_bot_name"),
    ("may i know your name", "ask_bot_name"),
    ("what should i refer to you as", "ask_bot_name"),
    ("could you tell me your name", "ask_bot_name"),
    ("what's the name of this chatbot", "ask_bot_name"),
    ("do you know your own name", "ask_bot_name"),
    ("what should i be calling you", "ask_bot_name"),

    # --- call_yourself ---
    ("call yourself max", "call_yourself"),
    ("i want to name you buddy", "call_yourself"),
    ("from now on your name is rex", "call_yourself"),
    ("i'm going to call you sam", "call_yourself"),
    ("your new name is nova", "call_yourself"),
    ("let's rename you to jarvis", "call_yourself"),
    ("i'm naming you charlie", "call_yourself"),
    ("from now on i'll call you pixel", "call_yourself"),
    ("your name is now zara", "call_yourself"),
    ("rename yourself to luna", "call_yourself"),
    ("change your name to felix", "call_yourself"),
    ("i'm renaming you to echo", "call_yourself"),
    ("from this point on you're called milo", "call_yourself"),
    ("please go by the name otto now", "call_yourself"),
    ("i'll be calling you ziggy from now on", "call_yourself"),
    ("let's call you robo", "call_yourself"),
    ("your assigned name is now atlas", "call_yourself"),
    ("i dub thee captain", "call_yourself"),
    ("starting now you'll be known as shadow", "call_yourself"),
    ("switch your name to comet", "call_yourself"),

    # --- ask_my_name ---
    ("what is my name", "ask_my_name"),
    ("do you remember my name", "ask_my_name"),
    ("what did i tell you my name was", "ask_my_name"),
    ("do you know who i am", "ask_my_name"),
    ("can you recall my name", "ask_my_name"),
    ("what name did i give you", "ask_my_name"),
    ("do you still remember my name", "ask_my_name"),
    ("did i tell you my name already", "ask_my_name"),
    ("what's my name again", "ask_my_name"),

    # --- remember_fact ---
    ("my favorite food is pizza", "remember_fact"),
    ("remember that my birthday is in june", "remember_fact"),
    ("my favorite color is blue", "remember_fact"),
    ("please remember that i have a dog named rex", "remember_fact"),
    ("my favorite movie is inception", "remember_fact"),
    ("remember this: i live in seattle", "remember_fact"),
    ("my favorite season is autumn", "remember_fact"),
    ("remember that i'm allergic to peanuts", "remember_fact"),
    ("my favorite sport is basketball", "remember_fact"),
    ("remember that my sister's name is mia", "remember_fact"),
    ("i work as a teacher, please remember that", "remember_fact"),

    # --- current_time ---
    ("what time is it right now", "current_time"),
    ("tell me the time", "current_time"),
    ("do you know what time it is", "current_time"),
    ("can you tell me the current time", "current_time"),
    ("what's the time right now", "current_time"),
    ("give me the time please", "current_time"),
    ("what time do you have", "current_time"),
    ("could you tell me what time it is", "current_time"),
    ("got the time", "current_time"),

    # --- current_date ---
    ("what is today's date", "current_date"),
    ("what's the date today", "current_date"),
    ("can you tell me today's date", "current_date"),
    ("what's today's date", "current_date"),
    ("do you know the date today", "current_date"),
    ("give me today's date", "current_date"),
    ("what date is it today", "current_date"),
    ("could you tell me the date", "current_date"),

    # --- days_until_holiday ---
    ("how many days until christmas", "days_until_holiday"),
    ("how many days left until new year", "days_until_holiday"),
    ("how long until halloween", "days_until_holiday"),
    ("how many days till my birthday", "days_until_holiday"),
    ("days remaining until thanksgiving", "days_until_holiday"),
    ("how far away is valentine's day", "days_until_holiday"),
    ("how many days until easter", "days_until_holiday"),
    ("how much longer until summer break", "days_until_holiday"),
    ("how many days are left until the new year", "days_until_holiday"),

    # --- days_between_dates ---
    ("how many days between these two dates", "days_between_dates"),
    ("what's the difference in days between january 1 and march 1", "days_between_dates"),
    ("how many days are between two specific dates", "days_between_dates"),
    ("calculate the days between 2024-01-01 and 2024-06-01", "days_between_dates"),
    ("how many days passed between those dates", "days_between_dates"),
    ("days between two dates please", "days_between_dates"),
    ("how many days separate these dates", "days_between_dates"),
    ("can you calculate the number of days between two dates", "days_between_dates"),

    # --- age_calculator ---
    ("how old would i be if i was born in 2000", "age_calculator"),
    ("calculate my age if i was born on a certain date", "age_calculator"),
    ("how old am i if my birthday is in 1995", "age_calculator"),
    ("figure out my age from my birth date", "age_calculator"),
    ("how many years old would someone born in 1990 be", "age_calculator"),
    ("what age would i be born in 2005", "age_calculator"),
    ("calculate someone's age from their birthdate", "age_calculator"),
    ("how old is someone born in 1988", "age_calculator"),

    # --- tell_story ---
    ("tell me an adventure story", "tell_story"),
    ("give me a story to read", "tell_story"),
    ("can you narrate a tale", "tell_story"),
    ("i want to hear a story", "tell_story"),
    ("tell me a mystery story", "tell_story"),
    ("got any good stories", "tell_story"),
    ("tell me a story about a dragon", "tell_story"),
    ("can you narrate a tale for me", "tell_story"),
    ("tell me a short story", "tell_story"),
    ("i'd love to hear a tale", "tell_story"),
    ("read me a story please", "tell_story"),
    ("got a sci-fi story for me", "tell_story"),

    # --- write_haiku ---
    ("write a haiku about the ocean", "write_haiku"),
    ("write me a haiku", "write_haiku"),
    ("can you compose a haiku", "write_haiku"),
    ("write a haiku about autumn", "write_haiku"),
    ("give me a haiku poem", "write_haiku"),
    ("haiku about the moon please", "write_haiku"),
    ("write a short haiku for me", "write_haiku"),
    ("can you write a haiku about rain", "write_haiku"),

    # --- write_acrostic ---
    ("write an acrostic poem for jordan", "write_acrostic"),
    ("can you make an acrostic poem with my name", "write_acrostic"),
    ("write an acrostic for the word ocean", "write_acrostic"),
    ("make me an acrostic poem", "write_acrostic"),
    ("acrostic poem using my name please", "write_acrostic"),
    ("compose an acrostic for friendship", "write_acrostic"),
    ("write an acrostic poem using the word hope", "write_acrostic"),

    # --- write_poem_general ---
    ("write a rhyming poem about love", "write_poem_general"),
    ("write me a poem", "write_poem_general"),
    ("can you write a poem about nature", "write_poem_general"),
    ("compose a short poem for me", "write_poem_general"),
    ("i'd like a poem about friendship", "write_poem_general"),
    ("write some poetry for me", "write_poem_general"),
    ("can you write a poem about the stars", "write_poem_general"),
    ("write a short poem about hope", "write_poem_general"),

    # --- simple_math ---
    ("what is 12 times 4", "simple_math"),
    ("calculate 9 plus 7", "simple_math"),
    ("what's 100 divided by 4", "simple_math"),
    ("can you do some quick math for me", "simple_math"),
    ("what's 15 minus 6", "simple_math"),
    ("solve 8 times 8", "simple_math"),
    ("what is 25 plus 17", "simple_math"),
    ("what's 7 times 9", "simple_math"),
    ("calculate 144 divided by 12", "simple_math"),
    ("what's 50 minus 23", "simple_math"),
    ("add 33 and 44 for me", "simple_math"),
    ("what is 6 squared", "simple_math"),
    ("multiply 12 by 11", "simple_math"),
    ("what's the square root of 81", "simple_math"),

    # --- tell_joke ---
    ("tell me a funny joke", "tell_joke"),
    ("make me laugh", "tell_joke"),
    ("tell me a joke", "tell_joke"),
    ("can you tell me a joke please", "tell_joke"),
    ("got any jokes", "tell_joke"),
    ("say something funny", "tell_joke"),
    ("i need a good laugh", "tell_joke"),
    ("do you know any funny jokes", "tell_joke"),
    ("crack a joke for me", "tell_joke"),
    ("tell me something hilarious", "tell_joke"),
    ("got a good one-liner for me", "tell_joke"),
    ("i'm bored, tell me a joke", "tell_joke"),

    # --- tell_quote ---
    ("tell me an inspirational quote", "tell_quote"),
    ("give me some wisdom", "tell_quote"),
    ("share an inspiring quote", "tell_quote"),
    ("i need some motivation, give me a quote", "tell_quote"),
    ("got a good quote for me", "tell_quote"),
    ("tell me something inspiring", "tell_quote"),
    ("share some words of wisdom", "tell_quote"),
    ("give me a motivational saying", "tell_quote"),
    ("i need an uplifting quote", "tell_quote"),
    ("share something thought-provoking", "tell_quote"),

    # --- tell_riddle ---
    ("give me a riddle to solve", "tell_riddle"),
    ("puzzle me with a brain teaser", "tell_riddle"),
    ("got a riddle for me", "tell_riddle"),
    ("i want to solve a riddle", "tell_riddle"),
    ("can you stump me with a riddle", "tell_riddle"),
    ("give me a tricky riddle", "tell_riddle"),
    ("challenge me with a riddle", "tell_riddle"),
    ("i feel like solving a puzzle", "tell_riddle"),
    ("hit me with a riddle", "tell_riddle"),
    ("got a brain teaser for me", "tell_riddle"),

    # --- tell_trivia ---
    ("ask me a trivia question", "tell_trivia"),
    ("quiz me on something", "tell_trivia"),
    ("test my knowledge with trivia", "tell_trivia"),
    ("got a trivia question for me", "tell_trivia"),
    ("i want to answer a trivia question", "tell_trivia"),
    ("give me something to quiz me on", "tell_trivia"),
    ("ask me something trivia related", "tell_trivia"),
    ("let's do a round of trivia", "tell_trivia"),

    # --- word_count_tool ---
    ("count the words in this sentence", "word_count_tool"),
    ("how many words are in this paragraph", "word_count_tool"),
    ("can you count the words for me", "word_count_tool"),
    ("word count for this text please", "word_count_tool"),
    ("how many words did i just type", "word_count_tool"),
    ("count words in the following text", "word_count_tool"),
    ("give me a word count for this", "word_count_tool"),

    # --- palindrome_check ---
    ("check if racecar is a palindrome", "palindrome_check"),
    ("is this word a palindrome", "palindrome_check"),
    ("can you tell if a word reads the same backwards", "palindrome_check"),
    ("palindrome check please", "palindrome_check"),
    ("does this word count as a palindrome", "palindrome_check"),
    ("verify if level is a palindrome", "palindrome_check"),
    ("is the word madam a palindrome", "palindrome_check"),

    # --- unit_convert ---
    ("convert 10 miles to kilometers", "unit_convert"),
    ("how many kilometers is 5 miles", "unit_convert"),
    ("convert pounds to kilograms for me", "unit_convert"),
    ("change 100 fahrenheit to celsius", "unit_convert"),
    ("how do i convert feet to meters", "unit_convert"),
    ("unit conversion please, miles to km", "unit_convert"),
    ("convert 50 kilograms to pounds", "unit_convert"),
    ("how many centimeters is 6 inches", "unit_convert"),
    ("convert 2 liters to gallons", "unit_convert"),
    ("how many ounces is 500 grams", "unit_convert"),
    ("change 30 celsius into fahrenheit", "unit_convert"),
    ("convert 20 yards to meters", "unit_convert"),

    # --- prime_check ---
    ("check if 17 is a prime number", "prime_check"),
    ("is 23 a prime number", "prime_check"),
    ("can you tell me if this number is prime", "prime_check"),
    ("verify whether 31 is prime", "prime_check"),
    ("prime number check please", "prime_check"),
    ("is 100 a prime number", "prime_check"),
    ("is 7 prime", "prime_check"),

    # --- number_to_words_tool ---
    ("spell out the number 1234", "number_to_words_tool"),
    ("write this number in words", "number_to_words_tool"),
    ("convert 567 into words", "number_to_words_tool"),
    ("how do you spell out 42 in english", "number_to_words_tool"),
    ("turn this number into written words", "number_to_words_tool"),
    ("number to words conversion please", "number_to_words_tool"),
    ("spell out 9999 for me", "number_to_words_tool"),

    # --- todo_add ---
    ("add buy milk to my to-do list", "todo_add"),
    ("remind me to call the dentist", "todo_add"),
    ("put grocery shopping on my list", "todo_add"),
    ("add finish homework to my tasks", "todo_add"),
    ("i need to remember to pay rent, add it", "todo_add"),
    ("can you add walk the dog to my to-do list", "todo_add"),
    ("put this on my to-do list: clean the garage", "todo_add"),
    ("add a new task to my list", "todo_add"),
    ("remind me to water the plants", "todo_add"),
    ("add schedule a dentist appointment to my list", "todo_add"),

    # --- todo_list ---
    ("show my to-do list", "todo_list"),
    ("what's on my to-do list", "todo_list"),
    ("can i see my tasks", "todo_list"),
    ("list everything on my to-do list", "todo_list"),
    ("what do i still need to do today", "todo_list"),
    ("pull up my to-do list please", "todo_list"),
    ("display my current tasks", "todo_list"),
    ("what's left on my list", "todo_list"),
    ("show me everything i still need to do", "todo_list"),

    # --- hangman_start ---
    ("let's play hangman", "hangman_start"),
    ("can we play a game of hangman", "hangman_start"),
    ("i want to play hangman", "hangman_start"),
    ("start a hangman game", "hangman_start"),
    ("hangman please", "hangman_start"),
    ("let's do hangman", "hangman_start"),
    ("can we start a round of hangman", "hangman_start"),

    # --- help ---
    ("show me the help menu", "help"),
    ("what can you do", "help"),
    ("what can i ask you", "help"),
    ("list your commands", "help"),
    ("what are all your features", "help"),
    ("how do i use this chatbot", "help"),
    ("show me your capabilities", "help"),
    ("what kinds of things can you help with", "help"),
    ("what commands do you support", "help"),
    ("give me a list of things you can do", "help"),
    ("show me a list of available commands", "help"),
    ("what functions do you have", "help"),
    ("i'm not sure what you can do, show me", "help"),
    ("pull up the help screen", "help"),
]

# ---- Auto-generated supplementary paraphrases -----------------------------
# Same idea as the hand-written examples above (more phrasings per class
# means a more meaningful train/validation split), generated here by wrapping
# the hand-written examples in common conversational prefixes/suffixes rather
# than hand-typing hundreds more one-off sentences.
NN_INTENT_EXAMPLES_EXTRA = [
    ("hello please", "greeting"),
    ("hey, hello if you can", "greeting"),
    ("hi there if you can", "greeting"),
    ("so, hi there real quick", "greeting"),
    ("hey, hey", "greeting"),
    ("quick one - hey", "greeting"),
    ("so, good morning for me", "greeting"),
    ("good morning thanks", "greeting"),
    ("so, good evening", "greeting"),
    ("just wondering, good evening", "greeting"),
    ("actually, yo what's up real quick", "greeting"),
    ("by the way, yo what's up", "greeting"),
    ("um, bye right now", "farewell"),
    ("bye when you get a chance", "farewell"),
    ("so anyway, goodbye if that's ok", "farewell"),
    ("goodbye if you can", "farewell"),
    ("just wondering, see you later thanks", "farewell"),
    ("see you later if you can", "farewell"),
    ("so anyway, talk to you soon", "farewell"),
    ("talk to you soon if that's ok", "farewell"),
    ("okay so i'm heading out when you get a chance", "farewell"),
    ("i'm heading out for me", "farewell"),
    ("gotta go now when you get a chance", "farewell"),
    ("gotta go now real quick", "farewell"),
    ("um, thanks a lot", "thanks"),
    ("so anyway, thanks a lot", "thanks"),
    ("thank you so much when you get a chance", "thanks"),
    ("actually, thank you so much for me", "thanks"),
    ("so, appreciate it thanks", "thanks"),
    ("appreciate it real quick", "thanks"),
    ("okay so thanks for the help", "thanks"),
    ("hey, thanks for the help", "thanks"),
    ("that's very kind of you thanks", "thanks"),
    ("actually, that's very kind of you if that's ok", "thanks"),
    ("so, much appreciated when you get a chance", "thanks"),
    ("actually, much appreciated", "thanks"),
    ("how are you if you can", "how_are_you"),
    ("hey, how are you thanks", "how_are_you"),
    ("by the way, how are you doing", "how_are_you"),
    ("just wondering, how are you doing", "how_are_you"),
    ("so, how's it going thanks", "how_are_you"),
    ("how's it going if you can", "how_are_you"),
    ("how have you been please", "how_are_you"),
    ("okay so how have you been when you get a chance", "how_are_you"),
    ("just wondering, you alright", "how_are_you"),
    ("hey, you alright", "how_are_you"),
    ("how do you feel today if you can", "how_are_you"),
    ("how do you feel today if that's ok", "how_are_you"),
    ("just wondering, i'm feeling great today", "feelings_happy"),
    ("i'm feeling great today right now", "feelings_happy"),
    ("real quick, i am so happy right now right now", "feelings_happy"),
    ("hey, i am so happy right now please", "feelings_happy"),
    ("today has been amazing right now", "feelings_happy"),
    ("just wondering, today has been amazing", "feelings_happy"),
    ("just wondering, i feel wonderful right now", "feelings_happy"),
    ("i feel wonderful right now", "feelings_happy"),
    ("by the way, i'm in such a good mood", "feelings_happy"),
    ("i'm in such a good mood if that's ok", "feelings_happy"),
    ("everything is going great for me if you can", "feelings_happy"),
    ("everything is going great for me thanks", "feelings_happy"),
    ("so, i'm feeling kind of down thanks", "feelings_sad"),
    ("so, i'm feeling kind of down", "feelings_sad"),
    ("um, i am sad today when you get a chance", "feelings_sad"),
    ("i am sad today when you get a chance", "feelings_sad"),
    ("not having a great day thanks", "feelings_sad"),
    ("so, not having a great day", "feelings_sad"),
    ("i feel pretty low right now right now", "feelings_sad"),
    ("real quick, i feel pretty low right now", "feelings_sad"),
    ("today has been rough real quick", "feelings_sad"),
    ("actually, today has been rough right now", "feelings_sad"),
    ("i'm feeling a bit blue if that's ok", "feelings_sad"),
    ("actually, i'm feeling a bit blue please", "feelings_sad"),
    ("by the way, i'm exhausted if you can", "feelings_tired"),
    ("actually, i'm exhausted when you get a chance", "feelings_tired"),
    ("i'm so tired please", "feelings_tired"),
    ("so, i'm so tired when you get a chance", "feelings_tired"),
    ("actually, i barely slept last night", "feelings_tired"),
    ("so, i barely slept last night", "feelings_tired"),
    ("so anyway, i need a nap", "feelings_tired"),
    ("i need a nap for me", "feelings_tired"),
    ("actually, i'm running on no sleep for me", "feelings_tired"),
    ("real quick, i'm running on no sleep if you can", "feelings_tired"),
    ("quick one - i feel drained today real quick", "feelings_tired"),
    ("so, i feel drained today", "feelings_tired"),
    ("so anyway, what's the weather like", "weather_smalltalk"),
    ("what's the weather like if that's ok", "weather_smalltalk"),
    ("is it sunny outside right now", "weather_smalltalk"),
    ("real quick, is it sunny outside", "weather_smalltalk"),
    ("just wondering, nice weather today if you can", "weather_smalltalk"),
    ("actually, nice weather today real quick", "weather_smalltalk"),
    ("is it raining out there when you get a chance", "weather_smalltalk"),
    ("just wondering, is it raining out there for me", "weather_smalltalk"),
    ("um, how's the weather where you are for me", "weather_smalltalk"),
    ("quick one - how's the weather where you are if you can", "weather_smalltalk"),
    ("it's pretty cold outside today please", "weather_smalltalk"),
    ("it's pretty cold outside today when you get a chance", "weather_smalltalk"),
    ("are you an ai if you can", "bot_capabilities_joke"),
    ("so, are you an ai for me", "bot_capabilities_joke"),
    ("hey, are you a robot if that's ok", "bot_capabilities_joke"),
    ("so, are you a robot", "bot_capabilities_joke"),
    ("what are you right now", "bot_capabilities_joke"),
    ("what are you for me", "bot_capabilities_joke"),
    ("so anyway, are you human thanks", "bot_capabilities_joke"),
    ("okay so are you human for me", "bot_capabilities_joke"),
    ("actually, are you a real person right now", "bot_capabilities_joke"),
    ("okay so are you a real person", "bot_capabilities_joke"),
    ("quick one - are you sentient if that's ok", "bot_capabilities_joke"),
    ("so anyway, are you sentient if you can", "bot_capabilities_joke"),
    ("um, what's your name", "ask_bot_name"),
    ("hey, what's your name thanks", "ask_bot_name"),
    ("real quick, who are you for me", "ask_bot_name"),
    ("okay so who are you", "ask_bot_name"),
    ("hey, do you have a name", "ask_bot_name"),
    ("so anyway, do you have a name please", "ask_bot_name"),
    ("okay so what should i call you right now", "ask_bot_name"),
    ("actually, what should i call you", "ask_bot_name"),
    ("quick one - tell me your name", "ask_bot_name"),
    ("real quick, tell me your name if you can", "ask_bot_name"),
    ("real quick, what is this bot's name please", "ask_bot_name"),
    ("so, what is this bot's name", "ask_bot_name"),
    ("quick one - call yourself max if you can", "call_yourself"),
    ("um, call yourself max", "call_yourself"),
    ("i want to name you buddy for me", "call_yourself"),
    ("i want to name you buddy if that's ok", "call_yourself"),
    ("from now on your name is rex please", "call_yourself"),
    ("actually, from now on your name is rex", "call_yourself"),
    ("i'm going to call you sam please", "call_yourself"),
    ("so, i'm going to call you sam", "call_yourself"),
    ("hey, your new name is nova please", "call_yourself"),
    ("so, your new name is nova if you can", "call_yourself"),
    ("let's rename you to jarvis when you get a chance", "call_yourself"),
    ("okay so let's rename you to jarvis right now", "call_yourself"),
    ("so anyway, what is my name for me", "ask_my_name"),
    ("what is my name when you get a chance", "ask_my_name"),
    ("okay so do you remember my name", "ask_my_name"),
    ("do you remember my name thanks", "ask_my_name"),
    ("so, what did i tell you my name was right now", "ask_my_name"),
    ("what did i tell you my name was when you get a chance", "ask_my_name"),
    ("do you know who i am for me", "ask_my_name"),
    ("so, do you know who i am right now", "ask_my_name"),
    ("so anyway, can you recall my name please", "ask_my_name"),
    ("actually, can you recall my name when you get a chance", "ask_my_name"),
    ("what name did i give you right now", "ask_my_name"),
    ("actually, what name did i give you for me", "ask_my_name"),
    ("my favorite food is pizza for me", "remember_fact"),
    ("so anyway, my favorite food is pizza", "remember_fact"),
    ("real quick, remember that my birthday is in june", "remember_fact"),
    ("so anyway, remember that my birthday is in june when you get a chance", "remember_fact"),
    ("just wondering, my favorite color is blue please", "remember_fact"),
    ("real quick, my favorite color is blue if you can", "remember_fact"),
    ("please remember that i have a dog named rex if that's ok", "remember_fact"),
    ("please remember that i have a dog named rex please", "remember_fact"),
    ("okay so my favorite movie is inception please", "remember_fact"),
    ("by the way, my favorite movie is inception if you can", "remember_fact"),
    ("actually, remember this: i live in seattle if that's ok", "remember_fact"),
    ("okay so remember this: i live in seattle thanks", "remember_fact"),
    ("hey, what time is it right now", "current_time"),
    ("real quick, what time is it right now please", "current_time"),
    ("tell me the time thanks", "current_time"),
    ("tell me the time please", "current_time"),
    ("okay so do you know what time it is", "current_time"),
    ("okay so do you know what time it is for me", "current_time"),
    ("so, can you tell me the current time", "current_time"),
    ("so anyway, can you tell me the current time real quick", "current_time"),
    ("so anyway, what's the time right now", "current_time"),
    ("just wondering, what's the time right now when you get a chance", "current_time"),
    ("quick one - give me the time please", "current_time"),
    ("so, give me the time please if that's ok", "current_time"),
    ("by the way, what is today's date right now", "current_date"),
    ("actually, what is today's date right now", "current_date"),
    ("hey, what's the date today when you get a chance", "current_date"),
    ("um, what's the date today", "current_date"),
    ("okay so can you tell me today's date please", "current_date"),
    ("real quick, can you tell me today's date", "current_date"),
    ("so anyway, what's today's date when you get a chance", "current_date"),
    ("actually, what's today's date when you get a chance", "current_date"),
    ("so, do you know the date today when you get a chance", "current_date"),
    ("do you know the date today if you can", "current_date"),
    ("give me today's date please", "current_date"),
    ("hey, give me today's date", "current_date"),
    ("how many days until christmas thanks", "days_until_holiday"),
    ("so, how many days until christmas", "days_until_holiday"),
    ("by the way, how many days left until new year", "days_until_holiday"),
    ("by the way, how many days left until new year please", "days_until_holiday"),
    ("so anyway, how long until halloween for me", "days_until_holiday"),
    ("how long until halloween right now", "days_until_holiday"),
    ("real quick, how many days till my birthday if you can", "days_until_holiday"),
    ("real quick, how many days till my birthday for me", "days_until_holiday"),
    ("just wondering, days remaining until thanksgiving real quick", "days_until_holiday"),
    ("just wondering, days remaining until thanksgiving", "days_until_holiday"),
    ("okay so how far away is valentine's day", "days_until_holiday"),
    ("hey, how far away is valentine's day for me", "days_until_holiday"),
    ("how many days between these two dates when you get a chance", "days_between_dates"),
    ("okay so how many days between these two dates", "days_between_dates"),
    ("by the way, what's the difference in days between january 1 and march 1", "days_between_dates"),
    ("real quick, what's the difference in days between january 1 and march 1 please", "days_between_dates"),
    ("by the way, how many days are between two specific dates thanks", "days_between_dates"),
    ("how many days are between two specific dates real quick", "days_between_dates"),
    ("just wondering, calculate the days between 2024-01-01 and 2024-06-01", "days_between_dates"),
    ("um, calculate the days between 2024-01-01 and 2024-06-01", "days_between_dates"),
    ("how many days passed between those dates thanks", "days_between_dates"),
    ("real quick, how many days passed between those dates if that's ok", "days_between_dates"),
    ("days between two dates please if you can", "days_between_dates"),
    ("just wondering, days between two dates please real quick", "days_between_dates"),
    ("how old would i be if i was born in 2000 right now", "age_calculator"),
    ("okay so how old would i be if i was born in 2000", "age_calculator"),
    ("calculate my age if i was born on a certain date when you get a chance", "age_calculator"),
    ("calculate my age if i was born on a certain date please", "age_calculator"),
    ("so anyway, how old am i if my birthday is in 1995 please", "age_calculator"),
    ("how old am i if my birthday is in 1995 real quick", "age_calculator"),
    ("so, figure out my age from my birth date please", "age_calculator"),
    ("by the way, figure out my age from my birth date", "age_calculator"),
    ("just wondering, how many years old would someone born in 1990 be", "age_calculator"),
    ("by the way, how many years old would someone born in 1990 be please", "age_calculator"),
    ("so anyway, what age would i be born in 2005 when you get a chance", "age_calculator"),
    ("what age would i be born in 2005 if you can", "age_calculator"),
    ("hey, tell me an adventure story for me", "tell_story"),
    ("tell me an adventure story for me", "tell_story"),
    ("by the way, give me a story to read", "tell_story"),
    ("give me a story to read if that's ok", "tell_story"),
    ("so anyway, can you narrate a tale", "tell_story"),
    ("um, can you narrate a tale right now", "tell_story"),
    ("real quick, i want to hear a story if you can", "tell_story"),
    ("i want to hear a story if you can", "tell_story"),
    ("by the way, tell me a mystery story right now", "tell_story"),
    ("so anyway, tell me a mystery story thanks", "tell_story"),
    ("got any good stories for me", "tell_story"),
    ("just wondering, got any good stories", "tell_story"),
    ("so anyway, write a haiku about the ocean right now", "write_haiku"),
    ("okay so write a haiku about the ocean right now", "write_haiku"),
    ("quick one - write me a haiku right now", "write_haiku"),
    ("write me a haiku when you get a chance", "write_haiku"),
    ("can you compose a haiku for me", "write_haiku"),
    ("can you compose a haiku when you get a chance", "write_haiku"),
    ("write a haiku about autumn thanks", "write_haiku"),
    ("by the way, write a haiku about autumn right now", "write_haiku"),
    ("just wondering, give me a haiku poem thanks", "write_haiku"),
    ("hey, give me a haiku poem if you can", "write_haiku"),
    ("quick one - haiku about the moon please", "write_haiku"),
    ("hey, haiku about the moon please", "write_haiku"),
    ("so anyway, write an acrostic poem for jordan when you get a chance", "write_acrostic"),
    ("by the way, write an acrostic poem for jordan for me", "write_acrostic"),
    ("can you make an acrostic poem with my name thanks", "write_acrostic"),
    ("real quick, can you make an acrostic poem with my name thanks", "write_acrostic"),
    ("okay so write an acrostic for the word ocean for me", "write_acrostic"),
    ("by the way, write an acrostic for the word ocean if that's ok", "write_acrostic"),
    ("hey, make me an acrostic poem real quick", "write_acrostic"),
    ("just wondering, make me an acrostic poem right now", "write_acrostic"),
    ("so anyway, acrostic poem using my name please", "write_acrostic"),
    ("acrostic poem using my name please if you can", "write_acrostic"),
    ("real quick, compose an acrostic for friendship", "write_acrostic"),
    ("compose an acrostic for friendship please", "write_acrostic"),
    ("just wondering, write a rhyming poem about love", "write_poem_general"),
    ("write a rhyming poem about love if that's ok", "write_poem_general"),
    ("quick one - write me a poem for me", "write_poem_general"),
    ("so, write me a poem", "write_poem_general"),
    ("real quick, can you write a poem about nature", "write_poem_general"),
    ("so anyway, can you write a poem about nature", "write_poem_general"),
    ("um, compose a short poem for me", "write_poem_general"),
    ("by the way, compose a short poem for me right now", "write_poem_general"),
    ("quick one - i'd like a poem about friendship right now", "write_poem_general"),
    ("um, i'd like a poem about friendship", "write_poem_general"),
    ("hey, write some poetry for me", "write_poem_general"),
    ("write some poetry for me real quick", "write_poem_general"),
    ("okay so what is 12 times 4", "simple_math"),
    ("what is 12 times 4 right now", "simple_math"),
    ("so anyway, calculate 9 plus 7", "simple_math"),
    ("hey, calculate 9 plus 7 when you get a chance", "simple_math"),
    ("just wondering, what's 100 divided by 4 real quick", "simple_math"),
    ("by the way, what's 100 divided by 4 when you get a chance", "simple_math"),
    ("actually, can you do some quick math for me", "simple_math"),
    ("um, can you do some quick math for me if you can", "simple_math"),
    ("real quick, what's 15 minus 6", "simple_math"),
    ("what's 15 minus 6 if you can", "simple_math"),
    ("by the way, solve 8 times 8 if you can", "simple_math"),
    ("so anyway, solve 8 times 8", "simple_math"),
    ("um, tell me a funny joke", "tell_joke"),
    ("by the way, tell me a funny joke", "tell_joke"),
    ("make me laugh for me", "tell_joke"),
    ("quick one - make me laugh", "tell_joke"),
    ("quick one - tell me a joke", "tell_joke"),
    ("um, tell me a joke real quick", "tell_joke"),
    ("can you tell me a joke please for me", "tell_joke"),
    ("just wondering, can you tell me a joke please", "tell_joke"),
    ("just wondering, got any jokes", "tell_joke"),
    ("got any jokes if you can", "tell_joke"),
    ("real quick, say something funny", "tell_joke"),
    ("say something funny real quick", "tell_joke"),
    ("hey, tell me an inspirational quote", "tell_quote"),
    ("so anyway, tell me an inspirational quote", "tell_quote"),
    ("just wondering, give me some wisdom", "tell_quote"),
    ("okay so give me some wisdom", "tell_quote"),
    ("um, share an inspiring quote", "tell_quote"),
    ("real quick, share an inspiring quote real quick", "tell_quote"),
    ("hey, i need some motivation, give me a quote", "tell_quote"),
    ("just wondering, i need some motivation, give me a quote for me", "tell_quote"),
    ("quick one - got a good quote for me real quick", "tell_quote"),
    ("quick one - got a good quote for me", "tell_quote"),
    ("um, tell me something inspiring", "tell_quote"),
    ("quick one - tell me something inspiring", "tell_quote"),
    ("give me a riddle to solve for me", "tell_riddle"),
    ("give me a riddle to solve if you can", "tell_riddle"),
    ("puzzle me with a brain teaser if that's ok", "tell_riddle"),
    ("by the way, puzzle me with a brain teaser", "tell_riddle"),
    ("hey, got a riddle for me", "tell_riddle"),
    ("um, got a riddle for me right now", "tell_riddle"),
    ("quick one - i want to solve a riddle", "tell_riddle"),
    ("so, i want to solve a riddle", "tell_riddle"),
    ("can you stump me with a riddle for me", "tell_riddle"),
    ("by the way, can you stump me with a riddle real quick", "tell_riddle"),
    ("give me a tricky riddle real quick", "tell_riddle"),
    ("so anyway, give me a tricky riddle", "tell_riddle"),
    ("ask me a trivia question when you get a chance", "tell_trivia"),
    ("okay so ask me a trivia question", "tell_trivia"),
    ("just wondering, quiz me on something for me", "tell_trivia"),
    ("quiz me on something real quick", "tell_trivia"),
    ("um, test my knowledge with trivia", "tell_trivia"),
    ("test my knowledge with trivia right now", "tell_trivia"),
    ("quick one - got a trivia question for me thanks", "tell_trivia"),
    ("got a trivia question for me real quick", "tell_trivia"),
    ("hey, i want to answer a trivia question", "tell_trivia"),
    ("actually, i want to answer a trivia question when you get a chance", "tell_trivia"),
    ("quick one - give me something to quiz me on real quick", "tell_trivia"),
    ("give me something to quiz me on right now", "tell_trivia"),
    ("so, count the words in this sentence thanks", "word_count_tool"),
    ("count the words in this sentence thanks", "word_count_tool"),
    ("hey, how many words are in this paragraph please", "word_count_tool"),
    ("hey, how many words are in this paragraph", "word_count_tool"),
    ("actually, can you count the words for me", "word_count_tool"),
    ("just wondering, can you count the words for me", "word_count_tool"),
    ("word count for this text please real quick", "word_count_tool"),
    ("so, word count for this text please please", "word_count_tool"),
    ("so, how many words did i just type right now", "word_count_tool"),
    ("so, how many words did i just type", "word_count_tool"),
    ("hey, count words in the following text", "word_count_tool"),
    ("okay so count words in the following text please", "word_count_tool"),
    ("hey, check if racecar is a palindrome real quick", "palindrome_check"),
    ("check if racecar is a palindrome if that's ok", "palindrome_check"),
    ("so, is this word a palindrome", "palindrome_check"),
    ("actually, is this word a palindrome", "palindrome_check"),
    ("real quick, can you tell if a word reads the same backwards please", "palindrome_check"),
    ("so, can you tell if a word reads the same backwards", "palindrome_check"),
    ("hey, palindrome check please please", "palindrome_check"),
    ("um, palindrome check please when you get a chance", "palindrome_check"),
    ("okay so does this word count as a palindrome", "palindrome_check"),
    ("actually, does this word count as a palindrome", "palindrome_check"),
    ("so, verify if level is a palindrome when you get a chance", "palindrome_check"),
    ("real quick, verify if level is a palindrome if you can", "palindrome_check"),
    ("just wondering, convert 10 miles to kilometers", "unit_convert"),
    ("actually, convert 10 miles to kilometers thanks", "unit_convert"),
    ("how many kilometers is 5 miles please", "unit_convert"),
    ("quick one - how many kilometers is 5 miles", "unit_convert"),
    ("okay so convert pounds to kilograms for me right now", "unit_convert"),
    ("um, convert pounds to kilograms for me when you get a chance", "unit_convert"),
    ("by the way, change 100 fahrenheit to celsius", "unit_convert"),
    ("quick one - change 100 fahrenheit to celsius right now", "unit_convert"),
    ("how do i convert feet to meters right now", "unit_convert"),
    ("quick one - how do i convert feet to meters if that's ok", "unit_convert"),
    ("unit conversion please, miles to km real quick", "unit_convert"),
    ("so, unit conversion please, miles to km thanks", "unit_convert"),
    ("so, check if 17 is a prime number for me", "prime_check"),
    ("okay so check if 17 is a prime number for me", "prime_check"),
    ("quick one - is 23 a prime number", "prime_check"),
    ("hey, is 23 a prime number please", "prime_check"),
    ("real quick, can you tell me if this number is prime please", "prime_check"),
    ("so anyway, can you tell me if this number is prime", "prime_check"),
    ("so, verify whether 31 is prime when you get a chance", "prime_check"),
    ("real quick, verify whether 31 is prime", "prime_check"),
    ("um, prime number check please for me", "prime_check"),
    ("so, prime number check please real quick", "prime_check"),
    ("is 100 a prime number thanks", "prime_check"),
    ("is 100 a prime number please", "prime_check"),
    ("spell out the number 1234 please", "number_to_words_tool"),
    ("so, spell out the number 1234 please", "number_to_words_tool"),
    ("actually, write this number in words", "number_to_words_tool"),
    ("quick one - write this number in words if that's ok", "number_to_words_tool"),
    ("hey, convert 567 into words if that's ok", "number_to_words_tool"),
    ("so anyway, convert 567 into words right now", "number_to_words_tool"),
    ("how do you spell out 42 in english if you can", "number_to_words_tool"),
    ("how do you spell out 42 in english real quick", "number_to_words_tool"),
    ("real quick, turn this number into written words real quick", "number_to_words_tool"),
    ("okay so turn this number into written words real quick", "number_to_words_tool"),
    ("real quick, number to words conversion please", "number_to_words_tool"),
    ("so, number to words conversion please right now", "number_to_words_tool"),
    ("quick one - add buy milk to my to-do list", "todo_add"),
    ("add buy milk to my to-do list real quick", "todo_add"),
    ("actually, remind me to call the dentist thanks", "todo_add"),
    ("remind me to call the dentist right now", "todo_add"),
    ("okay so put grocery shopping on my list real quick", "todo_add"),
    ("put grocery shopping on my list for me", "todo_add"),
    ("so, add finish homework to my tasks if that's ok", "todo_add"),
    ("just wondering, add finish homework to my tasks", "todo_add"),
    ("real quick, i need to remember to pay rent, add it please", "todo_add"),
    ("just wondering, i need to remember to pay rent, add it", "todo_add"),
    ("can you add walk the dog to my to-do list please", "todo_add"),
    ("can you add walk the dog to my to-do list if that's ok", "todo_add"),
    ("show my to-do list when you get a chance", "todo_list"),
    ("okay so show my to-do list for me", "todo_list"),
    ("real quick, what's on my to-do list thanks", "todo_list"),
    ("what's on my to-do list for me", "todo_list"),
    ("actually, can i see my tasks", "todo_list"),
    ("so, can i see my tasks", "todo_list"),
    ("so anyway, list everything on my to-do list", "todo_list"),
    ("quick one - list everything on my to-do list thanks", "todo_list"),
    ("so anyway, what do i still need to do today right now", "todo_list"),
    ("hey, what do i still need to do today", "todo_list"),
    ("so, pull up my to-do list please thanks", "todo_list"),
    ("by the way, pull up my to-do list please when you get a chance", "todo_list"),
    ("let's play hangman when you get a chance", "hangman_start"),
    ("just wondering, let's play hangman", "hangman_start"),
    ("um, can we play a game of hangman if that's ok", "hangman_start"),
    ("hey, can we play a game of hangman", "hangman_start"),
    ("just wondering, i want to play hangman", "hangman_start"),
    ("quick one - i want to play hangman", "hangman_start"),
    ("okay so start a hangman game please", "hangman_start"),
    ("start a hangman game when you get a chance", "hangman_start"),
    ("okay so hangman please", "hangman_start"),
    ("hangman please right now", "hangman_start"),
    ("okay so let's do hangman thanks", "hangman_start"),
    ("hey, let's do hangman", "hangman_start"),
    ("real quick, show me the help menu", "help"),
    ("okay so show me the help menu if you can", "help"),
    ("so anyway, what can you do please", "help"),
    ("quick one - what can you do", "help"),
    ("um, what can i ask you", "help"),
    ("hey, what can i ask you real quick", "help"),
    ("real quick, list your commands please", "help"),
    ("list your commands thanks", "help"),
    ("so, what are all your features", "help"),
    ("by the way, what are all your features please", "help"),
    ("how do i use this chatbot real quick", "help"),
    ("real quick, how do i use this chatbot thanks", "help"),
]
NN_INTENT_EXAMPLES.extend(NN_INTENT_EXAMPLES_EXTRA)

# ---- Second round of auto-generated supplementary paraphrases -------------
NN_INTENT_EXAMPLES_EXTRA_2 = [
    ("honestly, hello please", "greeting"),
    ("hmm, hey, hello if you can", "greeting"),
    ("ok but hi there if you can", "greeting"),
    ("honestly, so, hi there real quick no worries", "greeting"),
    ("for real, um, bye right now ok", "farewell"),
    ("so anyway, goodbye if that's ok ok", "farewell"),
    ("not gonna lie, goodbye if you can ok", "farewell"),
    ("well, um, thanks a lot ok", "thanks"),
    ("not gonna lie, so anyway, thanks a lot", "thanks"),
    ("hmm, thank you so much when you get a chance no worries", "thanks"),
    ("hmm, actually, thank you so much for me haha", "thanks"),
    ("hey, how are you thanks seriously", "how_are_you"),
    ("for real, by the way, how are you doing", "how_are_you"),
    ("ok but i'm feeling great today right now seriously", "feelings_happy"),
    ("hmm, real quick, i am so happy right now right now when free", "feelings_happy"),
    ("hey, i am so happy right now please no worries", "feelings_happy"),
    ("honestly, so, i'm feeling kind of down thanks", "feelings_sad"),
    ("hmm, so, i'm feeling kind of down if that works", "feelings_sad"),
    ("hmm, um, i am sad today when you get a chance", "feelings_sad"),
    ("look, i am sad today when you get a chance", "feelings_sad"),
    ("ok but by the way, i'm exhausted if you can", "feelings_tired"),
    ("so, i'm so tired when you get a chance when free", "feelings_tired"),
    ("so anyway, what's the weather like haha", "weather_smalltalk"),
    ("hmm, what's the weather like if that's ok ok", "weather_smalltalk"),
    ("well, is it sunny outside right now no worries", "weather_smalltalk"),
    ("are you an ai if you can haha", "bot_capabilities_joke"),
    ("look, so, are you an ai for me", "bot_capabilities_joke"),
    ("honestly, hey, are you a robot if that's ok", "bot_capabilities_joke"),
    ("ok but so, are you a robot", "bot_capabilities_joke"),
    ("look, um, what's your name when free", "ask_bot_name"),
    ("ok but hey, what's your name thanks no worries", "ask_bot_name"),
    ("for real, real quick, who are you for me", "ask_bot_name"),
    ("okay so who are you seriously", "ask_bot_name"),
    ("quick one - call yourself max if you can seriously", "call_yourself"),
    ("honestly, um, call yourself max", "call_yourself"),
    ("look, i want to name you buddy if that's ok seriously", "call_yourself"),
    ("so anyway, what is my name for me when free", "ask_my_name"),
    ("ok but what is my name when you get a chance", "ask_my_name"),
    ("for real, okay so do you remember my name haha", "ask_my_name"),
    ("honestly, do you remember my name thanks", "ask_my_name"),
    ("honestly, my favorite food is pizza for me seriously", "remember_fact"),
    ("real quick, remember that my birthday is in june ok", "remember_fact"),
    ("look, so anyway, remember that my birthday is in june when you get a chance", "remember_fact"),
    ("well, hey, what time is it right now ok", "current_time"),
    ("look, real quick, what time is it right now please haha", "current_time"),
    ("look, tell me the time thanks", "current_time"),
    ("look, tell me the time please ok", "current_time"),
    ("by the way, what is today's date right now if that works", "current_date"),
    ("hmm, actually, what is today's date right now", "current_date"),
    ("hey, what's the date today when you get a chance haha", "current_date"),
    ("ok but um, what's the date today no worries", "current_date"),
    ("well, how many days until christmas thanks", "days_until_holiday"),
    ("by the way, how many days left until new year seriously", "days_until_holiday"),
    ("honestly, by the way, how many days left until new year please haha", "days_until_holiday"),
    ("how many days between these two dates when you get a chance if that works", "days_between_dates"),
    ("by the way, what's the difference in days between january 1 and march 1 haha", "days_between_dates"),
    ("real quick, what's the difference in days between january 1 and march 1 please seriously", "days_between_dates"),
    ("for real, how old would i be if i was born in 2000 right now when free", "age_calculator"),
    ("for real, okay so how old would i be if i was born in 2000", "age_calculator"),
    ("well, calculate my age if i was born on a certain date when you get a chance", "age_calculator"),
    ("hmm, calculate my age if i was born on a certain date please if that works", "age_calculator"),
    ("hmm, hey, tell me an adventure story for me when free", "tell_story"),
    ("look, tell me an adventure story for me", "tell_story"),
    ("ok but by the way, give me a story to read ok", "tell_story"),
    ("give me a story to read if that's ok no worries", "tell_story"),
    ("ok but so anyway, write a haiku about the ocean right now when free", "write_haiku"),
    ("not gonna lie, okay so write a haiku about the ocean right now when free", "write_haiku"),
    ("for real, quick one - write me a haiku right now seriously", "write_haiku"),
    ("hmm, write me a haiku when you get a chance haha", "write_haiku"),
    ("for real, so anyway, write an acrostic poem for jordan when you get a chance haha", "write_acrostic"),
    ("by the way, write an acrostic poem for jordan for me ok", "write_acrostic"),
    ("honestly, can you make an acrostic poem with my name thanks when free", "write_acrostic"),
    ("real quick, can you make an acrostic poem with my name thanks ok", "write_acrostic"),
    ("ok but just wondering, write a rhyming poem about love no worries", "write_poem_general"),
    ("write a rhyming poem about love if that's ok ok", "write_poem_general"),
    ("ok but quick one - write me a poem for me", "write_poem_general"),
    ("ok but so, write me a poem", "write_poem_general"),
    ("for real, okay so what is 12 times 4 seriously", "simple_math"),
    ("not gonna lie, so anyway, calculate 9 plus 7 ok", "simple_math"),
    ("hey, calculate 9 plus 7 when you get a chance if that works", "simple_math"),
    ("look, um, tell me a funny joke", "tell_joke"),
    ("make me laugh for me when free", "tell_joke"),
    ("ok but quick one - make me laugh when free", "tell_joke"),
    ("hmm, okay so give me some wisdom", "tell_quote"),
    ("ok but give me a riddle to solve for me seriously", "tell_riddle"),
    ("look, give me a riddle to solve if you can if that works", "tell_riddle"),
    ("well, puzzle me with a brain teaser if that's ok", "tell_riddle"),
    ("by the way, puzzle me with a brain teaser if that works", "tell_riddle"),
    ("honestly, ask me a trivia question when you get a chance seriously", "tell_trivia"),
    ("honestly, okay so ask me a trivia question if that works", "tell_trivia"),
    ("look, quiz me on something real quick", "tell_trivia"),
    ("look, so, count the words in this sentence thanks", "word_count_tool"),
    ("count the words in this sentence thanks ok", "word_count_tool"),
    ("not gonna lie, hey, how many words are in this paragraph seriously", "word_count_tool"),
    ("hey, check if racecar is a palindrome real quick if that works", "palindrome_check"),
    ("not gonna lie, check if racecar is a palindrome if that's ok", "palindrome_check"),
    ("not gonna lie, so, is this word a palindrome", "palindrome_check"),
    ("actually, is this word a palindrome when free", "palindrome_check"),
    ("just wondering, convert 10 miles to kilometers haha", "unit_convert"),
    ("ok but actually, convert 10 miles to kilometers thanks no worries", "unit_convert"),
    ("honestly, how many kilometers is 5 miles please ok", "unit_convert"),
    ("look, quick one - how many kilometers is 5 miles", "unit_convert"),
    ("so, check if 17 is a prime number for me when free", "prime_check"),
    ("well, okay so check if 17 is a prime number for me", "prime_check"),
    ("hmm, quick one - is 23 a prime number ok", "prime_check"),
    ("honestly, hey, is 23 a prime number please when free", "prime_check"),
    ("well, spell out the number 1234 please", "number_to_words_tool"),
    ("well, so, spell out the number 1234 please seriously", "number_to_words_tool"),
    ("for real, actually, write this number in words when free", "number_to_words_tool"),
    ("quick one - add buy milk to my to-do list when free", "todo_add"),
    ("well, add buy milk to my to-do list real quick ok", "todo_add"),
    ("for real, actually, remind me to call the dentist thanks if that works", "todo_add"),
    ("remind me to call the dentist right now ok", "todo_add"),
    ("well, show my to-do list when you get a chance if that works", "todo_list"),
    ("honestly, okay so show my to-do list for me", "todo_list"),
    ("not gonna lie, let's play hangman when you get a chance", "hangman_start"),
    ("look, just wondering, let's play hangman", "hangman_start"),
    ("hey, can we play a game of hangman seriously", "hangman_start"),
    ("honestly, okay so show me the help menu if you can", "help"),
    ("for real, so anyway, what can you do please no worries", "help"),
    ("honestly, quick one - what can you do", "help"),
]
NN_INTENT_EXAMPLES.extend(NN_INTENT_EXAMPLES_EXTRA_2)

# A THIRD supplementary batch, added alongside the network-depth
# increase across this whole file: 3 fresh examples per label using
# genuinely different vocabulary from the existing batches above
# (not just reworded paraphrases of the same words), so the larger,
# deeper networks have more LEXICAL variety to generalize from, not
# just more repetitions of the same handful of words.
NN_INTENT_EXAMPLES_EXTRA_3 = [
    ("greetings, stranger", "greeting"),
    ("well hello to you", "greeting"),
    ("knock knock, anybody home", "greeting"),
    ("farewell for now, take care", "farewell"),
    ("catch you on the flip side", "farewell"),
    ("signing off, talk soon", "farewell"),
    ("how's life treating you", "how_are_you"),
    ("everything going alright with you", "how_are_you"),
    ("how are things on your end", "how_are_you"),
    ("i'm over the moon about this", "feelings_happy"),
    ("today has been absolutely delightful", "feelings_happy"),
    ("i'm grinning ear to ear", "feelings_happy"),
    ("i've been feeling pretty blue lately", "feelings_sad"),
    ("this news has me heartbroken", "feelings_sad"),
    ("i've had a really gloomy week", "feelings_sad"),
    ("i'm running on empty right now", "feelings_tired"),
    ("i could use a nap desperately", "feelings_tired"),
    ("my energy is completely drained", "feelings_tired"),
    ("go ahead and tell me a funny one", "tell_joke"),
    ("got any comedy for me", "tell_joke"),
    ("make me chuckle please", "tell_joke"),
    ("share an inspiring saying with me", "tell_quote"),
    ("give me some wisdom to reflect on", "tell_quote"),
    ("got a memorable line for me", "tell_quote"),
    ("stump me with a brain teaser", "tell_riddle"),
    ("give me a puzzle to solve", "tell_riddle"),
    ("challenge my thinking with a riddle", "tell_riddle"),
    ("spin me a tale", "tell_story"),
    ("narrate something imaginative", "tell_story"),
    ("i'd love to hear a narrative", "tell_story"),
    ("hit me with a fun fact", "tell_trivia"),
    ("teach me something obscure", "tell_trivia"),
    ("what's a neat piece of trivia", "tell_trivia"),
    ("let's start a round of hangman", "hangman_start"),
    ("fancy a word-guessing game", "hangman_start"),
    ("i want to try hangman now", "hangman_start"),
    ("what functions do you offer", "help"),
    ("walk me through your abilities", "help"),
    ("give me a rundown of your features", "help"),
    ("crunch these figures for me", "simple_math"),
    ("what does this arithmetic equal", "simple_math"),
    ("solve this calculation please", "simple_math"),
    ("convert these measurements for me", "unit_convert"),
    ("switch this to metric please", "unit_convert"),
    ("translate this unit into another", "unit_convert"),
    ("what's today's calendar date", "current_date"),
    ("tell me the date right now", "current_date"),
    ("what day falls today", "current_date"),
    ("what hour is it currently", "current_time"),
    ("give me the clock reading", "current_time"),
    ("what's the time this moment", "current_time"),
    ("figure out someone's age from their birthdate", "age_calculator"),
    ("how old would that make them", "age_calculator"),
    ("calculate age from a birthday", "age_calculator"),
    ("how many days separate these two dates", "days_between_dates"),
    ("count the days from here to there", "days_between_dates"),
    ("span between these calendar dates please", "days_between_dates"),
    ("how long until the next holiday", "days_until_holiday"),
    ("countdown to the upcoming celebration", "days_until_holiday"),
    ("when's the next festive day", "days_until_holiday"),
    ("jot this down for later", "remember_fact"),
    ("keep this detail in mind", "remember_fact"),
    ("store this note for me", "remember_fact"),
    ("put this on my task list", "todo_add"),
    ("add another chore to my list", "todo_add"),
    ("note this errand down for me", "todo_add"),
    ("what's still on my agenda", "todo_list"),
    ("show my pending tasks", "todo_list"),
    ("what chores are left", "todo_list"),
    ("is this word the same forwards and backwards", "palindrome_check"),
    ("check if this reads the same reversed", "palindrome_check"),
    ("does this phrase mirror itself", "palindrome_check"),
    ("is this figure only divisible by itself and one", "prime_check"),
    ("check whether this number is prime", "prime_check"),
    ("determine if this integer is prime", "prime_check"),
    ("spell out this numeral in words", "number_to_words_tool"),
    ("turn this digit into written form", "number_to_words_tool"),
    ("write this quantity out longhand", "number_to_words_tool"),
    ("tally the words in this passage", "word_count_tool"),
    ("how many words appear here", "word_count_tool"),
    ("count the terms in this text", "word_count_tool"),
    ("compose a short verse for me", "write_poem_general"),
    ("craft me some poetry", "write_poem_general"),
    ("pen a few rhyming lines", "write_poem_general"),
    ("write a 5-7-5 syllable verse", "write_haiku"),
    ("compose a haiku about nature", "write_haiku"),
    ("give me a short japanese-style poem", "write_haiku"),
    ("write a poem spelling out my name", "write_acrostic"),
    ("build an acrostic from this word", "write_acrostic"),
    ("craft a poem using these letters vertically", "write_acrostic"),
    ("what should i call you", "ask_bot_name"),
    ("do you go by a particular name", "ask_bot_name"),
    ("what's your given name", "ask_bot_name"),
    ("do you happen to remember my name", "ask_my_name"),
    ("what name did i give you earlier", "ask_my_name"),
    ("say my name if you know it", "ask_my_name"),
    ("describe yourself in a sentence", "call_yourself"),
    ("what kind of entity are you", "call_yourself"),
    ("how would you label yourself", "call_yourself"),
    ("brag about what you can pull off", "bot_capabilities_joke"),
    ("give me the funny version of your skills", "bot_capabilities_joke"),
    ("boast about your talents jokingly", "bot_capabilities_joke"),
    ("how's the forecast looking outside", "weather_smalltalk"),
    ("is it chilly or warm out there", "weather_smalltalk"),
    ("what's the sky doing today", "weather_smalltalk"),
    ("i appreciate you so much", "thanks"),
    ("cheers for the assistance", "thanks"),
    ("much obliged for your help", "thanks"),
]
NN_INTENT_EXAMPLES.extend(NN_INTENT_EXAMPLES_EXTRA_3)

# A FOURTH supplementary batch (targeting +65% total dataset size,
# alongside the broader "scale everything up" pass this belongs to).
# Fresh vocabulary per label again, same reasoning as EXTRA_3.
NN_INTENT_EXAMPLES_EXTRA_4 = [
    ("hiya, good to see you", "greeting"),
    ("top of the morning to you", "greeting"),
    ("hello again, it's been a while", "greeting"),
    ("i'll let you go, speak soon", "farewell"),
    ("heading out now, bye for now", "farewell"),
    ("that's all for today, until next time", "farewell"),
    ("what's the vibe like for you today", "how_are_you"),
    ("holding up okay over there", "how_are_you"),
    ("how's your day shaping up", "how_are_you"),
    ("i'm riding a real high right now", "feelings_happy"),
    ("everything feels golden today", "feelings_happy"),
    ("i can't stop smiling honestly", "feelings_happy"),
    ("i've been feeling a bit low lately", "feelings_sad"),
    ("today knocked the wind out of me emotionally", "feelings_sad"),
    ("i feel kind of hollow right now", "feelings_sad"),
    ("i'm running on absolute empty", "feelings_tired"),
    ("i could sleep for a week straight", "feelings_tired"),
    ("my eyelids are so heavy right now", "feelings_tired"),
    ("lay a good joke on me", "tell_joke"),
    ("give me your best one-liner", "tell_joke"),
    ("got a pun for me", "tell_joke"),
    ("drop some wisdom on me", "tell_quote"),
    ("share something thought-provoking", "tell_quote"),
    ("give me a line worth remembering", "tell_quote"),
    ("throw a tricky riddle my way", "tell_riddle"),
    ("i'm in the mood for a puzzle", "tell_riddle"),
    ("test my brain with a riddle", "tell_riddle"),
    ("weave me a little tale", "tell_story"),
    ("i want a short story right now", "tell_story"),
    ("tell me something imaginative please", "tell_story"),
    ("drop a fun fact on me", "tell_trivia"),
    ("surprise me with trivia", "tell_trivia"),
    ("what's an interesting fact you know", "tell_trivia"),
    ("let's kick off a hangman round", "hangman_start"),
    ("i'm up for hangman right now", "hangman_start"),
    ("start a word guessing challenge", "hangman_start"),
    ("run me through what you can do", "help"),
    ("show me your feature list", "help"),
    ("what tricks do you have up your sleeve", "help"),
    ("work out this math problem for me", "simple_math"),
    ("what's the total for this equation", "simple_math"),
    ("compute this for me please", "simple_math"),
    ("switch this measurement to another unit", "unit_convert"),
    ("convert this figure for me", "unit_convert"),
    ("what's this in different units", "unit_convert"),
    ("what's today's date exactly", "current_date"),
    ("remind me what day it is", "current_date"),
    ("give me today's date please", "current_date"),
    ("what time does the clock say", "current_time"),
    ("tell me the current time please", "current_time"),
    ("what's the time right now", "current_time"),
    ("work out someone's age for me", "age_calculator"),
    ("how old is someone born on this date", "age_calculator"),
    ("calculate their age please", "age_calculator"),
    ("how many days sit between these dates", "days_between_dates"),
    ("count the days from this date to that one", "days_between_dates"),
    ("what's the gap between these two dates", "days_between_dates"),
    ("how far off is the next holiday", "days_until_holiday"),
    ("count down to the next celebration", "days_until_holiday"),
    ("when's the next holiday coming up", "days_until_holiday"),
    ("hang onto this detail for me", "remember_fact"),
    ("save this info for later please", "remember_fact"),
    ("make a note of this for me", "remember_fact"),
    ("throw this onto my to-do list", "todo_add"),
    ("add this task to my list", "todo_add"),
    ("note down this errand for me", "todo_add"),
    ("what's left on my task list", "todo_list"),
    ("show me my pending tasks", "todo_list"),
    ("what chores do i still have", "todo_list"),
    ("check if this word reads the same backwards", "palindrome_check"),
    ("is this a mirror-image word", "palindrome_check"),
    ("does this phrase reverse into itself", "palindrome_check"),
    ("check if this number's only divisors are one and itself", "prime_check"),
    ("is this figure a prime number", "prime_check"),
    ("verify whether this number is prime", "prime_check"),
    ("write this number out in words", "number_to_words_tool"),
    ("spell this numeral out for me", "number_to_words_tool"),
    ("convert this digit to written form", "number_to_words_tool"),
    ("count how many words are in this", "word_count_tool"),
    ("how many words does this text have", "word_count_tool"),
    ("give me a word count for this", "word_count_tool"),
    ("write me some poetry please", "write_poem_general"),
    ("compose a poem for me", "write_poem_general"),
    ("give me a short piece of verse", "write_poem_general"),
    ("write a haiku about the seasons", "write_haiku"),
    ("compose a 5-7-5 poem for me", "write_haiku"),
    ("give me a haiku please", "write_haiku"),
    ("write an acrostic using my name", "write_acrostic"),
    ("make an acrostic poem for me", "write_acrostic"),
    ("build a poem from these letters", "write_acrostic"),
    ("what should i address you as", "ask_bot_name"),
    ("do you have a name i should use", "ask_bot_name"),
    ("what's your name exactly", "ask_bot_name"),
    ("do you recall what i'm called", "ask_my_name"),
    ("what did i tell you my name was", "ask_my_name"),
    ("say my name back to me", "ask_my_name"),
    ("sum yourself up in a few words", "call_yourself"),
    ("what would you call yourself", "call_yourself"),
    ("describe what you are exactly", "call_yourself"),
    ("give me the comedic rundown of your skills", "bot_capabilities_joke"),
    ("brag about yourself for a laugh", "bot_capabilities_joke"),
    ("boast about your powers jokingly", "bot_capabilities_joke"),
    ("what's it like outside right now", "weather_smalltalk"),
    ("is it sunny or overcast today", "weather_smalltalk"),
    ("how's the weather treating you", "weather_smalltalk"),
    ("i owe you a huge thanks", "thanks"),
    ("really grateful for your help here", "thanks"),
    ("thanks a bunch for that", "thanks"),
]
NN_INTENT_EXAMPLES.extend(NN_INTENT_EXAMPLES_EXTRA_4)

NN_INTENT_EXAMPLES_EXTRA_5 = [
    ("yo, what's good", "greeting"),
    ("nice to run into you again", "greeting"),
    ("alright, catch you later then", "farewell"),
    ("i'm off, take it easy", "farewell"),
    ("doing alright, thanks for asking", "how_are_you"),
    ("just checking in, how've you been", "how_are_you"),
    ("i'm on top of the world today", "feelings_happy"),
    ("today's been a genuinely great one", "feelings_happy"),
    ("i've been feeling kind of down", "feelings_sad"),
    ("this week has been emotionally heavy", "feelings_sad"),
    ("i'm dragging today, no energy left", "feelings_tired"),
    ("i need a serious recharge", "feelings_tired"),
    ("got any jokes stashed away", "tell_joke"),
    ("make me laugh with a joke", "tell_joke"),
    ("give me a quote to sit with", "tell_quote"),
    ("share a memorable line with me", "tell_quote"),
    ("i want a riddle to chew on", "tell_riddle"),
    ("puzzle me with something clever", "tell_riddle"),
    ("give me a short story to enjoy", "tell_story"),
    ("spin up a quick narrative", "tell_story"),
    ("what's a wild fact you know", "tell_trivia"),
    ("hit me with some trivia", "tell_trivia"),
    ("let's kick off hangman", "hangman_start"),
    ("i feel like playing hangman", "hangman_start"),
    ("what are you capable of doing", "help"),
    ("list out what you can help with", "help"),
    ("solve this equation for me", "simple_math"),
    ("what does this sum come out to", "simple_math"),
    ("change this into another unit for me", "unit_convert"),
    ("what's the equivalent in metric", "unit_convert"),
    ("what's the date today", "current_date"),
    ("remind me of today's date", "current_date"),
    ("what time is it currently", "current_time"),
    ("give me the current time", "current_time"),
    ("figure out this person's age", "age_calculator"),
    ("how old are they based on this birthdate", "age_calculator"),
    ("how many days between these two dates", "days_between_dates"),
    ("what's the day count between these dates", "days_between_dates"),
    ("how soon is the next holiday", "days_until_holiday"),
    ("days remaining until the holiday", "days_until_holiday"),
    ("keep this fact in your memory", "remember_fact"),
    ("remember this detail for me", "remember_fact"),
    ("add this to my task list please", "todo_add"),
    ("put another item on my to-do list", "todo_add"),
    ("what's still pending on my list", "todo_list"),
    ("show me what's left to do", "todo_list"),
    ("does this word read the same in reverse", "palindrome_check"),
    ("check this for a palindrome", "palindrome_check"),
    ("is this number prime or not", "prime_check"),
    ("confirm if this is a prime number", "prime_check"),
    ("turn this number into written words", "number_to_words_tool"),
    ("spell out this quantity", "number_to_words_tool"),
    ("what's the word count on this text", "word_count_tool"),
    ("count the words in this passage", "word_count_tool"),
    ("write a poem for me please", "write_poem_general"),
    ("give me some original verse", "write_poem_general"),
    ("write me a haiku", "write_haiku"),
    ("compose a nature haiku", "write_haiku"),
    ("write an acrostic poem with my name", "write_acrostic"),
    ("craft an acrostic from this word", "write_acrostic"),
    ("what do i call you", "ask_bot_name"),
    ("do you have a proper name", "ask_bot_name"),
    ("do you remember my name at all", "ask_my_name"),
    ("what name did i give you", "ask_my_name"),
    ("describe yourself briefly", "call_yourself"),
    ("what are you, exactly", "call_yourself"),
    ("give me a funny take on your abilities", "bot_capabilities_joke"),
    ("joke about what you can do", "bot_capabilities_joke"),
    ("what's the weather doing today", "weather_smalltalk"),
    ("is it raining out there", "weather_smalltalk"),
    ("thanks a lot for that", "thanks"),
    ("i appreciate you helping me out", "thanks"),
]
NN_INTENT_EXAMPLES.extend(NN_INTENT_EXAMPLES_EXTRA_5)


# ---- Sentiment classifier training data ------------------------------------
#
# A SEPARATE, smaller dataset for a SEPARATE network: this isn't intent
# (what the user wants done) but mood (how the user seems to feel),
# used to color the TONE of responses rather than route to a handler.
SENTIMENT_EXAMPLES = [
    ("i am so happy right now", "positive"),
    ("this is amazing, thank you", "positive"),
    ("i love this, it's great", "positive"),
    ("today has been a fantastic day", "positive"),
    ("i'm really excited about this", "positive"),
    ("that's wonderful news", "positive"),
    ("i feel awesome today", "positive"),
    ("this made my day", "positive"),
    ("i'm thrilled about it", "positive"),
    ("everything is going perfectly", "positive"),
    ("i'm proud of myself today", "positive"),
    ("what a great day this has been", "positive"),
    ("i'm super happy with how this turned out", "positive"),
    ("this is the best news i've heard all week", "positive"),
    ("i feel really good about this", "positive"),
    ("i'm grateful for everything today", "positive"),
    ("life is treating me well lately", "positive"),
    ("this is such a pleasant surprise", "positive"),
    ("i couldn't be happier right now", "positive"),
    ("everything worked out beautifully", "positive"),
    ("i'm in a really great mood", "positive"),
    ("this is fantastic, i love it", "positive"),

    ("i feel terrible today", "negative"),
    ("this is so frustrating", "negative"),
    ("i'm really upset right now", "negative"),
    ("everything is going wrong", "negative"),
    ("i hate how today went", "negative"),
    ("i'm so stressed out", "negative"),
    ("this has been an awful day", "negative"),
    ("i'm feeling really down", "negative"),
    ("nothing is working out for me", "negative"),
    ("i'm exhausted and overwhelmed", "negative"),
    ("i'm worried about everything right now", "negative"),
    ("i feel like giving up", "negative"),
    ("this is really disappointing", "negative"),
    ("i'm so annoyed right now", "negative"),
    ("i can't stand how this turned out", "negative"),
    ("today has been a complete disaster", "negative"),
    ("i'm feeling really anxious about this", "negative"),
    ("everything feels like too much right now", "negative"),
    ("i'm furious about how this went", "negative"),
    ("this situation is making me miserable", "negative"),
    ("i feel so defeated right now", "negative"),
    ("i'm really hurt by what happened", "negative"),

    ("what time is it", "neutral"),
    ("show my to-do list", "neutral"),
    ("convert 10 miles to kilometers", "neutral"),
    ("what is today's date", "neutral"),
    ("tell me a story", "neutral"),
    ("how many days until christmas", "neutral"),
    ("what is 12 times 4", "neutral"),
    ("write me a poem", "neutral"),
    ("count the words in this sentence", "neutral"),
    ("is 17 a prime number", "neutral"),
    ("add buy milk to my to-do list", "neutral"),
    ("what's your name", "neutral"),
    ("how do i spell this word", "neutral"),
    ("what's the capital of france", "neutral"),
    ("can you set a reminder for me", "neutral"),
    ("what's 9 plus 10", "neutral"),
    ("show me my tasks for today", "neutral"),
    ("convert this temperature to celsius", "neutral"),
    ("what day of the week is it", "neutral"),
    ("tell me the population of japan", "neutral"),
]

# ---- Auto-generated supplementary examples ---------------------------------
SENTIMENT_EXAMPLES_EXTRA = [
    ("so, i am so happy right now if you can", "positive"),
    ("this is amazing, thank you thanks", "positive"),
    ("i love this, it's great please", "positive"),
    ("today has been a fantastic day if you can", "positive"),
    ("so anyway, i'm really excited about this please", "positive"),
    ("so anyway, that's wonderful news", "positive"),
    ("i feel awesome today please", "positive"),
    ("um, this made my day", "positive"),
    ("i feel terrible today when you get a chance", "negative"),
    ("okay so this is so frustrating", "negative"),
    ("i'm really upset right now please", "negative"),
    ("by the way, everything is going wrong if you can", "negative"),
    ("by the way, i hate how today went thanks", "negative"),
    ("i'm so stressed out when you get a chance", "negative"),
    ("so, this has been an awful day if that's ok", "negative"),
    ("i'm feeling really down real quick", "negative"),
    ("so anyway, what time is it", "neutral"),
    ("hey, show my to-do list if that's ok", "neutral"),
    ("okay so convert 10 miles to kilometers real quick", "neutral"),
    ("what is today's date real quick", "neutral"),
    ("okay so tell me a story for me", "neutral"),
    ("hey, how many days until christmas", "neutral"),
    ("by the way, what is 12 times 4 thanks", "neutral"),
    ("actually, write me a poem", "neutral"),
]
SENTIMENT_EXAMPLES.extend(SENTIMENT_EXAMPLES_EXTRA)

# ---- Third round of auto-generated supplementary examples ------------------
SENTIMENT_EXAMPLES_EXTRA_2 = [
    ("honestly, so, i am so happy right now if you can", "positive"),
    ("honestly, this is amazing, thank you thanks", "positive"),
    ("honestly, i love this, it's great please", "positive"),
    ("like, today has been a fantastic day if you can", "positive"),
    ("well, so anyway, i'm really excited about this please", "positive"),
    ("honestly, so anyway, that's wonderful news", "positive"),
    ("like, i feel awesome today please", "positive"),
    ("honestly, um, this made my day", "positive"),
    ("well, i feel terrible today when you get a chance", "negative"),
    ("honestly, okay so this is so frustrating", "negative"),
    ("well, i'm really upset right now please", "negative"),
    ("like, by the way, everything is going wrong if you can", "negative"),
    ("like, by the way, i hate how today went thanks", "negative"),
    ("well, i'm so stressed out when you get a chance", "negative"),
    ("like, so, this has been an awful day if that's ok", "negative"),
    ("well, i'm feeling really down real quick", "negative"),
    ("well, so anyway, what time is it", "neutral"),
    ("like, hey, show my to-do list if that's ok", "neutral"),
    ("well, okay so convert 10 miles to kilometers real quick", "neutral"),
    ("well, what is today's date real quick", "neutral"),
    ("like, okay so tell me a story for me", "neutral"),
    ("well, hey, how many days until christmas", "neutral"),
    ("like, by the way, what is 12 times 4 thanks", "neutral"),
    ("like, actually, write me a poem", "neutral"),
]
SENTIMENT_EXAMPLES.extend(SENTIMENT_EXAMPLES_EXTRA_2)

# A THIRD supplementary batch, added alongside the network-depth
# increase across this whole file: fresh vocabulary per class rather
# than more rewordings of the same handful of feeling-words, so the
# now-deeper network has more lexical variety to generalize from.
SENTIMENT_EXAMPLES_EXTRA_3 = [
    ("this turned out better than i ever hoped", "positive"),
    ("i'm absolutely buzzing with excitement", "positive"),
    ("what a delightful surprise this was", "positive"),
    ("i feel like everything is finally clicking", "positive"),
    ("this made my entire week", "positive"),
    ("i'm so grateful things worked out", "positive"),
    ("this is exactly what i needed today", "positive"),
    ("i'm practically glowing with happiness", "positive"),
    ("everything about this feels right", "positive"),
    ("i couldn't ask for a better outcome", "positive"),
    ("this really lifted my spirits", "positive"),
    ("i'm thrilled beyond words", "positive"),
    ("today just kept getting better and better", "positive"),
    ("i feel so fortunate right now", "positive"),
    ("this brought a genuine smile to my face", "positive"),
    ("i'm devastated by how this played out", "negative"),
    ("everything feels like it's falling apart", "negative"),
    ("i've hit a really low point", "negative"),
    ("this situation is dragging me down", "negative"),
    ("i feel completely defeated", "negative"),
    ("nothing seems to be going right lately", "negative"),
    ("i'm at the end of my rope here", "negative"),
    ("this has left me feeling hollow", "negative"),
    ("i can't shake this heavy feeling", "negative"),
    ("i'm dreading what comes next", "negative"),
    ("this whole ordeal has worn me down", "negative"),
    ("i feel like i'm sinking", "negative"),
    ("today has been one disappointment after another", "negative"),
    ("i'm struggling to see any silver lining", "negative"),
    ("this outcome really stings", "negative"),
    ("the shipment arrives on thursday", "neutral"),
    ("here's the spreadsheet you requested", "neutral"),
    ("the meeting has been moved to room 4", "neutral"),
    ("the file size is about 12 megabytes", "neutral"),
    ("the store closes at nine", "neutral"),
    ("there are three items left in stock", "neutral"),
    ("the recipe calls for two cups of flour", "neutral"),
    ("the bus arrives every fifteen minutes", "neutral"),
    ("the document has been updated accordingly", "neutral"),
    ("the temperature reading is stable", "neutral"),
    ("the form requires a signature on page two", "neutral"),
    ("the package weighs about four pounds", "neutral"),
    ("the login page has a new layout", "neutral"),
    ("the report covers the last quarter", "neutral"),
    ("the settings menu is under the gear icon", "neutral"),
]
SENTIMENT_EXAMPLES.extend(SENTIMENT_EXAMPLES_EXTRA_3)

# A FOURTH supplementary batch (targeting +65% total dataset size).
SENTIMENT_EXAMPLES_EXTRA_4 = [
    ("i feel unstoppable after today", "positive"),
    ("this exceeded every expectation i had", "positive"),
    ("i'm bursting with pride right now", "positive"),
    ("everything just clicked into place perfectly", "positive"),
    ("i woke up feeling genuinely optimistic", "positive"),
    ("this has been such an uplifting week", "positive"),
    ("i'm overflowing with gratitude today", "positive"),
    ("what a triumphant end to the project", "positive"),
    ("i feel unusually at peace with everything", "positive"),
    ("this news made my entire month", "positive"),
    ("i'm on cloud nine after that call", "positive"),
    ("everything about today felt like a win", "positive"),
    ("i'm practically floating with excitement", "positive"),
    ("this turned my whole outlook around", "positive"),
    ("i feel so celebrated and appreciated right now", "positive"),
    ("i'm carrying a weight i can't put down", "negative"),
    ("this string of setbacks is exhausting", "negative"),
    ("i feel like i'm failing at everything lately", "negative"),
    ("this news left me completely hollow", "negative"),
    ("i can't seem to catch a break these days", "negative"),
    ("everything feels heavier than it should", "negative"),
    ("i'm running on fumes and it shows", "negative"),
    ("this disappointment is hard to shake off", "negative"),
    ("i feel like i'm constantly bracing for bad news", "negative"),
    ("today just chipped away at what was left of my patience", "negative"),
    ("i'm quietly falling apart over this", "negative"),
    ("nothing about this outcome sits right with me", "negative"),
    ("i feel so unseen in all of this", "negative"),
    ("this grief comes in waves i can't predict", "negative"),
    ("i'm bracing myself for more bad news", "negative"),
    ("the badge office is open until five today", "neutral"),
    ("the conference room seats twelve people", "neutral"),
    ("the update log lists all recent changes", "neutral"),
    ("the shuttle departs every twenty minutes", "neutral"),
    ("the warranty card is inside the box", "neutral"),
    ("the survey takes about five minutes", "neutral"),
    ("the folder contains last year's records", "neutral"),
    ("the software requires a restart to finish installing", "neutral"),
    ("the delivery window is between nine and noon", "neutral"),
    ("the manual covers setup and troubleshooting", "neutral"),
    ("the thermostat schedule can be adjusted in settings", "neutral"),
    ("the parking permit must be renewed annually", "neutral"),
    ("the report includes charts for each quarter", "neutral"),
    ("the ticket queue resets every morning", "neutral"),
    ("the building closes at eight on weekdays", "neutral"),
]
SENTIMENT_EXAMPLES.extend(SENTIMENT_EXAMPLES_EXTRA_4)

SENTIMENT_EXAMPLES_EXTRA_5 = [
    ("i'm so proud of how far we've come", "positive"),
    ("this small kindness made my whole day better", "positive"),
    ("i finally feel like i belong here", "positive"),
    ("everything is finally starting to feel manageable", "positive"),
    ("i'm genuinely excited for what's next", "positive"),
    ("this moment feels like a fresh start", "positive"),
    ("i can't stop smiling about the news", "positive"),
    ("i feel completely supported right now", "positive"),
    ("this is the encouragement i needed today", "positive"),
    ("i'm walking away from this feeling hopeful", "positive"),
    ("i feel like i'm constantly letting people down", "negative"),
    ("this exhaustion has settled into something deeper", "negative"),
    ("i keep bracing for the next thing to go wrong", "negative"),
    ("this loneliness has been hard to explain", "negative"),
    ("i feel stuck and i don't know how to move forward", "negative"),
    ("today drained every bit of motivation i had", "negative"),
    ("i'm tired of pretending everything is fine", "negative"),
    ("this setback feels bigger than it probably is", "negative"),
    ("i feel like i'm always the one who has to adjust", "negative"),
    ("this has been a quietly difficult season", "negative"),
    ("the badge scanner logs entries automatically", "neutral"),
    ("the recycling is collected every other tuesday", "neutral"),
    ("the elevator inspection certificate is posted inside", "neutral"),
    ("the shared drive syncs every fifteen minutes", "neutral"),
    ("the lease renewal notice arrives by mail", "neutral"),
    ("the printer supports both color and black and white", "neutral"),
    ("the schedule updates automatically each semester", "neutral"),
]
SENTIMENT_EXAMPLES.extend(SENTIMENT_EXAMPLES_EXTRA_5)

SENTIMENT_EXAMPLES_EXTRA_6 = [
    ("i feel like i can finally breathe again", "positive"),
    ("this small victory means so much to me", "positive"),
    ("i'm honestly just so content right now", "positive"),
    ("everything about this moment feels right", "positive"),
    ("i feel lighter than i have in weeks", "positive"),
    ("i'm quietly falling apart and don't know why", "negative"),
    ("this ache just won't go away today", "negative"),
    ("i feel like i'm disappointing everyone around me", "negative"),
    ("this week has chipped away at my resolve", "negative"),
    ("i feel so far from okay right now", "negative"),
    ("the invoice template is stored in the shared folder", "neutral"),
    ("the building's fire drill is scheduled for noon", "neutral"),
    ("the app update notes are listed below", "neutral"),
    ("the parking validation machine is by the entrance", "neutral"),
    ("the quarterly report is due on the fifteenth", "neutral"),
]
SENTIMENT_EXAMPLES.extend(SENTIMENT_EXAMPLES_EXTRA_6)


class _TextVocab:
    """
    A small hand-built vocabulary shared by both neural networks' torch
    backend: maps whitespace-tokenized lowercase words to integer ids,
    with <pad> (id 0) and <unk> (id 1) reserved tokens. This replaces
    TF-IDF for the torch path - instead of sparse one-hot-ish counts,
    each word gets a dense, LEARNED embedding vector (see nn.Embedding
    in the model classes below), trained jointly with the classifier so
    semantically related words can end up with similar vectors even if
    they never appeared together in training.
    """

    PAD, UNK = "<pad>", "<unk>"

    def __init__(self, texts, max_len=14):
        self.max_len = max_len
        vocab = set()
        for t in texts:
            vocab.update(self._tokenize(t))
        self.itos = [self.PAD, self.UNK] + sorted(vocab)
        self.stoi = {w: i for i, w in enumerate(self.itos)}

    @staticmethod
    def _tokenize(text):
        return text.lower().replace("'", " ").replace(",", " ").replace(":", " ").split()

    def encode(self, text):
        tokens = self._tokenize(text)[: self.max_len]
        ids = [self.stoi.get(tok, self.stoi[self.UNK]) for tok in tokens]
        ids += [self.stoi[self.PAD]] * (self.max_len - len(ids))
        return ids

    def __len__(self):
        return len(self.itos)


class _CharVocab:
    """
    Character-level counterpart to _TextVocab, added for the SAME
    reason the sklearn backend gained a character-n-gram TF-IDF feature
    set alongside word-level TF-IDF (see _fit_sklearn): character-level
    signal catches shared word roots and spelling patterns ("happ-" in
    "happy"/"happiness", "tire-" in "tired"/"tiring") that whole-word
    tokenization misses on a small vocabulary. The torch models use
    this via a SEPARATE nn.Embedding + mean-pool branch that gets
    concatenated with the word-embedding branch before the classifier
    head (see _IntentNet/_SentimentNet below) - two independent learned
    representations of the same text, fused together, mirroring the
    FeatureUnion(word, char) approach on the sklearn side.
    """

    PAD, UNK = "<pad>", "<unk>"

    def __init__(self, texts, max_len=48):
        self.max_len = max_len
        vocab = set()
        for t in texts:
            vocab.update(self._tokenize(t))
        self.itos = [self.PAD, self.UNK] + sorted(vocab)
        self.stoi = {c: i for i, c in enumerate(self.itos)}

    @staticmethod
    def _tokenize(text):
        return list(text.lower())

    def encode(self, text):
        chars = self._tokenize(text)[: self.max_len]
        ids = [self.stoi.get(c, self.stoi[self.UNK]) for c in chars]
        ids += [self.stoi[self.PAD]] * (self.max_len - len(ids))
        return ids

    def __len__(self):
        return len(self.itos)


class _BaseNeuralClassifier:
    """
    Shared scaffolding for NeuralIntentClassifier and SentimentClassifier:
    backend selection, train/val splitting, early stopping, persistence
    of user-verified corrections, and the predict() confidence API.
    Subclasses provide their example dataset and a couple of small
    backend-specific hooks (the torch nn.Module architecture and the
    sklearn estimator to use), since the two networks share almost
    everything except their training data and head sizes.
    """

    # Raised from 0.40 to 0.45 after the word+char FeatureUnion upgrade
    # (Section 6G) made the model more confident on gibberish/nonsense
    # inputs - measured via held-out validation: 0.45 keeps exactly the
    # same number of CORRECT predictions as 0.40 (59/63 in testing) while
    # rejecting more low-quality guesses, so this is a free improvement,
    # not a tradeoff. Going higher (0.50+) starts losing real correct
    # predictions, so this is the validated sweet spot, not a guess.
    CONFIDENCE_THRESHOLD = 0.45
    # Widened from the original 32/64 now that the training set has grown
    # to ~700 examples (see NN_INTENT_EXAMPLES_EXTRA above): a bigger
    # dataset can support a bigger network without immediately overfitting,
    # and held-out validation accuracy (see 'nn stats') is checked after
    # every fit specifically to catch it if that stops being true.
    EMBED_DIM = 48
    HIDDEN_DIM = 96
    MAX_EPOCHS = 150
    EARLY_STOP_PATIENCE = 20
    VAL_FRACTION = 0.18

    def __init__(self, training_path: str, base_examples, db: "Database" = None):
        self.training_path = training_path
        self.db = db
        self.backend = "torch" if TORCH_AVAILABLE else "sklearn"
        self.base_examples = list(base_examples)
        self.corrections = []
        # A richer persisted record than just the raw corrections: every
        # time this model is fit (startup or retrain), we append a
        # timestamped snapshot of {num_examples, val_accuracy, backend}
        # to training_history, persisted alongside corrections (in the
        # shared Database, Section 1B, when one's provided - falls back
        # to the older standalone JSON file otherwise). This turns
        # 'nn stats' from a single current number into an actual trend
        # over time, and survives across sessions like corrections do.
        self.training_history = []
        self._load_corrections()

        self.vocab = None              # torch backend
        self.char_vocab = None         # torch backend (character-level branch)
        self.vectorizer = None         # sklearn backend
        self.label_list = []
        self.label_to_idx = {}
        self.model = None
        self.last_training_loss = None
        self.last_val_accuracy = None
        self.last_train_size = None
        self.last_val_size = None

        self._fit()

    # ---- persistence --------------------------------------------------
    #
    # Each concrete subclass (NeuralIntentClassifier, SentimentClassifier)
    # sets CLASSIFIER_NAME to "intent" / "sentiment" - used as the
    # discriminator column when corrections/training_history are stored
    # in the shared Database's tables (both classifiers' rows live in
    # the same two tables, distinguished by this name).

    CLASSIFIER_NAME = "base"  # overridden by subclasses

    def _load_corrections(self):
        if self.db is not None:
            self.corrections = self.db.get_corrections(self.CLASSIFIER_NAME)
            self.training_history = self.db.get_training_history(self.CLASSIFIER_NAME)
            return

        # No shared Database provided - fall back to the original
        # standalone-JSON-file behavior, for callers that still
        # construct this class the old way.
        if os.path.exists(self.training_path):
            try:
                with open(self.training_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                self.corrections = [tuple(x) for x in data.get("corrections", [])]
                self.training_history = data.get("training_history", [])
            except (json.JSONDecodeError, OSError):
                self.corrections = []
                self.training_history = []

    def _save_corrections(self):
        if self.db is not None:
            return  # Database writes happen immediately in add_correction()
                     # and _record_training_snapshot() below - nothing to flush.
        try:
            with open(self.training_path, "w", encoding="utf-8") as f:
                json.dump(
                    {"corrections": self.corrections, "training_history": self.training_history},
                    f, indent=2, ensure_ascii=False,
                )
        except OSError as e:
            print(f"[warning] could not save classifier corrections: {e}")

    def _record_training_snapshot(self):
        """Appends a timestamped snapshot of this fit's results to
        training_history and persists it, so accuracy over time is a
        real, inspectable record rather than just the latest number."""
        snapshot = {
            "timestamp": dt.datetime.now().isoformat(timespec="seconds"),
            "backend": self.backend,
            "num_base_examples": len(self.base_examples),
            "num_corrections": len(self.corrections),
            "val_accuracy": self.last_val_accuracy,
            "training_loss": self.last_training_loss,
        }

        if self.db is not None:
            self.db.add_training_snapshot(
                self.CLASSIFIER_NAME, self.backend, len(self.base_examples),
                len(self.corrections), self.last_val_accuracy, self.last_training_loss,
            )
            self.training_history = self.db.get_training_history(self.CLASSIFIER_NAME)
            return

        self.training_history.append(snapshot)
        # Keep the history bounded so the file doesn't grow forever.
        if len(self.training_history) > 50:
            self.training_history = self.training_history[-50:]
        self._save_corrections()

    def _all_examples(self):
        return self.base_examples + self.corrections

    # ---- fitting --------------------------------------------------------

    def _fit(self):
        examples = self._all_examples()
        texts = [t for t, _ in examples]
        labels = [l for _, l in examples]

        self.label_list = sorted(set(labels))
        self.label_to_idx = {lab: i for i, lab in enumerate(self.label_list)}
        y = np.array([self.label_to_idx[l] for l in labels], dtype=np.int64)

        # A meaningful held-out split needs enough examples per class;
        # with very few examples (e.g. right after a single fresh
        # correction with no base data) we skip splitting and just
        # report training-set performance instead of a misleading
        # near-empty validation score.
        can_split = len(texts) >= 20 and min(np.bincount(y)) >= 2
        if can_split:
            idx_train, idx_val = train_test_split(
                np.arange(len(texts)), test_size=self.VAL_FRACTION,
                random_state=42, stratify=y,
            )
        else:
            idx_train = np.arange(len(texts))
            idx_val = np.arange(len(texts))

        if self.backend == "torch":
            self._fit_torch(texts, y, idx_train, idx_val)
        else:
            self._fit_sklearn(texts, y, idx_train, idx_val)

        self.last_train_size = len(idx_train)
        self.last_val_size = len(idx_val)
        self._record_training_snapshot()

    def _fit_torch(self, texts, y, idx_train, idx_val):
        self.vocab = _TextVocab(texts)
        self.char_vocab = _CharVocab(texts)
        X_word = np.array([self.vocab.encode(t) for t in texts], dtype=np.int64)
        X_char = np.array([self.char_vocab.encode(t) for t in texts], dtype=np.int64)
        num_classes = len(self.label_list)

        model = self._build_torch_model(len(self.vocab), len(self.char_vocab), num_classes)

        optimizer = optim.Adam(model.parameters(), lr=0.005, weight_decay=1e-5)
        scheduler = optim.lr_scheduler.StepLR(optimizer, step_size=40, gamma=0.5)
        criterion = nn.CrossEntropyLoss()

        Xw_train_t = torch.from_numpy(X_word[idx_train])
        Xc_train_t = torch.from_numpy(X_char[idx_train])
        y_train_t = torch.from_numpy(y[idx_train])
        Xw_val_t = torch.from_numpy(X_word[idx_val])
        Xc_val_t = torch.from_numpy(X_char[idx_val])
        y_val_t = torch.from_numpy(y[idx_val])

        best_val_acc = -1.0
        best_state = None
        patience_counter = 0
        final_loss = None

        for _epoch in range(self.MAX_EPOCHS):
            model.train()
            optimizer.zero_grad()
            outputs = model(Xw_train_t, Xc_train_t)
            loss = criterion(outputs, y_train_t)
            loss.backward()
            optimizer.step()
            scheduler.step()
            final_loss = float(loss.item())

            model.eval()
            with torch.no_grad():
                val_outputs = model(Xw_val_t, Xc_val_t)
                val_preds = val_outputs.argmax(dim=1)
                val_acc = (val_preds == y_val_t).float().mean().item()

            if val_acc > best_val_acc:
                best_val_acc = val_acc
                best_state = {k: v.clone() for k, v in model.state_dict().items()}
                patience_counter = 0
            else:
                patience_counter += 1
                if patience_counter >= self.EARLY_STOP_PATIENCE:
                    break

        if best_state is not None:
            model.load_state_dict(best_state)
        model.eval()

        self.model = model
        self.last_training_loss = final_loss
        self.last_val_accuracy = float(best_val_acc) if best_val_acc >= 0 else None

    def _fit_sklearn(self, texts, y, idx_train, idx_val):
        cache_key = model_cache_key(
            type(self).__name__ + "_sklearn_v1", texts, list(map(int, y)),
            list(map(int, idx_train)), list(map(int, idx_val)),
            self._sklearn_ngram_range(), self._sklearn_use_char_features(),
            self._sklearn_hidden_layers(), self._sklearn_alpha(),
        )
        cached = load_cached_model(cache_key)
        if cached is not None:
            self.vectorizer = cached["vectorizer"]
            self.model = cached["model"]
            self.last_training_loss = cached["last_training_loss"]
            self.last_val_accuracy = cached["last_val_accuracy"]
            return

        # STRONGER FEATURES: combine WORD-level and CHARACTER-level
        # TF-IDF via sklearn's FeatureUnion, rather than word n-grams
        # alone. Measured via repeated stratified cross-validation on
        # the intent dataset: word-unigrams alone ~79%, char n-grams
        # (2-4, word-boundary-aware) alone ~80%, the two COMBINED ~82%
        # - a real, repeatable gain, not a single lucky split. Character
        # n-grams capture shared word roots/spelling patterns (e.g.
        # "happ-" across "happy"/"happiness", "tire-" across
        # "tired"/"tiring") that word-level unigrams miss when the
        # vocabulary is this sparse, so the two feature views are
        # complementary rather than redundant.
        transformers = [
            ("word", TfidfVectorizer(ngram_range=self._sklearn_ngram_range(), sublinear_tf=True, min_df=1)),
        ]
        if self._sklearn_use_char_features():
            transformers.append(
                ("char", TfidfVectorizer(analyzer="char_wb", ngram_range=(2, 4), sublinear_tf=True, min_df=2))
            )
        self.vectorizer = FeatureUnion(transformers)
        X = self.vectorizer.fit_transform(texts)
        if hasattr(X, "toarray"):
            X = X.toarray()
        X = X.astype(np.float32)

        with warnings.catch_warnings():
            warnings.simplefilter("ignore", category=ConvergenceWarning)
            model = MLPClassifier(
                hidden_layer_sizes=self._sklearn_hidden_layers(),
                activation="relu",
                solver="adam",
                alpha=self._sklearn_alpha(),
                max_iter=3000,
                random_state=42,
            )
            model.fit(X[idx_train], y[idx_train])

        val_preds = model.predict(X[idx_val])
        self.model = model
        self.last_training_loss = float(model.loss_)
        self.last_val_accuracy = float(accuracy_score(y[idx_val], val_preds))
        save_cached_model(cache_key, {
            "vectorizer": self.vectorizer, "model": self.model,
            "last_training_loss": self.last_training_loss, "last_val_accuracy": self.last_val_accuracy,
        })

    # ---- inference --------------------------------------------------------

    def predict(self, text: str):
        """Returns (label, confidence) or None if below CONFIDENCE_THRESHOLD."""
        if not text.strip():
            return None

        if self.backend == "torch":
            word_ids = np.array([self.vocab.encode(text)], dtype=np.int64)
            char_ids = np.array([self.char_vocab.encode(text)], dtype=np.int64)
            with torch.no_grad():
                logits = self.model(torch.from_numpy(word_ids), torch.from_numpy(char_ids))
                probs = torch.softmax(logits, dim=1).numpy()[0]
        else:
            X = self.vectorizer.transform([text])
            if hasattr(X, "toarray"):
                X = X.toarray()
            X = X.astype(np.float32)
            probs = self.model.predict_proba(X)[0]

        best_idx = int(np.argmax(probs))
        best_conf = float(probs[best_idx])
        if best_conf < self.CONFIDENCE_THRESHOLD:
            return None
        return self.label_list[best_idx], best_conf

    # ---- online learning from user-verified corrections -------------------

    def add_correction(self, text: str, correct_label: str):
        self.corrections.append((text, correct_label))
        if self.db is not None:
            self.db.add_correction(self.CLASSIFIER_NAME, text, correct_label)
        else:
            self._save_corrections()

    def retrain(self):
        """Refits the model; returns (num_corrections, val_accuracy_before, val_accuracy_after)."""
        acc_before = self.last_val_accuracy
        self._fit()
        return len(self.corrections), acc_before, self.last_val_accuracy

    def known_labels(self):
        return list(self.label_list)

    # ---- hooks for subclasses ----------------------------------------------

    def _build_torch_model(self, word_vocab_size, char_vocab_size, num_classes):
        raise NotImplementedError

    def _sklearn_hidden_layers(self):
        return (64, 32)

    def _sklearn_ngram_range(self):
        return (1, 2)

    def _sklearn_alpha(self):
        return 0.01

    def _sklearn_use_char_features(self):
        """Whether to add character n-gram TF-IDF features alongside
        word-level ones (see _fit_sklearn). Defaults to True since this
        measurably helped both classifiers in testing; subclasses can
        override if their own measurements say otherwise."""
        return True


class NeuralIntentClassifier(_BaseNeuralClassifier):
    """
    Classifies free-form user text into an intent label - both ordinary
    conversation (greeting, farewell, feelings, ...) and bot commands
    (tell_joke, todo_add, ...). See module docstring above for the full
    architecture description.
    """

    CLASSIFIER_NAME = "intent"

    def __init__(self, training_path: str, db: "Database" = None):
        super().__init__(training_path, NN_INTENT_EXAMPLES, db=db)

    def _build_torch_model(self, word_vocab_size, char_vocab_size, num_classes):
        embed_dim, hidden_dim = self.EMBED_DIM, self.HIDDEN_DIM
        char_embed_dim = max(16, embed_dim // 2)

        class _ResidualBlock(nn.Module):
            """
            A small residual (skip-connection) block: Linear -> LayerNorm
            -> GELU -> Dropout -> Linear, with the block's INPUT added
            back to its output before returning. This is the standard
            trick that lets extra depth actually help instead of hurt:
            on the sklearn side, stacking plain hidden layers measurably
            HURT accuracy on this dataset size (a 3-layer plain MLP
            dropped to ~69% vs ~79% for one layer, since gradients and
            optimization get harder without a skip path and the model
            just has more ways to overfit). The residual connection
            means each block only needs to learn a small REFINEMENT to
            its input rather than reconstruct the signal from scratch,
            which is far more robust on a small dataset.
            """

            def __init__(self, dim, dropout=0.25):
                super().__init__()
                self.fc1 = nn.Linear(dim, dim)
                self.norm1 = nn.LayerNorm(dim)
                self.act = nn.GELU()
                self.dropout = nn.Dropout(dropout)
                self.fc2 = nn.Linear(dim, dim)
                self.norm2 = nn.LayerNorm(dim)

            def forward(self, x):
                residual = x
                h = self.fc1(x)
                h = self.norm1(h)
                h = self.act(h)
                h = self.dropout(h)
                h = self.fc2(h)
                h = self.norm2(h)
                return self.act(h + residual)

        class _IntentNet(nn.Module):
            """
            DUAL-BRANCH architecture: a WORD-level branch (nn.Embedding
            over whitespace tokens, mean-pooled) and a CHARACTER-level
            branch (nn.Embedding over characters, mean-pooled) are each
            processed independently, then CONCATENATED before the
            shared classifier head - the torch equivalent of the
            FeatureUnion(word_tfidf, char_tfidf) combination that
            measurably improved the sklearn backend (~79% to ~82% via
            cross-validation). The two branches learn complementary
            information: the word branch captures vocabulary/meaning,
            the character branch captures shared spelling/word-root
            patterns that help even when the exact word wasn't seen in
            training (e.g. "tiring" sharing structure with "tired").
            After fusion, FIVE residual blocks (see _ResidualBlock above,
            widened from an earlier 3-block version alongside the
            larger training set) give the network real depth without
            the overfitting that plain stacked layers caused in
            testing, regularized by LayerNorm + Dropout in every block
            plus weight_decay on the optimizer (set in _fit_torch).
            """

            def __init__(self, word_vocab_size, char_vocab_size, word_embed_dim,
                         char_embed_dim, hidden_dim, num_classes):
                super().__init__()
                self.word_embedding = nn.Embedding(word_vocab_size, word_embed_dim, padding_idx=0)
                self.char_embedding = nn.Embedding(char_vocab_size, char_embed_dim, padding_idx=0)

                fusion_dim = word_embed_dim + char_embed_dim
                self.fusion_proj = nn.Linear(fusion_dim, hidden_dim)
                self.fusion_norm = nn.LayerNorm(hidden_dim)
                self.fusion_act = nn.GELU()
                self.fusion_dropout = nn.Dropout(0.3)

                self.res_block1 = _ResidualBlock(hidden_dim, dropout=0.25)
                self.res_block2 = _ResidualBlock(hidden_dim, dropout=0.25)
                self.res_block3 = _ResidualBlock(hidden_dim, dropout=0.25)
                self.res_block4 = _ResidualBlock(hidden_dim, dropout=0.25)
                self.res_block5 = _ResidualBlock(hidden_dim, dropout=0.25)

                self.head = nn.Linear(hidden_dim, num_classes)

            @staticmethod
            def _mean_pool(embedded, token_ids):
                mask = (token_ids != 0).unsqueeze(-1).float()
                summed = (embedded * mask).sum(dim=1)
                counts = mask.sum(dim=1).clamp(min=1.0)
                return summed / counts

            def forward(self, word_ids, char_ids):
                word_embedded = self.word_embedding(word_ids)
                word_pooled = self._mean_pool(word_embedded, word_ids)

                char_embedded = self.char_embedding(char_ids)
                char_pooled = self._mean_pool(char_embedded, char_ids)

                fused = torch.cat([word_pooled, char_pooled], dim=1)
                h = self.fusion_proj(fused)
                h = self.fusion_norm(h)
                h = self.fusion_act(h)
                h = self.fusion_dropout(h)

                h = self.res_block1(h)
                h = self.res_block2(h)
                h = self.res_block3(h)
                h = self.res_block4(h)
                h = self.res_block5(h)

                return self.head(h)

        torch.manual_seed(42)
        return _IntentNet(word_vocab_size, char_vocab_size, embed_dim, char_embed_dim,
                           hidden_dim, num_classes)

    def _sklearn_hidden_layers(self):
        # Widened to a deeper stack alongside the torch side's 5
        # residual blocks. Earlier tuning notes found a plain 3-layer
        # MLP dropped to ~69% vs ~79% for one layer on the
        # then-smaller dataset - sklearn's MLPClassifier has no
        # residual/skip-connection option, so that risk is real and
        # still applies here. This is being widened anyway per an
        # explicit request for depth across every network; the
        # substantially larger training set (NN_INTENT_EXAMPLES_EXTRA2,
        # added alongside this change) helps offset some of that
        # overfitting risk, but 'nn stats' should be checked after
        # retraining to confirm validation accuracy didn't regress -
        # if it did, the torch backend (which handles depth far better
        # via its residual blocks) is the one actually carrying this
        # feature.
        return (128, 96, 64, 32)

    def _sklearn_ngram_range(self):
        # Word-level features use unigrams only (bigrams were too
        # sparse on these short phrases - see earlier tuning notes).
        # Character n-grams are added separately and unconditionally by
        # _fit_sklearn (see _sklearn_use_char_features) - those are what
        # pushed accuracy from ~79% to ~82%, since they catch shared
        # word roots/spelling that word-level unigrams can't.
        return (1, 1)

    def _sklearn_alpha(self):
        return 0.015


class SentimentClassifier(_BaseNeuralClassifier):
    """
    A SECOND, independent neural network: classifies free-form user
    text into a coarse mood (positive / negative / neutral). This does
    NOT decide what the bot should DO (that's NeuralIntentClassifier's
    job) - it only colors HOW a response is phrased, by letting the
    chatbot pick a warmer or more upbeat variant of a reply based on
    detected mood. Smaller than the intent classifier (3 classes, less
    data) so it uses a slightly smaller hidden layer.
    """

    # Also widened slightly (from 24/32) alongside the intent net now that
    # SENTIMENT_EXAMPLES_EXTRA gives it more examples per class to train on.
    EMBED_DIM = 32
    HIDDEN_DIM = 48
    CLASSIFIER_NAME = "sentiment"

    def __init__(self, training_path: str, db: "Database" = None):
        super().__init__(training_path, SENTIMENT_EXAMPLES, db=db)

    def _build_torch_model(self, word_vocab_size, char_vocab_size, num_classes):
        embed_dim, hidden_dim = self.EMBED_DIM, self.HIDDEN_DIM
        char_embed_dim = max(12, embed_dim // 2)

        class _SentimentNet(nn.Module):
            """
            Same dual-branch (word embedding + char embedding) fusion
            idea as NeuralIntentClassifier's _IntentNet, now widened to
            FOUR stacked residual refinement blocks (up from one)
            alongside the larger SENTIMENT_EXAMPLES_EXTRA2 training set
            added at the same time - each block learns a small GELU +
            Dropout correction to its input with a skip connection back
            to it, the same depth-without-overfitting trick used in
            _IntentNet's _ResidualBlock.
            """

            def __init__(self, word_vocab_size, char_vocab_size, word_embed_dim,
                         char_embed_dim, hidden_dim, num_classes):
                super().__init__()
                self.word_embedding = nn.Embedding(word_vocab_size, word_embed_dim, padding_idx=0)
                self.char_embedding = nn.Embedding(char_vocab_size, char_embed_dim, padding_idx=0)

                fusion_dim = word_embed_dim + char_embed_dim
                self.fusion_proj = nn.Linear(fusion_dim, hidden_dim)
                self.fusion_act = nn.ReLU()
                self.fusion_dropout = nn.Dropout(0.25)

                # Four lightweight residual refinement steps (up from
                # one): each learns a small correction to the fused
                # representation rather than overwriting it outright.
                self.refine_fc1 = nn.Linear(hidden_dim, hidden_dim)
                self.refine_act1 = nn.GELU()
                self.refine_dropout1 = nn.Dropout(0.2)

                self.refine_fc2 = nn.Linear(hidden_dim, hidden_dim)
                self.refine_act2 = nn.GELU()
                self.refine_dropout2 = nn.Dropout(0.2)

                self.refine_fc3 = nn.Linear(hidden_dim, hidden_dim)
                self.refine_act3 = nn.GELU()
                self.refine_dropout3 = nn.Dropout(0.2)

                self.refine_fc4 = nn.Linear(hidden_dim, hidden_dim)
                self.refine_act4 = nn.GELU()
                self.refine_dropout4 = nn.Dropout(0.2)

                self.head = nn.Linear(hidden_dim, num_classes)

            @staticmethod
            def _mean_pool(embedded, token_ids):
                mask = (token_ids != 0).unsqueeze(-1).float()
                summed = (embedded * mask).sum(dim=1)
                counts = mask.sum(dim=1).clamp(min=1.0)
                return summed / counts

            def _refine(self, h, fc, act, dropout):
                residual = h
                refined = fc(h)
                refined = act(refined)
                refined = dropout(refined)
                return refined + residual

            def forward(self, word_ids, char_ids):
                word_pooled = self._mean_pool(self.word_embedding(word_ids), word_ids)
                char_pooled = self._mean_pool(self.char_embedding(char_ids), char_ids)

                fused = torch.cat([word_pooled, char_pooled], dim=1)
                h = self.fusion_proj(fused)
                h = self.fusion_act(h)
                h = self.fusion_dropout(h)

                h = self._refine(h, self.refine_fc1, self.refine_act1, self.refine_dropout1)
                h = self._refine(h, self.refine_fc2, self.refine_act2, self.refine_dropout2)
                h = self._refine(h, self.refine_fc3, self.refine_act3, self.refine_dropout3)
                h = self._refine(h, self.refine_fc4, self.refine_act4, self.refine_dropout4)

                return self.head(h)

        torch.manual_seed(7)
        return _SentimentNet(word_vocab_size, char_vocab_size, embed_dim, char_embed_dim,
                              hidden_dim, num_classes)

    def _sklearn_hidden_layers(self):
        # Widened from a single 24-unit layer alongside the torch
        # side's 4 residual refinement blocks, per an explicit request
        # for depth across every network. Same caveat as the intent
        # classifier's sklearn fallback: sklearn's MLPClassifier has no
        # skip connections, so depth here is more overfitting-prone
        # than the torch backend - check 'nn stats' after retraining.
        return (48, 32, 24)

    def _sklearn_ngram_range(self):
        # Unlike the intent classifier, BIGRAMS measurably help here
        # (~58% vs ~56% for unigrams via 5-fold CV) - sentiment depends
        # more on short phrase patterns ("not having a great day") than
        # on isolated words, so losing word-order information hurts
        # more than the extra sparsity costs at this dataset size.
        return (1, 2)


# ==============================================================================
# SECTION 6H: SMART SUGGESTIONS (TensorFlow/Keras, distinct task)
# ==============================================================================
#
# SmartSuggestionEngine predicts a likely NEXT intent given the CURRENT
# one - a sequence/transition prediction problem, genuinely different
# from the two PyTorch networks above (which classify the text of the
# CURRENT message, not what's likely to come next). This is why it's
# a separate model on a separate backend, rather than a duplicate of
# the intent classifier: it answers a different question ("what will
# they probably want next") using different training data (transition
# pairs between intents, not example phrases).
#
# Backend selection:
#   - If TensorFlow/Keras is installed, trains a small
#     keras.Sequential model (Embedding -> Flatten -> Dense(relu) ->
#     Dropout -> Dense(softmax)) with model.fit(), real epochs, and a
#     real validation split/accuracy curve via Keras's own tooling.
#   - If TensorFlow is NOT installed, falls back to a simple frequency
#     table built from the same transition data - so "you might also
#     want to ask..." suggestions still work, just without the Keras
#     model backing them.
#
# This produces the "you might also want to ask..." suggestion chips
# shown after a response (see ChatBot.respond()'s use of
# self.smart_suggestions), which is the most directly "magical-feeling"
# UX addition in this whole upgrade: the bot proactively offers a next
# step instead of waiting to be asked.

# Synthetic-but-plausible (current_intent, next_intent, weight) triples,
# modeling realistic flows through the bot's command set. Weights
# reflect how common/sensible each transition is, not scraped data.
INTENT_TRANSITIONS = [
    ("greeting", "how_are_you", 8),
    ("greeting", "tell_joke", 5),
    ("greeting", "help", 4),
    ("greeting", "ask_my_name", 3),
    ("how_are_you", "tell_joke", 4),
    ("how_are_you", "feelings_happy", 3),
    ("how_are_you", "tell_story", 3),
    ("tell_joke", "tell_joke", 6),
    ("tell_joke", "tell_quote", 4),
    ("tell_joke", "tell_riddle", 4),
    ("tell_quote", "tell_joke", 3),
    ("tell_quote", "tell_riddle", 3),
    ("tell_riddle", "tell_riddle", 5),
    ("tell_riddle", "tell_trivia", 4),
    ("tell_trivia", "tell_trivia", 5),
    ("tell_trivia", "tell_riddle", 3),
    ("tell_story", "tell_story", 4),
    ("tell_story", "write_poem_general", 3),
    ("write_haiku", "write_poem_general", 4),
    ("write_poem_general", "write_haiku", 3),
    ("write_poem_general", "write_acrostic", 3),
    ("todo_add", "todo_list", 7),
    ("todo_list", "todo_add", 5),
    ("current_time", "current_date", 5),
    ("current_date", "current_time", 4),
    ("current_date", "days_until_holiday", 3),
    ("feelings_sad", "tell_joke", 5),
    ("feelings_sad", "tell_quote", 4),
    ("feelings_tired", "feelings_sad", 2),
    ("feelings_happy", "tell_joke", 3),
    ("hangman_start", "hangman_start", 4),
    ("help", "tell_joke", 3),
    ("help", "tell_story", 3),
    ("help", "todo_list", 2),
    ("ask_bot_name", "ask_my_name", 3),
    ("ask_my_name", "remember_fact", 3),
    ("remember_fact", "ask_my_name", 2),
    ("thanks", "farewell", 4),
    ("thanks", "greeting", 2),
]

# Human-readable phrasing for each transition target, used to render
# the suggestion as something the user could actually type.
_SUGGESTION_PHRASING = {
    "how_are_you": "ask how I'm doing",
    "tell_joke": "ask for another joke",
    "help": "type 'help' to see what I can do",
    "ask_my_name": "ask if I remember your name",
    "feelings_happy": "tell me how you're feeling",
    "tell_story": "ask for a story",
    "tell_quote": "ask for an inspiring quote",
    "tell_riddle": "ask for a riddle",
    "tell_trivia": "ask for a trivia question",
    "write_poem_general": "ask for a poem",
    "write_haiku": "ask for a haiku",
    "write_acrostic": "ask for an acrostic poem",
    "todo_list": "ask to see your to-do list",
    "todo_add": "add something to your to-do list",
    "current_time": "ask what time it is",
    "current_date": "ask for today's date",
    "days_until_holiday": "ask how many days until a holiday",
    "feelings_sad": "tell me how you're feeling",
    "hangman_start": "play another round of hangman",
    "ask_bot_name": "ask what my name is",
    "remember_fact": "tell me a fact to remember",
    "farewell": "say goodbye",
    "greeting": "say hello",
}


class SmartSuggestionEngine:
    """
    Predicts likely NEXT intents given the current one, to power
    proactive "you might also want to..." suggestions. See the Section
    6H module docstring above for why this is a distinct task from the
    PyTorch classifiers and gets its own (Keras-backed) model.
    """

    def __init__(self):
        labels = sorted(set([t[0] for t in INTENT_TRANSITIONS] + [t[1] for t in INTENT_TRANSITIONS]))
        self.vocab = {l: i for i, l in enumerate(labels)}
        self.idx_to_label = {i: l for l, i in self.vocab.items()}
        self.backend = "tensorflow" if TENSORFLOW_AVAILABLE else "frequency_table"
        self.model = None
        self.freq_table = None
        self.last_training_info = None
        self._fit()

    def _build_training_arrays(self):
        X, y = [], []
        for current, nxt, weight in INTENT_TRANSITIONS:
            for _ in range(weight):
                X.append(self.vocab[current])
                y.append(self.vocab[nxt])
        return np.array(X, dtype=np.int64), np.array(y, dtype=np.int64)

    def _fit(self):
        X, y = self._build_training_arrays()
        if self.backend == "tensorflow":
            self._fit_keras(X, y)
        else:
            self._fit_frequency_table()

    def _fit_keras(self, X, y):
        num_classes = len(self.vocab)
        tf.random.set_seed(42)

        # Built with the FUNCTIONAL API (rather than Sequential) so the
        # model is an explicit graph of named layers - this is the same
        # network conceptually, just using more of Keras's real surface
        # area: L2-regularized Dense layers, BatchNormalization between
        # them, and training callbacks (EarlyStopping +
        # ReduceLROnPlateau) instead of a fixed epoch count. Widened
        # from 2 to 5 Dense layers (128->96->64->48->32) alongside the
        # broader push for depth across every network in this file.
        inputs = keras.Input(shape=(1,), name="current_intent_id")
        x = keras.layers.Embedding(input_dim=num_classes, output_dim=16, name="intent_embedding")(inputs)
        x = keras.layers.Flatten()(x)
        x = keras.layers.Dense(
            128, activation="relu", kernel_regularizer=keras.regularizers.l2(1e-4), name="dense_1"
        )(x)
        x = keras.layers.BatchNormalization()(x)
        x = keras.layers.Dropout(0.25)(x)
        x = keras.layers.Dense(
            96, activation="relu", kernel_regularizer=keras.regularizers.l2(1e-4), name="dense_2"
        )(x)
        x = keras.layers.BatchNormalization()(x)
        x = keras.layers.Dropout(0.2)(x)
        x = keras.layers.Dense(
            64, activation="relu", kernel_regularizer=keras.regularizers.l2(1e-4), name="dense_3"
        )(x)
        x = keras.layers.BatchNormalization()(x)
        x = keras.layers.Dropout(0.2)(x)
        x = keras.layers.Dense(
            48, activation="relu", kernel_regularizer=keras.regularizers.l2(1e-4), name="dense_4"
        )(x)
        x = keras.layers.Dropout(0.15)(x)
        x = keras.layers.Dense(
            32, activation="relu", kernel_regularizer=keras.regularizers.l2(1e-4), name="dense_5"
        )(x)
        x = keras.layers.Dropout(0.15)(x)
        outputs = keras.layers.Dense(num_classes, activation="softmax", name="next_intent")(x)

        model = keras.Model(inputs=inputs, outputs=outputs, name="smart_suggestion_net")
        model.compile(
            optimizer=keras.optimizers.Adam(learning_rate=0.01),
            loss="sparse_categorical_crossentropy",
            metrics=["accuracy"],
        )

        callbacks = [
            keras.callbacks.EarlyStopping(monitor="val_loss", patience=10, restore_best_weights=True),
            keras.callbacks.ReduceLROnPlateau(monitor="val_loss", factor=0.5, patience=5, min_lr=1e-5),
        ]
        history = model.fit(
            X, y, epochs=100, verbose=0, validation_split=0.15, callbacks=callbacks
        )

        self.model = model
        self.last_training_info = {
            "final_loss": float(history.history["loss"][-1]),
            "final_val_accuracy": float(history.history.get("val_accuracy", [0.0])[-1]),
            "epochs_trained": len(history.history["loss"]),
        }

    def _fit_frequency_table(self):
        table = {}
        for current, nxt, weight in INTENT_TRANSITIONS:
            table.setdefault(current, Counter())[nxt] += weight
        self.freq_table = table
        self.last_training_info = {"final_loss": None, "final_val_accuracy": None}

    def suggest(self, current_label: str, top_k: int = 2):
        """Returns up to top_k (label, score) suggestions for a likely next ask."""
        if current_label not in self.vocab:
            return []

        if self.backend == "tensorflow":
            idx = np.array([[self.vocab[current_label]]])
            probs = self.model.predict(idx, verbose=0)[0]
            ranked = np.argsort(probs)[::-1]
            results = []
            for i in ranked:
                label = self.idx_to_label[int(i)]
                if label == current_label:
                    continue
                results.append((label, float(probs[i])))
                if len(results) >= top_k:
                    break
            return results
        else:
            counter = self.freq_table.get(current_label)
            if not counter:
                return []
            total = sum(counter.values())
            results = []
            for label, count in counter.most_common(top_k + 1):
                if label == current_label:
                    continue
                results.append((label, count / total))
                if len(results) >= top_k:
                    break
            return results

    def suggest_phrasing(self, current_label: str, top_k: int = 2):
        """Like suggest(), but returns ready-to-show phrasing strings."""
        results = self.suggest(current_label, top_k=top_k)
        phrasings = []
        for label, _score in results:
            phrase = _SUGGESTION_PHRASING.get(label)
            if phrase:
                phrasings.append(phrase)
        return phrasings


# ==============================================================================
# SECTION 6H2: MOOD-TREND FORECASTER (TensorFlow/Keras, LSTM - sequence model)
# ==============================================================================
#
# A SECOND Keras model, deliberately using a different layer type than
# SmartSuggestionEngine above: an LSTM, because this is a genuinely
# different kind of problem - not "classify this one input" but "given
# a SEQUENCE of the last few sentiment readings this session, forecast
# where the mood is heading next." A plain Dense network has no notion
# of order; feeding it "positive, positive, negative" and "negative,
# positive, positive" would look identical unless the layer type itself
# is sequence-aware. LSTM is the standard, well-established choice for
# exactly that.
#
# Training data is synthetic but modeled on plausible conversational
# mood dynamics: moods have inertia (a run of positive turns is more
# likely to continue positive than to flip), but do drift over time,
# and a single negative turn embedded in a mostly-positive run doesn't
# necessarily mean the whole trend broke. These dynamics are encoded as
# a simple weighted Markov chain, then used to SAMPLE realistic
# sequences for training - the model itself still has to learn the
# sequence-to-next-label mapping from examples, same as it would from
# any other sequence dataset.
#
# Falls back to a simple "repeat the most common recent label, weighted
# toward the most recent one" heuristic if TensorFlow isn't installed,
# so mood-trend suggestions still work, just without the LSTM behind
# them.

_MOOD_LABELS = ["positive", "neutral", "negative"]
_MOOD_TO_ID = {label: i for i, label in enumerate(_MOOD_LABELS)}

# Transition weights: mood_transitions[current][next] = relative weight.
# Encodes "moods have inertia" (diagonal weights are highest) plus a
# realistic amount of drift.
_MOOD_TRANSITION_WEIGHTS = {
    "positive": {"positive": 7, "neutral": 2, "negative": 1},
    "neutral": {"positive": 3, "neutral": 4, "negative": 3},
    "negative": {"positive": 1, "neutral": 3, "negative": 6},
}


def _sample_mood_sequence(rng: random.Random, length: int) -> list:
    """Samples one plausible mood sequence of the given length from the
    weighted Markov chain above, starting from a uniformly random mood."""
    sequence = [rng.choice(_MOOD_LABELS)]
    for _ in range(length - 1):
        current = sequence[-1]
        weights = _MOOD_TRANSITION_WEIGHTS[current]
        labels, weight_values = zip(*weights.items())
        next_mood = rng.choices(labels, weights=weight_values, k=1)[0]
        sequence.append(next_mood)
    return sequence


def _build_mood_sequence_dataset(num_sequences: int = 600, seq_len: int = 5, seed: int = 42):
    """
    Builds (X, y) where each row of X is a sequence of seq_len mood-id
    integers and the matching y is the id of the mood that FOLLOWED
    that sequence in the sampled chain - i.e. "given these last 5 moods,
    what came next" - genuinely a next-step sequence prediction dataset,
    not a relabeled classification dataset.
    """
    rng = random.Random(seed)
    X, y = [], []
    for _ in range(num_sequences):
        full_sequence = _sample_mood_sequence(rng, seq_len + 1)
        window = full_sequence[:seq_len]
        target = full_sequence[seq_len]
        X.append([_MOOD_TO_ID[m] for m in window])
        y.append(_MOOD_TO_ID[target])
    return np.array(X, dtype=np.int64), np.array(y, dtype=np.int64)


class MoodTrendForecaster:
    """
    Given the last few detected sentiment readings in a conversation
    (see SentimentClassifier, Section 6G), forecasts which mood is most
    likely next. Backed by an LSTM when TensorFlow is available (see the
    Section 6H2 module docstring above for why an LSTM specifically),
    with a simple recency-weighted frequency heuristic as an offline
    fallback.

    This powers an optional, low-key check-in nudge: if the forecaster
    is confident the conversation is trending negative, ChatBot can
    choose to soften its tone or surface supportive resources rather
    than plowing ahead - see ChatBot._maybe_check_in() for where this
    forecast actually gets used.
    """

    SEQUENCE_LENGTH = 5

    def __init__(self):
        self.backend = "tensorflow" if TENSORFLOW_AVAILABLE else "recency_weighted"
        self.model = None
        self.last_training_info = None
        self._fit()

    def _fit(self):
        X, y = _build_mood_sequence_dataset(seq_len=self.SEQUENCE_LENGTH)
        if self.backend == "tensorflow":
            self._fit_keras(X, y)
        else:
            self.last_training_info = {"note": "TensorFlow not installed - using recency-weighted heuristic"}

    def _fit_keras(self, X, y):
        tf.random.set_seed(42)
        num_classes = len(_MOOD_LABELS)

        # Widened from 2 to 3 LSTM layers plus 3 Dense layers (up from
        # 1), alongside the broader push for depth across every network
        # in this file.
        model = keras.Sequential([
            keras.layers.Input(shape=(self.SEQUENCE_LENGTH,)),
            keras.layers.Embedding(input_dim=num_classes, output_dim=8, name="mood_embedding"),
            keras.layers.LSTM(32, return_sequences=True, name="lstm_1"),
            keras.layers.Dropout(0.2),
            keras.layers.LSTM(24, return_sequences=True, name="lstm_2"),
            keras.layers.Dropout(0.2),
            keras.layers.LSTM(16, name="lstm_3"),
            keras.layers.Dense(32, activation="relu"),
            keras.layers.Dropout(0.15),
            keras.layers.Dense(24, activation="relu"),
            keras.layers.Dropout(0.15),
            keras.layers.Dense(16, activation="relu"),
            keras.layers.Dropout(0.1),
            keras.layers.Dense(num_classes, activation="softmax", name="next_mood"),
        ])
        model.compile(optimizer="adam", loss="sparse_categorical_crossentropy", metrics=["accuracy"])

        callbacks = [
            keras.callbacks.EarlyStopping(monitor="val_loss", patience=8, restore_best_weights=True),
        ]
        history = model.fit(
            X, y, epochs=60, batch_size=32, verbose=0, validation_split=0.15, callbacks=callbacks
        )
        self.model = model
        self.last_training_info = {
            "final_loss": float(history.history["loss"][-1]),
            "final_val_accuracy": float(history.history.get("val_accuracy", [0.0])[-1]),
            "epochs_trained": len(history.history["loss"]),
        }

    def forecast(self, recent_moods: list):
        """
        recent_moods: a list of sentiment label strings ("positive",
        "neutral", "negative"), most-recent LAST. Returns (predicted_
        label, confidence) or None if fewer than 2 moods were given
        (too little signal to forecast from).
        """
        cleaned = [m for m in recent_moods if m in _MOOD_TO_ID]
        if len(cleaned) < 2:
            return None

        if self.backend == "tensorflow":
            # Pad on the LEFT with the earliest known mood if the caller
            # gave us fewer than SEQUENCE_LENGTH readings, so a short
            # conversation still gets a forecast rather than being
            # rejected outright.
            padded = cleaned[:]
            while len(padded) < self.SEQUENCE_LENGTH:
                padded.insert(0, padded[0])
            window = padded[-self.SEQUENCE_LENGTH:]
            ids = np.array([[_MOOD_TO_ID[m] for m in window]])
            probs = self.model.predict(ids, verbose=0)[0]
            best_idx = int(np.argmax(probs))
            return _MOOD_LABELS[best_idx], float(probs[best_idx])

        return self._forecast_heuristic(cleaned)

    @staticmethod
    def _forecast_heuristic(cleaned: list):
        """Recency-weighted frequency fallback: more recent moods count
        more (linearly increasing weight by position), then normalize
        into a pseudo-confidence. Deterministic, no model needed."""
        weights = Counter()
        for i, mood in enumerate(cleaned):
            weights[mood] += (i + 1)  # later entries get more weight
        total = sum(weights.values())
        best_label, best_weight = weights.most_common(1)[0]
        return best_label, best_weight / total

    def format_forecast(self, recent_moods: list) -> str:
        result = self.forecast(recent_moods)
        if result is None:
            return "I don't have enough recent mood signal yet to forecast a trend."
        label, confidence = result
        backend_note = "an LSTM sequence model" if self.backend == "tensorflow" else "a recency-weighted heuristic"
        return f"Based on the last few messages, the mood trend looks {label} ({confidence:.0%} confidence, via {backend_note})."


# ==============================================================================
# SECTION 6H3: TORCH SEMANTIC MEMORY SEARCH (contrastive sentence embeddings)
# ==============================================================================
#
# A THIRD distinct PyTorch model in this file (alongside NeuralIntent
# Classifier and SentimentClassifier, Section 6G), solving a different
# problem than either: not "classify this text into a fixed label set,"
# but "learn a vector space where semantically similar sentences end up
# near each other," so remembered facts/notes can be searched by
# MEANING rather than exact keyword overlap. This is metric learning /
# contrastive learning, a genuinely different training objective from
# ordinary cross-entropy classification.
#
# How it's trained: NN_INTENT_EXAMPLES (Section 6G) already gives us,
# for free, a large set of (text, intent_label) pairs. Two texts that
# share an intent label are treated as a POSITIVE pair (should end up
# close in embedding space); two texts with different intent labels,
# sampled at random, are a NEGATIVE pair (should end up far apart).
# Training minimizes a margin-based contrastive loss over batches of
# such pairs - conceptually the same idea behind sentence-embedding
# models like SBERT, just at toy scale with a small EmbeddingBag
# encoder instead of a transformer, appropriate for an offline,
# dependency-light chatbot.
#
# Falls back to the existing TF-IDF-based SimilarityMatcher (Section
# 6F) if torch isn't installed - so semantic memory search still works,
# just via lexical (word-overlap) similarity instead of a learned
# embedding space.

class SemanticMemoryIndex:
    """
    Learns a small sentence-embedding space via contrastive training on
    NN_INTENT_EXAMPLES (see the Section 6H3 module docstring above),
    then uses it to answer "which of these remembered items means
    something similar to this query" - real vector search (cosine
    similarity over learned embeddings), not keyword matching.

    Two independent responsibilities, kept separate on purpose:
      - fit(): trains the encoder ONCE at construction time, on the
        fixed NN_INTENT_EXAMPLES paraphrase data.
      - index(items) / search(query): operate on whatever the CALLER
        wants searchable right now (e.g. the user's remembered facts
        from MemoryStore, or their to-do items) - nothing about the
        trained encoder is specific to any one caller's data.
    """

    EPOCHS = 8
    MARGIN = 0.3
    BATCH_SIZE = 32

    def __init__(self):
        self.backend = "torch" if TORCH_AVAILABLE else "tfidf_fallback"
        self.encoder = None
        self.vocab = None
        self._fallback_matcher = None
        self._indexed_items = []
        self._indexed_vectors = None
        self.last_training_info = None
        self._fit()

    # ---- training -------------------------------------------------------

    def _fit(self):
        if self.backend != "torch":
            # SimilarityMatcher (Section 6F) is purpose-built to match
            # against ITS OWN fixed intent-example list, so it can't be
            # reused directly for an arbitrary, caller-supplied item
            # list here - instead this fallback fits a fresh TfidfVectorizer
            # per search() call, over whatever items the caller passes in.
            # Same lexical-similarity idea, just not routed through a
            # class that assumes a fixed corpus.
            self.last_training_info = {"note": "torch not installed - using TF-IDF lexical fallback"}
            return

        texts = [t for t, _label in NN_INTENT_EXAMPLES]
        labels = [label for _t, label in NN_INTENT_EXAMPLES]
        self.vocab = _TextVocab(texts, max_len=14)
        self.encoder = self._build_encoder(vocab_size=len(self.vocab))

        by_label = {}
        for text, label in zip(texts, labels):
            by_label.setdefault(label, []).append(text)
        # Contrastive training needs at least 2 examples of a label to
        # form a positive pair - drop any singleton labels rather than
        # crashing on them.
        by_label = {k: v for k, v in by_label.items() if len(v) >= 2}
        all_labels = list(by_label.keys())

        torch.manual_seed(42)
        rng = random.Random(42)
        optimizer = torch.optim.Adam(self.encoder.parameters(), lr=0.01)

        final_loss = None
        for epoch in range(self.EPOCHS):
            epoch_losses = []
            for _ in range(self.BATCH_SIZE):
                anchor_label = rng.choice(all_labels)
                anchor_text, positive_text = rng.sample(by_label[anchor_label], 2)
                negative_label = rng.choice([l for l in all_labels if l != anchor_label])
                negative_text = rng.choice(by_label[negative_label])

                batch_ids = torch.tensor([
                    self.vocab.encode(anchor_text),
                    self.vocab.encode(positive_text),
                    self.vocab.encode(negative_text),
                ], dtype=torch.long)

                embeddings = self.encoder(batch_ids)
                anchor_vec, positive_vec, negative_vec = embeddings[0], embeddings[1], embeddings[2]

                positive_similarity = torch.dot(anchor_vec, positive_vec)
                negative_similarity = torch.dot(anchor_vec, negative_vec)
                # Margin-based contrastive (triplet-style) loss: push
                # positive_similarity to be at least MARGIN higher than
                # negative_similarity; zero loss once that margin holds.
                loss = torch.clamp(self.MARGIN - positive_similarity + negative_similarity, min=0.0)

                optimizer.zero_grad()
                loss.backward()
                optimizer.step()
                epoch_losses.append(loss.item())
            final_loss = sum(epoch_losses) / len(epoch_losses)

        self.encoder.eval()
        self.last_training_info = {
            "final_triplet_loss": round(final_loss, 4) if final_loss is not None else None,
            "epochs_trained": self.EPOCHS,
            "training_pairs_per_epoch": self.BATCH_SIZE,
        }

    @staticmethod
    def _build_encoder(vocab_size, embed_dim=32, hidden_dim=32, out_dim=24):
        """
        Builds the sentence encoder. Defined as a LOCAL class (like
        _IntentNet/_SentimentNet in Section 6G) rather than at module
        level, specifically so `nn.Module` is only ever referenced when
        this method actually runs - which only happens when torch is
        confirmed importable. A module-level `class _SentenceEncoder
        (nn.Module)` would crash at IMPORT time (NameError: nn is not
        defined) on any machine without torch installed, since Python
        evaluates a class's base classes immediately at definition time,
        not lazily.

        Architecture: mean-pooled word embeddings through a stack of
        FOUR hidden layers (widened from one, alongside the broader
        push for depth across every network in this file) before the
        final projection, L2-normalized at the output so cosine
        similarity and dot-product similarity coincide. Still no
        attention/recurrence - the point of this section is
        demonstrating a genuinely different TRAINING OBJECTIVE
        (contrastive learning), not architectural novelty; see
        NeuralIntentClassifier for this file's most elaborate
        architecture.
        """

        class _SentenceEncoder(nn.Module):
            def __init__(self):
                super().__init__()
                self.embedding = nn.Embedding(vocab_size, embed_dim, padding_idx=0)
                self.proj1 = nn.Linear(embed_dim, hidden_dim)
                self.act1 = nn.ReLU()
                self.proj2 = nn.Linear(hidden_dim, hidden_dim)
                self.act2 = nn.ReLU()
                self.proj3 = nn.Linear(hidden_dim, hidden_dim)
                self.act3 = nn.ReLU()
                self.proj4 = nn.Linear(hidden_dim, hidden_dim)
                self.act4 = nn.ReLU()
                self.proj5 = nn.Linear(hidden_dim, out_dim)

            def forward(self, token_ids):
                embedded = self.embedding(token_ids)  # (batch, seq_len, embed_dim)
                mask = (token_ids != 0).unsqueeze(-1).float()
                summed = (embedded * mask).sum(dim=1)
                counts = mask.sum(dim=1).clamp(min=1.0)
                pooled = summed / counts  # mean pool over real (non-pad) tokens

                h = self.act1(self.proj1(pooled))
                h = self.act2(self.proj2(h))
                h = self.act3(self.proj3(h))
                h = self.act4(self.proj4(h))
                out = self.proj5(h)
                return nn.functional.normalize(out, p=2, dim=1)  # unit-length vectors

        torch.manual_seed(42)
        return _SentenceEncoder()

    # ---- embedding + search ----------------------------------------------

    def embed(self, text: str):
        """Returns a unit-length embedding vector (numpy array) for one
        piece of text, or None if torch isn't available (callers should
        use search()/index(), which handle the fallback automatically,
        rather than calling embed() directly unless torch-specific
        behavior is actually needed)."""
        if self.backend != "torch":
            return None
        with torch.no_grad():
            ids = torch.tensor([self.vocab.encode(text)], dtype=torch.long)
            vec = self.encoder(ids)[0]
        return vec.numpy()

    def index(self, items: list):
        """Pre-computes and caches embeddings for a list of strings
        (e.g. the user's remembered facts), so repeated search() calls
        against the same item list don't re-embed everything each time."""
        self._indexed_items = list(items)
        if self.backend == "torch" and items:
            with torch.no_grad():
                ids = torch.tensor([self.vocab.encode(t) for t in items], dtype=torch.long)
                self._indexed_vectors = self.encoder(ids).numpy()
        else:
            self._indexed_vectors = None

    def search(self, query: str, items: list = None, top_k: int = 3):
        """
        Returns up to top_k (item, score) pairs from `items` (or the
        most recently index()-ed items, if items isn't given), ranked
        by semantic similarity to `query`. Falls back to
        SimilarityMatcher's TF-IDF cosine similarity if torch isn't
        available - same return shape either way, so callers don't need
        to know which backend answered.
        """
        candidates = items if items is not None else self._indexed_items
        if not candidates:
            return []

        if self.backend != "torch":
            return self._search_tfidf_fallback(query, candidates, top_k)

        if items is not None:
            self.index(items)
        if self._indexed_vectors is None or len(self._indexed_vectors) != len(candidates):
            self.index(candidates)

        query_vec = self.embed(query)
        similarities = self._indexed_vectors @ query_vec  # cosine sim (vectors are unit-length)
        ranked_idx = np.argsort(similarities)[::-1][:top_k]
        return [(candidates[i], float(similarities[i])) for i in ranked_idx]

    @staticmethod
    def _search_tfidf_fallback(query: str, candidates: list, top_k: int):
        """Generic TF-IDF + cosine-similarity search over an arbitrary
        candidate list, fit fresh each call (these lists - remembered
        facts, to-do items - are small and change often, so a persistent
        fitted vectorizer isn't worth the added state). scikit-learn is
        a hard dependency of this file (unlike torch/TensorFlow/OpenCV),
        so no further fallback-below-the-fallback is needed here."""
        try:
            vectorizer = TfidfVectorizer()
            vectors = vectorizer.fit_transform(candidates + [query])
            query_vec = vectors[-1]
            item_vecs = vectors[:-1]
            sims = cosine_similarity(query_vec, item_vecs)[0]
        except ValueError:
            return [(item, 0.0) for item in candidates[:top_k]]

        ranked_idx = np.argsort(sims)[::-1][:top_k]
        return [(candidates[i], float(sims[i])) for i in ranked_idx]

    def format_search(self, query: str, items: list, top_k: int = 3) -> str:
        results = self.search(query, items=items, top_k=top_k)
        if not results:
            return "I don't have anything to search through yet."
        backend_note = "learned semantic embeddings" if self.backend == "torch" else "keyword/TF-IDF similarity"
        lines = [f"Closest matches to '{query}' (via {backend_note}):"]
        for item, score in results:
            lines.append(f"  - {item}  (similarity {score:.2f})")
        return "\n".join(lines)

    # ---- near-duplicate detection ------------------------------------------

    def find_near_duplicates(self, items: list, threshold: float = 0.9):
        """
        Finds pairs of items in `items` that are near-duplicates in
        meaning (cosine similarity >= threshold), e.g. flagging that
        the user told the bot "my favorite color is blue" and, much
        later, "I really like the color blue" as saying essentially the
        same thing. Useful for MemoryStore hygiene (surfacing possibly-
        redundant remembered facts) without requiring exact text match.
        Returns a list of (item_a, item_b, similarity) tuples, highest
        similarity first.
        """
        n = len(items)
        if n < 2:
            return []

        if self.backend == "torch":
            self.index(items)
            vectors = self._indexed_vectors
            similarity_matrix = vectors @ vectors.T
        else:
            try:
                vectorizer = TfidfVectorizer()
                vectors = vectorizer.fit_transform(items)
                similarity_matrix = cosine_similarity(vectors)
            except ValueError:
                return []

        pairs = []
        for i in range(n):
            for j in range(i + 1, n):
                score = float(similarity_matrix[i][j])
                if score >= threshold:
                    pairs.append((items[i], items[j], score))
        pairs.sort(key=lambda triple: triple[2], reverse=True)
        return pairs

    def format_near_duplicates(self, items: list, threshold: float = 0.9) -> str:
        pairs = self.find_near_duplicates(items, threshold=threshold)
        if not pairs:
            return "I didn't find any near-duplicate entries."
        lines = [f"Possible near-duplicates (similarity >= {threshold}):"]
        for item_a, item_b, score in pairs:
            lines.append(f"  - '{item_a}' <-> '{item_b}'  ({score:.2f})")
        return "\n".join(lines)

    # ---- embedding space visualization -------------------------------------

    def project_2d(self, items: list):
        """
        Projects each item's embedding down to 2 dimensions via PCA
        (a standard, well-established linear dimensionality-reduction
        technique - captures the two directions of greatest variance
        in the embedding space), so the learned semantic space can be
        inspected/plotted rather than staying an opaque 24-dimensional
        vector. Falls back to the TF-IDF vectors (still real PCA, just
        on lexical rather than learned features) when torch isn't
        available, same fallback shape as everything else in this
        class. Returns a list of (item, x, y) tuples.
        """
        if len(items) < 2:
            return [(item, 0.0, 0.0) for item in items]

        if self.backend == "torch":
            self.index(items)
            vectors = self._indexed_vectors
        else:
            try:
                vectorizer = TfidfVectorizer()
                vectors = vectorizer.fit_transform(items).toarray()
            except ValueError:
                return [(item, 0.0, 0.0) for item in items]

        n_components = min(2, vectors.shape[0], vectors.shape[1])
        if n_components < 2:
            return [(item, float(vectors[i][0]), 0.0) for i, item in enumerate(items)]

        pca = PCA(n_components=2, random_state=42)
        coords = pca.fit_transform(vectors)
        return [(items[i], float(coords[i][0]), float(coords[i][1])) for i in range(len(items))]

    def format_2d_projection(self, items: list) -> str:
        projected = self.project_2d(items)
        if not projected:
            return "Nothing to project yet."
        backend_note = "learned embeddings" if self.backend == "torch" else "TF-IDF vectors"
        lines = [f"2D PCA projection (via {backend_note}):"]
        for item, x, y in projected:
            lines.append(f"  ({x:+.2f}, {y:+.2f})  {item}")
        return "\n".join(lines)


# ==============================================================================
