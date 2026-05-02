# IEE Comprehensive Audit and Implementation Roadmap

Date: 2026-04-23  
Scope: live deployment at `https://iee-integrated-employment-ecosystem.onrender.com/`, local backend in `app.py`, portal UI in `iee_government_portal.html`, and advanced superadmin prototype in `IEE_SuperAdmin_Advanced.html`

## Executive Summary

IEE is currently a functional role-based demo with real persistence for a narrow set of actions, not a production-ready employment ecosystem.

The current product already proves four important ideas:

- workers, employers, verifiers, and super admins can all enter distinct flows
- the portal can persist registrations, job posts, applications, verifier actions, notices, and sessions
- the UI theme can support multiple dashboards without redesigning the original portal shell
- the advanced superadmin prototype points to a much larger product vision around compliance, contract intelligence, worker lifecycle tracking, and finance

The main issue is that the live deployment combines demo behavior, public data exposure, and incomplete role enforcement. That makes the current system useful as a prototype and stakeholder demo, but unsafe as a real employment platform.

### Current State by Category

| Category | Assessment | Notes |
| --- | --- | --- |
| Worker flow | Partially implemented | Registration, login, worker verification, and job apply are real; most dashboard modules are static or seeded. |
| Employer flow | Partially implemented | Job posting, bulk request, and direct hire are real; lifecycle management and workforce operations are mostly demo-only. |
| Verifier flow | Partially implemented | Queue updates and field KYC submission are real; evidence capture, SLA, reassignment, and fraud escalation are missing. |
| Superadmin flow | Partially implemented but unsafe | Admin login, user actions, verifier creation, and notice publishing are real; module data is publicly accessible through `/api/module`. |
| Security and privacy | Unsafe for production | Public admin data exposure, plaintext passwords, missing RBAC, no session expiry, weak audit model. |
| Government interoperability | Prototype-only | The advanced prototype references eShram, NCS, EPFO, ESIC, GST, and PMKVY workflows, but the backend does not implement those integrations. |
| Analytics and intelligence | Prototype-only | Advanced compliance, fraud scoring, journey tracking, and contract intelligence exist in `IEE_SuperAdmin_Advanced.html` but not in `app.py`. |

### Status Legend

- `Implemented now`: live behavior backed by current server state and persisted in `portal_data.json`
- `Demo-only / static`: visible in the portal but powered by hard-coded rows, placeholders, or generic module payloads
- `Prototype-only`: present in the advanced HTML prototype but not backed by the current app
- `Missing but required`: not present, but necessary for a credible marketplace or government-grade deployment
- `Unsafe for production`: present behavior that would create security, privacy, compliance, or operational risk in a real launch

## Audit Method and Evidence Base

This audit is grounded in four evidence streams:

1. Local code review of `app.py`, `portal_data.json`, `iee_government_portal.html`, and `IEE_SuperAdmin_Advanced.html`
2. Live deployment review of `https://iee-integrated-employment-ecosystem.onrender.com/` on 2026-04-23
3. Live API verification of public endpoints on 2026-04-23
4. Benchmark review of official government and competitor sites listed in the appendix

## Confirmed Production Blockers

These issues should be treated as `Phase 0` blockers before any serious rollout.

| Blocker | Status | Evidence | Why it matters |
| --- | --- | --- | --- |
| Public access to superadmin module data | `Unsafe for production` | `app.py:1386-1391` returns `module_payload` for any `context`; live unauthenticated request to `/api/module?context=superadmin&name=all%20users` returned user registry data on 2026-04-23. | Exposes privileged operational data and breaks the boundary between public and admin-only surfaces. |
| Public worker verification data exposure | `Unsafe for production` | `app.py:1366-1383`; live unauthenticated request to `/api/workers/verify?id=IEE-WK-2026-00045821` returned worker name, city, rating, jobs completed, and status on 2026-04-23. | Leaks worker profile data and creates privacy and stalking risk. |
| Missing server-side RBAC on mutating endpoints | `Unsafe for production` | `app.py:1538-1689` mutates verifier, employer, and admin records without asserting role ownership. | Any authenticated or unauthenticated caller can potentially perform privileged actions depending on endpoint path and payload. |
| Plaintext passwords in state | `Unsafe for production` | Seed data contains raw passwords in `app.py:35-113`; login compares raw values in `app.py:1406-1422`; new registrations persist raw passwords in `app.py:1466` and `app.py:1499`. | Credential leakage risk, no password hygiene, no recovery model, and no compliance story. |
| Weak session model | `Unsafe for production` | Session tokens are stored in JSON state via `new_session` in `app.py:630-633`; cookies are `HttpOnly` and `SameSite=Lax` but have no `Secure` flag, no expiry, and no idle timeout in `app.py:1416`, `app.py:1427`, `app.py:1434`. | No session TTL, weak revocation model, and poor deployment hardening. |
| Guest worker application flow | `Unsafe for production` | `app.py:1617-1629` allows a guest applicant name when `current_user` is missing. | Enables fake applications and makes workforce matching untrustworthy. |
| Audit trail is informational, not trustworthy | `Unsafe for production` | `audit` uses a hard-coded IP default and truncates to 20 records in `app.py:284-292`. | No forensic quality, no actor assurance, no immutable history. |
| No consent, privacy, or document security model | `Missing but required` | No data retention, consent capture, DSR flow, document encryption, or role-scoped PII handling exists anywhere in the current schema. | High risk for any worker identity, KYC, or payroll rollout. |

