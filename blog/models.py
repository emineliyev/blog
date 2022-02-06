from django.contrib.auth.models import User
from django.db import models


class Post(models.Model):
    title = models.CharField(max_length=60, verbose_name='Title')
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    publish_date = models.DateTimeField(auto_now_add=True)
    published = models.BooleanField(verbose_name='Published', default=True)
    category = models.ForeignKey('Category', on_delete=models.CASCADE, verbose_name='Category')

    def __str__(self):
        return f"{self.title}"

    class Meta:
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'
        ordering = ['-publish_date']


class Comments(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Author')
    title = models.TextField(max_length=60, verbose_name='Title')
    publish_date = models.DateTimeField(auto_now_add=True, verbose_name='Published date')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, verbose_name='Post')

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-id']


class Category(models.Model):
    title = models.CharField(max_length=250, verbose_name='Category')
    slug = models.SlugField(unique=True, max_length=250)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'


class Reviews(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, verbose_name='Post')
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='User')
    text = models.TextField(verbose_name='Reviews text')
    rating = models.PositiveIntegerField(default=1, blank=True, null=True, verbose_name='Rating')
    date = models.DateTimeField(auto_now_add=True, verbose_name='Create date')

    def __str__(self):
        return self.text

    class Meta:
        verbose_name = 'Review'
        verbose_name_plural = 'Reviews'
        ordering = ['rating']