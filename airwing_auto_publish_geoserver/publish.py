#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pycurl
import StringIO
import urllib
import re

c = pycurl.Curl()
b = pycurl.Curl()
a = pycurl.Curl()
# 配置geoserver的账号密码
GLOBAL_USERPWD = "admin:geoserver"
# 格式化http状态码的输出方式
def httpPrint(word):
        print '\033[1;32;40m'
        print word
        print '\033[0m'
# 格式化错误提示的输出方式
def errorPrint(word):
        print '\033[1;31;40m'
        print word
        print '\033[0m'
# 添加一个新的workspace，以"user_"+"用户名"的格式给每一个用户新建一个新的workspace
def addnewWorkspace(curl, url, username):
        buf = StringIO.StringIO()
        curl.setopt(pycurl.POST, 1)
        curl.setopt(pycurl.URL, url)
        curl.setopt(pycurl.USERPWD, GLOBAL_USERPWD)
        curl.setopt(pycurl.HTTPHEADER, ["Content-type: application/xml"])
        xmlStr = "<workspace><name>" + username + "</name></workspace>"
        curl.setopt(pycurl.POSTFIELDS, xmlStr)
        curl.perform()
        httpCode = curl.getinfo(curl.HTTP_CODE)
        buf.close()
        if httpCode == 201:
                httpPrint('HTTP_CODE:201,Add new workspace success.')
                httpPrint('*'*50)
        elif str(httpCode)[0:2] == 30:
                errorPrint('HTTP_CODE:30X,Add new workspace success.Redirect; possibly a typo in the URL')
                errorPrint('*'*50)
        elif httpCode == 400:
                errorPrint('HTTP_CODE:400,Add new workspace success.bad request or invalid hostname')
                errorPrint('*'*50)
        elif httpCode == 401:
                errorPrint('HTTP_CODE:401,Add new workspace success.Invalid username or password')
                errorPrint('*'*50)
        elif httpCode == 405:
                errorPrint('HTTP_CODE:405,Add new workspace success.Method not Allowed: check request syntax')
                errorPrint('*'*50)
        elif httpCode == 500:
                errorPrint('HTTP_CODE:500,Add new workspace success.Geoserver is unable to process the request, e.g. the workspace already exists, the xml is malformed, ...')
                errorPrint('*'*50)
        elif httpCode == 0:
                errorPrint('HTTP_CODE:0,Add new workspace success.Couldn’t resolve host; possibly a typo in host name')
                errorPrint('*'*50)
        else:
                print '\033[1;31;40m'
                print 'HTTP_CODE:', httpCode, 'Add new workspace failed.Unknown problem'
                print '\n'
                print '*'*50
                print '\033[0m'
# 发布地图服务，地图数据应在本地硬盘目录下
def postData(curl, url, data):
        buf = StringIO.StringIO()
        curl.setopt(pycurl.WRITEFUNCTION, buf.write)
        curl.setopt(pycurl.POSTFIELDS,  data)
        curl.setopt(pycurl.URL, url)
        curl.setopt(pycurl.CUSTOMREQUEST, "PUT")
        curl.setopt(pycurl.USERPWD, GLOBAL_USERPWD)
        curl.perform()
        httpCode = curl.getinfo(curl.HTTP_CODE)
        buf.close()
        if httpCode == 201:
                httpPrint('HTTP_CODE:201,publish success')
                httpPrint('*'*50)
        elif str(httpCode)[0:2] == 30:
                errorPrint('HTTP_CODE:30X,publish failed.Redirect; possibly a typo in the URL')
                errorPrint('*'*50)
        elif httpCode == 400:
                errorPrint('HTTP_CODE:400,publish failed.bad request or invalid hostname')
                errorPrint('*'*50)
        elif httpCode == 401:
                errorPrint('HTTP_CODE:401,publish failed.Invalid username or password')
                errorPrint('*'*50)
        elif httpCode == 405:
                errorPrint('HTTP_CODE:405,publish failed.Method not Allowed: check request syntax')
                errorPrint('*'*50)
        elif httpCode == 500:
                errorPrint('HTTP_CODE:500,publish failed.Geoserver is unable to process the request, e.g. the workspace already exists, the xml is malformed, ...')
                errorPrint('*'*50)
        elif httpCode == 0:
                errorPrint('HTTP_CODE:0,publish failed.Couldn’t resolve host; possibly a typo in host name')
                errorPrint('*'*50)
        else:
                print '\033[1;31;40m'
                print 'HTTP_CODE:', httpCode, 'publish failed.Unknown problem'
                print '\n'
                print '*'*50
                print '\033[0m'
# 获得该发布地图的地理坐标信息，即左下角和右上角经纬度坐标
def getGeoinfo(curl, url, data):
        newUrl = url.split('/')
        newData = data.split('/')
        newdataName = newData[-1].split('.')[0]
        #y为请求地理信息的资源地址
        y = ""
        i = 0
        for x in newUrl:
                if i > len(newUrl)-2:
                        break
                i = i + 1
                y = y + x + '/'
        y = y + 'coverages/' + newdataName + '.html'
        buf = StringIO.StringIO()
        curl.setopt(pycurl.WRITEFUNCTION, buf.write)
        curl.setopt(pycurl.URL, y)
        c.setopt(pycurl.HTTPHEADER, ['Content-Type:application/json'])
        curl.setopt(pycurl.USERPWD, GLOBAL_USERPWD)
        curl.perform()
        thePage = buf.getvalue()
        # 正则匹配<li>标签
        reObj1 = re.compile('<li>[\s\S]*?</li>')
        if thePage[0:2] != '<!':
                errorPrint("Get geoinfo failed." + thePage)
                return
        # 下面为处理匹配到的结果字符串，提取出经纬度坐标信息，并存放在一个列表里
        geoInfo = reObj1.findall(thePage)[-1].split('[')[-1].split(']')[0].split(',')
        longitute = geoInfo[0].split(':')
        latitude = geoInfo[-1].split(':')
        latitude[0] = latitude[0].strip()
        latitude[1] = latitude[1].strip()
        longitute[0] = longitute[0].strip()
        longitute[1] = longitute[1].strip()
        newgeoInfo = [longitute[1], latitude[1], longitute[0], latitude[1]]
        return newgeoInfo
        buf.close()

# url为发布地图服务的请求资源地址（http协议），data为本地地图数据的存放路径（file协议）
url = ''
data = ''
workspaceUrl = "http://localhost:8080/geoserver/rest/workspaces/"
while 1:
        inputUser = raw_input("Please enter username:")
        if inputUser:
                user = 'user_' + inputUser
                break
        else:
                errorPrint("invalid username")
while 1:
        taskidInput = raw_input('Please enter taskID:')
        if taskidInput:
                taskID = taskidInput
                break
        else:
                errorPrint("invalid taskID")

url = "http://localhost:8080/geoserver/rest/workspaces/" + user + "/coveragestores/" + taskID + "/external.geotiff"
data = 'file:/mnt/geodata/' + taskID + '.tif'

if url:
        if data:
                print '\033[1;31;40m'
                addnewWorkspace(a, workspaceUrl, user)
                print '\033[0m'
                postData(c, url, data)
                newgeoInfo = getGeoinfo(b, url, data)
                if newgeoInfo:
                        print '\033[1;31;47m'
                        print 'Get geoinfo success,the geoinfo of this map is:'
                        print newgeoInfo
                        print '\033[0m'
        else:
                errorPrint('data is undefined')
else:
        errorPrint('url is undefined')