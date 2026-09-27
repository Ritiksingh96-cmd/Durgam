"""
DURGAM Sovereign Bank & Branch Master Registry
Hierarchy of major Scheduled Commercial Banks in India, their operational branches, IFSC codes, and GPS coordinates.
"""

from typing import List, Dict, Any

INDIAN_BANKS_REGISTRY: List[Dict[str, Any]] = [
    {
        "bank_code": "SBI",
        "bank_name": "State Bank of India",
        "branches": [
            {"branch_code": "SBIN0001024", "branch_name": "Connaught Place Main, New Delhi", "city": "Delhi", "state": "Delhi", "lat": 28.6315, "lng": 77.2167, "manager": "Pooja Verma"},
            {"branch_code": "SBIN0000300", "branch_name": "Nariman Point Branch, Mumbai", "city": "Mumbai", "state": "Maharashtra", "lat": 18.9256, "lng": 72.8242, "manager": "Rakesh Nair"},
            {"branch_code": "SBIN0004132", "branch_name": "Koramangala 4th Block, Bengaluru", "city": "Bengaluru", "state": "Karnataka", "lat": 12.9352, "lng": 77.6245, "manager": "Sunil Hegde"},
            {"branch_code": "SBIN0001234", "branch_name": "Nuh Main Branch, Mewat", "city": "Nuh", "state": "Haryana", "lat": 28.1065, "lng": 76.9984, "manager": "Manoj Sharma"},
            {"branch_code": "SBIN0000789", "branch_name": "Town Hall Branch, Jammu", "city": "Jammu", "state": "Jammu & Kashmir", "lat": 32.7266, "lng": 74.8570, "manager": "Kavita Jamwal"}
        ]
    },
    {
        "bank_code": "PNB",
        "bank_name": "Punjab National Bank",
        "branches": [
            {"branch_code": "PUNB0014200", "branch_name": "Sansad Marg Branch, New Delhi", "city": "Delhi", "state": "Delhi", "lat": 28.6219, "lng": 77.2144, "manager": "Ashok Aggarwal"},
            {"branch_code": "PUNB0021500", "branch_name": "Nuh Highway Branch, Mewat", "city": "Nuh", "state": "Haryana", "lat": 28.1090, "lng": 77.0180, "manager": "Dharmendra Khan"},
            {"branch_code": "PUNB0038900", "branch_name": "Sector 17, Chandigarh", "city": "Chandigarh", "state": "Punjab", "lat": 30.7333, "lng": 76.7794, "manager": "Harpreet Singh"}
        ]
    },
    {
        "bank_code": "HDFC",
        "bank_name": "HDFC Bank",
        "branches": [
            {"branch_code": "HDFC0000001", "branch_name": "Sandoz House, Worli, Mumbai", "city": "Mumbai", "state": "Maharashtra", "lat": 19.0144, "lng": 72.8479, "manager": "Aditya Puri"},
            {"branch_code": "HDFC0000120", "branch_name": "Barakhamba Road, New Delhi", "city": "Delhi", "state": "Delhi", "lat": 28.6298, "lng": 77.2274, "manager": "Neha Kapur"},
            {"branch_code": "HDFC0000543", "branch_name": "HITEC City Phase 2, Hyderabad", "city": "Hyderabad", "state": "Telangana", "lat": 17.4435, "lng": 78.3772, "manager": "Kalyan Rao"},
            {"branch_code": "HDFC0000981", "branch_name": "Salt Lake Sector V, Kolkata", "city": "Kolkata", "state": "West Bengal", "lat": 22.5804, "lng": 88.4378, "manager": "Subhash Ghosh"}
        ]
    },
    {
        "bank_code": "ICICI",
        "bank_name": "ICICI Bank",
        "branches": [
            {"branch_code": "ICIC0000004", "branch_name": "Bandra Kurla Complex, Mumbai", "city": "Mumbai", "state": "Maharashtra", "lat": 19.0688, "lng": 72.8681, "manager": "Sandeep Bakhshi"},
            {"branch_code": "ICIC0000145", "branch_name": "Connaught Place Outer, New Delhi", "city": "Delhi", "state": "Delhi", "lat": 28.6341, "lng": 77.2195, "manager": "Vandana Sethi"},
            {"branch_code": "ICIC0000892", "branch_name": "Indiranagar 100ft Road, Bengaluru", "city": "Bengaluru", "state": "Karnataka", "lat": 12.9784, "lng": 77.6408, "manager": "Pradeep Kumar"}
        ]
    },
    {
        "bank_code": "CANARA",
        "bank_name": "Canara Bank",
        "branches": [
            {"branch_code": "CNRB0000182", "branch_name": "J.C. Road Head Office, Bengaluru", "city": "Bengaluru", "state": "Karnataka", "lat": 12.9610, "lng": 77.5855, "manager": "K. Satyanarayana"},
            {"branch_code": "CNRB0001948", "branch_name": "Mihijam Market Branch, Jamtara", "city": "Jamtara", "state": "Jharkhand", "lat": 23.9576, "lng": 86.8042, "manager": "Bikash Soren"},
            {"branch_code": "CNRB0002104", "branch_name": "Chandni Chowk, Delhi", "city": "Delhi", "state": "Delhi", "lat": 28.6506, "lng": 77.2303, "manager": "Alok Gupta"}
        ]
    },
    {
        "bank_code": "BOB",
        "bank_name": "Bank of Baroda",
        "branches": [
            {"branch_code": "BARB0ALHABA", "branch_name": "Alkapuri Main, Vadodara", "city": "Vadodara", "state": "Gujarat", "lat": 22.3107, "lng": 73.1812, "manager": "Sanjiv Chadha"},
            {"branch_code": "BARB0DELHIC", "branch_name": "Parliament Street, New Delhi", "city": "Delhi", "state": "Delhi", "lat": 28.6251, "lng": 77.2149, "manager": "Ritu Mehrotra"},
            {"branch_code": "BARB0JAMBOB", "branch_name": "Jamtara Main Bazaar, Jharkhand", "city": "Jamtara", "state": "Jharkhand", "lat": 23.9629, "lng": 86.8014, "manager": "Manoj Tiwari"}
        ]
    },
    {
        "bank_code": "AXIS",
        "bank_name": "Axis Bank",
        "branches": [
            {"branch_code": "UTIB0000005", "branch_name": "Worli Central, Mumbai", "city": "Mumbai", "state": "Maharashtra", "lat": 19.0028, "lng": 72.8189, "manager": "Amitabh Chaudhry"},
            {"branch_code": "UTIB0000189", "branch_name": "Cyber City Phase 3, Gurugram", "city": "Gurugram", "state": "Haryana", "lat": 28.4950, "lng": 77.0890, "manager": "Simran Chawla"}
        ]
    }
]

def get_all_registered_banks() -> List[Dict[str, Any]]:
    """Returns list of registered banks and their branches"""
    return INDIAN_BANKS_REGISTRY

def find_branch_by_ifsc(ifsc: str) -> Dict[str, Any]:
    """Find specific branch information by IFSC code"""
    for bank in INDIAN_BANKS_REGISTRY:
        for branch in bank["branches"]:
            if branch["branch_code"].upper() == ifsc.upper():
                return {
                    "bank_code": bank["bank_code"],
                    "bank_name": bank["bank_name"],
                    **branch
                }
    return None
