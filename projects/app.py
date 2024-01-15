from flask import Flask, render_template, request, jsonify
from agentbase import RoomModel
app = Flask(__name__)
mesa_model = RoomModel()

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/start_simulation', methods=['POST'])
def start_simulation():
    # Logic to start or reset the Mesa simulation
    mesa_model.run_model()  # Example call to start the model
    return jsonify({"status": "success", "message": "Simulation started"})


@app.route('/get_simulation_data')
def get_simulation_data():
    # Logic to retrieve data from the Mesa model
    data = mesa_model.get_data()  # Example call to get data from the model
    return jsonify(data)


@app.route('/update_settings', methods=['POST'])
def update_settings():
    try:
        data = request.json
        temperature = data['Temperature']
        light = data['Light']
        acoustic = data['acoustics']
        airQuality = data['airQuality']

        # Update model settings
        RoomModel.temperature(temperature)
        RoomModel.light(light)
        RoomModel.acoustic(acoustic)
        RoomModel.air_quality(airQuality)

        return jsonify({"status": "success", "message": "Settings updated"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

if __name__ == '__main__':
    app.run(debug=True,port= 5001)