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

function onBookingPage() {
  window.location.href = "/booking";
}

// 導覽列預定行程按鈕
document
  .getElementById("bookingBtnNav")
  .addEventListener("click", function (e) {
    e.preventDefault();
    fetch(`/api/user`)
      .then((res) => {
        return res.json();
      })
      .then((result) => {
        console.log(result);
        if (result.data == null) {
          popLogin();
        } else {
          onBookingPage();
        }
      });
  });
