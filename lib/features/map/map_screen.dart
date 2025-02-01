import 'package:flutter/material.dart';
import 'package:google_maps_flutter/google_maps_flutter.dart';

class MapScreen extends StatefulWidget {
  final List<LatLng> routeCoordinates;
  final LatLng currentPosition;

  const MapScreen({
    super.key,
    required this.routeCoordinates,
    required this.currentPosition,
  });

  @override
  State<MapScreen> createState() => _MapScreenState();
}

class _MapScreenState extends State<MapScreen> {
  late GoogleMapController _mapController;
  final Set<Polyline> _polylines = {};
  final Set<Marker> _markers = {};

  @override
  void initState() {
    super.initState();
    _initializeMap();
  }

  void _initializeMap() {
    _polylines.add(Polyline(
      polylineId: const PolylineId('train_route'),
      points: widget.routeCoordinates,
      color: Colors.blue,
      width: 4,
    ));

    _markers.add(Marker(
      markerId: const MarkerId('current_position'),
      position: widget.currentPosition,
      icon: BitmapDescriptor.defaultMarkerWithHue(BitmapDescriptor.hueRed),
      infoWindow: const InfoWindow(title: 'Current Position'),
    ));
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Live Tracking')),
      body: GoogleMap(
        onMapCreated: (controller) => _mapController = controller,
        initialCameraPosition: CameraPosition(
          target: widget.currentPosition,
          zoom: 12,
        ),
        polylines: _polylines,
        markers: _markers,
      ),
    );
  }
}