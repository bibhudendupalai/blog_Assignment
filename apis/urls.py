from django.urls import path
from .views import *

urlpatterns = [
    # Endpoint for user registration
    path("signup/", Signup.as_view(), name='signup'),

    # Endpoint for user login
    path('signin/', Login.as_view(), name='signin'),

    # Endpoint for creating a new post
    path('createpost/', createPost.as_view(), name='createpost'),

    # Endpoint for retrieving a list of all posts
    path('getlistPost/', getlistPost.as_view(), name='getlistPost'),

    # Endpoint for updating a post by its primary key
    path('updateposts/<int:pk>/', updatePost.as_view(), name='updatePost'),

    # Endpoint for adding a comment to a post by its primary key
    path('commentposts/<int:pk>/', commentPost.as_view(), name='commentPost'),

    # Endpoint for liking/unliking a post by its primary key
    path('likeposts/<int:pk>/', likePost.as_view(), name='likePost'),
]