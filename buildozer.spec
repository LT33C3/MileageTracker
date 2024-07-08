[app]
title = Mileage Tracker
package.name = mileagetracker
package.domain = org.test
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 0.1
requirements = python3==3.9.16,kivy==2.1.0,requirements.txt
orientation = portrait
osx.python_version = 3
osx.kivy_version = 2.1.0
fullscreen = 0

# Android specific
android.permissions = INTERNET
android.api = 28
android.minapi = 21
android.ndk = 25b
android.sdk = 28
android.accept_sdk_license = True
android.archs = armeabi-v7a, arm64-v8a

# Python-for-Android options
p4a.branch = develop
p4a.bootstrap = sdl2

# Buildozer options
[buildozer]
log_level = 2
warn_on_root = 1

# Android build-specific options
android.gradle_dependencies = org.tensorflow:tensorflow-lite:+
android.add_gradle_repositories = maven { url 'https://google.bintray.com/tensorflow' }
android.add_packaging_options = 
    EXCLUDE META-INF/kotlin-stdlib.kotlin_module
    EXCLUDE META-INF/kotlin-stdlib-common.kotlin_module
    EXCLUDE META-INF/kotlin-stdlib-coroutines.kotlin_module
android.extra_manifest_xml = <uses-permission android:name="android.permission.INTERNET"/>

# Build options
build_mode = debug

# Virtual environment
virtualenv = python3

# SDL2 dependencies
sdl2_version = 2.0.22

# Other options
allow_download = True
log_level = 2

# Specify the Android NDK version
android.ndk_api = 21

# Specify the Java max heap size
android.gradle_daemon = True
android.accept_sdk_license = True
android.use_internet = True

# Enable AAPT2
android.enable_aapt2 = True

# Enable AndroidX
android.enable_androidx = True

# Enable Proguard
android.minify_python = False

# Enable asset packing
android.enable_asset_packing = True

# Enable Build cache
android.build_cache = True
