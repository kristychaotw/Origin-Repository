window.onload = function () {
  document.getElementById("logoutBtnNav").classList.add("active");
  document.getElementById("loginBtnNav").classList.remove("active");
  const deleteBtn = document.getElementById("deleteBtn");
  deleteBtn.addEventListener("click", deleteBooking);
  const logoutBtnNav = document.getElementById("logoutBtnNav");
  logoutBtnNav.addEventListener("click", logout);
  getBooking();
  getUser();
};

function getBooking() {
  fetch(`/api/booking`)
    .then((res) => {
      if (res.ok) {
        return res.json();
      } else if (res.status == 403) {
        window.location.href = "/";
      } else {
        return res.json();
      }
    })
    .then((result) => {
      console.log("fetchbooking:", result);
      showBooking(result);
    });
}
function getUser() {
  fetch(`/api/user`)
    .then((res) => {
      return res.json();
    })
    .then((data) => {
      console.log("fetchUser:", data);
      showUser(data);
    });
}

//==============================資料放到畫面上================================
function showContent(content, className) {
  box = document.createTextNode(content);
  document.querySelector(className).appendChild(box);
}
function showFormValue(content, className) {
  console.log("className:", className);
  document.querySelector(className).value = content;
}

function showBooking(e) {
  console.log("showbooking-e:", e);
  if (e.data == null) {
    document.querySelector(".mainContent").innerHTML =
      "目前沒有任何待預訂的行程";
    document.querySelector(".mainContent").style.marginTop = "35px";
    document.querySelector(".mainContent").style.marginBottom = "40px";
    document.querySelector("footer").style.height = "100vh";
  } else {
    const attraction = e.data.attraction;
    let time = "";
    if (e.data.time == "morning") {
      time = "早上 9 點到下午 4 點";
    } else {
      time = "下午 4 點到晚上 9 點";
    }
    let date = e.data.date;
    let newDate = new Date(date);
    let newDate2 =
      newDate.getFullYear() +
      "-" +
      newDate.getMonth() +
      "-" +
      newDate.getDate();
    document.querySelector(".mainImg").src = attraction.image;
    showContent(attraction.name, ".spot");
    showContent(attraction.address, ".location>span");
    showContent(newDate2, ".date>span");
    showContent(e.data.price, ".price>span");
    showContent(time, ".time>span");
    showContent(e.data.price, ".totalPrice");

    let trip = {
      order: {
        price: e.data.price,
        trip: {
          attraction: {
            id: attraction.id,
            name: attraction.name,
            address: attraction.address,
            image: attraction.image,
          },
        },
        date: newDate2,
        time: e.data.time,
      },
    };
    passTripData(trip);
  }
}

function showUser(e) {
  console.log("showUser-e:", e);
  console.log("e.data:", e.data);
  showContent(e.data.name, ".userName");

  if (document.querySelector(".conName") != null) {
    showFormValue(e.data.name, ".conName");
    showFormValue(e.data.email, ".conEmail");
  }
  let contact = {
    contact: {
      name: e.data.name,
      email: e.data.email,
      phone: null,
    },
  };
  passUserData(contact);

  //close loading animation
  document.querySelector(".loaderWrapper").style.display = "none";
  document.body.classList.remove("preload");
}

//============================刪掉booking==============================
function deleteBooking() {
  fetch(`/api/booking`, {
    method: "Delete",
  })
    .then((res) => {
      return res.json();
    })
    .then((result) => {
      console.log(result);
    });
  window.location.href = window.location.href;
}

//=================================登出====================================
function logout() {
  fetch(`/api/user`, {
    method: "Delete",
  })
    .then((res) => {
      return res.json();
    })
    .then((data) => {
      console.log("logout f: ", data);
      location.reload();
    }); // 重新載入頁面

  document.getElementById("logoutBtnNav").classList.remove("active");
  document.getElementById("loginBtnNav").classList.add("active");
  document.getElementById("logoutBtnNav").addEventListener("click", logout);
}
