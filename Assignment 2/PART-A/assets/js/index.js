let currentPage = "aboutdiv";
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

onStart();