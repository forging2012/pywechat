#coding: utf-8
import urllib2
import urllib
import json
import sys 
import string
import requests
import re

reload(sys) 
sys.setdefaultencoding('utf8')

___metatype__ = type


""" handle the user content """


Menu = """
help(帮助菜单):help，？，帮助
fy(翻译):fy 内容,如:fy 你好
tq(天气):tq 地名，如:tq 上海
xh(笑话):xh
gq(歌曲): gq 歌曲名
rb(每周日报):日报  获取每天日报
kd(快递):kd 快递公司 内容，如:kd 韵达 快递单号
bk(百度百科):bk 内容，如:bk 中国
bd(百度):bk 内容，如:bd 中国
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

def RequestTextGet(PostXml):



    """Get the content of user query"""

    PostXML = ET.fromstring(PostXML)
    ToUser = PostXML.find("ToUserName").text
    FromUser = PostXML.find("FromUserName").text
    UserContent  = PostXML.find("Content").text
    UserContent = UserContent.split()

    "错误处理"

    return ToUser,FromUser,UserContent

def ConfigGet(name):
    pass


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
        Func = getattr(self,Action,None)
        if callable(Func):self.Ret = Func(*args)
    def help(slef):
        return Menu


class TextHandler(Handler):
    def fy(self,Word,KeyFrom="youerning",Key="16283712"):
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

    def bd(self,Word):
        Word = urllib2.quote(Word.encode("utf8"))
        ReqURL = "http://www.baidu.com/s?wd=" + Word

        return ReqURL


    def tq(self,City,ApiKey="47885eaa7687f444901013c25f4b7745"):
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


    def bk(self,Word):
        Payload = {"bk_key":Word}
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
   def xh(self):
       XHResp = requests.get("http://www.qiushibaike.com/text/")
       XHRet = re.findall(r"""<div class="content">(\s*.*\s*)</div>""",XHResp)

