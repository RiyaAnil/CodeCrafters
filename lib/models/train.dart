class Train {
  final String id;
  final String number;
  final String name;
  final List<String> stations;
  final DateTime departureTime;
  final int delayMinutes;

  Train({
    required this.id,
    required this.number,
    required this.name,
    required this.stations,
    required this.departureTime,
    this.delayMinutes = 0,
  });

  factory Train.fromFirestore(Map<String, dynamic> data, String id) {
    return Train(
      id: id,
      number: data['number'],
      name: data['name'],
      stations: List<String>.from(data['stations']),
      departureTime: data['departureTime'].toDate(),
      delayMinutes: data['delayMinutes'] ?? 0,
    );
  }
  Future<double> getPredictedDelay(DelayPredictor predictor) async {
    return await predictor.predictDelay(number);
}