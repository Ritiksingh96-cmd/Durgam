# DURGAM Android Mobile Application Connectivity Guide

This guide documents the technical architecture, endpoints, data contracts, and production Kotlin implementation for connecting a native Android mobile application to the DURGAM backend.

---

## 1. Architecture Overview

```
 ┌────────────────────────────────────────────────────────┐
 │                   Android Mobile App                   │
 │                                                        │
 │  ┌─────────────────┐ ┌───────────────┐ ┌─────────────┐ │
 │  │ Biometric Auth  │ │ 1-Tap SOS     │ │ Police CAD  │ │
 │  │ (BiometricPrompt│ │ Account Freeze│ │ Field Radar │ │
 │  └────────┬────────┘ └───────┬───────┘ └──────┬──────┘ │
 │           │                  │                │        │
 │  ┌────────┴──────────────────┴────────────────┴──────┐ │
 │  │           DurgamApiService (Retrofit 2)           │ │
 │  └───────────────────────────┬───────────────────────┘ │
 │                              │                         │
 │  ┌───────────────────────────┴───────────────────────┐ │
 │  │        WorkManager (Offline Sync Worker)          │ │
 │  └───────────────────────────┬───────────────────────┘ │
 └──────────────────────────────┼─────────────────────────┘
                                │ HTTPS / REST (JWT Auth)
                                ▼
 ┌────────────────────────────────────────────────────────┐
 │               DURGAM FastAPI Backend                   │
 │                  /api/v1/android/...                   │
 └────────────────────────────────────────────────────────┘
```

---

## 2. API Endpoints Reference

Base URL: `https://<your-durgam-domain>/api/v1/android` (or `http://10.0.2.2:8000/api/v1/android` on Android Emulator)

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/handshake` | Handshake & version compatibility check |
| `GET` | `/config` | UI color tokens, statutory notices, feature toggles |
| `POST` | `/devices/register` | Register FCM push notification token |
| `POST` | `/auth/login` | Citizen / Official login with Biometric option |
| `POST` | `/citizen/sos-freeze` | **1-Tap SOS Account Freeze** (< 140ms Sec 106 BNSS) |
| `GET` | `/citizen/cases/{case_id}` | Case timeline and restitution tracking |
| `POST` | `/citizen/unblock-otp` | Dissolve false-positive lien via Aadhaar OTP |
| `GET` | `/police/field-radar` | Geocoded ATM hotspots with native Google Maps Intent URIs |
| `POST` | `/police/patrol-ack` | Patrol unit dispatch acknowledgment |
| `GET` | `/bank/holds` | Bank nodal active holds queue |
| `POST` | `/sync/offline-batch` | WorkManager batch sync for low-connectivity zones |

---

## 3. Kotlin Retrofit Interface Implementation

```kotlin
package in.gov.durgam.network

import retrofit2.Response
import retrofit2.http.*

data class DeviceRegisterRequest(
    val device_id: String,
    val fcm_token: String,
    val manufacturer: String,
    val model: String,
    val os_version: String,
    val app_version: String = "2.4.0-android"
)

data class MobileLoginRequest(
    val identifier: String,
    val password: String,
    val role: String = "citizen",
    val biometric_authenticated: Boolean = false,
    val device_id: String
)

data class SosFreezeRequest(
    val victim_name: String,
    val victim_phone: String,
    val victim_account_number: String,
    val victim_ifsc: String,
    val fraud_amount: Double,
    val transaction_ref_utr: String,
    val suspected_mule_account: String? = null,
    val suspected_mule_ifsc: String? = null,
    val incident_description: String,
    val statutory_affirmation_accepted: Boolean = true
)

data class OfflineSyncItem(
    val client_uuid: String,
    val action_type: String,
    val payload: Map<String, Any>,
    val client_timestamp: String
)

data class OfflineBatchRequest(
    val device_id: String,
    val items: List<OfflineSyncItem>
)

interface DurgamApiService {

    @GET("handshake")
    suspend fun getHandshake(): Response<Map<String, Any>>

    @GET("config")
    suspend fun getMobileConfig(): Response<Map<String, Any>>

    @POST("devices/register")
    suspend fun registerDevice(@Body req: DeviceRegisterRequest): Response<Map<String, Any>>

    @POST("auth/login")
    suspend fun loginMobile(@Body req: MobileLoginRequest): Response<Map<String, Any>>

    @POST("citizen/sos-freeze")
    suspend fun triggerSosFreeze(
        @Header("Authorization") bearerToken: String?,
        @Body req: SosFreezeRequest
    ): Response<Map<String, Any>>

    @GET("citizen/cases/{caseId}")
    suspend fun getCaseDetails(
        @Header("Authorization") bearerToken: String?,
        @Path("caseId") caseId: String
    ): Response<Map<String, Any>>

    @GET("police/field-radar")
    suspend fun getPoliceFieldRadar(
        @Header("Authorization") bearerToken: String,
        @Query("city") city: String = "Delhi"
    ): Response<Map<String, Any>>

    @POST("sync/offline-batch")
    suspend fun syncOfflineBatch(
        @Header("Authorization") bearerToken: String?,
        @Body req: OfflineBatchRequest
    ): Response<Map<String, Any>>
}
```

---

## 4. Google Maps Turn-by-Turn Navigation Intent (Field Police)

The `/api/v1/android/police/field-radar` endpoint returns a ready-to-use `android_intent_uri`. Trigger native navigation in your activity or fragment with:

```kotlin
fun launchGoogleMapsNavigation(context: Context, androidIntentUri: String) {
    val navIntent = Intent(Intent.ACTION_VIEW, Uri.parse(androidIntentUri)).apply {
        setPackage("com.google.android.apps.maps")
    }
    if (navIntent.resolveActivity(context.packageManager) != null) {
        context.startActivity(navIntent)
    } else {
        val genericIntent = Intent(Intent.ACTION_VIEW, Uri.parse(androidIntentUri))
        context.startActivity(genericIntent)
    }
}
```

---

## 5. Offline Queue with Android WorkManager

When a field officer or victim is outside mobile network coverage:
1. Store the transaction or dispatch event in local Room database.
2. Schedule a one-time or periodic `CoroutineWorker` requiring `NetworkType.CONNECTED`.
3. Post the queue to `/api/v1/android/sync/offline-batch`.
