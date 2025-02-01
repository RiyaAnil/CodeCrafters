let map;
let directionsService;
let directionsRenderer;
let userLocation = null; // User's current location
let destinations = []; // List of destinations for the route
let selectedCity = '';

function initMap() {
    directionsService = new google.maps.DirectionsService();
    directionsRenderer = new google.maps.DirectionsRenderer();

    // Create a map centered on a default location (you can change this)
    map = new google.maps.Map(document.getElementById("map"), {
        zoom: 12,
        center: { lat: 28.6139, lng: 77.2090 }, // Default to Delhi
    });

    directionsRenderer.setMap(map);

    // Get the user's current location
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function(position) {
            userLocation = new google.maps.LatLng(position.coords.latitude, position.coords.longitude);
            map.setCenter(userLocation);
        }, function() {
            alert("Geolocation is not supported by this browser.");
        });
    }
}

function loadInterests(city) {
    selectedCity = city;
    document.getElementById('city-selection').style.display = 'none';
    document.getElementById('interest-selection').style.display = 'block';
}

function loadAttractions(interest) {
    fetch('http://127.0.0.1:5000/city/${selectedCity}/${interest}')
        .then(response => response.json())
        .then(data => {
            const routeDetails = document.getElementById('route-details');
            routeDetails.innerHTML = '<h2>Personalized Route</h2>';
            destinations = []; // Reset destinations

            if (data.error) {
                routeDetails.innerHTML += '<p>${data.error}</p>';
            } else {
                data.forEach(attraction => {
                    routeDetails.innerHTML += `
                        <h3>${attraction.name}</h3>
                        <p><strong>Description:</strong> ${attraction.description}</p>
                        <p><strong>Timings:</strong> ${attraction.timing}</p>
                        <p><strong>Address:</strong> ${attraction.address}</p>
                    `;
                    // Add each destination to the destinations array
                    destinations.push({ 
                        name: attraction.name,
                        location: new google.maps.LatLng(attraction.lat, attraction.lng) // Assuming you get lat/lng from your data
                    });
                });
            }

            // Show the map and plot the route
            if (destinations.length > 0) {
                plotRoute();
            }
        })
        .catch(error => {
            console.error('Error fetching attractions:', error);
        });
}

function plotRoute() {
    if (userLocation) {
        let waypoints = destinations.map(destination => ({
            location: destination.location,
            stopover: true
        }));

        const request = {
            origin: userLocation,
            destination: destinations[destinations.length - 1].location, // Last destination
            waypoints: waypoints.slice(0, -1), // All destinations except the last one
            travelMode: google.maps.TravelMode.DRIVING, // You can also change it to WALKING, BICYCLING, etc.
            optimizeWaypoints: true, // Automatically optimizes the route
        };

        directionsService.route(request, function(result, status) {
            if (status === google.maps.DirectionsStatus.OK) {
                directionsRenderer.setDirections(result);
            } else {
                alert('Directions request failed due to ' + status);
            }
        });
    }
}