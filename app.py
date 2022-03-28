# from asyncio.windows_events import NULL
# from asyncio.windows_events import NULL
# from types import NoneType
# from typing import final
import os

from flask import *
from flask import jsonify,request,session

app=Flask(__name__, static_folder="public",static_url_path="/")
app.secret_key=str(os.environ.get('SECRET_KEY'))

app.config["JSON_AS_ASCII"]=False
app.config["TEMPLATES_AUTO_RELOAD"]=True
app.config['JSON_SORT_KEYS'] = False

# Pages
@app.route("/")
def index():
	return render_template("index.html")
@app.route("/attraction/<id>")
def attraction(id):
	return render_template("attraction.html")
@app.route("/booking")
def booking():
	return render_template("booking.html")
@app.route("/thankyou")
def thankyou():
	return render_template("thankyou.html")


#=================================== 雲端資料庫連線==========================


import mysql.connector
import boto3
import json
from mysql.connector import pooling
from mysql.connector import connect

client=boto3.client('secretsmanager')
response=client.get_secret_value(SecretId='conSQL')
secretDict=json.loads(response['SecretString'])


# 連線池
dbconfig={
	"host":secretDict['host'],
	"user":secretDict['username'],
	"password":secretDict['password'],
	"database":"travelsite",
}
cnxpool = pooling.MySQLConnectionPool( pool_name = "myPool",pool_size = 20, **dbconfig)
mydb=cnxpool.get_connection()
print(mydb)
mycursor=mydb.cursor()

# 原本的連線
# mydb = mysql.connector.connect(
#     host=secretDict['host'],
#     user=secretDict['username'],
#     password=secretDict['password'],
#     database="travelsite"
# )
# print(mydb)
# mycursor=mydb.cursor()
# mycursor.execute('SET GLOBAL max_allowed_packet=67108864')

#========================================本機資料庫連線=========================================

# import mysql.connector
# import os
# from mysql.connector import pooling
# from mysql.connector import connect

# # 連線池

# dbconfig={
# 	"host":"localhost",
# 	"user":os.environ.get('DB_USER'),
# 	"password":os.environ.get('DB_PWD'),
# 	"database":"travelsite",
# 	"port":3306
# }
# cnxpool = pooling.MySQLConnectionPool( pool_name = "myPool",pool_size = 20, **dbconfig)
# mydb=cnxpool.get_connection()
# print(mydb)
# mycursor=mydb.cursor()

# 原本的連線
# mydb = mysql.connector.connect(
#     host="localhost",
#     user=os.environ.get('DB_USER'),
#     password=os.environ.get('DB_PWD'),
#     database="travelsite",
# 	port="3306"
# )
# print(mydb)
# mycursor=mydb.cursor()
# mycursor.execute('SET GLOBAL max_allowed_packet=67108864')

#=========================================本機版結束=============================
# Attraction APIs
@app.route("/api/attractions")
def attractionsAPI():
	page=request.args.get("page",None)
	p=int(page or 0) # 輸入值從字串傳成數字
	kw=request.args.get("keyword",None)
	# print("搜尋字串結果:",p,kw,"kw型態:",type(kw))

	col="id,name,category,description,address,transport,mrt,latitude,longitude,images"
	
	def pick12Row(p):
		mydb=cnxpool.get_connection()
		mycursor=mydb.cursor()
		mycursor.execute("SELECT COUNT(*) FROM spotinfo10")
		numsofRows=mycursor.fetchone()
		# print("提取資料筆數:",numsofRows)
		nokwLastPage=numsofRows[0]//12
		# print("無KW最後一頁:",nokwLastPage)	

		nokwSelect="SELECT "+col+" FROM spotinfo10 ORDER BY id LIMIT 12 offset"+" "+str(p*12)
		mydb=cnxpool.get_connection()
		mycursor=mydb.cursor()
		mycursor.execute(nokwSelect)
		nokwDB=mycursor.fetchall()
		# print("撈到資料:",nokwDB,"資料型態:",type(nokwDB),"長度:",len(nokwDB))
		spotData=[]
		for n in range(0,len(nokwDB)):
			# print("資料:",nokwDB[n][0],nokwDB[n][1],nokwDB[n][8])
			idDB = nokwDB[n][0]
			nameDB = nokwDB[n][1]
			categoryDB = nokwDB[n][2]
			descriptionDB = nokwDB[n][3]
			addressDB = nokwDB[n][4]
			transportDB = nokwDB[n][5]
			mrtDB = nokwDB[n][6]
			latitudeDB = nokwDB[n][7]
			longitudeDB = nokwDB[n][8]
			imagesDB = nokwDB[n][9].split(",")
			# print("imagesDB內容:", imagesDB,"類型:",type(imagesDB))
			spotData.append({
				"id":idDB,
				"name":nameDB,
				"category":categoryDB,
				"description":descriptionDB,
				"address":addressDB,
				"transport":transportDB,
				"mrt":mrtDB,
				"latitude":float(latitudeDB),
				"longitude":float(longitudeDB),
				"images":imagesDB[1:len(imagesDB)]
				})
		# print("spotData內容:",spotData, type(spotData))
		# print("spotData資料長度:",len(spotData))
		result = [p+1,spotData,nokwLastPage]
		# print("裡面的result:",result)
		return (result)
		

	
	def pick12RowKW(p):
		mydb=cnxpool.get_connection()
		mycursor=mydb.cursor()
		mycursor.execute("SELECT COUNT(*) FROM spotinfo10 WHERE name LIKE '%"+kw+"%'")
		numsofRows=mycursor.fetchone()
		# print("提取資料筆數:",numsofRows)
		KWlastPage=numsofRows[0]//12
		# print("無KW最後一頁:",KWlastPage)
		

		kwSelect="SELECT "+col+" FROM spotinfo10 WHERE name LIKE '%"+kw+"%'" + " LIMIT 12 offset"+" "+str(p*12)
		# print(kwSelect)
		mydb=cnxpool.get_connection()
		mycursor=mydb.cursor()
		mycursor.execute(kwSelect)
		kwDB=mycursor.fetchall()
		# print("關鍵字:",kwDB)
		# print(len(kwDB))

		kwspotData=[]
		for n in range(0,len(kwDB)):
			imagesDB2 = kwDB[n][9].split(",")
			kwspotData.append({
				"id":kwDB[n][0],
				"name":kwDB[n][1],
				"category":kwDB[n][2],
				"description":kwDB[n][3],
				"address":kwDB[n][4],
				"transport":kwDB[n][5],
				"mrt":kwDB[n][6],
				"latitude":float(kwDB[n][7]),
				"longitude":float(kwDB[n][8]),
				"images":imagesDB2[1:len(imagesDB2)]
				})
		# print("kwspotData的長度:",len(kwspotData))
		dataPnKW = [p+1,kwspotData,KWlastPage]
		return (dataPnKW)
		
	


