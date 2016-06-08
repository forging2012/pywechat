#coding: utf-8
import urllib2
import urllib
import json
import sys 
import string
import requests
import re
from random import randint
from functools import wraps
import ConfigParser





###config file read###
Conf= ConfigParser.ConfigParser()
Conf.readfp(open("config.ini"))
YoudaoKey = Conf.get("datasource","YoudaoKey")
YoudaoKeyFrom = Conf.get("datasource","YoudaoKeyFrom")
BaiduAPI = Conf.get("datasource","BaiduAPI")

print BaiduAPI
print type(YoudaoKeyFrom)

reload(sys) 
sys.setdefaultencoding('utf8')

___metatype__ = type


""" handle the user content """


Menu = """
help(帮助菜单):help，？，帮助
fy(翻译):fy 内容,如:翻译 你好
tq(天气):tq 地名，如:天气 上海
xh(笑话):笑话
kd(快递):快递 快递公司 快递单号，如:kd 韵达 快递单号
bk(百度百科):百科 内容，如:百科 中国
bd(百度):百度 内容，如:百度 中国
"""

Menu2 = """
help(帮助菜单):help，？，帮助
fy(翻译):fy  “内容”
ss(搜索):ss “书籍” 
jqr(机器人)！！！可能
tq(天气):天气  地名
xh(笑话):xh
gp(股票，预测):gp  10020(股票代码)
gq(歌曲): gq 歌曲名
bt(bt搜索): bt 名字
dy(电影搜索): dy 电影名(正版视频网站或非正版，隐藏功能)
rb(每周日报):日报  获取每天日报
kd(快递):kd 快递公司 内容，如:kd 韵达 快递单号
bk(百度百科):bk 内容，如:bk 中国
bd(百度):bk 内容，如:bd 中国
----现在暂时只支持fy,tq,kd,bk----
"""



KDCode = {"申通":"shentong","EMS":"ems","顺丰":"shunfeng",
	"圆通":"yuantong","中通":"zhongtong","韵达":"yunda",
	"天天":"tiantian","汇通":"huitongkuaidi","全峰":"quanfengkuaidi",
	"德邦":"debangwuliu","宅急送":"zhaijisong"}

MenuCode = {"翻译":"fy","天气":"tq","笑话":"xh",
            "快递":"kd","百科":"bk","百度":"bd"}

def RequestTextGet(PostXml):



    """Get the content of user query"""

    PostXML = ET.fromstring(PostXML)
    ToUser = PostXML.find("ToUserName").text
    FromUser = PostXML.find("FromUserName").text
    UserContent  = PostXML.find("Content").text
    UserContent = UserContent.split()

    "错误处理"

    return ToUser,FromUser,UserContent

def ArgsConfig(Args=1): 
    def deco(func):
        @wraps(func)
        def wrap(self,*args,**kwargs):
            args = args[:Args]
            ret = func(self,*args,**kwargs)
            return ret
        return wrap
    return deco

class Handler():
    """
    handle the the request of user
    """
    #def __init__(self,Action):
    #    self.Action = Action

    #def callback(self,Action,*args):
    #    Func = getattr(self,Action,None)
    #    if callable(func):return Func(*args)
    def __init__(self,Ret=None):
        self.Ret = Ret
    


    def Get(self,Action,*args):
        if Action in MenuCode: Action = MenuCode[Action]
        Func = getattr(self,Action,None)
        if callable(Func):self.Ret = Func(*args)

    def help(slef):
        return Menu
    
    @ArgsConfig(1)
    def test(self,*args,**kwargs):
        print args,kwargs


class TextHandler(Handler):
    @ArgsConfig(1)
    def fy(self,Word,KeyFrom=YoudaoKeyFrom,Key=YoudaoKey):
        Payload = {"key":Key,"keyfrom":KeyFrom,"q":Word}
        ReqURL = u'http://fanyi.youdao.com/openapi.do?type=data&doctype=json&version=1.1'
        YoudaoRet = requests.get(ReqURL,params=Payload)
        RetJSON = YoudaoRet.json()

        
        if RetJSON["errorCode"] == 0:
            Trans = RetJSON["translation"]
            Trans = "\n".join(Trans)
            
            if "basic" in RetJSON.keys():
                OtherTrans = RetJSON["basic"]["explains"]
                OtherTrans = "\n".join(OtherTrans)
                OtherTrans = u"\n\n其他释义有:\n" + OtherTrans

            else:
                OtherTrans = ""
            
            Ret = u"'%s' 的查询结果为:\n" + Trans + OtherTrans

            return unicode(Ret).encode("utf8")
        else:
            return "查询内容有问题"

    @ArgsConfig(1)
    def bd(self,Word):
        Word = urllib2.quote(Word.encode("utf8"))
        ReqURL = "http://www.baidu.com/s?wd=" + Word

        return "点击下面链接\n" + ReqURL


    @ArgsConfig(1)
    def tq(self,City,ApiKey=BaiduAPI):
        ReqURL = 'http://apis.baidu.com/heweather/weather/free'
        Payload = {"city":City}

        header = {"apikey":ApiKey}
        
        TQRet = requests.post(ReqURL,data=Payload,headers=header)
        RetJSON = TQRet.json()

        k = "HeWeather data service 3.0"
        
        if  k in RetJSON.keys() and RetJSON[k][0]["status"] == "ok":
            RetCond =  RetJSON[k][0]["now"]["cond"]["txt"]
            RetBrf = RetJSON[k][0]["suggestion"]["comf"]["brf"] 
            RetBrfTXT = RetJSON[k][0]["suggestion"]["comf"]["txt"]

            Ret = "\n".join([RetCond,RetBrf,RetBrfTXT])
                
        else:
            Ret = "查询失败"

        return Ret


    @ArgsConfig(2)
    def kd(self,CpyName,PostID):
        CpyName = KDCode[CpyName]
        print CpyName,PostID
        Payload = {"type":CpyName,"postid":PostID}
        #url = "http://www.kuaidi100.com/query?type=%s&postid=%s" % (cpy_name,nums)
        ReqURL = "http://www.kuaidi100.com/query"

        KDRet = requests.get(ReqURL,params=Payload)
        print KDRet.url
        RetJSON = KDRet.json()


        if RetJSON["message"] == "ok":
            Data = RetJSON["data"]
            Ret = "\n".join([x for i in RetJSON["data"] for x in i.values()])
        else:
            #Ret = Ret["message"]
            Ret = "查询失败"

        return Ret


    @ArgsConfig(1)
    def bk(self,Word):
        Payload = {"bk_key":Word.encode("utf8")}
        ReqURL= "http://baike.baidu.com/api/openapi/BaikeLemmaCardApi?format=json&appid=379020"
        BKRet = requests.get(ReqURL,params=Payload)
        print BKRet.url
        RetJSON = BKRet.json()

        if len(RetJSON) != 0:
            Desc = RetJSON["desc"]
            # print desc
            Abstract = RetJSON["abstract"]
            # print abstract
            Ret = Desc + "\n" + Abstract
        else:        
            Ret = "该词条暂未收录"
            
        return Ret

    @ArgsConfig(0)
    def xh(self):
        XHResp = requests.get("http://www.qiushibaike.com/text/")
        XHRet = re.findall(r"""<div class="content">(\s*.*\s*)</div>""",XHResp.content)
        num = randint(0,len(XHRet))

        Ret = XHRet[num]

        return Ret
