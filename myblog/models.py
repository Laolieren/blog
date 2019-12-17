# -*- coding:utf-8 -*-

from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from . import db


class BaseModel(object):
    """模型基类，为每个模型补充创建时间与更新时间"""

    create_time = db.Column(db.DateTime, default=datetime.now)  # 记录的创建时间
    update_time = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)  # 记录的更新时间


class User(BaseModel, db.Model):
    """用户"""

    __tablename__ = "user_profile"

    id = db.Column(db.Integer, primary_key=True)  # 用户编号
    name = db.Column(db.String(32), unique=True, nullable=False)  # 用户暱称
    password_hash = db.Column(db.String(128), nullable=False)  # 加密的密码
    mobile = db.Column(db.String(11), unique=True, nullable=False)  # 手机号

    @property
    def password(self):
        """对应password属性的读取操作"""
        raise AttributeError("不支持读取操作")

    @password.setter
    def password(self, value):
        """对应password属性的设置操作, value用户设置的密码值"""
        self.password_hash = generate_password_hash(value)

    def check_password(self, value):
        """检查用户密码， value 是用户填写密码"""
        return check_password_hash(self.password_hash, value)


class Lives(BaseModel, db.Model):
    """用户"""

    __tablename__ = "lives_profile"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(32), unique=True, nullable=False)
    content = db.Column(db.String(800), nullable=False)

    def to_dict(self):
        """将基本信息转换为字典数据"""
        lives_dict = {
            "live_id": self.id,
            "title": self.title,
            "content": self.content,
            "ctime": self.create_time.strftime("%Y-%m-%d")
        }
        return lives_dict
