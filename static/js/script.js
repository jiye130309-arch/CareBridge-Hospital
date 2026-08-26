document.addEventListener("DOMContentLoaded", function () {
    const menuButton = document.getElementById("menu-button");
    const navLinks = document.getElementById("nav-links");
    const yearSpan = document.getElementById("current-year");

    if (yearSpan) {
        yearSpan.textContent = new Date().getFullYear();
    }

    function toLocalYMD(value) {
        const year = value.getFullYear();
        const month = String(value.getMonth() + 1).padStart(2, "0");
        const day = String(value.getDate()).padStart(2, "0");
        return year + "-" + month + "-" + day;
    }

    function getToday() {
        const today = new Date();
        today.setHours(0, 0, 0, 0);
        return today;
    }

    const dateOfBirth = document.getElementById("date-of-birth");
    if (dateOfBirth) {
        dateOfBirth.max = toLocalYMD(getToday());
    }

    setupAppointmentDatePicker();

    if (menuButton && navLinks) {
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
    }

    function eventElement(event) {
        if (event.target && event.target.nodeType === 1) {
            return event.target;
        }
        return event.target && event.target.parentElement ? event.target.parentElement : null;
    }

    function setupAppointmentDatePicker() {
        const input = document.getElementById("appointment-date");
        const calendar = document.getElementById("appointment-calendar");
        const monthLabel = document.getElementById("date-picker-month");
        const daysContainer = document.getElementById("date-picker-days");
        const prevButton = document.getElementById("date-picker-prev");
        const nextButton = document.getElementById("date-picker-next");
        const pickerField = input ? input.closest(".date-picker-field") : null;
        if (!input || !calendar || !monthLabel || !daysContainer || !prevButton || !nextButton || !pickerField) {
            return;
        }

        const DAYS_UNTIL_FIRST_AVAILABLE = 8;
        const startDay = getToday();
        let viewYear = startDay.getFullYear();
        let viewMonth = startDay.getMonth();

        function parseYMD(value) {
            const match = /^(\d{4})-(\d{2})-(\d{2})$/.exec(value);
            if (!match) {
                return null;
            }
            const parsed = new Date(
                Number(match[1]),
                Number(match[2]) - 1,
                Number(match[3])
            );
            return Number.isNaN(parsed.getTime()) ? null : parsed;
        }

        function getFirstAvailableYmd() {
            const firstAvailable = getToday();
            firstAvailable.setDate(
                firstAvailable.getDate() + DAYS_UNTIL_FIRST_AVAILABLE
            );
            return toLocalYMD(firstAvailable);
        }

        function isAvailable(ymd) {
            return ymd >= getFirstAvailableYmd();
        }

        function updateInputColor() {
            input.classList.remove("date-unavailable", "date-available");
            if (!input.value) {
                return;
            }
            if (isAvailable(input.value)) {
                input.classList.add("date-available");
            } else {
                input.classList.add("date-unavailable");
            }
        }

        function setOpen(isOpen) {
            calendar.hidden = !isOpen;
            input.setAttribute("aria-expanded", isOpen ? "true" : "false");
        }

        function shiftMonth(step) {
            const nextMonth = new Date(viewYear, viewMonth + step, 1);
            viewYear = nextMonth.getFullYear();
            viewMonth = nextMonth.getMonth();
            renderCalendar();
        }

        function renderCalendar() {
            const monthStart = new Date(viewYear, viewMonth, 1);
            monthLabel.textContent = monthStart.toLocaleString("en-GB", {
                month: "long",
                year: "numeric",
            });

            const startWeekday = (monthStart.getDay() + 6) % 7;
            const firstAvailableYmd = getFirstAvailableYmd();
            daysContainer.textContent = "";

            for (let index = 0; index < 42; index += 1) {
                const cellDate = new Date(viewYear, viewMonth, 1 - startWeekday + index);
                const ymd = toLocalYMD(cellDate);
                const dayButton = document.createElement("button");
                dayButton.type = "button";
                dayButton.className = "date-picker-day";
                dayButton.textContent = String(cellDate.getDate());
                dayButton.setAttribute("data-date", ymd);

                if (cellDate.getMonth() !== viewMonth) {
                    dayButton.classList.add("is-other-month");
                }
                if (ymd >= firstAvailableYmd) {
                    dayButton.classList.add("is-available");
                } else {
                    dayButton.classList.add("is-unavailable");
                    dayButton.disabled = true;
                    dayButton.setAttribute("aria-disabled", "true");
                }
                if (input.value === ymd) {
                    dayButton.classList.add("is-selected");
                }
                daysContainer.appendChild(dayButton);
            }
        }

        function openCalendar() {
            renderCalendar();
            updateInputColor();
            setOpen(true);
        }

        document.addEventListener("visibilitychange", function () {
            if (document.visibilityState === "visible" && !calendar.hidden) {
                renderCalendar();
                updateInputColor();
            }
        });

        pickerField.addEventListener("click", function (event) {
            event.stopPropagation();
        });

        input.addEventListener("click", function (event) {
            event.stopPropagation();
            openCalendar();
        });

        prevButton.addEventListener("click", function (event) {
            event.stopPropagation();
            shiftMonth(-1);
        });

        nextButton.addEventListener("click", function (event) {
            event.stopPropagation();
            shiftMonth(1);
        });

        daysContainer.addEventListener("click", function (event) {
            event.stopPropagation();
            const el = eventElement(event);
            const dayButton = el && el.closest ? el.closest(".date-picker-day") : null;
            if (!dayButton) {
                return;
            }
            const ymd = dayButton.getAttribute("data-date");
            if (!isAvailable(ymd)) {
                return;
            }
            input.value = ymd;
            updateInputColor();
            setOpen(false);
        });

        document.addEventListener("click", function (event) {
            const el = eventElement(event);
            if (!el || !pickerField.contains(el)) {
                setOpen(false);
            }
        });

        document.addEventListener("keydown", function (event) {
            if (event.key === "Escape") {
                setOpen(false);
            }
        });

        if (input.value) {
            const selected = parseYMD(input.value);
            if (selected) {
                viewYear = selected.getFullYear();
                viewMonth = selected.getMonth();
            }
            updateInputColor();
        }
    }
});
