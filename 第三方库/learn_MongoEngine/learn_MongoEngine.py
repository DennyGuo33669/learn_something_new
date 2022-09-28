from mongoengine import connect

from 第三方库.learn_MongoEngine.model import Users

#  连接到User数据库
conn = connect('user', host='127.0.0.1', port=27017)

print(conn)

users = Users.objects.all()  # 返回所有的文档对象列表
for u in users:
	print("name:", u.name, ",age:", u.age)

user1 = Users(
	name='郭子文',
	sex='男',
	age=18
)
# user1.save()
print(user1)
