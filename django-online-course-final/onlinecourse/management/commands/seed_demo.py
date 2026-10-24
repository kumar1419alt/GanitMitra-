"""Create sample course content for the final project screenshots."""
from django.core.management.base import BaseCommand
from onlinecourse.models import Course, Lesson, Question, Choice


class Command(BaseCommand):
    help = "Create a sample course, lesson, questions, and answer choices."

    def handle(self, *args, **options):
        course, _ = Course.objects.get_or_create(
            name="Introduction to Python",
            defaults={"description": "A beginner-friendly course covering Python fundamentals."},
        )
        lesson, _ = Lesson.objects.get_or_create(
            course=course,
            title="Python Basics",
            defaults={
                "description": "Review variables, functions, and core Python syntax.",
                "content": "This lesson introduces essential Python language features.",
                "order": 1,
                "duration": 20,
            },
        )
        samples = [
            {
                "question_text": "Which keyword is used to define a function in Python?",
                "grade": 1,
                "order": 1,
                "choices": [
                    ("func", False),
                    ("def", True),
                    ("function", False),
                    ("define", False),
                ],
            },
            {
                "question_text": "Which data type is used to store an ordered, mutable collection?",
                "grade": 1,
                "order": 2,
                "choices": [
                    ("tuple", False),
                    ("str", False),
                    ("list", True),
                    ("int", False),
                ],
            },
            {
                "question_text": "Which symbol starts a single-line comment in Python?",
                "grade": 1,
                "order": 3,
                "choices": [
                    ("//", False),
                    ("<!--", False),
                    ("#", True),
                    ("**", False),
                ],
            },
        ]
        for item in samples:
            question, _ = Question.objects.get_or_create(
                lesson=lesson,
                question_text=item["question_text"],
                defaults={"grade": item["grade"], "order": item["order"]},
            )
            for order, (label, is_correct) in enumerate(item["choices"], start=1):
                Choice.objects.get_or_create(
                    question=question,
                    choice_text=label,
                    defaults={"is_correct": is_correct, "order": order},
                )
        self.stdout.write(self.style.SUCCESS(
            "Demo data ready: Introduction to Python → Python Basics (3 questions)."
        ))
