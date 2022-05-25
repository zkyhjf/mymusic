from django.utils.encoding import escape_uri_path
from rest_framework.decorators import api_view
from django.http import Http404, StreamingHttpResponse
from common.response import Response
from django.db.models import Q
from django.shortcuts import get_object_or_404
from .models import Song
import requests


@api_view(['GET'])
def song_detail(request):
    """根据歌曲id获取歌曲数据"""
    song_id = request.GET.get('songid')           # 获取歌曲id

    # 歌曲id为空时返回错误信息
    if not song_id:
        return Response.fail('歌曲id不能为空')

    # 获取歌曲数据，歌曲不存在时返回404
    song = get_object_or_404(Song, id=song_id)
    return Response(song)


@api_view(['GET'])
def search_song(request):
    """根据关键词搜索音乐"""
    keyword = request.GET.get('keyword')

    # 搜索关键词为空时返回错误信息
    if not keyword:
        return Response.fail('搜索关键词不能为空')

    # 模糊查询标题或作者包含关键词的歌曲
    songs = Song.objects.filter(Q(title__contains=keyword) | Q(author__contains=keyword))
    return Response(songs, exclude='lrc')


@api_view(['GET'])
def song_toplist(request):
    """获取排行榜歌曲数据"""
    category = request.GET.get('category')  # 排行榜类别
    size = request.GET.get('size')          # 获取歌曲数量

    # 排行榜类别为空时返回错误信息
    if not category or not size:
        return Response.fail('参数错误')

    # 根据排行榜类别查询歌曲数据，并按排名进行排序
    songs = Song.objects.filter(toplist__category=category).order_by('toplist.rank')
    return Response(songs[:int(size)], exclude='lrc')


@api_view(['GET'])
def song_download(request):
    """歌曲下载"""
    song_id = request.GET.get('songid')  # 获取歌曲id

    # 获取歌曲数据，歌曲不存在时返回404
    song = get_object_or_404(Song, id=song_id)

    try:
        response = StreamingHttpResponse(filestream(song.url))
        response['content_type'] = "application/octet-stream"
        response['Content-Disposition'] = "attachment; filename*=utf-8''{}.mp3".format(escape_uri_path(song.title))
        return response
    except Exception:
        raise Http404


def filestream(song_url):
    """生成歌曲文件流"""
    res = requests.get(song_url, stream=True)
    for chunk in res.iter_content(chunk_size=1024):
        yield chunk