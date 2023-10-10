from django.db import models
from django.urls import reverse
from django.utils.html import format_html
from django.utils.text import slugify

from account.models import User


# Create your models here.
class Category(models.Model):
    title=models.CharField(max_length=40)
    publish_time = models.DateTimeField(auto_now_add=True)
    slug=models.SlugField(blank=True)
    def get_absolute_url(self):
        return reverse("blog_app:category_subset",args=[self.slug])
    def save(
        self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        self.slug=slugify(self.title)
        super().save()
    def __str__(self):
        return self.title
    class Meta:
        verbose_name="دسته بندی"
        verbose_name_plural="دسته بندی ها"
class Article(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,verbose_name="نویسنده")
    title=models.CharField(max_length=30,verbose_name="عنوان")
    category=models.ManyToManyField(Category,related_name='articles',verbose_name='')
    body=models.TextField(verbose_name="متن ")
    created_at=models.DateTimeField(auto_now_add=True)
    edited_at=models.DateTimeField(auto_now=True)
    slug=models.SlugField(blank=True,)
    image=models.ImageField(upload_to="images/article",blank=True,null=True,default="images/defult.jpeg")

    status=models.BooleanField(default=True,verbose_name="وضعیت")

    def get_absolute_url(self):
        return reverse("blog_app:detail",args=[self.slug])
    def save(
        self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        self.slug=slugify(self.title)
        super(Article,self).save()
    def showImages(self):
        return format_html(f"<img src='{self.image.url}' width='70px'>")
    def __str__(self):
        return self.title+" - "+self.body[:30]
    class Meta:
        verbose_name="مقاله"
        verbose_name_plural="مقالات"

class Comment(models.Model):
    article= models.ForeignKey(Article,on_delete=models.CASCADE,related_name="comments")
    created_at = models.DateField(auto_now_add=True)
    user =models.ForeignKey(User,on_delete=models.CASCADE,related_name="comments")
    parent=models.ForeignKey("self",on_delete=models.CASCADE,related_name="reply",null=True,blank=True)
    body=models.TextField()
    class Meta:
        verbose_name="کامنت"
        verbose_name_plural="کامنت ها"

    def __str__(self):
          return self.body[:50]

class Like(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name="likes")
    article=models.ForeignKey(Article,on_delete=models.CASCADE,related_name="likes",null=True,blank=True)
    created_at=models.DateTimeField(auto_now_add=True)
    comment=models.ForeignKey(Comment, on_delete=models.CASCADE,related_name="likes",null=True,blank=True)
    def __str__(self):
        if self.article is not None:
            return f"{self.user.username} - {self.article.title}"
        if self.comment is not None:
            return f"{self.user.username} - {self.comment.body[:50]}"

    class Meta:
        verbose_name = "لایک"
        verbose_name_plural = "لایک ها"