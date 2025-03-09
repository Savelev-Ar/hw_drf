from rest_framework import serializers

from lms.models import Course, Lesson
from lms.validators import UrlValidator
from users.models import Subscribe


class LessonSerializer(serializers.ModelSerializer):

    class Meta:
        model = Lesson
        fields = '__all__'
        validators = [UrlValidator(field='videolink')]


class CourseSerializer(serializers.ModelSerializer):
    number_of_lessons = serializers.SerializerMethodField()
    is_subscriber = serializers.SerializerMethodField()
    lessons = LessonSerializer(many=True, read_only=True)


    def get_number_of_lessons(self, obj):
        return obj.lessons.count()

    def get_is_subscriber(self, obj):
        user = self.context.get('request').user
        if user:
            subscribe = Subscribe.objects.all().filter(course=obj, user=user)
            if subscribe.exists():
                return 'подписан'
            else:
                return 'не подписан'
        else:
            return

    class Meta:
        model = Course
        fields = ('name', 'preview', 'description', 'number_of_lessons', 'lessons', 'is_subscriber')
