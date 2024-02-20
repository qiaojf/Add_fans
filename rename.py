import os

# path = "./imgs/"
# # 获取该目录下所有文件，存入列表中
# f = os.listdir(path)
# i = 0
# for i in range(len(f)):
#     oldname = f[i]
#     newname = str(i+1) + '.jpg'
#     os.rename(path+oldname, path+newname)
#     i += 1

with open('.\\加粉识别配置.txt', 'r',encoding='utf-8') as f:
    groups_names = f.readlines()
    groups_names = [i.strip('\n') for i in groups_names]
    groups_names = [i for i in groups_names if i !='']
    print(groups_names)
