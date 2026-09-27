document.addEventListener("DOMContentLoaded", function () {

    const progressBars = document.querySelectorAll(".progress-fill");

    progressBars.forEach(function (bar) {

        const width = bar.getAttribute("data-width");

        if (width !== null) {
            bar.style.width = width + "%";
        }

    });

});