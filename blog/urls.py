
from django.urls import path
from .views import article_views, auth_views, posts_views, users_views, categories_views,  comment_views
from .views import MyTokenObtainPairView

from rest_framework_simplejwt.views import (
    TokenRefreshView,
)


urlpatterns = [
    # AUTHENTICATION
    path('register', auth_views.RegisterView.as_view()),
    path('forgot-password', auth_views.TokenCreate.as_view()),
    path('reset-password', auth_views.ResetPassword.as_view()),
    #SIMPLE JWT TOKEN
    path('token', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    #ARTICLE API VIEWS
    path('articles', article_views.ArticleList.as_view()),
    path('articles/add', article_views.ArticleCreate.as_view()),
    path('articles/<int:article_id>', article_views.ArticleRetrieveUpdateDestroy.as_view()),
    # POST API VIEWS
    path('posts', posts_views.PostsList.as_view()),
    path('posts/<int:post_id>', posts_views.PostRetrieveDestroyUpdate.as_view()),
    # USER API VIEWS
    path('users/<int:id>', users_views.UserRetrieveUpdateDestroy.as_view()),
    path('users', users_views.UsersList.as_view()),
    # CATEGORIES API VIEWS
    path('categories', categories_views.CategoriesList.as_view()),
    path('categories/add', categories_views.CategoriesCreate.as_view()),
    path('categories/<int:category_id>', categories_views.CategoriesRetrieveUpdateDestroy.as_view()),
    # COMMENTS API
    path('comments/add', comment_views.CommentCreate.as_view())

]