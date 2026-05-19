from django.db import models
from django.utils.text import slugify

from .utils.image_optimizer import optimize_image


class OptimizedImageModel(models.Model):
    image_fields = []

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        for field in self.image_fields:
            image_field = getattr(self, field, None)
            if image_field and hasattr(image_field, "path"):
                optimize_image(image_field.path)

class Blog(OptimizedImageModel):
    image_fields = ["image"]

    image = models.ImageField(upload_to="blogs/", help_text="Blog cover image")
    slug = models.SlugField(unique=True, blank=True)
    title = models.CharField(max_length=200)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            counter = 1
            while Blog.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)


class Testimonial(OptimizedImageModel):
    image_fields = ["image"]

    name = models.CharField(max_length=100, help_text="Name of the person giving the testimonial")
    image = models.ImageField(upload_to="testimonials/", blank=True, null=True, help_text="Profile picture")
    review = models.TextField(help_text="Customer or client review")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Testimonial"
        verbose_name_plural = "Testimonials"

    def __str__(self):
        return self.name


class Contact(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    email = models.EmailField(blank=True, null=True)
    message = models.TextField(blank=True)
    best_time_to_contact = models.CharField(max_length=100, blank=True, null=True)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.phone}"


class Collection(OptimizedImageModel):
    image_fields = ["image"]

    name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(unique=True, blank=True)
    image = models.ImageField(upload_to="collections/")
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            slug = base_slug
            counter = 1
            while Collection.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)


class Category(OptimizedImageModel):
    image_fields = ["image"]
    collection = models.ForeignKey(Collection, on_delete=models.CASCADE, related_name="categories")
    name = models.CharField(max_length=200)
    slug = models.SlugField(blank=True)
    image = models.ImageField(upload_to="categories/", blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Categories"
        unique_together = (('collection', 'name'), ('collection', 'slug'))

    def __str__(self):
        return f"{self.collection.name} -> {self.name}"

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            slug = base_slug
            counter = 1
            while Category.objects.filter(collection=self.collection, slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)


class Product(models.Model):
    GENDER_CHOICES = [
        ("boys", "Boys"),
        ("girls", "Girls"),
        ("unisex", "Unisex"),
    ]

    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="products")
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField()
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    available_sizes = models.TextField(blank=True, null=True, help_text="Enter sizes comma-separated e.g. 0-3M, 3-6M, 1Y")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            slug = base_slug
            counter = 1
            while Product.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)


class ProductImage(OptimizedImageModel):
    image_fields = ["image"]

    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to="products/")

    def __str__(self):
        return f"Image for {self.product.name}"
