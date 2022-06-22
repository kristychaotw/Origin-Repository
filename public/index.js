// getData()=>showData()
let fetchingIndex = false;

// 函式1 : 執行fetch，變動的page和kw用函式參數代入
function getData(loadPage,KW){

    if(fetchingIndex != true){
    let src=`/api/attractions?page=${loadPage}&keyword=${KW}`
    fetchingIndex = true
    fetch(src)
    .then(response => response.json())
    .then(data => { showData(data)    
    fetchingIndex = false
    })
    }else{
    
    }
}

// 函式2 : 拿到fetch傳回資料，開始做盒子
function showData(data){
    if ( data.data[0] == null){
        document.getElementById("boxGroup").innerHTML="無此景點資料"
    }else{
        let name;
        let MRT;
        let type;
        let img;
        for (let i=0;i<data.data.length;i++){
            name=data.data[i].name
            MRT=data.data[i].mrt
            type=data.data[i].category
            img=data.data[i].images[0]
            id=data.data[i].id

            num=(data.nextPage-1)*12+(i+1)
            const div1=document.createElement("div")
            div1.classList.add("box", "box"+num+"");
            const div2=document.createElement("div")
            div2.classList.add("imgBox", "imgBox"+num+"");
            const div3=document.createElement("div")
            div3.classList.add("txtBox", "txtBox"+num+"");
            const div4=document.createElement("div")
            div4.classList.add("spotName");
            const div5=document.createElement("div")
            div5.classList.add("spotMRT");
            const div6=document.createElement("div")
            div6.classList.add("spotType");
            const aDiv=document.createElement('a')
            aDiv.setAttribute("href",`/attraction/${id}`)
            document.querySelector(".boxGroup").appendChild(aDiv)
            aDiv.appendChild(div1)
            document.querySelector(".box"+num+"").appendChild(div2)
            document.querySelector(".box"+num+"").appendChild(div3)
            document.querySelector(".txtBox"+num+"").appendChild(div4)
            document.querySelector(".txtBox"+num+"").appendChild(div5)
            document.querySelector(".txtBox"+num+"").appendChild(div6)
        


            let newBox =".box"+[(data.nextPage-1)*12+(i+1)]
            let newName = document.createTextNode (name);
            document.querySelector(""+newBox+">.txtBox>.spotName").appendChild(newName)
            let newMRT = document.createTextNode (MRT);
            document.querySelector(""+newBox+">.txtBox>.spotMRT").appendChild(newMRT)
            let newType = document.createTextNode (type);
            document.querySelector(""+newBox+">.txtBox>.spotType").appendChild(newType)
            let imgBox = document.querySelector(""+newBox+">.imgBox")
            imgBox.style.backgroundImage = "url(" + img + ")";
            
            let NP =data.nextPage
            getnP(NP)
            document.querySelector(".loaderWrapper").style.display='none'
            document.body.classList.remove('preload')

        }
    }    
}


// 觀察器
let options = {
    rootMargin:'0px',
    threshold:0.5   // 看到一半的target，就執行callback
}
let callback = (entries, observer) => {
    entries.forEach(entry => {
        newSrc=`/api/attractions?page=${loadPage}&keyword=${userKW}`
        if(loadPage != null){
        getData(loadPage,userKW)
        }else{
            const target = document.getElementById("ft")
            observer.unobserve(target)
        }
    })
    }
let observer = new IntersectionObserver(callback, options)


function getnP(p){
    loadPage = p

    if (loadPage != null) {
        const target = document.getElementById("ft")
        observer.observe(target)
    }else{
        // no data to load
        const target = document.getElementById("ft")
        observer.unobserve(target)
    }
}


//===============================================================================
// 主程式
//===============================================================================
let userKW = ''
let loadPage = 0


// 第一次載入
getData(loadPage,userKW)

// 關鍵字搜尋功能
document.getElementById('srBtn').addEventListener("click",function(){
    userKW = document.getElementById("userKW").value
    getData(0,userKW)
    document.getElementById("boxGroup").innerHTML=''
})




