from django.db import models
from django.utils.text import slugify
from ckeditor.fields import RichTextField

class Categorie(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Categorie, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.title}"


class Tag(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        # Генерируем slug из title, если он не указан
        if not self.slug:
            self.slug = slugify(self.title)
        super(Tag, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.title}"


class Post(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField()
    content = RichTextField(null=True)
    category_id = models.ForeignKey("Categorie", on_delete=models.CASCADE)
    views = models.IntegerField(default=0)
    thumbnail = models.ImageField(upload_to='thumbnails/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Post, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.title}"


class PostTagRelation(models.Model):
    tag_id = models.ForeignKey("Tag", on_delete=models.CASCADE)
    post_id = models.ForeignKey("Post", on_delete=models.CASCADE)
