---
created: 2026-08-17T14:31:04.132792
category: device-m31
tags: ["samsung", "m31", "crdroid", "magisk", "adb", "scrcpy"]
---

Samsung Galaxy M31 (SM-M315F) crDroid 12.11 (Android 16) setup completed: (1) ROM flashed via sideload in crDroid recovery (TWRP gets replaced by crDroid's own recovery on first boot — don't expect TWRP afterward); (2) adb "error: closed" on ALL commands after A16 ROMs was caused by MTP+ADB combined USB config + missing RSA authorization on user build (ro.debuggable=0, ro.adb.secure=1); fix = set persist.sys.usb.config=adb (adb-only USB) and authorize USB debugging once; (3) Magisk v30.7 flashed via recovery sideload (install from ADB, status 0), then installed Magisk APK; root grant for Shell needed manual tap in Magisk app Superuser tab (adb shell su was auto-denied). Phone has dead display+touchscreen; drive via scrcpy. m31 bootloader unlocked, patched vbmeta. Device serial RZ8NA2C1CPF.
