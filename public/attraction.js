// 半日遊、全日遊不同費率
const btn1=document.getElementById("morning")
const btn2=document.getElementById("evening")
const priceTxt=document.getElementById("priceTxt")

btn1.addEventListener("click",btn1Click)
btn2.addEventListener("click",btn2Click)

function btn1Click(){
    if ( checked = false ){
        checked = true;
        priceTxt.innerHTML = "新台幣 2000 元";
        btn2.checked = false;
    }else{
        btn2.checked = false;
        priceTxt.innerHTML = "新台幣 2000 元";
    }
}

function btn2Click(){
    if ( checked = false ){
        checked = true;
        priceTxt.innerHTML = "新台幣 2500 元";
        btn1.checked = false;
    }else{
        btn1.checked = false;
        priceTxt.innerHTML = "新台幣 2500 元";
    }
}

// 載入Fetch資料
let idData=null;
let id = window.location.pathname;
const src =`/api${id}`
async function initData(){
    const response = await fetch(src)
    const result_1 = await response.json()
    idData = result_1
}
async function main(){
    let i = await initData();
    render (i)
}

let imgID = null;
function render(){
nameID=document.createTextNode(idData.data.name)
document.getElementById("name").appendChild(nameID)
typeID=document.createTextNode(idData.data.category)
document.getElementById("type").appendChild(typeID)
mrtID=document.createTextNode(idData.data.mrt)
document.getElementById("MRT").appendChild(mrtID)
storyID=document.createTextNode(idData.data.description)
document.getElementById("story").appendChild(storyID)
addressID=document.createTextNode(idData.data.address)
document.getElementById("address").appendChild(addressID)
transportID=document.createTextNode(idData.data.transport)
document.getElementById("transport").appendChild(transportID)



imgID=idData.data.images
// console.log("imgID:",imgID);

for(x=0;x<imgID.length;x++){
    const imgDiv=document.createElement("div")
    num=x+1
    imgDiv.classList.add("slide","slide"+num+"")
    const img=document.createElement('img')
    img.src=null
    imgDiv.appendChild(img)
    console.log('imgDiv:',imgDiv);
    document.querySelector(".slideContent").appendChild(imgDiv)
    document.querySelector(".slide"+num+">img").src=imgID[x]
    // 圖上小點
    dot=document.createElement('div')
    dot.textContent=""
    dot.classList.add("dots","dot"+num+"")
    document.querySelector(".dot").appendChild(dot)
    
}
}

main()


window.onload = function(){
// 輪播
    // 輪播點點
    const firstDot = document.querySelector('.dot').firstChild
    const lastDot = document.querySelector('.dot').lastChild
    console.log('firstDot:',firstDot);
    firstDot.classList.add("active")
    dotNum = document.querySelector('.dot').childElementCount
    console.log('dotNum:',dotNum);


    // 1. 取得輪播需要數值
    // 單張圖片寬度
    let imgWidth = document.querySelector(".slide").getBoundingClientRect().width
    console.log("imgWidth:",imgWidth);
    // slide總寬度
    let contentWidth = document.querySelector(".slideContent").getBoundingClientRect().width
    console.log("slideContent:",contentWidth);
    let widthAll = contentWidth*(-1)
    console.log("widthAll:",widthAll);
 
    // 2. 註冊輪播事件
    const next = document.getElementById("next")
    const previous = document.getElementById("previous")
    next.addEventListener("click",goNext)
    previous.addEventListener("click",goPrevious)
    
    // 3. 設定操作對象&紀錄位置
    const content = document.getElementById("slideContent")
    let currentOffset = 0;
    let index=1
    activeDot = document.querySelector('.active')
    // console.log('activeDots:',activeDot);
    // nextDot = document.querySelector('.active').nextSibling
    // console.log('next:',nextDot);
    // previousDot = document.querySelector('.active').previousSibling
    // console.log('previous:',previousDot);


    function goNext(){
        activeDot = document.querySelector('.active')
        nextDot = document.querySelector('.active').nextSibling
        previousDot = document.querySelector('.active').previousSibling

        currentOffset = currentOffset - imgWidth
        console.log('右移動:',currentOffset);
        
        if( currentOffset > widthAll ){
            content.style.marginLeft = ""+currentOffset+"px";
            index=index+1
            console.log("現在位置:",currentOffset);
            console.log("index:",index);
            activeDot.classList.remove("active")
            nextDot.classList.add("active")

        }else{
            // content.style.marginLeft = ""+currentOffset+"px";
            content.style.marginLeft = 0;
            currentOffset = 0;
            index=1
            console.log("現在位置:",currentOffset)
            console.log("index:",index);
            activeDot.classList.remove("active")
            firstDot.classList.add("active")
        }
    }
    
    function goPrevious(){
        activeDot = document.querySelector('.active')
        nextDot = document.querySelector('.active').nextSibling
        previousDot = document.querySelector('.active').previousSibling

        currentOffset = currentOffset + imgWidth
        console.log('左移動:',currentOffset);
        
        if( currentOffset <= 0 ){
            content.style.marginLeft = ""+currentOffset+"px";
            index=index-1
            console.log("現在位置:",currentOffset);
            console.log("index:",index);
            activeDot.classList.remove("active")
            previousDot.classList.add("active")
        }else{
            // content.style.marginLeft = ""+currentOffset+"px";
            content.style.marginLeft = ""+(widthAll+imgWidth)+"px" ;
            currentOffset = widthAll + imgWidth;
            index=dotNum;
            console.log("現在位置:",currentOffset)
            console.log("index:",index);
            activeDot.classList.remove("active")
            lastDot.classList.add("active")
        }
    }
}



