from django.db import models
from django.utils.html import mark_safe
from django.urls import reverse
from User_app.models import User
import uuid
from django.db.models.signals import post_save, post_delete
from django.utils.text import slugify
from shortuuid.django_fields import ShortUUIDField


# Create your models here.
def user_directory_path(instance, filename):
    return 'user_{0}/{1}'.format(instance.user.id, filename)

class Category(models.Model):
    cid = ShortUUIDField(unique=True, length=10, max_length=20,prefix="cat", alphabet="abcdefgh12345",verbose_name='カテゴリーのid')
    title = models.CharField(max_length=100, default="Food",verbose_name='カテゴリー名')
    image = models.ImageField(upload_to="category", default="category.jpg",verbose_name='カテゴリーの写真')
    class Meta:
        verbose_name_plural = "カテゴリー"

    def category_image(self):
        return mark_safe('<img src="%s" width="150" height="50" />' % (self.image.url))



    def __str__(self):
        return self.title

class Tag(models.Model):
    title = models.CharField(max_length=75, verbose_name='タグ')
    slug = models.SlugField(null=False, unique=True, default=uuid.uuid1)

    class Meta:
        verbose_name = 'タグ'
        verbose_name_plural = 'タグ'

    def get_absolute_url(self):
        return reverse('tags', args=[self.slug])

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)
class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False,verbose_name='ポストid')
    picture = models.ImageField( upload_to=user_directory_path, default="product.jpg",verbose_name='ポストの写真')
    category = models.ForeignKey( Category, on_delete=models.SET_NULL, null=True, related_name="category",verbose_name='カテゴリー')

    caption = models.CharField(max_length=100, default="Fresh Pear",verbose_name='ポスト名')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True,verbose_name='ユーザ')
    tags=models.ManyToManyField(Tag,related_name='tags',verbose_name='タグ')
    description=models.TextField()

    posted = models.DateField(auto_now_add=True)
    description=models.TextField()
    status = models.BooleanField(default=True,verbose_name='ステータス')
    # section=models.ForeignKey(Section,on_delete=models.SET_NULL,null=True,verbose_name='セクション')
    class Meta:
        verbose_name_plural='ポスト'
    def get_absolute_url(self):
        return reverse("post-details", args=[str(self.id)])
    

class Follow(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='follower')
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following')

    class Meta:
        verbose_name_plural='フォロー'
    def user_follow(sender, instance, *args, **kwargs):
        follow = instance
        sender = follow.follower
        following = follow.following

    def user_unfollow(sender, instance, *args, **kwargs):
        follow = instance
        sender = follow.follower
        following = follow.following


class Stream(models.Model):
    following = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='stream_following')
    user = models.ForeignKey(User, on_delete=models.CASCADE,verbose_name='ユーザ')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True,verbose_name='ポスト')
    date = models.DateTimeField()


    def add_post(sender, instance, *args, **kwargs):
        post = instance
        user = post.user
        followers = Follow.objects.all().filter(following=user)

        for follower in followers:
            stream = Stream(post=post, user=follower.follower, date=post.posted, following=user)
            stream.save()
post_save.connect(Stream.add_post, sender=Post)

post_save.connect(Follow.user_follow, sender=Follow)
post_delete.connect(Follow.user_unfollow, sender=Follow)