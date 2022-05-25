from django.http import JsonResponse
from django.db.models.query import QuerySet
from django.db.models import Model
from django.forms.models import model_to_dict


class Response(JsonResponse):
    def __init__(self, data, msg='操作成功', status=200, exclude=None):
        """
        初始化属性
        :param data: 通信数据
        :param msg: 通信描述
        :param status: 通信状态
        :param exclude: 指定数据中需排除的字段，使其不传给前端
        """
        if exclude is None:
            exclude = []
        self.data = data
        self.covert_data(exclude=exclude)

        # 数据为空不返回
        if not self.data:
            result = {
                'msg': msg,
                'status': status
            }
        else:
            result = {
                'data': self.data,
                'msg': msg,
                'status': status
            }
        super().__init__(result, safe=False, json_dumps_params={'ensure_ascii': False})

    def covert_data(self, exclude):
        """数据转化为列表或字典"""
        if isinstance(self.data, QuerySet):
            # QuerySet对象转为字典列表，并指定数据转化时需排除的字段
            data_tmp = []
            for item in self.data:
                data_tmp.append(model_to_dict(item, exclude=exclude))
            self.data = data_tmp
        elif isinstance(self.data, Model):
            # 单个模型类对象转为字典，并指定数据转化时需排除的字段
            self.data = model_to_dict(self.data, exclude=exclude)
        elif isinstance(self.data, dict):
            # 移除字典指定键的元素
            self.data = dict(filter(lambda x: x[0] not in exclude, self.data.items()))

    @staticmethod
    def success(msg, status=200):
        """返回成功消息"""
        return Response(None, msg, status)

    @staticmethod
    def fail(msg, status=400):
        """返回失败消息"""
        return Response(None, msg, status)