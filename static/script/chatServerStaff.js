var socket = io.connect("http://127.0.0.1:5000");
socket.on("connect", function () {
  let customerId = "all";
  var mes = "connected";
  var mesObj = { mes, customerId };
  socket.send(mesObj);
});
peopleList = [];
socket.on("message", function (data) {
  peopleList = data;
  console.log(data)
  
  try {
    let plist = "";
    data.map((value) => {
      if (value.customerId != 0) {
        showDate = moment(value.date).startOf("hour").fromNow();
        plist =
          plist +
          `
          <div onclick='selectCustomer(${value.customerId})' id='${value.customerId}' class="chat_list all">
            <div class="chat_people">
              <div class="chat_img"> 
                <img src="https://ptetutorials.com/images/user-profile.png" alt="sunil"> 
              </div>
              <div class="chat_ib">
                <h5>${value.customerName} <span class="chat_date">${showDate}</span></h5>
                <p>${value.mes}</p>
              </div>
            </div>
          </div>
      `;
      }
    });
    $("#chat-people").html(plist);
  } catch (err) {
    if (data.customerId == customer) {
      showDate = moment(data.date).format("lll");
      if (data.from !== "customer") {
        if (0 != data.customerId) {
          var addDiv = $(
            `<div class="outgoing_msg">
            <div class="sent_msg">
            <p>${data.mes}</p><br>
            <span class="time_date"> ${showDate}</span> </div>
          </div>`
          );
        }
      } else {
        var addDiv = $(`
        <div class="incoming_msg">
            <div class="incoming_msg_img"> <img src="https://ptetutorials.com/images/user-profile.png" alt="sunil"> </div>
              <div class="received_msg">
                <div class="received_withd_msg">
                  <p>${data.mes}</p>
                  <span class="time_date">${showDate}</span>
                </div>
            </div>
          </div>
        `);
      }
      $("#out-mes").append(addDiv);
      $("#out-mes").animate({ scrollTop: 100000 }, 1);
    }
  }
});

let customer = 0;
let customerName = '';

function selectCustomer(customerId) {
  $(".all").removeClass("active_chat");
  $(`#${customerId}`).addClass("active_chat");
  customer = customerId;
  
  socket.emit("forgetmessage", customerId);
  socket.on("oldmessage", function (data) {
    let mlist = "";
    data.map((value) => {
      if (value.from !== "customer") {
        mlist =
          mlist +
          `<div class="outgoing_msg">
            <div class="sent_msg">
            <p>${value.mes}</p><br>
            <span class="time_date"> ${showDate}</span> </div>
          </div>`;
      } else {
        mlist =
          mlist +
          `
        <div class="incoming_msg">
            <div class="incoming_msg_img"> <img src="https://ptetutorials.com/images/user-profile.png" alt="sunil"> </div>
              <div class="received_msg">
                <div class="received_withd_msg">
                  <p>${value.mes}</p>
                  <span class="time_date">${showDate}</span>
                </div>
            </div>
          </div>
        `;
      }
    });
    $("#out-mes").html(mlist);
    $("#out-mes").animate({ scrollTop: 100000 }, 1);
  });
}

function send() {
  let customerId = customer.toString();
  from = "staff";
  var mes = $("#message-input").val();
  var date = new Date();
  var mesObj = { mes, customerId, from, date };
  socket.send(mesObj);
  $("#message-input").val("");
}

var input = document.getElementById("message-input");
input.addEventListener("keypress", function (event) {
  if (event.key === "Enter") {
    event.preventDefault();
    document.getElementById("send").click();
  }
});

document.querySelector("#filter").addEventListener("keyup", function () {
  let name = $("#filter").val();
  let result = peopleList.filter((val) => val.customerName.includes(name));

  let plist = "";
  result.map((value) => {
    showDate = moment(value.date).startOf("hour").fromNow();
    plist =
      plist +
      `
          <div onclick='selectCustomer(${value.customerId})' id='${value.customerId}' class="chat_list all">
            <div class="chat_people">
              <div class="chat_img"> 
                <img src="https://ptetutorials.com/images/user-profile.png" alt="sunil"> 
              </div>
              <div class="chat_ib">
                <h5>${value.customerName} <span class="chat_date">${showDate}</span></h5>
                <p>${value.mes}</p>
              </div>
            </div>
          </div>
      `;
  });
  $("#chat-people").html(plist);
});


