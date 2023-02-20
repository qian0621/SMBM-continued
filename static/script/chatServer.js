var socket = io.connect("http://127.0.0.1:5000");

// connect to chat server
socket.on("connect", function () {
  var customerId = $("#userId").val();
  var mes = "connected";
  var mesObj = { mes, customerId };
  socket.send(mesObj);
});
// receive data from server
socket.on("message", function (data) {
  var customerId = $("#userId").val();
  if (customerId === data.customerId) {
    showDate = moment(data.date).format("lll");
    if (data.from === "customer") {
      var addDiv = $(
        `<div class="outgoing_msg">
            <div class="sent_msg">
            <p>${data.mes}</p><br>
            <span class="time_date"> ${showDate}</span> </div>
          </div>`
      );
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
});
// send message to server
function send() {
  var customerId = $("#userId").val();
  var customerName = $("#userName").val();
  from = "customer";
  var mes = $("#message-input").val();
  var date = new Date();
  var mesObj = { mes, customerId, customerName, from, date };
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
function deleteOldMessage() {
  socket.emit("deletemessage");
  socket.on("newmessage", function (data) {
    $("#out-mes").html('');
   })
}