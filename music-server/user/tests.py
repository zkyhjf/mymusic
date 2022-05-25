from unittest import TestCase
import requests


class UserTest(TestCase):
    """针对用户模块的测试"""
    def setUp(self):
        """初始化请求根路径"""
        self.base_url = 'http://127.0.0.1:8000/user'

    def test_login(self):
        """测试用户登录接口"""
        user_from = {'username': 'abc', 'password': '123456'}
        r = requests.post(self.base_url + '/login', data=user_from)
        result = r.json()
        self.assertEqual(result.get('data').get('username'), 'abc')

    def test_get_favorites(self):
        """测试获取用户收藏的歌曲接口"""
        headers = {
            'Authorization': 'jwt eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.'
                             'eyJ1c2VyX2lkIjo0LCJ1c2VybmFtZSI6ImFiYyIs'
                             'ImV4cCI6MTY1MjE5NTE0MiwiZW1haWwiOiJhYmNAcXEuY29tIn0.'
                             'aZkiIHDdUfvl1iT2h9mb3_VVDypFOglBLSmKnA16EEA'
        }
        r = requests.get(f'{self.base_url}/favorites', headers=headers)
        result = r.json()
        self.assertEqual(result.get('data')[0].get('id'), '1293886117')

    def test_check_favorites(self):
        """测试判断歌曲是否为用户收藏接口"""
        params = {
            'songid': '1293886117'
        }
        headers = {
            'Authorization': 'jwt eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.'
                             'eyJ1c2VyX2lkIjo0LCJ1c2VybmFtZSI6ImFiYyIs'
                             'ImV4cCI6MTY1MjE5NTE0MiwiZW1haWwiOiJhYmNAcXEuY29tIn0.'
                             'aZkiIHDdUfvl1iT2h9mb3_VVDypFOglBLSmKnA16EEA'
        }
        r = requests.get(f'{self.base_url}/favorites/check', params=params, headers=headers)
        result = r.json()
        self.assertTrue(result.get('data').get('is_favorites'))