## What Is Implemented Today

### Role Flow Audit

| Role | Entry points | Real backend actions | Demo-only / static | Missing but required | Data touched |
| --- | --- | --- | --- | --- | --- |
| Worker | Main nav, register, login modal, worker dashboard, verify worker page | `POST /api/register`, `POST /api/login`, `GET /api/session`, `POST /api/worker/apply`, `POST /api/worker-id/generate`, `GET /api/workers/verify` | Most sidebar modules are generated from seeded rows in `module_payload` (`app.py:331-388`); work history, payments, certifications, notifications, and grievance data are mostly hard-coded snapshots. | Search and filters, saved profile editing, document upload, availability, saved jobs, application pipeline, messaging, grievance case workflow, real payments ledger, consent and privacy controls. | `users`, `workers`, `jobs.applicants`, `audit_log`, `sessions` |
| Employer | Main nav, login modal, employer dashboard | `POST /api/login`, `POST /api/employer/post-job`, `POST /api/employer/bulk-hire`, `POST /api/employer/hire` | Company profile, posted jobs, workforce, payroll, and analytics modules are mostly seeded tables in `module_payload` (`app.py:389-437`). | Candidate pipeline, shortlist management, chat/notifications, company verification, document collection, compliance profile, workforce roster by assignment, payroll approval, invoices, and audit-safe hiring stages. | `users`, `jobs`, `bulk_requests`, `audit_log`, `sessions` |
| Verifier | Main nav, login modal, verifier dashboard | `POST /api/login`, `POST /api/verifier/action`, `POST /api/verifier/field-kyc` | QR scanner, zone map, stats, and monthly report modules are seeded or declarative (`app.py:438-486`). The UI suggests evidence capture, but the backend only stores a status change. | Evidence upload, photo/document storage, case notes, duplicate detection, supervisor review, reassignment, SLA, fraud escalation, device trust, geo/time stamp validation. | `users`, `verification_queue`, `workers`, `audit_log`, `sessions` |
| Superadmin | Hidden shortcut, admin modal, superadmin dashboard | `POST /api/admin/login`, `POST /api/admin/user-action`, `POST /api/admin/create-verifier`, `POST /api/admin/publish-notice` | Dashboard modules under `module_payload` are read-only synthetic views backed by current JSON state (`app.py:487-552`). | True RBAC, admin scoping, review queues, policy controls, export tools, alerting, workflow approvals, audit search, integration monitoring, retention policies. | `users`, `notices`, `audit_log`, `sessions` |

### Shared UI and Backend Reality

