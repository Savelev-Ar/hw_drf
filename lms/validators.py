from rest_framework.serializers import ValidationError


class UrlValidator:
    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        tmp_val = dict(value).get(self.field)
        if tmp_val:
            if r'youtube.com/watch?v=' not in tmp_val:
                raise ValidationError('Url is incorrect')
