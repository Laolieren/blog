# coding:utf-8

from flask import request, jsonify, current_app, session
from . import api
from myblog.utils.response_code import RET
from myblog import db, models, redis_store, constants
from myblog.models import User
import logging, re


@api.route("/sessions", methods=["POST"])
def login():
    """登录"""
    # 获取参数、用户手机号  密码
    req_dict = request.get_json()
    mobile = req_dict.get("mobile")
    password = req_dict.get("password")

    # 检验参数
    if not all([mobile, password]):
        return jsonify(errno=RET.PARAMERR, errmsg="参数不完整")

    # 判断手机号格式
    if not re.match(r"1[34578]\d{9}", mobile):
        return jsonify(errno=RET.PARAMERR, errmsg="手机号格式不正确")

    # 判断用户的错误次数
    # 从redis中获取错误次数
    user_ip = request.remote_addr
    try:
        access_counts = redis_store.get("access_%s" % user_ip)
    except Exception as e:
        current_app.logger.error(e)
    else:
        # 如果有错误次数记录，并且超过最大次数，直接返回
        if access_counts is not None and int(access_counts) >= constants.LOGIN_ERROR_MAX_NUM:
            return jsonify(errno=RET.REQERR, errmsg="登录过于频繁")

    # 查询数据库，判断用户信息与密码
    try:
        user = User.query.filter_by(mobile=mobile).first()
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="查询用户信息异常")

    if user is None or not user.check_password(password):
        # 出现错误，累加错误次数
        try:
            redis_store.incr("access_%s" % user_ip)
            redis_store.expire("access_%s" % user_ip, constants.LOGIN_ERROR_FORBID_TIME)
        except Exception as e:
            current_app.logger.error(e)

        return jsonify(errno=RET.LOGINERR, errmsg="用户名或密码失败")

    # 登录成功，
    # 清除用户的登录错误次数
    try:
        redis_store.delete("access_%s" % user_ip)
    except Exception as e:
        current_app.logger.error(e)

    # 保存用户的登录状态
    session["user_id"] = user.id
    session["user_name"] = user.name
    session["mobile"] = user.mobile

    return jsonify(errno=RET.OK, errmsg="用户登录成功")


@api.route("/session", methods=["GET"])
def check_login():
    """检查登陆状态"""
    # 尝试从session中获取用户的名字
    name = session.get("user_name")
    # 如果session中数据name名字存在，则表示用户已登录，否则未登录
    if name is not None:
        return jsonify(errno=RET.OK, errmsg="true", data={"name": name})
    else:
        return jsonify(errno=RET.SESSIONERR, errmsg="false")


@api.route("/session", methods=["DELETE"])
def logout():
    """登出"""
    # 清除session数据
    session.clear()
    return jsonify(errno=RET.OK, errmsg="OK")