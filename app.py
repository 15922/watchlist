# -*- coding: utf-8 -*-
"""
Created on Fri Oct 26 16:16:09 2018

@author: xutao
"""
from flask import Flask
from flask import url_for

app = Flask(__name__)

@app.route('/')
@app.route('/index')
@app.route('/home')
def hello():
    return '<h1>Hello Totoro!</h1><img src="http://helloflask.com/totoro.gif">'

@app.route('/user/<name>')
def user_page(name):
    return 'User: %s' % name

@app.route('/test')
def test_url_for():
    # ������һЩ����ʾ����
    print(url_for('hello'))  # �����/
    # ע����������������������ɰ��� URL ������ URL ��
    print(url_for('user_page', name='greyli'))  # �����/user/greyli
    print(url_for('user_page', name='peter'))  # �����/user/peter
    print(url_for('test_url_for'))  # �����/test
    # ����������ô����˶���Ĺؼ��ֲ��������ǻᱻ��Ϊ��ѯ�ַ������ӵ� URL ���档
    print(url_for('test_url_for', num=2))  # �����/test?num=2
    return 'Test page'