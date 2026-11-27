from app.database import SessionLocal
from app.models import Question

DEFAULT_QUESTIONS = [
    {
        "title": "What is your favorite season of the year?",
        "option_1": "Spring",
        "option_2": "Summer",
        "option_3": "Autumn",
        "option_4": "Winter",
    },
    {
        "title": "How do you prefer to spend your weekend?",
        "option_1": "Relaxing at home",
        "option_2": "Going out with friends",
        "option_3": "Doing sports",
        "option_4": "Taking a short trip",
    },
    {
        "title": "What type of food do you like the most?",
        "option_1": "Italian",
        "option_2": "Asian",
        "option_3": "Mediterranean",
        "option_4": "Fast food",
    },
    {
        "title": "Which kind of movies do you enjoy watching the most?",
        "option_1": "Action",
        "option_2": "Comedy",
        "option_3": "Drama",
        "option_4": "Science fiction",
    },
    {
        "title": "How do you usually get to work or school?",
        "option_1": "Car",
        "option_2": "Public transportation",
        "option_3": "Bicycle or scooter",
        "option_4": "Walking",
    },
    {
        "title": "Which pet would you most like to have?",
        "option_1": "Dog",
        "option_2": "Cat",
        "option_3": "Fish",
        "option_4": "Bird",
    },
    {
        "title": "What is your favorite way to listen to music?",
        "option_1": "Streaming apps",
        "option_2": "Radio",
        "option_3": "Live concerts",
        "option_4": "I don't listen to music much",
    },
    {
        "title": "How often do you shop online?",
        "option_1": "Every week",
        "option_2": "Every month",
        "option_3": "A few times a year",
        "option_4": "Almost never",
    },
    {
        "title": "Between the following, what do you most love to do?",
        "option_1": "Watch TV",
        "option_2": "Play the computer",
        "option_3": "Hanging out with friends",
        "option_4": "Travel the world",
    },
    {
        "title": "Where is your preferred place to travel?",
        "option_1": "USA",
        "option_2": "France",
        "option_3": "South America",
        "option_4": "Thailand",
    },
]


def seed_questions() -> None:
    db = SessionLocal()
    try:
        if db.query(Question).count() > 0:
            return
        for question_data in DEFAULT_QUESTIONS:
            db.add(Question(**question_data))
        db.commit()
        print(f"Seeded {len(DEFAULT_QUESTIONS)} default questions")
    finally:
        db.close()