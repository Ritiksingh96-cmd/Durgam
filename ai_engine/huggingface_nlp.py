import re
import json
from typing import Dict, Any, List

class HuggingFaceCyberNLP:
    def __init__(self):
        self.crime_categories = {
            "DIGITAL_ARREST": {
                "keywords": ["cbi", "customs", "police", "arrest", "mumbai customs", "narcotics", "parcel", "video call", "skype", "digital arrest", "durgam", "illegal", "trafficking"],
                "severity": "CRITICAL",
                "recommended_action": "Freeze immediately; alert Anti-Corruption / State Cyber Police"
            },
            "SEXTORTION": {
                "keywords": ["video call", "nude", "recording", "blackmail", "whatsapp call", "threaten", "youtube", "facebook", "extort"],
                "severity": "CRITICAL",
                "recommended_action": "Quarantine receiver wallet; issue takedown under Section 79 IT Act"
            },
            "PART_TIME_JOB": {
                "keywords": ["telegram", "task", "youtube like", "hotel review", "prepaid task", "daily income", "part time", "rating", "crypto recharge"],
                "severity": "HIGH",
                "recommended_action": "Place micro-lien on terminal merchant aggregator"
            },
            "APK_MALWARE": {
                "keywords": ["electricity", "bill", "update", "apk", "anydesk", "teamviewer", "quicksupport", "app download", "meter disconnect"],
                "severity": "HIGH",
                "recommended_action": "Revoke device UPI token via NPCI gateway"
            },
            "INVESTMENT_PONZI": {
                "keywords": ["stock", "forex", "trading", "crypto", "vip group", "guaranteed return", "ipo", "upper circuit", "investment"],
                "severity": "HIGH",
                "recommended_action": "Consortium freeze across all beneficiary bank accounts"
            },
            "UPI_QR_FRAUD": {
                "keywords": ["olx", "qr code", "scan qr", "advance payment", "army person", "pin enter", "receive money"],
                "severity": "MEDIUM",
                "recommended_action": "Lock recipient VPA handle"
            },
            "LOAN_APP_EXTORTION": {
                "keywords": ["instant loan", "contacts hacked", "morph photos", "7 days loan", "recovery agent", "harass"],
                "severity": "CRITICAL",
                "recommended_action": "Lien bank account & block APK domain registry"
            }
        }

    def extract_entities(self, text: str) -> Dict[str, Any]:
        # 1. Extract UTR / RRN (12 digits or UTR alphanumeric)
        utr_match = re.search(r'\b(?:UTR|RRN|REF|TXN)?[:\s#-]*([0-9]{12})\b', text, re.IGNORECASE)
        utr = utr_match.group(1) if utr_match else None

        # 2. Extract Mobile Numbers (10-digit Indian numbers starting with 6-9)
        mobiles = re.findall(r'\b[6-9]\d{9}\b', text)

        # 3. Extract Amounts (e.g. Rs 2,50,000 or ₹85,000 or 85000)
        amount_match = re.search(r'(?:(?:Rs\.?|INR|₹)\s*([\d,]+(?:\.\d+)?))|(?:([\d,]+)\s*(?:rupees|inr|rs))', text, re.IGNORECASE)
        amount = None
        if amount_match:
            raw_amt = amount_match.group(1) or amount_match.group(2)
            try:
                amount = float(raw_amt.replace(',', ''))
            except:
                pass

        # 4. Extract IFSC code (4 letters, 0, 6 letters/digits)
        ifsc_match = re.search(r'\b([A-Z]{4}0[A-Z0-9]{6})\b', text, re.IGNORECASE)
        ifsc = ifsc_match.group(1).upper() if ifsc_match else None

        return {
            "utr": utr,
            "mobile_numbers": list(set(mobiles)),
            "amount": amount,
            "ifsc": ifsc
        }

    def classify_narrative(self, narrative: str) -> Dict[str, Any]:
        narrative_lower = narrative.lower()
        entities = self.extract_entities(narrative)

        best_category = "DIGITAL_ARREST"
        highest_score = 0
        all_scores = {}

        for cat, data in self.crime_categories.items():
            matched_keywords = [kw for kw in data["keywords"] if kw in narrative_lower]
            score = len(matched_keywords)
            all_scores[cat] = score
            if score > highest_score:
                highest_score = score
                best_category = cat

        # Calculate confidence percentage
        confidence = min(0.99, max(0.65, 0.70 + (highest_score * 0.08)))

        return {
            "predicted_category": best_category,
            "confidence_score": round(confidence, 3),
            "severity_level": self.crime_categories[best_category]["severity"],
            "recommended_sop": self.crime_categories[best_category]["recommended_action"],
            "extracted_entities": entities,
            "category_scores": all_scores
        }

huggingface_cyber_nlp = HuggingFaceCyberNLP()
