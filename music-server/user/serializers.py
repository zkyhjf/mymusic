from rest_framework import serializers
from .models import User, Favorites


class UserSerializer(serializers.ModelSerializer):
    """用户数据序列化器"""
    username = serializers.CharField(min_length=3, max_length=10)
    password = serializers.CharField(min_length=6, max_length=15)

    class Meta:
        model = User                # 指定用户模型
        fields = '__all__'          # 序列化所有字段


class FavoritesSerializer(serializers.ModelSerializer):
    """用户收藏数据序列化器"""
    class Meta:
        model = Favorites           # 指定用户收藏模型
        fields = '__all__'          # 序列化所有字段