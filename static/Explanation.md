####[手机登陆测试页面](/PhoneLogin)##
####[api测试页面](/static/PhoneTest.html)##

>邀请加入圈子的api，指定的roleid暂时都无效，使用现在使用的是圈子默认的新人id，以后再说roleid的具体指定问题，现在修改roleid是运营后台负责

App登陆使用http，或者https 方便以后登陆方式变更。登陆后，得到一个sessionid，用session id建立websocket长连接进行数据通信。Session id有一定的有效期，需要在到期前进行更换操作，过期需要重新登入。

##客户端标准方法：##
1. 通过 get https://site.com/login?name=xxxx&psw=yyyy 返回一个session id字符串，有效期 和一个 websocket连接地址 如 ws://site.com/ws
2. 连接 ws://site.com/ws 建立连接发送session id建立会话，进行远程调用和接收推送。
websocket是以数据帧为单位传输的，使用json协议进行通信。
#####(1)	请求应答模式：#
请求：

```python
{
	"func":"function_name", #函数名
	"parm":{				#参数表，以参数名:参数值的形式组织，
        "parm1":value,    #参数值可以是数组，字典等他形式
		"parm2":value,
		…
	},
	"cdata":something
}
```
应答：

```python
{
	"errno":0,    #错误码，0是成功
	"error":"ok", #错误信息
	"cdata":"something", #这个字段来自请求，将完全复制请求的相同内容，客户端可以用来协调自己的行为，如用这个key调用特定回掉函数
	"result":{ ……   #处理结果
    }
}
```
#####(2)	服务器推送数据：#
```python
{
	"push":true，#推送标记，客户端用来识别推送信息和一般应答
	"type":1  ,#协议标记，待定
	"data":{
	….      //推送数据
    }
}
```

#####(3)	注意事项：#
客户端的请求，服务器都应该有应答。
服务器的应答顺序不保证和请求顺序相同，客户端请使用cdata标志位来区分请求应答的对应关系。推送数据也可能在应答数据之间出现，客户端必须注意区分。
服务器提供压缩模式可选，客户端尽量使用压缩模式工作，压缩模式压缩的是数据帧，使用deflate算法，请求,应答，推送帧同时以压缩模式传输，启用压缩模式在链接后加上开关参数即可,如 ws://site.com/ws?usezlib=1
3.图片等大文件建议使用 7牛 等第三方服务商提供，大文件上传下载使用一般http请求。

#服务端结构#
服务器采用一个websocket服务前端接收客户端请求，将请求加入任务队列，后台处理进程从任务队列提取任务，处理出结果再将结果返回结果队列，由websocket前端将结果推送回客户端。

现在已经实现的部分包括 websocket前端使用 tornado websocket模块，理论上一台服务器可以保持10w个连接，队列服务器使用rabbitmq，任务队列和结果队列在同一个rabbitmq实例上。处理进程是同一个程序启动多个实例形成进程池。现在用python实现，考虑到这部分功能开发中可能会频繁变动，虽然交接起来会麻烦一些，但是这部分服务器都是一些独立指令，可能也没什么可交接的，除了一些bug修改的情况之外，用python会有利一些，甚至可以在服务器直接修改。推送任务的产生可以直接来自外部系统，或者内部的通知产生进程。

每个websocket前端会生成一个前端guid，每个连接也会生成一个连接guid，这两个guid会和任务数据一起发送，任何一个部分都可以根据这两个guid将数据发送到特定客户端

服务器部分还应该实现一个将手机应用用户id关联到连接guid的对照表，可以用kv数据库实现一个


###协议#
Web站点部分
Web站点包括登陆和涉及到上传大文件的指令（如发图片，声音，视频聊天等）

/getcode?phone=&lt;phone&gt;
服务器向特定手机号发验证码

/PhoneLogin?phone=&lt;phone&gt&code=&lt;code&gt;
使用手机号和验证码登录，返回内容：
```python
{"sessionid": "AaJIMq5LeVICdZT", "ws": "ws:\/\/127.0.0.1:8000\/ws", "timeout": 1387973440.355645}
```

|Sessionid|会话id|
|---------------|-------------------|
|Ws|websocket站点链接|
|Timeout |会话超时时间，时间戳方式(相对于1970.1.1 00:00:00以秒计算的偏移量)|

