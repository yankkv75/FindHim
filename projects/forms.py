from django.forms import ModelForm, widgets
from .models import Project, Review
from django import forms


class ProjectForm(ModelForm):
    """ Форма проекта """
    class Meta:
        model = Project
        fields = ['title', 'description', 'demo_link', 'source_link',
                  'featured_image', 'tags']
        widgets = {
            'tags': forms.CheckboxSelectMultiple()
        }

    def __init__(self, *args, **kwargs):
        super(ProjectForm, self). __init__(*args, **kwargs)

        # for name, field in self.fields.items():
        #     field.widget.attrs.update({'class': 'input', 'placeholder': 'Add title'})

        self.fields['title'].widget.attrs.update({'class': 'input', 'placeholder': 'Add title'})
        self.fields['description'].widget.attrs.update({'class': 'input', 'placeholder': 'Add description'})
        self.fields['source_link'].widget.attrs.update({'class': 'input', 'placeholder': 'https://'})
        self.fields['demo_link'].widget.attrs.update({'class': 'input', 'placeholder': 'https://'})


class ReviewForm(ModelForm):
    """ Форма комментария """
    class Meta:
        model = Review
        fields = ['value', 'body']

        labels = {
            'value': 'Choose your vote',
            'body': 'Write your comment here'
        }

    def __init__(self, *args, **kwargs):
        super(ReviewForm, self). __init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})