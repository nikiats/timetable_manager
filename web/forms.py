from django import forms
from django.conf import settings

HOUR_MIN = getattr(settings, 'DAY_TIME_MIN')
HOUR_MAX = getattr(settings, 'DAY_TIME_MAX')


class UserSignupForm(forms.Form):
    username = forms.CharField(
        label='username',
        error_messages={'required': 'Введите имя пользователя'}
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
            self.add_error('password', 'Пароли не совпадают')
        
        return cleaned_data
    

class UserLoginForm(forms.Form):
    username = forms.CharField(
        label='username',
        error_messages={'required': 'Введите имя пользователя'}
    )
    password = forms.CharField(
        label='password',
        error_messages={'required': 'Введите пароль'}
    )


class TimetableCellEditForm(forms.Form):
    day_index = forms.IntegerField(
        label='day_index',
        error_messages={'required': 'Не указан индекс дня недели'}
    )
    hour = forms.IntegerField(
        label='hour',
        error_messages={'required': 'Не указан час занятия для изменения'}
    )
    value = forms.CharField(
        label='value',
        required=False,
        error_messages={'required': 'Не указано значение ячейки'}
    )

    def clean(self):
        cleaned_data = super().clean()
        hour = cleaned_data.get('hour')
        day_index = cleaned_data.get('day_index')
        
        if hour < HOUR_MIN or hour > HOUR_MAX:
            self.add_error('hour', 'Час вне допустимого диапазона')
        if day_index < 0 or day_index > 7 - 1:
            self.add_error('day_index', 'Допустим индекс дня от 0 до 6')
        
        return cleaned_data
