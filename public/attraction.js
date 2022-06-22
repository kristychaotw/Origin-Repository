getAttractionData();
// 事件註冊: 半日、全日費率
const morningBtn = document.getElementById("morning");
const eveningBtn = document.getElementById("evening");
const priceTxt = document.getElementById("priceTxt");
morningBtn.addEventListener("click", clickMorningBtn);
eveningBtn.addEventListener("click", clickEveningBtn);
// 事件註冊: 預定行程按紐
const goReservationBtn = document.getElementById("goReservation");
goReservationBtn.addEventListener("click", checkUser);

// 半日遊、全日遊不同費率
function clickMorningBtn() {
  if ((checked = false)) {
    checked = true;
    priceTxt.innerHTML = "新台幣 2000 元";
    eveningBtn.checked = false;
  } else {
    eveningBtn.checked = false;
    priceTxt.innerHTML = "新台幣 2000 元";
  }
}

function clickEveningBtn() {
  if ((checked = false)) {
    checked = true;
    priceTxt.innerHTML = "新台幣 2500 元";
    morningBtn.checked = false;
  } else {
    morningBtn.checked = false;
    priceTxt.innerHTML = "新台幣 2500 元";
  }
}

// 載入景點資料
function getAttractionData() {
  let id = window.location.pathname.split("/")[2];

  fetch(`/api/attraction/${id}`)
    .then((res) => {
      return res.json();
    })
    .then((data) => {
      let idData = data;
      showAttractionData(idData);
    });
}

// 將景點資料呈現在畫面上
function showAttractionData(idData) {
  nameID = document.createTextNode(idData.data.name);
  document.getElementById("name").appendChild(nameID);
  typeID = document.createTextNode(idData.data.category);
  document.getElementById("type").appendChild(typeID);
  mrtID = document.createTextNode(idData.data.mrt);
  document.getElementById("MRT").appendChild(mrtID);
  storyID = document.createTextNode(idData.data.description);
  document.getElementById("story").appendChild(storyID);
  addressID = document.createTextNode(idData.data.address);
  document.getElementById("address").appendChild(addressID);
  transportID = document.createTextNode(idData.data.transport);
  document.getElementById("transport").appendChild(transportID);

  let imgID = null;
  imgID = idData.data.images;

  for (x = 0; x < imgID.length; x++) {
    const imgDiv = document.createElement("div");
    num = x + 1;
    imgDiv.classList.add("slide", "slide" + num + "");
    const img = document.createElement("img");
    img.src = null;
    imgDiv.appendChild(img);
    document.querySelector(".slideContent").appendChild(imgDiv);
    document.querySelector(".slide" + num + ">img").src = imgID[x];
    dot = document.createElement("div");
    dot.textContent = "";
    dot.classList.add("dots", "dot" + num + "");
    document.querySelector(".dot").appendChild(dot);
  }
  carousel();
}

