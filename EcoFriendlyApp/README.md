# EcoFriendlyApp(Gaiathon Build-green)

## Overview

**EcoFriendlyApp** is an Android application that empowers users in Blantyre, Malawi, to report waste issues and promote eco-conscious habits. The app features an interactive map, waste reporting system, eco tips, and user profile management, all built with a focus on sustainability and community action.

## Project Details

- **Languages**: Kotlin (Jetpack Compose for UI)
- **Dependencies**:

  - Firebase (Authentication, Firestore, Storage)
  - osmdroid (OpenStreetMap)
  - Accompanist Permissions

- **Target SDK**: 35 (Android 15)
- **Minimum SDK**: 23 (Android 6.0)

---

## Features

- **Dashboard Screen**:
  Interactive map centered on Blantyre, Malawi, with clickable waste bin markers showing coordinates. Built using `osmdroid` with OpenStreetMap tiles.

- **Report Screen**:
  Submit waste issue reports with a title, description, geolocation, and optional photo. Data is stored in Firebase Firestore; photos are uploaded to Firebase Storage.

- **Plans Screen**:
  Offers eco tips (e.g., recycling practices) and motivational messages to encourage eco-friendly living.

- **Profile Screen**:
  View and edit user information such as display name and email. Synced with Firebase Authentication.

- **User Authentication**:
  Secure sign-in via Firebase Authentication.

- **Offline Support**:
  Map tiles are cached for offline usage via osmdroid.

---

## Setup Instructions

### Prerequisites

- Android Studio (latest version)
- Java Development Kit (JDK) 17
- Android emulator or physical device (Android 6.0+)
- Firebase project with Authentication, Firestore, and Storage enabled

### Installation Steps

#### 1. Clone the Repository

```bash
git clone git@github.com:Mtendekuyokwa19/gaiathon.git

cd EcoFriendlyApp/
```

#### 2. Set Up Firebase

- Create a project on [Firebase Console](https://console.firebase.google.com/).
- Enable **Authentication**, **Firestore**, and **Storage**.
- Upgrade to the **Blaze** plan (required for Storage). A billing account is required but can be closed to avoid charges within the free tier.
- Download the `google-services.json` file and place it in the `app/` directory.

#### 3. Configure Keystore

Create a keystore:

```bash
keytool -genkeypair -v -keystore mynewkeystore.keystore -alias mynewalias \
-keyalg RSA -keysize 2048 -validity 10000
```

Update `app/build.gradle` with your keystore path, password, and alias under `signingConfigs`.

#### 4. Add Dependencies

In `app/build.gradle`, ensure the following dependencies are included:

```kotlin
implementation platform('com.google.firebase:firebase-bom:33.5.0')
implementation 'com.google.firebase:firebase-auth-ktx'
implementation 'com.google.firebase:firebase-firestore-ktx'
implementation 'com.google.firebase:firebase-storage-ktx'
implementation 'org.osmdroid:osmdroid-android:6.1.18'
implementation "com.google.accompanist:accompanist-permissions:0.34.0"
```

Sync the project.

#### 5. Update Permissions

In `AndroidManifest.xml`, add:

```xml
<uses-permission android:name="android.permission.INTERNET" />
<uses-permission android:name="android.permission.WRITE_EXTERNAL_STORAGE" />
<uses-permission android:name="android.permission.READ_EXTERNAL_STORAGE" />
```

#### 6. Build and Install the App

- Open the project in Android Studio.
- Sync Gradle files.
- Generate a signed APK via **Build > Generate Signed Bundle / APK**.
- Install the APK on your emulator or device.

---

## Usage

- **Dashboard**: View interactive map with clickable waste bin markers.
- **Report**: Submit reports with title, description, photo, and location.
- **Plans**: Access motivational eco-friendly tips.
- **Profile**: Edit display name and view user email.
- **Offline Mode**: Cached tiles allow map functionality when offline.

---

## Troubleshooting

- **Map Not Loading**: Check internet connection or pre-cache tiles. Use `adb logcat` to debug.
- **Upload Fails**: Verify `photoUri`, ensure correct Firebase rules, and confirm Blaze plan activation.
- **Install Issues**: Check `minSdk = 23`, `targetSdk = 35`, and verify keystore setup.
- **Authentication Errors**: Ensure Firebase Authentication is initialized and the user is logged in.

---
