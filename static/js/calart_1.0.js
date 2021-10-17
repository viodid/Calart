let degrees = 180;
displaySideBar = false;

function listen() {
    document.querySelector(".button-nav")
        .addEventListener("click", function(){
            document.querySelector(".button-nav").style.transform = `rotate(${degrees}deg)`;
            degrees += 180;
            displayNavbar();
        });
}

function displayNavbar() {
    if (!displaySideBar) {
        document.querySelector(".sidebar").classList.add("show");
        displaySideBar = true;
    } else {
        document.querySelector(".sidebar").classList.remove("show");
        displaySideBar = false;
    }
}

document.addEventListener("DOMContentLoaded", listen);