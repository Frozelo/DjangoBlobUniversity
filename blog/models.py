from django.db import models

# Create your models here.

from django.db import models
from ckeditor.fields import RichTextField


class Categorie(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title}"


class Tag(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return f"{self.title}"


class Post(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    content = RichTextField(null=True)
    category_id = models.ForeignKey("Categorie", on_delete=models.CASCADE)
    views = models.IntegerField(default=0)
    thumbnail = models.ImageField(upload_to='thumbnails/', null=True, blank=True)

    def __str__(self):
        return f"{self.title}"


class PostTagRelation(models.Model):
    tag_id = models.ForeignKey("Tag", on_delete=models.CASCADE)
    post_id = models.ForeignKey("Post", on_delete=models.CASCADE)
