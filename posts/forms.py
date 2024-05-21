from django import forms
from .models import Post, Image, Comment, Reaction, Tag
from django.forms import inlineformset_factory
from django_select2 import forms as select2_forms


class TagSelect2Widget(select2_forms.ModelSelect2MultipleWidget):
    search_fields = [
        "name__icontains",
    ]
    queryset = Tag.objects.all()


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["content", "reply_to"]


class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ["image", "alt", "is_featured"]

    def __init__(self, *args, **kwargs):
        super(ImageForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({"class": "form-control"})


class PostForm(forms.ModelForm):
    new_tag = forms.CharField(label="New Tag", required=False)

    class Meta:
        model = Post
        fields = ["title", "content", "status", "tags", "archived"]
        widgets = {
            "tags": TagSelect2Widget,
        }

    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({"class": "form-control"})

    def clean(self):
        cleaned_data = super().clean()
        new_tag = cleaned_data.get("new_tag")
        if new_tag:
            tag, created = Tag.objects.get_or_create(name=new_tag)
            cleaned_data["tags"] = list(cleaned_data.get("tags", [])) + [tag]
        return cleaned_data


class ReactionForm(forms.ModelForm):
    class Meta:
        model = Reaction
        fields = ["liked", "disliked"]
        widgets = {"liked": forms.HiddenInput(), "disliked": forms.HiddenInput()}


class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ["name"]


ImageFormSet = inlineformset_factory(
    Post, Image, form=ImageForm, extra=3, can_delete=True
)
