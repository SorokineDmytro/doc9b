from django import forms
from .models import Page

class PageForm(forms.ModelForm):
    class Meta:
        model = Page
        fields = (
            "space",
            "parent",
            "title",
            "slug",
            "content",
            "order",
            "categories",
            "tags",
        )