聊天内容提交格式，等同于web表单
从 /PostWithFile 取得上传token
```html
<form method="post" action="http://up.qiniu.com/" enctype="multipart/form-data">
	<input name="x:sessionid" type="hidden" value="{{这里填会话id}}">
	<input name="x:gid" type="hidden" value="{{发布到的group id}}">
	<input name="x:content" type="text" value="{{文字信息}}">
	<input name="x:filetype" type="hidden" value="1"> 1是图片，2是声音，3是视频
	<input name="x:length" type="hidden" value="{{音频或者视频长度，毫秒数}}">
		<input name="token" type="hidden" value="{{ 上传token }}">
		<input name="file" type="file" />
		<input type="submit" value="提交"/>
</form>
```
请不要自定义文件名，上传后会自动根据文件hash生成文件名，自定义文件名有错误覆盖的可能，我们的服务器不接受自定义文件名，指定自定义文件名将导致文件无法找到。
只有文字的聊天内容可以使用WebSocket指令10
##WebSocket 站点部分#
###请求和应答协议
请求：
```python
{
	"func":"function_name", #函数名
	"parm":{				#参数表，以参数名:参数值的形式组织，
"parm1":value,    #参数值可以是数组，字典等他形式
		"parm2":value,
		…
	},
	"cdata":something
}
```
在下面的说明中请求简写为
```python
	function_name(parm1<参数注释>,parm2={有默认值的参数},…)
```

应答：
```python
{
	"push":false,
	"errno":0,    #错误码，0是成功
	"error":"string", #错误信息
	"cdata":something, #这个字段来自请求，将完全复制请求的相同内容，
#客户端可以用来协调自己的行为，如用这个key调用特定回掉函数
	"result":{ ……   #处理结果
}
}
```
以下应答只说明result部分


1. session.start2(sessionid)连接启动，建立websocket连接后第一个指令必须是这个，否则其他指令无效，
[删除sessionid,用来测试session失效](/operational_background/DeleteSessionID?sessionid=dARxvDhFQgyHpJz)
sesionid现在的有效期是半年，用这个让某个session立刻失效，
[删除用户昵称,用来测试注册](/operational_background/DeleteNick?uid={uid}),请在参数中填写合法的uid，填写错误页面会出错

```python
{
  "push": false,
  "errno": 0,
  "result": {
    "invite_list": [   #被邀请第一次登录才有invite_list,正常的只有user
      {
        "joined_uid": 29,
        "uid": 3,
        "join_roleid": 2,
        "headpic": "http://baidu.com",
        "height": 12,
        "phone": "12345789",
        "birthday": 448693200,
        "sex": 1,
        "invite_id": 1,
        "sms_send_time": null,
        "nick": "牛逼人生",
        "create_time": 1401257930,
        "marriage": 1,
        "join_cid": 1,
        "position": "成都"
      }
    ],
    "user": {
      "background_image": null,
      "actor_level": 1,
      "uid": 29,
      "create_time": 1401303144,
      "headpic": "http://baidu.com",
      "active_by": 0,
      "actor": 0,
      "sex": 1,
      "nick": "牛逼人生",
      "birthday": 448693200,
      "marriage": 1,
      "is_stew": 0,
      "signature": null,
      "position": "成都",
      "height": 12,
      "active_level": 0
    }
  },
  "cdata": "7r4zu23c2i",
  "error": "no error"
} 
```
2. user.add\_friend(uid<可以是用户id数组或者是用户id>) 添加好友
3. user.del\_friend(uid<可以是用户id数组或者是用户id>) 删除好友
4. group.join(gid<群id>) 参加群
5. group.leave(gid) 离开群
6. group.invite (gid,uid<可以是用户id数组>) 邀请用户加入群
7. user.friend\_list(uid,pos=0<开始位置>,count=50<数量>)某个用户的好友列表，pos和count用来翻页

