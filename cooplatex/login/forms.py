from django import forms


class RegisterForm(forms.Form):
    name = forms.CharField(widget=forms.TextInput({
      'required': True,
      'id': 'inputName',
      'class': 'form-control',
      'placeholder': 'Name'
    }),
    min_length=3, max_length=20)

    email = forms.EmailField(widget=forms.EmailInput(attrs={
      'required': True,
      'id': 'inputEmail',
      'class': 'form-control',
      'placeholder': 'Email'
    }))

    password = forms.CharField(widget=forms.PasswordInput(attrs={
      'required': True,
      'class': 'form-control',
      'id': 'inputPassword',
      'placeholder': 'Password'
    }), min_length=8)

    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
      'required': True,
      'class': 'form-control',
      'id': 'inputPassword1',
      'placeholder': 'Retype Password'
    }), min_length=8)
