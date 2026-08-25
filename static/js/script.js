document.addEventListener("DOMContentLoaded", function () {
    const menuButton = document.getElementById("menu-button");
    const navLinks = document.getElementById("nav-links");
    const yearSpan = document.getElementById("current-year");

    if (yearSpan) {
        yearSpan.textContent = new Date().getFullYear();
    }

    const dateOfBirth = document.getElementById("date-of-birth");
    const appointmentDate = document.getElementById("appointment-date");
    const today = new Date().toISOString().split("T")[0];

    if (dateOfBirth) {
        dateOfBirth.max = today;
    }

    if (appointmentDate) {
        appointmentDate.min = today;
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
