# -*-*-*-*- coding: utf-8 -*-*-*-*-
# @Time    : 2018/11/16 下午10:32
# @Author  : LpL
# @Email   : peilun2050@gmail.com
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*
import functools
import random
from collections import OrderedDict

from tornado import gen

from slowworld.services.manage_service import ScoreManageService, CollectionManageService
from slowworld.utils.date_util import str_to_timestamp


def get_banner(banner_addr=0, instrument_type=4):
    from slowworld.services.banner_service import BannerService
    return BannerService().find_many(**{'banner_addr': banner_addr, 'instrument': {'$in': [instrument_type]}})


@gen.coroutine
def get_banner_async(banner_addr=0, instrument_type=4):
    from slowworld.services.banner_service import BannerService
    ret = yield BannerService().find_many_async(**{'banner_addr': banner_addr, 'instrument': {'$in': [instrument_type]}})
    raise gen.Return(ret)


def get_category(category_type=0, instrument_type=4):
    from slowworld.services.category_service import CategoryService
    categories = CategoryService().find_many(
        **{'category_type': category_type, 'instrument': {'$in': [instrument_type]}})
    category_dict = OrderedDict()
    for item in categories:
        category_dict[item.key] = item.name
    return category_dict


@gen.coroutine
def get_category_async(category_type=0, instrument_type=4):
    from slowworld.services.category_service import CategoryService
    categories = yield CategoryService().find_many_async(
        **{'category_type': category_type, 'instrument': {'$in': [instrument_type]}})
    category_dict = OrderedDict()
    for item in categories:
        category_dict[item.key] = item.name
    raise gen.Return(category_dict)


def des_page_size(method):
    """
    分页装饰器
    :param method:
    :return:
    """

    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        page, size = int(self.get_argument('page', 0)), int(self.get_argument('size', 15))
        return method(self, page, size, *args, **kwargs)

    return wrapper


def des_chk_version(method):
    """
    版本装饰器
    :param method:
    :return:
    """

    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        # version = self.get_argument('version', '1.0')
        version = '1.0'
        return method(self, version, *args, **kwargs)

    return wrapper


def des_instrument(method):
    """
    乐器装饰器
    :param method:
    :return:
    """

    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        instrument_type = int(self.request.headers.get("instrument-type", 4))
        return method(self, instrument_type, *args, **kwargs)

    return wrapper


def des_score_filter(method):
    """
    最新 new：按照时间排序，不筛选分类
    推荐 recommend: 出banner，排序为hot

    :param method:
    :return:
    """

    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        instrument_type = int(self.request.headers.get("instrument-type", 4))
        version = self.request.headers.get("Version", '1.0')
        is_android = str(self.request.headers.get("platform", '')) == '1'
        category = self.get_argument('category', '')
        score_type = self.get_argument('type', 1)
        filter_query, sort_query, extra_query = {'bgt': {'$ne': {}}, 'diff': {'$gt': 27},
                                                 'instrument': {'$in': [instrument_type]}}, (('hot', -1),), \
                                                {'version': version, 'categories': get_category(2, instrument_type),
                                                 'need_vip': True, 'instrument_type': instrument_type,
                                                 'is_index': False, 'default_author': u'考级曲'}
        if category:
            if category == 'new':
                sort_query = (('add_time', -1), ('hot', -1))
            elif category == 'recommend':
                score_type = 1
                extra_query['banners'] = [banner.to_doc() for banner in get_banner(instrument_type=instrument_type)]
                extra_query['is_index'] = True
                filter_query['diff'] = {'$gte': 0}
                extra_query['default_author'] = u'练习曲'
            elif category == 'vip':
                filter_query['$or'] = [{'is_vip': 1}, {'is_vip_tmp': '1'}]
            else:
                filter_query['category'] = {'$in': [category]}
        else:
            if is_android or version != '1.0':
                filter_query['category'] = {'$in': ['popular']}

        is_tmp = False
        # 审核版本对应
        if not is_android and version == '1.0':
            filter_query['$and'] = [{'category': category if (category not in ['', 'new', 'recommend']) else 'tmp'},
                                    {'category': 'tmp'}]
            extra_query['categories'] = {'$in': ['tmp']}
            extra_query['need_vip'] = False
            is_tmp = True

        # 难度筛选
        if not int(score_type):
            filter_query['diff'] = {'$lte': 27}  # 入门以及普通以27作为限制
            extra_query['categories'] = {'$in': ['course']} if is_tmp else get_category(1, instrument_type)
            extra_query['default_author'] = u'练习曲'
        return method(self, filter_query, sort_query, extra_query, *args, **kwargs)

    return wrapper


def des_manage_filter(method):
    """
    最新 new：按照时间排序，不筛选分类
    推荐 recommend: 出banner，排序为hot

    :param method:
    :return:
    """

    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        instrument_type = int(self.request.headers.get("instrument-type", 4))
        category = self.get_argument('category', '')
        diff = self.get_argument('diff', "all")
        filter_query, sort_query, extra_query = {'instrument': {'$in': [instrument_type]}}, \
                                                (('hot', -1),), {'is_test': True}

        if category:
            filter_query['category'] = {'$in': [category]}

        if diff == "easy":
            filter_query['diff'] = {'$lte': 27}
        elif diff == "general":
            filter_query['diff'] = {'$gt': 27, "$lt": 50}
        elif diff == "difficult":
            filter_query['diff'] = {'$gte': 50}
        return method(self, filter_query, sort_query, extra_query, *args, **kwargs)

    return wrapper


