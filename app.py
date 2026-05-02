import json
import os
import secrets
from copy import deepcopy
from datetime import datetime
from email.utils import formatdate
from html import escape
from http import HTTPStatus
from http.cookies import SimpleCookie
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from threading import Lock
from urllib.parse import parse_qs, urlparse

from advanced_admin import (
    advanced_dashboard_payload,
    build_advanced_admin_page,
    build_advanced_gate_page,
    ensure_advanced_state,
)


BASE_DIR = Path(__file__).resolve().parent
PORTAL_HTML = BASE_DIR / "iee_government_portal.html"
DB_PATH = BASE_DIR / "portal_data.json"
SESSION_COOKIE = "iee_portal_session"
STATE_LOCK = Lock()


DEFAULT_STATE = {
    "meta": {
        "next_worker_seq": 45824,
        "next_employer_seq": 1249,
        "next_verifier_seq": 2,
        "next_job_seq": 5,
        "next_bulk_seq": 1,
        "next_notice_seq": 1,
        "next_session_seq": 1,
    },
    "users": [
        {
            "row_id": "ur-1",
            "role": "worker",
            "status": "Active",
            "name": "Rajan Kumar",
            "mobile": "9876500010",
            "email": "",
            "password": "Worker@001",
            "login_id": "9876500010",
            "iee_id": "IEE-WK-2026-00045821",
            "occupation": "Construction Mason",
            "city": "Chennai, Tamil Nadu",
            "rating": "4.9/5",
            "jobs_completed": 23,
            "registered": "10 Apr 2026",
        },
        {
            "row_id": "ur-2",
            "role": "employer",
            "status": "Active",
            "name": "Skyline Constructions",
            "mobile": "",
            "email": "skyline@company.com",
            "password": "Employ@001",
            "login_id": "skyline@company.com",
            "employer_id": "EMP-TN-2026-001248",
            "sector": "Construction",
            "city": "Chennai, Tamil Nadu",
            "registered": "08 Apr 2026",
        },
        {
            "row_id": "ur-3",
            "role": "verifier",
            "status": "Active",
            "name": "S. Anbarasan",
            "mobile": "+91 90210 45678",
            "email": "verifier001@iee.gov.in",
            "password": "Verify@001",
            "login_id": "verifier001@iee.gov.in",
            "verifier_id": "IEE-VRF-2026-001",
            "zone": "Zone 3 - North Chennai",
            "registered": "05 Apr 2026",
        },
        {
            "row_id": "ur-4",
            "role": "worker",
            "status": "KYC Pending",
            "name": "Priya Devi",
            "mobile": "9876500020",
            "email": "",
            "password": "Worker@002",
            "login_id": "9876500020",
            "iee_id": "IEE-WK-2026-00091",
            "occupation": "Maid / Housekeeper",
            "city": "Chennai, Tamil Nadu",
            "rating": "4.6/5",
            "jobs_completed": 11,
            "registered": "18 Apr 2026",
        },
        {
            "row_id": "ur-5",
            "role": "employer",
            "status": "Flagged",
            "name": "Ram Nivas Contractors",
            "mobile": "",
            "email": "ramnivas@firm.com",
            "password": "Firm@001",
            "login_id": "ramnivas@firm.com",
            "employer_id": "EMP-TN-2026-009912",
            "sector": "Construction",
            "city": "Chennai, Tamil Nadu",
            "registered": "12 Apr 2026",
        },
        {
            "row_id": "ur-0",
            "role": "superadmin",
            "status": "Active",
            "name": "Super Administrator",
            "mobile": "",
            "email": "superadmin@iee.gov.in",
            "password": "Admin@IEE2026",
            "login_id": "superadmin@iee.gov.in",
            "registered": "01 Jan 2026",
        },
    ],
    "workers": [
        {
            "name": "Rajan Kumar",
            "iee_id": "IEE-WK-2026-00045821",
            "mobile": "9876500010",
            "occupation": "Construction Mason",
            "city": "Chennai",
            "rating": "4.9/5",
            "jobs_completed": 23,
            "status": "Verified",
            "skills": ["Masonry", "Tiling"],
        },
        {
            "name": "Suresh Babu",
            "iee_id": "IEE-WK-2026-00045822",
            "mobile": "9876500030",
            "occupation": "Carpenter",
            "city": "Chennai",
            "rating": "4.8/5",
            "jobs_completed": 18,
            "status": "Verified",
            "skills": ["Woodwork", "Framework"],
        },
        {
            "name": "Murugan S",
            "iee_id": "IEE-WK-2026-00045823",
            "mobile": "9876500040",
            "occupation": "Electrician",
            "city": "Chennai",
            "rating": "4.5/5",
            "jobs_completed": 31,
            "status": "Verified",
            "skills": ["Wiring", "Safety"],
        },
        {
            "name": "Vijay R",
            "iee_id": "IEE-WK-2026-00045824",
            "mobile": "9876500050",
            "occupation": "Plumber",
            "city": "Chennai",
            "rating": "4.7/5",
            "jobs_completed": 16,
            "status": "Verified",
            "skills": ["Plumbing", "Repair"],
        },
    ],
    "verification_queue": [
        {
            "queue_id": "vr-1",
            "name": "Ganesh Kumar",
            "iee_id": "IEE-WK-2026-00091",
            "mobile": "+91 99345 67890",
            "role": "Mason",
            "aadhaar": "Pending",
            "priority": "HIGH",
            "status": "Pending",
        },
        {
            "queue_id": "vr-2",
            "name": "Priya Devi",
            "iee_id": "IEE-WK-2026-00092",
            "mobile": "+91 98765 43210",
            "role": "Maid",
            "aadhaar": "Provided",
            "priority": "MED",
            "status": "Pending",
        },
        {
            "queue_id": "vr-3",
            "name": "Mohammed Rafi",
            "iee_id": "IEE-WK-2026-00093",
            "mobile": "+91 87654 32109",
            "role": "Electrician",
            "aadhaar": "Pending",
            "priority": "HIGH",
            "status": "Pending",
        },
        {
            "queue_id": "vr-4",
            "name": "Lakshmi Bai",
            "iee_id": "IEE-WK-2026-00094",
            "mobile": "+91 76543 21098",
            "role": "Cook",
            "aadhaar": "Provided",
            "priority": "LOW",
            "status": "Pending",
        },
    ],
    "jobs": [
        {
            "job_id": "job-1",
            "title": "Brick Mason - Full Day",
            "employer": "Skyline Constructions",
            "distance": "1.2 km",
            "wage": 850,
            "type": "Urgent",
            "applicants": [],
        },
        {
            "job_id": "job-2",
            "title": "Plastering Work - 3 Days",
            "employer": "Prestige Builders",
            "distance": "2.8 km",
            "wage": 750,
            "type": "Daily",
            "applicants": [],
        },
        {
            "job_id": "job-3",
            "title": "Concrete Laying - 7 Days",
            "employer": "Metro Works",
            "distance": "4.1 km",
            "wage": 900,
            "type": "Bulk",
            "applicants": [],
        },
        {
            "job_id": "job-4",
            "title": "Foundation Work - 10 Days",
            "employer": "CMRL Phase 2",
            "distance": "5.2 km",
            "wage": 950,
            "type": "Bulk",
            "applicants": [],
        },
    ],
    "bulk_requests": [],
    "notices": [],
    "audit_log": [
        {"time": "09:42", "user": "superadmin", "action": "LOGIN", "ip": "103.38.50.x", "status": "OK"},
        {"time": "09:38", "user": "verifier-001", "action": "VERIFY_APPROVE", "ip": "103.38.50.x", "status": "OK"},
        {"time": "09:25", "user": "skyline", "action": "BULK_HIRE_REQ", "ip": "103.38.50.x", "status": "Pending"},
        {"time": "09:10", "user": "system", "action": "SCHEDULED_MATCH", "ip": "internal", "status": "OK"},
        {"time": "08:55", "user": "verifier-001", "action": "VERIFY_REJECT", "ip": "103.38.50.x", "status": "Review"},
        {"time": "08:30", "user": "superadmin", "action": "CONFIG_UPDATE", "ip": "103.38.50.x", "status": "OK"},
    ],
    "sessions": {},
}


LIVE_SERVICE_CATALOG = [
    {"id": "ai-interview", "cat": "platform", "role": "AI Screening", "ico": "&#129302;", "title": "AI Interview Screening Bot", "desc": "Voice and text screening for workers with fit score, language checks, availability and employer shortlist routing.", "status": "Live", "metric": "92%", "metricLbl": "screening accuracy", "forms": [["select", "Role", "Mason|Carpenter|Electrician|Welder|General Labour"], ["select", "Language", "Hindi|Tamil|Telugu|English"], ["input", "Worker ID", "IEE-WK-2026-00045821"], ["select", "Availability", "Today|Tomorrow|This Week"]], "summary": "Shortlists candidates and prepares interview notes."},
    {"id": "adaptive-learning", "cat": "worker", "role": "Skills", "ico": "&#127891;", "title": "Adaptive Learning Engine for Skills", "desc": "Personalised courses based on worker skill, local demand, certification gaps and acceptance history.", "status": "Live", "metric": "3", "metricLbl": "courses suggested", "forms": [["select", "Current Skill", "Masonry|Painting|Electrical|Plumbing|Site Safety"], ["select", "City", "Chennai|Hyderabad|Bengaluru|Mumbai"], ["select", "Goal", "Higher wage|Safety certificate|Supervisor path|New trade"]], "summary": "Builds a worker-specific learning path."},
    {"id": "safety-incident", "cat": "safety", "role": "Safety", "ico": "&#9874;", "title": "Construction Safety Incident Reporting", "desc": "Site incident intake with severity, GPS-ready escalation, inspector alerting and employer safety analytics.", "status": "Live", "metric": "15m", "metricLbl": "critical SLA", "forms": [["input", "Site Name", "OMR Metro Site"], ["select", "Severity", "Low|Medium|High|Critical"], ["select", "Incident Type", "Near miss|Fall|Equipment|Electrical|Medical"], ["textarea", "Details", "Worker slipped near scaffolding zone."]], "summary": "Creates a safety ticket and escalation path."},
    {"id": "seasonal-surge", "cat": "employer", "role": "Hiring", "ico": "&#128200;", "title": "Seasonal Labour Surge Management", "desc": "Predicts harvest, festival and construction demand spikes and activates worker notification pools.", "status": "Live", "metric": "85%", "metricLbl": "forecast score", "forms": [["select", "Sector", "Construction|Agriculture|Events|Logistics"], ["input", "District", "Chennai"], ["input", "Workers Needed", "120"], ["select", "Window", "Next 7 days|Next 14 days|Next 30 days"]], "summary": "Generates a surge staffing plan."},
    {"id": "gst-einvoice", "cat": "compliance", "role": "Tax", "ico": "&#129534;", "title": "GST E-Invoice Auto-Generation", "desc": "Generates GST-ready invoice numbers, IRN-style references, tax split and employer download records.", "status": "Live", "metric": "100%", "metricLbl": "invoice coverage", "forms": [["input", "Employer GSTIN", "33AABCS1234Z1Z5"], ["input", "Taxable Amount", "85000"], ["select", "Supply Type", "B2B|B2C|RCM"], ["select", "GST Rate", "5|12|18"]], "summary": "Calculates tax and produces invoice metadata."},
    {"id": "msme-fast-track", "cat": "employer", "role": "Onboarding", "ico": "&#127970;", "title": "MSME Employer Fast-Track Portal", "desc": "Three-minute Udyam-led employer onboarding with provisional posting access and KYC queueing.", "status": "Live", "metric": "3m", "metricLbl": "onboarding time", "forms": [["input", "Udyam Number", "UDYAM-TN-02-0012345"], ["input", "Business Name", "Skyline Works"], ["input", "Mobile", "9876500000"], ["select", "Entity Type", "Micro|Small|Medium"]], "summary": "Creates provisional employer access."},
    {"id": "nps-lite", "cat": "worker", "role": "Pension", "ico": "&#128176;", "title": "Worker Pension NPS-Lite Auto-Enrolment", "desc": "PRAN-style enrolment simulation with contribution setup, opt-out state and projected worker corpus.", "status": "Live", "metric": "&#8377;500", "metricLbl": "monthly micro-save", "forms": [["input", "Worker ID", "IEE-WK-2026-00045821"], ["input", "Contribution per Payment", "50"], ["select", "Employer Match", "No match|25% match|50% match"], ["select", "Consent", "Enrol now|Opt out"]], "summary": "Enrols worker into pension workflow."},
    {"id": "benefits-portability", "cat": "worker", "role": "Welfare", "ico": "&#128506;", "title": "Cross-State Benefits Portability", "desc": "Routes migrant worker benefits across states including ration, insurance and welfare scheme continuity.", "status": "Live", "metric": "36", "metricLbl": "states and UTs", "forms": [["input", "Worker ID", "IEE-WK-2026-00045821"], ["select", "From State", "Tamil Nadu|Bihar|Odisha|Uttar Pradesh"], ["select", "To State", "Karnataka|Maharashtra|Delhi|Tamil Nadu"], ["select", "Benefit", "Ration|Insurance|BOCW Welfare|All"]], "summary": "Checks portability status and scheme routing."},
    {"id": "api-marketplace", "cat": "platform", "role": "Integration", "ico": "&#128279;", "title": "API Marketplace for HRMS Integration", "desc": "OAuth-ready sandbox connectors for SAP, Workday, Oracle HCM, Darwinbox, GreytHR and custom HRMS tools.", "status": "Live", "metric": "6", "metricLbl": "connectors", "forms": [["select", "HRMS", "SAP SuccessFactors|Workday|Oracle HCM|Darwinbox|GreytHR|Custom REST"], ["select", "Scope", "Worker verification|Payroll sync|Attendance webhook|Full access"], ["input", "Callback URL", "https://hrms.example.com/iee/webhook"]], "summary": "Issues sandbox credentials and webhook plan."},
    {"id": "referral-network", "cat": "employer", "role": "Growth", "ico": "&#129309;", "title": "Employer Referral Network", "desc": "Referral codes, conversion tracking, anti-fraud checks and automatic reward credit after first hire.", "status": "Live", "metric": "&#8377;1500", "metricLbl": "sample reward", "forms": [["input", "Employer ID", "EMP-TN-2026-001248"], ["input", "Referred Business", "MetroBuild MSME"], ["select", "Expected Hiring", "1-10 workers|11-50 workers|51-200 workers"]], "summary": "Creates referral code and reward tracker."},
    {"id": "accessibility", "cat": "worker", "role": "Accessibility", "ico": "&#9855;", "title": "Worker Disability &amp; Accessibility Features", "desc": "PwD-aware job filters, high contrast support, screen-reader labels and accessible-site matching.", "status": "Live", "metric": "AA", "metricLbl": "WCAG target", "forms": [["select", "Accessibility Need", "Mobility support|Low vision|Hearing support|Cognitive support"], ["select", "Job Preference", "Accessible construction|Office support|Packaging|Remote verification"], ["select", "UI Mode", "Standard|High contrast"]], "summary": "Applies accessible job matching and UI preferences."},
    {"id": "women-night-safety", "cat": "safety", "role": "Women Safety", "ico": "&#128680;", "title": "Women Worker Safety &amp; Night Shift Module", "desc": "Night shift eligibility, transport declaration, POSH routing and SOS escalation for women workers.", "status": "Live", "metric": "10m", "metricLbl": "SOS response", "forms": [["input", "Worker Name", "Priya Devi"], ["input", "Site", "Chennai Port Night Shift"], ["select", "Transport Provided", "Yes|No"], ["select", "Shift", "Day|Night"]], "summary": "Validates safety and compliance requirements."},
    {"id": "blockchain-credential", "cat": "platform", "role": "Credentials", "ico": "&#128272;", "title": "Blockchain Credential Verification", "desc": "Verifiable credential proof for PMKVY and skill certificates with tamper-evident hash and QR verification.", "status": "Live", "metric": "3s", "metricLbl": "verification time", "forms": [["input", "Certificate ID", "PMKVY-TN-2026-7782"], ["select", "Issuer", "PMKVY|ITI|NSDC|Employer Academy"], ["input", "Worker ID", "IEE-WK-2026-00045821"]], "summary": "Verifies credential authenticity."},
    {"id": "dispute-chatbot", "cat": "safety", "role": "Dispute", "ico": "&#128172;", "title": "Dispute Resolution Chatbot", "desc": "Multilingual complaint intake for payment disputes, misconduct, job cancellation and wage mismatch.", "status": "Live", "metric": "24h", "metricLbl": "first response", "forms": [["select", "Dispute Type", "Payment delay|Wage mismatch|Misconduct|Job cancelled"], ["select", "Language", "English|Hindi|Tamil|Telugu"], ["textarea", "Message", "Employer has not released payment for three days of masonry work."]], "summary": "Classifies complaint and creates case."},
    {"id": "dpdpa-compliance", "cat": "compliance", "role": "Privacy", "ico": "&#128274;", "title": "Data Anonymisation &amp; DPDPA Compliance", "desc": "Consent ledger, data minimisation checks, anonymised exports and privacy impact workflow.", "status": "Live", "metric": "0", "metricLbl": "direct identifiers", "forms": [["select", "Dataset", "Worker profiles|Employer payroll|Dispute cases|Training history"], ["select", "Action", "Anonymise export|Revoke consent|Generate DPIA|View consent log"], ["input", "Record Count", "1250"]], "summary": "Runs privacy-safe data action."},
    {"id": "tds-form16b", "cat": "compliance", "role": "Tax", "ico": "&#128179;", "title": "Employer TDS Deduction &amp; Form 16B Auto", "desc": "TDS calculation, deduction record, challan status and Form 16B generation for contracted worker payments.", "status": "Live", "metric": "7d", "metricLbl": "form issue SLA", "forms": [["input", "Worker PAN", "ABCDE1234F"], ["input", "Payment Amount", "50000"], ["select", "TDS Rate", "1|2|5|10"], ["select", "Quarter", "Q1|Q2|Q3|Q4"]], "summary": "Calculates deduction and form record."},
    {"id": "epfo-esic-filing", "cat": "compliance", "role": "Payroll", "ico": "&#128188;", "title": "Automated EPFO / ESIC Filing (Employer)", "desc": "Monthly ECR-style filing, UAN generation queue, ESIC coverage and compliance certificate output.", "status": "Live", "metric": "5m", "metricLbl": "filing time", "forms": [["input", "Employer ID", "EMP-TN-2026-001248"], ["input", "Workers in Filing", "148"], ["select", "Month", "April 2026|May 2026|June 2026"], ["select", "Scheme", "EPFO + ESIC|EPFO only|ESIC only"]], "summary": "Prepares statutory filing output."},
    {"id": "job-alerts", "cat": "worker", "role": "AI Matching", "ico": "&#128276;", "title": "Job Alert Personalisation Engine", "desc": "Personalised alerts using role, distance, wage floor, availability and worker acceptance signals.", "status": "Live", "metric": "5", "metricLbl": "alerts today", "forms": [["select", "Role", "Mason|Carpenter|Electrician|Painter|Welder"], ["input", "Max Distance KM", "5"], ["input", "Minimum Wage", "800"], ["select", "Availability", "Today|Tomorrow|Weekend"]], "summary": "Generates a ranked worker job feed."},
    {"id": "mental-health", "cat": "worker", "role": "Wellbeing", "ico": "&#128153;", "title": "Worker Mental Health Support Module", "desc": "PHQ-4 style check-in, anonymous support option, counselling resource routing and crisis escalation.", "status": "Live", "metric": "1h", "metricLbl": "crisis SLA", "forms": [["select", "Mood Today", "Good|Stressed|Anxious|Very low"], ["select", "Sleep Quality", "Good|Average|Poor"], ["select", "Support Mode", "Anonymous chat|Call counsellor|Self-help resources"]], "summary": "Creates wellbeing support recommendation."},
    {"id": "carbon-credit", "cat": "green", "role": "Sustainability", "ico": "&#127793;", "title": "Carbon Credit for Green Construction", "desc": "Green construction metrics, material savings, audit queue and estimated carbon credit generation.", "status": "Live", "metric": "tCO2e", "metricLbl": "credit estimate", "forms": [["input", "Project Name", "Green Metro Depot"], ["input", "Cement Saved Tonnes", "35"], ["input", "Recycled Waste Tonnes", "120"], ["select", "Energy Source", "Grid|Solar mix|Diesel|Hybrid"]], "summary": "Estimates green construction credit."},
]

