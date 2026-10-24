"""Views for displaying courses and evaluating lesson exams."""
from django.http import HttpResponseNotAllowed
from django.shortcuts import get_object_or_404, redirect, render
from .models import Choice, Course, Lesson, Submission


def course_details(request, course_id=None):
    """Display a course, lessons, questions, and answer choices."""
    if course_id is None:
        course = Course.objects.prefetch_related("lessons__questions__choices").first()
        if course is None:
            return render(request, "onlinecourse/course_details_bootstrap.html", {"course": None, "lessons": []})
    else:
        course = get_object_or_404(Course.objects.prefetch_related("lessons__questions__choices"), pk=course_id)
    return render(request, "onlinecourse/course_details_bootstrap.html", {
        "course": course,
        "lessons": course.lessons.all(),
    })


def submit(request, lesson_id):
    """Evaluate exam answers, store a submission, and redirect to the result."""
    if request.method != "POST":
        return HttpResponseNotAllowed(["POST"])

    lesson = get_object_or_404(Lesson.objects.select_related("course"), pk=lesson_id)
    questions = list(lesson.questions.prefetch_related("choices"))
    max_score = sum(question.grade for question in questions)
    earned_score = 0
    selected_choice_ids = []

    for question in questions:
        submitted_ids = request.POST.getlist(f"question_{question.pk}")
        allowed_ids = set(question.choices.filter(pk__in=submitted_ids).values_list("pk", flat=True))
        selected_choice_ids.extend(allowed_ids)
        correct_ids = set(question.choices.filter(is_correct=True).values_list("pk", flat=True))
        if correct_ids and allowed_ids == correct_ids:
            earned_score += question.grade

    submission = Submission.objects.create(
        user=request.user if request.user.is_authenticated else None,
        lesson=lesson,
        score=earned_score,
        max_score=max_score,
    )
    submission.selected_choices.set(Choice.objects.filter(pk__in=selected_choice_ids))
    return redirect("onlinecourse:show_exam_result", submission_id=submission.pk)


def show_exam_result(request, submission_id):
    """Render the score and question-by-question correctness details."""
    submission = get_object_or_404(
        Submission.objects.select_related("lesson__course").prefetch_related("selected_choices"),
        pk=submission_id,
    )
    selected_ids = set(submission.selected_choices.values_list("pk", flat=True))
    results = []
    for question in submission.lesson.questions.prefetch_related("choices"):
        choices = list(question.choices.all())
        selected_for_question = {choice.pk for choice in choices if choice.pk in selected_ids}
        correct_ids = {choice.pk for choice in choices if choice.is_correct}
        results.append({
            "question": question,
            "choices": choices,
            "selected_ids": selected_for_question,
            "correct_ids": correct_ids,
            "is_correct": bool(correct_ids) and selected_for_question == correct_ids,
        })
    return render(request, "onlinecourse/exam_result.html", {"submission": submission, "results": results})
