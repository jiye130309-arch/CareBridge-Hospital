document.addEventListener("DOMContentLoaded", function () {
    const menuButton = document.getElementById("menu-button");
    const navLinks = document.getElementById("nav-links");
    const yearSpan = document.getElementById("current-year");

    if (yearSpan) {
        yearSpan.textContent = new Date().getFullYear();
    }

    const dateOfBirth = document.getElementById("date-of-birth");

    function toLocalYMD(value) {
        const year = value.getFullYear();
        const month = String(value.getMonth() + 1).padStart(2, "0");
        const day = String(value.getDate()).padStart(2, "0");
        return year + "-" + month + "-" + day;
    }

    const todayLocal = toLocalYMD(new Date());

    if (dateOfBirth) {
        dateOfBirth.max = todayLocal;
    }

    if (!menuButton || !navLinks) {
        return;
    }

    menuButton.addEventListener("click", function () {
        const isOpen = navLinks.classList.toggle("is-open");
        menuButton.setAttribute("aria-expanded", isOpen);
    });

    navLinks.querySelectorAll("a").forEach(function (link) {
        link.addEventListener("click", function () {
            navLinks.classList.remove("is-open");
            menuButton.setAttribute("aria-expanded", "false");
        });
    });
});