// 輪播
function carousel() {
  // 事件註冊: 輪播事件
  const nextBtn = document.getElementById("next");
  const previousBtn = document.getElementById("previous");
  nextBtn.addEventListener("click", goNext);
  previousBtn.addEventListener("click", goPrevious);
  function checkDotIndex(n) {
    if (n < 1) {
      return dotNum;
    } else if (n > dotNum) {
      return 1;
    } else {
      return n;
    }
  }

  function dotGoNext() {
    dotIndex = dotIndex + 1;
    newDotIndex = checkDotIndex(dotIndex);
    if (newDotIndex > 1) {
      dots[newDotIndex - 1].classList.add("active");
      let preDotIndex = newDotIndex - 1;
      let newPreDotIndex = checkDotIndex(preDotIndex);
      dots[newPreDotIndex - 1].classList.remove("active");
    } else {
      lastDot.classList.remove("active");
      firstDot.classList.add("active");
      dotIndex = 1;
    }
  }
  function dotGoPrevious() {
    dotIndex = dotIndex - 1;
    newDotIndex = checkDotIndex(dotIndex);
    if (newDotIndex < 8) {
      dots[newDotIndex - 1].classList.add("active");
      let nextDotIndex = newDotIndex + 1;
      let newNextDotIndex = checkDotIndex(nextDotIndex);
      dots[newNextDotIndex - 1].classList.remove("active");
    } else {
      lastDot.classList.add("active");
      firstDot.classList.remove("active");
      dotIndex = dotNum;
    }
  }

  function goNext() {
    currentOffset = currentOffset - imgWidth;
    dotGoNext();

    if (currentOffset > widthAll) {
      slide.style.marginLeft = "" + currentOffset + "px";
    } else {
      slide.style.marginLeft = 0;
      currentOffset = 0;
    }
  }

  function goPrevious() {
    currentOffset = currentOffset + imgWidth;
    dotGoPrevious();

    if (currentOffset <= 0) {
      slide.style.marginLeft = "" + currentOffset + "px";
    } else {
      slide.style.marginLeft = "" + (widthAll + imgWidth) + "px";
      currentOffset = widthAll + imgWidth;
    }
  }

  // 輪播點點
  let firstDot = document.querySelector(".dot").firstChild;
  let lastDot = document.querySelector(".dot").lastChild;
  firstDot.classList.add("active");
  let dotNum = document.querySelector(".dot").childElementCount;
  let dotIndex = 1;
  let dots = document.querySelector(".dot").children;

  //  輪播換圖
  let currentOffset = 0;
  const slide = document.getElementById("slideContent");
  // 單張圖片寬度
  let imgWidth = document.querySelector(".slide").getBoundingClientRect().width;
  // slide總寬度
  let slideWidth = document
    .querySelector(".slideContent")
    .getBoundingClientRect().width;
  let widthAll = slideWidth * -1;

  //close loading animation
  document.querySelector(".loaderWrapper").style.display = "none";
  document.body.classList.remove("preload");
}

//=========================景點頁預定行程按紐=========================================

function popLogin() {
  document
    .querySelectorAll(".popUp")
    .forEach((popUp) => popUp.classList.add("active"));
  document.querySelector(".overlay").classList.add("active");
  document.getElementById("Login").style.zIndex = "99";
  document.getElementById("Login").style.opacity = "1";
  document.getElementById("Signup").style.zIndex = "1";
  document.getElementById("Signup").style.opacity = "0";
  msg("");
}

function goBookingPage() {
  window.location.href = "/booking";
}

function priceRate(time) {
  if (time == "morning") {
    // 上午;
    return 2000;
  } else {
    // 下午;
    return 2500;
  }
}

let createBookingStatus = false;
// 將 booking 存入資料庫
function createBooking() {
  const idNum = window.location.pathname.split("/")[2];
  const date = document.getElementById("calendar").value;
  const newdate = date.toString();
  const time = document
    .querySelector('input[type="radio"]:checked')
    .getAttribute("name");
  const price = priceRate(time);

  if (createBookingStatus != true) {
    createBookingStatus == true;
    fetch(`/api/booking`, {
      method: "POST",
      headers: {
        Accept: "application/json",
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        attractionId: idNum,
        date: newdate,
        time: time,
        price: price,
      }),
    })
      .then((res) => {
        return res.json();
      })
      .then((data) => {
        if (data["ok"]) {
          console.log("儲存預定");
        } else {
          console.log(data["message"]);
        }
        createBookingStatus == false;
      })
      .catch((error) => {
        console.log(error);
        createBookingStatus == false;
      });
  } else {
  }
}

let checkUserStatus = false;
// 確認使用者
function checkUser(e) {
  e.preventDefault();
  if (checkUserStatus != true) {
    checkUserStatus = true;
    fetch(`/api/user`)
      .then((res) => {
        return res.json();
      })
      .then((result) => {
        if (result.data == null) {
          popLogin();
        } else {
          checkBookingData();
        }
        checkUserStatus = false;
      });
  } else {
  }
}

function checkBookingData() {
  const date = document.getElementById("calendar").value;
  if (date != "") {
    let selectDate = new Date(date);
    let today = new Date();
    if (selectDate.getTime() > today.getTime()) {
      // 日期可選，呼叫存入預定
      return createBooking();
    } else {
      return alert("日期已過，請選擇新日期");
    }
  } else {
    return alert("日期空白，請重新選擇");
  }
}
