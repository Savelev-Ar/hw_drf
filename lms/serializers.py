from rest_framework import serializers

from lms.models import Course, Lesson


class CourseSerializer(serializers.ModelSerializer):
    number_of_lessons = serializers.SerializerMethodField()

    def get_number_of_lessons(self, obj):
        return obj.lessons.count()

    class Meta:
        model = Course
        fields = ('name', 'preview', 'description', 'number_of_lessons')


class LessonSerializer(serializers.ModelSerializer):


    class Meta:
        model = Lesson
        fields = ('__all__')
