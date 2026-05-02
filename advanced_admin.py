from copy import deepcopy
from datetime import datetime
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
ADVANCED_ADMIN_HTML = BASE_DIR / "iee_superadmin_advanced.html"


ADVANCED_DEFAULTS = {
    "metrics": {
        "total_workers": 5421,
        "verified_profiles": 4087,
        "active_employers": 312,
        "live_job_postings": 142,
        "total_placements": 23480,
        "wages_disbursed": 42000000,
        "micro_loans_live": 94000000,
        "contract_net_value": 84000000,
        "kyc_pending": 38,
        "ai_high_risk_flags": 3,
        "gst_defaults": 14,
        "avg_time_to_fill_hours": 1.8,
        "live_contracts": 142,
        "workers_deployed": 4087,
        "avg_daily_rate": 1240,
        "wage_diversion_per_day": 14400,
        "unread_alerts": 12,
    },
    "health": [
        {"label": "Worker Verification Rate", "value": 75.4, "tone": "pg2"},
        {"label": "Job Fill Rate", "value": 94.0, "tone": "pi"},
        {"label": "EPFO Compliance (Employers)", "value": 95.5, "tone": "pg2"},
        {"label": "GST Filing Rate", "value": 97.4, "tone": "pb2"},
        {"label": "Salary On-Time Rate", "value": 98.8, "tone": "pg2"},
        {"label": "Contract Compliance", "value": 88.0, "tone": "pa"},
        {"label": "eShram UAN Link Rate", "value": 67.3, "tone": "pb2"},
        {"label": "AI Anomaly Resolution", "value": 82.0, "tone": "ppu"},
    ],
    "alerts": [
        {
            "title": "AI ALERT — Contract Fraud Pattern Detected",
            "body": "IEE-CTR-2026-0044 — Annur Infra showing worker count mismatch vs GST turnover. AI confidence: 94%",
            "time": "1 min",
            "unread": True,
        },
        {
            "title": "EPFO ECR Default — Ram Nivas Contractors",
            "body": "March 2026 ECR not filed — 34 workers affected — principal employer liability triggered",
            "time": "8 min",
            "unread": True,
        },
        {
            "title": "Micro-Loan Disbursement Ready",
            "body": "Rs 14.2L approved across 48 workers — NBFC IDFC First — awaiting SA authorisation",
            "time": "22 min",
            "unread": True,
        },
        {
            "title": "eShram UAN Link — 412 New Workers",
            "body": "412 workers linked eShram UAN to IEE Worker ID this week — NDUW sync complete",
            "time": "1 hr",
            "unread": True,
        },
        {
            "title": "KYC Queue — 38 Pending",
            "body": "Zone 3 North Chennai — verifier capacity exceeded — recommend overflow assignment",
            "time": "2 hr",
            "unread": True,
        },
        {
            "title": "GST Non-Filing — 8 Employers",
            "body": "GST-3B not filed for March 2026 — automated notice issued to 8 employers",
            "time": "3 hr",
            "unread": True,
        },
        {
            "title": "Salary Batch Rs 1.84Cr — Pending Auth",
            "body": "April 2026 payroll ready — 4,064 workers — DBT channel",
            "time": "4 hr",
            "unread": False,
        },
        {
            "title": "PM-SAYSAM Scheme — 4,087 Enrolled",
            "body": "97.2% delivery — Rs 2.04 Crore benefit value launched",
            "time": "Yesterday",
            "unread": False,
        },
    ],
    "live_feed": [
        {
            "tone": "g",
            "title": "<strong>Rajan Kumar</strong> placement confirmed — Skyline Constructions, Mason L3, Rs 850/day — eShram UAN linked",
            "meta": "Just now — Chennai",
        },
        {
            "tone": "r",
            "title": "<strong>AI Flag:</strong> Annur Infra GST turnover (Rs 1.2Cr) vs 55 workers deployed — expected GST minimum Rs 2.4Cr — mismatch Rs 1.2Cr — fraud risk: HIGH",
            "meta": "2 min ago — AI Engine",
        },
        {
            "tone": "b",
            "title": "<strong>Micro-loan approved:</strong> Mohammed Rafi — Rs 18,000 at 12% via IDFC First NBFC — 3-month repayment — IEE income verified",
            "meta": "5 min ago — Finance Engine",
        },
        {
            "tone": "a",
            "title": "<strong>EPFO ECR filed:</strong> Skyline Constructions — 148 workers — TRRN: EPFO2026041200148 — Rs 1.78L PF deposited",
            "meta": "12 min ago — EPFO Sync",
        },
        {
            "tone": "r",
            "title": "<strong>Ram Nivas Contractors</strong> EPFO ECR default — March 2026 — 34 workers unprotected — principal employer notice triggered",
            "meta": "18 min ago — Compliance Engine",
        },
        {
            "tone": "p",
            "title": "<strong>PMKVY Sync:</strong> 61 new certifications from Nihar Skills mapped to IEE Worker IDs — Skill India Digital Hub confirmed",
            "meta": "1 hr ago — NSDC Sync",
        },
    ],
    "worker_registry": [
        {
            "worker_id": "IEE-WK-00045821",
            "name": "Rajan Kumar",
            "role": "Construction Mason",
            "level": "L3 Skilled",
            "city": "Chennai",
            "eshram_uan": "WB-TN-2819043821",
            "epfo_uan": "100000004821",
            "esic_status": "Active",
            "risk_score": 4,
            "jobs_completed": 23,
            "earnings": 42800,
            "status": "Verified",
            "aadhaar_last4": "4821",
            "bank_account": "SBI — XXXX 4821",
            "ytd_earnings": 394200,
            "active_loan": 18000,
            "pf_balance": 47240,
            "flags": ["Verified", "eShram Linked", "EPFO Active", "ESIC Covered"],
        },
        {
            "worker_id": "IEE-WK-00047201",
            "name": "Murugan S",
            "role": "Electrician",
            "level": "L3 Skilled",
            "city": "Coimbatore",
            "eshram_uan": "WB-TN-2819047201",
            "epfo_uan": "100000047201",
            "esic_status": "Active",
            "risk_score": 6,
            "jobs_completed": 31,
            "earnings": 55200,
            "status": "Verified",
            "aadhaar_last4": "7201",
            "bank_account": "Indian Bank — XXXX 7201",
            "ytd_earnings": 468400,
            "active_loan": 25000,
            "pf_balance": 58220,
            "flags": ["Verified", "eShram Linked", "EPFO Active", "ESIC Covered"],
        },
        {
            "worker_id": "IEE-WK-00091",
            "name": "Ganesh Kumar",
            "role": "Mason",
            "level": "L1 Unskilled",
            "city": "Chennai",
            "eshram_uan": "",
            "epfo_uan": "",
            "esic_status": "Pending",
            "risk_score": 41,
            "jobs_completed": 0,
            "earnings": 0,
            "status": "KYC Pending",
            "aadhaar_last4": "",
            "bank_account": "",
            "ytd_earnings": 0,
            "active_loan": 0,
            "pf_balance": 0,
            "flags": ["KYC Pending"],
        },
        {
            "worker_id": "IEE-WK-00094",
            "name": "Lakshmi Bai",
            "role": "Cook",
            "level": "L2 Semi-Skilled",
            "city": "Madurai",
            "eshram_uan": "WB-TN-2819000094",
            "epfo_uan": "100000000094",
            "esic_status": "Active",
            "risk_score": 9,
            "jobs_completed": 8,
            "earnings": 18400,
            "status": "Verified",
            "aadhaar_last4": "0094",
            "bank_account": "Canara Bank — XXXX 0094",
            "ytd_earnings": 108600,
            "active_loan": 0,
            "pf_balance": 14820,
            "flags": ["Verified", "eShram Linked", "ESIC Covered"],
        },
    ],
    "employer_registry": [
        {
            "employer_id": "EMP-TN-001248",
            "company": "Skyline Constructions",
            "gstin": "33AABCS1234Z1Z5",
            "epfo_code": "TN/CHN/001248",
            "esic_code": "33-00-001248",
            "workers": 148,
            "contracts": 3,
            "risk_score": 12,
            "compliance_pct": 100.0,
            "sector": "Construction",
            "city": "Chennai",
            "contact_person": "M. Suresh",
            "contact_mobile": "+91 98840 11248",
        },
        {
            "employer_id": "EMP-TN-009912",
            "company": "Ram Nivas Contractors",
            "gstin": "33AAFRN4421C1Z2",
            "epfo_code": "TN/CHN/009912",
            "esic_code": "33-00-009912",
            "workers": 34,
            "contracts": 1,
            "risk_score": 91,
            "compliance_pct": 41.0,
            "sector": "Construction",
            "city": "Chennai",
            "contact_person": "R. Nivas",
            "contact_mobile": "+91 98710 99120",
        },
        {
            "employer_id": "EMP-TN-003380",
            "company": "Annur Infra",
            "gstin": "33AACIA9988B1Z9",
            "epfo_code": "TN/CBE/003380",
            "esic_code": "33-00-003380",
            "workers": 55,
            "contracts": 1,
            "risk_score": 94,
            "compliance_pct": 0.0,
            "sector": "Infrastructure",
            "city": "Coimbatore",
            "contact_person": "K. Sundaram",
            "contact_mobile": "+91 98650 33800",
        },
        {
            "employer_id": "EMP-TN-004499",
            "company": "Metro Works (CMRL)",
            "gstin": "33AABCM2200H1Z4",
            "epfo_code": "TN/CHN/004499",
            "esic_code": "33-00-004499",
            "workers": 220,
            "contracts": 2,
            "risk_score": 8,
            "compliance_pct": 98.6,
            "sector": "Construction",
            "city": "Chennai",
            "contact_person": "R. Krishnamurthy",
            "contact_mobile": "+91 98110 44990",
        },
    ],
    "contracts": [
        {
            "contract_id": "IEE-CTR-2026-0092",
            "title": "CMRL Phase 2 — Foundation and Concrete Work",
            "principal_employer": "Chennai Metro Rail Ltd",
            "contractor": "Metro Works Pvt Ltd",
            "handler": "R. Krishnamurthy, PM",
            "contract_value": 20900000,
            "workers_deployed": 220,
            "epfo_workers": 220,
            "worker_rate": 950,
            "client_rate": 1045,
            "start_date": "01 Mar 2026",
            "end_date": "31 Aug 2026",
            "license_no": "TN-2026-0044",
            "compliance_pct": 98.6,
            "rating": 4.8,
            "april_payment": 2090000,
            "ai_flags": 0,
            "risk_score": 8,
            "wage_diversion_per_day": 0,
            "estimated_misuse": 0,
            "status_label": "Live",
            "status_tone": "bg",
            "secondary_badge": "",
        },
        {
            "contract_id": "IEE-CTR-2026-0044",
            "title": "Annur Infra — Electrical and Civil Work, Coimbatore",
            "principal_employer": "Annur Municipal Corp",
            "contractor": "Annur Infra",
            "handler": "K. Sundaram, Director",
            "contract_value": 4800000,
            "workers_deployed": 55,
            "epfo_workers": 21,
            "worker_rate": 900,
            "client_rate": 1100,
            "start_date": "15 Jan 2026",
            "end_date": "15 Jul 2026",
            "license_no": "Not Filed",
            "compliance_pct": 0.0,
            "rating": 0.0,
            "april_payment": 0,
            "ai_flags": 2,
            "risk_score": 94,
            "wage_diversion_per_day": 14400,
            "estimated_misuse": 1296000,
            "status_label": "AI Flagged",
            "status_tone": "br",
            "secondary_badge": "Fraud Risk",
        },
        {
            "contract_id": "IEE-CTR-2026-0067",
            "title": "Prestige Builders — Residential Complex, Mumbai",
            "principal_employer": "Prestige Projects Pvt Ltd",
            "contractor": "Prestige Builders",
            "handler": "P. Menon, Site Director",
            "contract_value": 7200000,
            "workers_deployed": 72,
            "epfo_workers": 72,
            "worker_rate": 650,
            "client_rate": 850,
            "start_date": "01 Feb 2026",
            "end_date": "31 Jul 2026",
            "license_no": "MH-2026-0021",
            "compliance_pct": 76.0,
            "rating": 4.2,
            "april_payment": 576000,
            "ai_flags": 1,
            "risk_score": 87,
            "wage_diversion_per_day": 14400,
            "estimated_misuse": 864000,
            "status_label": "Under Review",
            "status_tone": "ba",
            "secondary_badge": "",
        },
    ],
    "broadcast_history": [
        {"title": "PM-SAYSAM Scheme Launch", "recipients": 5421, "delivery_pct": 97.2, "date": "18 Apr 2026", "status": "Sent"},
        {"title": "eShram-IEE Integration Live", "recipients": 5421, "delivery_pct": 95.8, "date": "15 Apr 2026", "status": "Sent"},
        {"title": "EPFO Default Notice — Workers", "recipients": 34, "delivery_pct": 100.0, "date": "12 Apr 2026", "status": "Sent"},
        {"title": "IEE App — Download Now", "recipients": 5421, "delivery_pct": 98.4, "date": "01 Apr 2026", "status": "Sent"},
    ],
    "salary_batch": {
        "batch_id": "SAL-APR-2026-01",
        "amount": 18400000,
        "workers": 4064,
        "status": "Pending Auth",
        "last_processed": "",
    },
    "journeys": {
        "IEE-WK-00045821": {
            "worker_id": "IEE-WK-00045821",
            "name": "Rajan Kumar",
            "avatar": "RK",
            "role": "Construction Mason",
            "level": "L3 Skilled",
            "city": "Chennai, Tamil Nadu",
            "eshram_uan": "WB-TN-2819043821",
            "aadhaar_last4": "4821",
            "epfo_uan": "100000004821",
            "esic_ip": "31-00-046821-000",
            "bank_account": "SBI — XXXX 4821",
            "risk_score": 4,
            "risk_label": "Low",
            "flags": ["Verified", "eShram Linked", "EPFO Active", "ESIC Covered"],
            "financials": {
                "month": 42800,
                "ytd": 394200,
                "loan": 18000,
                "pf_balance": 47240,
                "gross": 42800,
                "pf_deduction": 2880,
                "esic_deduction": 321,
                "loan_emi": 6200,
                "take_home": 33399,
            },
            "timeline": [
                {"tone": "grn", "step": "1", "title": "Registration on IEE Platform", "description": "Registered via CSC MeeSeva, Chennai. Documents submitted: Aadhaar, Voter ID. eShram UAN linked: WB-TN-2819043821.", "meta": ["10 Apr 2026", "Via CSC Centre, Ambattur", "IP: 103.38.50.201"], "tags": []},
                {"tone": "acc", "step": "2", "title": "KYC Verification — Field Approved", "description": "Field verifier S. Anbarasan (Zone 3) verified physical presence. Aadhaar biometric confirmed. NDUW eShram DB cross-referenced — no duplicates.", "meta": ["11 Apr 2026", "Verifier: IEE-VRF-2026-001"], "tags": []},
                {"tone": "blu", "step": "3", "title": "Worker ID Issued — Level 3 Skilled", "description": "IEE Worker ID Card generated with QR code. Skill level set to L3 based on PMKVY Advanced Masonry certificate from Nihar Skills Education.", "meta": ["11 Apr 2026", "Cert: NSDC-TN-PMKVY-2024-09821"], "tags": ["PMKVY Certified", "Nihar Skills", "L3 Skilled"]},
                {"tone": "pur", "step": "4", "title": "Job Matching — AI Engine Assigned", "description": "System matched to 5 jobs within 3 km. Notification sent via App + WhatsApp. Brick Mason — Skyline Constructions, 1.2 km, Rs 850/day — accepted in 4 minutes.", "meta": ["12 Apr 2026", "Match score: 94%", "Accepted in 4 min"], "tags": []},
                {"tone": "grn", "step": "5", "title": "Placement Confirmed — Skyline Constructions", "description": "Contract IEE-CTR-2026-0088: 3-day assignment. GPS check-in enabled. Daily wage Rs 850 confirmed on IEE platform.", "meta": ["13 Apr 2026", "Rs 2,550 expected", "CLRA compliant"], "tags": []},
                {"tone": "grn", "step": "6", "title": "EPFO Enrolment — PF UAN Issued", "description": "Auto-enrolled on first placement. PF UAN: 100000004821. ECR filed by Skyline for this worker.", "meta": ["13 Apr 2026", "EPFO Code: TN/CHN/001248"], "tags": []},
                {"tone": "tel", "step": "7", "title": "ESIC Coverage Activated", "description": "Auto-enrolled under ESIC with active medical coverage for the assignment period.", "meta": ["13 Apr 2026", "ESIC Sub-Code: TN-CHN-014"], "tags": []},
                {"tone": "grn", "step": "8", "title": "Assignment Completed + Rated", "description": "3-day assignment complete. 4.9/5 by employer. Earnings Rs 2,550 disbursed via DBT.", "meta": ["16 Apr 2026", "Rating: 4.9/5", "DBT: Rs 2,550"], "tags": []},
                {"tone": "blu", "step": "9", "title": "Micro-Loan Pre-Approved", "description": "Based on consistent income and completed assignments, a micro-loan of Rs 18,000 was pre-approved via IEE finance partners.", "meta": ["18 Apr 2026", "NBFC: IDFC First", "Tenure: 3 months"], "tags": []},
                {"tone": "pur", "step": "10", "title": "eShram Welfare Benefits Activated", "description": "PMSBY and PM-SYM checks completed with IEE-linked eligibility assistance.", "meta": ["19 Apr 2026", "PMSBY: Active", "PM-SYM: Active"], "tags": []},
            ],
        },
        "IEE-WK-00047201": {
            "worker_id": "IEE-WK-00047201",
            "name": "Murugan S",
            "avatar": "MS",
            "role": "Electrician",
            "level": "L3 Skilled",
            "city": "Coimbatore, Tamil Nadu",
            "eshram_uan": "WB-TN-2819047201",
            "aadhaar_last4": "7201",
            "epfo_uan": "100000047201",
            "esic_ip": "31-00-047201-000",
            "bank_account": "Indian Bank — XXXX 7201",
            "risk_score": 6,
            "risk_label": "Low",
            "flags": ["Verified", "eShram Linked", "EPFO Active", "ESIC Covered"],
            "financials": {
                "month": 55200,
                "ytd": 468400,
                "loan": 25000,
                "pf_balance": 58220,
                "gross": 55200,
                "pf_deduction": 3640,
                "esic_deduction": 414,
                "loan_emi": 8500,
                "take_home": 42646,
            },
            "timeline": [
                {"tone": "grn", "step": "1", "title": "Registration on IEE Platform", "description": "Registered via field induction camp in Coimbatore with Aadhaar and bank proof.", "meta": ["02 Apr 2026", "Via Field Camp, Coimbatore"], "tags": []},
                {"tone": "acc", "step": "2", "title": "KYC Verification Approved", "description": "Verifier confirmed identity and address. eShram link established successfully.", "meta": ["03 Apr 2026", "Verifier: IEE-VRF-2026-001"], "tags": []},
                {"tone": "blu", "step": "3", "title": "Electrical Safety Certification Mapped", "description": "NSDC certificate mapped to IEE profile and level updated to L3 Skilled.", "meta": ["04 Apr 2026", "Cert mapped"], "tags": ["NSDC", "Electrical", "L3 Skilled"]},
                {"tone": "grn", "step": "4", "title": "Metro Works Placement Confirmed", "description": "Assigned to a multi-week site role with verified wages and shift roster.", "meta": ["06 Apr 2026", "Rs 920/day"], "tags": []},
                {"tone": "grn", "step": "5", "title": "Payroll and Benefits Active", "description": "PF, ESIC, and DBT payment rails activated with salary history now visible in IEE.", "meta": ["11 Apr 2026", "Payroll active"], "tags": []},
            ],
        },
        "IEE-WK-00091": {
            "worker_id": "IEE-WK-00091",
            "name": "Ganesh Kumar",
            "avatar": "GK",
            "role": "Mason",
            "level": "L1 Unskilled",
            "city": "Chennai, Tamil Nadu",
            "eshram_uan": "",
            "aadhaar_last4": "",
            "epfo_uan": "",
            "esic_ip": "",
            "bank_account": "",
            "risk_score": 41,
            "risk_label": "Medium",
            "flags": ["KYC Pending"],
            "financials": {
                "month": 0,
                "ytd": 0,
                "loan": 0,
                "pf_balance": 0,
                "gross": 0,
                "pf_deduction": 0,
                "esic_deduction": 0,
                "loan_emi": 0,
                "take_home": 0,
            },
            "timeline": [
                {"tone": "acc", "step": "1", "title": "Registration Captured", "description": "Worker profile created and submitted for verification from a local registration drive.", "meta": ["18 Apr 2026", "Pending KYC"], "tags": []},
                {"tone": "red", "step": "2", "title": "Verification Pending", "description": "Aadhaar proof and bank details still pending. Verifier queue action required before activation.", "meta": ["Awaiting verifier", "Zone 3 queue"], "tags": ["KYC Pending"]},
            ],
        },
    },
    "selected_scheme": "PM-SAYSAM — Wage Insurance",
}


