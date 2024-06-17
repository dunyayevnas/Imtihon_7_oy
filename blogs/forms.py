from django import forms

from blogs.models import BlogCommentModel


class BlogsCommentModelForm(forms.ModelForm):
    class Meta:
        model = BlogCommentModel
        fields = ['message']
