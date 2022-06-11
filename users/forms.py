from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm
from .models import Profile, Skill


class RegisterForm(UserCreationForm):
    """Форма создания нового юзера"""
    class Meta:
        model = User
        fields = ['first_name', 'email', 'username', 'password1', 'password2']
        labels = {
            'first_name': 'Name',
            'email': 'Email',
        }

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            self.fields['username'].help_text = ''
            self.fields['email'].help_text = ''
            self.fields['password1'].help_text = 'Your password can’t be entirely numeric ' \
                                                 'and must contain at least 8 characters.'


class ProfileForm(ModelForm):
    """ Форма редактирования аккаунта юзера """
    class Meta:
        model = Profile
        fields = ['name', 'email', 'username', 'location', 'short_intro', 'bio', 'profile_image',
                  'social_github', 'social_telegram', 'social_linkedin', 'social_twitter']
        labels = {
            'social_github': 'GitHub',
            'social_telegram': 'Telegram',
            'social_linkedin': 'LinkedIn',
            'social_twitter': 'Twitter',
        }

    def __init__(self, *args, **kwargs):
        super(ProfileForm, self). __init__(*args, **kwargs)

        self.fields['email'].widget.attrs.update({'class': 'input', 'placeholder': 'name@gmail.com'})
        self.fields['social_github'].widget.attrs.update({'class': 'input', 'placeholder': 'https://github.com/'})
        self.fields['social_telegram'].widget.attrs.update({'class': 'input', 'placeholder': 'https://t.me/'})
        self.fields['social_linkedin'].widget.attrs.update(
            {'class': 'input', 'placeholder': 'https://www.linkedin.com/in/'})
        self.fields['social_twitter'].widget.attrs.update({'class': 'input', 'placeholder': 'https://twitter.com/'})


class SkillForm(ModelForm):
    """ Форма скиллов """
    class Meta:
        model = Skill
        fields = '__all__'
        exclude = ['owner'] # Исключение

    def __init__(self, *args, **kwargs):
        super(SkillForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})
