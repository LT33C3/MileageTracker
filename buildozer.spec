[app]
title = Mileage Tracker
package.name = mileagetracker
package.domain = org.test
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 0.1
requirements = python3==3.9.16,kivy==2.1.0
orientation = portrait
osx.python_version = 3
osx.kivy_version = 2.1.0
fullscreen = 0

# Android specific
android.permissions = INTERNET
android.api = 28
android.minapi = 21
android.accept_sdk_license = True
android.archs = armeabi-v7a, arm64-v8a

# Python-for-Android options
p4a.branch = develop
p4a.source_dir = /home/user/.buildozer/android/platform/python-for-android

# Buildozer options
[buildozer]
log_level = 2
warn_on_root = 1

# Android build-specific options
android.gradle_dependencies = 'androidx.webkit:webkit:1.4.0'
android.add_activites = com.github.kovak.webviewfilechooser.WebViewFileChooser
android.add_gradle_repositories = maven { url 'https://jitpack.io' }
android.extra_manifest_application_arguments = android:usesCleartextTraffic="true"

# Build options
build_mode = debug

# Virtual environment
virtualenv = python3

# SDL2 dependencies
sdl2_version = 2.0.22

# Other options
allow_download = True
