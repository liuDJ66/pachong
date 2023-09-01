# pachong
# 本设计为基于python爬虫+数据库mysql的数据抽取项目。
# 本程序爬取了掌上高考网站专业详情页有关专业列表，专业信息，专业就业率等专业男女比例等数据，总爬取数据量达2万多，并将爬取数据存储至mysql数据中
# 本项目中包含的内容共计以下几个：
# 1.db.python：数据库数据插入程序
# 2.index.python:爬取数据程序
# 3.chuang.sql：数据据数据结构创建语句。
# 4.finish.sql：本人爬取的数据（仅供参考）
# 请先在支持mysql的数据库管理软件中运行chuang.sql文件创建数据结构后再运行python中的index.py文件对数据进行爬取。
# db.python中端口及ip地址请以实际情况为准.
# 本项目运行在环境:python==3.9.0,pymysql==1.01,requests==2.31.0,mysql==8.0.1上。