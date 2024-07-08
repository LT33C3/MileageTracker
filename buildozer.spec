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
android.permissions = INTERNET
android.api = 28
android.minapi = 21
android.accept_sdk_license = True
android.archs = armeabi-v7a, arm64-v8a
p4a.branch = develop

[buildozer]
log_level = 2
warn_on_root = 1
