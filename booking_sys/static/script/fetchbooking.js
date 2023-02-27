const csrf = document.querySelector('meta[name="csrf-token"]').getAttribute('content');
var delbuttons = document.querySelectorAll('button.delete');

if (delbuttons) {
	delbuttons.forEach(function(delbut){
	    delbut.addEventListener('click', function(event){
	        event.stopPropagation()
	        cancel(this.dataset.link, makenoti())
	    });
	});
}

const resendlink = document.getElementById('resend')

if (resendlink) {
	resendlink.addEventListener('click', function(){
		buttonloading(this);
		resend(location.href, this.parentElement);
	});
}

function resend(link, noti) {
	let data = new FormData()
	data.append("action", "mail")
	fetch(link, {
		method: 'POST',
		headers: {'X-CSRF-TOKEN': csrf},
		body: data
	})
	.then(response => response.text())
	.then(msg => {
		notifying(noti, msg)
	})
	.catch(error => {
		console.error(error);
		notifying(noti,
		'Booking email failed to send.<button class="btn btn-link btn-sm link-light ms-2" id="resend">Retry?</button>')
	});
}

function cancel(link, noti) {
    if (confirm('Bookings are non-refundable. Do you stiil want to cancel?')) {
        fetch(link, {
		    method: 'DELETE',
		    headers: {
		        'Content-Type': 'application/json',
		        'X-CSRF-TOKEN': csrf
		    }
		})
		.then(response => window.location = response.url)
		.catch((error) => {
		    notifying(makenoti('noti'), 'Sorry, cancel failed. <button class="btn btn-link btn-sm link-light ms-2">Retry?</button>')
		});
	}
}
