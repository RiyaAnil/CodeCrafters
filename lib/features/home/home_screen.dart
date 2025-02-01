import 'package:flutter/material.dart';
import '../../models/train.dart';
import '../../services/firestore_service.dart';

class HomeScreen extends StatelessWidget {
  const HomeScreen({super.key});

  @override
  Widget build(BuildContext context) {
    final firestoreService = FirestoreService();

    return Scaffold(
      appBar: AppBar(
        title: const Text('Live Trains'),
        actions: [
          IconButton(
            icon: const Icon(Icons.logout),
            onPressed: () => Navigator.pushNamed(context, '/login'),
          ),
        ],
      ),
      body: StreamBuilder<List<Train>>(
        stream: firestoreService.getTrains(),
        builder: (context, snapshot) {
          if (snapshot.hasError) {
            return Center(child: Text('Error: ${snapshot.error}'));
          }

          if (snapshot.connectionState == ConnectionState.waiting) {
            return const Center(child: CircularProgressIndicator());
          }

          final trains = snapshot.data!;

          return ListView.builder(
            itemCount: trains.length,
            itemBuilder: (context, index) {
              final train = trains[index];
              return ListTile(
                // Inside ListTile in home_screen.dart
subtitle: Column(
  crossAxisAlignment: CrossAxisAlignment.start,
  children: [
    Text('Current delay: ${train.delayMinutes} mins'),
    FutureBuilder<double>(
      future: DelayPredictor(FirebaseFirestore.instance)
          .predictDelay(train.number),
      builder: (context, snapshot) {
        if (snapshot.hasData) {
          return Text('Predicted delay: ${snapshot.data!.toStringAsFixed(1)} mins');
        }
        return const Text('Calculating prediction...');
      },
    ),
  ],
),
                title: Text(train.name),
                subtitle: Text('Train No: ${train.number}'),
                trailing: Chip(
                  label: Text('${train.delayMinutes} min delay'),
                  backgroundColor: train.delayMinutes > 30 
                      ? Colors.red[100] 
                      : Colors.green[100],
                ),
                // Inside ListTile in home_screen.dart
onTap: () {
  Navigator.push(
    context,
    MaterialPageRoute(
      builder: (context) => MapScreen(
        routeCoordinates: _convertToLatLng(train.stations),
        currentPosition: _getCurrentPosition(train),
      ),
    ),
  );
},

// Helper methods
List<LatLng> _convertToLatLng(List<String> stationCodes) {
  // Implement actual station coordinates lookup
  return [LatLng(19.0760, 72.8777), LatLng(28.7041, 77.1025)]; // Mock data
}

LatLng _getCurrentPosition(Train train) {
  // Implement actual current position logic
  return LatLng(19.0760, 72.8777); // Mock Mumbai coordinates
}
              );
            },
          );
        },
      ),
    );
  }
}