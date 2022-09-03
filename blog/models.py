import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models


class CommonModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(max_length=60, null=True)
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.CharField(max_length=60, null=True)

    class Meta:
        abstract = True


class Role(CommonModel):
    role_id = models.AutoField(primary_key=True)
    role_name = models.CharField(max_length=100)
    def __str__(self):
        return self.role_name


class User(CommonModel, AbstractUser):
    id = models.AutoField(primary_key=True)
    email = models.CharField(max_length=100, unique=True)
    date_of_birth = models.DateField()
    phone = models.CharField(max_length=15)
    picture = models.TextField(blank=True)
    is_blocked = models.BooleanField(default=False)
    wrong_password_attempt = models.IntegerField(default=0)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)

    username = None
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []


    def __str__(self):
        return self.first_name + ' ' + self.last_name


class Country(CommonModel):
    country_id = models.AutoField(primary_key=True)
    country_name = models.CharField(max_length=100)
    code_iso3 = models.CharField(max_length=3)
    def __str__(self):
        return self.country_name


class City(CommonModel):
    city_id = models.AutoField(primary_key=True)
    city_name = models.CharField(max_length=100)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    def __str__(self):
        return self.city_name


class Address(CommonModel):
    address_id = models.AutoField(primary_key=True)
    is_primary = models.BooleanField(default=False)
    province = models.CharField(max_length=100)
    street = models.CharField(max_length=500)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    def __str__(self):
        return self.street


class Member(CommonModel):
    member_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    def __str__(self):
        return self.user.__str__()


class Author(CommonModel):
    author_id = models.AutoField(primary_key=True)
    nbr_of_posts = models.IntegerField(default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    def __str__(self):
        return self.user


class Admin(CommonModel):
    admin_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    def __str__(self):
        return self.user.__str__()

class Category(CommonModel):
    category_id = models.AutoField(primary_key=True)
    category_name = models.CharField(max_length=100)
    def __str__(self):
        return self.category_name

class Article(CommonModel):
    article_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)
    content = models.TextField(blank=True)
    image = models.TextField(blank=True)
    nbr_likes = models.IntegerField(default=0)
    nbr_dislikes = models.IntegerField(default=0)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    def __str__(self):
        return self.title


class Post(CommonModel):
    post_id = models.AutoField(primary_key=True)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    post_date = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.article.__str__()


class Comment(CommonModel):
    comment_id = models.AutoField(primary_key=True)
    content = models.CharField(max_length=500)
    image = models.TextField(blank=True)
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    def __str__(self):
        return self.content


class Like(CommonModel):
    like_id = models.AutoField(primary_key=True)
    is_like = models.BooleanField(default=True)
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    def __str__(self):
        return self.like_id


class Token(CommonModel):
    token_id= models.AutoField(primary_key=True)
    expire_at= models.DateTimeField()
    token= models.UUIDField(default=uuid.uuid4)
    user= models.ForeignKey(User, on_delete=models.CASCADE)

# class ConstantType(CommonModel):
#     constant_type_id= models.AutoField(primary_key=True)
#     value=  models.CharField(max_length=200)
#
# class Constant(CommonModel):
#     constant_id= models.AutoField(primary_key=True)
#     value= models.CharField(max_length=200)
#     constantType= models.ForeignKey(ConstantType, on_delete=models.CASCADE)