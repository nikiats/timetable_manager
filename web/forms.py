from django import forms
from django.conf import settings


HOUR_MIN = getattr(settings, 'DAY_TIME_MIN')
HOUR_MAX = getattr(settings, 'DAY_TIME_MAX')
MAX_LESSON_LENGTH = getattr(settings, 'MAX_LESSON_LENGTH')
MAX_USERNAME_LENGTH = getattr(settings, 'MAX_USERNAME_LENGTH')


class UserSignupForm(forms.Form):
    username = forms.CharField(
        label='username',
        max_length=MAX_USERNAME_LENGTH,
        error_messages={
            'required': 'Введите имя пользователя',
            'max_length': f'Превышена максимальная длина имени пользователя ({MAX_USERNAME_LENGTH})'
        }
    )
    password = forms.CharField(
        label='password',
        error_messages={'required': 'Введите пароль'}
    )
    password_repeat = forms.CharField(
        label='password_repeat', 
        error_messages={'required': 'Введите повтор пароля'},
    )

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('password_repeat')

        if password != confirm_password:
            self.add_error('password_repeat', 'Пароли не совпадают')
        
        return cleaned_data
    

class UserLoginForm(forms.Form):
    username = forms.CharField(
        label='username',
        max_length=MAX_USERNAME_LENGTH,
        error_messages={
            'required': 'Введите имя пользователя',
            'max_length': f'Превышена максимальная длина имени пользователя ({MAX_USERNAME_LENGTH})'
        }
    )
    password = forms.CharField(
        label='password',
        error_messages={'required': 'Введите пароль'}
    )


class TimetableCellEditForm(forms.Form):
    day_index = forms.IntegerField(
        label='day_index',
        min_value=0,
        max_value=6,
        error_messages={
            'required': 'Не указан индекс дня недели',
            'min_value': 'Индекс дня недели не может быть меньше 0',
            'max_value': 'Индекс дня недели не может быть больше 6',
        }
    )
    hour = forms.IntegerField(
        label='hour',
        min_value=HOUR_MIN,
        max_value=HOUR_MAX,
        error_messages={
            'required': 'Не указан час занятия для изменения',
            'min_value': 'Некорректный час (меньше нижней границы)',
            'max_value': 'Некорректный час (выше верхней границы)'
        }
    )
    value = forms.CharField(
        label='value',
        required=False,
        max_length=MAX_LESSON_LENGTH,
        error_messages={
            'required': 'Не указано значение ячейки',
            'max_length': 'Превышена максимальная длина текста занятия'
        }
    )
