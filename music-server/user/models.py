from django.db import models
from django.contrib.auth.models import AbstractUser
from song.models import Song


class User(AbstractUser):
    """用户模型类"""
    # 性别选项
    gender_choices = (
        (1, '男'),
        (0, '女')
    )
    username = models.CharField('用户名', max_length=10, unique=True)
    gender = models.SmallIntegerField('性别', choices=gender_choices, blank=True)
    email = models.EmailField('邮箱', blank=True)
    tel = models.CharField('联系电话', max_length=20, blank=True)
    introduce = models.CharField('个人介绍', max_length=50, blank=True, null=True, default='')
    # 多对多，用户可以收藏多个歌曲
    favorites = models.ManyToManyField(
        to=Song, through='Favorites', through_fields=('user_id', 'song_id'))

    class Meta:
        db_table = 'user'       # 指定表名

    def __str__(self):
        return f'username:{self.username}, password:{self.password}, ' \
               f'gender:{self.gender}, email:{self.email}, tel:{self.tel}'


class Favorites(models.Model):
    """用户收藏模型类"""
    user_id = models.ForeignKey(to='User', db_column='user_id', on_delete=models.RESTRICT, related_name='favorites_user')
    song_id = models.ForeignKey(to=Song, db_column='song_id', on_delete=models.RESTRICT, related_name='favorites_song')
    create_time = models.DateTimeField('创建时间', auto_now_add=True, blank=True)   # 自动添加创建时间

    class Meta:
        db_table = "favorites"
        # 添加唯一约束
        constraints = [models.UniqueConstraint(fields=['user_id', 'song_id'], name='unique_favorites')]