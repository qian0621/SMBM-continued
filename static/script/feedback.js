// add event listener to the form
const form = document.getElementById("feedback-form");
form.addEventListener("submit", function(event) {
  event.preventDefault();

  // validate form fields
  if (form.name.value === "") {
    alert("Name is required");
    return;
  }
  if (form.email.value === "") {
    alert("Email is required");
    return;
  }
  if (form.feedback.value === "") {
    alert("Feedback is required");
    return;
  }

  // submit form data to the server
  const data = {
    name: form.name.value,
    email: form.email.value,
    feedback: form.feedback.value
  };
  submitFormData(data);
});

function submitFormData(data) {
  // use Fetch API or XMLHttpRequest to submit the data to the server
  // in this example I use fetch API
  fetch("/submit-feedback", {
    method: "POST",
    body: JSON.stringify(data),
    headers: { "Content-Type": "application/json" }
  })
    .then(response => response.json())
    .then(data => {
      alert("Feedback submitted successfully!");
    })
    .catch(error => {
      console.error("Error:", error);
    });
}
