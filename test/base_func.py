#!/usr/bin/python
# -*- coding: utf-8 -*-

import os,sys
import subprocess
import time

def color_red(string):    #显示红色字体
    return"%s[31;10m%s%s[0m"%(chr(27),string,chr(27))

def color_yellow(string):    #显示黄色字体
    return"%s[33;10m%s%s[0m"%(chr(27),string,chr(27))

def log(logcontent):    #安装过程写入日志，日志文件生成在本目录
    logfile = open('installlog.txt','a')
    logfile.write('%s' % logcontent)
    logfile.write('\n')
    logfile.close()

def check_user():    #检测是否有用户anyuan以及是否使用root用户执行该脚本
    command = 'grep -iw anyuan /etc/passwd'
    execute  = subprocess.Popen(command,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    result = execute.communicate()
    if execute.poll() == 0:
        pass
    else:
        print "you should create user anyuan, command: adduser anyuan"
        sys.exit(555)
    if os.geteuid() != 0:
        print "This program must be run as root. Aborting."
        sys.exit(404)

def input_passwd(passwdname):  #设置相关密码
    if passwdname == 'mysqlroot':
        mysqlrootpasswd = raw_input('please input mysql root\'s password: ')
        return mysqlrootpasswd
    elif passwdname == 'mysqlnormal':
        mysqlnormalpasswd = raw_input('please input mysql normaluser(anyuan)\'s password: ')
        return mysqlnormalpasswd
    elif passwdname == 'zsh':
        zshpasswd = raw_input('please input systemuser(anyuan)\'s password: ')
        return zshpasswd 
    elif passwdname == 'mongo':
        mongopasswd = raw_input('please input mongodb user(anyuan)\'s password: ')
        return mongopasswd

def backup(source, dest):
    if not os.path.exists(dest):
        print dest+" does not exist,create it"
        os.mkdir(dest)
    if not os.path.exists(source):
        print source+" does not exist."
        sys.exit() 
    filedate = time.strftime('%Y%m%d')+"_"+time.strftime('%H%M%S')
    filename = os.path.split(source)[1]+"_"+filedate+".tar.gz"
    backup_command = "tar zcf %s %s" % (dest+'/'+filename,source)
    if os.system(backup_command) == 0:
        print "backup "+source+" successful!"
    else:
        print "backup "+source+" failed.........."

def replace(filepath, oldstr, newstr):  #替换文件中的字符 
  try:
    print newstr+' replace '+oldstr+' in '+filepath
    f = open(filepath,'r+')  
    all_lines = f.readlines()  
    f.seek(0)  
    f.truncate()  
    for line in all_lines:  
      line = line.replace(oldstr, newstr)  
      f.write(line)  
    f.close()
    print color_red(newstr+' replace '+oldstr+' in '+filepath+'    '+'ok')
    log(newstr+' replace '+oldstr+' in '+filepath+'    '+'ok')
    time.sleep(3)
  except Exception,e:  
    log(newstr+' replace '+oldstr+' in '+filepath+'    '+'error '+e)
    print e

def add_filecontent(basefile,content,pos):    
    #将content文件中的内容增加到basefile中的pos处，pos可以是数字也可以是字符，数字代表插入行数所在的下面一行，字符代表插入所在的那一行上面的一行
  try:
    print content+' addto '+basefile
    base_filename = open(basefile, "r")
    file_content = open(content,"r")
    if pos.isdigit():
        add_content = file_content.read()
        file_content.close()
        lines=[]
        for line in base_filename:
            lines.append(line)
        base_filename.close()
        lines.insert(int(pos),add_content)
        result=''.join(lines)
        f = open(basefile, "w")
        f.write(result)
        f.close()
        print color_red(content+' addto '+basefile+'    '+'ok')
        log(content+' addto '+basefile+'    '+'ok')
        time.sleep(3)
    else:
        content = base_filename.read()
        add_content = file_content.read()
        base_filename.close()
        file_content.close()
        pos = content.find(pos)
        print pos
        if pos != -1:
            content = content[:pos] + add_content + content[pos:]
            f = open(basefile, "w")
            f.write(content)
            f.close()
        print color_red(content+' addto '+basefile+'    '+'ok')
        log(content+' addto '+basefile+'    '+'ok')
        time.sleep(3)
  except Exception,e:
    log(content+' addto '+basefile+'    '+'error '+e)
    print e

#def env(filename):
#    f = open(filename)
#    for command in f.readlines():
#        print color('****************')
#        print command
#        execute  = subprocess.Popen(command,shell=True,stderr=subprocess.PIPE)
#        result = execute.communicate()
#        output = result[0]
#        error = result[1]
#        if output is None and error == '':
#            print color(command.strip('\n')+'   '+'ok')
#            continue
#        else:
#            print error
#            break

#def main():
#    file_path = os.path.abspath('.')
#    env_file = file_path+'/'+'envcreate.txt'
#    env(env_file)


#def base_nojudge(command):
#    subprocess.call(command,shell=True)
#    print color_red('starting'+command)

def base(command):   #执行shell命令
    print color_red('****************')
    print command
    execute  = subprocess.Popen(command,shell=True,stderr=subprocess.PIPE)
    result = execute.communicate()
    output = result[0]
    error = result[1]
    if execute.poll() == 0:
        print color_red(command.strip('\n')+'   '+'ok')
        log(command.strip('\n')+'    '+'ok')
        time.sleep(3)
    else:
        if 'oh-my-zsh' in command:
            print color_red(command.strip('\n')+'   '+'ok')
            log(command.strip('\n')+'    '+'ok')    
        else:
            print error
            print color_yellow('error: please execute again after checking.')
            log(command+'    '+'error'+'\n'+error)
            sys.exit(250)

def base_passwd(passwd,command):   #执行需要输入密码的shell命令
    print color_red('****************')
    print command
    outputpasswd = subprocess.Popen(['echo',passwd],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    execute = subprocess.Popen(command,shell=True,stdin=outputpasswd.stdout,stderr=subprocess.PIPE)
    result = execute.communicate()
    output = result[0]
    error = result[1]
    if execute.poll() == 0:
        print color_red(command.strip('\n')+'   '+'ok')
        log(command.strip('\n')+'    '+'ok')
        time.sleep(3)
    else:
        print error
        print color_yellow('error: please execute again after checking.')
        log(command+'    '+'error'+'\n'+error)
        sys.exit(250)