# 判斷 1-1 : kw有輸入值
	if kw != None:
		dataPnKW=pick12RowKW(p)
		# print("有輸入關鍵字。kw是:",kw,"p是:",p,"最後一頁:",dataPnKW[2])
		# 判斷 1-2 : 頁數輸入值為整數 
		if p or p == 0:
			# 判斷 1-3 : p < 最後一頁
			if p < dataPnKW[2] :
				return {"nextPage": dataPnKW[0],"data":dataPnKW[1]}
			elif p == dataPnKW[2]:
				return {"nextPage": None,"data":dataPnKW[1]}
			else:
				return "error: 此頁數無資料"
		else:
			return "error: 頁數輸入值不是整數，無效"

	else:
		dataP=pick12Row(p)
		# print("沒有輸入關鍵字。kw是:",kw,"p是:",p,"最後一頁:",dataP[2])
		# 判斷 2-1 : 頁數輸入值為整數
		if p or p == 0:
			# 判斷 2-2 : p < 最後一頁
			if p < dataP[2]:
				return {"nextPage": dataP[0],"data":dataP[1]}		
			elif p == dataP[2]:
				return {"nextPage": None,"data":dataP[1]}		
			else:
				return "error: 此頁數無資料"
			
		else:
			return "error: 頁數輸入值不是整數，無效"

	mycursor.close()
	mydb.close()





@app.route("/api/attraction/<attractionID>")
def attractionAPI(attractionID):
	col="id,name,category,description,address,transport,mrt,latitude,longitude,images"
	# print("id為:",attractionID,"id換數字",(int(attractionID)))
	mydb=cnxpool.get_connection()
	mycursor=mydb.cursor()
	mycursor.execute("SELECT COUNT(*) FROM spotinfo10")
	numsofRows=mycursor.fetchone()
	mycursor.close()
	mydb.close()

	# print("資料筆數:",numsofRows[0],type(numsofRows[0]))
	
	# 判斷 1 : 輸入值為整數
	if int(attractionID):
		# 判斷 2 : 輸入值為有效整數 (非0、非超過資料筆數)
		if int(attractionID) != 0 and int(attractionID) <= numsofRows[0]:
			idSelect="SELECT "+col+" FROM spotinfo10 WHERE id = "+attractionID+""
			mydb=cnxpool.get_connection()
			mycursor=mydb.cursor()
			mycursor.execute(idSelect)
			dataDBId=mycursor.fetchall()
			mycursor.close()
			mydb.close()
			# print(idSelect)
			# print(dataDBId)
			for x in dataDBId:
				# print("x[0]:",x[0],x[1],x[2],x[3])
				imgs=x[9].split(',')
		
				getData={"data":{
					"id":x[0],
					"name":x[1],
					"category":x[2],
					"description":x[3],
					"address":x[4],
					"transport":x[5],
					"mrt":x[6],
					"latitude":float(x[7]),
					"longitude":float(x[8]),
					"images":imgs[1:len(imgs)]
					}}
				return getData
			return jsonify(getData)
		
		# 判斷 2 : 輸入值為無效整數 (0 或 超過資料筆數)
		else:
			return "error: 此編號無資料"

    # 判斷 1 : 輸入值不是整數 ( 空值、字串... )  
	else: 
		return "error: 輸入值不是整數，無效"
	mycursor.close()
	mydb.close()
	


