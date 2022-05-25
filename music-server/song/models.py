from django.db import models


class Song(models.Model):
    """歌曲模型类"""
    id = models.CharField('歌曲id', primary_key=True, max_length=20)
    title = models.CharField('歌曲名称', max_length=100)
    author = models.CharField('歌手', max_length=100)
    lrc = models.TextField('歌词')
    url = models.URLField('歌曲播放链接', max_length=250)
    pic = models.URLField('图片链接', max_length=100)

    class Meta:
        db_table = 'song'

    def __str__(self):
        return f'id:{self.id},title:{self.title},author:{self.author},url:{self.url},pic:{self.pic}'


class Toplist(models.Model):
    """排行榜模型类"""
    # 排行榜类别选项
    category_choices = (
        (1, '飙升榜'),
        (2, '新歌榜'),
        (3, '原创榜'),
        (4, '热歌榜')
    )

    rank = models.IntegerField('排名')
    # 一对多，一首歌曲可以在多个排行榜上
    song = models.ForeignKey(to='Song', on_delete=models.CASCADE, related_name='toplist')
    category = models.SmallIntegerField('排行榜类别', choices=category_choices)

    class Meta:
        db_table = 'toplist'