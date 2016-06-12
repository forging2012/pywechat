#coding: utf-8
import time

"""for Get and Respsonse the wechat's Server posted XML"""

def TextResp(ToUser,FromUser,RespContent):
    """ format the response text content and response"""
    RespFomat = "<xml><ToUserName><![CDATA[%s]]></ToUserName><FromUserName><![CDATA[%s]]></FromUserName><CreateTime>%s</CreateTime><MsgType><![CDATA[text]]></MsgType><Content><![CDATA[%s]]></Content><FuncFlag>0</FuncFlag></xml>"
	
    "处理文本查询"
    RespXML = RespFomat % (FromUser,ToUser,int(time.time()),RespContent)

    return RespXML

