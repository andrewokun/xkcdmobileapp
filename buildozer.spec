[app]
title = XKCD Comic Generator
package.name = xkcdcomicgenerator
package.domain = org.aointeractive

source.dir = .
source.include_exts = py,png,jpg,kv,atlas

version = 0.1
requirements = python3,kivy,requests,urllib3,charset-normalizer,idna,certifi,openssl

orientation = portrait
fullscreen = 0
icon.filename = %(source.dir)s/icon.png

android.permissions = INTERNET
android.archs = arm64-v8a
android.api = 33
android.minapi = 21
android.accept_sdk_license = True

[buildozer]
log_level = 2
warn_on_root = 1
