#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask import Flask,render_template,request,redirect,url_for
from werkzeug.utils import secure_filename
import os,time
import base_func

app = Flask(__name__)

@app.route('/upload', methods=['POST', 'GET'])
def upload():
    if request.method == 'POST':
        base_func.base('service tomcat7 stop')
        base_func.base('rm -rf /var/lib/tomcat7/webapps/mianyang.war')
        base_func.base('rm -rf /var/lib/tomcat7/webapps/mianyang')
        f = request.files['file']
        #basepath = os.path.dirname(__file__)  # 当前文件所在路径
        upload_path = os.path.join('/var/lib/tomcat7/webapps',secure_filename(f.filename))
        f.save(upload_path)
        base_func.base('service tomcat7 restart')
        time.sleep(5)
        base_func.backup('/var/lib/tomcat7/webapps/mianyang','/home/anyuan/Backtomcat')
        base_func.backup('/var/lib/tomcat7/webapps/mianyang.war','/home/anyuan/Backtomcat')
        return redirect(url_for('upload'))
    return render_template('upload.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)
