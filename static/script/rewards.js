document.getElementById('rewardSubmit').addEventListener('click', () => {
    if (document.getElementById('reward').value != '') alert(`Redeemed points for: ${document.getElementById("reward").value} voucher!`)
})

// Claim Reward Algorithm
var customerPoints = parseInt(document.getElementById('custPoints').textContent.replace('Current Points: ', ''))

for (i in pointsList) {
    if (customerPoints >= pointsList[i]) document.getElementById(`${pointsList[i]}points`).style.display = 'block'
}
if (customerPoints < pointsList[0]) document.getElementById('notEnoughPoints').style.display='block'
// End of file