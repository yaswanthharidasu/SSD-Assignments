let currentPage = "educationdiv";
let divs = ["aboutdiv", "educationdiv", "projectsdiv", "workdiv"];

function onStart() {
	for (let i = 0; i < divs.length; i++) {
		if (divs[i] === currentPage)
			document.getElementById(divs[i]).style.display = "block";
		else document.getElementById(divs[i]).style.display = "none";
	}
}

function loadPages(page) {
	document.getElementById(currentPage).style.display = "none";
	currentPage = page.id + "div";
	document.getElementById(currentPage).style.display = "block";
}

function openMenu() {
	console.log("Menu opened");
	var menu = document.getElementById("menu");

	if (menu.classList.contains("open")) {
		menu.classList.remove("open");
	} else {
		menu.classList.add("open");
	}
}

function closeMenu() {
	console.log("Menu closed");
	var menu = document.getElementById("menu");
	menu.classList.remove("open");
}

function refreshTime() {
	var refresh = 1000; // Refresh rate in milli seconds
	mytime = setTimeout("displayTime()", refresh);
}

function displayTime() {
	var today = new Date();
	var date =
		today.getDate() +
		"/" +
		(today.getMonth() + 1) +
		"/" +
		today.getFullYear();
	var currentHours = ("0" + today.getHours()).substr(-2);
	var currentMins = ("0" + today.getMinutes()).substr(-2);
	var currentSecs = ("0" + today.getSeconds()).substr(-2);
	var time = currentHours + ":" + currentMins + ":" + currentSecs;
	var dateTime = date + " " + time;
	console.log(dateTime);
	var id = document.getElementById("display-date-time");
	id.innerHTML = dateTime;
	refreshTime();
}

displayTime();

onStart();
