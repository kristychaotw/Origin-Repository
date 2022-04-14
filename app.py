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


#========================================資料庫連線=========================================

import mysql.connector
import os
from mysql.connector import pooling,connect,Error

# 連線池

dbconfig={
	"host":"database-1.cohxynft1tdv.us-east-1.rds.amazonaws.com",
	"user":os.environ.get('DB_USER'),
	"password":os.environ.get('DB_PWD'),
	"database":"travelsite",
	"port":3306
}
cnxpool = pooling.MySQLConnectionPool( pool_name = "myPool",pool_size = 20, **dbconfig)


#=========================================本機版結束=============================

def dbConnect(sqlquery):
	try:
		mydb=cnxpool.get_connection()
		mycursor=mydb.cursor()
		mycursor.execute(sqlquery)
		dbResult=mycursor.fetchall()
		# mydb.commit()
		return dbResult
	except Error as e:
		print("資料庫連線失敗:", e)
	finally:
		if (mydb.is_connected()):
			mycursor.close()
			mydb.close()


def dbConnectOne(sqlquery):
	try:
		mydb=cnxpool.get_connection()
		mycursor=mydb.cursor()
		mycursor.execute(sqlquery)
		dbResult=mycursor.fetchone()
		# mydb.commit()
		return dbResult
	except Error as e:
		print("資料庫連線失敗:", e)
	finally:
		if (mydb.is_connected()):
			mycursor.close()
			mydb.close()


def dbConnect_insert(name,email,password):
	try:
		mydb=cnxpool.get_connection()
		mycursor=mydb.cursor()
		mycursor.execute("INSERT INTO member (name, email, password) VALUES (%s,%s,%s)",(name, email, password))
		mydb.commit()
		return "commit done"
	except Error as e:
		print("資料庫連線失敗:", e)
	finally:
		if (mydb.is_connected()):
			mycursor.close()
			mydb.close()

#======================================= Attraction APIs ===============================================

# Attractions API
@app.route("/api/attractions")
def attractionsAPI():
	page=request.args.get("page",None)
	p=int(page or 0) # 輸入值從字串傳成數字
	kw=request.args.get("keyword",None)
	# print("搜尋字串結果:",p,kw,"kw型態:",type(kw))

	col="id,name,category,description,address,transport,mrt,latitude,longitude,images"
	
	def pick12Row(p):
		numsofRows=dbConnect("SELECT COUNT(*) FROM spotinfo10")
		# print(numsofRows)
		nokwLastPage=numsofRows[0][0]//12
		# print("無KW最後一頁:",nokwLastPage)	

		nokwSelect="SELECT "+col+" FROM spotinfo10 ORDER BY id LIMIT 12 offset"+" "+str(p*12)
		nokwDB=dbConnect(nokwSelect)
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
		numsofRows=dbConnect("SELECT COUNT(*) FROM spotinfo10 WHERE name LIKE '%"+kw+"%'")
		# print("回傳:",numsofRows[0])
		KWlastPage=numsofRows[0][0]//12
		# print("無KW最後一頁:",KWlastPage)
		

		kwSelect="SELECT "+col+" FROM spotinfo10 WHERE name LIKE '%"+kw+"%'" + " LIMIT 12 offset"+" "+str(p*12)
		# print(kwSelect)
		kwDB=dbConnect(kwSelect)
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





# attractionID API
@app.route("/api/attraction/<attractionID>")
def attractionAPI(attractionID):
	col="id,name,category,description,address,transport,mrt,latitude,longitude,images"
	# print("id為:",attractionID,"id換數字",(int(attractionID)))
	numsofRows=dbConnect("SELECT COUNT(*) FROM spotinfo10")


	# print("資料筆數:",numsofRows[0],type(numsofRows[0]))
	
	# 判斷 1 : 輸入值為整數
	if int(attractionID):
		# 判斷 2 : 輸入值為有效整數 (非0、非超過資料筆數)
		if int(attractionID) != 0 and int(attractionID) <= numsofRows[0][0]:
			idSelect="SELECT "+col+" FROM spotinfo10 WHERE id = "+attractionID+""
			dataDBId=dbConnect(idSelect)
		
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


