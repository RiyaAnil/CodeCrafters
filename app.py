
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
    # Existing cities (Delhi, Jaipur, Kochi)
   'Delhi': {
        'pilgrimage': [
            {'name': 'Kashi Vishwanath Temple', 'lat': 25.3176, 'lng': 82.9739, 'description': 'A major pilgrimage site.', 'timing': '5 AM to 10 PM', 'address': 'Varanasi, India'},
            {'name': 'Baba Vishwanath Temple', 'lat': 25.3267, 'lng': 82.9687, 'description': 'Famous pilgrimage destination.', 'timing': '6 AM to 8 PM', 'address': 'Varanasi, India'}
        ],
        'history': [
            {'name': 'Qutub Minar', 'lat': 28.5244, 'lng': 77.1855, 'description': 'A UNESCO World Heritage site.', 'timing': '8 AM to 6 PM', 'address': 'Mehrauli, Delhi'},
            {'name': 'Red Fort', 'lat': 28.6562, 'lng': 77.2410, 'description': 'A symbol of India\'s history and architecture.', 'timing': '9 AM to 6 PM', 'address': 'Chandni Chowk, Delhi'}
        ],
        'leisure': [
            {'name': 'India Gate', 'lat': 28.6139, 'lng': 77.2295, 'description': 'A memorial for soldiers.', 'timing': 'Open 24 hours', 'address': 'Rajpath, Delhi'},
            {'name': 'Lodhi Gardens', 'lat': 28.5855, 'lng': 77.2190, 'description': 'A beautiful park.', 'timing': '5 AM to 8 PM', 'address': 'Lodhi Road, Delhi'}
        ]
    },
    'Jaipur': {
        'pilgrimage': [
            {'name': 'Birla Mandir', 'lat': 26.9124, 'lng': 75.8203, 'description': 'A beautiful temple dedicated to Lord Vishnu and Lakshmi.', 'timing': '6 AM to 8 PM', 'address': 'Jaipur, Rajasthan'}
        ],
        'history': [
            {'name': 'Amber Fort', 'lat': 26.9853, 'lng': 75.8514, 'description': 'A UNESCO World Heritage site, famous for its historical architecture.', 'timing': '8 AM to 5:30 PM', 'address': 'Amber, Jaipur'},
            {'name': 'City Palace', 'lat': 26.9250, 'lng': 75.8260, 'description': 'A majestic palace complex built by the rulers of Jaipur.', 'timing': '9 AM to 5 PM', 'address': 'Jaipur, Rajasthan'}
        ],
        'leisure': [
            {'name': 'Jal Mahal', 'lat': 26.9681, 'lng': 75.8514, 'description': 'A beautiful palace in the middle of a lake.', 'timing': '9 AM to 6 PM', 'address': 'Jaipur, Rajasthan'}
        ]
    },
    'Kochi': {
        'pilgrimage': [
            {'name': 'Vypin Island', 'lat': 9.9700, 'lng': 76.2097, 'description': 'A famous pilgrimage site.', 'timing': '6 AM to 8 PM', 'address': 'Kochi, Kerala'}
        ],
        'history': [
            {'name': 'Fort Kochi', 'lat': 9.9656, 'lng': 76.2216, 'description': 'Historic site showcasing Portuguese and Dutch colonial history.', 'timing': '9 AM to 6 PM', 'address': 'Kochi, Kerala'}
        ],
        'leisure': [
            {'name': 'Marine Drive', 'lat': 9.9820, 'lng': 76.2813, 'description': 'A scenic promenade along the backwaters.', 'timing': 'Open 24 hours', 'address': 'Kochi, Kerala'}
        ]
    },
    # New cities
    'Chennai': {
        'pilgrimage': [
            {'name': 'Kapaleeshwarar Temple', 'lat': 13.6288, 'lng': 80.1921, 'description': 'Famous Shiva temple.', 'timing': '5 AM to 12 PM, 4 PM to 9 PM', 'address': 'Mylapore, Chennai'},
            {'name': 'Santhome Cathedral Basilica', 'lat': 13.0333, 'lng': 80.2747, 'description': 'Important Christian pilgrimage site.', 'timing': '6 AM to 8 PM', 'address': 'Santhome, Chennai'}
        ],
        'history': [
            {'name': 'Fort St. George', 'lat': 13.0797, 'lng': 80.2870, 'description': 'Historic British fortress.', 'timing': '9 AM to 5 PM', 'address': 'Rajaji Rd, Chennai'},
            {'name': 'Government Museum', 'lat': 13.0688, 'lng': 80.2634, 'description': 'Oldest museum in India.', 'timing': '9:30 AM to 5 PM', 'address': 'Egmore, Chennai'}
        ],
        'leisure': [
            {'name': 'Marina Beach', 'lat': 13.0544, 'lng': 80.2833, 'description': 'Longest urban beach in India.', 'timing': 'Open 24 hours', 'address': 'Marina Beach Rd, Chennai'},
            {'name': 'Guindy National Park', 'lat': 13.0041, 'lng': 80.2444, 'description': 'Protected area in the city.', 'timing': '9 AM to 5:30 PM', 'address': 'Guindy, Chennai'}
        ]
    },
    'Mumbai': {
        'pilgrimage': [
            {'name': 'Siddhivinayak Temple', 'lat': 19.0175, 'lng': 72.8303, 'description': 'Renowned Ganesha temple.', 'timing': '5:30 AM to 9:30 PM', 'address': 'Prabhadevi, Mumbai'},
            {'name': 'Haji Ali Dargah', 'lat': 18.9822, 'lng': 72.8094, 'description': 'Iconic mosque and tomb.', 'timing': '5:30 AM to 10 PM', 'address': 'Worli, Mumbai'}
        ],
        'history': [
            {'name': 'Gateway of India', 'lat': 18.9220, 'lng': 72.8347, 'description': 'Historic monument overlooking the Arabian Sea.', 'timing': 'Open 24 hours', 'address': 'Apollo Bandar, Mumbai'},
            {'name': 'Chhatrapati Shivaji Maharaj Vastu Sangrahalaya', 'lat': 18.9267, 'lng': 72.8316, 'description': 'Premier art and history museum.', 'timing': '10:15 AM to 6 PM', 'address': 'Fort, Mumbai'}
        ],
        'leisure': [
            {'name': 'Juhu Beach', 'lat': 19.1077, 'lng': 72.8263, 'description': 'Popular beach with street food.', 'timing': 'Open 24 hours', 'address': 'Juhu, Mumbai'},
            {'name': 'Sanjay Gandhi National Park', 'lat': 19.2143, 'lng': 72.9140, 'description': 'Large protected area with biodiversity.', 'timing': '7:30 AM to 6:30 PM', 'address': 'Borivali East, Mumbai'}
        ]
    },
    'Bangalore': {
        'pilgrimage': [
            {'name': 'ISKCON Temple', 'lat': 13.0103, 'lng': 77.5510, 'description': 'Famous Krishna temple.', 'timing': '4:15 AM to 8:30 PM', 'address': 'Rajajinagar, Bangalore'},
            {'name': 'Dodda Ganapathi Temple', 'lat': 12.9343, 'lng': 77.5119, 'description': 'Large Ganesha idol temple.', 'timing': '6 AM to 8 PM', 'address': 'Basavanagudi, Bangalore'}
        ],
        'history': [
            {'name': 'Bangalore Palace', 'lat': 12.9982, 'lng': 77.5925, 'description': 'Royal palace with Tudor architecture.', 'timing': '10 AM to 5:30 PM', 'address': 'Vasanth Nagar, Bangalore'},
            {'name': 'Tipu Sultan\'s Summer Palace', 'lat': 12.9611, 'lng': 77.5736, 'description': 'Historic wooden palace.', 'timing': '8:30 AM to 5:30 PM', 'address': 'Chamarajpet, Bangalore'}
        ],
        'leisure': [
            {'name': 'Cubbon Park', 'lat': 12.9764, 'lng': 77.5927, 'description': 'Landmark park with greenery.', 'timing': '6 AM to 6 PM', 'address': 'Sampangi Rama Nagar, Bangalore'},
            {'name': 'Lalbagh Botanical Garden', 'lat': 12.9507, 'lng': 77.5848, 'description': 'Famous botanical garden.', 'timing': '6 AM to 7 PM', 'address': 'Lalbagh, Bangalore'}
        ]
    }
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