def _merge_defaults(target, defaults):
    changed = False
    for key, value in defaults.items():
        if key not in target:
            target[key] = deepcopy(value)
            changed = True
        elif isinstance(value, dict) and isinstance(target.get(key), dict):
            changed = _merge_defaults(target[key], value) or changed
    return changed


def _derive_worker_row(user, worker_record=None):
    city = user.get("city") or (worker_record or {}).get("city") or "Tamil Nadu"
    role = user.get("occupation") or (worker_record or {}).get("occupation") or "General Labour"
    rating = str(user.get("rating") or (worker_record or {}).get("rating") or "New")
    risk_score = 8 if user.get("status") == "Active" else 41
    status = "Verified" if user.get("status") == "Active" else user.get("status", "KYC Pending")
    row = {
        "worker_id": user.get("iee_id", ""),
        "name": user.get("name", "Worker"),
        "role": role,
        "level": "L2 Semi-Skilled" if status == "Verified" else "L1 Unskilled",
        "city": city.split(",")[0],
        "eshram_uan": "",
        "epfo_uan": "",
        "esic_status": "Active" if status == "Verified" else "Pending",
        "risk_score": risk_score,
        "jobs_completed": int(user.get("jobs_completed", 0)),
        "earnings": 0 if status != "Verified" else 2400 * max(int(user.get("jobs_completed", 0)), 1),
        "status": status,
        "aadhaar_last4": "",
        "bank_account": "",
        "ytd_earnings": 0 if status != "Verified" else 16000 * max(int(user.get("jobs_completed", 0)), 1),
        "active_loan": 0,
        "pf_balance": 0 if status != "Verified" else 2800 * max(int(user.get("jobs_completed", 0)), 1),
        "flags": ["Verified"] if status == "Verified" else [status],
        "rating": rating,
    }
    return row