LIVE_SERVICE_DOMAINS = {
    "ai-interview": "interview_screenings",
    "adaptive-learning": "learning_paths",
    "safety-incident": "safety_incidents",
    "seasonal-surge": "surge_plans",
    "gst-einvoice": "gst_invoices",
    "msme-fast-track": "msme_onboarding",
    "nps-lite": "pension_enrolments",
    "benefits-portability": "benefit_portability",
    "api-marketplace": "api_clients",
    "referral-network": "employer_referrals",
    "accessibility": "accessibility_profiles",
    "women-night-safety": "women_safety_checks",
    "blockchain-credential": "credential_proofs",
    "dispute-chatbot": "dispute_cases",
    "dpdpa-compliance": "privacy_actions",
    "tds-form16b": "tds_forms",
    "epfo-esic-filing": "statutory_filings",
    "job-alerts": "personalised_alerts",
    "mental-health": "wellbeing_checks",
    "carbon-credit": "carbon_credit_projects",
}


def read_state():
    with STATE_LOCK:
        if not DB_PATH.exists():
            _atomic_write(DEFAULT_STATE)
        state = json.loads(DB_PATH.read_text(encoding="utf-8"))
        changed = ensure_advanced_state(state)
        before = json.dumps(state.get("live_services", {}), sort_keys=True)
        ensure_live_services_state(state)
        if json.dumps(state.get("live_services", {}), sort_keys=True) != before:
            changed = True
        if changed:
            _atomic_write(state)
        return state


def write_state(state):
    with STATE_LOCK:
        _atomic_write(state)


def _atomic_write(state):
    tmp_path = DB_PATH.with_suffix(".tmp")
    tmp_path.write_text(json.dumps(state, indent=2), encoding="utf-8")
    tmp_path.replace(DB_PATH)


def now_time():
    return datetime.now().strftime("%H:%M")


def today_label():
    return datetime.now().strftime("%d %b %Y")


def audit(state, user, action, status="OK", ip="127.0.0.1"):
    state["audit_log"].insert(0, {
        "time": now_time(),
        "user": user,
        "action": action,
        "ip": ip,
        "status": status,
    })
    state["audit_log"] = state["audit_log"][:20]


def ensure_live_services_state(state):
    meta = state.setdefault("meta", {})
    meta.setdefault("next_live_service_seq", 1)
    meta.setdefault("next_service_entity_seq", 1)
    services = state.setdefault("live_services", {})
    services.setdefault("records", [])
    services.setdefault("stats", {
        "total_runs": 0,
        "automations_completed": 0,
        "compliance_documents": 0,
        "worker_welfare_actions": 0,
    })
    domains = services.setdefault("domains", {})
    for domain in LIVE_SERVICE_DOMAINS.values():
        domains.setdefault(domain, [])
    return services


def service_by_id(service_id):
    return next((service for service in LIVE_SERVICE_CATALOG if service["id"] == service_id), None)


def _num(value, default=0.0):
    try:
        return float(str(value).replace(",", "").strip() or default)
    except (TypeError, ValueError):
        return default


def _int(value, default=0):
    try:
        return int(float(str(value).replace(",", "").strip() or default))
    except (TypeError, ValueError):
        return default


def service_code(prefix):
    return f"{prefix}-{secrets.token_hex(3).upper()}"


def live_services_payload(state):
    services = ensure_live_services_state(state)
    records = services["records"][:12]
    counts = {}
    for service in LIVE_SERVICE_CATALOG:
        counts[service["cat"]] = counts.get(service["cat"], 0) + 1
    domain_counts = {domain: len(rows) for domain, rows in services.get("domains", {}).items()}
    return {
        "ok": True,
        "services": LIVE_SERVICE_CATALOG,
        "activity": records,
        "domainCounts": domain_counts,
        "stats": {
            **services["stats"],
            "catalog_size": len(LIVE_SERVICE_CATALOG),
            "categories": counts,
            "domain_records": sum(domain_counts.values()),
        },
    }


def live_service_result(service_id, inputs, current_user):
    inputs = inputs or {}
    amount = _num(inputs.get("Taxable Amount") or inputs.get("Payment Amount"))
    rate = _num(inputs.get("GST Rate") or inputs.get("TDS Rate"))
    tax = round(amount * rate / 100)
    workers = _int(inputs.get("Workers Needed") or inputs.get("Workers in Filing"))
    actor = current_user["name"] if current_user else "Public user"

    result_map = {
        "ai-interview": {
            "headline": "Screening complete",
            "message": f"{inputs.get('Worker ID', 'IEE-WK-2026-00045821')} scored 87/100 for {inputs.get('Role', 'Mason')}. Shortlisted for employer review with {inputs.get('Language', 'Hindi')} interview notes and availability marked {inputs.get('Availability', 'Today')}.",
            "items": ["Suggested questions: safety practice, wage expectation, previous site experience.", "Employer action: auto-shortlist and schedule 8 minute call."],
            "status": "Shortlisted",
        },
        "adaptive-learning": {
            "headline": "Learning path ready",
            "message": f"{inputs.get('Current Skill', 'Masonry')} worker in {inputs.get('City', 'Chennai')} should take Advanced Safety, Blueprint Reading and Supervisor Basics. Placement uplift estimate: 31%.",
            "items": ["Course 1: Construction Safety refresh", "Course 2: Blueprint reading", "Course 3: Wage negotiation and supervisor basics"],
            "status": "Path Created",
        },
        "safety-incident": {
            "headline": f"Incident ticket {service_code('SAFE')} created",
            "message": f"Severity {inputs.get('Severity', 'High')} at {inputs.get('Site Name', 'site')} routed to employer safety officer.",
            "items": ["Inspector escalation timer started for high and critical issues.", "Evidence pack and witness notes are attached to the case."],
            "status": "Escalated" if inputs.get("Severity") in {"High", "Critical"} else "Logged",
        },
        "seasonal-surge": {
            "headline": "Surge plan activated",
            "message": f"{workers or 120} {inputs.get('Sector', 'Construction')} workers needed in {inputs.get('District', 'Chennai')}. Forecast demand confidence: 85%.",
            "items": ["Worker pool notified in 5 km, 15 km, and cross-district rings.", "Employer reminder scheduled 48 hours before start window."],
            "status": "Forecast Live",
        },
        "gst-einvoice": {
            "headline": "GST e-invoice generated",
            "message": f"Invoice {service_code('INV')}, IRN {service_code('IRN')}. Taxable value Rs.{int(amount or 85000):,}, GST @ {int(rate or 18)}% = Rs.{int(tax or 15300):,}. Supply type: {inputs.get('Supply Type', 'B2B')}.",
            "items": ["PDF and JSON invoice payload stored for employer download.", "Audit trail linked to GSTIN " + inputs.get("Employer GSTIN", "33AABCS1234Z1Z5")],
            "status": "Invoice Ready",
        },
        "msme-fast-track": {
            "headline": "MSME fast-track approved",
            "message": f"Provisional Employer ID {service_code('EMP')} issued for {inputs.get('Business Name', 'Skyline Works')}. Job posting access enabled while KYC is queued.",
            "items": ["Udyam number captured for KYC verification.", "First three job posts are allowed under provisional risk limits."],
            "status": "Provisioned",
        },
        "nps-lite": {
            "headline": "NPS-Lite workflow updated",
            "message": "Opt-out recorded with consent log." if inputs.get("Consent") == "Opt out" else f"PRAN {service_code('PRAN')} generated. Contribution per payment: Rs.{inputs.get('Contribution per Payment', '50')}. Employer match: {inputs.get('Employer Match', 'No match')}.",
            "items": ["Worker can view projected corpus in welfare dashboard.", "Consent event stored with timestamp and actor."],
            "status": "Opted Out" if inputs.get("Consent") == "Opt out" else "Enrolled",
        },
        "benefits-portability": {
            "headline": "Benefits portability checked",
            "message": f"{inputs.get('Worker ID', 'Worker')} moving from {inputs.get('From State', 'Tamil Nadu')} to {inputs.get('To State', 'Karnataka')}. {inputs.get('Benefit', 'All')} routing status: portable.",
            "items": ["Ration, insurance, and BOCW eligibility mapped to destination state.", "District helpdesk contact added to worker notification."],
            "status": "Portable",
        },
        "api-marketplace": {
            "headline": "API sandbox issued",
            "message": f"Key {service_code('API')} for {inputs.get('HRMS', 'HRMS')} with scope {inputs.get('Scope', 'Worker verification')}. Webhook subscribed at {inputs.get('Callback URL', 'callback URL')}.",
            "items": ["OAuth client and rate limit policy created.", "Swagger-style endpoint pack is ready for HRMS testing."],
            "status": "Sandbox Active",
        },
        "referral-network": {
            "headline": "Referral created",
            "message": f"Code REF-{secrets.token_hex(3).upper()} linked to {inputs.get('Employer ID', 'EMP')}. Reward estimate: Rs.1,500 after first verified hire by {inputs.get('Referred Business', 'referred employer')}.",
            "items": ["Anti-fraud duplicate business check queued.", "Referral conversion dashboard updated."],
            "status": "Tracking",
        },
        "accessibility": {
            "headline": "Accessibility profile saved",
            "message": f"{inputs.get('Accessibility Need', 'Mobility support')} matched with 12 suitable jobs for {inputs.get('Job Preference', 'accessible work')}. UI mode: {inputs.get('UI Mode', 'Standard')}.",
            "items": ["Accessible-site filter turned on for future job alerts.", "Screen-reader labels and larger focus targets enabled in session."],
            "status": "Preferences Saved",
        },
        "women-night-safety": {
            "headline": "Safety validation complete",
            "message": f"{inputs.get('Worker Name', 'Worker')} {'requires transport, SOS contact and POSH compliance before approval' if inputs.get('Shift') == 'Night' else 'is cleared for day-shift matching'}. Transport declaration: {inputs.get('Transport Provided', 'No')}.",
            "items": ["Emergency escalation group mapped to the site.", "POSH compliance evidence requested from employer."],
            "status": "Safety Checked",
        },
        "blockchain-credential": {
            "headline": "Credential verified",
            "message": f"{inputs.get('Certificate ID', 'certificate')} from {inputs.get('Issuer', 'issuer')} anchored with proof hash 0x{secrets.token_hex(6)}. Verification time: 2.4 seconds.",
            "items": ["QR verification event logged.", "Credential issuer and worker ID match the registry record."],
            "status": "Verified",
        },
        "dispute-chatbot": {
            "headline": f"Dispute case {service_code('CASE')} opened",
            "message": f"Type {inputs.get('Dispute Type', 'Payment delay')} classified for {inputs.get('Language', 'English')} response. Bot reply: payment evidence requested; SLA clock started.",
            "items": ["Tier-1 chatbot collected the complaint summary.", "Labour inspector escalation will trigger if not resolved within SLA."],
            "status": "Case Open",
        },
        "dpdpa-compliance": {
            "headline": "DPDPA action complete",
            "message": f"{inputs.get('Action', 'Anonymise export')} applied to {inputs.get('Dataset', 'dataset')} for {inputs.get('Record Count', '1250')} records. Direct identifiers removed and consent log updated.",
            "items": ["Privacy impact note stored.", "Only anonymised aggregates are available to employer dashboards."],
            "status": "Compliant",
        },
        "tds-form16b": {
            "headline": "TDS calculated",
            "message": f"Payment Rs.{int(amount or 50000):,}, rate {int(rate or 2)}%, deduction Rs.{int(tax or 1000):,}. Form 16B draft {service_code('F16B')} created for PAN {inputs.get('Worker PAN', 'ABCDE1234F')}.",
            "items": ["Quarterly statement updated.", "TRACES-style filing package prepared for employer review."],
            "status": "Form Drafted",
        },
        "epfo-esic-filing": {
            "headline": "Statutory filing prepared",
            "message": f"{workers or 148} workers included for {inputs.get('Month', 'April 2026')}. ECR {service_code('ECR')} and challan {service_code('CHLN')} ready for {inputs.get('Scheme', 'EPFO + ESIC')}.",
            "items": ["UAN generation queue refreshed for new workers.", "Compliance certificate will unlock after employer confirmation."],
            "status": "Filing Ready",
        },
        "job-alerts": {
            "headline": "Personalised alerts generated",
            "message": f"5 jobs ranked for {inputs.get('Role', 'Mason')} within {inputs.get('Max Distance KM', '5')} km above Rs.{inputs.get('Minimum Wage', '800')}/day.",
            "items": ["Metro Works - 96% match - Rs.950/day", "Skyline Site - 91% match - Rs.875/day", "Prestige Builders - 84% match - Rs.825/day"],
            "status": "Alerts Sent",
        },
        "mental-health": {
            "headline": "Wellbeing check-in complete",
            "message": f"Mood {inputs.get('Mood Today', 'Stressed')}, sleep {inputs.get('Sleep Quality', 'Average')}. Recommended support: {inputs.get('Support Mode', 'Anonymous chat')}.",
            "items": ["High-risk escalation is enabled only for severe indicators.", "Employer dashboards receive anonymised aggregate signals only."],
            "status": "Support Routed",
        },
        "carbon-credit": {
            "headline": "Green credit estimate ready",
            "message": f"{inputs.get('Project Name', 'Project')} can claim approximately {max(1, round((_num(inputs.get('Cement Saved Tonnes'), 35) * 0.8) + (_num(inputs.get('Recycled Waste Tonnes'), 120) * 0.05)))} tCO2e credits. Audit queue {service_code('GREEN')} created.",
            "items": ["Third-party audit checklist generated.", "Green Employer badge will publish after verification."],
            "status": "Audit Queued",
        },
    }

    result = result_map.get(service_id, {"headline": "Service completed", "message": "The platform workflow completed successfully.", "items": [], "status": "Completed"})
    result["actor"] = actor
    return result


