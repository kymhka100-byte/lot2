[app]
title = My Kivy Game
package.name = mygame
package.domain = org.test

source.dir = .
source.include_exts = py,png,jpg,kv,atlas,wav,mp3

version = 0.1

requirements = python3,kivy

orientation = portrait
fullscreen = 1

# Android 설정 (V3/V4 및 API 34 호환)
android.api = 34
android.minapi = 21
android.ndk = 25b
android.archs = arm64-v8a, armeabi-v7a
android.allow_backup = True

# 빌드 플래그
p4a.branch = master