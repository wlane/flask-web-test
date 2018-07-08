#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask import Flask,render_template,request,redirect,url_for
from werkzeug.utils import secure_filename
import os
import base_func

app = Flask(__name__)

@app.route('/upload', methods=['POST', 'GET'])
def upload():
    if request.method == 'POST':
        f = request.files['file']
        #basepath = os.path.dirname(__file__)  # 当前文件所在路径
        upload_path = os.path.join('/var/lib/tomcat7/webapps',secure_filename(f.filename))  #注意：没有的文件夹一定要先创建，不然会提示没有该路径
        f.save(upload_path)
        base_func.base('service tomcat7 restart')
        #return redirect(url_for('upload'))
    return render_template('upload.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)
