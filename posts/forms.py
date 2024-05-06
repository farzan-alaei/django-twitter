from django import forms
from .models import Post, Image, Comment, Reaction, Tag
from django.forms import inlineformset_factory


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content', 'reply_to']


class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ['image', 'alt', 'is_featured']


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'status', 'tags', 'archived']


class ReactionForm(forms.ModelForm):
    class Meta:
        model = Reaction
        fields = ['liked', 'disliked']
        widgets = {'liked': forms.HiddenInput(), 'disliked': forms.HiddenInput()}


class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ['name']


ImageFormSet = inlineformset_factory(Post, Image, form=ImageForm, extra=5, can_delete=True)
