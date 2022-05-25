from django.urls import path
from rest_framework_jwt.views import obtain_jwt_token
from . import views

urlpatterns = [
    path('login', obtain_jwt_token),                          # 用户登录
    path('register', views.register),                         # 用户注册
    path('favorites', views.get_favorites),                   # 获取用户收藏的歌曲
    path('favorites/check', views.check_favorites),           # 判断歌曲是否为用户收藏
    path('favorites/add', views.add_favorites),               # 添加用户收藏
    path('favorites/delete', views.delete_favorites)          # 取消用户收藏
]