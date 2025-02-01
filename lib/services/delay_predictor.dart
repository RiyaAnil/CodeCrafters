import 'package:cloud_firestore/cloud_firestore.dart';

class DelayPredictor {
  final FirebaseFirestore _firestore;

  DelayPredictor(this._firestore);

  Future<double> predictDelay(String trainNumber) async {
    final history = await _firestore
        .collection('delayHistory')
        .doc(trainNumber)
        .collection('records')
        .orderBy('date', descending: true)
        .limit(7)
        .get();

    if (history.docs.isEmpty) return 0.0;

    final totalDelay = history.docs.fold(0, (sum, doc) => sum + doc['delayMinutes']);
    return totalDelay / history.docs.length;
  }
}