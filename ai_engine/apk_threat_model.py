"""
DURGAM APK Dex/Smali Opcode Sequence Threat Classifier
Specialized for detecting Banking Trojans, SMS OTP Stealers, and Accessibility Keyloggers.
Admissible under Section 66D IT Act 2000 & Section 63 BSA 2023.
"""

import re
from typing import Dict, Any, List

class APKOpcodeThreatClassifier:
    def __init__(self):
        # Critical malicious smali API signatures
        self.malicious_signatures = {
            "ACCESSIBILITY_KEYLOGGER": [
                "android.accessibilityservice.AccessibilityService",
                "performGlobalAction",
                "onAccessibilityEvent",
                "TYPE_VIEW_TEXT_CHANGED"
            ],
            "SMS_OTP_FORWARDER": [
                "android.provider.Telephony.SMS_RECEIVED",
                "getDisplayMessageBody",
                "sendTextMessage",
                "abortBroadcast"
            ],
            "OVERLAY_INJECTION_TROJAN": [
                "SYSTEM_ALERT_WINDOW",
                "WindowManager.LayoutParams.TYPE_APPLICATION_OVERLAY",
                "ACTION_MANAGE_OVERLAY_PERMISSION"
            ],
            "C2_DYNAMIC_PAYLOAD_LOADER": [
                "dalvik.system.DexClassLoader",
                "Runtime.getRuntime().exec",
                "loadClass"
            ]
        }

    def analyze_apk_metadata_and_opcodes(self, app_name: str, package_name: str, opcodes_str: str, permissions: List[str]) -> Dict[str, Any]:
        detected_categories = []
        threat_score = 0.15
        matched_indicators = []

        combined_text = f"{opcodes_str} {' '.join(permissions)} {package_name}".lower()

        for category, patterns in self.malicious_signatures.items():
            matches = [p for p in patterns if p.lower() in combined_text]
            if len(matches) >= 1:
                detected_categories.append(category)
                threat_score += 0.28
                matched_indicators.extend(matches)

        for perm in permissions:
            if "RECEIVE_SMS" in perm or "READ_SMS" in perm:
                threat_score += 0.24
                matched_indicators.append(perm)
            if "BIND_ACCESSIBILITY_SERVICE" in perm:
                threat_score += 0.32
                matched_indicators.append(perm)
            if "SYSTEM_ALERT_WINDOW" in perm:
                threat_score += 0.18
                matched_indicators.append(perm)

        threat_score = min(0.99, max(0.05, threat_score))
        is_malicious = threat_score >= 0.50

        threat_level = "CRITICAL_MALICIOUS_STEALER" if threat_score >= 0.75 else ("SUSPICIOUS_HIGH_RISK" if threat_score >= 0.50 else "BENIGN_APPLICATION")


        return {
            "app_name": app_name,
            "package_name": package_name,
            "threat_score": round(threat_score, 4),
            "threat_level": threat_level,
            "is_malicious": is_malicious,
            "detected_trojan_categories": detected_categories,
            "matched_indicators_count": len(matched_indicators),
            "critical_indicators": matched_indicators[:6],
            "statutory_action": "ISSUE_CERT_IN_ADVISORY_AND_DO_NOT_INSTALL" if is_malicious else "ALLOW_MONITORED_EXECUTION",
            "statutory_anchor": "Section 66D IT Act 2000 & Section 63 BSA 2023"
        }

apk_opcode_classifier = APKOpcodeThreatClassifier()
DalvikDexMalwareClassifier = APKOpcodeThreatClassifier
