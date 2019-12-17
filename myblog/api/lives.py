# coding:utf-8

from flask import request, jsonify, current_app, session
from . import api
from myblog.utils.response_code import RET
from myblog import db, models,constants
from myblog.models import Lives
import logging


@api.route("/lives", methods=["POST"])
def mylives():

    name = session.get("user_name")
    if name is None:
        return jsonify(errno=RET.ROLEERR, errmsg="对不起，只有站长才可以发表动态")
    req_dict = request.get_json()
    title = req_dict.get("title")
    content = req_dict.get("content")
    if not all([title, content]):
        return jsonify(errno=RET.PARAMERR, errmsg="参数不完整")

    lives = Lives(title=title, content=content)
    try:
        db.session.add(lives)
        db.session.commit()
    except Exception as e:
        current_app.logger.error(e)
        db.session.rollback()
        # 表示已经注册过
        resp = {
            "errno": RET.DATAERR,
            "errmsg": "数据创建失败"
        }
        return jsonify(resp)

    resp = {
        "errno": RET.OK,
        "errmsg": "发表成功"
    }
    return jsonify(resp)

@api.route("/lives", methods=["GET"])
def get_lives():
    page = request.args.get("page", 1)
    limit = request.args.get("limit")# 页数
    try:
        page = int(page)
        limit = int(limit)
    except Exception:
        page = 1
        limit = 6
    lives_query = Lives.query.order_by(Lives.create_time.desc())
    try:
        #                                 页数     每页数量                    错误输出
        live_page = lives_query.paginate(page, limit, False)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="数据库异常")

    live_li = live_page.items  # 当前页中的数据结果
    total_page = live_page.pages  # 总页数

    lives = []
    for live in live_li:
        lives.append(live.to_dict())

    return jsonify(errno=RET.OK,errmsg="查询成功",data={"lives":lives,"total_page":total_page,"current_page":page})