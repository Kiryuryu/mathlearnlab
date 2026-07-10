library;

import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';

/// 静逸书卷 design system — warm paper palette.
class AppTheme {
  static const Color _accent = Color(0xFF5B7B94);
  static const Color _accentWarm = Color(0xFF8B7355);
  static const Color _bgPage = Color(0xFFFAF8F5);
  static const Color _bgCard = Color(0xFFFFFFFF);
  static const Color _bgNav = Color(0xFFF5F0E8);
  static const Color _textPrimary = Color(0xFF2C2C2C);
  static const Color _textSecondary = Color(0xFF5C5C5C);
  static const Color _textMuted = Color(0xFF8C8C8C);
  static const Color _border = Color(0xFFE8E0D5);

  static ThemeData get light => ThemeData(
        useMaterial3: true,
        colorScheme: ColorScheme.light(
          primary: _accent,
          secondary: _accentWarm,
          surface: _bgPage,
        ),
        scaffoldBackgroundColor: _bgPage,
        cardColor: _bgCard,
        dividerColor: _border,
        textTheme: GoogleFonts.notoSansScTextTheme().copyWith(
          bodyLarge: const TextStyle(color: _textPrimary, fontSize: 15),
          bodyMedium: const TextStyle(color: _textSecondary, fontSize: 14),
          titleLarge: GoogleFonts.notoSerifSc(
              color: _textPrimary,
              fontSize: 21,
              fontWeight: FontWeight.w600),
          titleMedium: GoogleFonts.notoSerifSc(
              color: _textPrimary,
              fontSize: 17,
              fontWeight: FontWeight.w600),
          labelSmall: const TextStyle(
            color: _textMuted,
            fontSize: 11,
            letterSpacing: 1.5,
          ),
        ),
        appBarTheme: AppBarTheme(
          backgroundColor: _bgNav,
          foregroundColor: _textPrimary,
          elevation: 0,
          titleTextStyle: GoogleFonts.notoSerifSc(
            color: _textPrimary,
            fontSize: 17,
            fontWeight: FontWeight.w700,
          ),
        ),
        navigationDrawerTheme: NavigationDrawerThemeData(
          backgroundColor: _bgNav,
        ),
        inputDecorationTheme: InputDecorationTheme(
          border: OutlineInputBorder(
            borderRadius: BorderRadius.circular(4),
            borderSide: const BorderSide(color: _border),
          ),
          enabledBorder: OutlineInputBorder(
            borderRadius: BorderRadius.circular(4),
            borderSide: const BorderSide(color: _border),
          ),
          focusedBorder: OutlineInputBorder(
            borderRadius: BorderRadius.circular(4),
            borderSide: const BorderSide(color: _accent),
          ),
          contentPadding:
              const EdgeInsets.symmetric(horizontal: 12, vertical: 9),
          isDense: true,
        ),
        elevatedButtonTheme: ElevatedButtonThemeData(
          style: ElevatedButton.styleFrom(
            backgroundColor: _accent,
            foregroundColor: Colors.white,
            shape: RoundedRectangleBorder(
              borderRadius: BorderRadius.circular(4),
            ),
            padding: const EdgeInsets.symmetric(horizontal: 18, vertical: 10),
          ),
        ),
        cardTheme: CardThemeData(
          color: _bgCard,
          elevation: 0,
          shape: RoundedRectangleBorder(
            borderRadius: BorderRadius.circular(8),
            side: const BorderSide(color: _border),
          ),
        ),
      );

  // ── Dark mode ──
  static const Color _darkBg = Color(0xFF1A1814);
  static const Color _darkCard = Color(0xFF24211C);
  static const Color _darkNav = Color(0xFF1E1C17);
  static const Color _darkText = Color(0xFFE8E0D0);
  static const Color _darkTextSecondary = Color(0xFFB0A898);
  static const Color _darkBorder = Color(0xFF3A3530);
  static const Color _darkAccent = Color(0xFF7A9EB3);

  static ThemeData get dark => ThemeData(
        useMaterial3: true,
        colorScheme: ColorScheme.dark(
          primary: _darkAccent,
          secondary: const Color(0xFFC4A97A),
          surface: _darkBg,
        ),
        scaffoldBackgroundColor: _darkBg,
        cardColor: _darkCard,
        dividerColor: _darkBorder,
        textTheme: GoogleFonts.notoSansScTextTheme().copyWith(
          bodyLarge: const TextStyle(color: _darkText, fontSize: 15),
          bodyMedium:
              const TextStyle(color: _darkTextSecondary, fontSize: 14),
          titleLarge: GoogleFonts.notoSerifSc(
              color: _darkText, fontSize: 21, fontWeight: FontWeight.w600),
          titleMedium: GoogleFonts.notoSerifSc(
              color: _darkText, fontSize: 17, fontWeight: FontWeight.w600),
          labelSmall: const TextStyle(
            color: Color(0xFF7A7262),
            fontSize: 11,
            letterSpacing: 1.5,
          ),
        ),
        appBarTheme: AppBarTheme(
          backgroundColor: _darkNav,
          foregroundColor: _darkText,
          elevation: 0,
          titleTextStyle: GoogleFonts.notoSerifSc(
            color: _darkText,
            fontSize: 17,
            fontWeight: FontWeight.w700,
          ),
        ),
        inputDecorationTheme: InputDecorationTheme(
          border: OutlineInputBorder(
            borderRadius: BorderRadius.circular(4),
            borderSide: const BorderSide(color: _darkBorder),
          ),
          enabledBorder: OutlineInputBorder(
            borderRadius: BorderRadius.circular(4),
            borderSide: const BorderSide(color: _darkBorder),
          ),
          focusedBorder: OutlineInputBorder(
            borderRadius: BorderRadius.circular(4),
            borderSide: const BorderSide(color: _darkAccent),
          ),
          contentPadding:
              const EdgeInsets.symmetric(horizontal: 12, vertical: 9),
          isDense: true,
        ),
        elevatedButtonTheme: ElevatedButtonThemeData(
          style: ElevatedButton.styleFrom(
            backgroundColor: _darkAccent,
            foregroundColor: Colors.white,
            shape: RoundedRectangleBorder(
              borderRadius: BorderRadius.circular(4),
            ),
            padding: const EdgeInsets.symmetric(horizontal: 18, vertical: 10),
          ),
        ),
        cardTheme: CardThemeData(
          color: _darkCard,
          elevation: 0,
          shape: RoundedRectangleBorder(
            borderRadius: BorderRadius.circular(8),
            side: const BorderSide(color: _darkBorder),
          ),
        ),
      );
}
