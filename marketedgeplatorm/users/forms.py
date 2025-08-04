from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from .models import Profile, CustomUser



class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['email', 'username', 'password1', 'password2']
        labels = {
            'username': 'Username',
        }

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})


class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = ['email', 'username', 'bio', 'profile_image',
    ]

    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        self.fields['email'].disabled = True

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})

    def clean_email(self):
        # Return the original value from the instance to prevent tampering
        return self.instance.email      