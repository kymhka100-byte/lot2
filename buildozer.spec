[app]

# (str) Title of your application
title = Lotto365

# (str) Package name
package.name = lotto365

# (str) Package domain (used for the Android package ID)
package.domain = org.lotto365

# (str) Source code directory
source.dir = .

# (str) Main Python entry point
source.main = main.py

# (str) Application version
version = 1.0

# (list) Python files and other assets to include
source.include_exts = py,wav,png,jpg,jpeg

# (list) Python requirements
requirements = python3,kivy

# (str) Supported orientation
orientation = portrait

# (bool) Fullscreen mode
fullscreen = 0

# (str) Android API level
android.api = 35

# (str) Minimum Android API level
android.minapi = 23

# (str) Android NDK version
android.ndk = 27c

# (str) Android architecture
android.arch = arm64-v8a

# (str) Android app permissions
android.permissions = VIBRATE

# (bool) Show Android boot splash
android.presplash_color = #000000

# (str) Android app icon
# icon.filename = %(source.dir)s/icon.png

# (str) Android application activity
android.entrypoint = org.kivy.android.PythonActivity

# (bool) Keep build artifacts between builds
android.add_src =

# (str) Extra command line arguments
android.extra_args =

[buildozer]

# (str) Log level
log_level = 2

# (str) Warning if running as root
warn_on_root = 1
