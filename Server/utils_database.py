# -*- coding: utf-8 -*-
"""
    Author: KaiyanZhang
    Date：  2019/4/30 14:05 
    Description: 
"""
import pymysql
# 连接数据库
db = pymysql.connect("localhost", "root", "password", "database_name")

# 使用cursor()获取操作游标
cursor = db.cursor()

# 使用游标执行SQL命令
cursor.execute('sql_command')

# 提交到数据库执行
db.commit()

# 关闭数据库连接
db.close()