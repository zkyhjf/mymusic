from unittest import TestCase
import requests


class SongTest(TestCase):
    """针对歌曲模块的测试"""
    def setUp(self):
        """初始化请求根路径"""
        self.base_url = 'http://127.0.0.1:8000/song'

    def test_song_detail(self):
        """测试根据歌曲id获取歌曲数据接口"""
        song_id = '1293886117'
        api_url = f'{self.base_url}/detail?songid={song_id}'
        r = requests.get(api_url)
        result = r.json()
        self.assertEqual(result.get('data').get('title'), '年少有为')

    def test_search_song(self):
        """测试根据关键词搜索音乐接口"""
        keyword = '张杰'
        api_url = f'{self.base_url}/search?keyword={keyword}'
        r = requests.get(api_url)
        result = r.json()
        song = {
            'id': '28059417',
            'title': '他不懂',
            'author': '张杰',
            'url': 'http://music.163.com/song/media/outer/url?id=28059417.mp3',
            'pic': 'http://p2.music.126.net/mW53BkMgGy37I7yVrUg-aQ==/109951163117902077.jpg?param=300x300'
        }
        self.assertIn(song, result.get('data'))

    def test_song_toplist(self):
        """测试获取排行榜歌曲数据接口"""
        params = {
            'category': 2,
            'size': 5
        }
        r = requests.get(self.base_url + '/toplist', params=params)
        result = r.json()
        song = {
          'id': '1940770243',
          'title': '遥远的她',
          'author': '毛不易',
          'url': 'http://music.163.com/song/media/outer/url?id=1940770243.mp3',
          'pic': 'http://p2.music.126.net/rk7d6mL3Y5NKQ-2v-bQPZw==/109951167333213984.jpg?param=300x300'
        }
        self.assertEqual(len(result.get('data')), 5)
        self.assertIn(song, result.get('data'))