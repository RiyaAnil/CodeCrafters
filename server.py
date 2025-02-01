from flask import Flask, jsonify, request
from flask_cors import CORS
from math import radians, sin, cos, sqrt, atan2

app = Flask(__name__)
CORS(app)

def haversine(lon1, lat1, lon2, lat2):
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * atan2(sqrt(a), sqrt(1-a))
    return c * 6371  # Earth radius in km

cities = {
    # Sample city data as shown in your initial code
}

@app.route('/city/<city>/<interest>')
def get_attractions(city, interest):
    user_lat = request.args.get('lat', type=float)
    user_lng = request.args.get('lng', type=float)
    
    if city not in cities or interest not in cities.get(city, {}):
        return jsonify({'error': 'City or interest not found'}), 404
    
    attractions = cities[city][interest]
    
    if user_lat and user_lng:
        attractions = sorted(attractions, key=lambda attr: haversine(user_lng, user_lat, attr['lng'], attr['lat']))
    
    return jsonify(attractions)

if __name__ == '__main__':
    app.run(debug=True)
