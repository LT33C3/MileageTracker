[app]
title = Mileage Tracker
package.name = mileagetracker
package.domain = org.test
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 0.1
requirements = python3,kivy,sqlalchemy,googlemaps
orientation = portrait
osx.python_version = 3
osx.kivy_version = 1.9.1
fullscreen = 0
android.permissions = INTERNET,ACCESS_FINE_LOCATION
android.api = 28
android.minapi = 21
android.ndk = 25b
android.sdk = 28
android.accept_sdk_license = True
android.archs = armeabi-v7a
python_version = 3.8

[buildozer]
log_level = 2
warn_on_root = 1
