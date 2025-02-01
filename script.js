let map;
let markers = [];
let routeLine = null;
let selectedCity = "";

function initMap() {
    map = L.map('map').setView([20.5937, 78.9629], 5);
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png').addTo(map);
}

function loadAttractions(interest) {
    document.getElementById('interest-selection').style.display = 'none';
    document.getElementById('route-container').style.display = 'block';

    if (!map) {
        initMap();
    }

    // Check if geolocation is supported
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(
            (position) => {
                const userLat = position.coords.latitude;
                const userLng = position.coords.longitude;
                fetchData(interest, userLat, userLng);
            },
            (error) => {
                console.error("Geolocation error:", error);
                fetchData(interest); // Proceed without user's location
            }
        );
    } else {
        fetchData(interest); // Fallback to original logic
    }
}

function fetchData(interest, userLat = null, userLng = null) {
    let url = `http://127.0.0.1:5000/city/${selectedCity}/${interest}`;

    if (userLat && userLng) {
        url += `?lat=${userLat}&lng=${userLng}`;
    }

    fetch(url)
        .then(response => response.json())
        .then(data => {
            displayAttractions(data);
        });
}

function displayAttractions(attractions) {
    if (markers.length) {
        markers.forEach(marker => marker.remove());
        markers = [];
    }

    if (routeLine) {
        routeLine.remove();
        routeLine = null;
    }

    attractions.forEach(attraction => {
        const { lat, lng, name, description, address, timing } = attraction;
        const marker = L.marker([lat, lng]).addTo(map);

        marker.bindPopup(`<b>${name}</b><br>${description}<br>${address}<br>${timing}`);

        markers.push(marker);
    });

    if (markers.length > 1) {
        const latlngs = markers.map(marker => marker.getLatLng());
        routeLine = L.polyline(latlngs, { color: 'blue' }).addTo(map);
    }
}