def live_service_entity(state, service_id, inputs, result):
    service = service_by_id(service_id) or {"title": service_id, "cat": "platform"}
    domain = LIVE_SERVICE_DOMAINS.get(service_id, "service_records")
    entity_id = f"{domain[:3].upper()}-{state['meta']['next_service_entity_seq']:06d}"
    state["meta"]["next_service_entity_seq"] += 1
    base = {
        "entityId": entity_id,
        "serviceId": service_id,
        "service": service["title"],
        "domain": domain,
        "category": service["cat"],
        "status": result.get("status", "Completed"),
        "headline": result.get("headline", "Service completed"),
        "createdAt": datetime.now().isoformat(timespec="seconds"),
        "date": today_label(),
        "time": now_time(),
        "inputs": inputs,
        "summary": result.get("message", ""),
    }
    detail_map = {
        "gst-einvoice": {"documentType": "GST_E_INVOICE", "gstin": inputs.get("Employer GSTIN"), "taxableAmount": _num(inputs.get("Taxable Amount")), "gstRate": _num(inputs.get("GST Rate"))},
        "tds-form16b": {"documentType": "FORM_16B", "pan": inputs.get("Worker PAN"), "paymentAmount": _num(inputs.get("Payment Amount")), "tdsRate": _num(inputs.get("TDS Rate"))},
        "epfo-esic-filing": {"documentType": "STATUTORY_FILING", "employerId": inputs.get("Employer ID"), "workers": _int(inputs.get("Workers in Filing")), "scheme": inputs.get("Scheme")},
        "safety-incident": {"site": inputs.get("Site Name"), "severity": inputs.get("Severity"), "incidentType": inputs.get("Incident Type")},
        "dispute-chatbot": {"caseType": inputs.get("Dispute Type"), "language": inputs.get("Language"), "sla": "24 hours"},
        "api-marketplace": {"hrms": inputs.get("HRMS"), "scope": inputs.get("Scope"), "callbackUrl": inputs.get("Callback URL")},
        "job-alerts": {"role": inputs.get("Role"), "maxDistanceKm": _num(inputs.get("Max Distance KM")), "minimumWage": _num(inputs.get("Minimum Wage"))},
        "carbon-credit": {"project": inputs.get("Project Name"), "estimatedCredits": max(1, round((_num(inputs.get("Cement Saved Tonnes"), 35) * 0.8) + (_num(inputs.get("Recycled Waste Tonnes"), 120) * 0.05)))},
        "nps-lite": {"workerId": inputs.get("Worker ID"), "contribution": _num(inputs.get("Contribution per Payment")), "consent": inputs.get("Consent")},
        "benefits-portability": {"workerId": inputs.get("Worker ID"), "fromState": inputs.get("From State"), "toState": inputs.get("To State"), "benefit": inputs.get("Benefit")},
        "blockchain-credential": {"certificateId": inputs.get("Certificate ID"), "issuer": inputs.get("Issuer"), "workerId": inputs.get("Worker ID")},
        "women-night-safety": {"workerName": inputs.get("Worker Name"), "site": inputs.get("Site"), "shift": inputs.get("Shift"), "transportProvided": inputs.get("Transport Provided")},
        "mental-health": {"mood": inputs.get("Mood Today"), "sleepQuality": inputs.get("Sleep Quality"), "supportMode": inputs.get("Support Mode"), "privacy": "anonymised-for-employer"},
        "dpdpa-compliance": {"dataset": inputs.get("Dataset"), "action": inputs.get("Action"), "recordCount": _int(inputs.get("Record Count"))},
        "msme-fast-track": {"udyamNumber": inputs.get("Udyam Number"), "businessName": inputs.get("Business Name"), "entityType": inputs.get("Entity Type")},
        "referral-network": {"employerId": inputs.get("Employer ID"), "referredBusiness": inputs.get("Referred Business"), "rewardStatus": "pending-first-hire"},
        "adaptive-learning": {"skill": inputs.get("Current Skill"), "city": inputs.get("City"), "goal": inputs.get("Goal")},
        "ai-interview": {"workerId": inputs.get("Worker ID"), "role": inputs.get("Role"), "language": inputs.get("Language"), "score": 87},
        "seasonal-surge": {"sector": inputs.get("Sector"), "district": inputs.get("District"), "workersNeeded": _int(inputs.get("Workers Needed")), "window": inputs.get("Window")},
        "accessibility": {"need": inputs.get("Accessibility Need"), "jobPreference": inputs.get("Job Preference"), "uiMode": inputs.get("UI Mode")},
    }
    base.update(detail_map.get(service_id, {}))
    return domain, base


def result_to_html(result):
    items = "".join(f'<div class="mini-item">{escape(str(item))}</div>' for item in result.get("items", []))
    return (
        f'<strong>{escape(result.get("headline", "Service completed"))}:</strong> '
        f'{escape(result.get("message", ""))}'
        f'{f"<div class=\"mini-list\">{items}</div>" if items else ""}'
    )


def advanced_state(state):
    ensure_advanced_state(state)
    return state["advanced"]


def find_advanced_worker(state, worker_id):
    return next((row for row in advanced_state(state)["worker_registry"] if row.get("worker_id") == worker_id), None)


def find_advanced_employer(state, employer_id):
    return next((row for row in advanced_state(state)["employer_registry"] if row.get("employer_id") == employer_id), None)


def prepend_advanced_alert(state, title, body, time_label="Just now", unread=True):
    alerts = advanced_state(state)["alerts"]
    alerts.insert(0, {
        "title": title,
        "body": body,
        "time": time_label,
        "unread": unread,
    })
    del alerts[12:]


def prepend_advanced_feed(state, tone, title, meta):
    live_feed = advanced_state(state)["live_feed"]
    live_feed.insert(0, {
        "tone": tone,
        "title": title,
        "meta": meta,
    })
    del live_feed[12:]


def module_payload(state, context, name, current_user):
    name = (name or "").strip().lower()
    user_name = current_user["name"] if current_user else "Current User"
    worker_apps = []
    for job in state["jobs"]:
        if user_name in job.get("applicants", []):
            worker_apps.append([job["title"], job["employer"], f"Rs.{job['wage']}/day", "Applied"])

    shared_courses = [
        ["Advanced Masonry - Level 2", "In Progress", "65%", "Resume module 4"],
        ["Construction Safety (OSHA)", "Completed", "100%", "Certificate ready"],
        ["Waterproofing Techniques", "Not Started", "20%", "Recommended next"],
    ]
    payment_rows = [
        ["12 Apr 2026", "Skyline Constructions", "Rs.2,550", "Settled"],
        ["08 Apr 2026", "Prestige Builders", "Rs.3,750", "Settled"],
        ["01 Apr 2026", "CMRL Phase 2", "Rs.9,000", "Processing"],
    ]
    notif_rows = [
        ["New nearby job alert", "Brick Mason role from Skyline Constructions", "10 min ago"],
        ["Payment update", "Rs.9,000 payout moved to processing", "2 hr ago"],
        ["Training recommendation", "Waterproofing Techniques added to your learning path", "Today"],
    ]
    grievance_rows = [
        ["GR-2041", "Delayed wage credit", "In Review", "Opened 17 Apr 2026"],
        ["GR-1988", "Site attendance mismatch", "Resolved", "Closed 11 Apr 2026"],
    ]
    active_workers = [[w["name"], w["occupation"], w["city"], w["rating"]] for w in state["workers"][:4]]
    verifier_rows = [[u["name"], u.get("verifier_id", "-"), u.get("zone", "-"), u["status"]] for u in state["users"] if u["role"] == "verifier"]
    employer_rows = [[u["name"], u.get("employer_id", "-"), u.get("sector", "-"), u["status"]] for u in state["users"] if u["role"] == "employer"]
    worker_rows = [[u["name"], u.get("iee_id", "-"), u.get("occupation", "-"), u["status"]] for u in state["users"] if u["role"] == "worker"]
    flagged_rows = [[u["name"], u["role"].title(), u.get("email") or u.get("mobile") or "-", u["status"]] for u in state["users"] if u["status"] in {"Flagged", "Banned", "Suspended"}]
    notice_rows = [[n["title"], n["category"], n["priority"], n["published"]] for n in state["notices"][:8]]
    audit_rows = [[a["time"], a["user"], a["action"], a["status"]] for a in state["audit_log"][:10]]
    queue_rows = [[q["name"], q["iee_id"], q["role"], q["priority"], q["status"]] for q in state["verification_queue"]]

    modules = {
        ("worker", "my profile"): {
            "title": "My Profile",
            "summary": f"Profile summary for {user_name}.",
            "stats": [{"label": "Verification", "value": current_user.get("status", "Active") if current_user else "Active"},
                      {"label": "Occupation", "value": current_user.get("occupation", "Worker") if current_user else "Worker"},
                      {"label": "City", "value": current_user.get("city", "Tamil Nadu") if current_user else "Tamil Nadu"}],
            "columns": ["Field", "Value"],
            "rows": [["Name", user_name], ["Worker ID", current_user.get("iee_id", current_user.get("ieeId", "-")) if current_user else "-"], ["Mobile", current_user.get("mobile", "-") if current_user else "-"], ["Rating", current_user.get("rating", "4.5/5") if current_user else "4.5/5"]],
        },
        ("worker", "available jobs"): {
            "title": "Available Jobs",
            "summary": "Latest backend-matched jobs based on worker skill and distance.",
            "columns": ["Job", "Employer", "Wage", "Type"],
            "rows": [[j["title"], j["employer"], f"Rs.{j['wage']}/day", j["type"]] for j in state["jobs"][:8]],
        },
        ("worker", "my applications"): {
            "title": "My Applications",
            "summary": "Applications sent from the worker dashboard.",
            "columns": ["Job", "Employer", "Wage", "Status"],
            "rows": worker_apps or [["No applications yet", "-", "-", "Use the Apply buttons on the dashboard"]],
        },
        ("worker", "work history"): {
            "title": "Work History",
            "summary": "Recent completed assignments and outcomes.",
            "columns": ["Employer", "Role", "Days", "Earnings"],
            "rows": [["Skyline Const.", "Mason", "3", "Rs.2,550"], ["Prestige Bldrs", "Plastering", "5", "Rs.3,750"], ["Annur Infra", "Masonry", "7", "Rs.5,600"], ["CMRL Phase 2", "Labour", "10", "Rs.9,000"]],
        },
        ("worker", "earnings & payments"): {
            "title": "Earnings & Payments",
            "summary": "Backend settlement ledger for recent worker payouts.",
            "columns": ["Date", "Employer", "Amount", "Status"],
            "rows": payment_rows,
        },
        ("worker", "upskilling courses"): {
            "title": "Upskilling Courses",
            "summary": "Assigned courses and progress synced from the learning backend.",
            "columns": ["Course", "Status", "Progress", "Note"],
            "rows": shared_courses,
        },
        ("worker", "certifications"): {
            "title": "Certifications",
            "summary": "Issued and pending worker certifications.",
            "columns": ["Certification", "Status", "Issued By", "Action"],
            "rows": [["Construction Safety (OSHA)", "Issued", "IEE Learning", "Download enabled"], ["Masonry Level 1", "Issued", "State Skill Mission", "Verified"], ["Waterproofing Basics", "Pending", "IEE Learning", "Complete course"]],
        },
        ("worker", "notifications"): {
            "title": "Notifications",
            "summary": "Recent account, job, and payment notifications.",
            "columns": ["Type", "Message", "When"],
            "rows": notif_rows,
        },
        ("worker", "grievance & support"): {
            "title": "Grievance & Support",
            "summary": "Support cases and grievance handling status.",
            "columns": ["Ticket", "Issue", "Status", "Note"],
            "rows": grievance_rows,
        },
        ("employer", "company profile"): {
            "title": "Company Profile",
            "summary": "Employer registration and verification details.",
            "columns": ["Field", "Value"],
            "rows": [["Company", current_user["name"] if current_user else "Employer"], ["Employer ID", current_user.get("employer_id", current_user.get("empId", "-")) if current_user else "-"], ["Sector", current_user.get("sector", "Construction") if current_user else "Construction"], ["City", current_user.get("city", "Tamil Nadu") if current_user else "Tamil Nadu"]],
        },
        ("employer", "post a single job"): {
            "title": "Post a Single Job",
            "summary": "Use the job form on the dashboard; backend posting is active.",
            "columns": ["Recently Posted Job", "Employer", "Wage", "Type"],
            "rows": [[j["title"], j["employer"], f"Rs.{j['wage']}/day", j["type"]] for j in state["jobs"][-4:]],
        },
        ("employer", "bulk hiring request"): {
            "title": "Bulk Hiring Requests",
            "summary": "Most recent multi-position requests received by the backend.",
            "columns": ["Category", "Workers", "Location", "Status"],
            "rows": [[r["category"], r["workers_required"], r["location"], "Matching"] for r in state["bulk_requests"][-8:]] or [["No bulk requests yet", "-", "-", "Submit from dashboard"]],
        },
        ("employer", "browse verified workers"): {
            "title": "Verified Workers",
            "summary": "Backend-available worker pool for direct hiring.",
            "columns": ["Name", "Role", "City", "Rating"],
            "rows": active_workers,
        },
        ("employer", "my posted jobs"): {
            "title": "My Posted Jobs",
            "summary": "Jobs currently stored in the employer hiring backend.",
            "columns": ["Job", "Employer", "Wage", "Applicants"],
            "rows": [[j["title"], j["employer"], f"Rs.{j['wage']}/day", len(j.get("applicants", []))] for j in state["jobs"]],
        },
        ("employer", "active workforce"): {
            "title": "Active Workforce",
            "summary": "Workers currently available or assigned to the employer network.",
            "columns": ["Name", "Role", "City", "Rating"],
            "rows": active_workers,
        },
        ("employer", "payroll & payments"): {
            "title": "Payroll & Payments",
            "summary": "Latest payout and settlement data for employer operations.",
            "columns": ["Batch", "Workers", "Amount", "Status"],
            "rows": [["PAY-204", "18", "Rs.48,600", "Released"], ["PAY-203", "12", "Rs.31,200", "Processing"], ["PAY-202", "24", "Rs.67,850", "Settled"]],
        },
        ("employer", "analytics & reports"): {
            "title": "Analytics & Reports",
            "summary": "Hiring performance metrics from the employer backend.",
            "stats": [{"label": "Fill Rate", "value": "94%"}, {"label": "Avg. Time", "value": "1.8 hr"}, {"label": "Retention", "value": "89%"}],
            "columns": ["Metric", "Value"],
            "rows": [["Open positions", "12"], ["Active workers hired", "148"], ["Urgent roles", "3"], ["Employer NPS", "+42"]],
        },
        ("verifier", "pending kyc"): {
            "title": "Pending KYC",
            "summary": "Live backend queue of profiles awaiting field verification.",
            "columns": ["Worker", "IEE ID", "Role", "Priority", "Status"],
            "rows": [r for r in queue_rows if r[4] == "Pending"] or [["No pending records", "-", "-", "-", "-"]],
        },
        ("verifier", "completed today"): {
            "title": "Completed Today",
            "summary": "Verification items already processed today.",
            "columns": ["Worker", "IEE ID", "Role", "Priority", "Status"],
            "rows": [r for r in queue_rows if r[4] == "Approved"] or [["No completed verifications yet", "-", "-", "-", "-"]],
        },
        ("verifier", "rejected / flagged"): {
            "title": "Rejected / Flagged",
            "summary": "Profiles requiring review, rejection, or fraud escalation.",
            "columns": ["Worker", "IEE ID", "Role", "Priority", "Status"],
            "rows": [r for r in queue_rows if r[4] in {"Rejected", "Flagged"}] or [["No rejected or flagged profiles", "-", "-", "-", "-"]],
        },
        ("verifier", "field kyc upload"): {
            "title": "Field KYC Upload",
            "summary": "The Field KYC form on the dashboard is backend-enabled and stores submissions.",
            "columns": ["Field", "Status"],
            "rows": [["Worker lookup", "Active"], ["Aadhaar capture", "Active"], ["Document type", "Active"], ["Notes", "Stored in backend"]],
        },
        ("verifier", "qr scanner"): {
            "title": "QR Scanner",
            "summary": "QR verification service is connected for on-site verification actions.",
            "columns": ["Scanner Flow", "Status"],
            "rows": [["Public verification QR", "Ready"], ["Field KYC QR", "Ready"], ["ID validation", "Ready"]],
        },
        ("verifier", "zone map"): {
            "title": "Zone Map",
            "summary": "Verifier zone coverage and assignment data.",
            "columns": ["Zone", "Coverage", "Verifier"],
            "rows": [["Zone 1", "South Chennai", "Team A"], ["Zone 2", "Central Chennai", "Team B"], ["Zone 3", "North Chennai", "S. Anbarasan"], ["Zone 4", "West Chennai", "Team D"]],
        },
        ("verifier", "my statistics"): {
            "title": "My Statistics",
            "summary": "Verifier performance snapshot.",
            "stats": [{"label": "Verified", "value": "247"}, {"label": "Completed Today", "value": "12"}, {"label": "Rejected", "value": "14"}],
            "columns": ["Metric", "Value"],
            "rows": [["High priority resolved", "8"], ["Average turnaround", "22 min"], ["Field visits", "6 today"]],
        },
        ("verifier", "monthly report"): {
            "title": "Monthly Report",
            "summary": "Operational report for verifier activity this month.",
            "columns": ["Category", "Count", "Comment"],
            "rows": [["Approved", "103", "Steady throughput"], ["Rejected", "14", "Mostly document mismatch"], ["Flagged", "6", "Escalated"], ["Remote KYC", "19", "Supervisor reviewed"]],
        },
        ("superadmin", "all users"): {
            "title": "All Users",
            "summary": "Full user registry from the administration backend.",
            "columns": ["Name", "Role", "Login", "Status"],
            "rows": [[u["name"], u["role"].title(), u.get("email") or u.get("mobile") or u.get("login_id"), u["status"]] for u in state["users"] if u["role"] != "superadmin"],
        },
        ("superadmin", "worker profiles"): {
            "title": "Worker Profiles",
            "summary": "All worker accounts and worker registry details.",
            "columns": ["Worker", "IEE ID", "Occupation", "Status"],
            "rows": worker_rows,
        },
        ("superadmin", "employer accounts"): {
            "title": "Employer Accounts",
            "summary": "Registered employer organizations and status.",
            "columns": ["Employer", "Employer ID", "Sector", "Status"],
            "rows": employer_rows,
        },
        ("superadmin", "verifier management"): {
            "title": "Verifier Management",
            "summary": "Verifier roster and zone assignments.",
            "columns": ["Verifier", "Verifier ID", "Zone", "Status"],
            "rows": verifier_rows,
        },
        ("superadmin", "all job postings"): {
            "title": "All Job Postings",
            "summary": "All jobs currently visible in the hiring backend.",
            "columns": ["Job", "Employer", "Wage", "Applicants"],
            "rows": [[j["title"], j["employer"], f"Rs.{j['wage']}/day", len(j.get("applicants", []))] for j in state["jobs"]],
        },
        ("superadmin", "payment ledger"): {
            "title": "Payment Ledger",
            "summary": "Top-level payment settlements across the platform.",
            "columns": ["Reference", "Party", "Amount", "Status"],
            "rows": [["LED-301", "Skyline Constructions", "Rs.48,600", "Settled"], ["LED-302", "Worker payouts", "Rs.31,200", "Processing"], ["LED-303", "Training reimbursements", "Rs.12,400", "Released"]],
        },
        ("superadmin", "flagged profiles"): {
            "title": "Flagged Profiles",
            "summary": "Accounts requiring admin review or enforcement action.",
            "columns": ["Name", "Role", "Contact", "Status"],
            "rows": flagged_rows or [["No flagged profiles", "-", "-", "-"]],
        },
        ("superadmin", "broadcast notices"): {
            "title": "Broadcast Notices",
            "summary": "Published announcements across the portal.",
            "columns": ["Title", "Category", "Priority", "Published"],
            "rows": notice_rows or [["No notices published yet", "-", "-", "-"]],
        },
        ("superadmin", "system settings"): {
            "title": "System Settings",
            "summary": "Current platform configuration snapshot.",
            "columns": ["Setting", "Value"],
            "rows": [["Public registration", "Enabled"], ["Captcha protection", "Enabled"], ["Admin hidden access", "Enabled"], ["Data persistence", "Local JSON backend"]],
        },
        ("superadmin", "role & permissions"): {
            "title": "Role & Permissions",
            "summary": "Core access model across the platform.",
            "columns": ["Role", "Access", "Scope"],
            "rows": [["Worker", "Self-service", "Jobs, payments, profile"], ["Employer", "Hiring", "Post jobs, hire, payroll"], ["Verifier", "Field ops", "Queue, KYC, QR tools"], ["Super Admin", "Full control", "All users and platform settings"]],
        },
        ("superadmin", "audit log"): {
            "title": "Audit Log",
            "summary": "Most recent tracked platform actions.",
            "columns": ["Time", "User", "Action", "Status"],
            "rows": audit_rows,
        },
    }

    default_module = {
        "title": name.title(),
        "summary": "Backend module is available.",
        "columns": ["Item", "Status"],
        "rows": [[name.title(), "Available"]],
    }
    return modules.get((context, name), default_module)