def _derive_queue_worker_row(queue_item):
    return {
        "worker_id": queue_item.get("iee_id", ""),
        "name": queue_item.get("name", "Worker"),
        "role": queue_item.get("role", "Worker"),
        "level": "L1 Unskilled",
        "city": "Tamil Nadu",
        "eshram_uan": "",
        "epfo_uan": "",
        "esic_status": "Pending",
        "risk_score": 41 if queue_item.get("priority") == "HIGH" else 27,
        "jobs_completed": 0,
        "earnings": 0,
        "status": "KYC Pending" if queue_item.get("status") == "Pending" else queue_item.get("status", "Pending"),
        "aadhaar_last4": "",
        "bank_account": "",
        "ytd_earnings": 0,
        "active_loan": 0,
        "pf_balance": 0,
        "flags": [queue_item.get("status", "Pending")],
        "rating": "New",
    }


def _derive_employer_row(user):
    return {
        "employer_id": user.get("employer_id", ""),
        "company": user.get("name", "Employer"),
        "gstin": "",
        "epfo_code": "",
        "esic_code": "",
        "workers": 12 if user.get("status") == "Active" else 0,
        "contracts": 1,
        "risk_score": 18 if user.get("status") == "Active" else 86,
        "compliance_pct": 96.0 if user.get("status") == "Active" else 45.0,
        "sector": user.get("sector", "Other"),
        "city": user.get("city", "Tamil Nadu"),
        "contact_person": user.get("name", "Employer"),
        "contact_mobile": user.get("mobile") or "",
    }


def _ensure_worker_journey(adv, row):
    worker_id = row.get("worker_id")
    if not worker_id:
        return False
    if worker_id in adv["journeys"]:
        return False
    adv["journeys"][worker_id] = {
        "worker_id": worker_id,
        "name": row.get("name", "Worker"),
        "avatar": "".join(part[:1] for part in row.get("name", "Worker").split()[:2]).upper() or "WK",
        "role": row.get("role", "Worker"),
        "level": row.get("level", "L1 Unskilled"),
        "city": row.get("city", "Tamil Nadu"),
        "eshram_uan": row.get("eshram_uan", ""),
        "aadhaar_last4": row.get("aadhaar_last4", ""),
        "epfo_uan": row.get("epfo_uan", ""),
        "esic_ip": "",
        "bank_account": row.get("bank_account", ""),
        "risk_score": row.get("risk_score", 22),
        "risk_label": "Low" if row.get("risk_score", 22) < 20 else "Medium",
        "flags": row.get("flags", []),
        "financials": {
            "month": row.get("earnings", 0),
            "ytd": row.get("ytd_earnings", 0),
            "loan": row.get("active_loan", 0),
            "pf_balance": row.get("pf_balance", 0),
            "gross": row.get("earnings", 0),
            "pf_deduction": 0,
            "esic_deduction": 0,
            "loan_emi": 0,
            "take_home": row.get("earnings", 0),
        },
        "timeline": [
            {
                "tone": "acc",
                "step": "1",
                "title": "Profile Created in IEE",
                "description": "Worker was registered on the platform and is awaiting the next operational step.",
                "meta": [datetime.now().strftime("%d %b %Y"), "Created from live admin console"],
                "tags": row.get("flags", []),
            }
        ],
    }
    return True


