#coding: utf-8
import urllib2
import urllib
import json
import sys 
import string
import requests

reload(sys) 
sys.setdefaultencoding('utf8')

___metatype__ = type


""" handle the user content """


Menu = """
help(帮助菜单):help，？，帮助
fy(翻译):fy  “内容”
ss(搜索):ss “书籍” 
jqr(机器人)！！！可能
tq(天气):天气  地名
xh(笑话):xh
gp(股票，最新价格):gp  10020(股票代码)
gq(歌曲): gq 歌曲名
bt(bt搜索): bt 名字
dy(电影搜索): dy 电影名(正版视频网站或非正版，隐藏功能)
rb(每周日报):日报  获取每天日报
kd(快递):kd 快递公司 内容，如:kd 韵达 快递单号
bk(百度百科):bk 内容，如:bk 中国
----现在暂时只支持fy,tq,kd,bk----
"""

kd_code = {"申通":"shentong","EMS":"ems","顺丰":"shunfeng",
	"圆通":"yuantong","中通":"zhongtong","韵达":"yunda",
	"天天":"tiantian","汇通":"huitongkuaidi","全峰":"quanfengkuaidi",
	"德邦":"debangwuliu","宅急送":"zhaijisong"}

def TextGet(PostXml):



    """Get the content of user query"""

    PostXML = ET.fromstring(PostXML)
    ToUser = PostXML.find("ToUserName").text
    FromUser = PostXML.find("FromUserName").text
    UserContent  = PostXML.find("Content").text

    "错误处理"

    return ToUser,FromUser,UserContent

class Handler():
    """
    handle the the request of user
    """
    #def __init__(self,Action):
    #    self.Action = Action

    #def callback(self,Action,*args):
    #    Func = getattr(self,Action,None)
    #    if callable(func):return Func(*args)

    def Get(self,Action):
        Func = getattr(self,Action,None)
        if callable(func):return Func(*args)

class TextHandler(Handler):
    def fy(KeyFrom,Key,Word):
        Qword = urllib2.quote(word.encode("utf8"))
        
        ReqURL = u'http://fanyi.youdao.com/openapi.do?keyfrom=%s&key=%s&type=data&doctype=json&version=1.1&q=%s'
        ReqURL = ReqURL % (KeyFrom,Key,Qword)
        
        YoudaoRet = requests.get(ReqURL)
        RetJSON = Ret.json()

        
        if RetJSON["errorCode"] == 0:
            Trans = RetJSON["translation"]
            Trans = "\n".join(Trans)
            
            if "basic" in ret_fy.keys():
                Explains = ret_fy["basic"]["explains"]
                Explains = "\n".join(other_trans)
                OtherTrans = u"\n\n其他释义有:\n" + other_trans

            else:
                OtherTrans = ""
            
            Ret = u"'%s' 的查询结果为:\n" + Trans + OtherTrans

            return unicode(Ret).encode("utf8")
        else:
            return "查询内容有问题"


    def baidu_search(keyword):
        p= {'wd': keyword}
        res=urllib2.urlopen("http://www.baidu.com/s?"+urllib.urlencode(p))
        html=res.read()
        return html


    def tq(city):
        city = city.strip()
        url = 'http://apis.baidu.com/heweather/weather/free?city=' + city
        req = urllib2.Request(url)

        req.add_header("apikey", "47885eaa7687f444901013c25f4b7745")

        resp = urllib2.urlopen(req)
        content = resp.read()
        if(content):
            ret = json.loads(content)
            # ret = ret["HeWeather data service 3.0"]
            ret =  ret["HeWeather data service 3.0"][0]["now"]["cond"]["txt"]
                
        else:
            ret = "查询失败"

        return ret


    def kd(name):
        cpy_name = name.split()[0]
        cpy_name = kd_name[cpy_name]
        nums = name.split()[1]
        url = "http://www.kuaidi100.com/query?type=%s&postid=%s" % (cpy_name,nums)
        #print url
        content = urllib2.urlopen(url).read()
        ret = ""
        if(content):
            # print content
            ret = json.loads(content)
            if ret["message"] == "ok":
                ret = ret["data"]
            else:
                ret = ret["message"]
        else:
            ret = "查询失败"

        return ret


    def bk(name):
        name = name.strip()
        name = urllib2.quote(name.encode("utf8"))
        url = "http://baike.baidu.com/api/openapi/BaikeLemmaCardApi?scope=103&format=json&appid=379020&bk_key=%s&bk_length=600" % name
        
        resp = urllib2.urlopen(url)
        content = resp.read()
        content = json.loads(content)

        if len(content) != 0:
            desc = content["desc"]
            # print desc
            abstract = content["abstract"]
            # print abstract
            ret = desc + "\na" + abstract
        else:        
            ret = "该词条暂未收录"
            
        return ret     

