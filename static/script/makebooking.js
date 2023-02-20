const dates = document.getElementsByClassName('timeslots')
const slots = document.querySelectorAll("input[name='slot']");
const booknow = document.getElementById("booknow");
const sloterrordiv = document.getElementById('slot-error')
const dateinput = document.getElementById('date')
const typeinput = document.getElementById('type')
const whydisabled = new bootstrap.Tooltip(booknow)

typeinput.addEventListener("change", function() {
	validate(this, this.value === 'Guided Tour', showslots);
});

function pickedate() {
	validate(
		dateinput,
		(dateinput.validity.valid && availdates.includes(dateinput.value)),
		function() {
			calender.datepicker('update', dateinput.value);
			showslots()
		}
	);
}

calender.on('changeDate', function() {
    dateinput.value = calender.datepicker('getFormattedDate')
    pickedate()
});

dateinput.addEventListener("change", pickedate)

function showslots() {
	const type = typeinput.value
	const selecteddate = dateinput.value
	Array.from(dates).forEach(function(date) {
	    date.hidden = true
	});
	slots.forEach(function(slot) {
		slot.checked = false
	})
	subuttdisable(booknow, whydisabled)
	if (typeinput.classList.contains('is-valid') && dateinput.classList.contains('is-valid')) {
		const dayslot = document.getElementById(selecteddate)
		dayslot.hidden = false;
	}
}

slots.forEach(function(slot) {
    slot.addEventListener("change", function() {
        if (this.checked) {
            if (sloterrordiv) {
			    sloterrordiv.style.display = null;
			}
            subuttenable(booknow, whydisabled)
        } else {
            subuttdisable(booknow, whydisabled)
        }
    });
});
