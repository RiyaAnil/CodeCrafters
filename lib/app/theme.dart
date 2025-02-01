import 'package:flutter/material.dart';

class AppTheme {
  static final lightTheme = ThemeData(
    colorScheme: ColorScheme.light(
      primary: Colors.deepPurple,
      secondary: Colors.amber,
    ),
    useMaterial3: true,
  );

  static final darkTheme = ThemeData(
    colorScheme: ColorScheme.dark(
      primary: Colors.deepPurpleAccent,
      secondary: Colors.amberAccent,
    ),
    useMaterial3: true,
  );
}