| Feature area | Classification | Evidence | Notes |
| --- | --- | --- | --- |
| Worker registration and login | `Implemented now` | `iee_government_portal.html:357-372`, `app.py:1437-1512` | Worker and employer registrations are persisted. |
| Role dashboards | `Implemented now` | Dashboard UI exists in `iee_government_portal.html:538-929`; session restore in `app.py:739-751` | Dashboards render and route correctly after login. |
| Sidebar modules | `Demo-only / static` | Generic modal loader in `app.py` script opens `/api/module`; many returned rows are hard-coded (`app.py:331-552`) | Useful for demos, not for production workflows. |
| Worker ID generation | `Implemented now` | `app.py:1514-1536` | Generates an ID and appends a worker row, but bypasses a real verification lifecycle. |
| Public worker verification page | `Implemented now` and `Unsafe for production` | `iee_government_portal.html` verify surfaces plus `app.py:1366-1383` | Current data exposure is too broad. |
| Bulk hiring | `Implemented now` | `iee_government_portal.html:662-675`, `app.py:1565-1584` | Persists a request but does not run real matching. |
| Single job posting | `Implemented now` | `app.py:1586-1604` | Persists listings, but no candidate pipeline or eligibility checks. |
| Direct worker hire | `Implemented now` | `app.py:1606-1615` | Logs an action only; does not create a contract or assignment record. |
| Field KYC submission | `Implemented now` | `iee_government_portal.html:777-789`, `app.py:1632-1643` | Stores only a status update, not structured evidence. |
| Admin user actions | `Implemented now` but `Unsafe for production` | `iee_government_portal.html:882-891`, `app.py:1551-1563` | No server-side admin role assertion. |
| Verifier creation | `Implemented now` but `Unsafe for production` | `iee_government_portal.html:899-909`, `app.py:1645-1671` | Creates live credentials in plaintext. |
| Notice publishing | `Implemented now` | `iee_government_portal.html:913-921`, `app.py:1673-1689` | Notices are persisted and visible in admin modules. |
| Grievance, help, payment, upskilling shortcuts | `Demo-only / static` | Action map in `app.py:1691-1711` | These return generic toasts and do not open real systems. |

## Prototype-Only Capabilities in `IEE_SuperAdmin_Advanced.html`

The advanced superadmin prototype is materially ahead of the current backend. It should be treated as product direction, not current capability.

### Prototype-Only Modules

- AI governance and anomaly intelligence
- Compliance matrix across GST, EPFO, ESIC, wage integrity, and contract matching
- Worker journey tracker from registration to placement, PF, DBT, and rating
- Contract intelligence with principal employer and contractor views
- Finance, banking, micro-loan, and DBT orchestration
- Employer risk scoring and fraud referrals
- NCS, eShram, PMKVY, and NSDC sync storytelling

### Evidence

`IEE_SuperAdmin_Advanced.html` contains references to:

- contract fraud detection and AI risk scoring
- EPFO, ESIC, GST, and NCS sync modules
- worker journey timelines with eShram, PMKVY, PF UAN, and DBT milestones
- contract-level compliance and wage diversion calculations
- finance and micro-loan management

None of these concepts exist in the current persisted schema in `portal_data.json`, and none of the related backend routes exist in `app.py`.

## Benchmark Matrix

The goal here is not to copy competitors feature-for-feature. It is to understand what each category already teaches the market and what IEE must do to be credible.

### Government Stack

| Platform | Strengths relevant to IEE | What IEE should learn |
| --- | --- | --- |
| National Career Service (NCS) | National jobs marketplace, career centres, counselling, events, and multi-stakeholder public employment services. | IEE needs a stronger worker discovery layer, employer onboarding rigor, and assisted-service operations for low-digital users. |
| eShram | Large-scale unorganised worker registration with portable identity and welfare orientation. | IEE should not invent worker identity in isolation; it should model external identity linkage and consented data sync readiness. |
| Skill India Digital Hub | Unified skilling, certification, and opportunity discovery across learners and ecosystem partners. | IEE needs a real skilling graph: courses, certifications, provider metadata, and employability matching. |
| EPFO | Employer/employee account services, UAN lifecycle, contribution records, and employer filing workflows. | IEE employer compliance data must become structured, auditable, and role-specific, not a marketing metric. |
| ESIC | Employer and beneficiary service workflows, contribution and benefit administration. | Welfare and social protection surfaces should be modeled as structured worker benefits, not dashboard labels. |

### Marketplace and Hiring Stack

| Platform | Strengths relevant to IEE | What IEE should learn |
| --- | --- | --- |
| Digital Labour Chowk (DLC) | Blue-collar/construction positioning, verified field-ready workers, local trust model, and reduced middlemen narrative. | IEE can compete if it combines DLC-style field trust with better public-sector interoperability and stronger workflow depth. |
| apna | App-first blue-collar and entry-level matching, fast applications, high employer throughput, and direct HR conversations. | IEE needs mobile-first speed, alerts, messaging, and low-friction application flow. |
| Naukri | Mature recruiter tooling, resume search, employer products, and structured demand capture. | IEE employer workflows need search, shortlist, filters, and recruiter productivity tools. |
| LinkedIn | Trust, identity graph, recruiter CRM, employer branding, and deep workflow integrations. | IEE needs an employment graph: worker profile quality, history, references, and verifiable credentials. |
| foundit | Talent search, assessments, branding, and sourcing workflows. | IEE should add fit signals beyond raw role and wage matching. |
| Indeed | Simple job posting, screening questions, employer dashboard, and conversion-focused UX. | IEE should simplify employer posting and worker apply flows before adding heavy intelligence layers. |