```python
Result={
	"friend_id":
		[
			11,
			12,
			13
		]
	"pos":0,
	"count":10
}
```
8. user.info2(uid) 查询一个用户基本信息，可以随便调用不影响服务器性能
```python
{
  "push": false,
  "errno": 0,
  "result": {
    "circles": [
      {
        "interact_poster": 0,
        "cid": 1,
        "roleid": 2,
        "level": 2,
        "poster_url": null,
        "name": "vv",
        "by_uid": 1,
        "board": "vfv",
        "time": 1347163200,
        "title": "服务员",
        "icon_url": null,
        "store_group_id": 3
      }
    ],
    "exdata": {
      "like_me_count": 3,
      "uid": 1,
      "tags": [
        "大师",
        "品质"
      ]
    },
    "user": {
      "background_image": null,
      "actor_level": 1,
      "uid": 1,
      "create_time": 1397275200,
      "headpic": null,
      "active_by": 0,
      "actor": 0,
      "sex": 0,
      "nick": "a",
      "birthday": null,
      "marriage": null,
      "is_stew": 0,
      "signature": null,
      "position": null,
      "height": 0,
      "active_level": 0
    }
  },
  "cdata": "4uq9haktil",
  "error": "no error"
}
```
9. group.info(gid<群id或者id数组>) 查询群基本信息
10. ~~post.add(gid,content) 发布信息~~
11. group.post\_list(gid,pos=0,count=50) 返回的是倒序列表，pos，count用于向过去翻页
12. group.regupdate(gid) 注册群的消息更新，用于进入群聊界面的时候刷新消息，新消息将通过推送到达，
13. group.unregupdate(gid) 取消群消息更新
14. group.my() 我加入的群
15. group.get\_new\_post(gid,frompos) 取得新消息，从某个位置开始，用于掉线后重新连上的情况
16. group.create(name,board,type) 创建群
17. group.delete(gid) 删除群，必须是创建者
18. user.update(nick=None, signature=None,sex=None, birthday=None, marriage=None, height=None, position=None,headpic=None,job=None) 更新自己的信息,不提供的参数不更新,
头像是http地址，请使用[上传图片文件](#uploadimage)上传，不检查图片是否存在
19. ~~post.like(postid) 点喜欢~~
20. ~~post.dislike(postid) 点不喜欢~~
21. ~~post.reply(postid,content) 回帖，只能回原帖~~
22. ~~post.get\_reply(postid,pos=0,count=50) 读取回复~~
23. message.send(uid,content=None,lat=None,long=None,picture=None) 私信,发送坐标或者文本或者图片,都填写就是发送文本，图片请使用[上传图片文件](#uploadimage)
24. message.read(afterid=0) 读私信
25. ~~post.likes(postid,pos=0,count=50) //喜欢的人~~
26. phonebook.upload(phone\_list) 上传通信录，不用每次上传完整的，服务器会合并
	请求例子，注意参数是数组
```python
{
    "func":"phonebook.upload",
    "parm":{
        "phone_list":[
             {"phone":"13445677","name":"可以不填"},
             {"phone":"13345677","name":"可以不填2"}
           ]
    }
}
```

27. ios.reg(device\_token,is\_debug) 注册ios设备，is\_debug指的是是否是测试证书，测试证书将通过测试通道推送
28. group.members(gid) 群成员列表
29. event.read(pos=0) 取得历史事件，从某个id开始，如果超过50条，只取最新的50条
30. active.generate\_code（level）生成激活码，激活等级默认为1，不能高于自己的actor\_level
31. active.do(active\_code) 激活自己，返回激活等级和激活者的id
32. user.search(nick) 按昵称或者手机号搜索用户，不支持全文检索,nick 是昵称或者手机号的前半部分或者全部，全是数字的时候按照手机号搜索
33. geo.user.report(lat,long) 上报当前坐标,如lat=35.233334 long=134.556743
34. group.update(gid,name=None,board=None,type=0,position=None,everyone\_caninvite=None,
only\_member\_speak=None,only\_member\_watch=None, lat=None,long=None,member\_control=None) 更新群信息,必须是创建者, member\_control 是否启用成员权限控制(1或0)
35. geo.user.search(lat,long) 搜索某个坐标附近的人
36. ~~post.get(postid) 参数可以是数组~~
37. ~~post.delete(postid) 删除帖子,只能删除自己的,同时删除跟贴和喜欢列表,不发通知~~

38. ~~post.reply\_to\_me (from\_reply=0) 回复自己的贴子列表,只返回某个回复之后的回复~~
39. ~~user.posts(uid,before=None,count=None) before是postid~~
40. ~~post.readex(postid) 取得帖子的附加多媒体信息,建议看到帖子的时候再拉取或者更新~~
41. user.friend\_timeline(before=None,count=None)
42. group.remove\_member(gid,uid) 群创建者踢人,uid可以是数组
43. user.update\_tag(tags=["大师","品质"]) 设置用户标签
44. user.get\_tag("uids":[1,2]) 取得用户标签
45. user.filter(alltag,lat,long) 搜索用户

```python
{
    "func":"user.filter",
    "parm":{
        "alltag":["大师","品质"], #用户至少包含所有的tag
        "lat":12.4455, #坐标不填就是全部用户搜索
        "long":138.223
    }
}
```
46. post.get\_new\_reply(from\_reply=0, like\_after=None) 返回最近的回复,不会超过30条,不会包括最近20个post以外的回复 like\_after 某个时间点之后的喜欢,不会包括最近20个post以外的喜欢,不填就没有
47. group.set\_member\_control(gid, uid, can\_post=None) 设置某个群成员是否可以发帖
48. circle.info(cid) 列出一个圈子的所有子标签
49. circle.set(cid,roleid)设置自己的圈子和等级，测试用，以后可能会删掉
user.info 里的每个user 增加 circle字段
50. circle.invite\_code(cid,roleid) 生成圈子邀请码,注意每个圈子角色都有level,不能生成比自己角色level高的角色邀请 用 circle.info 取得圈子的全部角色列表
51. circle.join(vcode)  填写 circle.invite\_code 的返回值,加入某个圈子并成为某个角色.不能接受降低level的角色,相同角色正常返回,但是数据不会有任何变化
52. circle.leave(cid) 退出圈子
52. circle.users(cid) 圈子所有成员
53. user.find(phone) 根据手机号模糊搜索用户,比如输入 180 会返回 180288777877 和 18098277332 等手机号的用户,最多4个,输入完整手机号只会返回1个
54. active.by\_user(uid) 和active.do一样,直接输入对方uid即可
55. circle.by\_user(uid,cid=None) 加入某个用户所在的圈子,不指定cid的话加入默认的圈子
56. circle.my() 我加入的圈子,用来读取圈子列表,返回所有我加入的圈子
57. circle.board\_history(cid) 公告板历史记录，就是圈子通知
58. circle.postlist(cid,before\_postid=None,count=20) 圈子动态列表，before\_postid用于向前翻页，现在是同时拉出所有点赞和回复
58. circle.post\_after(cid,after\_postid) 圈子动态列表下拉刷新，取得比after\_postid更晚的新贴
59. circle.addpost(cid,content,pictures=[],mid=None) 发圈子动态，pictures是图片链接字符串数组，上传方法按照[上传图片文件](#uploadimage) mid 是商品id,要推荐商品的话参考 `merchandise.list`
60. circle.likepost(postid) 给圈子动态点赞，重复给同一个动态点赞会返回过去的记录，不会有效果，可以通过记录的时间戳判断
70. circle.addreply(postid,content) 给圈子动态回复，现在只能回复文字，需要回复图片就说很容易加上的
71. tools.save\_data() 上传客户端的任意数据，参数表是任意的，喜欢用什么就用什么，如
```python
{
	"func":"tools.save_data",
	"parm":{
"ok":["sce","128"],
"shit":1,
"ff":{"ss":2}
	}
}
```
72. tools.read\_data() 取得上传的数据
73. user.invite(phone,nick,headpic=None,sex=None,birthday = None,marriage = 0,height = 0,position = None,join\_cid=None,join\_roleid=None) 邀请其他用户，
必须填手机号和昵称，头像上传请使用[上传图片文件](#uploadimage)，第一次邀请会发短信，可以反复邀请，重复的邀请只是会修改邀请数据，最多一天只会发送一次短信,
用户已经存在，返回2002错误和用户的信息，已经接受邀请返回2001错误
74. user.invite\_list() 已经发出的邀请列表，返回值中的joined\_uid表示接受邀请的用户的用户id
75. <a name="qiniu_uploadtoken" id="qiniu_uploadtoken"></a> tools.qiniu_uploadtoken() 和[上传图片文件](#uploadimage) 取得token的方法完全相同，每个token有1个小时的有效期，
可以在有效时间内上传无限的图片，建议要上传多张图片的时候，取得一个新token，然后依次上传图片，取得每张图片的url地址
76. circle.request\_join(uid,cid) 向某个用户请求加入某个圈子，会向对方推送请求通知
```python
{
  "push": true,
  "data": {
    "event": {
      "cid": 2,
      "create_time": 1401990301,
      "type": "request_join_circle",
      "eid": 31,
      "uid": 2
    }
  },
  "type": "event"
} 
```
77. circle.accept\_join(eid,roleid=None) 同意某人加入圈子，需要对应通知的eid，如果不提供roleid就是自己的roleid,如果提供，角色level不能高于自己
```python
{
  "push": true,
  "data": {
    "event": {
      "cid": 2,
      "roleid": 1,
      "by_uid": 19,
      "create_time": 1401990395,
      "eid": 35,
      "type": "accept_join_circle"
    }
  },
  "type": "event"
} 
```
58. group.postlist(gid,before\_postid=None,count=20) 群动态列表，before\_postid用于向前翻页，现在是同时拉出所有点赞和回复
58. group.post\_after(gid,after\_postid) 群动态列表下拉刷新，取得比after\_postid更晚的新贴
59. group.addpost(gid,content=None,pictures=[],video=None,videolen=None,voice=None,voicelen=None,
    lat=None,lng=None) 发圈子动态，pictures是图片链接字符串数组，上传方法按照[上传图片文件](#uploadimage) ,可以上传视频(video=视频链接)，声音(voice=音频链接)，长度单位是毫秒整数，
    视频音频上传方法和图片相同，取得视频截图可以使用类似这样的链接附加参数 http://open.qiniudn.com/thinking-in-go.mp4<b style="color:red">?</b>vframe/jpg/offset/7<b style="color:red">|</b>imageView2/1/w/150/h/200/q/56/format/JPG
    后面参数部分的意义是（1） vframe/jpg/offset/7 将视频第7秒截图 （2）imageView2/1/w/150/h/200/q/56/format/JPG 将截图重新压制成新的图片尺寸。
60. circle.likepost(postid) 给群动态点赞，重复给同一个动态点赞会返回过去的记录，不会有效果，可以通过记录的时间戳判断
70. circle.addreply(postid,content) 给群动态回复，现在只能回复文字，需要回复图片就说很容易加上的
71. endorsement.list_user() 列出所有的代言人

72. album.add(url,filetype,content=None,width=None,height=None,length=None) 添加相册，url文件链接，filetype文件类型(1=图片，2=声音，3=视频),content 附加一句话，witdh=图片宽度(filetype=1)，height=图片高度(filetype=1)，length内容长度(filetype=2,3)
73. album.read(uid,before=None,count=10) 读取相册，before=读取某个did之前的文件
74. album.delete(did) 删除某个文件
###向客户端推送消息
####1. 事件推送
```python
    {"push": true,
	 "type": "event",
       "data":
        {
            "event":{
                "create_time": 1388978778.0,
                "type": "add_friend",
                "eid": 3,
                "uid": 1
             } #event的内容和event.read取得的结构完全相同
        }
    }
```
####2. 新消息提示，推送的消息包括好友的消息和注册的群的消息，客户端可以根据groupid区分,可能会重复推送同一条消息，如好友在当前群中，客户端注意容错
```python
	{
	"push":true，#推送标记，客户端用来识别推送信息和一般应答
	"type":"newpost"
	"data":{
		"post":{
				"postid":
				"uid":
				"group_id":
				"content":
				"picture":
				"video":
				"voice":
				"width":200
				"height":100
				"length":344555
				"like":12,
				"time":
        }
        }
	}
```
####4 新私信提示,私信不分用户推送，客户端可以根据用户id分组
```python
	{
		"push":true，//推送标记，客户端用来识别推送信息和一般应答
		"type":"newmsg"
		"data":{
				"message":
					{
					"msgid":
					"uid":
					"content":
					"time":
					}
			}
}
```
####5 推荐用户，推荐加为好友的用户，来自通信录,数据带有手机号码信息
```python
	{
		"push":true,
		"type":"fromphonebook",
		"data":{
			"users":[
				{
"uid":,
"phone":
"nick":
"headpic":
"sex":
"birthday":
"marriage":
"background_image":
"height":
"create_time":
				},
				….
			]
		}
	}
```
6.回复推送,推给原帖所有者
```python
{
    "push": true,
     "data":
      {
            "gid":1,
            "reply":
             {"content":"you bitch",
              "postid": 1,
              "replyid": 2,
              "uid": 2,
              "time": 1389336522.0
              }
      },
      "type": "newreply"
}
```
7 喜欢推送,推送给原帖所有者
```python
{"push": true,
 "data":
    {"like":
        {"postid": 1,
         "uid": 2,
          "time": 1389338046.0
         }
    },
"type": "newlike"
}
```
8 圈子新公告通知
```python
{
    "push":true,
    "data":
        {"board":
            {"bid":2,
             "cid":1,
             "board":"大家好",
             "time":1400613859.0
             }
        },
    "type":"circle.newboard"
}
```
#多媒体消息 （请自己替换一个自己的sessionid）
**客户端上传的时候，去掉 usepage=1 直接获得 token**
##~~上传头像~~user.update已经支持直接填写图片连接
http://service.laixinle.com/upload/HeadImg?sessionid=5Wnp5qPWgpAhDRK&usepage=1 测试页面
http://service.laixinle.com/upload/HeadImg?sessionid=5Wnp5qPWgpAhDRK      取得token
##~~群里发多媒体帖子~~group.addpost 已经支持直接填写多张图片地址
http://service.laixinle.com/upload/Post?sessionid=5Wnp5qPWgpAhDRK&usepage=1
##~~多媒体私信~~message.send 已经支持直接填写图片连接
http://service.laixinle.com/upload/Message?sessionid=YtcS7pKQSydYPnJ&usepage=1
##~~向帖子附加多媒体内容,只能向自己的贴子附加,服务器检查帖子的归属~~ group.addpost 已经支持直接填写多张图片地址
http://service.laixinle.com/upload/PostEx?sessionid=05eh4JdjqeBPh2j&postid=71&usepage=1
<a name="uploadimage" id="uploadimage"></a>
##上传图片文件，得到图片链接,客户端请参考[这个指令](#qiniu_uploadtoken)，
**一个token可以在1小时内上传无限次**
http://service.laixinle.com/upload/Image?usepage=1&sessionid=kkfZCxu1gQyVT9G
#交易接口
1. merchandise.groups() //商品分组
2. merchandise.list(gid), //列出分组的所有商品列表,暂时先这样
3. merchandise.count\_price(mid,people\_count), //计算价格 people\_count是人数
4. merchandise.createorder(mid,people\_count,hardwareid) //网页支付,获取网页地址打开浏览器操作,用于第一次支付或者不想用已有的卡支付的情况,
hardwareid是客户端生成的能标识特定手机的字符串，随便用什么方法生成都行，每个手机要每次生成的都一样，支付平台要求这个字段
5. merchandise.history(before,count) //before=订单号，用于翻页，默认不填是第一页  paystate= 0(未付款) 1(已付款) 2(已退款) 3(已预订) -1(订单错误)
6. merchandise.recommendbyme(before,count)  //因为我推荐而完成的订单,参数全部可选
7. merchandise.get(mid=[1,3]) //取得特定的多个商品，商品id可以是数组
8. merchandise.cards() //取得用户已绑定银行卡的列表,这个接口操作缓慢，如果没有使用新卡每次都一样，客户端请缓存
9. merchandise.paybycard(cardid,mid,people\_count,hardwareid) //银行卡直接扣款,cardid从`merchandise.cards()`取得，其他同`merchandise.createorder`
10. merchandise.pre_order(mid) 预订商品。这个方式不会有付款流程，返回数据里没有跳转url，但是有订单号，历史记录里，这种订单的**paystate=3** 就是已预订状态

##支付成功推送:
发起支付时都会返回orderid ,这里通过orderid来更新本地数据状态,有可能会重复推送成功信息,因为不同途径的支付成功通知无法区别,但是orderid肯定是一样的

```python
{
"push":true,
    "data":{
    "log":
        {
            "orderid":"1394090000-749",
            "payid":6,
            "uid":17,
            "mid":1,
            "productname":"测试 商品",
            "amount":8,
            "create_time":1394090516.0,
            "productdesc":"测试商品介绍",
            "ex_people":2,
            "productcatalog":1,
            "paystate":1
         }
     },
    "type":"paylog"
}
```
#应答错误码

0=成功<br>
1=session id无效需要重新登入<br>
2=没有权限进行这个操作<br>
3=查询目标不存在<br>
4=操作速度过快，现在大部分写入接口只能10s操作一次，请不要无视这个错误，这通常和客户端bug有关<br>
1000 昵称已使用<br>
1001 新号码和旧号码相同<br>
1002 手机号已被另一个账号使用<br>
1003 验证码错误<br>
2001 已经接受邀请<br>
2002 手机号对应的用户已存在