# ====================================== JWT (待做) ========================================================

import jwt

# 新增member表單
# mycursor.execute("CREATE TABLE member (id bigint PRIMARY KEY AUTO_INCREMENT, name VARCHAR(255) NOT NULL,email VARCHAR(255) NOT NULL, password VARCHAR(255) NOT NULL, time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP)")
# mydb.commit()


#======================================= Member System APIs ===============================================
# 註冊 post  
@app.route("/api/user", methods=['POST'])	
def createUser():
	data=request.get_json()
	name=data['name']
	email=data['email']
	password=data['password']
	# print("使用者註冊輸入:",name,email,password)

	checkUser=dbConnect("SELECT name FROM member WHERE name="+"'"+name+"'")
	# print("checkuser:",checkUser)
	
	if len(checkUser) != 0: # db裡面有資料
		for i in checkUser: 
			if name == i[0]: # 有資料且有符合
				print("資料庫裡有:"+name+"")
				return jsonify({"error": True,"message": "帳號已經被註冊"})
			else: # 有資料但不符合 user
				# target="INSERT INTO member (name, email, password) VALUES (%s,%s,%s)",(name, email, password)
				dbConnect_insert(name,email,password)
				print("已將"+name+"資料存入資料庫")
				return  jsonify({"ok": True})
				# return redirect ("/")
	else: # db裡面沒有資料
		# target="INSERT INTO member (name, email, password) VALUES (%s,%s,%s)",(name, email, password)
		dbConnect_insert(name,email,password)
		print("已將"+name+"資料存入資料庫")
		return jsonify({"ok": True})



# 登入 patch   
@app.route("/api/user", methods=['PATCH'])
def loginUser():
	data=request.get_json()
	email=data["email"]
	password=data["password"]

	target="SELECT email, password,name FROM member WHERE email="+"'"+email+"'"
	checklogin=dbConnect(target)

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
		Data=dbConnect(target)
		# print("Data是:",Data)

		idDB = Data[0][0]
		emailDB= Data[0][1]
		nameDB =Data[0][2]
		return jsonify({
					"data":{"id": idDB,
						"name": nameDB ,
							"email": emailDB
								}
		})


# 登出 delete 
@app.route("/api/user", methods=['DELETE'])
def logoutUser():
	session.pop("user",None)
	return jsonify({"ok": True})



#============================================= Booking Sql ===========================================
def dbInsert_table(sql,value):
	try:
		mydb=cnxpool.get_connection()
		mycursor=mydb.cursor()
		mycursor.execute(sql,value)
		mydb.commit()
		return "commit done"
	# mycursor.execute("INSERT INTO member (name, email, password) VALUES (%s,%s,%s)",(name, email, password))
	except Error as e:
		print("資料庫連線失敗:", e)
	finally:
		if (mydb.is_connected()):
			mycursor.close()
			mydb.close()


def dbDelete(sql):
	try:
		mydb=cnxpool.get_connection()
		mycursor=mydb.cursor()
		mycursor.execute(sql)
		mydb.commit()
		return "commit done"
	# mycursor.execute("INSERT INTO member (name, email, password) VALUES (%s,%s,%s)",(name, email, password))
	except Error as e:
		print("資料庫連線失敗:", e)
	finally:
		if (mydb.is_connected()):
			mycursor.close()
			mydb.close()
#============================================= Booking APIs ===========================================

# 新增booking table
# mydb=cnxpool.get_connection()
# mycursor=mydb.cursor()
# mycursor.execute("CREATE TABLE booking (id BIGINT PRIMARY KEY AUTO_INCREMENT, attractionID BIGINT NOT NULL, date DATE NOT NULL, time TINYTEXT NOT NULL, price SMALLINT NOT NULL,timenow DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP)")
# mydb.commit()
# mydb.close()


