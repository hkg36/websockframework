#coding:utf-8
from sqlalchemy import text, or_
from datamodel.connection_info import ConnectionInfo
from datamodel.events import Events
from datamodel.friendlist import FriendList
from datamodel.user import User, UserInviteLog, UserExData
from datamodel.user_circle import UserCircle
from tools.addPushQueue import AddEventNotify
from tools.helper import Res

__author__ = 'amen'
import BackEndEnvData
import dbconfig
import json
def run(sessionid):
    if BackEndEnvData.uid is None:
        data=dbconfig.redisdb.get(str('session:%s'%sessionid))
        if data is None:
            return {"errno":1,"error":"session not found","result":{}}
        data=json.loads(data)
        be_uid=int(data['uid'])
    else:
        be_uid=BackEndEnvData.uid
    beinvitelist=[]
    with dbconfig.Session() as session:
        user_data=session.query(User).filter(User.uid==be_uid).first()
        new_user=not user_data.nick
        user_data_json=user_data.toJson()
        session.execute(text('delete from connection_info where uid=:uid or (queue_id=:queue_id and connection_id=:connection_id);'+
                    'insert into connection_info(uid,queue_id,connection_id) values(:uid,:queue_id,:connection_id);'),
                             {"uid":user_data.uid,"queue_id":BackEndEnvData.reply_queue,"connection_id":BackEndEnvData.connection_id})
        session.commit()

        if new_user:
            eventpost=[]
            for one in list(UserInviteLog.objects(phone=user_data.phone).order_by('-invite_id')):
                one.joined_uid=user_data.uid
                one.save()
                if one.join_cid and one.join_roleid:
                    usercircle=UserCircle()
                    usercircle.uid=user_data.uid
                    usercircle.by_uid=one.uid
                    usercircle.cid=one.join_cid
                    usercircle.roleid=one.join_roleid
                    session.merge(usercircle)

                friend=FriendList()
                friend.uid=user_data.uid
                friend.friendid=one.uid
                friend.type=2
                session.merge(friend)

                friend=FriendList()
                friend.uid=one.uid
                friend.friendid=user_data.uid
                friend.type=3
                session.merge(friend)

                event=Events()
                event.touid=one.uid
                event.param1=user_data.uid
                event.param2=3
                event.type="add_friend"
                event=session.merge(event)
                eventpost.append(event)

                beinvitelist.append(one.toJson())
            session.commit()
            if beinvitelist:
                inviteinfo=beinvitelist[0]
                user_data.nick=inviteinfo['nick']
                user_data.headpic=inviteinfo['headpic']
                user_data.sex=inviteinfo['sex']
                user_data.birthday=inviteinfo['birthday']
                user_data.marriage=inviteinfo['marriage']
                user_data.height=inviteinfo['height']
                user_data.position=inviteinfo['position']
                user_data=session.merge(user_data)
                session.commit()
            for one in eventpost:
                AddEventNotify(one)

        uexd=UserExData.objects(uid=BackEndEnvData.uid).first()
        resultdata={"user":user_data_json}
        if uexd:
            resultdata['client_data']=uexd.client_data
        if beinvitelist:
            resultdata['invite_list']=beinvitelist
        return Res(resultdata)
