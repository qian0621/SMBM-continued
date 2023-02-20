//Add event listener to search button
function customerPath() {
    //Get search name
    var search = document.querySelector('#searchBar').value;
    // Assign website path name
    if (search == '') window.location.assign('search');
    else if (window.location.pathname == '/search') window.location.assign(`search/${search}`);
    else window.location.assign(search);
}
document.querySelector('#searchBtn').addEventListener('click', customerPath)

//Add enter key event listener so that enter key is a shortcut of pressing the search button
document.addEventListener('keypress', (e) => { if (e.key == 'Enter') { e.preventDefault(); customerPath(); } })