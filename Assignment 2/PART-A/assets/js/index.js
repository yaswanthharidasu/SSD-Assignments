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
