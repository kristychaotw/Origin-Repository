function popLogin(){
    document.querySelectorAll(".popUp").forEach(popUp => popUp.classList.add("active"))
    document.querySelector(".overlay").classList.add("active")
    document.getElementById("Login").style.zIndex='99'
    document.getElementById("Login").style.opacity='1'
    document.getElementById("Signup").style.zIndex='1'
    document.getElementById("Signup").style.opacity='0'
    msg("")
}



function onBookingPage(){
    window.location.href = '/booking'
}


// 導覽列預定行程按鈕
document.getElementById("bookingBtnNav").addEventListener("click",function(e){
    e.preventDefault()
    fetch(`/api/user`)
    .then(res=> {
        return res.json()
    }).then(result => {
        console.log(result)
        if(result.data==null){
            popLogin()
        }else{
            onBookingPage()
        }
    })

})



//===============景點頁預定行程按紐=========================================

function popLogin(){
    document.querySelectorAll(".popUp").forEach(popUp => popUp.classList.add("active"))
    document.querySelector(".overlay").classList.add("active")
    document.getElementById("Login").style.zIndex='99'
    document.getElementById("Login").style.opacity='1'
    document.getElementById("Signup").style.zIndex='1'
    document.getElementById("Signup").style.opacity='0'
    msg("")
}

function createBooking(){
    const idNum=window.location.pathname.split('/')[2]
    const date=document.getElementById("calendar").value
    const time=document.querySelector('input[type="radio"]:checked').getAttribute('name')
    let f = (time) => {
                    if(time == "morning"){
                        console.log("上午");
                        return 2000
                    }else{
                        console.log("下午");
                        return 2500}
    }

    const price=f(time)
    console.log(idNum,date, time ,price);

    fetch(`/api/booking`,{
        method:'POST',
        headers:{
            'Accept':'application/json',
            'Content-Type': 'application/json'
        },
        body:JSON.stringify({
            'attractionId': idNum,
            'date': date,
            'time': time,
            'price': price
        })
        }).then(res => {
            return res.json()
        }).then(data => {
        if(data["ok"]){
            console.log("儲存預定")
            onBookingPage()
        }else{
            console.log(data["message"])}
        })
        .catch(error => log(error))
}

document.getElementById("goReservation").addEventListener("click",function(e){
    e.preventDefault()
    
    fetch(`/api/booking`)
    .then(res=> {
        if (res.ok){
            return res.json()
        }else if(res.status==403){
            popLogin()
        }
    })
    .then(result => {
        console.log(result)
        createBooking()
        ;
    })
})


