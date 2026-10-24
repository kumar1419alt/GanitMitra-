"""Admin configuration for the OnlineCourse models."""
from django.contrib import admin
from .models import Course, Lesson, Instructor, Learner, Question, Choice, Submission


class QuestionInline(admin.TabularInline):
    """Allow questions to be maintained on a lesson form."""
    model = Question
    extra = 1
    fields = ("question_text", "grade", "order")


class ChoiceInline(admin.TabularInline):
    """Allow choices to be maintained on a question form."""
    model = Choice
    extra = 2
    fields = ("choice_text", "is_correct", "order")


class QuestionAdmin(admin.ModelAdmin):
    """Admin configuration for exam questions."""
    list_display = ("question_text", "lesson", "grade", "order")
    list_filter = ("lesson__course", "lesson")
    search_fields = ("question_text",)
    inlines = (ChoiceInline,)


class LessonAdmin(admin.ModelAdmin):
    """Admin configuration for course lessons and their questions."""
    list_display = ("title", "course", "order", "duration", "updated_at")
    list_filter = ("course",)
    search_fields = ("title", "description", "content")
    readonly_fields = ("created_at", "updated_at")
    inlines = (QuestionInline,)


class CourseAdmin(admin.ModelAdmin):
    """Admin configuration for courses."""
    list_display = ("name", "pub_date")
    search_fields = ("name", "description")


class SubmissionAdmin(admin.ModelAdmin):
    """Admin configuration for exam attempts."""
    list_display = ("user", "lesson", "score", "max_score", "submitted_at")
    list_filter = ("lesson__course", "submitted_at")
    search_fields = ("user__username", "lesson__title")
    readonly_fields = ("user", "lesson", "score", "max_score", "submitted_at", "selected_choices")


admin.site.register(Course, CourseAdmin)
admin.site.register(Lesson, LessonAdmin)
admin.site.register(Instructor)
admin.site.register(Learner)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice)
admin.site.register(Submission, SubmissionAdmin)
