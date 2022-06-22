window.onload = function () {
  document.getElementById("signupBtn").addEventListener("click", register);
  document.getElementById("loginBtn").addEventListener("click", login);
  document.getElementById("logoutBtnNav").addEventListener("click", logout);
  //loading animation
  document.body.classList.add("preload");
  // check if user login
  checkUser();
};

//=============================顯示登入表單==================================
document.getElementById("loginBtnNav").addEventListener("click", function () {
  document
    .querySelectorAll(".popUp")
    .forEach((popUp) => popUp.classList.add("active"));
  document.querySelector(".overlay").classList.add("active");
});

document.querySelectorAll(".closeBtn").forEach((closeBtn) =>
  closeBtn.addEventListener("click", function () {
    document
      .querySelectorAll(".popUp")
      .forEach((popUp) => popUp.classList.remove("active"));
    document.querySelector(".overlay").classList.remove("active");
  })
);

document.getElementById("goLogin").addEventListener("click", function () {
  document.getElementById("Login").style.zIndex = "99";
  document.getElementById("Login").style.opacity = "1";
  document.getElementById("Signup").style.zIndex = "1";
  document.getElementById("Signup").style.opacity = "0";
  msg("");
});

document.getElementById("goSignup").addEventListener("click", function () {
  document.getElementById("Signup").style.zIndex = "99";
  document.getElementById("Signup").style.opacity = "1";
  document.getElementById("Login").style.zIndex = "1";
  document.getElementById("Login").style.opacity = "0";
  msg("");
});

// 登入狀態檢查
function checkUser() {
  fetch(`/api/user`)
    .then((res) => {
      return res.json();
    })
    .then((data) => {
      if (data["data"] == null) {
        document.getElementById("logoutBtnNav").classList.remove("active");
        document.getElementById("loginBtnNav").classList.add("active");
      } else {
        document.getElementById("logoutBtnNav").classList.add("active");
        document.getElementById("loginBtnNav").classList.remove("active");
      }
    });
}

// 註冊
function register(e) {
  e.preventDefault();
  let fnameS = document.getElementById("fnameS").value;
  let femailS = document.getElementById("femailS").value;
  let fpasswordS = document.getElementById("fpwdS").value;
  console.log("使用者註冊輸入:", fnameS, femailS, fpasswordS);

  //Email Regular expression Testing
  emailRule =
    /^\w+((-\w+)|(\.\w+))*\@[A-Za-z0-9]+((\.|-)[A-Za-z0-9]+)*\.[A-Za-z]+$/;

  const validateEmail = (email) => {
    if (email.search(emailRule) != -1) {
      return true;
    } else {
      return false;
    }
  };

  console.log("test:", validateEmail(femailS));

  if (fnameS == "" || femailS == "" || fpasswordS == "") {
    msg("有欄位空白，請重新輸入");
  } else if (validateEmail(femailS) == false) {
    msg("信箱格式錯誤，請重新輸入");
  } else {
    fetch(`/api/user`, {
      method: "POST",
      headers: {
        Accept: "application/json",
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        name: fnameS,
        email: femailS,
        password: fpasswordS,
      }),
    })
      .then((res) => {
        return res.json();
      })
      .then((data) => {
        if (data["ok"]) {
          msg("註冊成功");
        } else {
          msg(data["message"]);
        }
      })
      .catch((error) => log(error));
  }
}

// 登入
function login(e) {
  e.preventDefault();
  let femailL = document.getElementById("femailL").value;
  let fpasswordL = document.getElementById("fpwdL").value;
  console.log("使用者登入輸入:", femailL, fpasswordL);

  if (femailL == "" || fpasswordL == "") {
    msg("有欄位空白，請重新輸入");
  } else {
    fetch(`/api/user`, {
      method: "PATCH",
      headers: {
        Accept: "application/json",
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        email: femailL,
        password: fpasswordL,
      }),
    })
      .then((res) => {
        return res.json();
      })
      .then((data) => {
        if (data["ok"]) {
          msg("登入成功");
          location.reload(); // 重新載入頁面
        } else {
          msg(data["message"]);
        }
      })
      .catch((error) => console.log(error));
  }
}

// form 提示
function msg(p) {
  document.querySelectorAll(".msg").forEach((msg) => (msg.innerHTML = p));
}

// 登出
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
}
