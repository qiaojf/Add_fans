# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import os
import sys

import requests
import inspect
import tools.infer.predict_system as ps
import tools.infer.utility as utility
import oss2
import wechat
import json
import time
from wechat import WeChatManager, MessageType
from imgdecode import *
import shutil
import datetime

AUTH = oss2.Auth('LTAI4G9VUuFuD8uSEfK58wRY', 'JeYhD05R0IgEP1lsQk3T14A7rXP7Ho')
BUCKET = oss2.Bucket(AUTH, 'http://oss-cn-beijing.aliyuncs.com', 'feicui002')
url = 'http://8.140.167.172:8080/powdering/addPowdering?'
headers = {'Content-Type': 'application/json'}

today = datetime.datetime.today()
year = today.year
month = today.month
if len(str(month))==1:
    month = '0' + str(month)

MEMBER_LIST = []
REG_CHATROOMS_WXID = []
wechat_manager = WeChatManager(libs_path='.\libs')

# 这里测试函数回调
@wechat.CONNECT_CALLBACK(in_class=False)
def on_connect(client_id):
    print('[on_connect] client_id: {0}'.format(client_id))


# @wechat.RECV_CALLBACK(in_class=False)
# def on_recv(client_id, message_type, message_data):
#     # if message_type == MessageType.MT_DATA_CHATROOMS_MSG:
#         print('[on_recv] client_id: {0}, message_type: {1}, message:{2}'.format(client_id,
#                                                                                 message_type, message_data))

@wechat.CLOSE_CALLBACK(in_class=False)
def on_close(client_id):
    print('[on_close] client_id: {0}'.format(client_id))

def get_chatroom_names():
    with open('./识别群配置.txt','r',encoding='utf-8') as f:
        chatroom_names = []
        for chatroom in f:
            chatroom_names.append(chatroom.strip('\n'))
    return chatroom_names

def get_nickname(from_member_wxid,member_info):
    for member in member_info:
        if member['member_id'] == from_member_wxid:
            nickname = member['member_nickname']
    return nickname

def reg_img(wechat_manager,send_to,fileName,nickname):
    fansname,rec_res = ps.main(utility.parse_args())
    rec_res = [i[0] for i in rec_res]
    fansname = [i[0] for i in fansname]
    # print(rec_res,fansname)
    msg_time = None
    for i in fansname:
        if i in ['<','00'] or ':' in i or '：' in i:
            fansname.remove(i)
    for i in rec_res:
        if ':' in i or '：' in i:
            msg_time = i
            break
    if fansname != []:
        if len(fansname)>1:
            fansName = fansname[0]+fansname[1]
        else:
            fansName = fansname[0]
    else:
        fansName = None
    fansName = fansName if fansName else '昵称未识别'
    msg_time = msg_time if msg_time else '时间未识别'
    # print(fansName,msg_time)
    if fansName == '昵称未识别' and msg_time == '时间未识别':
        wechat_manager.send_text(1,to_wxid=send_to, text='这张图片未识别')
    else:
        wechat_manager.send_text(1,to_wxid=send_to, text='昵称：%s,时间：%s'%(fansName,msg_time))
    msg_data = 'time=%s&url=%s&customerName=%s&fansName=%s'%(msg_time,fileName,nickname,fansName)
    new_url = (url+msg_data).encode('utf-8')
    req = requests.get(new_url)
    print(req.text)
    BUCKET.put_object_from_file('imge/%s'%fileName, r'./imgs\\%s'%fileName)
    os.remove(r'./imgs\\%s'%fileName)

# 这里测试类回调， 函数回调与类回调可以混合使用
class LoginTipBot(wechat.CallbackHandler):

    @wechat.RECV_CALLBACK(in_class=True)
    def on_message(self, client_id, message_type, message_data):

        # chatroom_names = get_chatroom_names()
        # 判断登录成功后，就向文件助手发条消息
        if message_type == MessageType.MT_USER_LOGIN:
            time.sleep(2)
            wechat_manager.get_chatrooms(1)
        if message_type == MessageType.MT_DATA_CHATROOMS_MSG:
            if isinstance(message_data,list):
                reg_chatrooms = [ i for i in message_data if i['nickname'] in chatroom_names]
                reg_chatrooms_wxid = [i['wxid'] for i in reg_chatrooms]
                for i in reg_chatrooms_wxid:
                    wechat_manager.get_chatroom_members(1,i)
                    REG_CHATROOMS_WXID.append(i)
        if message_type == MessageType.MT_DATA_CHATROOM_MEMBERS_MSG:
            for member in message_data['member_list']:
                if {'member_id':member['wxid'],'member_nickname':member['nickname']} not in MEMBER_LIST:
                    MEMBER_LIST.append({'member_id':member['wxid'],'member_nickname':member['nickname']})
        if message_type == MessageType.MT_RECV_PICTURE_MSG:
            if message_data['to_wxid'] in REG_CHATROOMS_WXID:     
                time.sleep(1)
                path = r'C:\\Users\\coder\\Documents\\WeChat Files\\wxid_1ssew2cdblyk12\\FileStorage\\Image\\{0}-{1}'.format(year,month)
                target_path = r'./imgs\\'
                img = find_datfile(path)
                fileName = str(img)[:-4]+'.jpg'
                shutil.move(path+'\\'+img+'.jpg', target_path+fileName)
                from_member_wxid = message_data['from_wxid']
                nickname = get_nickname(from_member_wxid,MEMBER_LIST)
                reg_img(wechat_manager,message_data['to_wxid'],fileName,nickname)


if __name__ == "__main__":
    chatroom_names = get_chatroom_names()
    print('接收识别群如下：')
    for i in chatroom_names:
        print(str(chatroom_names.index(i))+'：'+i)

    bot = LoginTipBot()

    # # 添加回调实例对象
    wechat_manager.add_callback_handler(bot)
    wechat_manager.manager_wechat(smart=True)

    # 阻塞主线程
    while True:
        time.sleep(0.2)




