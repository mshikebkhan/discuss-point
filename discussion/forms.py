from django import forms
from .models import Discussion, Category

#category_choices
def get_category_choices():
    return [
        (category.title, category.title) for category in Category.objects.all()
    ]

class DiscussionForm(forms.ModelForm):
    title = forms.CharField(max_length=100)
    category = forms.ChoiceField(choices=get_category_choices, widget=forms.Select, required=True)
    description = forms.Textarea()
    class Meta():
        model = Discussion
        fields = ['title', 'category', 'description']