def user_payload(user):
    payload = {
        "role": user["role"],
        "name": user["name"],
        "status": user.get("status", "Active"),
    }
    if user["role"] == "worker":
        payload.update({
            "ieeId": user.get("iee_id"),
            "occupation": user.get("occupation", "Worker"),
            "city": user.get("city", ""),
            "mobile": user.get("mobile", ""),
            "rating": user.get("rating", "4.5/5"),
            "jobsCompleted": user.get("jobs_completed", 0),
        })
    elif user["role"] == "employer":
        payload.update({
            "empId": user.get("employer_id"),
            "city": user.get("city", ""),
            "sector": user.get("sector", ""),
            "email": user.get("email", ""),
        })
    elif user["role"] == "verifier":
        payload.update({
            "verifierId": user.get("verifier_id"),
            "zone": user.get("zone", ""),
            "email": user.get("email", ""),
        })
    return payload


def find_user(state, role, identifier):
    identifier = (identifier or "").strip().lower()
    for user in state["users"]:
        if user["role"] != role:
            continue
        options = [user.get("login_id", ""), user.get("email", ""), user.get("mobile", ""), user.get("iee_id", ""), user.get("employer_id", ""), user.get("verifier_id", "")]
        lowered = [str(v).strip().lower() for v in options if v]
        if identifier in lowered:
            return user
    return None


def find_worker(state, identifier):
    lookup = (identifier or "").strip().upper()
    for worker in state["workers"]:
        if lookup in {worker["iee_id"].upper(), worker["mobile"], worker["name"].upper()}:
            return worker
    for user in state["users"]:
        if user["role"] != "worker":
            continue
        if lookup in {str(user.get("iee_id", "")).upper(), str(user.get("mobile", "")).upper(), user["name"].upper()}:
            return {
                "name": user["name"],
                "iee_id": user.get("iee_id", ""),
                "mobile": user.get("mobile", ""),
                "occupation": user.get("occupation", "General Labour"),
                "city": user.get("city", "Tamil Nadu"),
                "rating": user.get("rating", "4.2/5"),
                "jobs_completed": user.get("jobs_completed", 0),
                "status": "Verified" if user.get("status") == "Active" else user.get("status", "Pending"),
                "skills": [user.get("occupation", "General Labour")],
            }
    return None


def new_session(state, user):
    token = secrets.token_hex(16)
    state["sessions"][token] = {"login_id": user["login_id"], "role": user["role"]}
    return token


