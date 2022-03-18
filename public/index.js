// 全域變數，檢查fetch執行的狀態
let fetching = false;
console.log("fetching is:",fetching);


// 函式1 : 執行fetch，變動的page和kw用函式參數代入
function getData(loadPage,KW){

    if(fetching != true){
    let src=`/api/attractions?page=${loadPage}&keyword=${KW}`
    // let src="/api/attractions?page="+loadPage+"&keyword="+KW+""
    fetching = true
    fetch(src)
    .then(response => response.json())
    .then(data => { loadData(data)    
    fetching = false
    console.log("完成fetching");
    })
    }else{
        console.log("不做任何事");
    // fetching = false
    }
}

// 函式2 : 拿到fetch傳回資料，開始做盒子
function loadData(data){
    console.log("nextPate:",data.nextPage)
    console.log("API回傳:",data);
    // console.log("長度:",data.data.length);
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
            //新增紀錄id
            id=data.data[i].id
            // console.log("會使用的資料:",name,MRT,type,img,id);

            // 做盒子
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
            // 多做一個a，設href為/id，append到.boxGroup，把做好的盒子放進去
            const aDiv=document.createElement('a')
            aDiv.setAttribute("href",`/attraction/${id}`)
            document.querySelector(".boxGroup").appendChild(aDiv)
            aDiv.appendChild(div1)
            document.querySelector(".box"+num+"").appendChild(div2)
            document.querySelector(".box"+num+"").appendChild(div3)
            document.querySelector(".txtBox"+num+"").appendChild(div4)
            document.querySelector(".txtBox"+num+"").appendChild(div5)
            document.querySelector(".txtBox"+num+"").appendChild(div6)
            // console.log("做好的盒子:",div1);
        


            // 資料塞到盒子
            let newBox =".box"+[(data.nextPage-1)*12+(i+1)]
            // console.log('this is newBox',newBox)
            let newName = document.createTextNode (name);
            document.querySelector(""+newBox+">.txtBox>.spotName").appendChild(newName)
            let newMRT = document.createTextNode (MRT);
            document.querySelector(""+newBox+">.txtBox>.spotMRT").appendChild(newMRT)
            let newType = document.createTextNode (type);
            document.querySelector(""+newBox+">.txtBox>.spotType").appendChild(newType)
            let imgBox = document.querySelector(""+newBox+">.imgBox")
            // console.log("this is imgBox:",imgBox);
            imgBox.style.backgroundImage = "url(" + img + ")";
            // console.log("final url:",imgBox);
            
            // 把NextPage資訊傳回去
            let NP =data.nextPage
            // console.log("傳回去的NP:",NP);
            getnP(NP)
        }
    }    
}


// 觀察器
let options = {
    // root: document.querySelector("scrollArea"),
    rootMargin:'0px',
    threshold:0.5   // 看到一半的target，就執行callback
}
let callback = (entries, observer) => {
    entries.forEach(entry => {
        console.log("IO works");
        newSrc=`/api/attractions?page=${loadPage}&keyword=${userKW}`
        console.log("loadPage使用:",loadPage,"kw:",userKW);
        if(loadPage != null){
        getData(loadPage,userKW)
        }else{
            const target = document.getElementById("ft")
            observer.unobserve(target)
        }
    })
    }
let observer = new IntersectionObserver(callback, options)



//===============================================================================
// 主程式
//===============================================================================
let userKW = ''
console.log("目前的userKW:",userKW);

let loadPage = 0
console.log("目前的要載入的page:",loadPage);



// 第一次載入
getData(loadPage,userKW)

// 關鍵字搜尋
const srBtn = document.getElementById('srBtn')
srBtn.addEventListener("click",function(){
    userKW = document.getElementById("userKW").value
    console.log('userKW:',userKW);
    // console.log('srBtn:',srBtn);
    // 呼叫getData，傳入關鍵字
    getData(0,userKW)
    // 清空畫面
    document.getElementById("boxGroup").innerHTML=''
})

// 判斷: 如果nP不是空值，代表有下一頁，加上捲動觀察器，開始製作div跟載入下頁資料
function getnP(p){
    loadPage = p
    console.log("下一頁:", loadPage );

    if (loadPage != null) {
        const target = document.getElementById("ft")
        observer.observe(target)
    }else{
        console.log("no data to load");
        const target = document.getElementById("ft")
        observer.unobserve(target)
    }
}
