import time

"""for Get and Respsonse the wechat's Server posted XML"""

def TextGet(PostXml):
    """Get the content of user query"""

    PostXML = ET.fromstring(PostXML)
    ToUser = PostXML.find("ToUserName").text
    FromUser = PostXML.find("FromUserName").text
    UserContent  = PostXML.find("Content").text
    
    "错误处理"

    return ToUser,FromUser,UserContent

def TextResp(ToUser,FromUser,UserContent):
    """ format the response text content and response"""
    RespFomat = "<xml><ToUserName><![CDATA[%s]]></ToUserName><FromUserName><![CDATA[%s]]></FromUserName><CreateTime>%s</CreateTime><MsgType><![CDATA[text]]></MsgType><Content><![CDATA[%s]]></Content><FuncFlag>0</FuncFlag></xml>"
	
    "处理文本查询"
    RespXML = RespFomat % (FromUser,ToUser,int(time.time()),RespContent

    return RespXML
 
