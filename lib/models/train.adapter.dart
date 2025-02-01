import 'package:hive/hive.dart';
import 'train.dart';

class TrainAdapter extends TypeAdapter<Train> {
  @override
  final int typeId = 0;

  @override
  Train read(BinaryReader reader) {
    return Train(
      id: reader.read(),
      number: reader.read(),
      name: reader.read(),
      stations: reader.read(),
      departureTime: reader.read(),
      delayMinutes: reader.read(),
    );
  }

  @override
  void write(BinaryWriter writer, Train obj) {
    writer.write(obj.id);
    writer.write(obj.number);
    writer.write(obj.name);
    writer.write(obj.stations);
    writer.write(obj.departureTime);
    writer.write(obj.delayMinutes);
  }
}