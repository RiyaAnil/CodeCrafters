import 'package:cloud_firestore/cloud_firestore.dart';
import '../models/train.dart';

class FirestoreService {
  final FirebaseFirestore _firestore = FirebaseFirestore.instance;

  Stream<List<Train>> getTrains() {
    return _firestore
        .collection('trains')
        .snapshots()
        .map((snapshot) => snapshot.docs
            .map((doc) => Train.fromFirestore(doc.data(), doc.id))
            .toList());
  }

  Future<void> addTrain(Train train) async {
    await _firestore.collection('trains').doc(train.id).set({
      'number': train.number,
      'name': train.name,
      'stations': train.stations,
      'departureTime': train.departureTime,
      'delayMinutes': train.delayMinutes,
    });
  }

  class FirestoreService {
  // ... existing code
  
  Stream<List<Train>> getTrains() {
    return _firestore.collection('trains').snapshots().asyncMap((snapshot) async {
      final trains = snapshot.docs.map((doc) => Train.fromFirestore(doc.data(), doc.id)).toList();
      
      // Cache to Hive
      final box = await Hive.openBox<Train>('trainsCache');
      await box.clear();
      await box.addAll(trains);
      
      return trains;
    });
  }

  Future<List<Train>> getCachedTrains() async {
    final box = await Hive.openBox<Train>('trainsCache');
    return box.values.toList();
  }
}
}