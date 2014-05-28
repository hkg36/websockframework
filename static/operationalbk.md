#这个页面的接口正式运营需要限制访问IP地址，搞完了记得把IP地址列表发给我
###这里提到的接口都是get打开获得测试页面，post提交是真正的操作接口。建议使用浏览器调试功能查看请求的具体格式#
<a href="/operational_background/SendMessageToUser">向用户发送消息</a><br>
<a href="/operational_background/UpdateCircleBoard">更新圈子公告(同时向圈子成员发通知)</a><br>
<a href="/operational_background/SendMessageToCircleUser">向圈子用户发送消息</a><br>

###一般接口，没有测试页面，直接用GET
<a href="/operational_background/FindSession?sessionid=FJQoPSXJZahPsYk">搜索sessionid，注意自己改一个合法的id尝试</a><br>

###以下是上传文件相关的页面#
上传文件是上传到七牛云存储，将链接中的参数 usepage=1 去掉就能得到上传的token
请参考 <a href="http://developer.qiniu.com/docs/v6/api/overview/up/form-upload.html">七牛表单上传</a>

<a href="/operational_background/CircleIcon?usepage=1">更新圈子图标</a><br>
<a href="/operational_background/Image?usepage=1">上传图片文件，得到链接用于其他用途</a>