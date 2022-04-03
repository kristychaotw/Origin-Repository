window.onload=function loadBooking(){
    fetch(`/api/booking`)
    .then(res=> {
        if (res.ok){
            return res.json()
        }else if(res.status==403){
            window.location.href='/'
        }else{
            return res.json()
        }
    })
    .then(result => {
        console.log(result)
        showBooking(result)
    })

    document.getElementById("logoutBtnNav").classList.add("active")
    document.getElementById("loginBtnNav").classList.remove("active")


    fetch(`/api/user`)
    .then(res => {
        return res.json()
    }).then(data => {
        showUser(data)
    })
}



//=================================登出====================================
function logout(){
    fetch(`/api/user`,{
        method:"Delete"
    })
    .then(res => {return res.json()})
    .then(data => {
        console.log("logout f: ",data);
        location.reload()}) // 重新載入頁面
}
document.getElementById("logoutBtnNav").classList.remove("active")
document.getElementById("loginBtnNav").classList.add("active")

document.getElementById("logoutBtnNav").addEventListener("click", logout)


//==============================資料放到畫面上================================
function showContent(content,gowhere){
    box=document.createTextNode(content)
    document.querySelector(gowhere).appendChild(box)
}
function showFormValue(content,gowhere){
    document.querySelector(gowhere).value=content
}

function showBooking(e){
    console.log("showbooking-e:",e);
    if(e.data==null){
        document.querySelector(".mainContent").innerHTML="目前沒有任何待預訂的行程"
        document.querySelector(".mainContent").style.marginTop="35px"
        document.querySelector(".mainContent").style.marginBottom="40px"
        document.querySelector("footer").style.height="100vh"
    }else{
        const attraction=e.data.attraction
        let time=""
        if(e.data.time=="morning"){
            time ="早上 9 點到下午 4 點"
        }else{
            time="下午 4 點到晚上 9 點"
        }
        let date=e.data.date
        let newDate=new Date(date)
        let newDate2=newDate.getFullYear()+"-"+newDate.getMonth()+"-"+newDate.getDate()
        console.log("newDate2:",newDate2);
        document.querySelector(".mainImg").src=attraction.image
        showContent(attraction.name,".spot")
        showContent(attraction.address,".location>span")
        showContent(newDate2,".date>span")
        showContent(e.data.price,".price>span")
        showContent(time,".time>span")
        showContent(e.data.price,".totalPrice")
    }
}

function showUser(e){
    showContent(e.data.name,".userName")
    showFormValue(e.data.name,".conName")
    showFormValue(e.data.email,".conEmail")

}

//============================刪掉booking==============================

document.getElementById("deleteBtn").addEventListener("click",function(){
    fetch(`/api/booking`,{
        method:"Delete"
    }).then(res=>{return res.json()
    }).then(result => {
        console.log(result);
    })
    // window.location.reload()
    window.location.href = window.location.href

})


