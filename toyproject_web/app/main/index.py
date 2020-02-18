# file name : index.py
# pwd : /project_name/app/main/index.py
 
from flask import Blueprint, request, render_template, flash, redirect, url_for
from flask import current_app as app
# 추가할 모듈이 있다면 추가
 
main= Blueprint('main', __name__, url_prefix='/')

@main.route('/main', methods=['GET'])
def index():
      # /main/index.html은 사실 /project_name/app/templates/main/index.html을 가리킵니다.
      return render_template('/main/login.html')

@main.route('/result', methods=['GET','POST'])
def result():
      if request.method == 'POST':
            result = request.form
            return render_template("/main/result.html",result = result)

@main.route('/home', methods=['GET'])
def home():
      return render_template("/home/home.html")

@main.route('/container', methods=['GET'])
def container():
      return render_template("/home/container.html")

@main.route('/detail1', methods=['GET'])
def detail1():
      return render_template("/home/detail1.html")

@main.route('/setting', methods=['GET'])
def setting():
      return render_template("/home/Setting.html")