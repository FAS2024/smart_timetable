// timetable.js

document.addEventListener("DOMContentLoaded", function () {
    // Highlight the current day in the timetable
    const today = new Date().getDay(); // Sunday = 0, Monday = 1, ..., Saturday = 6
    const days = document.querySelectorAll(".day-column");
    days.forEach((day, index) => {
        if (index === today - 1) { // Adjust for Monday as first day
            day.classList.add("highlight-today");
        }
    });

    // Handle form submission
    const forms = document.querySelectorAll(".timetable-form");
    forms.forEach((form) => {
        form.addEventListener("submit", function (event) {
            const inputs = form.querySelectorAll("input, select, textarea");
            let isValid = true;

            inputs.forEach((input) => {
                if (input.required && !input.value.trim()) {
                    isValid = false;
                    input.classList.add("error");
                } else {
                    input.classList.remove("error");
                }
            });

            if (!isValid) {
                event.preventDefault();
                alert("Please fill out all required fields.");
            }
        });
    });

    // Real-time display adjustments for time slots
    const timeInputs = document.querySelectorAll(".time-slot-input");
    timeInputs.forEach((input) => {
        input.addEventListener("change", function () {
            const row = input.closest(".time-slot-row");
            const start = row.querySelector(".start-time").value;
            const end = row.querySelector(".end-time").value;

            if (start && end && new Date(`1970-01-01T${start}:00`) >= new Date(`1970-01-01T${end}:00`)) {
                alert("Start time must be before end time.");
                input.value = "";
            }
        });
    });
});
