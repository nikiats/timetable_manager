from django import forms


class UserSignupForm(forms.Form):
    username = forms.CharField(label='username', widget=forms.PasswordInput)
    password = forms.CharField(label='password', widget=forms.PasswordInput)
    password_repeat = forms.CharField(label='password_repeat', widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('password_repeat')

        if password != confirm_password:
            raise forms.ValidationError('Passwords don\'t match.')
        
        return cleaned_data