from django import forms
from django.utils import timezone

from .models import Blog, Category, Contact, Testimonial, Collection, Product


class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ["image", "title", "description"]
        widgets = {
            "description": forms.Textarea(attrs={"class": "form-control rich-editor"}),
        }


class TestimonialForm(forms.ModelForm):
    class Meta:
        model = Testimonial
        fields = ["name", "image", "review"]



class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ["first_name", "last_name", "phone", "email", "message", "best_time_to_contact"]


class CollectionForm(forms.ModelForm):
    class Meta:
        model = Collection
        fields = ["name", "image", "description"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.fields['image'].required = False


class CategoryForm(forms.ModelForm):
    collection = forms.ModelChoiceField(
        queryset=Collection.objects.all().order_by("name"),
        empty_label="Select Collection"
    )

    class Meta:
        model = Category
        fields = ["collection", "name", "image", "description"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.fields['image'].required = False


class ProductForm(forms.ModelForm):
    category = forms.ModelChoiceField(
        queryset=Category.objects.all().order_by("name"),
        empty_label="Select Category"
    )

    class Meta:
        model = Product
        fields = ["category", "name", "description", "gender", "available_sizes"]
        widgets = {
            "gender": forms.Select(choices=Product.GENDER_CHOICES),
            "available_sizes": forms.Textarea(attrs={"rows": 3}),
        }