# Post 建立新的預定行程
@app.route("/api/booking", methods=["POST"])
def createBooking():
	if session == {}:
		print("session中無使用者")
		return jsonify({"error": True,"message": "未登入系統，拒絕存取"}),403
	else:
		cleanTable=dbDelete("DELETE FROM booking")
		print("cleanTable:",cleanTable)
		data=request.get_json()
		attractionId=data["attractionId"]
		dateUser=str(data["date"])
		timeUser=data["time"]
		priceUser=data["price"]
		sql="INSERT INTO booking (attractionID,date,time,price) VALUES (%s,%s,%s,%s)"
		value=(attractionId,dateUser,timeUser,priceUser)	
		result=dbInsert_table(sql,value)
		# print(result)
		if result=="commit done":
			return jsonify({"ok": True}),200
		else:
			return jsonify({"error": True,"message": "建立失敗，輸入不正確或其他原因"}),400


# Get 取得尚未確認下單的預定行程
@app.route("/api/booking",methods=['GET'])
def getBooking():
	if session == {}:
		print("session中無使用者")
		return jsonify({"error": True,"message": "未登入系統，拒絕存取"}),403
	else:
		sql2="SELECT attractionID,date,time,price FROM booking"
		bookingDB=dbConnect(sql2)
		if bookingDB != []:
			booking=bookingDB[0]
			# print("booking[0]:",booking[0])
			attractionID=str(booking[0])
			sql="SELECT id,name,address,images FROM spotinfo10 WHERE id="+attractionID+""
			spot=dbConnect(sql)[0]
			# print("spot:",spot)
			oneImg=spot[3].split(",")[1]
			# print("oneImg:",oneImg)
			return jsonify({"data":{"attraction": 
			{
				"id": spot[0],
				"name":spot[1],
				"address": spot[2],
				"image": oneImg
			},
			"date": booking[1],
			"time": booking[2],
			"price":booking[3]
			}
			}),200
		else:
			return jsonify({"data":None}),200


# Delete 刪除目前的預定行程
@app.route("/api/booking",methods=["DELETE"])
def deleteBooking():
	if session == {}:
		print("session中無使用者")
		return jsonify({"error": True,"message": "未登入系統，拒絕存取"}),403
	else:
		sql="DELETE FROM booking"
		dbDelete(sql)
		return jsonify({"ok": True}),200
	
#===========================================新增order表單-複製from booking======================================
mydb=cnxpool.get_connection()
mycursor=mydb.cursor()
mycursor.execute("DROP TABLE triporder")
mycursor.execute("CREATE TABLE triporder (number BIGINT NOT NULL, trip JSON NOT NULL, contact JSON NOT NULL, status TINYINT NOT NULL)")
mydb.commit()
mydb.close()



def createNumber():
	from datetime import datetime
	currentDay = datetime.now().day
	currentMonth = datetime.now().month
	currentYear = datetime.now().year
	# print("test日期:",currentDay,type(currentDay))
	n=dbConnectOne("SELECT COUNT(*) FROM triporder")[0]
	# print("n:",n)
	result=str(currentYear)+str(currentMonth)+str(currentDay)+"00"+str(n+1)
	print("num:",result)
	return result

def addOrderData(sql,value):
	try:
		mydb=cnxpool.get_connection()
		mycursor=mydb.cursor()
		mycursor.execute(sql,value)
		mydb.commit()
		return "success add data"
	except Error as e:
		print("資料庫連線失敗:", e)
	finally:
		if (mydb.is_connected()):
			mycursor.close()
			mydb.close()

def updateOrderData(sql):
	try:
		mydb=cnxpool.get_connection()
		mycursor=mydb.cursor()
		mycursor.execute(sql)
		mydb.commit()
		return "success update data"
	except Error as e:
		print("資料庫連線失敗:", e)
	finally:
		if (mydb.is_connected()):
			mycursor.close()
			mydb.close()

