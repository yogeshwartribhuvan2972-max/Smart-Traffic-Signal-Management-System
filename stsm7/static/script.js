setInterval(() => {
    let j = new URLSearchParams(window.location.search).get("j");
    if (!j) return;

    fetch("/status/" + j)
    .then(r => r.json())
    .then(data => {
        document.getElementById("signal-block").innerHTML =
            "<p>North: " + data.signal.north + "</p>" +
            "<p>South: " + data.signal.south + "</p>" +
            "<p>East: " + data.signal.east + "</p>" +
            "<p>West: " + data.signal.west + "</p>";
    });

}, 1000);
