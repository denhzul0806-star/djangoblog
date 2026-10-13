from email.mime import image
from django import forms
from .models import Post
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["title", "content", "category", "tags", "status", "cover_image"]  # was "image"
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "content": forms.Textarea(attrs={"class": "form-control", "rows": 8}),
            "category": forms.Select(attrs={"class": "form-select"}),
            "tags": forms.SelectMultiple(attrs={"class": "form-select", "size": 5}),
            "status": forms.Select(attrs={"class": "form-select"}),
            "cover_image": forms.ClearableFileInput(attrs={"class": "form-control"}),  # was "image"
        }

        def clean_title(self):
            title = self.cleaned_data('title')
            if len(title) < 5:
                raise forms.ValidationError("Title  must be at least 5 characters long.")
            return title

    def clean_title(self):
        title = self.cleaned_data['title']
        if len(title) < 5:
            raise forms.ValidationError("Title must be at least 5 characters")
        return title
    def clean_cover_image(self):
       image = self.cleaned_data.get('cover_image')
       if image:
           if image.size > 5 * 1024 * 1024:  # 5MB limit
               raise forms.ValidationError("Image file too large (max 5MB).")
           valid_extensions = [".jpg", ".jpeg", ".png", ".webp"]
           if not any(image.name.lower().endswith(ext) for ext in valid_extensions):
               raise forms.ValidationError("Unsupported file type. Use JPG, PNG, or WebP.")
           return image