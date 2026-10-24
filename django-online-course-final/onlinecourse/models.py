"""Database models for courses, lessons, quizzes, and submissions."""
from django.conf import settings
from django.db import models


class Course(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    pub_date = models.DateField(auto_now_add=True)
    instructors = models.ManyToManyField("Instructor", related_name="courses", blank=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Instructor(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    full_time = models.BooleanField(default=True)
    total_learners = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.user.get_username()


class Learner(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    occupation = models.CharField(max_length=200, blank=True)
    social_link = models.URLField(blank=True)

    def __str__(self):
        return self.user.get_username()


class Lesson(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="lessons")
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    content = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=0)
    video_url = models.URLField(blank=True)
    duration = models.PositiveIntegerField(default=0, help_text="Duration in minutes")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        return f"{self.course.name}: {self.title}"


class Question(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name="questions")
    question_text = models.TextField()
    grade = models.PositiveIntegerField(default=1, help_text="Points awarded for a correct answer")
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        return self.question_text[:80]


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="choices")
    choice_text = models.CharField(max_length=500)
    is_correct = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        return self.choice_text[:80]


class Submission(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name="exam_submissions")
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name="submissions")
    selected_choices = models.ManyToManyField(Choice, related_name="submissions", blank=True)
    score = models.PositiveIntegerField(default=0)
    max_score = models.PositiveIntegerField(default=0)
    submitted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-submitted_at"]

    def __str__(self):
        learner = self.user.get_username() if self.user else "Anonymous learner"
        return f"{learner} — {self.lesson.title} ({self.score}/{self.max_score})"

    @property
    def percentage(self):
        if not self.max_score:
            return 0
        return round(self.score * 100 / self.max_score, 1)