### Capability Comparison

| Capability | IEE now | Government stack benchmark | Marketplace benchmark | Gap assessment |
| --- | --- | --- | --- | --- |
| Worker onboarding and identity | Basic registration + demo worker ID | Strong in eShram and NCS-assisted flows | Moderate to strong, usually optimized for speed | IEE needs verified identity, assisted onboarding, consent, and profile completion. |
| Employer onboarding and hiring workflow | Basic registration, posting, bulk request | Moderate; public systems are usually more procedural | Strong in Naukri, LinkedIn, Indeed, apna | IEE needs candidate pipeline, search, communication, and compliance data. |
| Job discovery and matching quality | Basic listing and apply | Moderate; NCS is broad but not marketplace-fast | Strong in leading marketplaces | IEE needs filters, ranking, alerts, availability, and response-time optimization. |
| Verification and trust | Verifier role exists, evidence model missing | Strong in identity-linked public systems | Moderate; trust comes from profiles, reviews, and product tooling | IEE needs real case management and audit-safe verification. |
| Skills, certifications, and training | Seeded courses and certificates only | Strong in Skill India ecosystem | Moderate to strong depending on platform | IEE needs actual course/certificate records and matching logic. |
| Payroll, benefits, welfare linkage | Seeded payment rows only | Strong in EPFO and ESIC for formal benefits | Limited to moderate in private job marketplaces | Major opportunity for IEE if modeled properly. |
| Grievance and support | Toasts and seeded rows | Strong expectation in public systems | Varies; usually support-first, not statutory grievance | IEE needs a real case system. |
| Mobile, accessibility, multilingual reach | Desktop-friendly portal, limited assisted-service depth | Strong expectation for public platforms | Strong in app-first players like apna | IEE needs mobile-native and multilingual delivery. |
| Analytics, compliance, and admin operations | Admin dashboard + prototype vision | Strong in public administration systems | Strong in recruiter analytics, weaker on labour compliance | IEE can differentiate here, but only after Phase 0 hardening. |

## Prioritized Gap List and Roadmap

### Phase 0: Platform Hardening

Objective: turn the current demo into a safe system foundation.

#### Build scope

- Replace plaintext password storage with salted hashing.
- Introduce `auth`, `authorization`, `session`, and `public` endpoint boundaries.
- Add role guards for every mutating route and every privileged read route.
- Remove public access to superadmin module payloads.
- Narrow public worker verification to minimal card-validation output, or require signed QR tokens.
- Add session expiry, revocation, `Secure` cookies, and idle timeout.
- Create an immutable audit event model with actor, role, timestamp, source IP, target entity, and before/after metadata.
- Separate worker PII from public worker profile fields.
- Add consent capture and data retention policy fields.

#### Exit criteria

- Unauthenticated users can access only approved public content.
- Every privileged route fails closed without the right role.
- Passwords are never stored or compared in plaintext.
- Audit search works and retains more than an in-memory or capped JSON slice.

### Phase 1: Core Marketplace

Objective: make worker-employer matching operationally credible.

#### Worker

- Editable profile, skills, languages, documents, availability, preferred wage, preferred radius
- Searchable and filterable job feed
- Saved jobs, tracked applications, offer states, and assignment history
- Alerts, notification center, and grievance case tracker

#### Employer

- Verified company onboarding and approver journey
- Job lifecycle: draft, published, shortlisted, offered, filled, closed
- Candidate search, shortlist, notes, messaging, rejection reasons
- Workforce roster and assignment view
- Payroll approval and settlement status

#### Verifier

- Structured verification case queue
- Evidence capture with documents, photos, notes, geo/time metadata
- Duplicate and fraud flags
- Escalation, reassignment, supervisor review, SLA timers

#### Superadmin

