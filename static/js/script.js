const form = document.getElementById("checkinForm");

form.addEventListener("submit", function (event) {
    const sleep = parseFloat(document.getElementById("sleep").value);
    const water = parseInt(document.getElementById("water").value);
    const exercise = parseInt(document.getElementById("exercise").value);
    const errorMsg = document.getElementById("errorMsg");

    errorMsg.textContent = "";

    if (sleep < 0 || sleep > 24) {
        errorMsg.textContent = "Sleep hours must be between 0 and 24.";
        event.preventDefault();
        return;
    }

    if (water < 0 || water > 30) {
        errorMsg.textContent = "Water glasses must be between 0 and 30.";
        event.preventDefault();
        return;
    }

    if (exercise < 0 || exercise > 600) {
        errorMsg.textContent = "Exercise minutes must be between 0 and 600.";
        event.preventDefault();
        return;
    }
});