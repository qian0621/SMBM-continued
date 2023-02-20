let checkbox = document.getElementById("includepast");
let rows = document.querySelectorAll("#bookingsview tbody tr");

checkbox.addEventListener("change", function() {
	let now = new Date();
	Array.from(rows).forEach(function(row) {
		if (checkbox.checked) {
			// show all rows
			row.hidden = false;
		} else {
			let date = new Date(row.children[1].textContent);
			// hide rows for past dates
			if (date < now) {
				row.hidden = true;
			} else {
				row.hidden = false;
			}
		}
	});
});

for (row of rows) {
	row.addEventListener('click', function(){location.assign(this.dataset.link)})
}
