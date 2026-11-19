const dataBox = document.getElementById("chartData");

const labels = JSON.parse(dataBox.dataset.labels);
const sleepData = JSON.parse(dataBox.dataset.sleep);
const waterData = JSON.parse(dataBox.dataset.water);
const exerciseData = JSON.parse(dataBox.dataset.exercise);

new Chart(document.getElementById("sleepWaterChart"), {
    type: "line",
    data: {
        labels: labels,
        datasets: [
            {
                label: "Sleep (hrs)",
                data: sleepData,
                borderColor: "#2e8b57",
                tension: 0.3
            },
            {
                label: "Water (glasses)",
                data: waterData,
                borderColor: "#1e90ff",
                tension: 0.3
            }
        ]
    },
    options: { responsive: true }
});

new Chart(document.getElementById("exerciseChart"), {
    type: "bar",
    data: {
        labels: labels,
        datasets: [
            {
                label: "Exercise (min)",
                data: exerciseData,
                backgroundColor: "#f4a261"
            }
        ]
    },
    options: { responsive: true }
});