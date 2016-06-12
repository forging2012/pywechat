#coding:utf-8
from flask import Flask,render_template,request,make_response
import time
import hashlib
import xml.etree.ElementTree as ET
from handler import RequestTextGet,TextHandler
from resp import TextResp


app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World"

@app.route("/test")
def test():
    return render_template("test.html")


@app.route("/wechat",methods = ["GET","POST"])
def wechat_auth():
    if request.method == 'GET':  
        if len(request.args) > 3:
            token = 'youerning' 
            query = request.args  
            signature = query['signature'] 
            timestamp = query['timestamp'] 
            nonce = query['nonce']  
            echostr = query['echostr'] 
            s = [timestamp, nonce, token]  
            s.sort()  
            s = ''.join(s)
	    sha1str = hashlib.sha1(s).hexdigest()
	    if sha1str == signature:
	        return make_response(echostr)
            else:
	        return make_response("认证失败")
        else:
            return "认证失败"
    else:
        PostXML = request.stream.read()
        ToUser,FromUser,UserContent = RequestTextGet
        Handle = TextHandler()

        Handle.Get(UserContent[0],*UserContent[1:])
        if Handle.Ret:
            RespXML = make_response(TextResp(ToUser,FromUser,Handle.Ret))
        else:
            Handle.help()
            RespXML = make_response(TextResp(ToUser,FromUser,Handle.Ret))
            RespXML.content_type = "application/xml"
        
        return RespXML
@app.route("/gzh",methods = ["GET"])
def gzh():
    pass

