from django.db import models
from accounts.models import User
from django.utils.translation import gettext_lazy as _
from django.db.models import Count


# Create your models here.
class Post(models.Model):
    class Status(models.TextChoices):
        DRAFT = 'D', _('Draft')
        PUBLISHED = 'P', _('Published')

    class Meta:
        verbose_name = _("Post")
        verbose_name_plural = _("Posts")

    title = models.CharField(verbose_name=_('title'), max_length=255)
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE, related_name='posts')
    content = models.TextField(verbose_name=_('content'), blank=True)
    status = models.CharField(verbose_name=_('status'),
                              max_length=1,
                              choices=Status.choices,
                              default=Status.PUBLISHED,
                              )
    tags = models.ManyToManyField('Tag', related_name='posts', blank=True)
    archived = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def count_reactions(self):
        likes = self.reaction_set.filter(liked=True).count()
        dislikes = self.reaction_set.filter(disliked=True).count()
        return likes, dislikes

    def __str__(self):
        return f"{self.title} - {self.user}"


class Reaction(models.Model):
    user = models.ForeignKey(User, verbose_name=_("user"), on_delete=models.CASCADE)
    related_post = models.ForeignKey(Post, verbose_name=_("Post"), on_delete=models.CASCADE)
    liked = models.BooleanField(default=False)
    disliked = models.BooleanField(default=False)


class Comment(models.Model):
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE)
    post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    reply_to = models.ForeignKey("self", null=True, blank=True, on_delete=models.CASCADE, related_name='replies')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.content


class Image(models.Model):
    post = models.ForeignKey('Post', verbose_name=_('post'), on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='post/image/')
    is_featured = models.BooleanField(verbose_name=_('is featured'), default=False)
    alt = models.CharField(verbose_name=_('alternative'), max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-is_featured', '-created_at']


class Tag(models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class PostTagFollow(models.Model):
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE)
    tag = models.ForeignKey('Tag', on_delete=models.CASCADE)
