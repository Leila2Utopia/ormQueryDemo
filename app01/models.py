from django.db import models

# Create your models here.
class Book(models.Model):
    title = models.CharField(max_length=32)
    publishDate = models.DateField()
    price = models.DecimalField(max_digits=5, decimal_places=2)

    #创建一对多的关联字段
    publish = models.ForeignKey("Publish")

    #创建多对多的关系
    authors = models.ManyToManyField("Author")

    def __str__(self):return self.title

class Publish(models.Model):
    nid = models.AutoField(primary_key=True)
    name = models.CharField(max_length=32)
    email = models.EmailField()

class Author(models.Model):
    name = models.CharField(max_length=32)
    age = models.IntegerField()

class AuthorDetail(models.Model):
    addr = models.CharField(max_length=32)
    email = models.EmailField()
    author = models.OneToOneField("Author")


