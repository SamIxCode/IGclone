from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile, Post

# Create your forms here.
class NewUserForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super(NewUserForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user


class EditProfile(ModelForm):
    class Meta:
        model = Profile
        fields = ("bio", "location", "profile_image")

    def save(self, commit=True):
        profile = super(EditProfile, self).save(commit=False)
        if commit:
            profile.save()
        return profile


class UploadPost(ModelForm):
    class Meta:
        model = Post
        fields = ("caption", "image")

    def save(self, commit=True):
        post = super(UploadPost, self).save(commit=False)
        if commit:
            post.save()
        return post


