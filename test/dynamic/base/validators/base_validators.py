import json
from django.core.exceptions import ValidationError

class CustomBaseValidator:
    code = 'required'
    def __init__(self, message=None):
        self.message = message

    def __call__(self, value):
        if self.is_invalid(value):
            raise ValidationError(self.message, code=self.code, params={'value': value})

    def is_invalid(self, value):
        return bool(value)

class ExistValidator(CustomBaseValidator):
    code = '%(field)s_exist'

    def __init__(self, message=None, model=None, field=None):
        self.message = message if message else '"%(value)s" đã tồn tại.'
        self.model = model
        self.field = field

    def is_invalid(self, value):
        return bool(self.model.objects.filter(**{self.field: value}).exists())

class UploadValidator(CustomBaseValidator):
    code = '%(field)s_error'

    def __init__(self, message=None):
        self.message = message if message else 'Lỗi: "%(value)s"'
    
    def is_invalid(self, value):
        return value.lower() != 'true'.lower() and '/' not in value

class JSONValidator(CustomBaseValidator):
    code = '%(field)s_error'

    def __init__(self, message=None):
        self.message = message if message else 'Lỗi: "%(value)s"'
    
    def is_invalid(self, value):
        try:
            json.loads(value)
        except json.JSONDecodeError:
            return '/' not in value