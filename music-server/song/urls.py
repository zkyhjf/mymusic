from django.urls import path
from . import views

urlpatterns = [
    path('detail', views.song_detail),      # 根据歌曲id获取歌曲数据
    path('search', views.search_song),      # 根据关键词搜索音乐
    path('toplist', views.song_toplist),    # 获取排行榜歌曲数据
    path('download', views.song_download)   # 歌曲下载
]