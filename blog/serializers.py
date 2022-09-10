from os import write

from django.urls import path, include
from .models import Article, Post, Category, Country, City, Address, Author, Admin, Member, Comment, Role, User, Like, \
    Token
from rest_framework import serializers

class RoleSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Role
        fields = ['role_id', 'role_name']

class UserSerializer(serializers.HyperlinkedModelSerializer):
    role = RoleSerializer(read_only=True)
    role_id = serializers.IntegerField()
    password = serializers.CharField(max_length=100, required=False, default=None)
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email', 'date_of_birth', 'phone', 'picture', 'is_blocked','wrong_password_attempt', 'role', 'role_id', 'password', 'is_active']

    def create(self, validated_data):
        password = validated_data.pop('password')
        instance = self.Meta.model(**validated_data)
        instance.set_password(password)
        instance.save()
        return instance

class CountrySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Country
        fields = ['country_id', 'country_name', 'code_iso3']

class CitySerializer(serializers.HyperlinkedModelSerializer):
    country = CountrySerializer()
    class Meta:
        model = City
        fields = ['city_id', 'city_name', 'country']

class AddressSerializer(serializers.HyperlinkedModelSerializer):
    user = UserSerializer()
    city = CitySerializer()
    class Meta:
        model = Address
        fields = ['address_id', 'is_primary', 'province', 'street', 'user', 'city']

class MemberSerializer(serializers.HyperlinkedModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Member
        fields = ['member_id', 'user']

class AuthorSerializer(serializers.HyperlinkedModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Author
        fields = ['author_id', 'nbr_of_posts','user']

class AdminSerializer(serializers.HyperlinkedModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Admin
        fields = ['admin_id', 'user']


class CategorySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Category
        fields = ['category_id', 'category_name']


class CommentSerializer(serializers.HyperlinkedModelSerializer):
    user_id = serializers.IntegerField()
    article_id = serializers.IntegerField()
    class Meta:
        model = Comment
        fields = ['comment_id', 'content', 'image', 'user_id', 'article_id']

class ArticleSerializer(serializers.HyperlinkedModelSerializer):
    category = CategorySerializer(read_only=True)
    category_id = serializers.IntegerField()
    # image = serializers.ImageField(required=False)
    class Meta:
        model = Article
        fields = ['article_id', 'title', 'content', 'image', 'nbr_likes', 'nbr_dislikes', 'category_id', 'created_at', 'category']

class PostSerializer(serializers.HyperlinkedModelSerializer):
    author = AuthorSerializer()
    article = ArticleSerializer()
    class Meta:
        model = Post
        fields = ['post_id', 'article', 'author', 'post_date']



class LikeSerializer(serializers.HyperlinkedModelSerializer):
    member = MemberSerializer()
    article = ArticleSerializer()
    class Meta:
        model = Like
        fields = ['like_id', 'is_like', 'member', 'article']

class TokenSerializer(serializers.HyperlinkedModelSerializer):
    user = UserSerializer()
    user_id = serializers.IntegerField()
    email = serializers.CharField(max_length=100, write_only=True)

    class Meta:
        model = Token
        fields = ['token_id', 'token', 'user', 'user_id', 'email']


