from flask import current_app, jsonify
from flask import g
from flask import render_template
from flask import request
from flask import session

from info import constants
from info import redis_store
from info.models import User, News, Category
from info.utils.common import user_login_data
from info.utils.response_code import RET
from . import index_blu


@index_blu.route('/news_list')
def news_list():
    cid = request.args.get("cid", "1")
    page = request.args.get("page", "1")
    per_page = request.args.get("per_page", "10")

    try:
        page = int(page)
        cid = int(cid)
        per_page = int(per_page)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.PARAMERR, errmsg="参数")
    filters = [News.status == 0]
    if cid != 1:
        filters.append(News.category_id == cid)

    try:
        paginate = News.query.filter(*filters).order_by(News.create_time.desc()).paginate(page, per_page, False)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="数据查询错误")

    news_model_list = paginate.items
    total_page = paginate.pages
    current_page = paginate.pages

    news_dict_li = []
    for news in news_model_list:
        news_dict_li.append(news.to_basic_dict())
    data = {
        "total_page":total_page,
        "current_page":current_page,
        "news_dict_li":news_dict_li
    }

    return jsonify(errno=RET.OK, errmsg="OK", data=data)

@index_blu.route('/')
@user_login_data
def index():
    """
    显示首页
    1. 如果用户已经登录，将当前`登录用户的数据传到模板中，供模板显示

    """
    # 显示用户是否登录的逻辑
    # 取到用户id
    # user_id = session.get("user_id", None)
    # user = None
    # if user_id:
    #     # 尝试查询用户的模型
    #     try:
    #         user = User.query.get(user_id)
    #     except Exception as e:
    #         current_app.logger.error(e)

    user = g.user

    # 右侧的新闻排行的逻辑
    news_list = []
    try:
        news_list = News.query.order_by(News.clicks.desc()).limit(constants.CLICK_RANK_MAX_NEWS)
    except Exception as e:
        current_app.logger.error(e)

    # 定义一个空的字典列表，里面装的就是字典
    news_dict_li = []
    # 遍历对象列表，将对象的字典添加到字典列表中
    for news in news_list:
        news_dict_li.append(news.to_basic_dict())

    # 查询分类数据，通过模板的形式渲染出来
    categories = Category.query.all()

    category_li = []
    for category in categories:
        category_li.append(category.to_dict())

    data = {
        "user": user.to_dict() if user else None,
        "news_dict_li": news_dict_li,
        "category_li": category_li
    }
    print(data)

    return render_template('news/index.html', data=data)


# 在打开网页的时候，浏览器会默认去请求根路径+favicon.ico作网站标签的小图标
# send_static_file 是 flask 去查找指定的静态文件所调用的方法
@index_blu.route('/favicon.ico')
def favicon():
    return current_app.send_static_file('news/favicon.ico')
