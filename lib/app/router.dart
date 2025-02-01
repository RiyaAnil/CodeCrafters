import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';
import '../services/auth_service.dart';
import '../features/home/home_screen.dart';
import '../features/auth/login_screen.dart';

final router = GoRouter(
  redirect: (context, state) {
    final authService = AuthService();
    final isLoggedIn = authService.user.value != null;
    final isLoggingIn = state.location == '/login';

    if (!isLoggedIn && !isLoggingIn) return '/login';
    if (isLoggedIn && isLoggingIn) return '/';
    return null;
  },
  routes: [
    GoRoute(
      path: '/',
      builder: (context, state) => const HomeScreen(),
    ),
    GoRoute(
      path: '/login',
      builder: (context, state) => const LoginScreen(),
    ),
  ],
);