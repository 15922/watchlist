# -*- coding: utf-8 -*-
"""
Created on Fri Oct 26 16:16:09 2018

@author: xutao
"""


#加载数据库就要带着这个了
import os
import sys


#自动创建数据库加载的
import click


from flask import Flask, render_template
from flask import url_for
from flask_sqlalchemy import SQLAlchemy  # 导入数据库扩展类


#对不同系统进行判断
WIN = sys.platform.startswith('win')
if WIN:  # 如果是 Windows 系统，使用三个斜线
    prefix = 'sqlite:///'
else:  # 否则使用四个斜线
    prefix = 'sqlite:////'


app = Flask(__name__)


#Flask 提供了一个统一的接口来写入和获取这些配置变量：Flask.config 字典
#配置变量的名称必须使用大写，写入配置的语句一般会放到扩展类实例化语句之前
#app.root_path 返回程序实例所在模块的路径
app.config['SQLALCHEMY_DATABASE_URI'] = prefix + os.path.join(app.root_path, 'data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # 关闭对模型修改的监控


# 在扩展类实例化前加载配置
db = SQLAlchemy(app)  # 初始化扩展，传入程序实例 app


#自定义命令来自动执行创建数据库表操作
@app.cli.command()  # 注册为命令
@click.option('--drop', is_flag=True, help='Create after drop.')  # 设置选项
def initdb(drop):
    """Initialize the database."""
    if drop:  # 判断是否输入了选项
        db.drop_all()
    db.create_all()
    click.echo('Initialized database.')  # 输出提示信息


#模型类要声明继承 db.Model
class User(db.Model):  # 表名将会是 user（自动生成，小写处理）
	#每一个类属性（字段）要实例化 db.Column，传入的参数为字段的类型
	#在 db.Column() 中添加额外的选项（参数）可以对字段进行设置，比如，primary_key 设置当前字段是否为主键
    id = db.Column(db.Integer, primary_key=True)  # 主键
    name = db.Column(db.String(20))  # 名字


class Movie(db.Model):  # 表名将会是 movie
    id = db.Column(db.Integer, primary_key=True)  # 主键
    title = db.Column(db.String(60))  # 电影标题
    year = db.Column(db.String(4))  # 电影年份


#自定义命令函数把虚拟数据添加到数据库里
@app.cli.command()
def forge():
    """Generate fake data."""
    db.create_all()

    # 全局的两个变量移动到这个函数内
    name = 'Grey Li'
    movies = [
        {'title': 'My Neighbor Totoro', 'year': '1988'},
        {'title': 'Dead Poets Society', 'year': '1989'},
        {'title': 'A Perfect World', 'year': '1993'},
        {'title': 'Leon', 'year': '1994'},
        {'title': 'Mahjong', 'year': '1996'},
        {'title': 'Swallowtail Butterfly', 'year': '1996'},
        {'title': 'King of Comedy', 'year': '1999'},
        {'title': 'Devils on the Doorstep', 'year': '1999'},
        {'title': 'WALL-E', 'year': '2008'},
        {'title': 'The Pork of Music', 'year': '2012'},
    ]

    user = User(name=name)
    db.session.add(user)
    for m in movies:
        movie = Movie(title=m['title'], year=m['year'])
        db.session.add(movie)

    db.session.commit()
    click.echo('Done.')

@app.route('/')
def index():
    user = User.query.first()  # 读取用户记录
    movies = Movie.query.all()  # 读取所有电影记录
    return render_template('index.html', user=user, movies=movies)


@app.route('/index')
@app.route('/home')
def hello():
    return '<h1>Hello Totoro!</h1><img src="http://helloflask.com/totoro.gif">'

@app.route('/user/<name>')
def user_page(name):
    return 'User: %s' % name

@app.route('/test')
def test_url_for():
    print(url_for('hello'))
    print(url_for('user_page', name='greyli'))  
    print(url_for('user_page', name='peter'))
    print(url_for('test_url_for')) 
    print(url_for('test_url_for', num=2))  
    return 'Test page'