- Governance dashboard with approval queues
- User and organization controls with scoped permissions
- Notice center, configuration policies, and audit review
- Operational dashboards based on real data rather than seeded metrics

### Phase 2: Government and Ecosystem Interoperability

Objective: become integration-ready without over-claiming live sync before approvals exist.

- eShram linkage readiness for worker identity matching and consented sync
- NCS job publishing and placement audit readiness
- Skill India Digital Hub or NSDC-aligned certification mapping
- Employer compliance profile for EPFO, ESIC, GST, CLRA, and wage-related metadata
- Worker welfare and scheme eligibility surfaces
- Integration status monitoring, retries, and degraded-mode UX

### Phase 3: Advanced Platform Intelligence

Objective: bring the superadmin prototype vision into real, governed workflows.

- Worker journey timeline across identity, verification, training, placement, earnings, and welfare
- Contract intelligence: principal employer, contractor, deployed workers, rates, compliance status
- Risk scoring and anomaly detection for ghost workers, wage suppression, and filing mismatch
- Payroll and DBT orchestration
- Grievance intelligence and resolution monitoring
- Financial inclusion features such as salary-linked finance or micro-loan integrations

## Required Public Interfaces

The current ad hoc endpoints should be replaced with role-gated domain APIs.

### Public

- `GET /api/public/worker-card/:token`
- `POST /api/public/register-worker`
- `POST /api/public/register-employer`
- `POST /api/public/interest`

### Auth

- `POST /api/auth/login`
- `POST /api/auth/logout`
- `GET /api/auth/session`
- `POST /api/auth/password-reset`
- `POST /api/auth/verify-otp`

### Workers

- `GET /api/workers/me`
- `PATCH /api/workers/me`
- `GET /api/workers/jobs`
- `POST /api/workers/applications`
- `GET /api/workers/applications`
- `GET /api/workers/payments`
- `GET /api/workers/grievances`
- `POST /api/workers/grievances`

### Employers

- `GET /api/employers/me`
- `PATCH /api/employers/me`
- `POST /api/employers/jobs`
- `GET /api/employers/jobs`
- `GET /api/employers/candidates`
- `POST /api/employers/hires`
- `GET /api/employers/payroll`
- `GET /api/employers/compliance`

### Verifiers

- `GET /api/verifiers/cases`
- `GET /api/verifiers/cases/:id`
- `POST /api/verifiers/cases/:id/evidence`
- `POST /api/verifiers/cases/:id/decision`
- `POST /api/verifiers/cases/:id/escalate`

### Admin

- `GET /api/admin/overview`
- `GET /api/admin/users`
- `POST /api/admin/users/:id/status`
- `POST /api/admin/verifiers`
- `GET /api/admin/notices`
- `POST /api/admin/notices`
- `GET /api/admin/audit`
- `GET /api/admin/integrations`

### Integrations

- `GET /api/integrations/status`
- `POST /api/integrations/eshram/sync`
- `POST /api/integrations/ncs/publish`
- `POST /api/integrations/skills/map`

## Minimum Shared Domain Types

These are the minimum types needed to stop mixing display tables with domain state.

```ts
type WorkerProfile = {
  workerId: string;
  legalName: string;
  mobile: string;
  city: string;
  skills: string[];
  verificationStatus: "pending" | "approved" | "rejected" | "flagged";
  availability: "available" | "assigned" | "inactive";
  documents: DocumentRef[];
  linkedIds: ExternalIdentityLink[];
  privacy: PrivacySettings;
};

type EmployerAccount = {
  employerId: string;
  companyName: string;
  sector: string;
  city: string;
  verificationStatus: "pending" | "approved" | "suspended";
  compliance: ComplianceProfile;
  contacts: EmployerContact[];
};

type JobPosting = {
  jobId: string;
  employerId: string;
  title: string;
  category: string;
  wage: number;
  location: string;
  duration: string;
  status: "draft" | "published" | "filled" | "closed";
  requirements: string[];
};

type Application = {
  applicationId: string;
  jobId: string;
  workerId: string;
  status: "submitted" | "shortlisted" | "offered" | "hired" | "rejected";
  timestamps: {
    createdAt: string;
    updatedAt: string;
  };
};

type VerificationCase = {
  caseId: string;
  workerId: string;
  assignedVerifierId: string;
  status: "pending" | "in_review" | "approved" | "rejected" | "escalated";
  evidence: EvidenceItem[];
  riskFlags: string[];
  slaDueAt: string | null;
};

type ContractRecord = {
  contractId: string;
  employerId: string;
  principalEmployerName: string | null;
  workerIds: string[];
  wageTerms: WageTerms;
  compliance: ComplianceStatus;
};

type PaymentBatch = {
  batchId: string;
  employerId: string;
  workerIds: string[];
  totalAmount: number;
  status: "draft" | "processing" | "released" | "failed";
};

type Notice = {
  noticeId: string;
  title: string;
  category: string;
  priority: "low" | "medium" | "high";
  content: string;
  publishedAt: string;
};

type AuditEvent = {
  auditId: string;
  actorId: string;
  actorRole: string;
  action: string;
  targetType: string;
  targetId: string;
  sourceIp: string;
  createdAt: string;
  metadata: Record<string, string | number | boolean>;
};

type IntegrationStatus = {
  integrationKey: string;
  status: "ready" | "degraded" | "offline" | "not_configured";
  lastSuccessAt: string | null;
  lastError: string | null;
};
```

