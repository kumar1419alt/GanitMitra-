# Django Online Course Exam Project

This project demonstrates Django models (Question, Choice, Submission), admin inlines, a Bootstrap course detail page, exam submission/evaluation, and a detailed result page.

## Run locally
```bash
python -m venv .venv
# Windows: .venv\\Scripts\\activate
# macOS/Linux: source .venv/bin/activate
python -m pip install -r requirements.txt
python manage.py makemigrations onlinecourse
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```
Open http://127.0.0.1:8000/admin/ and add a Course, Lesson, Questions, and Choices. Mark the correct choice(s), then visit http://127.0.0.1:8000/ and submit an exam.

## Grading files
- `onlinecourse/models.py`: Question, Choice, Submission and supporting models
- `onlinecourse/admin.py`: seven model imports and required admin inlines/classes
- `onlinecourse/templates/onlinecourse/course_details_bootstrap.html`: Bootstrap course details, lessons, questions, choices
- `onlinecourse/views.py`: `submit` and `show_exam_result`
- `onlinecourse/urls.py`: exam submission and result routes

The required admin and final-result screenshots must be captured from the running app after adding sample data; this repository does not pretend to include live screenshots.