APP_SCRIPT = r"""
const api = async (path, options = {}) => {
  const cfg = { credentials: 'same-origin', headers: {}, ...options };
  if (cfg.body && typeof cfg.body !== 'string') {
    cfg.headers['Content-Type'] = 'application/json';
    cfg.body = JSON.stringify(cfg.body);
  }
  const res = await fetch(path, cfg);
  const data = await res.json().catch(() => ({}));
  if (!res.ok || data.ok === false) {
    throw new Error(data.message || 'Request failed');
  }
  return data;
};

let currentUser = null;
let clicks = 0;
let ctimer = null;

const portalPageByRole = {
  worker: 'worker-page',
  employer: 'employer-page',
  verifier: 'verifier-page',
  superadmin: 'superadmin-page',
};
const allowedPagesByRole = {
  worker: ['worker-page'],
  employer: ['employer-page'],
  verifier: ['verifier-page'],
  superadmin: ['superadmin-page'],
};

function $(id){ return document.getElementById(id); }

function lockedPortalPage(){
  return currentUser && portalPageByRole[currentUser.role] ? portalPageByRole[currentUser.role] : null;
}

function updateSessionChrome(){
  const locked = !!lockedPortalPage();
  document.querySelectorAll('.mainnav,.ticker,.footer,.bc').forEach(el => {
    el.style.display = locked ? 'none' : '';
  });
}

function showPage(id){
  const lockedPage = lockedPortalPage();
  const allowedPages = currentUser && allowedPagesByRole[currentUser.role] ? allowedPagesByRole[currentUser.role] : [];
  if (lockedPage && !allowedPages.includes(id)) {
    id = lockedPage;
    showToast('Please sign out before opening another page or portal.', 'warn');
  }
  document.querySelectorAll('.page').forEach(p => p.classList.remove('show'));
  const pg = $(id);
  if(pg){ pg.classList.add('show'); window.scrollTo(0,0); }
  updateSessionChrome();
}

function setNav(el){
  document.querySelectorAll('.nl').forEach(n => n.classList.remove('act'));
  if (el) el.classList.add('act');
}

function openModal(id){ const el = $(id); if(el) el.classList.add('show'); }
function closeModal(id){ const el = $(id); if(el) el.classList.remove('show'); }

function setMTab(id, el){
  document.querySelectorAll('.mtab').forEach(t => t.classList.remove('act'));
  document.querySelectorAll('.mpane').forEach(p => p.classList.remove('show'));
  if (el) el.classList.add('act');
  const pane = $('mp-' + id);
  if (pane) pane.classList.add('show');
}

function portalNav(role, section, el){
  if (!currentUser || currentUser.role !== role) {
    showToast('Please sign in to the correct portal first.', 'warn');
    return;
  }
  const page = $(role + '-page');
  if (!page) return;
  page.querySelectorAll('.portal-section').forEach(s => s.classList.remove('on'));
  const target = $(role + '-' + section);
  if (target) target.classList.add('on');
  page.querySelectorAll('.dlink').forEach(l => l.classList.remove('act'));
  if (el) el.classList.add('act');
  if (role === 'worker' && section === 'schemes') renderWorkerSchemes();
  window.scrollTo(0, 0);
}

function resetPortal(role){
  const page = $(role + '-page');
  if (!page) return;
  page.querySelectorAll('.portal-section').forEach(s => s.classList.remove('on'));
  const overview = $(role + '-overview');
  if (overview) overview.classList.add('on');
  page.querySelectorAll('.dlink').forEach(l => l.classList.remove('act'));
  const first = page.querySelector(".dlink[onclick*=\"'overview'\"]");
  if (first) first.classList.add('act');
}

function renderWorkerSchemes(){
  const box = $('worker-launched-scheme');
  if (!box) return;
  const launched = localStorage.getItem('ieeLaunchedScheme') || 'PM-SAYSAM - Wage Insurance';
  box.innerHTML = '<strong>Latest Admin Launch:</strong> ' + launched + ' is available for eligible workers. Review your eligibility below and apply from this portal.';
}

function openWorkerSchemes(){
  const link = [...document.querySelectorAll('#worker-page .dlink')].find(el => el.textContent.includes('Available Schemes'));
  portalNav('worker', 'schemes', link);
}

function applyWorkerScheme(name){
  showToast(name + ' application submitted for worker verification.');
  const rows = document.querySelectorAll('#worker-scheme-table tr');
  rows.forEach(row => {
    if (row.children[0] && row.children[0].textContent.includes(name.split(' ')[0])) {
      const status = row.children[3];
      if (status) status.innerHTML = '<span class="badge b-green">Submitted</span>';
    }
  });
}

const CC='ABCDEFGHJKLMNPQRSTUVWXYZ23456789';
function newCap(id){
  let s='';
  for(let i=0;i<5;i++) s += CC[Math.floor(Math.random()*CC.length)];
  if ($(id)) $(id).textContent = s;
}

function showToast(msg,type){
  const t = $('toast');
  if(!t) return;
  t.textContent = msg;
  t.style.borderLeftColor = type==='danger' ? 'var(--red)' : type==='warn' ? 'var(--orange)' : 'var(--green)';
  t.classList.add('show');
  clearTimeout(t._timer);
  t._timer = setTimeout(() => t.classList.remove('show'), 3400);
}

function updateCard(){
  const name = $('id-name')?.value || 'Worker Name';
  const role = $('id-role')?.value || 'General Labour';
  const loc = $('id-loc')?.value || 'Location';
  const s1 = $('id-skill1')?.value || 'Skill 1';
  const s2 = $('id-skill2')?.value || 'Skill 2';
  const initials = name.split(' ').map(w => w[0] || '').join('').toUpperCase().slice(0,2) || 'WK';
  if ($('ic-name')) $('ic-name').textContent = name;
  if ($('ic-role')) $('ic-role').textContent = role;
  if ($('ic-loc')) $('ic-loc').textContent = loc;
  if ($('ic-s1')) $('ic-s1').textContent = s1;
  if ($('ic-s2')) $('ic-s2').textContent = s2;
  if ($('ic-photo')) $('ic-photo').textContent = initials;
}

function applyUserToDashboard(user){
  if (!user) return;
  if (user.role === 'worker') {
    if ($('w-name')) $('w-name').textContent = user.name;
    if ($('w-iee-id')) $('w-iee-id').textContent = user.ieeId || '';
    if ($('w-dash-title')) $('w-dash-title').textContent = user.name + ' Dashboard';
    if ($('w-dash-sub')) $('w-dash-sub').textContent = `${user.occupation || 'Worker'} - ${user.city || 'Tamil Nadu'}`;
    if ($('w-avatar')) $('w-avatar').textContent = user.name.split(' ').map(w => w[0] || '').join('').toUpperCase().slice(0,2);
  }
  if (user.role === 'employer') {
    if ($('e-name')) $('e-name').textContent = user.name;
    if ($('e-emp-id')) $('e-emp-id').textContent = user.empId || '';
    if ($('e-dash-title')) $('e-dash-title').textContent = user.name + ' Dashboard';
    if ($('e-dash-sub')) $('e-dash-sub').textContent = `${user.name} - ${user.city || 'Tamil Nadu'}`;
  }
  if (user.role === 'verifier') {
    if ($('vf-name')) $('vf-name').textContent = user.name;
    if ($('vf-sub')) $('vf-sub').textContent = `${user.name} - ${user.zone || 'Assigned Zone'} - ID: ${user.verifierId || ''}`;
  }
}

function setLoggedIn(user){
  currentUser = user;
  const hb = $('header-btns');
  if(hb) hb.innerHTML = '<button class="btn-reg" onclick="doLogout()" style="margin-right:6px">Sign Out</button><button class="btn-login" onclick="goDash()">My Dashboard</button>';
  applyUserToDashboard(user);
  updateSessionChrome();
}

async function restoreSession(){
  try {
    const data = await api('/api/session');
    if (data.user) {
      setLoggedIn(data.user);
      resetPortal(data.user.role);
      showPage(portalPageByRole[data.user.role]);
    }
  } catch (_) {}
}

function goDash(){
  if(!currentUser){ openModal('login-modal'); return; }
  showPage(portalPageByRole[currentUser.role]);
}

async function doLogout(){
  try { await api('/api/logout', { method: 'POST' }); } catch (_) {}
  currentUser = null;
  const hb = $('header-btns');
  if(hb) hb.innerHTML = '<button class="btn-reg" onclick="showPage(\'register-page\')" style="margin-right:6px">Register</button><button class="btn-login" onclick="openModal(\'login-modal\')">Login</button>';
  updateSessionChrome();
  showPage('home');
  showToast('You have been signed out securely.');
}

function requireLogin(role){
  if(!currentUser){
    openModal('login-modal');
    if(role==='employer'){
      setTimeout(() => {
        document.querySelectorAll('.mtab').forEach(t => t.classList.remove('act'));
        document.querySelectorAll('.mpane').forEach(p => p.classList.remove('show'));
        const tab = document.querySelectorAll('.mtab')[1];
        const pane = $('mp-employer');
        if(tab) tab.classList.add('act');
        if(pane) pane.classList.add('show');
      }, 100);
    }
    return;
  }
  if (role && currentUser.role !== role && currentUser.role !== 'superadmin') {
    goDash();
    showToast('Please sign out before opening another portal.', 'warn');
    return;
  }
  goDash();
}

function trigAdmin(){
  clicks++;
  clearTimeout(ctimer);
  ctimer = setTimeout(() => { clicks = 0; }, 2200);
  if(clicks >= 5){ clicks = 0; openModal('admin-modal'); }
}

document.addEventListener('keydown', e => {
  if(e.ctrlKey && e.shiftKey && e.altKey && e.key === 'A'){ openModal('admin-modal'); }
});

async function doLogin(role){
  const idMap = {worker:'w-id-inp', employer:'e-id-inp', verifier:'vf-id-inp'};
  const pwMap = {worker:'w-pw-inp', employer:'e-pw-inp', verifier:'vf-pw-inp'};
  const identifier = $(idMap[role])?.value?.trim() || '';
  const password = $(pwMap[role])?.value?.trim() || '';
  try {
    const data = await api('/api/login', { method: 'POST', body: { role, identifier, password } });
    setLoggedIn(data.user);
    closeModal('login-modal');
    resetPortal(role);
    showPage(portalPageByRole[role]);
    showToast(data.message || ('Welcome, ' + data.user.name + '.'));
  } catch (err) {
    showToast(err.message, 'danger');
  }
}

async function doAdminLogin(){
  const identifier = $('sa-id')?.value?.trim() || '';
  const password = $('sa-pw')?.value?.trim() || '';
  try {
    const data = await api('/api/admin/login', { method: 'POST', body: { identifier, password } });
    setLoggedIn(data.user);
    closeModal('admin-modal');
    showPage(portalPageByRole.superadmin);
    showToast(data.message || 'Super Admin access granted. All actions monitored.');
  } catch (err) {
    showToast(err.message, 'danger');
  }
}

function toggleRegFields(){
  const v = $('reg-as')?.value;
  if ($('reg-worker-f')) $('reg-worker-f').style.display = v === 'worker' ? '' : 'none';
  if ($('reg-emp-f')) $('reg-emp-f').style.display = v === 'employer' ? '' : 'none';
}

function registrationPayload(){
  const card = document.querySelector('#register-page .card-bd');
  const inputs = Array.from(card.querySelectorAll('input, select'));
  return {
    accountType: $('reg-as')?.value || 'worker',
    name: inputs[0]?.value?.trim() || '',
    mobile: inputs[1]?.value?.trim() || '',
    email: inputs[2]?.value?.trim() || '',
    password: inputs[3]?.value?.trim() || '',
    city: inputs[4]?.value?.trim() || '',
    occupation: document.querySelector('#reg-worker-f select')?.value || '',
    skill: document.querySelector('#reg-worker-f input')?.value?.trim() || '',
    companyName: document.querySelector('#reg-emp-f input')?.value?.trim() || '',
    sector: document.querySelector('#reg-emp-f select')?.value || '',
  };
}

async function doRegister(){
  const btn = event?.target;
  if (btn) { btn.disabled = true; btn.textContent = 'Processing...'; }
  try {
    const payload = registrationPayload();
    const data = await api('/api/register', { method: 'POST', body: payload });
    showPage('home');
    if ($('w-id-inp')) $('w-id-inp').value = payload.mobile || data.loginId || '';
    showToast(data.message);
  } catch (err) {
    showToast(err.message, 'danger');
  } finally {
    if (btn) { btn.disabled = false; btn.textContent = 'Submit Registration'; }
  }
}

async function generateID(){
  try {
    const payload = {
      name: $('id-name')?.value?.trim() || '',
      role: $('id-role')?.value || '',
      skill1: $('id-skill1')?.value?.trim() || '',
      skill2: $('id-skill2')?.value?.trim() || '',
      location: $('id-loc')?.value?.trim() || '',
    };
    const data = await api('/api/worker-id/generate', { method: 'POST', body: payload });
    if ($('ic-id-disp')) $('ic-id-disp').textContent = data.worker.ieeId;
    if ($('ic-idnum')) $('ic-idnum').textContent = data.worker.ieeId;
    if ($('ic-url')) $('ic-url').textContent = data.worker.ieeId;
    if ($('verify-inp')) $('verify-inp').value = data.worker.ieeId;
    showToast(data.message);
  } catch (err) {
    showToast(err.message, 'danger');
  }
}

async function doVerify(){
  const id = $('verify-inp')?.value?.trim() || '';
  if(!id){ showToast('Please enter a Worker ID.','warn'); return; }
  try {
    const data = await api('/api/workers/verify?id=' + encodeURIComponent(id));
    const r = $('verify-result');
    if (r) {
      r.style.display = 'flex';
      r.textContent = `Worker ${data.worker.ieeId} - Status: ${data.worker.status}. Profile is active and in good standing.`;
    }
    showToast(`Worker ${data.worker.name} verified successfully.`);
  } catch (err) {
    showToast(err.message, 'danger');
  }
}

async function doVerifyPage(){
  const id = $('v-id-inp')?.value?.trim() || '';
  if(!id){ showToast('Please enter a Worker ID.','warn'); return; }
  try {
    const data = await api('/api/workers/verify?id=' + encodeURIComponent(id));
    $('vr-name').textContent = data.worker.name;
    $('vr-iee').textContent = data.worker.ieeId;
    $('vr-role').textContent = data.worker.role;
    $('vr-city').textContent = data.worker.city;
    $('vr-rating').textContent = data.worker.rating;
    $('vr-jobs').textContent = data.worker.jobsCompleted;
    $('v-result').style.display = 'block';
    showToast(`Worker ${data.worker.name} verified successfully.`);
  } catch (err) {
    showToast(err.message, 'danger');
  }
}

async function vAction(rowId, name, action){
  try {
    const data = await api('/api/verifier/action', { method: 'POST', body: { rowId, action } });
    const row = $(rowId);
    if(row){
      row.style.opacity = '.4';
      row.querySelectorAll('button').forEach(b => b.disabled = true);
    }
    showToast(data.message || `${name}: ${action} successfully.`);
  } catch (err) {
    showToast(err.message, 'danger');
  }
}

async function uAction(rowId, action){
  try {
    const data = await api('/api/admin/user-action', { method: 'POST', body: { rowId, action } });
    const row = $(rowId);
    if(row){
      const badge = row.querySelectorAll('.badge')[1] || row.querySelector('.badge');
      if(badge){
        if(action === 'Activated'){ badge.className='badge b-green'; badge.textContent='Active'; row.style.opacity = ''; }
        else if(action === 'Suspended'){ badge.className='badge b-amber'; badge.textContent='Suspended'; row.style.opacity = ''; }
        else if(action === 'Banned'){ badge.className='badge b-red'; badge.textContent='Banned'; row.style.opacity = '.45'; }
      }
    }
    showToast(data.message);
  } catch (err) {
    showToast(err.message, 'danger');
  }
}

function cardByHeading(text){
  return Array.from(document.querySelectorAll('.card')).find(card => {
    const hd = card.querySelector('.card-hd');
    return hd && hd.textContent.includes(text);
  });
}

async function submitBulkHire(){
  try {
    const card = cardByHeading('Bulk Hiring Request');
    const fields = card ? card.querySelectorAll('input, select') : [];
    const data = await api('/api/employer/bulk-hire', {
      method: 'POST',
      body: {
        category: fields[0]?.value || '',
        workersRequired: fields[1]?.value || '',
        location: fields[2]?.value?.trim() || '',
        wage: fields[3]?.value || '',
        duration: fields[4]?.value || '',
        skillLevel: fields[5]?.value || '',
      }
    });
    showToast(data.message);
  } catch (err) {
    showToast(err.message, 'danger');
  }
}

async function submitSingleJob(){
  try {
    const card = cardByHeading('Post a Single Job');
    const fields = card ? card.querySelectorAll('input, select') : [];
    const data = await api('/api/employer/post-job', {
      method: 'POST',
      body: {
        title: fields[0]?.value?.trim() || '',
        sector: fields[1]?.value || '',
        wage: fields[2]?.value || '',
        duration: fields[3]?.value || '',
        address: fields[4]?.value?.trim() || '',
      }
    });
    showToast(data.message);
  } catch (err) {
    showToast(err.message, 'danger');
  }
}

async function hireRecommendedWorker(name){
  try {
    const data = await api('/api/employer/hire', { method: 'POST', body: { name } });
    showToast(data.message);
  } catch (err) {
    showToast(err.message, 'danger');
  }
}

async function submitFieldKyc(){
  try {
    const card = cardByHeading('Field KYC');
    const fields = card ? card.querySelectorAll('input, select, textarea') : [];
    const data = await api('/api/verifier/field-kyc', {
      method: 'POST',
      body: {
        workerLookup: fields[0]?.value?.trim() || '',
        aadhaarLast4: fields[1]?.value?.trim() || '',
        documentType: fields[2]?.value || '',
        physicalPresence: fields[3]?.value || '',
        notes: fields[4]?.value?.trim() || '',
      }
    });
    showToast(data.message);
  } catch (err) {
    showToast(err.message, 'danger');
  }
}

async function createVerifierAccount(){
  try {
    const card = cardByHeading('Create New Verifier Account');
    const fields = card ? card.querySelectorAll('input, select') : [];
    const data = await api('/api/admin/create-verifier', {
      method: 'POST',
      body: {
        name: fields[0]?.value?.trim() || '',
        zone: fields[1]?.value || '',
        email: fields[2]?.value?.trim() || '',
        mobile: fields[3]?.value?.trim() || '',
        password: fields[4]?.value?.trim() || '',
      }
    });
    showToast(data.message);
  } catch (err) {
    showToast(err.message, 'danger');
  }
}

async function publishNotice(){
  try {
    const card = cardByHeading('Broadcast Notice');
    const fields = card ? card.querySelectorAll('input, select, textarea') : [];
    const data = await api('/api/admin/publish-notice', {
      method: 'POST',
      body: {
        title: fields[0]?.value?.trim() || '',
        category: fields[1]?.value || '',
        priority: fields[2]?.value || '',
        content: fields[3]?.value?.trim() || '',
      }
    });
    showToast(data.message);
  } catch (err) {
    showToast(err.message, 'danger');
  }
}

async function applyAvailableJob(index){
  try {
    const buttons = cardByHeading('Available Jobs Near You')?.querySelectorAll('button') || [];
    const data = await api('/api/worker/apply', { method: 'POST', body: { jobIndex: index } });
    if (buttons[index]) buttons[index].disabled = true;
    showToast(data.message);
  } catch (err) {
    showToast(err.message, 'danger');
  }
}

async function genericAction(actionKey){
  try {
    const data = await api('/api/action', { method: 'POST', body: { actionKey } });
    showToast(data.message);
  } catch (err) {
    showToast(err.message, 'danger');
  }
}

function escapeHtml(value){
  return String(value ?? '').replaceAll('&', '&amp;').replaceAll('<', '&lt;').replaceAll('>', '&gt;').replaceAll('"', '&quot;');
}

window.liveServiceCatalog = [];
window.liveServiceActivity = [];

function defaultInputsForService(service){
  const values = {};
  (service.forms || []).forEach(field => {
    const type = field[0], label = field[1], raw = field[2] || '';
    values[label] = type === 'select' ? raw.split('|')[0] : raw;
  });
  return values;
}

function liveServiceById(id){
  return (window.liveServiceCatalog || []).find(item => item.id === id);
}

function renderLiveConsole(activity, stats){
  const consoleEl = $('service-console');
  if (!consoleEl) return;
  const latest = (activity || []).slice(0, 6).map(row => {
    return `[${row.time}] ${row.runId} ${row.entityId || ''} ${row.title} - ${row.status}`;
  }).join('\n');
  consoleEl.textContent =
    `IEE backend service console online.\n` +
    `Catalog: ${(window.liveServiceCatalog || []).length} live modules | Runs: ${stats?.total_runs || 0} | Domain records: ${stats?.domain_records || 0} | Compliance docs: ${stats?.compliance_documents || 0}\n\n` +
    (latest || 'No service runs yet. Open any service and generate a live result.');
}

function ensureOperationsPanel(){
  if ($('backend-ops-panel')) return $('backend-ops-panel');
  const consoleCard = $('service-console')?.closest('.card');
  if (!consoleCard) return null;
  const panel = document.createElement('div');
  panel.className = 'card';
  panel.id = 'backend-ops-panel';
  panel.style.marginTop = '18px';
  panel.innerHTML = `
    <div class="card-hd green" style="justify-content:space-between">
      <span>Backend Operations Centre</span>
      <button class="btn-w btn-sm" onclick="refreshBackendOperations()">Refresh</button>
    </div>
    <div class="card-bd" id="backend-ops-body">
      <div class="alert a-info">Backend status loading...</div>
    </div>`;
  consoleCard.insertAdjacentElement('afterend', panel);
  return panel;
}

function renderBackendOperations(payload, health){
  ensureOperationsPanel();
  const body = $('backend-ops-body');
  if (!body) return;
  const stats = payload?.stats || {};
  const domains = payload?.domainCounts || {};
  const activity = payload?.activity || [];
  const topDomains = Object.entries(domains).filter(([, count]) => count > 0).slice(0, 8);
  body.innerHTML = `
    <div class="alert ${health?.status === 'healthy' ? 'a-success' : 'a-warn'}">
      Backend ${escapeHtml(health?.status || 'online')} - ${escapeHtml(health?.service || 'IEE Portal Backend')} - ${escapeHtml(health?.time || '')}
    </div>
    <div class="stat-row" style="margin-bottom:14px">
      <div class="sbox"><div class="sval">${stats.catalog_size || 20}</div><div class="slbl">Service APIs</div><div class="schg sup">Catalog loaded</div></div>
      <div class="sbox gr"><div class="sval">${stats.total_runs || 0}</div><div class="slbl">Backend Runs</div><div class="schg sup">Persisted workflows</div></div>
      <div class="sbox or"><div class="sval">${stats.domain_records || 0}</div><div class="slbl">Domain Records</div><div class="schg sup">Invoices, filings, cases</div></div>
      <div class="sbox sa"><div class="sval">${stats.compliance_documents || 0}</div><div class="slbl">Compliance Docs</div><div class="schg sup">GST, TDS, EPFO/ESIC</div></div>
    </div>
    <div style="display:grid;grid-template-columns:1fr 1fr;gap:14px">
      <div>
        <div style="font-size:11px;font-weight:700;color:var(--navy);letter-spacing:.04em;text-transform:uppercase;margin-bottom:8px">Active Domain Stores</div>
        <div class="mini-list">
          ${(topDomains.length ? topDomains : [['No records yet', 0]]).map(([name,count]) => `<div class="mini-item" style="display:flex;justify-content:space-between;gap:10px"><span>${escapeHtml(name)}</span><strong>${count}</strong></div>`).join('')}
        </div>
      </div>
      <div>
        <div style="font-size:11px;font-weight:700;color:var(--navy);letter-spacing:.04em;text-transform:uppercase;margin-bottom:8px">Latest Backend Activity</div>
        <div class="mini-list">
          ${(activity.length ? activity.slice(0,5) : [{runId:'-', title:'No workflow runs yet', status:'Ready', time:'--:--'}]).map(row => `<div class="mini-item"><strong>${escapeHtml(row.runId || '-')}</strong> ${escapeHtml(row.entityId || '')}<br><span>${escapeHtml(row.title || '')} - ${escapeHtml(row.status || '')} - ${escapeHtml(row.time || '')}</span></div>`).join('')}
        </div>
      </div>
    </div>`;
}

async function refreshBackendOperations(){
  try {
    const [payload, health] = await Promise.all([
      api('/api/live-services'),
      api('/api/health')
    ]);
    window.liveServiceActivity = payload.activity || [];
    renderLiveConsole(window.liveServiceActivity, payload.stats || {});
    renderBackendOperations(payload, health);
  } catch (err) {
    showToast(err.message, 'danger');
  }
}

async function loadLiveServices(){
  try {
    const [data, health] = await Promise.all([
      api('/api/live-services'),
      api('/api/health')
    ]);
    window.liveServiceCatalog = data.services || [];
    window.liveServiceActivity = data.activity || [];
    if (typeof renderLiveServices === 'function' && $('live-grid')) {
      renderLiveServices(window.liveServiceCatalog);
    }
    renderLiveConsole(window.liveServiceActivity, data.stats || {});
    renderBackendOperations(data, health);
  } catch (err) {
    const consoleEl = $('service-console');
    if (consoleEl) consoleEl.textContent = 'Live service backend unavailable: ' + err.message;
  }
}

async function ensureLiveServicesLoaded(){
  if (!window.liveServiceCatalog || !window.liveServiceCatalog.length) {
    await loadLiveServices();
  }
}

function getLiveInputs(){
  const out = {};
  document.querySelectorAll('#lf-body .live-input').forEach(el => {
    out[el.dataset.label] = el.value;
  });
  return out;
}

function ensureLiveFeatureModal(){
  if ($('live-feature-modal')) return;
  const wrap = document.createElement('div');
  wrap.className = 'overlay';
  wrap.id = 'live-feature-modal';
  wrap.onclick = function(event){ if(event.target === this) closeModal('live-feature-modal'); };
  wrap.innerHTML = `
    <div class="modal" style="width:680px;max-width:96vw">
      <div class="modal-hd">
        <h3 id="lf-title">Portal Tool</h3>
        <button class="mclose" onclick="closeModal('live-feature-modal')">&times;</button>
      </div>
      <div class="modal-bd" id="lf-body"></div>
    </div>`;
  document.body.appendChild(wrap);
}

async function openFeatureModal(id){
  await ensureLiveServicesLoaded();
  ensureLiveFeatureModal();
  const f = liveServiceById(id);
  if (!f) {
    showToast('Live service not found.', 'danger');
    return;
  }
  const body = $('lf-body');
  if (!$('live-feature-modal') || !body) {
    showToast('Live service modal is not available on this page.', 'danger');
    return;
  }
  $('lf-title').textContent = f.title;
  body.innerHTML = `
    <div class="alert a-info">${escapeHtml(f.desc)}</div>
    <div class="feature-form-grid">
      ${(f.forms || []).map((field, i) => {
        const type = field[0], label = field[1], val = field[2] || '', fid = `lf-${f.id}-${i}`;
        if (type === 'select') {
          return `<div class="fg"><label class="fl">${escapeHtml(label)}</label><select class="fs live-input" id="${fid}" data-label="${escapeHtml(label)}">${val.split('|').map(o => `<option>${escapeHtml(o)}</option>`).join('')}</select></div>`;
        }
        if (type === 'textarea') {
          return `<div class="fg" style="grid-column:1/-1"><label class="fl">${escapeHtml(label)}</label><textarea class="fi live-input" id="${fid}" data-label="${escapeHtml(label)}" rows="3">${escapeHtml(val)}</textarea></div>`;
        }
        return `<div class="fg"><label class="fl">${escapeHtml(label)}</label><input class="fi live-input" id="${fid}" data-label="${escapeHtml(label)}" value="${escapeHtml(val)}"></div>`;
      }).join('')}
    </div>
    <div style="display:flex;gap:8px;margin-top:12px;flex-wrap:wrap">
      <button class="btn-p" onclick="runLiveFeature('${f.id}',true)">Generate Live Result</button>
      <button class="btn-w" onclick="showToast('${escapeHtml(f.title)} saved to dashboard.')">Save to Dashboard</button>
      <button class="btn-o" onclick="closeModal('live-feature-modal')">Close</button>
    </div>
    <div id="lf-output" class="feature-output" style="display:none"></div>`;
  openModal('live-feature-modal');
}

async function runLiveFeature(id, fromModal){
  await ensureLiveServicesLoaded();
  const f = liveServiceById(id);
  if (!f) {
    showToast('Live service not found.', 'danger');
    return;
  }
  const inputs = fromModal ? getLiveInputs() : defaultInputsForService(f);
  try {
    const data = await api('/api/live-services/run', { method: 'POST', body: { serviceId: id, inputs } });
    window.liveServiceActivity = data.activity || window.liveServiceActivity || [];
    if (id === 'accessibility' && inputs['UI Mode'] === 'High contrast') {
      document.documentElement.classList.add('accessible-mode');
    }
    const consoleEl = $('service-console');
    if (consoleEl) {
      consoleEl.textContent = `[${new Date().toLocaleTimeString('en-IN')}] ${data.runId} ${data.entityId || ''} ${f.title}\n` +
        `${data.result.headline}: ${data.result.message}\n\n` +
        `Status: ${data.result.status}\nDomain: ${data.domain}\nActor: ${data.result.actor}`;
    }
    await refreshBackendOperations();
    const output = $('lf-output');
    if (fromModal && output) {
      output.style.display = 'block';
      output.innerHTML = `<div style="display:flex;gap:6px;flex-wrap:wrap;margin-bottom:8px"><span class="badge b-green">${escapeHtml(data.runId)}</span><span class="badge b-blue">${escapeHtml(data.entityId || '')}</span><span class="badge b-blue">${escapeHtml(data.result.status)}</span><span class="badge b-gray">Backend persisted</span><span class="badge b-gray">${escapeHtml(data.domain || '')}</span></div>${data.html}`;
    }
    showToast(data.message || (f.title + ' completed.'));
  } catch (err) {
    showToast(err.message, 'danger');
  }
}

function ensureFeatureModal(){
  if ($('feature-modal')) return;
  const wrap = document.createElement('div');
  wrap.className = 'overlay';
  wrap.id = 'feature-modal';
  wrap.onclick = function(event){ if (event.target === this) closeModal('feature-modal'); };
  wrap.innerHTML = `
    <div class="modal" style="width:760px;max-width:96vw">
      <div class="modal-hd">
        <h3 id="feature-title">Portal Module</h3>
        <button class="mclose" onclick="closeModal('feature-modal')">&times;</button>
      </div>
      <div class="modal-bd" id="feature-body"></div>
    </div>`;
  document.body.appendChild(wrap);
}

function renderModuleData(data){
  const stats = (data.stats || []).map(item => `
    <div style="background:var(--stripe);border:1px solid var(--border);border-radius:4px;padding:10px 12px">
      <div style="font-size:1.2rem;font-weight:800;color:var(--navy)">${escapeHtml(item.value)}</div>
      <div style="font-size:11px;color:var(--muted)">${escapeHtml(item.label)}</div>
    </div>`).join('');
  const rows = (data.rows || []).map(row => `<tr>${row.map(cell => `<td>${escapeHtml(cell)}</td>`).join('')}</tr>`).join('');
  return `
    <div class="alert a-info">${escapeHtml(data.summary || 'Backend module loaded.')}</div>
    ${stats ? `<div style="display:grid;grid-template-columns:repeat(${Math.min((data.stats || []).length, 4)},1fr);gap:10px;margin-bottom:14px">${stats}</div>` : ''}
    <table class="tbl">
      <thead><tr>${(data.columns || []).map(col => `<th>${escapeHtml(col)}</th>`).join('')}</tr></thead>
      <tbody>${rows}</tbody>
    </table>`;
}

async function openModule(context, name){
  ensureFeatureModal();
  try {
    const data = await api(`/api/module?context=${encodeURIComponent(context)}&name=${encodeURIComponent(name)}`);
    $('feature-title').textContent = data.title || name;
    $('feature-body').innerHTML = renderModuleData(data);
    openModal('feature-modal');
  } catch (err) {
    showToast(err.message, 'danger');
  }
}

function normalizeMenuLabel(el){
  const clone = el.cloneNode(true);
  clone.querySelectorAll('.dbadge2').forEach(node => node.remove());
  return (clone.textContent || '').replace(/\s+/g, ' ').trim();
}

function wireSidebarLinks(){
  const contextMap = {
    'worker-page': 'worker',
    'employer-page': 'employer',
    'verifier-page': 'verifier',
    'superadmin-page': 'superadmin',
  };
  Object.entries(contextMap).forEach(([pageId, context]) => {
    const page = $(pageId);
    if (!page) return;
    Array.from(page.querySelectorAll('.dlink')).forEach(link => {
      if (link.getAttribute('onclick')) return;
      const label = normalizeMenuLabel(link);
      if (!label || label.toLowerCase().includes('dashboard') || label.toLowerCase().includes('overview') || label.toLowerCase().includes('admin dashboard')) return;
      link.onclick = () => openModule(context, label);
    });
  });
}

function buildSteps(){
  const ws = [
    ['Register','Via App, WhatsApp, IVR, or Field Kiosk'],
    ['Get Worker ID','Unique QR-linked identity card issued'],
    ['Receive Job Alerts','Matched by skill, distance and availability'],
    ['Accept and Check In','One-tap acceptance and QR check-in'],
    ['Get Paid','Same-day digital payment to linked account'],
  ];
  const es = [
    ['Post Requirement','Single, recurring, or bulk hiring'],
    ['Receive Matches','Verified, scored and ranked workers'],
    ['Confirm Slots','Review profiles and approve workers'],
    ['Workforce Arrives','Verified, on-time, quality workforce'],
    ['Pay and Rate','Bulk payroll and worker feedback'],
  ];
  function render(data, id, col){
    const el = $(id);
    if(!el) return;
    el.innerHTML = data.map(([t,d],i) => `
      <div style="display:flex;gap:10px;margin-bottom:10px;align-items:flex-start">
        <div style="width:22px;height:22px;border-radius:50%;background:${col};color:#fff;display:flex;align-items:center;justify-content:center;font-size:10.5px;font-weight:700;flex-shrink:0">${i+1}</div>
        <div><div style="font-size:12px;font-weight:600;color:var(--navy)">${t}</div><div style="font-size:11px;color:var(--muted)">${d}</div></div>
      </div>`).join('');
  }
  render(ws,'worker-steps','var(--blue)');
  render(es,'emp-steps','var(--green)');
}

function animateCounters(){
  document.querySelectorAll('.hstat-val[data-count]').forEach(el => {
    const target = parseInt(el.getAttribute('data-count'));
    let cur = 0;
    const step = Math.ceil(target / 60);
    const timer = setInterval(() => {
      cur = Math.min(cur + step, target);
      el.textContent = cur.toLocaleString('en-IN');
      if(cur >= target) clearInterval(timer);
    }, 16);
  });
}

function changeFontSize(dir){
  const map = {'-1':11, '0':13, '1':15.5};
  document.documentElement.style.fontSize = (map[dir] || 13) + 'px';
}

function wireButtons(){
  const availableJobButtons = cardByHeading('Available Jobs Near You')?.querySelectorAll('button') || [];
  availableJobButtons.forEach((btn, index) => btn.onclick = () => applyAvailableJob(index));

  const certBtn = Array.from(document.querySelectorAll('button')).find(btn => btn.textContent.trim() === 'Download' && btn.closest('.card')?.textContent.includes('Construction Safety'));
  if (certBtn) certBtn.onclick = () => genericAction('download_certificate');

  const printBtn = Array.from(document.querySelectorAll('button')).find(btn => btn.textContent.trim() === 'Print Card');
  if (printBtn) printBtn.onclick = () => genericAction('print_id_card');

  const pdfBtn = Array.from(document.querySelectorAll('#id-page button')).find(btn => btn.textContent.includes('Download PDF'));
  if (pdfBtn) pdfBtn.onclick = () => genericAction('download_id_pdf');

  const verifyScanBtn = Array.from(document.querySelectorAll('#verify-page button')).find(btn => btn.textContent.includes('Scan QR Code'));
  if (verifyScanBtn) verifyScanBtn.onclick = () => genericAction('scan_public_qr');

  const fieldKycCard = cardByHeading('Field KYC');
  if (fieldKycCard) {
    const btns = fieldKycCard.querySelectorAll('button');
    if (btns[0]) btns[0].onclick = submitFieldKyc;
    if (btns[1]) btns[1].onclick = () => genericAction('scan_field_qr');
  }

  const bulkBtn = Array.from(cardByHeading('Bulk Hiring Request')?.querySelectorAll('button') || [])[0];
  if (bulkBtn) bulkBtn.onclick = submitBulkHire;

  const jobBtn = Array.from(cardByHeading('Post a Single Job')?.querySelectorAll('button') || [])[0];
  if (jobBtn) jobBtn.onclick = submitSingleJob;

  const hireCard = cardByHeading('Top Verified Workers');
  if (hireCard) {
    Array.from(hireCard.querySelectorAll('tbody tr')).forEach(row => {
      const name = row.querySelector('td div')?.textContent?.trim();
      const btn = row.querySelector('button');
      if (btn && name) btn.onclick = () => hireRecommendedWorker(name);
    });
  }

  const verifierCard = cardByHeading('Create New Verifier Account');
  if (verifierCard) {
    const btn = verifierCard.querySelector('button');
    if (btn) btn.onclick = createVerifierAccount;
  }

  const noticeCard = cardByHeading('Broadcast Notice');
  if (noticeCard) {
    const btn = noticeCard.querySelector('button');
    if (btn) btn.onclick = publishNotice;
  }

  const actionMap = [
    ['Android APK', 'download_android_app'],
    ['iOS App Store', 'open_ios_listing'],
    ['Continue', 'continue_course'],
    ['Start', 'start_course'],
  ];
  actionMap.forEach(([label, actionKey]) => {
    Array.from(document.querySelectorAll('button')).filter(btn => btn.textContent.trim() === label).forEach(btn => {
      btn.onclick = () => genericAction(actionKey);
    });
  });

  Array.from(document.querySelectorAll('a[onclick*="Bulk hiring portal loading"]')).forEach(a => a.onclick = () => genericAction('bulk_portal'));
  Array.from(document.querySelectorAll('a[onclick*="Grievance portal loading"]')).forEach(a => a.onclick = () => genericAction('grievance_portal'));
  Array.from(document.querySelectorAll('a[onclick*="Help section coming soon"]')).forEach(a => a.onclick = () => genericAction('help_portal'));
  Array.from(document.querySelectorAll('a[onclick*="Payment status portal loading"]')).forEach(a => a.onclick = () => genericAction('payment_status'));
  Array.from(document.querySelectorAll('a[onclick*="Upskilling portal loading"]')).forEach(a => a.onclick = () => genericAction('upskilling_portal'));
}

function tick(){
  const n = new Date();
  if ($('clk')) $('clk').textContent = n.toLocaleTimeString('en-IN',{hour:'2-digit',minute:'2-digit',second:'2-digit',hour12:true});
  if ($('clkd')) $('clkd').textContent = n.toLocaleDateString('en-IN',{weekday:'short',day:'2-digit',month:'short',year:'numeric'}) + ' IST';
  setTimeout(tick, 1000);
}

document.addEventListener('DOMContentLoaded', async () => {
  tick();
  toggleRegFields();
  updateCard();
  buildSteps();
  animateCounters();
  wireButtons();
  wireSidebarLinks();
  await loadLiveServices();
  await restoreSession();
});
"""


