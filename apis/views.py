from django.shortcuts import render
from django.conf import settings
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import get_user_model,authenticate
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status, permissions, pagination
from rest_framework.pagination import PageNumberPagination
from django.contrib.auth.hashers import make_password
from .models import *
from datetime import date,timedelta
from .serializers import *

class CustomPagination(pagination.PageNumberPagination):
    page_size = 2  # Number of items per page
    page_size_query_param = 'page_size'
    max_page_size = 10  # Maximum number of items per page

    def get_paginated_response(self, data):
        return Response({
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'count': self.page.paginator.count,
            'results': data
        })


User=get_user_model()

class Signup(APIView):
    permission_classes=[AllowAny]
    def post(self,request):
        if "username" not in request.data:
            Err="username not Given"
            return Response({"msg":"Username missing"},status=status.HTTP_401_UNAUTHORIZED)

        if "password" not in request.data:
            return Response({"msg":"Password missing"},status=status.HTTP_401_UNAUTHORIZED)       


        username=request.data["username"].replace(" ","")
        password=request.data['password'].replace(" ","")

        if User.objects.filter(username=username).exists():
            return Response({"msg":"User is  exist try another"},status=status.HTTP_401_UNAUTHORIZED)
        
        try:
            hash_password=make_password(password)
            User(username=username,password=hash_password,email=username,isVerify=True).save()
            return Response({"msg":"Registation s successfull"}, status=status.HTTP_200_OK)
                
        except:
            return Response({"msg":"Invalid"}, status=status.HTTP_401_UNAUTHORIZED)



class Login(APIView):
    permission_classes=[AllowAny]
    def post(self,request):
        if "username" not in request.data:
            Err="username not Given"
            return Response({"msg":"Username missing"},status=status.HTTP_401_UNAUTHORIZED)

        if "password" not in request.data:
            return Response({"msg":"Password missing"},status=status.HTTP_401_UNAUTHORIZED)       


        username=request.data["username"].replace(" ","")
        password=request.data['password'].replace(" ","")

        if not  User.objects.filter(username=username).exists():
            return Response({"msg":"User Not exist"},status=status.HTTP_401_UNAUTHORIZED)
        
        try:
            if authenticate(username=username, password=password):
                user = User.objects.get(username=username)
                token, _ = Token.objects.get_or_create(user=user)
                return Response({'token': token.key,"msg":"Login successfull"}, status=status.HTTP_200_OK)
                
        except:
            return Response({"msg":"Invalid"}, status=status.HTTP_401_UNAUTHORIZED)


class LogoutAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # Delete the user's token to force logout
        request.user.auth_token.delete()
        return Response({"detail": "Successfully logged out."})

class createPost(APIView):
    permission_classes=[IsAuthenticated]
    def post(self,request):
        data=request.data
        if 'title' not in data:
            return Response({"msg":"please write somthing in titel"},status=401)
        if 'content' not in data:
            return Response({"msg":"please write somthing in content"},status=401) 
    
        serializer=PostModelSerializer(data=data,context={'user':request.user})
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            print(serializer.data)
            return Response({"data":serializer.data,"msg":"data save successfull"},status=201)
        return Response({"msg":"somthing went Wrong"},status=401)
    
class getlistPost(APIView):
    permission_classes=[IsAuthenticated]
    pagination_class = CustomPagination
    def get(self,request):
        queryset=Post.objects.all()
        serializer=PostSerializer(queryset,many=True)
        print(serializer.data)
        return Response({"data":serializer.data},status=200)
    
class updatePost(APIView):
    permission_classes=[IsAuthenticated]
    def patch(self,request,pk=None):
        data=request.data
        #here it will check if the user own this post or not if not it will return you can not change it
        if not Post.objects.filter(author=request.user,pk=pk).exists():
            return Response({"msg":"you can not edit this"},status=401)
        instance=Post.objects.get(pk=pk)
        serializer=PostSerializer(instance,data=data,partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    
class deletePost(APIView):
    permission_classes=[IsAuthenticated]
    def delete(self,request,pk=None):
        if not Post.objects.filter(author=request.user,pk=pk).exists():
            return Response({"msg":"you can not delete  this"},status=401)
        
        Post.objects.get(pk=pk).delete()
        return Response({"msg":"Post delete succeful"})

class commentPost(APIView):
    permission_classes=[IsAuthenticated]
    def post(self,request,pk=None):
        if not Post.objects.filter(pk=pk).exists():
            return Response({"msg":"you can not delete  this"},status=401)

        if 'content' not in request.data:
            return Response({"msg":"Content is not there"},status=401)
        
        comment=Comment.objects.create(author=request.user,text=request.data.get('content',""))
        post=Post.objects.get(pk=pk)
        post.comment.add(comment)

        return Response({"msg":"comment has been add"},status=201)
    
class likePost(APIView):
    permission_classes=[IsAuthenticated]
    def post(self,request,pk=None):
        if not Post.objects.filter(pk=pk).exists():
            return Response({"msg":"you can not delete  this"},status=401)
        user=request.user
        post=Post.objects.get(pk=pk)
        
        if  Like.objects.filter(author=user).exists():
            like=Like.objects.get(author=request.user)
            post.like.remove(like)
            like.delete()
            post.save()
            likes_count = post.like.count()
            return Response({"msg":"like has been removed","data":likes_count},status=201)
        else:
            like=Like.objects.create(author=request.user)
            post.like.add(like)
            post.save()
            likes_count = post.like.count()
            return Response({"msg":"like has been added","data":likes_count},status=201)

        
        


        


    