import requests
#================================== 金流API =======================================
@app.route('/api/orders',methods=["POST"])
def createOrders():
	if session == {}:
		print("session中無使用者")
		return jsonify({"error": True,"message": "未登入系統，拒絕存取"}),403
	else:
		orderData=request.get_json()
		print("前端傳送的值:",orderData)
		order=json.dumps(orderData["order"])
		contact=json.dumps(orderData["contact"])
		prime=orderData["prime"]
		status=1
		number=createNumber()
		# print("post內容:",order,contact,"prime密鑰:",prime,"訂單狀態:",status,number,"contact類型:",type(contact))
		sql="INSERT INTO triporder (number,trip,contact,status) VALUES (%s,%s,%s,%s)"
		value=(number,order,contact,status)
		result=addOrderData(sql,value)
		print("資料庫連線result:",result)
		
		if result != "success add data" :
			return jsonify({
				"error": true,
				"message": "訂單建立失敗，輸入不正確或其他原因"
				}),400
		else:
			# 連線 TAPPAY 準備付款
			url="https://sandbox.tappaysdk.com/tpc/payment/pay-by-prime"
			headers={ 
			"Content-Type": "application/json",
			"x-api-key": os.environ.get('PAY_KEY'),
			}
			data={
			"prime": prime,
			"partner_key": os.environ.get('PAY_KEY'),
			"merchant_id": "runformoneytw2022_CTBC",
			"details":"TapPay Test",
			"amount": orderData["order"]["price"],
			"cardholder": {
				"phone_number": orderData["contact"]["phone"],
				"name": orderData["contact"]["name"],
				"email": orderData["contact"]["email"],
			},
			"remember": True
			}

			r = requests.post(url, headers = headers, data=json.dumps(data)).json()
			# print("r:",r)
			if r["status"]==0:
				print("payment success.")
				updateSql="UPDATE triporder SET status=1 WHERE number="+number+""
				updateResult=updateOrderData(updateSql)
				# print(updateResult)
				# 付款成功，刪掉預定行程
				sql="DELETE FROM booking"
				dbDelete(sql)
				return jsonify({
					"data": {
						"number": number,
						"payment": {
						"status": 0,
						"message": "付款成功"
						}
					}
					}),200

			else:
				print("payment failed.")
				return jsonify({
					"data": {
						"number": number,
						"payment": {
						"status": 1,
						"message": "付款失敗"
						}
					}
					}),200


@app.route('/api/order/<orderNumber>',methods=["GET"])
def getOrder(orderNumber):
	if session == {}:
		print("session中無使用者")
		return jsonify({"error": True,"message": "未登入系統，拒絕存取"}),403
	else:
		print("session有使用者")
		# sql="SELECT number,trip,contact,status FROM triporder WHERE number="+orderNumber+""
		sql="SELECT number,trip,contact,status FROM triporder WHERE number="+orderNumber+""
		getOrder=dbConnectOne(sql)
		# print("getOrder:",getOrder[0],"1是:",getOrder[1],"1type:",type(getOrder[1]),"2是:",getOrder[2],"3是:",getOrder[3])
		# print("測試:",json.jumps(getORder),"測試type:",type(getOrder),"測試2:",json.loads(getORder),"測試type:",type(getOrder))
		# print("測試type:",type(dict(getOrder)))
		newOrder1=eval(getOrder[1])  # tuple=>dict
		newOrder2=eval(getOrder[2])
		# print("測試type:",type(newOrder1))
		getOrderFinal={
			"data": {
				"number": getOrder[0],
				"price": newOrder1["price"],
				"trip":newOrder1["trip"],
				"date": newOrder1["date"],
				"time": newOrder1["time"]
				},
				"contact": newOrder2,
				"status": getOrder[3]
		}
		print("getOrderFinal:",getOrderFinal)
		return jsonify(getOrderFinal),200

# app.run(host='0.0.0.0',port=3000)
app.run(port=3000)