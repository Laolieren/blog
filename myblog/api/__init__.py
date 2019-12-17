# coding:utf-8


from flask import Blueprint

# 创建蓝图对象
api = Blueprint("api", __name__)

from . import login, lives
