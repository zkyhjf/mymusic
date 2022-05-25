from django.db import IntegrityError
from django.contrib.auth.models import make_password
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from common.response import Response
from .serializers import UserSerializer, FavoritesSerializer
from .models import User, Favorites


@api_view(['POST'])
def register(request):
    """用户注册"""
    # 获取注册用户数据
    serializer = UserSerializer(data=request.data)

    # 请求数据不合法，返回错误提示
    if not serializer.is_valid():
        return Response.fail('参数错误')

    # 访问serializer.data后就不能调用save方法了，需要使用validated_data访问数据
    username = serializer.validated_data['username']    # 获取serializer中的用户名

    # 判断用户名是否已存在
    user = User.objects.filter(username=username).first()
    if user:
        return Response.fail('用户名已存在')

    # 密码加密处理
    password = serializer.validated_data['password']
    serializer.validated_data['password'] = make_password(password)

    # 用户数据保存到数据库
    serializer.save()
    return Response.success('注册成功')


@api_view(['GET'])
@permission_classes([IsAuthenticated])      # 用户经过认证后才能访问
def get_favorites(request):
    """获取用户收藏的歌曲"""
    user_id = request.user.id      # 获取当前登录用户id
    songs = get_object_or_404(User, id=user_id).favorites.all()
    return Response(songs, exclude='lrc')


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def check_favorites(request):
    """判断歌曲是否为用户收藏"""
    # 获取请求数据
    song_id = request.GET.get('songid')  # 获取歌曲id

    # 歌曲id为空时返回错误信息
    if not song_id:
        return Response.fail('歌曲id不能为空')

    user_id = request.user.id      # 获取当前登录用户id

    # 判断指定用户是否收藏指定歌曲
    favorites = Favorites.objects.filter(user_id=user_id, song_id=song_id)
    res = {'is_favorites': False}
    if not favorites:
        return Response(res)
    res['is_favorites'] = True
    return Response(res)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_favorites(request):
    """添加用户收藏"""
    user_id = request.user.id  # 获取当前登录用户id
    data = {
        'user_id': user_id,
        'song_id': request.data.get('songid')
    }

    # 根据已有数据构造序列化器
    serializer = FavoritesSerializer(data=data)

    # 请求数据不合法，返回错误提示
    if not serializer.is_valid():
        return Response.fail('参数错误')

    # 保存数据，并检查数据库完整性错误
    try:
        serializer.save()
    except IntegrityError:
        return Response.fail('不能重复收藏歌曲')
    return Response.success('添加用户收藏成功')


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def delete_favorites(request):
    """取消用户收藏"""
    # 获取请求数据
    song_id = request.data.get('songid')  # 获取歌曲id

    # 歌曲id为空时返回错误信息
    if not song_id:
        return Response.fail('歌曲id不能为空')

    user_id = request.user.id  # 获取当前登录用户id

    # 删除指定数据
    favorites = get_object_or_404(Favorites, user_id=user_id, song_id=song_id)
    favorites.delete()
    return Response.success('取消用户收藏成功')