def ensure_advanced_state(state):
    advanced = state.setdefault("advanced", {})
    changed = _merge_defaults(advanced, ADVANCED_DEFAULTS)

    worker_registry = advanced.setdefault("worker_registry", [])
    worker_index = {row.get("worker_id"): row for row in worker_registry if row.get("worker_id")}
    worker_lookup = {row.get("iee_id"): row for row in state.get("workers", [])}

    for user in state.get("users", []):
        if user.get("role") != "worker" or not user.get("iee_id"):
            continue
        row = worker_index.get(user["iee_id"])
        derived = _derive_worker_row(user, worker_lookup.get(user["iee_id"]))
        if row is None:
            worker_registry.append(derived)
            worker_index[user["iee_id"]] = worker_registry[-1]
            changed = True
        else:
            for key, value in derived.items():
                if row.get(key) in (None, "", [], 0) and value not in (None, "", [], 0):
                    row[key] = value
                    changed = True
            next_name = user.get("name", row["name"])
            next_city = (user.get("city") or row["city"]).split(",")[0]
            next_status = "Verified" if user.get("status") == "Active" else user.get("status", row["status"])
            next_jobs_completed = int(user.get("jobs_completed", row.get("jobs_completed", 0)))
            next_risk_score = 8 if next_status == "Verified" else max(row.get("risk_score", 22), 22)
            if row.get("name") != next_name:
                row["name"] = next_name
                changed = True
            if row.get("city") != next_city:
                row["city"] = next_city
                changed = True
            if row.get("status") != next_status:
                row["status"] = next_status
                changed = True
            if row.get("jobs_completed") != next_jobs_completed:
                row["jobs_completed"] = next_jobs_completed
                changed = True
            if row.get("risk_score") != next_risk_score:
                row["risk_score"] = next_risk_score
                changed = True
        changed = _ensure_worker_journey(advanced, worker_index[user["iee_id"]]) or changed

    for queue_item in state.get("verification_queue", []):
        queue_id = queue_item.get("iee_id")
        if queue_id and queue_id not in worker_index:
            row = _derive_queue_worker_row(queue_item)
            worker_registry.append(row)
            worker_index[queue_id] = row
            changed = True
            changed = _ensure_worker_journey(advanced, row) or changed

    employer_registry = advanced.setdefault("employer_registry", [])
    employer_index = {row.get("employer_id"): row for row in employer_registry if row.get("employer_id")}
    for user in state.get("users", []):
        if user.get("role") != "employer" or not user.get("employer_id"):
            continue
        row = employer_index.get(user["employer_id"])
        derived = _derive_employer_row(user)
        if row is None:
            employer_registry.append(derived)
            employer_index[user["employer_id"]] = employer_registry[-1]
            changed = True
        else:
            next_company = user.get("name", row["company"])
            next_sector = user.get("sector", row.get("sector", "Other"))
            next_city = user.get("city", row.get("city", "Tamil Nadu"))
            next_contact_mobile = user.get("mobile") or row.get("contact_mobile", "")
            if row.get("company") != next_company:
                row["company"] = next_company
                changed = True
            if row.get("sector") != next_sector:
                row["sector"] = next_sector
                changed = True
            if row.get("city") != next_city:
                row["city"] = next_city
                changed = True
            if row.get("contact_mobile") != next_contact_mobile:
                row["contact_mobile"] = next_contact_mobile
                changed = True
            if user.get("status") == "Flagged":
                next_risk_score = max(row.get("risk_score", 0), 91)
                next_compliance_pct = min(row.get("compliance_pct", 100.0), 41.0)
                if row.get("risk_score") != next_risk_score:
                    row["risk_score"] = next_risk_score
                    changed = True
                if row.get("compliance_pct") != next_compliance_pct:
                    row["compliance_pct"] = next_compliance_pct
                    changed = True

    advanced["worker_registry"] = sorted(worker_registry, key=lambda row: row.get("worker_id", ""), reverse=True)
    advanced["employer_registry"] = sorted(employer_registry, key=lambda row: row.get("employer_id", ""), reverse=True)
    advanced["contracts"] = sorted(advanced["contracts"], key=lambda row: row.get("contract_id", ""), reverse=True)
    return changed


def advanced_dashboard_payload(state, current_user=None):
    advanced = state["advanced"]
    metrics = advanced["metrics"]
    unread_alerts = sum(1 for item in advanced["alerts"] if item.get("unread"))
    metrics["unread_alerts"] = unread_alerts
    metrics["kyc_pending"] = max(metrics.get("kyc_pending", 0), sum(1 for item in advanced["worker_registry"] if "Pending" in item.get("status", "")))

    high_risk_contracts = sum(1 for item in advanced["contracts"] if item.get("risk_score", 0) >= 80)
    metrics["ai_high_risk_flags"] = max(metrics.get("ai_high_risk_flags", 0), high_risk_contracts)

    summary = (
        f"{metrics['ai_high_risk_flags']} high-risk contracts flagged. "
        f"{metrics['gst_defaults']} compliance defaults need review. "
        f"{metrics['kyc_pending']} KYC cases are still pending field action."
    )
    detail = (
        f"AI Engine processed 84,210 data points in the last 6 hours across contracts, wages, compliance, "
        f"identity links, and payroll records. Next scheduled scan: {datetime.now().strftime('%H:00')} IST."
    )
    return {
        "ok": True,
        "generatedAt": datetime.now().strftime("%d %B %Y, %H:%M IST"),
        "user": {
            "name": current_user.get("name", "Super Administrator") if current_user else "Super Administrator",
            "role": current_user.get("role", "superadmin") if current_user else "superadmin",
        },
        "metrics": metrics,
        "health": advanced["health"],
        "alerts": advanced["alerts"][:12],
        "liveFeed": advanced["live_feed"][:12],
        "workers": advanced["worker_registry"][:20],
        "employers": advanced["employer_registry"][:20],
        "contracts": advanced["contracts"][:10],
        "journeys": advanced["journeys"],
        "broadcastHistory": advanced["broadcast_history"][:12],
        "auditLog": state.get("audit_log", [])[:20],
        "salaryBatch": advanced["salary_batch"],
        "selectedScheme": advanced.get("selected_scheme", ADVANCED_DEFAULTS["selected_scheme"]),
        "aiSummary": summary,
        "aiDetail": detail,
    }


def build_advanced_admin_page():
    html = ADVANCED_ADMIN_HTML.read_text(encoding="utf-8", errors="replace")
    injection = f"<script>{ADVANCED_ADMIN_SCRIPT}</script>"
    if "</body>" in html:
        html = html.replace("</body>", injection + "</body>")
    else:
        html += injection
    return html.encode("utf-8", errors="replace")


