import json

with open ("taipei-attractions.json","r",encoding="utf-8") as f:
    p=json.load(f)
    plist=p["result"]["results"]
    
    for i in plist:
        title=i["stitle"]
        id=i["_id"]
        print(id)
        with open("spotlist.txt","a",encoding="utf-8") as file:
                    file.write(str(id)+""+title+"\n")

    spotInfo=[]
    imgList=[]
    for i in range (0,58):
        imgUrl=spotInfo[8]
        imgUrlList=imgUrl.replace("https",",https").lower().split(',') # 將urls轉換成list
        # print("urllist長度:",len(imgUrlList))
        # print(spotInfo[0],imgUrlList,"類型:",type(imgUrlList))

        for n in range (1,len(imgUrlList)):
            # print(spotInfo[0]+imgUrlList[n])
            sqlData2=spotInfo[0],imgUrlList[n]
            # mycursor.execute("INSERT INTO spotImg (images, name) VALUES (%s,%s)",(sqlData2))
            # mydb.commit()   



# 補充：若需存成文字檔，a => without overwriting
# with open("imgUrl.txt","a",encoding="utf-8") as file:
#     for n in range (1,len(imgUrlList)):
#     file.write(spotInfo[0]+imgUrlList[n])

