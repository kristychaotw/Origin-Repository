# from asyncio.windows_events import NULL
from typing import final
from flask import *
from flask import jsonify
app=Flask(__name__)
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


#=============================================================

import mysql.connector
import boto3
import json

client=boto3.client('secretsmanager')
response=client.get_secret_value(SecretId='conSQL')

secretDict=json.loads(response['SecretString'])
mydb = mysql.connector.connect(
    host=secretDict['host'],
    user=secretDict['username'],
    password=secretDict['password'],
    database=secretDict['dbname']
)
print(mydb)
mycursor=mydb.cursor()

#========================================原版=========================================

# 資料庫連線
# import mysql.connector
# import os

# user=os.environ.get('DB_USER')
# password=os.environ.get('DB_PWD')
# print(user,password)

# mydb = mysql.connector.connect(
#     host="database-1.cohxynft1tdv.us-east-1.rds.amazonaws.com",
#     # user=os.environ['DB_USER'],
#     # password=os.environ['DB_PWD'],
#     user=os.environ.get('DB_USER'),
#     password=os.environ.get('DB_PWD'),
#     database="travelSite"
# )
# print(mydb)
# mycursor=mydb.cursor()

#=========================================原版結束=============================

# APIs
@app.route("/api/attractions")
def attractionsAPI():
	page=request.args.get("page",None)
	p=int(page or 0)
	kw=request.args.get("keyword",None)
	col="id,name,category,description,address,transport,mrt,latitude,longitude,images"
	print("搜尋字串結果:",p,kw)


	def pick12Row(p):
		# mycursor.execute("select count(*) from spotInfo10 ORDER BY id LIMIT 12")
		# print(list(mycursor))
		nokwSelect="SELECT "+col+" FROM spotInfo10 ORDER BY id LIMIT 12 offset"+" "+str(p*12)
		mycursor.execute(nokwSelect)
		nokwDB=mycursor.fetchall()
		# print("頁數:",p,"關鍵字:",kw)
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
		result = {"nextPage": p+1,"data":spotData}
		# print("裡面的result:",result)
		return (result)


	def pick12RowKW(p):
		kwSelect="SELECT "+col+" FROM spotInfo10 WHERE name LIKE '%"+kw+"%'" + " LIMIT 12 offset"+" "+str(p*12)
		print(kwSelect)
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
		result = {"nextPage": p+1,"data":kwspotData}
		return (result)


	if kw != None:
		
		finalData=pick12RowKW(p)
		return jsonify(finalData)

		
	else:
		finalData=pick12Row(p)
		return jsonify(finalData)



@app.route("/api/attraction/<attractionID>")
def attractionAPI(attractionID):
	col="id,name,category,description,address,transport,mrt,latitude,longitude,images"
	# print("id為:",attractionID,"id換數字",(int(attractionID)))
	mycursor.execute("SELECT COUNT(*) FROM spotInfo10")
	numsofRows=mycursor.fetchone()
	# print("資料筆數:",numsofRows[0],type(numsofRows[0]))
	
	# 判斷 1 : 輸入值為整數
	if int(attractionID):
		# 判斷 2 : 輸入值為有效整數 (非0、非超過資料筆數)
		if int(attractionID) != 0 and int(attractionID) <= numsofRows[0]:
			idSelect="SELECT "+col+" FROM spotInfo10 WHERE id = "+attractionID+""
			mycursor.execute(idSelect)
			dataDBId=mycursor.fetchall()
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
	message={"error": True,"message": "400自訂的錯誤訊息"}
	return jsonify(message), 400


@app.errorhandler(500)
def page_not_found(error):
	message={"error": True,"message": "500自訂的錯誤訊息"}
	return jsonify(message), 500

app.run(host='0.0.0.0',port=3000)