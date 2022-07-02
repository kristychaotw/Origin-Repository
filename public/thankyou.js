function getOrder() {
  const orderNum = window.location.href.split("?")[1].split("=")[1];
  document.querySelector(".showOrderNum").innerHTML =
    "您的訂單編號如下：" + orderNum;
  fetch(`/api/order/${orderNum}`)
    .then((res) => {
      return res.json();
    })
    .then((result) => {
      // console.log(result);
    });
  // remove loading animation
  document.querySelector(".loaderWrapper").style.display = "none";
  document.body.classList.remove("preload");
}

getOrder();
