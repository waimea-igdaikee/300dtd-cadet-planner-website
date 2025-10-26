/*
Tooltip.js - default html tooltips don't work in an overflow:scroll container as they get clipped,
so this script generates absolutely positioned divs above the table headings. These divs have readable tooltips.
*/

document.addEventListener("DOMContentLoaded", () => {
    const tooltipPairs = []; // Store th + tooltip div relationships
    const scrollContainer = document.getElementById("stats_table"); // your scroll container

    function createAndPosition(th) {
        let tooltip = th._tooltipDiv;

        // Create once
        if (!tooltip) {
            tooltip = document.createElement("div");
            tooltip.setAttribute("data-tooltip", th.getAttribute("custom-tooltip"));
            tooltip.style.position = "absolute";
            tooltip.style.display = "none"; // hide initially
            document.body.appendChild(tooltip);

            th._tooltipDiv = tooltip; // Keep reference on the element
            tooltipPairs.push({ th, tooltip });
        }

        // Get bounding rectangles
        const thRect = th.getBoundingClientRect();
        const containerRect = scrollContainer.getBoundingClientRect();

        // Check if th is fully visible in the container (with 5px room)
        const fullyVisible =
            thRect.top >= containerRect.top - 5 &&
            thRect.bottom <= containerRect.bottom + 5 &&
            thRect.left >= containerRect.left - 5 &&
            thRect.right <= containerRect.right + 5;

        if (fullyVisible) {
            tooltip.style.display = "block";
            tooltip.style.left = `${thRect.left}px`;
            tooltip.style.top = `${thRect.top}px`;
            tooltip.style.width = `calc(${thRect.width}px)`;
            tooltip.style.height = `${thRect.height}`;
        } else {
            tooltip.style.display = "none";
        }
    }

    // Initial placement
    requestAnimationFrame(() => {
        document.querySelectorAll("th[custom-tooltip]").forEach(th => {
            createAndPosition(th);
        });
    });

    // Update on window resize
    window.addEventListener("resize", () => {
        tooltipPairs.forEach(({ th }) => createAndPosition(th));
    });

    // Update on scroll of the table container
    if (scrollContainer) {
        scrollContainer.addEventListener("scroll", () => {
            tooltipPairs.forEach(({ th }) => createAndPosition(th));
        });
    }
});