## Implementation Sequence

1. Ship `Phase 0` security, privacy, and RBAC changes first.
2. Replace seeded module payloads with real service-backed worker, employer, verifier, and admin read models.
3. Add the core marketplace workflow before attempting government sync or AI/compliance intelligence.
4. Introduce integration adapters only after the domain model is stable.
5. Rebuild the advanced superadmin prototype on top of real contract, compliance, and audit records.

## Test Plan

### Security and Access

- Unauthenticated users cannot read admin, verifier, employer-private, or worker-private data.
- A worker cannot invoke verifier or admin actions.
- An employer cannot suspend users or create verifier accounts.
- Sessions expire and revoked sessions stop working immediately.

### Worker

- A worker can register, log in, edit profile, discover jobs, apply, and track outcomes.
- Duplicate worker registrations are rejected or resolved through a defined merge flow.
- Worker verification visibility is limited to allowed public fields only.

### Employer

- An employer can create jobs, view candidates, move applicants through stages, and confirm hires.
- Employer compliance data is visible only to employer admins and superadmins.

### Verifier

- A verifier can receive assigned cases, upload evidence, decide cases, and escalate suspicious records.
- Evidence and decisions are audit-linked and cannot be silently overwritten.

### Superadmin

- A superadmin can manage users, publish notices, assign verifiers, inspect audit events, and review integration status.
- Suspended or banned users lose access immediately.

### Integrations and Analytics

- Integration failures degrade safely and do not expose raw partner responses.
- Risk scores and compliance flags are visible only to authorized roles.
- Prototype-only metrics are not shown as live operational truth until backed by real data.

## Decisions and Defaults

- Product scope remains India-first and focused on blue-collar, informal, and semi-skilled employment.
- `DLC` is treated as Digital Labour Chowk.
- The recommended posture is balanced: strong marketplace usability plus phased government/compliance readiness.
- Government integrations should be described as readiness or phased sync unless production agreements and credentials exist.
- The current portal should be described externally as a prototype or pilot platform until `Phase 0` is complete.

## Appendix: Benchmark Sources

Official or primary sources reviewed for the benchmark matrix:

- NCS about page: <https://www.ncs.gov.in/pages/about-us.aspx>
- eShram about page: <https://eshram.gov.in/about-e-shram-portal>
- eShram objectives: <https://eshram.gov.in/e-shram-objectives>
- Skill India Digital Hub courses: <https://courses.skillindiadigital.gov.in/courses/>
- EPFO employer unified portal: <https://unifiedportal-emp.epfindia.gov.in/>
- ESIC employer portal: <https://portal.esic.gov.in/ESICInsurance1/ESICInsurancePortal/portallogin.aspx>
- Digital Labour Chowk about page: <https://digitallabourchowk.com/about-us/>
- apna employer page: <https://employer.apna.co/>
- Naukri Hiring Suite: <https://recruit.naukri.com/hiringsuite/index.html>
- LinkedIn Talent Solutions: <https://business.linkedin.com/talent-solutions/>
- LinkedIn Recruiter: <https://business.linkedin.com/talent-solutions/recruiter/>
- foundit recruiter products: <https://recruiter.foundit.in/>
- Indeed for employers: <https://in.indeed.com/hire>

These sources were used for directional benchmarking only. Exact partner integrations, commercial terms, or API availability should be validated separately before implementation.
