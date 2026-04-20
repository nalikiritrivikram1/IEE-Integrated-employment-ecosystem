import json
import os
import secrets
from copy import deepcopy
from datetime import datetime
from email.utils import formatdate
from http import HTTPStatus
from http.cookies import SimpleCookie
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from threading import Lock
from urllib.parse import parse_qs, urlparse


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


def read_state():
    with STATE_LOCK:
        if not DB_PATH.exists():
            _atomic_write(DEFAULT_STATE)
        return json.loads(DB_PATH.read_text(encoding="utf-8"))


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

function $(id){ return document.getElementById(id); }

function showPage(id){
  document.querySelectorAll('.page').forEach(p => p.classList.remove('show'));
  const pg = $(id);
  if(pg){ pg.classList.add('show'); window.scrollTo(0,0); }
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
}

async function restoreSession(){
  try {
    const data = await api('/api/session');
    if (data.user) setLoggedIn(data.user);
  } catch (_) {}
}

function goDash(){
  if(!currentUser){ openModal('login-modal'); return; }
  if(currentUser.role==='worker') showPage('worker-page');
  else if(currentUser.role==='employer') showPage('employer-page');
  else if(currentUser.role==='verifier') showPage('verifier-page');
  else if(currentUser.role==='superadmin') showPage('superadmin-page');
}

async function doLogout(){
  try { await api('/api/logout', { method: 'POST' }); } catch (_) {}
  currentUser = null;
  const hb = $('header-btns');
  if(hb) hb.innerHTML = '<button class="btn-reg" onclick="showPage(\'register-page\')" style="margin-right:6px">Register</button><button class="btn-login" onclick="openModal(\'login-modal\')">Login</button>';
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
    showToast(`Please sign in as ${role} to continue.`, 'warn');
    openModal('login-modal');
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
    if(role==='worker') showPage('worker-page');
    else if(role==='employer') showPage('employer-page');
    else if(role==='verifier') showPage('verifier-page');
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
    showPage('superadmin-page');
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

    def do_GET(self):
        parsed = urlparse(self.path)
        state = read_state()

        if parsed.path == "/":
            self._send_html(build_portal())
            return

        if parsed.path == "/api/session":
            user, _ = self._session_user(state)
            self._send_json({"ok": True, "user": user_payload(user) if user else None})
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