def build_advanced_gate_page():
    html = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>IEE Superadmin Access</title>
  <style>
    :root{--ink:#0c1a28;--ink2:#1b3150;--acc:#b07000;--acc2:#8a5500;--bd:#d7e0ea;--bg:#f4f7fb;--w:#fff;--muted:#607892;--err:#8b1515}
    *{box-sizing:border-box}
    body{margin:0;min-height:100vh;font-family:'Segoe UI',system-ui,sans-serif;background:linear-gradient(135deg,#071524,#10304d);display:grid;place-items:center;padding:24px}
    .card{width:min(420px,100%);background:rgba(255,255,255,.98);border-radius:12px;padding:28px 24px;box-shadow:0 24px 64px rgba(0,0,0,.35)}
    h1{margin:0 0 8px;font-size:24px;color:var(--ink)}
    p{margin:0 0 18px;color:var(--muted);line-height:1.6}
    label{display:block;font-size:12px;font-weight:700;letter-spacing:.04em;color:var(--ink2);text-transform:uppercase;margin:0 0 6px}
    input{width:100%;padding:11px 12px;border:1px solid var(--bd);border-radius:8px;font:inherit;margin:0 0 14px}
    input:focus{outline:none;border-color:#2c6cb0;box-shadow:0 0 0 3px rgba(44,108,176,.12)}
    button{width:100%;padding:11px 14px;border:none;border-radius:8px;background:var(--acc);color:var(--w);font:700 14px 'Segoe UI',system-ui,sans-serif;cursor:pointer}
    button:hover{background:var(--acc2)}
    .hint{margin-top:14px;font-size:12px;color:var(--muted)}
    .status{display:none;margin-top:12px;padding:10px 12px;border-radius:8px;background:#fbeaea;color:var(--err);font-size:13px}
    .status.on{display:block}
    code{background:#eef3f8;padding:2px 5px;border-radius:4px}
  </style>
</head>
<body>
  <div class="card">
    <h1>Superadmin Access</h1>
    <p>Sign in to open the live advanced intelligence console wired to the current IEE backend.</p>
    <form id="gate-form">
      <label for="gate-email">Administrator ID</label>
      <input id="gate-email" type="email" value="superadmin@iee.gov.in" autocomplete="username">
      <label for="gate-password">Password</label>
      <input id="gate-password" type="password" value="Admin@IEE2026" autocomplete="current-password">
      <button type="submit" id="gate-submit">Open Advanced Console</button>
    </form>
    <div class="status" id="gate-status"></div>
    <div class="hint">After login, you’ll be redirected to <code>/superadmin/advanced</code>.</div>
  </div>
  <script>
    const form = document.getElementById('gate-form');
    const status = document.getElementById('gate-status');
    const submit = document.getElementById('gate-submit');
    form.addEventListener('submit', async (event) => {
      event.preventDefault();
      status.classList.remove('on');
      submit.disabled = true;
      submit.textContent = 'Opening...';
      try {
        const response = await fetch('/api/admin/login', {
          method: 'POST',
          credentials: 'same-origin',
          headers: {'Content-Type':'application/json'},
          body: JSON.stringify({
            identifier: document.getElementById('gate-email').value.trim(),
            password: document.getElementById('gate-password').value.trim(),
          })
        });
        const data = await response.json();
        if (!response.ok || !data.ok) throw new Error(data.message || 'Access denied.');
        location.href = '/superadmin/advanced';
      } catch (error) {
        status.textContent = error.message || 'Unable to sign in.';
        status.classList.add('on');
        submit.disabled = false;
        submit.textContent = 'Open Advanced Console';
      }
    });
  </script>
</body>
</html>"""
    return html.encode("utf-8")


ADVANCED_ADMIN_SCRIPT = r"""
(function(){
  const adminApi = async (path, options = {}) => {
    const cfg = {method: 'GET', credentials: 'same-origin', headers: {}, ...options};
    if (cfg.body && typeof cfg.body !== 'string') {
      cfg.headers['Content-Type'] = 'application/json';
      cfg.body = JSON.stringify(cfg.body);
    }
    const res = await fetch(path, cfg);
    const data = await res.json();
    if (!res.ok || data.ok === false) throw new Error(data.message || 'Request failed');
    return data;
  };

  const escapeHtml = (value) => String(value ?? '')
    .replaceAll('&', '&amp;')
    .replaceAll('<', '&lt;')
    .replaceAll('>', '&gt;')
    .replaceAll('"', '&quot;');

  const fmtInt = (value) => new Intl.NumberFormat('en-IN').format(Number(value || 0));
  const fmtMoney = (value) => {
    const num = Number(value || 0);
    if (num >= 10000000) return 'Rs ' + (num / 10000000).toFixed(1).replace(/\.0$/, '') + 'Cr';
    if (num >= 100000) return 'Rs ' + (num / 100000).toFixed(1).replace(/\.0$/, '') + 'L';
    return 'Rs ' + fmtInt(num);
  };
  const fmtPct = (value) => Number(value || 0).toFixed(1).replace(/\.0$/, '') + '%';
  const riskClass = (score) => score >= 80 ? 'risk-high' : score >= 40 ? 'risk-med' : 'risk-low';
  const riskLabel = (score) => score >= 80 ? 'High' : score >= 40 ? 'Med' : 'Low';
  const statusBadge = (status) => {
    const map = {
      'Verified': 'bg',
      'KYC Pending': 'ba',
      'Active': 'bt',
      'Pending': 'ba',
      'Suspended': 'br',
      'Rejected': 'br',
      'Approved': 'bg',
      'Sent': 'bg',
    };
    return `<span class="b ${map[status] || 'bk'}">${escapeHtml(status || 'Unknown')}</span>`;
  };

  const state = {dashboard: null, selectedJourney: null};

  const findNode = (selector, text) => Array.from(document.querySelectorAll(selector)).find((node) => node.textContent.includes(text));
  const setMetricCard = (card, value, label, detail) => {
    if (!card) return;
    const valueNode = card.querySelector('.kv');
    const labelNode = card.querySelector('.kl');
    const detailNode = card.querySelector('.kd');
    if (valueNode) valueNode.textContent = value;
    if (labelNode) labelNode.textContent = label;
    if (detailNode) detailNode.textContent = detail;
  };

  const updateMenuBadges = (metrics) => {
    const alertsCount = metrics.unread_alerts;
    const workersCount = metrics.kyc_pending;
    const contractsCount = metrics.ai_high_risk_flags;
    const gstCount = metrics.gst_defaults;
    const alertBtnCount = document.getElementById('alerts-btn-count');
    if (alertBtnCount) alertBtnCount.textContent = fmtInt(alertsCount);
    const panelTitle = document.getElementById('alerts-panel-title');
    if (panelTitle) panelTitle.textContent = `System Alerts — ${fmtInt(alertsCount)} Unread`;

    [findNode('.nt', 'Workers'), findNode('.si', 'Workers')].forEach((node) => {
      const badge = node?.querySelector('.nc, .sbg');
      if (badge) badge.textContent = fmtInt(workersCount);
    });
    [findNode('.nt', 'Contract Intelligence'), findNode('.si', 'Contract Intelligence')].forEach((node) => {
      const badge = node?.querySelector('.nc, .sbg');
      if (badge) badge.textContent = fmtInt(contractsCount);
    });
    [findNode('.nt', 'GST / EPFO / ESIC'), findNode('.si', 'GST / EPFO / ESIC')].forEach((node) => {
      const badge = node?.querySelector('.nc, .sbg');
      if (badge) badge.textContent = fmtInt(gstCount);
    });
    const employersNode = findNode('.si', 'Employers');
    const employersBadge = employersNode?.querySelector('.sbg');
    if (employersBadge) employersBadge.textContent = fmtInt(metrics.active_employers);
  };

  const renderAlerts = (alerts) => {
    const list = document.querySelector('#np .npl');
    if (!list) return;
    list.innerHTML = alerts.map((item) => `
      <div class="npi ${item.unread ? 'u' : ''}">
        <div style="display:flex;justify-content:space-between;align-items:flex-start;">
          <h4>${escapeHtml(item.title)}</h4>
          <span class="npt">${escapeHtml(item.time)}</span>
        </div>
        <p>${escapeHtml(item.body)}</p>
      </div>
    `).join('');
  };

  const renderLiveFeed = (items) => {
    const feed = document.getElementById('aff');
    if (!feed) return;
    feed.innerHTML = items.map((item) => `
      <div class="af">
        <div class="afd ${escapeHtml(item.tone || 'g')}"></div>
        <div>
          <div class="aft">${item.title}</div>
          <div class="afm">${escapeHtml(item.meta)}</div>
        </div>
      </div>
    `).join('');
  };

  const renderOverview = (dashboard) => {
    const metrics = dashboard.metrics;
    const kpis = document.querySelectorAll('#overview-kpis .kpi');
    const cards = [
      [fmtInt(metrics.total_workers), 'Total Workers', `+${Math.max(metrics.total_workers - 5297, 0)} this cycle`],
      [fmtInt(metrics.verified_profiles), 'Verified Profiles', fmtPct((metrics.verified_profiles / metrics.total_workers) * 100)],
      [fmtInt(metrics.active_employers), 'Active Employers', `+${Math.max(metrics.active_employers - 294, 0)} this month`],
      [fmtInt(metrics.live_job_postings), 'Live Job Postings', 'Real backend-linked postings'],
      [fmtInt(metrics.total_placements), 'Total Placements', 'Cross-role placement ledger'],
      [fmtMoney(metrics.wages_disbursed), 'Wages Disbursed', 'April 2026'],
      [fmtMoney(metrics.micro_loans_live), 'Micro-Loans Live', 'NBFC + DBT linked'],
      [fmtMoney(metrics.contract_net_value), 'Contract Net Value', `${fmtInt(metrics.live_contracts)} contracts`],
      [fmtInt(metrics.kyc_pending), 'KYC Pending', 'Needs verifier attention'],
      [fmtInt(metrics.ai_high_risk_flags), 'AI High-Risk Flags', 'Immediate review'],
      [fmtInt(metrics.gst_defaults), 'GST/Comp Defaults', 'Active notices'],
      [metrics.avg_time_to_fill_hours.toFixed(1) + 'h', 'Avg Time-to-Fill', 'Operational benchmark'],
    ];
    cards.forEach((card, index) => setMetricCard(kpis[index], card[0], card[1], card[2]));

    const tag = document.getElementById('dashboard-ai-tag');
    const summary = document.getElementById('dashboard-ai-summary');
    const detail = document.getElementById('dashboard-ai-detail');
    if (tag) tag.textContent = `AI Intelligence Summary — ${dashboard.generatedAt}`;
    if (summary) summary.textContent = dashboard.aiSummary;
    if (detail) detail.textContent = dashboard.aiDetail;

    const ticker = document.getElementById('tkt');
    if (ticker) {
      ticker.innerHTML = `&nbsp;&nbsp;&nbsp;&nbsp;NATIONAL EMPLOYMENT INTELLIGENCE PLATFORM — LIVE &nbsp;|&nbsp; AI Engine: ACTIVE &nbsp;|&nbsp; ${fmtInt(metrics.total_workers)} Workers Tracked &nbsp;|&nbsp; ${fmtInt(metrics.ai_high_risk_flags)} HIGH-RISK Contracts Detected &nbsp;|&nbsp; ${fmtInt(metrics.active_employers)} Employers Monitored &nbsp;|&nbsp; ${fmtInt(metrics.live_contracts)} Active Contracts — ${fmtMoney(metrics.contract_net_value)} Net Value &nbsp;|&nbsp; Payroll: ${fmtMoney(dashboard.salaryBatch.amount)} Pending Auth &nbsp;|&nbsp; eShram Sync: Active &nbsp;|&nbsp; GST Defaults: ${fmtInt(metrics.gst_defaults)} &nbsp;|&nbsp; Micro-Loans Live: ${fmtMoney(metrics.micro_loans_live)} &nbsp;&nbsp;&nbsp;&nbsp;`;
    }

    renderLiveFeed(dashboard.liveFeed);

    const healthRows = document.querySelectorAll('#pg-dash .card:nth-of-type(2) .cbd > div');
    dashboard.health.forEach((item, index) => {
      const row = healthRows[index];
      if (!row) return;
      const label = row.querySelector('span');
      const value = row.querySelector('strong');
      const fill = row.querySelector('.pbf');
      if (label) label.textContent = item.label;
      if (value) value.textContent = fmtPct(item.value);
      if (fill) {
        fill.style.width = item.value + '%';
        fill.className = 'pbf ' + item.tone;
      }
    });
  };

  const renderWorkers = (dashboard) => {
    const tbody = document.getElementById('worker-registry-tbody');
    if (!tbody) return;
    tbody.innerHTML = dashboard.workers.map((worker) => `
      <tr>
        <td><code>${escapeHtml(worker.worker_id)}</code></td>
        <td><strong>${escapeHtml(worker.name)}</strong></td>
        <td>${escapeHtml(worker.role)} — ${escapeHtml(worker.level)}</td>
        <td>${escapeHtml(worker.city)}</td>
        <td>${worker.eshram_uan ? `<code>${escapeHtml(worker.eshram_uan)}</code>` : '—'}</td>
        <td>${worker.epfo_uan ? `<code>${escapeHtml(worker.epfo_uan)}</code>` : '—'}</td>
        <td>${statusBadge(worker.esic_status)}</td>
        <td class="${riskClass(worker.risk_score)}">${escapeHtml(riskLabel(worker.risk_score))} — ${escapeHtml(worker.risk_score)}/100</td>
        <td>${fmtInt(worker.jobs_completed)}</td>
        <td>${fmtMoney(worker.earnings)}</td>
        <td>${statusBadge(worker.status)}</td>
        <td><button class="btn btn-o btn-xs" onclick="showJourney(${JSON.stringify(worker.worker_id)})">Journey</button></td>
      </tr>
    `).join('');

    const count = document.getElementById('worker-registry-count');
    if (count) count.textContent = `Showing ${fmtInt(dashboard.workers.length)} of ${fmtInt(dashboard.metrics.total_workers)}`;
    const subtitle = document.querySelector('#pg-workers .ptb p');
    if (subtitle) subtitle.textContent = `${fmtInt(dashboard.metrics.total_workers)} workers — full profile with eShram, EPFO, ESIC, financial and journey data`;
  };

  const renderEmployers = (dashboard) => {
    const tbody = document.getElementById('employer-registry-tbody');
    if (!tbody) return;
    tbody.innerHTML = dashboard.employers.map((employer) => `
      <tr>
        <td><code>${escapeHtml(employer.employer_id)}</code></td>
        <td><strong>${escapeHtml(employer.company)}</strong></td>
        <td>${employer.gstin ? `<code>${escapeHtml(employer.gstin)}</code>` : '—'}</td>
        <td>${employer.epfo_code ? `<code>${escapeHtml(employer.epfo_code)}</code>` : '—'}</td>
        <td>${employer.esic_code ? `<code>${escapeHtml(employer.esic_code)}</code>` : '—'}</td>
        <td>${fmtInt(employer.workers)}</td>
        <td>${fmtInt(employer.contracts)}</td>
        <td><span class="${riskClass(employer.risk_score)}">${escapeHtml(employer.risk_score)}/100</span></td>
        <td style="font-weight:700;color:${employer.compliance_pct >= 90 ? 'var(--grn)' : employer.compliance_pct >= 60 ? 'var(--acc)' : 'var(--red)'};">${fmtPct(employer.compliance_pct)}</td>
        <td><button class="btn ${employer.risk_score >= 80 ? 'btn-r' : 'btn-o'} btn-xs" onclick="toast(${JSON.stringify(employer.risk_score >= 80 ? 'High-risk employer queued for investigation' : 'Employer profile opened')}, ${JSON.stringify(employer.risk_score >= 80 ? 'ter' : 'tin')})">${employer.risk_score >= 80 ? 'Investigate' : 'View'}</button></td>
      </tr>
    `).join('');

    const subtitle = document.querySelector('#pg-employers .ptb p');
    if (subtitle) subtitle.textContent = `${fmtInt(dashboard.metrics.active_employers)} employers — full GST, EPFO, ESIC, contract, and compliance intelligence`;
  };

  const renderContracts = (dashboard) => {
    const metrics = dashboard.metrics;
    const kpis = document.querySelectorAll('#contract-kpis .kpi');
    const cards = [
      [fmtInt(metrics.live_contracts), 'Total Contracts', ''],
      [fmtMoney(metrics.contract_net_value), 'Total Net Value', ''],
      [fmtInt(metrics.workers_deployed), 'Workers Deployed', ''],
      ['Rs ' + fmtInt(metrics.avg_daily_rate), 'Avg Daily Rate', ''],
      [fmtInt(metrics.ai_high_risk_flags), 'AI Flagged', ''],
      [fmtMoney(metrics.wage_diversion_per_day) + '/day', 'Wage Diversion (AI)', ''],
    ];
    cards.forEach((card, index) => setMetricCard(kpis[index], card[0], card[1], card[2]));

    const list = document.getElementById('contract-list');
    if (!list) return;
    list.innerHTML = dashboard.contracts.map((contract) => `
      <div class="ctc ${contract.risk_score >= 80 ? 'dispute' : contract.compliance_pct >= 90 ? 'live' : 'review'}">
        <div class="ctc-hd">
          <div>
            <div class="ctc-id">${escapeHtml(contract.contract_id)}</div>
            <h4>${escapeHtml(contract.title)}</h4>
            <p style="font-size:10.5px;color:var(--ink4);">Principal Employer: ${escapeHtml(contract.principal_employer)} &nbsp;|&nbsp; Contractor: ${escapeHtml(contract.contractor)} &nbsp;|&nbsp; Handler: ${escapeHtml(contract.handler)}</p>
          </div>
          <div style="display:flex;gap:5px;align-items:center;">
            <span class="b ${escapeHtml(contract.status_tone)}">${escapeHtml(contract.status_label)}</span>
            ${contract.secondary_badge ? `<span class="b br">${escapeHtml(contract.secondary_badge)}</span>` : ''}
          </div>
        </div>
        <div class="ctc-grid">
          <div class="ctcf"><strong>${fmtMoney(contract.contract_value)}</strong>Contract Net Value</div>
          <div class="ctcf"><strong>${fmtInt(contract.workers_deployed)} deployed / ${fmtInt(contract.epfo_workers)} ECR</strong>Workers</div>
          <div class="ctcf"><strong>Rs ${fmtInt(contract.worker_rate)}/day</strong>Worker Rate</div>
          <div class="ctcf"><strong>${escapeHtml(contract.start_date)} – ${escapeHtml(contract.end_date)}</strong>Contract Period</div>
          <div class="ctcf"><strong>Rs ${fmtInt(contract.client_rate)}/day billed</strong>Client Invoice Rate</div>
          <div class="ctcf"><strong>${contract.wage_diversion_per_day ? fmtMoney(contract.wage_diversion_per_day) + '/day' : 'Rs ' + fmtInt(contract.client_rate - contract.worker_rate) + '/day'}</strong>${contract.wage_diversion_per_day ? 'Wage Diversion' : 'Margin'}</div>
          <div class="ctcf"><strong>CLRA Lic: ${escapeHtml(contract.license_no)}</strong>Licence Status</div>
          <div class="ctcf"><strong>${contract.compliance_pct >= 90 ? 'EPFO: Filed | ESIC: Filed | GST: Filed' : contract.compliance_pct <= 10 ? 'EPFO: Partial | ESIC: Missing | GST: Mismatch' : 'EPFO: Filed | ESIC: Filed | GST: Review'}</strong>Compliance</div>
        </div>
        <div class="msr">
          <div class="msi"><div class="v" style="color:${contract.compliance_pct >= 90 ? 'var(--grn)' : contract.compliance_pct >= 60 ? 'var(--acc)' : 'var(--red)'};">${fmtPct(contract.compliance_pct)}</div><div class="l">Compliance</div></div>
          <div class="msi"><div class="v" style="color:${contract.rating >= 4.5 ? 'var(--grn)' : contract.rating > 0 ? 'var(--acc)' : 'var(--red)'};">${contract.rating ? escapeHtml(contract.rating.toFixed(1)) : '0.0'}</div><div class="l">Worker Rating</div></div>
          <div class="msi"><div class="v">${fmtMoney(contract.april_payment)}</div><div class="l">April Payment</div></div>
          <div class="msi"><div class="v" style="color:${contract.risk_score >= 80 ? 'var(--red)' : contract.risk_score >= 40 ? 'var(--acc)' : 'var(--grn)'};">${escapeHtml(contract.risk_score)}/100</div><div class="l">AI Risk Score</div></div>
        </div>
      </div>
    `).join('');

    const subtitle = document.querySelector('#pg-contracts .ptb p');
    if (subtitle) subtitle.textContent = `Full visibility of all employment contracts — who awarded, who handled, workers deployed, contract value, and compliance status`;
  };

  const renderBroadcastHistory = (dashboard) => {
    const tbody = document.getElementById('broadcast-history-tbody');
    if (!tbody) return;
    tbody.innerHTML = dashboard.broadcastHistory.map((item) => `
      <tr>
        <td>${escapeHtml(item.title)}</td>
        <td>${fmtInt(item.recipients)}</td>
        <td>${fmtPct(item.delivery_pct)}</td>
        <td>${escapeHtml(item.date)}</td>
        <td>${statusBadge(item.status)}</td>
      </tr>
    `).join('');
  };

  const renderAuditLog = (dashboard) => {
    const tbody = document.getElementById('audit-log-tbody');
    if (!tbody) return;
    tbody.innerHTML = dashboard.auditLog.map((item) => `
      <tr>
        <td>${escapeHtml(item.time)}</td>
        <td>${escapeHtml(item.user)}</td>
        <td>${escapeHtml(item.action)}</td>
        <td>${escapeHtml(item.ip)}</td>
        <td>${statusBadge(item.status)}</td>
      </tr>
    `).join('');
  };

  const renderJourney = (journey) => {
    if (!journey) return;
    state.selectedJourney = journey.worker_id;
    const profile = document.getElementById('wpc');
    if (profile) {
      profile.innerHTML = `
        <div class="wpc-top">
          <div class="wpc-av">${escapeHtml(journey.avatar || 'WK')}</div>
          <div>
            <div class="wpc-name">${escapeHtml(journey.name)}</div>
            <div class="wpc-id">${escapeHtml(journey.worker_id)}</div>
            <div id="journey-tags" style="display:flex;gap:5px;margin-top:5px;flex-wrap:wrap;">
              ${(journey.flags || []).map((flag, index) => `<span class="b ${index === 0 ? 'bg' : index === 1 ? 'ba' : index === 2 ? 'bb' : 'bt'}">${escapeHtml(flag)}</span>`).join('')}
            </div>
          </div>
        </div>
        <div class="wpc-grid">
          <div class="wpcf"><label>Role</label><span>${escapeHtml(journey.role)} — ${escapeHtml(journey.level)}</span></div>
          <div class="wpcf"><label>City</label><span>${escapeHtml(journey.city)}</span></div>
          <div class="wpcf"><label>eShram UAN</label><span>${journey.eshram_uan ? escapeHtml(journey.eshram_uan) : '—'}</span></div>
          <div class="wpcf"><label>Aadhaar (Last 4)</label><span>${journey.aadhaar_last4 ? 'XXXX-XXXX-' + escapeHtml(journey.aadhaar_last4) : '—'}</span></div>
          <div class="wpcf"><label>PF UAN</label><span>${journey.epfo_uan ? escapeHtml(journey.epfo_uan) : '—'}</span></div>
          <div class="wpcf"><label>ESIC IP No.</label><span>${journey.esic_ip ? escapeHtml(journey.esic_ip) : '—'}</span></div>
          <div class="wpcf"><label>Bank (DBT)</label><span>${journey.bank_account ? escapeHtml(journey.bank_account) : '—'}</span></div>
          <div class="wpcf"><label>AI Risk Score</label><span style="color:${journey.risk_score >= 40 ? 'var(--acc)' : '#5de89a'};">${escapeHtml(journey.risk_label)} — ${escapeHtml(journey.risk_score)}/100</span></div>
        </div>
      `;
    }

    const financial = document.getElementById('journey-financial-body');
    if (financial) {
      const f = journey.financials || {};
      financial.innerHTML = `
        <div class="g2" style="gap:8px;">
          <div style="background:var(--s);border-radius:3px;padding:10px;text-align:center;"><div style="font-size:16px;font-weight:700;color:var(--grn);">${fmtMoney(f.month)}</div><div style="font-size:10px;color:var(--ink4);">This Month</div></div>
          <div style="background:var(--s);border-radius:3px;padding:10px;text-align:center;"><div style="font-size:16px;font-weight:700;color:var(--ink);">${fmtMoney(f.ytd)}</div><div style="font-size:10px;color:var(--ink4);">YTD Earnings</div></div>
          <div style="background:var(--s);border-radius:3px;padding:10px;text-align:center;"><div style="font-size:16px;font-weight:700;color:var(--blu);">${fmtMoney(f.loan)}</div><div style="font-size:10px;color:var(--ink4);">Active Loan</div></div>
          <div style="background:var(--s);border-radius:3px;padding:10px;text-align:center;"><div style="font-size:16px;font-weight:700;color:var(--tel);">${fmtMoney(f.pf_balance)}</div><div style="font-size:10px;color:var(--ink4);">PF Balance</div></div>
        </div>
        <hr>
        <div style="font-size:10.5px;color:var(--ink4);display:flex;flex-direction:column;gap:4px;">
          <div style="display:flex;justify-content:space-between;"><span>Gross Earnings (Current Cycle)</span><strong>${fmtMoney(f.gross)}</strong></div>
          <div style="display:flex;justify-content:space-between;"><span>PF Deduction</span><strong style="color:var(--red);">- ${fmtMoney(f.pf_deduction)}</strong></div>
          <div style="display:flex;justify-content:space-between;"><span>ESIC Contribution</span><strong style="color:var(--red);">- ${fmtMoney(f.esic_deduction)}</strong></div>
          <div style="display:flex;justify-content:space-between;"><span>Loan EMI</span><strong style="color:var(--red);">- ${fmtMoney(f.loan_emi)}</strong></div>
          <hr>
          <div style="display:flex;justify-content:space-between;"><span style="font-weight:700;">Net Take-Home</span><strong style="color:var(--grn);font-size:13px;">${fmtMoney(f.take_home)}</strong></div>
        </div>
      `;
    }

    const timeline = document.getElementById('journey-timeline');
    if (timeline) {
      timeline.innerHTML = (journey.timeline || []).map((event) => `
        <div class="jte">
          <div class="jt-dot ${escapeHtml(event.tone || 'grn')}">${escapeHtml(event.step || '')}</div>
          <div class="jt-body">
            <h4>${escapeHtml(event.title)}</h4>
            <p>${escapeHtml(event.description)}</p>
            <div class="jt-meta">${(event.meta || []).map((meta) => `<span>${escapeHtml(meta)}</span>`).join('')}</div>
            ${(event.tags || []).length ? `<div style="margin-top:4px;">${event.tags.map((tag) => `<span class="jt-tag">${escapeHtml(tag)}</span>`).join('')}</div>` : ''}
          </div>
        </div>
      `).join('');
    }

    const search = document.getElementById('wj-search');
    if (search) search.value = journey.worker_id;
  };

  const showJourney = (workerId) => {
    if (!state.dashboard) return;
    const journey = state.dashboard.journeys[workerId];
    if (!journey) {
      toast('Journey not found for ' + workerId, 'twa');
      return;
    }
    nav('journey', null);
    renderJourney(journey);
  };

  const resolveJourney = (term) => {
    const lookup = (term || '').trim().toLowerCase();
    if (!lookup || !state.dashboard) {
      return state.dashboard ? state.dashboard.journeys[Object.keys(state.dashboard.journeys)[0]] : null;
    }
    const exact = state.dashboard.journeys[term];
    if (exact) return exact;
    return Object.values(state.dashboard.journeys).find((journey) =>
      journey.worker_id.toLowerCase() === lookup || journey.name.toLowerCase().includes(lookup)
    ) || null;
  };

  const collectWorkerPayload = () => {
    const fields = document.querySelectorAll('#worker-modal-fields input, #worker-modal-fields select');
    return {
      name: fields[0]?.value?.trim() || '',
      mobile: fields[1]?.value?.trim() || '',
      role: fields[2]?.value || '',
      level: fields[3]?.value || '',
      city: fields[4]?.value?.trim() || '',
      eshramUan: fields[5]?.value?.trim() || '',
      aadhaarLast4: fields[6]?.value?.trim() || '',
      bankAccount: fields[7]?.value?.trim() || '',
    };
  };

  const collectEmployerPayload = () => {
    const fields = document.querySelectorAll('#employer-modal-fields input, #employer-modal-fields select');
    return {
      company: fields[0]?.value?.trim() || '',
      gstin: fields[1]?.value?.trim() || '',
      epfoCode: fields[2]?.value?.trim() || '',
      esicCode: fields[3]?.value?.trim() || '',
      sector: fields[4]?.value || '',
      city: fields[5]?.value?.trim() || '',
      contactPerson: fields[6]?.value?.trim() || '',
      contactMobile: fields[7]?.value?.trim() || '',
    };
  };

  const collectContractPayload = () => {
    const fields = document.querySelectorAll('#contract-modal-fields input, #contract-modal-fields select');
    return {
      principalEmployer: fields[0]?.value || '',
      contractor: fields[1]?.value?.trim() || '',
      contractValue: fields[2]?.value || '',
      workersRequired: fields[3]?.value || '',
      workerRate: fields[4]?.value || '',
      clientRate: fields[5]?.value || '',
      startDate: fields[6]?.value || '',
      endDate: fields[7]?.value || '',
      licenseNo: fields[8]?.value?.trim() || '',
      handler: fields[9]?.value?.trim() || '',
    };
  };

  const refreshDashboard = async () => {
    state.dashboard = await adminApi('/api/admin/advanced/dashboard');
    renderAlerts(state.dashboard.alerts);
    updateMenuBadges(state.dashboard.metrics);
    renderOverview(state.dashboard);
    renderWorkers(state.dashboard);
    renderEmployers(state.dashboard);
    renderContracts(state.dashboard);
    renderBroadcastHistory(state.dashboard);
    renderAuditLog(state.dashboard);
    const currentJourney = resolveJourney(state.selectedJourney || '');
    renderJourney(currentJourney);
  };

  window.loadJourney = () => {
    const search = document.getElementById('wj-search');
    const journey = resolveJourney(search?.value || '');
    if (!journey) {
      toast('No matching journey found', 'twa');
      return;
    }
    renderJourney(journey);
    toast('Loaded journey for ' + journey.name, 'tin');
  };

  window.showJourney = showJourney;

  window.launchScheme = async () => {
    try {
      const payload = {
        schemeName: document.getElementById('sch-n')?.textContent?.trim() || 'PM-SAYSAM — Wage Insurance',
        regions: Array.from(document.querySelectorAll('#rgrid .rt.sel')).map((node) => node.textContent.trim()),
      };
      const data = await adminApi('/api/admin/advanced/launch-scheme', {method: 'POST', body: payload});
      const bp = document.getElementById('sch-bp');
      bp.classList.add('on');
      document.getElementById('schbp-b').textContent = 'Launching';
      document.getElementById('schbp-b').className = 'b ba';
      let delivered = 0;
      const total = Number(data.campaign.recipients || state.dashboard.metrics.verified_profiles);
      const iv = setInterval(() => {
        const chunk = Math.floor(Math.random() * 220) + 100;
        delivered = Math.min(delivered + chunk, total);
        const pct = Math.round((delivered / total) * 100);
        document.getElementById('schbp-f').style.width = pct + '%';
        document.getElementById('schbp-c').textContent = fmtInt(delivered) + ' / ' + fmtInt(total);
        document.getElementById('schbp-app').textContent = fmtInt(Math.floor(delivered * 0.61));
        document.getElementById('schbp-sms').textContent = fmtInt(Math.floor(delivered * 0.95));
        document.getElementById('schbp-wa').textContent = fmtInt(Math.floor(delivered * 0.59));
        document.getElementById('schbp-fail').textContent = fmtInt(Math.floor(delivered * 0.027));
        if (delivered >= total) {
          clearInterval(iv);
          document.getElementById('schbp-b').textContent = 'Delivered';
          document.getElementById('schbp-b').className = 'b bg';
          toast(data.message, 'tok');
        }
      }, 180);
      await refreshDashboard();
    } catch (error) {
      toast(error.message, 'ter');
    }
  };

  window.procSalary = async () => {
    try {
      const data = await adminApi('/api/admin/advanced/process-payroll', {method: 'POST'});
      const bp = document.getElementById('sal-bp');
      bp.classList.add('on');
      let delivered = 0;
      const total = Number(data.batch.workers || state.dashboard.salaryBatch.workers);
      const iv = setInterval(() => {
        const chunk = Math.floor(Math.random() * 210) + 90;
        delivered = Math.min(delivered + chunk, total);
        const ok = Math.floor(delivered * 0.994);
        const pct = Math.round((delivered / total) * 100);
        document.getElementById('sal-b').style.width = pct + '%';
        document.getElementById('sal-c').textContent = fmtInt(delivered) + ' workers paid';
        document.getElementById('sal-ok').textContent = fmtInt(ok);
        document.getElementById('sal-fl').textContent = fmtInt(delivered - ok);
        document.getElementById('sal-am').textContent = fmtMoney(Math.round((ok / total) * data.batch.amount));
        if (delivered >= total) {
          clearInterval(iv);
          toast(data.message, 'tok');
        }
      }, 180);
      await refreshDashboard();
    } catch (error) {
      toast(error.message, 'ter');
    }
  };

  window.sendBC = async () => {
    try {
      const audienceSelect = document.getElementById('bc-a');
      const payload = {
        title: document.getElementById('bc-t')?.value?.trim() || 'Platform Broadcast',
        message: document.getElementById('bc-b')?.value?.trim() || '',
        audience: audienceSelect?.options[audienceSelect.selectedIndex]?.text || 'All',
        recipients: Number(audienceSelect?.value || state.dashboard.metrics.total_workers),
      };
      const data = await adminApi('/api/admin/advanced/broadcast', {method: 'POST', body: payload});
      const bp = document.getElementById('bc-pnl');
      bp.classList.add('on');
      document.getElementById('bcp-t').textContent = payload.title;
      document.getElementById('bcp-b').textContent = 'Sending';
      document.getElementById('bcp-b').className = 'b ba';
      let delivered = 0;
      const total = Number(data.broadcast.recipients || payload.recipients);
      const iv = setInterval(() => {
        const chunk = Math.floor(Math.random() * 380) + 180;
        delivered = Math.min(delivered + chunk, total);
        const pct = Math.round((delivered / total) * 100);
        document.getElementById('bcp-f').style.width = pct + '%';
        document.getElementById('bcp-c').textContent = fmtInt(delivered) + ' / ' + fmtInt(total) + ' delivered';
        document.getElementById('bcp-app').textContent = fmtInt(Math.floor(delivered * 0.61));
        document.getElementById('bcp-sms').textContent = fmtInt(Math.floor(delivered * 0.95));
        document.getElementById('bcp-wa').textContent = fmtInt(Math.floor(delivered * 0.59));
        document.getElementById('bcp-fail').textContent = fmtInt(Math.floor(delivered * 0.028));
        if (delivered >= total) {
          clearInterval(iv);
          document.getElementById('bcp-b').textContent = 'Delivered';
          document.getElementById('bcp-b').className = 'b bg';
          toast(data.message, 'tok');
        }
      }, 140);
      await refreshDashboard();
    } catch (error) {
      toast(error.message, 'ter');
    }
  };

  const bindFormActions = () => {
    const workerSubmit = document.getElementById('worker-modal-submit');
    const employerSubmit = document.getElementById('employer-modal-submit');
    const contractSubmit = document.getElementById('contract-modal-submit');

    if (workerSubmit) {
      workerSubmit.onclick = async () => {
        try {
          const payload = collectWorkerPayload();
          const data = await adminApi('/api/admin/advanced/register-worker', {method: 'POST', body: payload});
          closeM('m-worker');
          toast(data.message, 'tok');
          await refreshDashboard();
          showJourney(data.worker.workerId);
        } catch (error) {
          toast(error.message, 'ter');
        }
      };
    }

    if (employerSubmit) {
      employerSubmit.onclick = async () => {
        try {
          const payload = collectEmployerPayload();
          const data = await adminApi('/api/admin/advanced/register-employer', {method: 'POST', body: payload});
          closeM('m-emp');
          toast(data.message, 'tok');
          await refreshDashboard();
        } catch (error) {
          toast(error.message, 'ter');
        }
      };
    }

    if (contractSubmit) {
      contractSubmit.onclick = async () => {
        try {
          const payload = collectContractPayload();
          const data = await adminApi('/api/admin/advanced/register-contract', {method: 'POST', body: payload});
          closeM('m-new-contract');
          toast(data.message, 'tok');
          await refreshDashboard();
          nav('contracts', null);
        } catch (error) {
          toast(error.message, 'ter');
        }
      };
    }
  };

  document.addEventListener('DOMContentLoaded', async () => {
    bindFormActions();
    try {
      await refreshDashboard();
    } catch (error) {
      toast(error.message || 'Unable to load advanced dashboard', 'ter');
    }
  });
})();
"""
