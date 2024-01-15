function sendSetting() {
    
    const temperatureValue = document.getElementById("temperature").value; // Get the value from the input
    const light = document.getElementById('light').value;
    const acoustics = document.getElementById('acoutics').value;
    const airQuality = document.getElementById('air_quality').value;
   
    fetch('/update_settings', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ Temperature: temperatureValue ,light: light ,acoustics: acoustics,airQuality: airQuality  }),

    })
    .then(response => response.json())
    .then(data => {
        console.log('Success:', data);
    })
    .catch((error) => {
        console.error('Error:', error);
    });
}
// static/js/script.js

function startSimulation() {
    fetch('/start_simulation', { method: 'POST' })
        .then(response => response.json())
        .then(data => console.log(data));
}

function updateUIWithSimulationData() {
    fetch('/get_simulation_data')
        .then(response => response.json())
        .then(data => {
            document.getElementById('temperature').value = data.temperature;
            document.getElementById('light').value = data.light;
            document.getElementById('airQuality').value = data.airQuality;
            document.getElementById('acoustics').value = data.acoustics;
        })
        .catch((error) => {
            console.error('Error:', error);
        });
}
const mesaValuesContainer = document.getElementById('mesa-values');

fetch('http://127.0.0.1:5001/api/get_mesa_values')
  .then(response => response.json())
  .then(data => {
    // Update the HT ML element with Mesa values
    mesaValuesContainer.textContent = JSON.stringify(data, null, 2);
  })
  .catch(error => {
    console.error('Error fetching Mesa values:', error);
  });

setInterval(updateUIWithSimulationData, 5000);  // Update every second
