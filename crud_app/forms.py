from django import forms
from .models import Student


Hobby_choices = [
    ('python','Python'),
    ('java', 'Java'),
    ('js', 'JavaScript'),
]


class StudentForm(forms.ModelForm):
    hobbies = forms.MultipleChoiceField(
        choices = Hobby_choices,
        widget = forms.CheckboxSelectMultiple,
        required = False
    )

    class Meta:
        model = Student
        fields = ['name', 'email', 'course', 'gender', 'hobbies', 'is_active']
        widget = {
            'gender': forms.RadioSelect(),
            }

def __init__(self, *args, **kwargs):
    super().__init__(*args, *kwargs)

    if self.instance and self.instance.pk:
        self.fields['hobbies'].initial = self.instance.get_hobby_list()

def save(self, commit = True):
    instance = super().save(commit= False)
    hobbies_list = self.cleaned_data.get('hobbies', [])
    instance.hobbies = ','.join(hobbies_list)
    if commit:
        instance.save()
    return instance