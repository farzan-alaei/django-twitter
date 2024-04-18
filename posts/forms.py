from django import forms
from .models import Post, Image
from django.forms import inlineformset_factory


class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ['image', 'alt']


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'status', 'tags']


ImageFormSet = inlineformset_factory(Post, Image, form=ImageForm, extra=1, can_delete=True)
