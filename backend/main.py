from flask import Flask, request, jsonify
from flask_cors import CORS
from utils.neoFeed import neoFeed
from config import API_KEY
from utils.neoObjectApproach import neoObjectDataStructure
from datetime import datetime, timedelta
from utils.marsFeed import mars
from utils.neoOrbitImage import plot_orbit
import json

app = Flask(__name__)
CORS(app)

# Store the orbital data from the previous route
previous_orbital_data = None

@app.route('/api/neo', methods=['GET', 'POST'])
def neo_data():
    if request.method == 'POST':
        response = request.get_json()
        # Get NEO date range for API request
        start_date_str = response.get('start_date')
        end_date_str = response.get('end_date')
        
        # Validate and convert dates
        if not start_date_str or not end_date_str:
            return jsonify({"error": "Start date and end date are required"}), 400

        try:
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d')
        except ValueError:
            return jsonify({"error": "Invalid date format. Use YYYY-MM-DD"}), 400
        
        # neoFeed.py - NASA NEO API data for Neo.js 
        data = neoFeed(start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d'))        
        return jsonify(data=data)
    
    if request.method == 'GET':
        # Default to today
        today = datetime.now()
        start_date = today.strftime('%Y-%m-%d')
        end_date = today.strftime('%Y-%m-%d')        
        data = neoFeed(start_date, end_date)

        return jsonify(data=data)


@app.route('/api/neoObject', methods=['POST', 'GET'])
def neo_identifier():
    if request.method == 'POST':
        print('/api/neoObject', 'POST')
        response = request.get_json()
        # Obtains the user selected NEO ID
        identifier = response.get('id')

        if not identifier:
            return jsonify({"error": "ID is required"}), 400
        
        # neoObjectApproach.py - NASA API data for NeoObject.js and Chart.js
        data = neoObjectDataStructure(identifier)         
        if data:
            # Avoids second API call 
            global previous_orbital_data
            previous_orbital_data = json.loads(data)  
            return jsonify(data=data, identifier=identifier)
        else:
            return jsonify({"error": "No data found"}), 404
    else:
        orbital_data = previous_orbital_data['orbital_data']
        return jsonify(data=orbital_data)
        
    
# Working on this portion
@app.route('/api/updatedChart', methods=['GET', 'POST'])
def updated_chart():
    if request.method == 'POST':
        response = request.get_json()        
        selectedDate = response['date'] 

        # Stored orbital data from /api/neoObject            
        orbital_data = previous_orbital_data['orbital_data']

        # print(type(orbital_data[0]))
        # print(type(orbital_data))
        # print(orbital_data['sorted_approaches'])
        # print(selectedDate)
        # print(orbital_data['object_id'])

        # neoOrbitImage.py - Constructs new chart for NeoObject.js  
        newChart = plot_orbit(orbital_data, selectedDate)
        return jsonify(data=newChart)  
    else:
        return {'message': 'Send a POST request'}, 200  



        

    
@app.route('/api/mars', methods=['GET'])
def mars_data():

    data = mars()
    print(data)
    
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)
