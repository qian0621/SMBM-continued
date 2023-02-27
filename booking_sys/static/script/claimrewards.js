const addrewardbut = document.getElementById('addrewardbut')
const rewardselect = document.getElementById('rewardselect')
const claimed = document.getElementById('claimed')
const claims = [];

function validate_reward(func, args) {
	validate(rewardselect, availrewards.hasOwnProperty(rewardselect.value), func, args);
}

rewardselect.addEventListener("input", () => validate_reward() );

addrewardbut.addEventListener("click", () => validate_reward(addreward, [rewardselect.value]));

function addreward(id) {
	name = availrewards[id]
	// add reward to cart
	addtocart(false, name, '', id)
	claims.push(id)
	claimed.value = JSON.stringify(claims)
	// remove reward from select
	rewardselect.removeChild(rewardselect.querySelector('option[value="' + id + '"]'));
	rewardselect.classList.remove('is-valid');
	delete availrewards[id];
}

function delreward(id, name) {
	// add reward back
    availrewards[id] = name
    rewardopt = document.createElement('option')
    rewardopt.innerText = name
    rewardopt.value = id
    rewardselect.appendChild(rewardopt)
    // remove from hidden field claimed
    claims.remove(id);
	claimed.value = JSON.stringify(claims);
}

function voucher_amt(voucher, subtotal) {
	const params = new URLSearchParams();
	params.append('voucher', voucher);
	params.append('subtotal', subtotal);
	return fetch(cal_voucher_url + '?' + params.toString())
	    .then(response => response.text())
	    .then(data => {
			console.log(data);
			return parseFloat(data);
	    })
	    .catch(error => {
			console.error(error);
			return 0; // or any other default value
	    });
}
