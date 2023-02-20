function validate(input, bool, func, args=[]) {
	if(bool) {
        input.classList.remove('is-invalid')
        input.classList.add('is-valid')
        console.log(input)
        if (func) {
            console.log(func, ...args)
            func(...args)
        }
    } else {
        input.classList.remove('is-valid')
		input.classList.add('is-invalid')
    }
    return bool
}

function subuttdisable(butt, tooltip) {
	butt.ariaDisabled = true
	butt.addEventListener('click', scrollt1sterror)
	if (tooltip) {
		tooltip.enable()
	}
}

function scrollt1sterror() {
// todo
//	const errormsg = document.querySelectorAll('.invalid-feedback:not(:hidden)')
//	if (errormsg) {
//		errormsg[0].scrollIntoView();
//	}
}

function subuttenable(butt, tooltip) {
	butt.ariaDisabled = false
	butt.removeEventListener('click', scrollt1sterror)
	if (tooltip) {
		tooltip.disable()
	}
}

function buttonloading(butt) {
	butt.disabled = true
	butt.innerHTML += '<span class="spinner-border spinner-border-sm text-light ms-2" role="status" aria-hidden="true"></span>'
	// accesibility
	butt.innerHTML += '<span class="visually-hidden">Loading...</span>'
}

datepicktodays = document.querySelectorAll('.datepicker table tr td.today');
Array.from(datepicktodays).forEach(function(today) {
	today.ariaCurrent = 'date';
});
// todo: add aria-selected = 'true' and stop the date picker from removing aria-current when date selected