def des_manage_sore(method):
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        score_id = self.get_argument('score_id', '')
        if not score_id:
            return self.write({'msg': '曲谱id不能为空', 'error': True})
        score = ScoreManageService().find_by_id(score_id)
        return method(self, score, *args, **kwargs)

    return wrapper


def des_manage_collection(method):
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        collection_id = self.get_argument('collection_id', '')
        if not collection_id:
            return self.write({'msg': '合集id不能为空', 'error': True})
        collection = CollectionManageService().find_by_id(collection_id)
        return method(self, collection, *args, **kwargs)

    return wrapper


def des_manage_scores(method):
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        score_ids = self.get_argument("score_id", "")
        if not score_ids:
            return self.write({'msg': '曲谱id不能为空', 'error': True})
        return method(self,
                      [ScoreManageService().find_by_id(score_id) for score_id in score_ids.split(",")],
                      *args, **kwargs)

    return wrapper


def des_manage_collections(method):
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        collection_ids = self.get_argument("collection_id", "")
        if not collection_ids:
            return self.write({'msg': '合集id不能为空', 'error': True})
        return method(self,
                      [CollectionManageService().find_by_id(collection_id) for collection_id in
                       collection_ids.split(",")],
                      *args,
                      **kwargs)

    return wrapper


def des_manage_search(method):
    @functools.wraps(method)
    def wrapper(self, filter_query, *args, **kwargs):
        text = self.get_argument("text", "")
        try:
            start_time = str_to_timestamp(self.get_argument("start_time", ""))
            end_time = str_to_timestamp(self.get_argument("end_time", ""))
        except ValueError:
            start_time = ""
            end_time = ""

        if text:
            filter_query['$text'] = {'$search': text}
        if start_time:
            filter_query["$or"] = [
                {"create_at": {"$gt": start_time, "$lt": end_time}},
                {"add_time": {"$gt": start_time, "$lt": end_time}}
            ]
        return method(self, filter_query, *args, **kwargs)

    return wrapper


def des_score_filter_v2(method):
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        instrument_type = int(self.request.headers.get("instrument-type", 4))
        version = self.request.headers.get("Version", '1.0')
        is_android = str(self.request.headers.get("platform", '')) == '1'
        category = self.get_argument('category', '')
        score_type = self.get_argument('type', 1)
        categories = get_category(2, instrument_type)
        filter_query, sort_query, extra_query = {'diff': {'$gt': 27},
                                                 'instrument': {'$in': [instrument_type]}}, (('hot', -1),), \
                                                {'version': version, 'categories': categories,
                                                 'need_vip': True, 'instrument_type': instrument_type,
                                                 'is_index': False, 'default_author': u'考级曲'}
        if category:
            if category == 'recommend':
                score_type = 1
                banners = get_banner(instrument_type=instrument_type)
                extra_query['banners'] = [banner.to_doc() for banner in banners]
                extra_query['is_index'] = True
                filter_query.pop("diff")
                extra_query['default_author'] = u'练习曲'
                filter_query['category'] = {'$in': [category]}

                # 随机推荐 筛选条件
                # filter_query["random_int"] = random.randrange(0, 1798)
                # extra_query["category"] = True

            elif category == 'vip':
                filter_query["is_vip"] = {"$gte": 1}
            else:
                filter_query['category'] = {'$in': [category]}
        else:
            if is_android or version != '1.0':
                filter_query['category'] = {'$in': ['popular']}

        is_tmp = False
        # 审核版本对应
        if not is_android and version == '1.0':
            filter_query['$and'] = [{'category': category if (category not in ['', 'new', 'recommend']) else 'tmp'},
                                    {'category': 'tmp'}]
            extra_query['categories'] = {'$in': ['tmp']}
            extra_query['need_vip'] = False
            is_tmp = True

        # 难度筛选
        if not int(score_type):
            filter_query['diff'] = {'$lte': 27}  # 入门以及普通以27作为限制
            extra_query['categories'] = {'$in': ['course']} if is_tmp else get_category(1, instrument_type)
            extra_query['default_author'] = u'练习曲'
        return method(self, filter_query, sort_query, extra_query, *args, **kwargs)

    return wrapper


def des_ai_score_filter(method):
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        instrument_type = int(self.request.headers.get("instrument-type", 4))
        category = self.get_argument('label', 'b1909939-429b-42d5-a22e-bbf9247a5b5f')
        score_type = self.get_argument('diff', "")
        filter_query, extra_query = {"category": {"$in": [category]}, 'instrument': {'$in': [instrument_type]}}, \
                                    {'categories': get_category(4, instrument_type), 'instrument_type': instrument_type}
        sort_query = (("create_at", -1),) if category == "ea857b69-ca8a-45a3-aadc-d5456c55b79a" else (("order", 1), ('hot', -1))

        # 难度筛选
        if score_type == "easy":
            filter_query['diff'] = {'$lte': 27}
        elif score_type == "general":
            filter_query['diff'] = {'$gt': 27, "$lt": 50}
        elif score_type == "difficult":
            filter_query['diff'] = {'$gte': 50}
        return method(self, filter_query, sort_query, extra_query, *args, **kwargs)

    return wrapper
