from django.db import models
from django.utils.text import slugify
from ckeditor.fields import RichTextField

class Category(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Tag(models.Model):
    title = models.CharField(max_length=50)
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class News(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    content = RichTextField() 
    main_image = models.ImageField(upload_to='news/main_images/')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='news')
    tags = models.ManyToManyField(Tag, blank=True)
    view_count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            counter = 1
            while News.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class NewsGalleryImage(models.Model):
    news = models.ForeignKey(News, on_delete=models.CASCADE, related_name='gallery_images')
    image = models.ImageField(upload_to='news/gallery/')

    def __str__(self):
        return f"{self.news.title} - Gallery Image"


class SiteSettings(models.Model):
    site_title = models.CharField(max_length=100)
    logo = models.ImageField(upload_to='settings/logo/')
    favicon = models.ImageField(upload_to='settings/favicon/')
    description = models.TextField(blank=True)
    contact_email = models.EmailField(blank=True)
    phone_number = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return "Site Settings"
