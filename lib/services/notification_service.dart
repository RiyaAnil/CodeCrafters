import 'package:firebase_messaging/firebase_messaging.dart';

class NotificationService {
  // ... previous code

  Future<void> initializeNotifications() async {
    await FirebaseMessaging.instance.setAutoInitEnabled(true);
    
    // Get device token
    final token = await FirebaseMessaging.instance.getToken();
    print('Device Token: $token');

    // Handle notifications when app is in foreground
    FirebaseMessaging.onMessage.listen((RemoteMessage message) {
      _showNotification(message);
    });

    // Handle notification taps
    FirebaseMessaging.onMessageOpenedApp.listen((RemoteMessage message) {
      _handleNotificationTap(message);
    });
  }

  void _showNotification(RemoteMessage message) {
    // Implement local notifications using flutter_local_notifications
  }

  void _handleNotificationTap(RemoteMessage message) {
    // Example: Navigate to specific train screen
    final trainId = message.data['trainId'];
    // context.go('/train/$trainId');
  }
}