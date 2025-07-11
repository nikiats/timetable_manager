from django import forms


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
