# 每个人都是普通人，我也是，如果不写这个文档的话，每次隔几天再看这些文件自己就会发蒙，
# 如果写了这些文档，就可以顺着这些笔记，找回思路，迅速上手。
文件：
config.ini
	配置信息文件，提供了数据库配置参数，cookie值，入口微博账户。
	每次只要更新cookie为有效的cookie即可访问微博。

configutil.py:
	工具模块，提供配置文件访问操作。

database_structure.sql:
	为数据库所有表的结构。
	
detailprofile.py:
	为详细信息表的实体，封装了微博用户的详细信息，重载了输出函数。

detailprofile_db.py:
	提供了详细信息表的数据库操作。

education.py:
	为教育表的实体，封装了教育的信息。

education_db.py:
	提供了教育表的数据库操作。

getAllEducation.py:
	下载profile表中的所有未下载教育信息的微博用户

getAllProfile.py:
	下载特定学校微博用户中的那些未下载关注列表的（is_profile=-1）人的关注列表，存储到profile表中
	注：每次需要改动学校名称
	依赖：getconnect.py(获取数据库连接),profile.py(使用profile实体),profile_db.py(profile实体的数据库操作)

getAllSchool.py:
	将education中属于某个特定学校的用户id插入到对应的学校表中
	注：每次需要改动学校名称
	依赖：getconnect.py(获取数据库连接)，school_info.py,school_db.py

getAllWeibos.py
	下载某个学校未下载微博的用户的原创无图微博
	注：每次需要改动学校名称
	依赖：wb_ori_no_pic.py

getconnect.py:
	提供数据库连接，相关数据库操作方法

md5util.py:
	工具模块，提供md5函数，给定字符串，返回其md5值

profile.py:
	为微博账号实体，封装了微博帐号，昵称等信息。

profile_db.py:
	提供了微博账户表的数据库操作。

reutil.py:
	工具模块，提供了相关网页正则表达式提取函数。

school_info.py:
	封装了一个学校的微博用户的微博号，是否下载过关注列表的标识，是否下载过原创无图微博标识。
	注：我使用了五个学校用户表，每个表存储一个学校微博用户的上述信息。

school_db.py:
	提供了每个学校微博用户表的数据库操作。

wb_ori_no_pic.py:
	封装一个学校的原创无图微博属性。
	注：每次需要改动学校名称
	注：我使用了五个学校原创无图用户表，每个表存储对应学校的原创无图微博。

wb_ori_no_pic_db.py:
	提供了一个学校的原创无图微博的数据库操作。