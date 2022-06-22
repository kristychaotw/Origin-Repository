//==============================金流==========================
// TPDirect.card.setup(config)
TPDirect.setupSDK(
  124013,
  "app_2kvlG92VXBRFnxJd02qSmMd9OslaGm5CMLZOsoxjp1zva0hpASo96mXD5Rp0",
  "sandbox"
);

TPDirect.card.setup({
  fields: {
    number: {
      element: document.getElementById("card-number"),
      placeholder: "**** **** **** ****",
    },
    expirationDate: {
      element: document.getElementById("card-expiration-date"),
      placeholder: "MM / YY",
    },
    ccv: {
      element: document.getElementById("card-ccv"),
      placeholder: "ccv",
    },
  },
});

const submitButton = document.getElementById("goBooking");

TPDirect.card.onUpdate(function (update) {
  // update.canGetPrime === true
  // --> you can call TPDirect.card.getPrime()
  if (update.canGetPrime) {
    // Enable submit Button to get prime.
    submitButton.removeAttribute("disabled");
    console.log("getPrimeOK");
  } else {
    // Disable submit Button to get prime.
    submitButton.setAttribute("disabled", true);
    console.log("getPrimeNotOK");
  }
});

// call TPDirect.card.getPrime when user submit form to get tappay prime
document.getElementById("bookingForm").addEventListener("submit", onSubmit);
// $('form').on('submit', onSubmit)

let prime = "";
function onSubmit(event) {
  event.preventDefault();

  // 取得 TapPay Fields 的 status
  const tappayStatus = TPDirect.card.getTappayFieldsStatus();

  // 確認是否可以 getPrime
  if (tappayStatus.canGetPrime === false) {
    console.log("can not get prime");
    alert("請完整填寫所有欄位");
    return;
  }

  // Get prime
  TPDirect.card.getPrime((result) => {
    if (result.status !== 0) {
      console.log("get prime error " + result.msg);
      return;
    }
    console.log("get prime 成功，prime: " + result.card.prime);
    prime = result.card.prime;
    createOrder(prime);

    // send prime to your server, to pay with Pay by Prime API .
    // Pay By Prime Docs: https://docs.tappaysdk.com/tutorial/zh/back.html#pay-by-prime-api
  });
}

let contact = {};
let trip = {};

function passUserData(e) {
  console.log("userData:", e);
  contact = e;
}
function passTripData(e) {
  console.log("tripData:", e);
  trip = e;
}

let createOrderStatus = false;
function createOrder(prime) {
  let name = document.getElementById("conName").value;
  let email = document.getElementById("conEmail").value;
  let phone = document.getElementById("conNumber").value;
  if (createOrderStatus != true) {
    createOrderStatus = true;
    fetch(`/api/orders`, {
      method: "POST",
      headers: {
        Accept: "application/json",
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        prime: prime,
        order: trip["order"],
        contact: {
          name: name,
          email: email,
          phone: phone,
        },
      }),
    })
      .then((res) => {
        return res.json();
      })
      .then((result) => {
        console.log(result["data"]["payment"]["status"]);
        if (result["data"]["payment"]["status"] == 0) {
          window.location.href = `/thankyou?number=${result["data"]["number"]}`;
        } else {
          window.alert(result["data"]["payment"]["message"] + "。請重新操作");
        }
        createOrderStatus = false;
      });
  } else {
  }
}
