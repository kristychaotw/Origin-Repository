import mysql.connector
import os

mydb = mysql.connector.connect(
    host="localhost",
    user=os.environ.get('DB_USER'),
    password=os.environ.get('DB_PWD'),
    database="travelSite"
)
print(mydb)

mycursor=mydb.cursor()

# 創建資料庫&資料表&插入值 #刪除資料表
# mycursor.execute("CREATE DATABASE travelSite")
# mycursor.execute("CREATE TABLE spotInfo10 (id bigint PRIMARY KEY AUTO_INCREMENT, name VARCHAR(255) NOT NULL, category VARCHAR(255) NOT NULL, description TEXT NOT NULL, address VARCHAR(255) NOT NULL, transport TEXT NOT NULL, mrt VARCHAR(255), latitude DECIMAL( 10, 8 ) NOT NULL, longitude DECIMAL( 11, 8 ) NOT NULL, images TEXT NOT NULL)")
# mycursor.execute("INSERT INTO spotInfo10 (name, category, description, address, transport, mrt, latitude, longitude) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)",(spotInfo["stitle"],spotInfo["CAT2"],spotInfo["xbody"],spotInfo["address"],spotInfo["info"],spotInfo["MRT"],spotInfo["latitude"],spotInfo["longitude"]))
# mycursor.execute("CREATE TABLE spotImg (id bigint PRIMARY KEY AUTO_INCREMENT, images VARCHAR(255), name VARCHAR(255) NOT NULL, time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP)")
# mycursor.execute("INSERT INTO spotImg (images, name) VALUES (%s,%s)",(spotInfo["file"],spotInfo["stitle"])
# mycursor.execute("DROP TABLE spotInfo10")
# mydb.commit()
# mydb.close()

# 確認表內資料
# mycursor.execute("DESCRIBE spotInfo10")
# data=mycursor.execute("SELECT * FROM spotInfo10")
# print(data.COLUMN_NAME)
# mycursor.execute("SELECT * FROM spotImg")
# checklist=mycursor.fetchall()
# print("表:",checklist)

import json

with open ("taipei-attractions.json","r",encoding="utf-8") as f:
    p=json.load(f)
    plist=p["result"]["results"]
    # print("plist:",plist["result"]["results"])
    # print("plist-len:", len(plist))   # plist有58個項目,資料列別為list
    
   
# 需要資料為 name, category, description, address, transport, mrt, latitude, longitude, images
# JSON名稱   stitle, CAT2  , xbody      , address, info     , MRT, latitude, longitude, file
   
    spotInfo=[]
    imgList=[]
    for i in range (0,58):
        spotInfo=plist[i]["stitle"],plist[i]["CAT2"],plist[i]["xbody"],plist[i]["address"],plist[i]["info"],plist[i]["MRT"],plist[i]["latitude"],plist[i]["longitude"],plist[i]["file"]
        img=plist[i]["file"] 
        imgNew=img.replace("https",",https").lower() #.split(',') # 將urls轉換成list
        print("img結果:",imgNew)
        
        sqlData=spotInfo[0],spotInfo[1],spotInfo[2],spotInfo[3],spotInfo[4],spotInfo[5],spotInfo[6],spotInfo[7],imgNew
        # mycursor.execute("INSERT INTO spotInfo10 (name, category, description, address, transport, mrt, latitude, longitude, images) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)",(sqlData))
        # mydb.commit()

# mydb.close()

 
