#这个页面的接口正式运营需要限制访问IP地址，搞完了记得把IP地址列表发给我
###这里提到的接口都是get打开获得测试页面，post提交是真正的操作接口。建议使用浏览器调试功能查看请求的具体格式#
1. [向用户发送消息](/operational_background/SendMessageToUser)
2. [更新圈子公告(同时向圈子成员发通知)](/operational_background/UpdateCircleBoard)
3. [向圈子用户发送消息](/operational_background/SendMessageToCircleUser)
4. [发布圈子动态](/operational_background/NewCirclePost)

###一般接口，没有测试页面，直接用GET
1. [搜索sessionid，注意自己改一个合法的id尝试](/operational_background/FindSession?sessionid=FJQoPSXJZahPsYk)
2. [删除用户昵称,用来测试注册](/operational_background/DeleteNick?uid={uid}),请在参数中填写合法的uid，填写错误页面会出错

###以下是上传文件相关的页面#
上传文件是上传到七牛云存储，将链接中的参数 usepage=1 去掉就能得到上传的token
请参考 [七牛表单上传](http://developer.qiniu.com/docs/v6/api/overview/up/form-upload.html)

1. [更新圈子图标](/operational_background/CircleIcon?usepage=1)
2. [上传图片文件，得到链接用于其他用途](/operational_background/Image?usepage=1)