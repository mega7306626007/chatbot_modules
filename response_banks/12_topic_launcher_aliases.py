"""Section 8B: generic topic launcher aliases
Part of the response-bank data set - see chatbot_modules/13_response_banks_loader.py.
"""

# SECTION 8B: GENERIC TOPIC LAUNCHER ALIASES
# ==============================================================================
#
# Maps the natural word someone would actually say after "let's talk
# about ___" to the internal topic key used throughout TOPICS /
# simple_topic_banks (e.g. "date" -> "date_query", "anxiety" ->
# "anxiety_topic"). This is what lets "let's talk about X" work for ANY
# of the 240+ existing topics without enumerating every one of them
# inside a giant regex - the regex (discuss_topic_request, Section 7)
# only captures WHAT the user said; this table decides whether that
# matches something the bot actually has a topic for.
#
# Deliberately covers the topics someone would plausibly NAME directly
# (date, anxiety, money, family, ...) rather than every single one of
# the 240+ topics - many of those exist to catch incidental mentions
# inside a sentence, not to be addressed by name ("let's talk about
# small_talk_busy_topic" isn't something anyone would actually type).
# Unmatched topic names fall through to a clear "I don't have a topic
# for that yet" response rather than a wrong guess.
TOPIC_LAUNCHER_ALIASES = {
    # core utility topics
    "date": "date_query", "dates": "date_query", "calendar": "date_query",
    "time": "time_query", "math": "math_topic", "maths": "math_topic",
    "arithmetic": "math_topic", "jokes": "joke", "joke": "joke",
    "quotes": "quote", "quote": "quote", "riddles": "riddle", "riddle": "riddle",
    "trivia": "trivia", "stories": "story", "story": "story",
    "poems": "poem", "poetry": "poem", "todo": "todo_topic", "to-do": "todo_topic",
    "hangman": "hangman_topic", "weather": "weather_smalltalk",
    # emotional / mental health topics
    "anxiety": "anxiety_topic", "anxious": "anxiety_topic",
    "stress": "anxiety_topic", "stressed": "anxiety_topic",
    "feelings": "feelings_sad", "emotions": "feelings_sad",
    "sadness": "feelings_sad", "happiness": "feelings_happy",
    "anger": "feelings_angry_topic", "angry": "feelings_angry_topic",
    "nerves": "feelings_nervous_topic", "nervousness": "feelings_nervous_topic",
    "loneliness": "feelings_lonely_topic", "lonely": "feelings_lonely_topic",
    "pride": "feelings_proud_topic", "jealousy": "feelings_jealous_topic",
    "relief": "feelings_relieved_topic", "mental health": "mental_health_checkin_topic",
    "fear": "fear_phobia_topic", "phobias": "fear_phobia_topic",
    "grief": "grief_loss_topic", "loss": "grief_loss_topic",
    "climate anxiety": "climate_anxiety_topic", "ai": "ai_technology_fear_topic",
    "therapy": "therapy_counseling_topic", "counseling": "therapy_counseling_topic",
    "self care": "self_care_routine_topic", "self-care": "self_care_routine_topic",
    "mindfulness": "meditation_mindfulness_topic", "meditation": "meditation_mindfulness_topic",
    "forgiveness": "forgiveness_topic", "trust": "trust_issues_topic",
    "boundaries": "setting_boundaries_topic", "feeling stuck": "feeling_stuck_topic",
    "hope": "hope_future_topic", "gratitude": "gratitude",
    # everyday life topics
    "food": "food_hungry", "hunger": "food_hungry", "thirst": "food_thirsty",
    "hobbies": "hobbies_topic", "family": "family_topic", "work": "work_school_topic",
    "school": "work_school_topic", "money": "money_topic", "finances": "money_topic",
    "love": "love_relationships_topic", "relationships": "love_relationships_topic",
    "dating": "online_dating_topic", "music": "music_topic", "sports": "sports_topic",
    "books": "books_topic", "reading": "books_topic", "technology": "technology_topic",
    "tech": "technology_topic", "pets": "pets_animals_topic", "animals": "pets_animals_topic",
    "dog": "pets_animals_topic", "dogs": "pets_animals_topic", "cat": "pets_animals_topic",
    "cats": "pets_animals_topic", "puppy": "pets_animals_topic", "kitten": "pets_animals_topic",
    "travel": "travel_topic", "health": "health_topic", "birthdays": "birthday_topic",
    "birthday": "birthday_topic", "weekend": "weekend_topic", "holidays": "holiday_smalltalk",
    "learning": "learning_topic", "goals": "motivation_goals_topic",
    "motivation": "motivation_goals_topic", "nostalgia": "nostalgia_topic",
    "future plans": "future_plans_topic", "gaming": "gaming_topic", "games": "gaming_topic",
    "cooking": "cooking_topic", "food prep": "cooking_topic", "recipes": "cooking_topic",
    # sports aliases - "football" vs "soccer" vary by region, and only
    # "sports" used to resolve here, so "let's talk about football"
    # bounced with "I don't have a topic for that yet".
    "football": "sports_topic", "footie": "sports_topic", "soccer": "sports_topic",
    "basketball": "sports_topic", "ball": "sports_topic", "rugby": "sports_topic",
    "cricket": "sports_topic", "tennis": "sports_topic", "volleyball": "sports_topic",
    # photography / arts - previously unlaunchable by name.
    "photography": "photography_art_topic", "photograph": "photography_art_topic",
    "photos": "photography_art_topic", "photographs": "photography_art_topic",
    "camera": "photography_art_topic", "photography art": "photography_art_topic",
    # music instrument/genre names - "let's talk about jazz" should land
    # on the music topic rather than the "no topic" reply.
    "jazz": "music_topic", "guitar": "music_topic", "piano": "music_topic",
    "concerts": "music_topic", "albums": "music_topic",
    "nature": "nature_outdoors_topic",
    "outdoors": "nature_outdoors_topic", "sleep": "sleep_dreams_topic",
    "dreams": "sleep_dreams_topic", "humor": "humor_appreciation_topic",
    "comedy": "humor_appreciation_topic", "movies": "movies_tv_topic", "tv": "movies_tv_topic",
    "shopping": "shopping_topic", "coffee": "coffee_tea_topic", "tea": "coffee_tea_topic",
    "exercise": "exercise_fitness_topic", "fitness": "exercise_fitness_topic",
    "gym": "gym_intimidation_topic", "parenting": "parenting_topic",
    "career": "career_change_topic", "job": "job_interview_topic",
    "interviews": "job_interview_topic", "productivity": "productivity_tools_topic",
    "procrastination": "procrastination_topic", "social media": "social_media_topic",
    "remote work": "remote_work_topic", "fashion": "fashion_style_topic",
    "astrology": "astrology_zodiac_topic", "zodiac": "astrology_zodiac_topic",
    "spirituality": "spirituality_topic", "politics": "politics_deflect_topic",
    "volunteering": "volunteer_work_topic", "moving": "moving_city_topic",
    "weddings": "wedding_engagement_topic", "graduation": "graduation_topic",
    "pregnancy": "pregnancy_baby_topic", "siblings": "siblings_topic",
    "roommates": "roommates_topic", "immigration": "immigration_topic",
    "languages": "language_practice_topic", "language learning": "fluency_goals_topic",
}


# ==============================================================================
