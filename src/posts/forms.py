from django import forms
from django.contrib.auth.models import User
from . import models


class CreateBlog(forms.ModelForm):
    class Meta:
        model = models.Post
        fields = ['title','body','image']

class CommentForm(forms.ModelForm):
    body = forms.CharField(label='Comment',widget=forms.Textarea(attrs={"rows":3,"cols":101}))
    class Meta:
        model = models.Comment
        fields = ['body']
        labels = {'body':'Comment'}

class EditProfile(forms.ModelForm):
    class Meta:
        model = models.Profile
        fields = ['bio','image']

class EditUser(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username','first_name','last_name','email']

class EditPost(forms.ModelForm):
    class Meta:
        model = models.Post
        fields = ['title','body','image']

