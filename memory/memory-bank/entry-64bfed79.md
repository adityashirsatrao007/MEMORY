---
created: 2026-08-17T12:49:44.201760
category: general
tags: ["nihongo-n5", "expo", "android", "github-actions", "apk"]
---

nihongo-n5 (Expo SDK 54, RN 0.81) is a PRIVATE GitHub repo. Added .github/workflows/build-apk.yml: ubuntu runner, node22+JDK17 temurin, `npx expo prebuild --platform android --clean`, gradle assembleDebug by default (signed w/ debug key, installable ~140MB all-ABIs); if secrets ANDROID_KEYSTORE_BASE64/PASSWORD/KEY_ALIAS/KEY_PASSWORD set it builds signed assembleRelease. APK artifact: NihongoN5.apk. Downloaded build lives at ~/Desktop/Downloads/NihongoN5-debug.apk.