@app.errorhandler(404)
def page_not_found(error):
	msg=request.args.get("message","400自訂的錯誤訊息")
	# message={"error": True,"message": "400自訂的錯誤訊息"}
	message={"error": True,"message": msg}
	return jsonify(message), 400


@app.errorhandler(500)
def page_not_found(error):
	msg=request.args.get("message","500自訂的錯誤訊息")
	message={"error": True,"message":msg}
	return jsonify(message), 500




import jwt

# 使用者登入系統API
# 新增member表單
# mycursor.execute("CREATE TABLE member (id bigint PRIMARY KEY AUTO_INCREMENT, name VARCHAR(255) NOT NULL,email VARCHAR(255) NOT NULL, password VARCHAR(255) NOT NULL, time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP)")
# mydb.commit()

# 註冊 post  
@app.route("/api/user", methods=['POST'])	
def createUser():
	data=request.get_json()
	name=data['name']
	email=data['email']
	password=data['password']
	print("使用者註冊輸入:",name,email,password)

	mydb=cnxpool.get_connection()
	mycursor=mydb.cursor()	
	mycursor.execute("SELECT name FROM member WHERE name="+"'"+name+"'")
	checkUser=mycursor.fetchall()
	print("checkuser:",checkUser)
	
	if len(checkUser) != 0: # db裡面有資料
		for i in checkUser: 
			if name == i[0]: # 有資料且有符合
				print("資料庫裡有:"+name+"")
				mycursor.close()
				mydb.close()
				return jsonify({"error": True,"message": "帳號已經被註冊"})
			else: # 有資料但不符合 user
				mydb=cnxpool.get_connection()
				mycursor=mydb.cursor()
				mycursor.execute("INSERT INTO member (name, email, password) VALUES (%s,%s,%s)",(name, email, password))
				mydb.commit()
				mycursor.close()
				mydb.close()
				print("已將"+name+"資料存入資料庫")
				return  jsonify({"ok": True})
				# return redirect ("/")
	else: # db裡面沒有資料
		mydb=cnxpool.get_connection()
		mycursor=mydb.cursor()
		mycursor.execute("INSERT INTO member (name, email, password) VALUES (%s,%s,%s)",(name, email, password))
		mydb.commit()
		mycursor.close()
		mydb.close()
		print("已將"+name+"資料存入資料庫")
		return jsonify({"ok": True})
	mycursor.close()
	mydb.close()


# 登入 patch   
@app.route("/api/user", methods=['PATCH'])
def loginUser():
	data=request.get_json()
	email=data["email"]
	password=data["password"]

	target="SELECT email, password,name FROM member WHERE email="+"'"+email+"'"
	mydb=cnxpool.get_connection()
	mycursor=mydb.cursor()
	mycursor.execute(target)
	checklogin=mycursor.fetchall()

	if len(checklogin) != 0: # db裡面有資料
		for p in checklogin:
			if p[0] == email and p[1] ==password:
				session["user"]=p[2]
				print("帳密符合")
				result={"ok": True}
				break

			else:
				print("帳密不符合")
				result={"error": True, "message": "登入失敗，帳號或密碼輸入錯誤"}
				continue

		return jsonify(result)

	else: # db裡面沒資料
		result={"error": True, "message": "登入失敗，帳號或密碼錯誤或其他原因"}
	return jsonify(result)
	mycursor.close()
	mydb.close()


# 取得登入狀態 get
@app.route("/api/user", methods=['GET'])
def getUserStatus():

	print("session檢查:",session)

	if session == {}:
		print("session中無使用者")
		return jsonify({"data": None})
	else:
		nameSession=session["user"]
		print("session中有使用者，使用者名稱:",nameSession)
		target="SELECT id, email,name FROM member WHERE name="+"'"+nameSession+"'"
		mydb=cnxpool.get_connection()
		mycursor=mydb.cursor()
		mycursor.execute(target)
		Data=mycursor.fetchone()

		idDB = Data[0]
		emailDB= Data[1]
		nameDB =Data[2]
		return jsonify({
					"data":{"id": idDB,
						"name": nameDB ,
							"email": emailDB
								}
		})
	mycursor.close()
	mydb.close()


# 登出 delete 
@app.route("/api/user", methods=['DELETE'])
def logoutUser():
	session.pop("user",None)
	return jsonify({"ok": True})



app.run(host='0.0.0.0',port=3000)
# app.run(port=3000)