const notis = document.querySelectorAll('#notis > .noti');
for (noti of notis) {
	notifying(noti);
}

function makenoti(category, content) {
	const main = document.getElementsByTagName('main')[0];
	var notis = main.querySelector('.toast-container#notis');
	if (!notis) {
		notis = document.createElement('div');
		notis.id = "notis"
		notis.classList.add('toast-container', 'position-absolute', 'z-3', 'start-50', 'translate-middle-x')
		main.insertBefore(notis, main.firstElementChild);
	}
	const noti = document.createElement('div');
	noti.classList.add("toast", "align-items-center", "noti")
	if (category === 'noti') {
		noti.classList.add('text-bg-primary')
	} else if (category === 'error') {
		noti.classList.add('text-bg-danger')
	}
	noti.setAttribute('role', "alert")
	noti.setAttribute('aria-live', "assertive")
    noti.setAttribute('aria-atomic', "true")
    noti.setAttribute('data-bs-autohide', "false")
    notis.appendChild(noti)
    const contentwrap = document.createElement('div');
    contentwrap.classList.add("d-flex")
    noti.appendChild(contentwrap)
    const contentdiv = document.createElement('div');
    contentdiv.classList.add("toast-body");
    if (content) {
        contentdiv.innerHTML = content
    }
    contentwrap.appendChild(contentdiv)
    const closebtn = document.createElement('button');
    closebtn.type = "button"
    closebtn.classList.add("btn-close", "me-2", "m-auto")
    closebtn.dataset.bsDismiss = "toast";
    closebtn.setAttribute('aria-label', "Close")
    contentwrap.appendChild(closebtn)
	return contentdiv
}

function notifying(noti, msg) {
	if (msg) {
		noti.innerHTML = msg;
	}
	const notitoast = bootstrap.Toast.getOrCreateInstance(noti, {autohide: false});
	notitoast.show();
}
