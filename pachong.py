# -*- codeing = utf-8 -*-
# @time : 2020/11/27 18:06
# @Author : 胡诚
# @Fime : pachong.PY
# @SOFEWARE : PyCharm

from py2neo import Graph, Node, Relationship   #输入neo4j
import urllib.request                          #制定url,获取网页数据
import json

#1.爬取网页信息
baseurl = urllib.request.urlopen("https://www.luogu.com.cn/problem/list?page=1&_contentOnly=1")
#读到信息内容
message = baseurl.read().decode("utf-8")
#将信息转为json包处理
infomessage = json.dumps(message)
#json包导出‘str’型数据
jsonmessage  =  json.loads(infomessage)
#再次利用json包导出字典型数据
pythonmessage = json.loads(jsonmessage)



#定义一个函数来获取字典中的字典
def dict_get(dict, objkey, default):
    tmp = dict
    for key,value in tmp.items():
        if key == objkey:
            return value
        else:
            if type(value) is type(dict):
                ret = dict_get(value, objkey, default)
                if ret is not default:
                    return ret
    return default
#2.数据处理
#录取到result中的键值对
sjlist = dict_get(pythonmessage,"result",1)
#读取每个要求的元素
tags = []
wantsTranslations = []
totalSubmits = []
totalAccepteds = []
flags = []
pids = []
titles = []
difficultys = []
types = []

for i in sjlist:
    tags.append(i['tags'])
    wantsTranslations.append(i['wantsTranslation'])
    totalSubmits.append(i['totalSubmit'])
    totalAccepteds.append(i['totalAccepted'])
    flags.append(i['flag'])
    pids.append(i['pid'])
    titles.append(i['title'])
    difficultys.append(i['difficulty'])
    types.append(i['type'])

#用py2neo包创建各个节点
graph = Graph(
    "http://localhost:7474",
    username="neo4j",
    password="123456"
)
graph.delete_all()                         #删除数据库中以往的图

#做一个lists列表，这个lists列表包含所有节点
lists = []
for s in range(0,len(tags)):
    lists.append("列表"+str(s))
# 创建tags节点,属性为tag，tag每个tags列表里的数，下面都一样，将所有节点指向列表【1】
#封装的a可多次使用
for a in range(0,len(tags)):
    a = Relationship(Node("tags",tag = tags[a]), '标签的名称', Node("lists",list = lists[a]))
    graph.create(a)

for a in range(0, len(wantsTranslations)):
    a = Relationship(Node("wantsTranslations",wantsTranslation = wantsTranslations[a]), '难度的名称', Node("lists",list = lists[a]))
    graph.create(a)

for a in range(0, len(totalSubmits)):
    a = Relationship(Node("totalSubmit",totalSubmit = totalSubmits[a]), '标签的序号', Node("lists",list = lists[a]))
    graph.create(a)

for a in range(0, len(totalAccepteds)):
    a = Relationship(Node("totalAccepteds",totalAccepted = totalAccepteds[a]), '类型的序号', Node("lists",list = lists[a]))
    graph.create(a)

for a in range(0, len(flags)):
    a = Relationship(Node("flags",flag = flags[a]), '类型的名称', Node("lists",list = lists[a]))
    graph.create(a)

for a in range(0, len(pids)):
    a = Relationship(Node("pids",pid = pids[a]), '题目的编号', Node("lists",list = lists[a]))
    graph.create(a)

for a in range(0, len(titles)):
    a = Relationship(Node("titles",title = titles[a]), '题目的名称', Node("lists",list = lists[a]))
    graph.create(a)

for a in range(0, len(difficultys)):
    a = Relationship(Node("difficultys",difficulty = difficultys[a]), '难度的等级', Node("lists",list = lists[a]))
    graph.create(a)

for a in range(0, len(types)):
    a = Relationship(Node("types",type = types[a]), '标签的类型', Node("lists",list = lists[a]))
    graph.create(a)

#由于列表之间还有在同一字典里的关系，设一个总结点，把相同属性连接起来
node_1 = Node("dict", dicts = "字典")
graph.create(node_1)
for k in range(0,len(tags)):
    node_1_call_lists = Relationship(node_1,'类型',Node("lists",list = lists[k]))
    graph.create(node_1_call_lists)