def build_portal():
    html = PORTAL_HTML.read_text(encoding="utf-8", errors="replace")
    start = html.rfind("<script>")
    end = html.rfind("</script>")
    if start != -1 and end != -1 and end > start:
        html = html[:start] + f"<script>{APP_SCRIPT}</script>" + html[end + len("</script>"):]
    return html.encode("utf-8", errors="replace")


class PortalHandler(BaseHTTPRequestHandler):
    server_version = "IEEPortal/1.0"

    def _cookies(self):
        raw = self.headers.get("Cookie", "")
        jar = SimpleCookie()
        jar.load(raw)
        return jar

    def _session_user(self, state):
        token = self._cookies().get(SESSION_COOKIE)
        if not token:
            return None, None
        session = state["sessions"].get(token.value)
        if not session:
            return None, token.value
        user = find_user(state, session["role"], session["login_id"])
        return user, token.value

    def _client_ip(self):
        forwarded = self.headers.get("X-Forwarded-For", "")
        if forwarded:
            return forwarded.split(",")[0].strip()
        return self.client_address[0] if self.client_address else "127.0.0.1"

    def _require_role_json(self, user, role):
        if not user:
            self._send_json({"ok": False, "message": "Please sign in to continue."}, HTTPStatus.UNAUTHORIZED)
            return False
        if user.get("role") != role:
            self._send_json({"ok": False, "message": f"{role.title()} access is required for this action."}, HTTPStatus.FORBIDDEN)
            return False
        return True

    def _read_json(self):
        length = int(self.headers.get("Content-Length", "0"))
        if length <= 0:
            return {}
        raw = self.rfile.read(length).decode("utf-8")
        return json.loads(raw) if raw else {}

    def _send_json(self, payload, status=HTTPStatus.OK, cookie_header=None):
        body = json.dumps(payload).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        if cookie_header:
            self.send_header("Set-Cookie", cookie_header)
        self.end_headers()
        self.wfile.write(body)

    def _send_html(self, body):
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def _send_no_content(self):
        self.send_response(HTTPStatus.NO_CONTENT)
        self.send_header("Cache-Control", "public, max-age=86400")
        self.end_headers()

    def do_GET(self):
        parsed = urlparse(self.path)
        state = read_state()

        if parsed.path == "/":
            self._send_html(build_portal())
            return

        if parsed.path == "/favicon.ico":
            self._send_no_content()
            return

        if parsed.path == "/superadmin/advanced":
            user, _ = self._session_user(state)
            if not user or user.get("role") != "superadmin":
                self._send_html(build_advanced_gate_page())
                return
            self._send_html(build_advanced_admin_page())
            return

        if parsed.path == "/api/session":
            user, _ = self._session_user(state)
            self._send_json({"ok": True, "user": user_payload(user) if user else None})
            return

        if parsed.path == "/api/live-services":
            self._send_json(live_services_payload(state))
            return

        if parsed.path == "/api/health":
            services = ensure_live_services_state(state)
            self._send_json({
                "ok": True,
                "status": "healthy",
                "service": "IEE Portal Backend",
                "time": datetime.now().isoformat(timespec="seconds"),
                "checks": {
                    "portalHtml": PORTAL_HTML.exists(),
                    "jsonStore": DB_PATH.exists(),
                    "liveCatalog": len(LIVE_SERVICE_CATALOG),
                    "liveRuns": services["stats"].get("total_runs", 0),
                    "domainRecords": sum(len(rows) for rows in services.get("domains", {}).values()),
                },
            })
            return

        if parsed.path == "/api/live-services/activity":
            params = parse_qs(parsed.query)
            domain = params.get("domain", [""])[0]
            limit = min(_int(params.get("limit", ["25"])[0], 25), 100)
            services = ensure_live_services_state(state)
            if domain:
                rows = services.get("domains", {}).get(domain)
                if rows is None:
                    self._send_json({"ok": False, "message": "Live service domain not found."}, HTTPStatus.NOT_FOUND)
                    return
                self._send_json({"ok": True, "domain": domain, "records": rows[:limit]})
                return
            self._send_json({"ok": True, "activity": services["records"][:limit], "domainCounts": {k: len(v) for k, v in services.get("domains", {}).items()}})
            return

        if parsed.path == "/api/admin/advanced/dashboard":
            user, _ = self._session_user(state)
            if not self._require_role_json(user, "superadmin"):
                return
            self._send_json(advanced_dashboard_payload(state, user))
            return

        if parsed.path == "/api/workers/verify":
            identifier = parse_qs(parsed.query).get("id", [""])[0]
            worker = find_worker(state, identifier)
            if not worker:
                self._send_json({"ok": False, "message": "Worker not found in the registry."}, HTTPStatus.NOT_FOUND)
                return
            self._send_json({
                "ok": True,
                "worker": {
                    "name": worker["name"],
                    "ieeId": worker["iee_id"],
                    "role": worker["occupation"],
                    "city": worker["city"],
                    "rating": worker["rating"],
                    "jobsCompleted": worker["jobs_completed"],
                    "status": worker["status"],
                }
            })
            return

        if parsed.path == "/api/module":
            params = parse_qs(parsed.query)
            user, _ = self._session_user(state)
            context = params.get("context", [""])[0]
            name = params.get("name", [""])[0]
            self._send_json({"ok": True, **module_payload(state, context, name, user)})
            return

        self._send_json({"ok": False, "message": "Not found."}, HTTPStatus.NOT_FOUND)

    def do_POST(self):
        parsed = urlparse(self.path)
        state = read_state()
        data = self._read_json()
        current_user, token = self._session_user(state)

        if parsed.path == "/api/login":
            role = data.get("role", "")
            identifier = data.get("identifier", "")
            password = data.get("password", "")
            user = find_user(state, role, identifier)
            if not user or user.get("password") != password:
                self._send_json({"ok": False, "message": "Invalid credentials. Please check your ID and password."}, HTTPStatus.UNAUTHORIZED)
                return
            if user.get("status") == "Banned":
                self._send_json({"ok": False, "message": "This account is banned and cannot sign in."}, HTTPStatus.FORBIDDEN)
                return
            session_token = new_session(state, user)
            audit(state, user["login_id"], "LOGIN", "OK")
            write_state(state)
            self._send_json({"ok": True, "message": f"Login successful. Welcome, {user['name']}.", "user": user_payload(user)}, cookie_header=f"{SESSION_COOKIE}={session_token}; Path=/; HttpOnly; SameSite=Lax")
            return

        if parsed.path == "/api/admin/login":
            user = find_user(state, "superadmin", data.get("identifier", ""))
            if not user or user.get("password") != data.get("password", ""):
                self._send_json({"ok": False, "message": "Invalid administrator credentials. Access denied."}, HTTPStatus.UNAUTHORIZED)
                return
            session_token = new_session(state, user)
            audit(state, "superadmin", "SUPERADMIN_LOGIN", "OK")
            write_state(state)
            self._send_json({"ok": True, "message": "Super Admin access granted. All actions monitored.", "user": user_payload(user)}, cookie_header=f"{SESSION_COOKIE}={session_token}; Path=/; HttpOnly; SameSite=Lax")
            return

        if parsed.path == "/api/logout":
            if token and token in state["sessions"]:
                state["sessions"].pop(token, None)
                write_state(state)
            self._send_json({"ok": True}, cookie_header=f"{SESSION_COOKIE}=deleted; Path=/; Expires={formatdate(0, usegmt=True)}; HttpOnly; SameSite=Lax")
            return

        if parsed.path == "/api/register":
            account_type = data.get("accountType", "worker")
            name = (data.get("name") or "").strip()
            mobile = (data.get("mobile") or "").strip()
            password = (data.get("password") or "").strip()
            city = (data.get("city") or "").strip()
            if not name or not mobile or not password or not city:
                self._send_json({"ok": False, "message": "Please fill all required registration details."}, HTTPStatus.BAD_REQUEST)
                return
            for user in state["users"]:
                if mobile and user.get("mobile") == mobile:
                    self._send_json({"ok": False, "message": "A user with this mobile number already exists."}, HTTPStatus.CONFLICT)
                    return
                if data.get("email") and user.get("email", "").lower() == data.get("email", "").lower():
                    self._send_json({"ok": False, "message": "A user with this email already exists."}, HTTPStatus.CONFLICT)
                    return

            row_id = f"ur-{len([u for u in state['users'] if u['role'] != 'superadmin']) + 1}"
            if account_type == "worker":
                seq = state["meta"]["next_worker_seq"]
                state["meta"]["next_worker_seq"] += 1
                iee_id = f"IEE-WK-2026-{seq:08d}"
                user = {
                    "row_id": row_id,
                    "role": "worker",
                    "status": "KYC Pending",
                    "name": name,
                    "mobile": mobile,
                    "email": data.get("email", ""),
                    "password": password,
                    "login_id": mobile,
                    "iee_id": iee_id,
                    "occupation": data.get("occupation") or "General Labour",
                    "city": city,
                    "rating": "New",
                    "jobs_completed": 0,
                    "registered": today_label(),
                }
                state["workers"].append({
                    "name": name,
                    "iee_id": iee_id,
                    "mobile": mobile,
                    "occupation": user["occupation"],
                    "city": city,
                    "rating": "New",
                    "jobs_completed": 0,
                    "status": "KYC Pending",
                    "skills": [data.get("skill") or user["occupation"]],
                })
                msg = f"Registration submitted. Your Worker ID {iee_id} is pending verification."
                login_id = mobile
            else:
                seq = state["meta"]["next_employer_seq"]
                state["meta"]["next_employer_seq"] += 1
                employer_id = f"EMP-TN-2026-{seq:06d}"
                user = {
                    "row_id": row_id,
                    "role": "employer",
                    "status": "KYC Pending",
                    "name": data.get("companyName") or name,
                    "mobile": mobile,
                    "email": data.get("email", ""),
                    "password": password,
                    "login_id": data.get("email") or mobile,
                    "employer_id": employer_id,
                    "sector": data.get("sector") or "Other",
                    "city": city,
                    "registered": today_label(),
                }
                msg = f"Registration submitted. Employer profile {employer_id} has been created for review."
                login_id = user["login_id"]
            state["users"].append(user)
            audit(state, login_id, "REGISTER", "Pending")
            write_state(state)
            self._send_json({"ok": True, "message": msg, "loginId": login_id})
            return

        if parsed.path == "/api/worker-id/generate":
            name = (data.get("name") or "").strip()
            if not name:
                self._send_json({"ok": False, "message": "Enter worker details before generating an ID card."}, HTTPStatus.BAD_REQUEST)
                return
            seq = state["meta"]["next_worker_seq"]
            state["meta"]["next_worker_seq"] += 1
            iee_id = f"IEE-WK-2026-{seq:08d}"
            state["workers"].append({
                "name": name,
                "iee_id": iee_id,
                "mobile": "",
                "occupation": data.get("role") or "General Labour",
                "city": data.get("location") or "Tamil Nadu",
                "rating": "4.2/5",
                "jobs_completed": 0,
                "status": "Verified",
                "skills": [data.get("skill1") or "Skill 1", data.get("skill2") or "Skill 2"],
            })
            audit(state, current_user["login_id"] if current_user else "public", "GENERATE_WORKER_ID", "OK")
            write_state(state)
            self._send_json({"ok": True, "message": f"Worker ID Generated: {iee_id}", "worker": {"ieeId": iee_id}})
            return

        if parsed.path == "/api/verifier/action":
            row_id = data.get("rowId", "")
            action = data.get("action", "")
            for item in state["verification_queue"]:
                if item["queue_id"] == row_id:
                    item["status"] = action
                    audit(state, current_user["login_id"] if current_user else "verifier", f"VERIFY_{action.upper()}", "OK")
                    write_state(state)
                    self._send_json({"ok": True, "message": f"{item['name']}: {action} successfully."})
                    return
            self._send_json({"ok": False, "message": "Verification record not found."}, HTTPStatus.NOT_FOUND)
            return

        if parsed.path == "/api/admin/user-action":
            row_id = data.get("rowId", "")
            action = data.get("action", "")
            status_map = {"Activated": "Active", "Suspended": "Suspended", "Banned": "Banned"}
            for user in state["users"]:
                if user.get("row_id") == row_id:
                    user["status"] = status_map.get(action, user["status"])
                    audit(state, current_user["login_id"] if current_user else "superadmin", f"USER_{action.upper()}", "OK")
                    write_state(state)
                    self._send_json({"ok": True, "message": f"User {action.lower()} successfully."})
                    return
            self._send_json({"ok": False, "message": "User not found."}, HTTPStatus.NOT_FOUND)
            return

        if parsed.path == "/api/employer/bulk-hire":
            count = int(data.get("workersRequired") or 0)
            if count <= 0 or not data.get("location") or not data.get("wage"):
                self._send_json({"ok": False, "message": "Enter the required count, site location, and wage for bulk hiring."}, HTTPStatus.BAD_REQUEST)
                return
            req_id = f"bulk-{state['meta']['next_bulk_seq']}"
            state["meta"]["next_bulk_seq"] += 1
            state["bulk_requests"].append({
                "request_id": req_id,
                "category": data.get("category"),
                "workers_required": count,
                "location": data.get("location"),
                "wage": data.get("wage"),
                "duration": data.get("duration"),
                "skill_level": data.get("skillLevel"),
            })
            audit(state, current_user["login_id"] if current_user else "employer", "BULK_HIRE_REQ", "Pending")
            write_state(state)
            self._send_json({"ok": True, "message": f"Bulk request submitted. Matching {count} verified workers now..."})
            return

        if parsed.path == "/api/employer/post-job":
            if not data.get("title") or not data.get("wage") or not data.get("address"):
                self._send_json({"ok": False, "message": "Enter the job title, wage, and site address before posting."}, HTTPStatus.BAD_REQUEST)
                return
            job_id = f"job-{state['meta']['next_job_seq']}"
            state["meta"]["next_job_seq"] += 1
            state["jobs"].append({
                "job_id": job_id,
                "title": data.get("title"),
                "employer": current_user["name"] if current_user else "Employer",
                "distance": "New listing",
                "wage": int(data.get("wage")),
                "type": data.get("duration") or "Open",
                "applicants": [],
            })
            audit(state, current_user["login_id"] if current_user else "employer", "POST_JOB", "OK")
            write_state(state)
            self._send_json({"ok": True, "message": "Job posted. Workers are being matched and notified."})
            return

        if parsed.path == "/api/employer/hire":
            name = data.get("name", "")
            worker = find_worker(state, name)
            if not worker:
                self._send_json({"ok": False, "message": "Worker profile not found for hiring."}, HTTPStatus.NOT_FOUND)
                return
            audit(state, current_user["login_id"] if current_user else "employer", "DIRECT_HIRE", "OK")
            write_state(state)
            self._send_json({"ok": True, "message": f"{worker['name']} hired. Confirmation sent."})
            return

        if parsed.path == "/api/worker/apply":
            index = int(data.get("jobIndex", -1))
            if current_user and current_user.get("role") != "worker":
                self._send_json({"ok": False, "message": "Only worker accounts can apply for jobs."}, HTTPStatus.FORBIDDEN)
                return
            if index < 0 or index >= len(state["jobs"]):
                self._send_json({"ok": False, "message": "Job not found."}, HTTPStatus.NOT_FOUND)
                return
            applicant = current_user["name"] if current_user else "Guest Worker"
            state["jobs"][index]["applicants"].append(applicant)
            audit(state, current_user["login_id"] if current_user else "worker", "APPLY_JOB", "OK")
            write_state(state)
            self._send_json({"ok": True, "message": f"Application submitted for {state['jobs'][index]['title']}."})
            return

        if parsed.path == "/api/verifier/field-kyc":
            lookup = (data.get("workerLookup") or "").strip()
            if not lookup:
                self._send_json({"ok": False, "message": "Enter the worker IEE ID or mobile number first."}, HTTPStatus.BAD_REQUEST)
                return
            worker = find_worker(state, lookup)
            if worker:
                worker["status"] = "KYC Submitted"
            audit(state, current_user["login_id"] if current_user else "verifier", "FIELD_KYC", "Pending")
            write_state(state)
            self._send_json({"ok": True, "message": "Field KYC submitted for processing."})
            return

        if parsed.path == "/api/admin/create-verifier":
            name = (data.get("name") or "").strip()
            email = (data.get("email") or "").strip()
            if not name or not email:
                self._send_json({"ok": False, "message": "Enter the verifier name and email before creating the account."}, HTTPStatus.BAD_REQUEST)
                return
            seq = state["meta"]["next_verifier_seq"]
            state["meta"]["next_verifier_seq"] += 1
            verifier_id = f"IEE-VRF-2026-{seq:03d}"
            row_id = f"ur-{len([u for u in state['users'] if u['role'] != 'superadmin']) + 1}"
            state["users"].append({
                "row_id": row_id,
                "role": "verifier",
                "status": "Active",
                "name": name,
                "mobile": data.get("mobile", ""),
                "email": email,
                "password": data.get("password") or "Verify@001",
                "login_id": email,
                "verifier_id": verifier_id,
                "zone": data.get("zone") or "Zone Assignment Pending",
                "registered": today_label(),
            })
            audit(state, current_user["login_id"] if current_user else "superadmin", "CREATE_VERIFIER", "OK")
            write_state(state)
            self._send_json({"ok": True, "message": f"Verifier account created. Credentials sent to {email}."})
            return

        if parsed.path == "/api/admin/publish-notice":
            if not data.get("title") or not data.get("content"):
                self._send_json({"ok": False, "message": "Enter both a notice title and notice content."}, HTTPStatus.BAD_REQUEST)
                return
            state["notices"].insert(0, {
                "notice_id": f"notice-{state['meta']['next_notice_seq']}",
                "title": data.get("title"),
                "category": data.get("category"),
                "priority": data.get("priority"),
                "content": data.get("content"),
                "published": today_label(),
            })
            state["meta"]["next_notice_seq"] += 1
            audit(state, current_user["login_id"] if current_user else "superadmin", "PUBLISH_NOTICE", "OK")
            write_state(state)
            self._send_json({"ok": True, "message": "Notice published and visible to all users."})
            return

        if parsed.path == "/api/live-services/run":
            service_id = data.get("serviceId", "")
            service = service_by_id(service_id)
            if not service:
                self._send_json({"ok": False, "message": "Live service not found."}, HTTPStatus.NOT_FOUND)
                return
            inputs = data.get("inputs") or {}
            services = ensure_live_services_state(state)
            result = live_service_result(service_id, inputs, current_user)
            domain, entity = live_service_entity(state, service_id, inputs, result)
            run_id = f"LS-{state['meta']['next_live_service_seq']:06d}"
            state["meta"]["next_live_service_seq"] += 1
            entity["runId"] = run_id
            services["domains"].setdefault(domain, []).insert(0, entity)
            del services["domains"][domain][60:]
            record = {
                "runId": run_id,
                "entityId": entity["entityId"],
                "serviceId": service_id,
                "title": service["title"],
                "domain": domain,
                "category": service["cat"],
                "status": result["status"],
                "actor": current_user["login_id"] if current_user else "public",
                "time": now_time(),
                "date": today_label(),
                "inputs": inputs,
                "result": result,
            }
            services["records"].insert(0, record)
            del services["records"][80:]
            services["stats"]["total_runs"] += 1
            services["stats"]["automations_completed"] += 1
            if service["cat"] == "compliance":
                services["stats"]["compliance_documents"] += 1
            if service["cat"] == "worker":
                services["stats"]["worker_welfare_actions"] += 1
            audit(state, current_user["login_id"] if current_user else "public", f"LIVE_SERVICE_{service_id.upper()}", result["status"], self._client_ip())
            write_state(state)
            self._send_json({
                "ok": True,
                "message": f"{service['title']} completed.",
                "runId": run_id,
                "entityId": entity["entityId"],
                "domain": domain,
                "service": service,
                "result": result,
                "entity": entity,
                "html": result_to_html(result),
                "activity": services["records"][:12],
                "domainCounts": {k: len(v) for k, v in services.get("domains", {}).items()},
                "stats": services["stats"],
            })
            return

        if parsed.path == "/api/admin/advanced/register-worker":
            if not self._require_role_json(current_user, "superadmin"):
                return
            name = (data.get("name") or "").strip()
            mobile = (data.get("mobile") or "").strip()
            city = (data.get("city") or "").strip()
            role = (data.get("role") or "").strip()
            if not name or not mobile or not city or not role:
                self._send_json({"ok": False, "message": "Enter the worker name, mobile, role, and city before issuing an IEE record."}, HTTPStatus.BAD_REQUEST)
                return
            if any(user.get("mobile") == mobile for user in state["users"]):
                self._send_json({"ok": False, "message": "A worker with this mobile number already exists."}, HTTPStatus.CONFLICT)
                return

            seq = state["meta"]["next_worker_seq"]
            state["meta"]["next_worker_seq"] += 1
            worker_id = f"IEE-WK-2026-{seq:08d}"
            row_id = f"ur-{len([u for u in state['users'] if u['role'] != 'superadmin']) + 1}"
            level_label = (data.get("level") or "L1 — Unskilled").split("—")[0].strip()
            password = data.get("password") or "Worker@Temp1"

            user = {
                "row_id": row_id,
                "role": "worker",
                "status": "KYC Pending",
                "name": name,
                "mobile": mobile,
                "email": "",
                "password": password,
                "login_id": mobile,
                "iee_id": worker_id,
                "occupation": role,
                "city": city,
                "rating": "New",
                "jobs_completed": 0,
                "registered": today_label(),
            }
            state["users"].append(user)
            state["workers"].append({
                "name": name,
                "iee_id": worker_id,
                "mobile": mobile,
                "occupation": role,
                "city": city,
                "rating": "New",
                "jobs_completed": 0,
                "status": "KYC Pending",
                "skills": [role],
            })

            adv = advanced_state(state)
            adv["metrics"]["total_workers"] += 1
            adv["metrics"]["kyc_pending"] += 1
            worker_row = find_advanced_worker(state, worker_id)
            if worker_row:
                worker_row.update({
                    "level": f"{level_label} Skilled" if "L3" in level_label else f"{level_label} Semi-Skilled" if "L2" in level_label else f"{level_label} Unskilled",
                    "city": city.split(",")[0],
                    "status": "KYC Pending",
                    "risk_score": 26,
                    "aadhaar_last4": (data.get("aadhaarLast4") or "").strip(),
                    "bank_account": (data.get("bankAccount") or "").strip(),
                    "eshram_uan": (data.get("eshramUan") or "").strip(),
                    "flags": ["KYC Pending"],
                })
            journey = adv["journeys"].get(worker_id)
            if journey:
                journey.update({
                    "name": name,
                    "avatar": "".join(part[:1] for part in name.split()[:2]).upper() or "WK",
                    "role": role,
                    "level": worker_row.get("level", level_label) if worker_row else level_label,
                    "city": city,
                    "eshram_uan": (data.get("eshramUan") or "").strip(),
                    "aadhaar_last4": (data.get("aadhaarLast4") or "").strip(),
                    "bank_account": (data.get("bankAccount") or "").strip(),
                    "risk_score": 26,
                    "risk_label": "Medium",
                    "flags": ["KYC Pending"],
                    "timeline": [
                        {
                            "tone": "acc",
                            "step": "1",
                            "title": "Worker Added from Advanced Admin Console",
                            "description": "A new worker record was created in the live superadmin console. Field verification is still pending.",
                            "meta": [today_label(), f"Registered by {current_user['name']}", city],
                            "tags": ["KYC Pending"],
                        }
                    ],
                })

            prepend_advanced_alert(state, f"New Worker Registered — {name}", f"{worker_id} created from superintendent admin console. Verification pending.", "Just now")
            prepend_advanced_feed(state, "g", f"<strong>{name}</strong> added to IEE registry — {role} — {city} — verification pending", "Just now — Superadmin")
            audit(state, current_user["login_id"], "ADV_REGISTER_WORKER", "OK", self._client_ip())
            write_state(state)
            self._send_json({
                "ok": True,
                "message": f"Worker registered — {worker_id} — KYC pending.",
                "worker": {"workerId": worker_id, "name": name},
            })
            return

        if parsed.path == "/api/admin/advanced/register-employer":
            if not self._require_role_json(current_user, "superadmin"):
                return
            company = (data.get("company") or "").strip()
            city = (data.get("city") or "").strip()
            sector = (data.get("sector") or "").strip()
            if not company or not city:
                self._send_json({"ok": False, "message": "Enter the employer company name and city before registering."}, HTTPStatus.BAD_REQUEST)
                return

            seq = state["meta"]["next_employer_seq"]
            state["meta"]["next_employer_seq"] += 1
            employer_id = f"EMP-TN-2026-{seq:06d}"
            row_id = f"ur-{len([u for u in state['users'] if u['role'] != 'superadmin']) + 1}"
            email_stub = company.lower().replace(" ", "")[:18]
            login_id = f"{email_stub}@iee-employer.local"
            state["users"].append({
                "row_id": row_id,
                "role": "employer",
                "status": "KYC Pending",
                "name": company,
                "mobile": (data.get("contactMobile") or "").strip(),
                "email": login_id,
                "password": data.get("password") or "Employ@Temp1",
                "login_id": login_id,
                "employer_id": employer_id,
                "sector": sector or "Other",
                "city": city,
                "registered": today_label(),
            })

            adv = advanced_state(state)
            adv["metrics"]["active_employers"] += 1
            employer_row = find_advanced_employer(state, employer_id)
            if employer_row:
                employer_row.update({
                    "company": company,
                    "gstin": (data.get("gstin") or "").strip(),
                    "epfo_code": (data.get("epfoCode") or "").strip(),
                    "esic_code": (data.get("esicCode") or "").strip(),
                    "workers": 0,
                    "contracts": 0,
                    "risk_score": 18,
                    "compliance_pct": 72.0,
                    "sector": sector or "Other",
                    "city": city,
                    "contact_person": (data.get("contactPerson") or "").strip() or company,
                    "contact_mobile": (data.get("contactMobile") or "").strip(),
                })

            prepend_advanced_alert(state, f"New Employer Onboarded — {company}", f"{employer_id} created with GST / EPFO / ESIC profile pending verification.", "Just now")
            prepend_advanced_feed(state, "b", f"<strong>{company}</strong> added to employer registry — sector {sector or 'Other'} — compliance review queued", "Just now — Superadmin")
            audit(state, current_user["login_id"], "ADV_REGISTER_EMPLOYER", "OK", self._client_ip())
            write_state(state)
            self._send_json({
                "ok": True,
                "message": f"Employer registered — {employer_id} — compliance verification pending.",
                "employer": {"employerId": employer_id, "company": company},
            })
            return

        if parsed.path == "/api/admin/advanced/register-contract":
            if not self._require_role_json(current_user, "superadmin"):
                return
            contractor = (data.get("contractor") or "").strip()
            principal = (data.get("principalEmployer") or "").strip()
            handler = (data.get("handler") or "").strip()
            if not contractor or not principal or not data.get("contractValue") or not data.get("workersRequired"):
                self._send_json({"ok": False, "message": "Enter the contract owner, value, and worker count before registering."}, HTTPStatus.BAD_REQUEST)
                return

            next_contract_seq = state["meta"].setdefault("next_contract_seq", 143)
            contract_id = f"IEE-CTR-2026-{next_contract_seq:04d}"
            state["meta"]["next_contract_seq"] += 1

            contract_value = int(data.get("contractValue") or 0)
            workers_required = int(data.get("workersRequired") or 0)
            worker_rate = int(data.get("workerRate") or 0)
            client_rate = int(data.get("clientRate") or worker_rate)

            contract = {
                "contract_id": contract_id,
                "title": f"{contractor} — {principal}",
                "principal_employer": principal,
                "contractor": contractor,
                "handler": handler or current_user["name"],
                "contract_value": contract_value,
                "workers_deployed": workers_required,
                "epfo_workers": workers_required,
                "worker_rate": worker_rate,
                "client_rate": client_rate,
                "start_date": data.get("startDate") or today_label(),
                "end_date": data.get("endDate") or "Open",
                "license_no": (data.get("licenseNo") or "").strip() or "Pending",
                "compliance_pct": 91.0,
                "rating": 4.5,
                "april_payment": int(contract_value * 0.1) if contract_value else 0,
                "ai_flags": 0,
                "risk_score": 14,
                "wage_diversion_per_day": max(client_rate - worker_rate, 0) if client_rate > worker_rate else 0,
                "estimated_misuse": 0,
                "status_label": "Live",
                "status_tone": "bg",
                "secondary_badge": "",
            }
            adv = advanced_state(state)
            adv["contracts"].insert(0, contract)
            adv["metrics"]["live_contracts"] += 1
            adv["metrics"]["contract_net_value"] += contract_value
            adv["metrics"]["workers_deployed"] += workers_required
            if worker_rate:
                adv["metrics"]["avg_daily_rate"] = int(((adv["metrics"]["avg_daily_rate"] * max(adv["metrics"]["live_contracts"] - 1, 1)) + worker_rate) / max(adv["metrics"]["live_contracts"], 1))

            prepend_advanced_alert(state, f"New Contract Registered — {contractor}", f"{contract_id} linked to {principal} with {workers_required} workers and AI monitoring activated.", "Just now")
            prepend_advanced_feed(state, "a", f"<strong>{contractor}</strong> contract registered — {workers_required} workers — AI compliance monitoring active", "Just now — Contracts")
            audit(state, current_user["login_id"], "ADV_REGISTER_CONTRACT", "OK", self._client_ip())
            write_state(state)
            self._send_json({
                "ok": True,
                "message": f"Contract {contract_id} registered — AI monitoring activated.",
                "contract": {"contractId": contract_id},
            })
            return

        if parsed.path == "/api/admin/advanced/broadcast":
            if not self._require_role_json(current_user, "superadmin"):
                return
            title = (data.get("title") or "").strip()
            message = (data.get("message") or "").strip()
            recipients = int(data.get("recipients") or 0)
            if not title or not message or recipients <= 0:
                self._send_json({"ok": False, "message": "Enter a title, message, and valid audience before broadcasting."}, HTTPStatus.BAD_REQUEST)
                return

            delivery_pct = 97.2
            history_row = {
                "title": title,
                "recipients": recipients,
                "delivery_pct": delivery_pct,
                "date": today_label(),
                "status": "Sent",
            }
            adv = advanced_state(state)
            adv["broadcast_history"].insert(0, history_row)
            del adv["broadcast_history"][12:]
            state["notices"].insert(0, {
                "notice_id": f"notice-{state['meta']['next_notice_seq']}",
                "title": title,
                "category": "Broadcast",
                "priority": "High",
                "content": message,
                "published": today_label(),
            })
            state["meta"]["next_notice_seq"] += 1
            prepend_advanced_alert(state, f"Broadcast Sent — {title}", f"Delivered to {recipients} recipients across app, SMS, WhatsApp, and assisted channels.", "Just now", unread=False)
            prepend_advanced_feed(state, "p", f"<strong>Broadcast sent:</strong> {title} — audience {recipients}", "Just now — Broadcast")
            audit(state, current_user["login_id"], "ADV_BROADCAST", "OK", self._client_ip())
            write_state(state)
            self._send_json({
                "ok": True,
                "message": f"Broadcast complete — {recipients:,} recipients queued across all active channels.",
                "broadcast": history_row,
            })
            return

        if parsed.path == "/api/admin/advanced/launch-scheme":
            if not self._require_role_json(current_user, "superadmin"):
                return
            scheme_name = (data.get("schemeName") or "").strip()
            regions = data.get("regions") or []
            if not scheme_name:
                self._send_json({"ok": False, "message": "Choose a scheme before launching it."}, HTTPStatus.BAD_REQUEST)
                return

            adv = advanced_state(state)
            adv["selected_scheme"] = scheme_name
            recipients = adv["metrics"]["verified_profiles"]
            prepend_advanced_alert(state, f"Scheme Launch Approved — {scheme_name}", f"Campaign authorised for {len(regions) or 1} region scope and {recipients} eligible workers.", "Just now")
            prepend_advanced_feed(state, "g", f"<strong>Scheme launched:</strong> {scheme_name} — {recipients} verified workers targeted", "Just now — Welfare Engine")
            audit(state, current_user["login_id"], "ADV_SCHEME_LAUNCH", "OK", self._client_ip())
            write_state(state)
            self._send_json({
                "ok": True,
                "message": f"Scheme launched — {recipients:,} eligible workers targeted.",
                "campaign": {
                    "schemeName": scheme_name,
                    "recipients": recipients,
                    "regions": regions,
                },
            })
            return

        if parsed.path == "/api/admin/advanced/process-payroll":
            if not self._require_role_json(current_user, "superadmin"):
                return
            adv = advanced_state(state)
            batch = adv["salary_batch"]
            batch["status"] = "Processed"
            batch["last_processed"] = today_label()
            prepend_advanced_alert(state, "Payroll Batch Authorised", f"{batch['batch_id']} approved for {batch['workers']} workers and DBT release initiated.", "Just now", unread=False)
            prepend_advanced_feed(state, "g", f"<strong>Payroll authorised:</strong> {batch['batch_id']} — {batch['workers']} workers — {batch['amount']:,} rupees", "Just now — Payroll")
            audit(state, current_user["login_id"], "ADV_PROCESS_PAYROLL", "OK", self._client_ip())
            write_state(state)
            self._send_json({
                "ok": True,
                "message": f"Salary complete — {batch['workers']:,} workers processed via DBT.",
                "batch": batch,
            })
            return

        if parsed.path == "/api/action":
            action_key = data.get("actionKey", "")
            messages = {
                "download_certificate": "Certificate download started.",
                "print_id_card": "Preparing print layout...",
                "download_id_pdf": "PDF download started.",
                "scan_public_qr": "QR scanner initialising...",
                "scan_field_qr": "QR scanner opening...",
                "download_android_app": "Android APK download is ready for this demo portal.",
                "open_ios_listing": "iOS App Store listing opened for review.",
                "continue_course": "Course progress resumed from your last checkpoint.",
                "start_course": "Training module started successfully.",
                "bulk_portal": "Bulk hiring portal loaded with your latest employer requests.",
                "grievance_portal": "Grievance portal opened with your current ticket history.",
                "help_portal": "Help section loaded with FAQs and support contacts.",
                "payment_status": "Payment status portal loaded with the latest settlement snapshot.",
                "upskilling_portal": "Upskilling portal loaded with recommended courses.",
            }
            audit(state, current_user["login_id"] if current_user else "public", f"ACTION_{action_key.upper()}", "OK")
            write_state(state)
            self._send_json({"ok": True, "message": messages.get(action_key, "Action completed successfully.")})
            return

        self._send_json({"ok": False, "message": "Not found."}, HTTPStatus.NOT_FOUND)


if __name__ == "__main__":
    if not PORTAL_HTML.exists():
        raise FileNotFoundError(f"Portal file not found: {PORTAL_HTML}")
    read_state()
    host = os.environ.get("HOST", "0.0.0.0")
    port = int(os.environ.get("PORT", "8000"))
    server = ThreadingHTTPServer((host, port), PortalHandler)
    print(f"IEE portal server running at http://{host}:{port}")
    server.serve_forever()
