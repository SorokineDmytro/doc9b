from django import forms
from .models import Page, Space
from taggit.models import Tag

class PageForm(forms.ModelForm):
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all().order_by("name"),
        required=False,
        widget=forms.SelectMultiple,
    )

    class Meta:
        model = Page
        fields = (
            "space",
            "parent",
            "title",
            "content",
            "order",
            "tags",
        )

class SpaceForm(forms.ModelForm):
    class Meta:
        model = Space
        fields= (
            "name",
            "description",
        )