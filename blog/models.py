
from django.db import models
from django.utils.text import slugify
from django.conf import settings
from PIL import Image


class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Post(models.Model):
    STATUS_CHOICES = [
        ("draft", "Draft"),
        ("published", "Published"),
    ]

    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True, blank=True)
    content = models.TextField()

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="blog_posts",
        null=True,
        blank=True,
    )

    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="posts",
    )

    tags = models.ManyToManyField(Tag, blank=True)

    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default="published",
    )

    cover_image = models.ImageField(
        upload_to="covers/",
        blank=True,
        null=True,
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            counter = 1

            while Post.objects.filter(slug=slug).exists():
                counter += 1
                slug = f"{base_slug}-{counter}"

            self.slug = slug

        super().save(*args, **kwargs)

        # Resize images larger than 800 x 800 pixels
        if self.cover_image:
            try:
                with Image.open(self.cover_image.path) as img:
                    if img.width > 800 or img.height > 800:
                        img.thumbnail((800, 800))
                        img.save(self.cover_image.path)
            except (OSError, ValueError):
                pass

    def __str__(self):
        return self.title
