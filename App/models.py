#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

#初始化db
db = SQLAlchemy()

class Grade(db.Model):
    '''班级模型'''
    g_id= db.Column(db.Integer,autoincrement=True,primary_key=True)
    g_name = db.Column(db.String(20),unique=True)
    g_create_time = db.Column(db.DateTime,default=datetime.now)
    #设置与班级 一对多的关联关系
    students = db.relationship('Student',backref='grade')
    #自定义表名
    __tablename__ = 'grade'
    #初始化字段,方便以后视图使用
    def __init__(self,name):
        self.g_name = name
    #定义保存数据的方法
    def save(self):
        db.session.add(self)
        db.session.commit()

class Student(db.Model):
    '''学生模型'''
    s_id= db.Column(db.Integer,autoincrement=True,primary_key=True)
    s_name = db.Column(db.String(16),unique=True)
    s_sex = db.Column(db.Integer)
    #设置与班级 一对多的关联关系
    grade_id= db.Column(db.Integer,db.ForeignKey('grade.g_id'),nullable=True)
    __tablename__ = 'student'
    def __init__(self,s_name,s_sex,grade_id):
        self.s_name = s_name
        self.s_sex = s_sex
        self.grade_id = grade_id
    def save(self):
        db.session.add(self)
        db.session.commit()

class User(db.Model):
    '''用户模型'''
    u_id= db.Column(db.Integer,autoincrement=True,primary_key=True)
    username = db.Column(db.String(16),unique=True)
    password = db.Column(db.String(250))
    u_create_time = db.Column(db.DateTime,default=datetime.now)
    #用户和角色的一对多的关联关联关系
    role_id = db.Column(db.Integer,db.ForeignKey('role.r_id'))
    __tablename__ = 'user'
    def __init__(self,username,password):
        self.username = username
        self.password = password

    def save(self):
        db.session.add(self)
        db.session.commit()

#角色和权限的(多对多)关联表
#r_p为关联表的表名
r_p= db.Table('r_p',db.Column('role_id',db.Integer,db.ForeignKey('role.r_id'),primary_key=True),
              db.Column('permission_id',db.Integer,db.ForeignKey('permission.p_id'),primary_key=True))

class Role(db.Model):
    r_id = db.Column(db.Integer,autoincrement=True,primary_key=True)
    r_name = db.Column(db.String(10))
    #用户和角色的一对多的关联关系
    users = db.relationship('User',backref='role')
    __tablename__ = 'role'
    def __init__(self,r_name):
        self.r_name = r_name
    def save(self):
        db.session.add(self)
        db.session.commit()

class Permission(db.Model):
    p_id = db.Column(db.Integer,autoincrement=True,primary_key=True)
    p_name = db.Column(db.String(16),unique=True)
    p_er = db.Column(db.String(16),unique=True)
    #角色和权限的多对多的关系
    roles = db.relationship('Role',secondary=r_p,backref=db.backref('permission',lazy=True))
    __tablename__ = 'permission'
    def __init__(self,p_name,p_er):
        self.p_name = p_name
        self.p_er = p_er
    def save(self):
        db.session.add(self)
        db.session.commit()


