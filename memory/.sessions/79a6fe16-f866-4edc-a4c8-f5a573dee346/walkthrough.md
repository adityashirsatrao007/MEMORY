# Walkthrough: Installed Google Chrome & Configured SDKs

All items are successfully configured with no workarounds needed.

## Actions Taken to Resolve Issues

### 1. Google Chrome Installation
- Downloaded and installed the official **Google Chrome Stable** release (`google-chrome-stable_current_amd64.deb`).
- Verified that Flutter natively detects Chrome at `google-chrome` without any path helpers.

### 2. Android Toolchain Resolution
- Configured the official **Android SDK Command-Line Tools** inside `~/Android/Sdk`.
- Installed the required API packages (`platforms;android-36`, `build-tools;36.0.0`, `build-tools;28.0.3`, and `platform-tools`).
- Accepted all licenses and set the Android SDK path in the global Flutter configuration (`flutter config --android-sdk /home/aditya/Android/Sdk`).

### 3. Linux Toolchain Driver Warnings
- Installed `mesa-utils` to resolve the `eglinfo` warning.

---

## Final Flutter Doctor Verification

```bash
$ flutter doctor -v
[✓] Flutter (Channel stable, 3.44.2, on Ubuntu 26.04 LTS 7.0.0-22-generic, locale en_US.UTF-8)
[✓] Android toolchain - develop for Android devices (Android SDK version 36.0.0)
    • Android SDK at /home/aditya/Android/Sdk
    • Platform android-36, build-tools 36.0.0
    • All Android licenses accepted.
[✓] Chrome - develop for the web
    • Chrome at google-chrome
[✓] Linux toolchain - develop for Linux desktop
    • clang version 10.0.0-4ubuntu1
    • OpenGL core renderer: llvmpipe (LLVM 21.1.8, 256 bits)
[✓] Connected device (2 available)
[✓] Network resources

• No issues found!
```
