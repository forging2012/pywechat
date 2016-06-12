#coding: utf-8
import urllib2
import urllib
import json
import sys 
import string
import requests
import re
import xml.etree.ElementTree as ET
from random import randint
from functools import wraps
import ConfigParser


reload(sys) 
sys.setdefaultencoding('utf8')

___metatype__ = type


""" handle the user content """


#config file read###
Conf= ConfigParser.ConfigParser()
Conf.readfp(open("apikey.ini"))
YoudaoKey = Conf.get("datasource","YoudaoKey")
YoudaoKeyFrom = Conf.get("datasource","YoudaoKeyFrom")
BaiduAPI = Conf.get("datasource","BaiduAPI")


Menu = """
帮助菜单:输入任意字符

翻译:中英文翻译
发送信息如,翻译 你好

天气:查询天气
发送消息如,天气 上海

笑话:返回笑话
发送消息如,笑话

快递:查询快递
发送消息如,快递 韵达 快递单号

百度百科:词条查询
发送消息如:百科 中国

百度搜索:百度搜索
发送消息如:百度 中国
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

KDCode = {u"申通":"shentong","EMS":"ems",u"顺丰":"shunfeng",
	u"圆通":"yuantong",u"中通":"zhongtong",u"韵达":"yunda",
	u"天天":"tiantian",u"汇通":"huitongkuaidi",u"全峰":"quanfengkuaidi",
	u"德邦":"debangwuliu",u"宅急送":"zhaijisong"}

MenuCode = {u"翻译":u"fy",u"天气":"tq",u"笑话":"xh",
            u"快递":u"kd",u"百科":"bk",u"百度":"bd"}


def RequestTextGet(PostXML):

    """Get the content of user query"""

    PostXML = ET.fromstring(PostXML)
    ToUser = PostXML.find("ToUserName").text
    FromUser = PostXML.find("FromUserName").text
    UserContent  = PostXML.find("Content").text
    UserContent = UserContent.split()


    return ToUser,FromUser,UserContent

def ArgsConfig(Args=1):
    """
	process the args number
    """
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

    def __init__(self,Ret=Menu):
        self.Ret = Ret

    def Get(self,Action,*args):
        if Action in MenuCode: Action = MenuCode[Action]
        Func = getattr(self,Action,None)
        if callable(Func):self.Ret = Func(*args)
    def help(slef):
        return Menu


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
            
            Ret = Word + u" 的查询结果为:\n" + Trans + OtherTrans

            return unicode(Ret).encode("utf8")
        else:
            return "查询内容有问题"

    @ArgsConfig(1)
    def bd(self,Word):
        Word = urllib2.quote(Word.encode("utf8"))
        ReqURL = "http://www.baidu.com/s?wd=" + Word

        return ReqURL


    @ArgsConfig(1)
    def tq(self,City,ApiKey=BaiduAPI):
        ReqURL = 'http://apis.baidu.com/heweather/weather/free'
        Payload = {"city":City}

        header = {"apikey":ApiKey}
        
        TQRet = requests.post(ReqURL,data=Payload,headers=header)
        RetJSON = TQRet.json()

        if RetJSON["HeWeather data service 3.0"][0]["status"] == "ok":
            RetCond =  RetJSON["HeWeather data service 3.0"][0]["now"]["cond"]["txt"]
            RetBrf = RetJSON["HeWeather data service 3.0"][0]["suggestion"]["comf"]["brf"] 
            RetBrfTXT = RetJSON["HeWeather data service 3.0"][0]["suggestion"]["comf"]["txt"]

            Ret = "\n".join([RetCond,RetBrf,RetBrfTXT])
                
        else:
            Ret = "查询失败"

        return Ret


    @ArgsConfig(2)
    def kd(self,CpyName,PostID):
        CpyName = KDCode[CpyName]
        Payload = {"type":CpyName,"postid":PostID}
        ReqURL = "http://www.kuaidi100.com/query"

        KDRet = requests.get(ReqURL,params=Payload)
        RetJSON = KDRet.json()


        if RetJSON["message"] == "ok":
            Data = RetJSON["data"]
            Ret = "\n".join([x for i in RetJSON["data"] for x in i.values()])
        else:
            Ret = "查询失败"

        return Ret


    @ArgsConfig(1)
    def bk2(self,Word):
        ReqURL= "http://baike.baidu.com/api/openapi/BaikeLemmaCardApi?format=json&appid=379020&bk_key=" + urllib2.quote(Word.encode("utf8"))
        BKRet = requests.get(ReqURL)
        RetJSON = BKRet.json()

        if len(RetJSON) != 0:
            Desc = RetJSON["desc"]
            Abstract = RetJSON["abstract"]
            Ret = Desc + "\n" + Abstract
        else:        
            Ret = "该词条暂未收录"
            
        return Ret

    @ArgsConfig(1)
    def bk(self,name):
        name = urllib2.quote(name.encode("utf8"))
        url = u"http://baike.baidu.com/api/openapi/BaikeLemmaCardApi?scope=103&format=json&appid=379020&bk_key=%s&bk_length=600" % name
        resp = urllib2.urlopen(url)
        content = resp.read()
        content = json.loads(content)

        if len(content) != 0:
           desc = content["desc"]
           abstract = content["abstract"]
           ret = desc + "\n" + abstract
        else:
           ret = "该词条暂未收录"

        return ret

    @ArgsConfig(0)
    def xh(self):
        randp = randint(1,6)
        Payload = {"page":randp}

        XHResp = requests.get("http://www.walxh.com/pc/hot/",params=Payload)
        XHRet = re.findall("""<p>(.*?)</p>""",XHResp.content)
        num = randint(0,len(XHRet))

        Ret = XHRet[num]

        return Ret
