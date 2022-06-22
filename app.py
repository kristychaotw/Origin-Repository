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
	p=int(page or 0) 
	kw=request.args.get("keyword",None)

	col="id,name,category,description,address,transport,mrt,latitude,longitude,images"
	
	def pick12Row(p):
		numsofRows=dbConnect("SELECT COUNT(*) FROM spotinfo10")
		nokwLastPage=numsofRows[0][0]//12

		nokwSelect="SELECT "+col+" FROM spotinfo10 ORDER BY id LIMIT 12 offset"+" "+str(p*12)
		nokwDB=dbConnect(nokwSelect)
		spotData=[]
		for n in range(0,len(nokwDB)):
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
		result = [p+1,spotData,nokwLastPage]
		return (result)
		

	
	def pick12RowKW(p):
		numsofRows=dbConnect("SELECT COUNT(*) FROM spotinfo10 WHERE name LIKE '%"+kw+"%'")
		KWlastPage=numsofRows[0][0]//12
		

		kwSelect="SELECT "+col+" FROM spotinfo10 WHERE name LIKE '%"+kw+"%'" + " LIMIT 12 offset"+" "+str(p*12)
		kwDB=dbConnect(kwSelect)

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
		dataPnKW = [p+1,kwspotData,KWlastPage]
		return (dataPnKW)
		
	


# 判斷 1-1 : kw有輸入值
	if kw != None:
		dataPnKW=pick12RowKW(p)
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
	print("id為:",attractionID,"id換數字",(int(attractionID)))
	numsofRows=dbConnect("SELECT COUNT(*) FROM spotinfo10")
	
	# 判斷 1 : 輸入值為整數
	if int(attractionID):
		# 判斷 2 : 輸入值為有效整數 (非0、非超過資料筆數)
		if int(attractionID) != 0 and int(attractionID) <= numsofRows[0][0]:
			idSelect="SELECT "+col+" FROM spotinfo10 WHERE id = "+attractionID+""
			dataDBId=dbConnect(idSelect)
		
			for x in dataDBId:
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
	message={"error": True,"message": msg}
	return jsonify(message), 400


@app.errorhandler(500)
def page_not_found(error):
	msg=request.args.get("message","500自訂的錯誤訊息")
	message={"error": True,"message":msg}
	return jsonify(message), 500



#======================================= Member System APIs ===============================================
# 註冊 post  
@app.route("/api/user", methods=['POST'])	
def createUser():
	data=request.get_json()
	name=data['name']
	email=data['email']
	password=data['password']

	checkUser=dbConnect("SELECT name FROM member WHERE name="+"'"+name+"'")
	
	if len(checkUser) != 0: # db裡面有資料
		for i in checkUser: 
			if name == i[0]: # 有資料且有符合
				print("資料庫裡有:"+name+"")
				return jsonify({"error": True,"message": "帳號已經被註冊"})
			else: # 有資料但不符合 user
				dbConnect_insert(name,email,password)
				print("已將"+name+"資料存入資料庫")
				return  jsonify({"ok": True})
				# return redirect ("/")
	else: # db裡面沒有資料
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
	n=dbConnectOne("SELECT COUNT(*) FROM triporder")[0]
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
			"merchant_id": os.environ.get('MERCHANT_ID'),
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
			print("付款資訊:",r)
			if r["status"]==0:
				print("payment success.")
				updateSql="UPDATE triporder SET status=1 WHERE number="+number+""
				updateResult=updateOrderData(updateSql)
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
		sql="SELECT number,trip,contact,status FROM triporder WHERE number="+orderNumber+""
		getOrder=dbConnectOne(sql)
		newOrder1=eval(getOrder[1])  # tuple=>dict
		newOrder2=eval(getOrder[2])
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