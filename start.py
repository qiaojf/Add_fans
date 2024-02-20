import itchat, time
from itchat.content import *
import tools.infer.predict_system as ps
import tools.infer.utility as utility
import os
import oss2
import json
import requests
import threading

auth = oss2.Auth('LTAI4G9VUuFuD8uSEfK58wRY', 'JeYhD05R0IgEP1lsQk3T14A7rXP7Ho')
bucket = oss2.Bucket(auth, 'http://oss-cn-beijing.aliyuncs.com', 'feicui002')
url = 'http://8.140.167.172:8080/powdering/addPowdering?'
headers = {'Content-Type': 'application/json'}


# @itchat.msg_register(TEXT,isGroupChat=True)
# def text_msg(msg):
#     if msg['User']['NickName'] in ['加粉识别','自动加粉']:
#         print(msg)
#     msg_time = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(msg['CreateTime']))
#     msg_data = {'Time':msg_time,'FromUser':msg['User']['Self']['NickName'],'Content':msg['Content']}
    # print(msg_data)
    # response = requests.post(url, data = json.dumps(msg_data), headers = headers)
    # print(response.text)

@itchat.msg_register(PICTURE,isGroupChat=True)
def download_files(msg):
    if msg['User']['NickName'] in ['加粉识别','自动加粉']:
        msg.download('./imgs/%s' %msg.fileName)
        fansname,rec_res = ps.main(utility.parse_args())
        rec_res = [i[0] for i in rec_res]
        fansname = [i[0] for i in fansname]
        print(rec_res,fansname)
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
        fansName = fansName if fansName else '名称未识别'
        msg_time = msg_time if msg_time else '时间未识别'
        print(fansName,msg_time)
        if fansName == '名称未识别' and msg_time == '时间未识别':
            itchat.send('这张图片未识别，请重新发',msg['FromUserName'])
        else:
            itchat.send('昵称：%s,时间：%s'%(fansName,msg_time),msg['FromUserName'])
            msg_data = 'time=%s&url=%s&customerName=%s&fansName=%s'%(msg_time,msg.fileName,msg['ActualNickName'],fansName)
            new_url = (url+msg_data).encode('utf-8')
            req = requests.get(new_url)
            print(req.text)
            bucket.put_object_from_file('imge/%s'%msg.fileName, './imgs/%s'%msg.fileName)
        os.remove('./imgs/%s' %msg.fileName)


# @itchat.msg_register(FRIENDS)
# def add_friend(msg):
#     msg.user.verify()
#     msg.user.send('Nice to meet you!')

# @itchat.msg_register(PICTURE,isGroupChat=True)
# def send_files(img_path,i):
#     chat_group = itchat.search_chatrooms(name='自动加粉')[0]
    # for i in os.listdir(img_path):
    # chat_group.send('@img@%s' % (img_path+i))
#         time.sleep(1)

    



# itchat.auto_login(hotReload=True)

# itchat.run()


bucket.put_object_from_file('imge/123.zip.jpg', './imgs/123.zip.jpg')


ssh-keygen -t rsa -C "qiao18615740527@outlook.com" -f "coding_id_rsa"








