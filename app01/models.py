from django.db import models

# Create your models here.


# 用户表
class User(models.Model):
    name = models.CharField(max_length=32)
    pwd = models.CharField(max_length=32)
    email = models.EmailField()
    register_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


# 文章表
class Article(models.Model):
    TYPE = (
        (1,  u"51区"),
        (2,  u"段子"),
        (3,  u"图片"),
    )
    type = models.IntegerField(choices=TYPE)
    title = models.CharField(max_length=256)
    url = models.URLField()
    abstract = models.CharField(max_length=256, null=True, blank=True)
    user = models.ForeignKey("User", null=True, blank=True)
    recommend = models.ManyToManyField("User", blank=True, related_name="RA")
    favorite = models.ManyToManyField("User", blank=True, related_name="FA")
    add_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.abstract


# 评论表
class Comment(models.Model):
    user = models.ForeignKey("User")
    article = models.ForeignKey("Article", null=True, blank=True)
    text = models.CharField(max_length=256)
    add_time = models.DateTimeField(auto_now_add=True)
    father_comment = models.ForeignKey("self", default=False)

    def __str__(self):
        return self.text


# 图片表
class Picture(models.Model):
    article = models.ForeignKey("Article", default=None)
    describe = models.CharField(max_length=256, default=None)
    pic = models.FileField()

