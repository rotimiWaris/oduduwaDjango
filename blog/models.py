from django.db import models
from django.conf import settings
from django.db.models import Q
from django.utils import timezone
from django.shortcuts import reverse
from datetime import datetime, date
from ckeditor.fields import RichTextField
from django.db.models.signals import pre_save
from oduduwa.utils import unique_slug_generator
# from django.contrib.auth.models import User


CATEGORY_CHOICES = [
    ('coding', 'Coding'),
    ('entertainment', 'Entertainment')
    ]


CLASS_NAME_CHOICES = [
    ('JSS1', 'JSS1'),
    ('JSS2', 'JSS2'),
    ('JSS3', 'JSS3'),
    ('SSS1', 'SSS1'),
    ('SSS2', 'SSS2'),
    ('SSS3', 'SSS3'),
    ('Other Class', 'Other Class'),
    ]

ROLE_CHOICES = [
    ('Student', 'Student'),
    ('Old Student', 'Old Student'),
    ('Teacher', 'Teacher'),
    ('Principal', 'Principal'),
    ('Vice-Principal', 'Vice-Principal'),
    ('Non-Member', 'Non-Member'),
    ]

# class Category(models.Model):
#     name = models.CharField(max_length=225)
    
#     def __str__(self):
#         return self.name

#     def get_absolute_url(self):
#         return "/"

# NOTE Do this later

class BlogPostQuerySet(models.query.QuerySet):
    def search(self, query):
        lookups = (
            Q(title__icontains=query) |
            Q(timestamp__icontains=query) |
            Q(category__icontains=query)
        )
        return self.filter(lookups).distinct()


class BlogPostManager(models.Manager):
    def get_queryset(self):
        return BlogPostQuerySet(self.model, using=self._db)

    def search(self, query=None):
        return self.get_queryset().search(query)


class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, null=True, on_delete=models.CASCADE)
    bio = models.TextField(null=True, blank=True)
    profile_pic = models.ImageField(null=True, blank=True, upload_to="profile-images/")
    class_name = models.CharField(choices=CLASS_NAME_CHOICES, max_length=225, null=True, blank=True)
    role = models.CharField(choices=ROLE_CHOICES, max_length=225, null=True, blank=True)

    def __str__(self):
        return str(self.user)


class BlogPost(models.Model):
    title = models.CharField(max_length=225)
    image = models.ImageField(null=True, blank=True, upload_to="blog-images/")
    slug = models.SlugField(max_length=500, null=True, blank=True)
    # content = models.TextField(null=True, blank=True)
    content = RichTextField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=225)
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='blog_posts_likes', null=True, blank=True)
    # image = models.ImageField(upload_to='image/', blank=True, null=True)
    # slug = models.SlugField(unique=True)
    # publish_date = models.DateTimeField(auto_now=False, auto_now_add=False, null=True, blank=True)
    # updated = models.DateTimeField(auto_now=True)
    
    objects = BlogPostManager()
    
    class Meta:
        ordering = ['-timestamp']
    
    def __str__(self):
        return f'{self.title} BY == {self.user}'
    
    def total_likes(self):
        return self.likes.count()

    def get_absolute_url(self):
        return f"/posts/{self.id}"
        # return reverse("blog:detail", args=(str(self.id)))

    def search(self, query=None):
        if query is None:
            return self.objects.none()
        return self.objects.search()


def slug_generator(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)


pre_save.connect(slug_generator, sender=BlogPost)


class Comment(models.Model):
    blog_post = models.ForeignKey(BlogPost, related_name="comments", on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    body = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f'{self.blog_post.title} == {self.user}'