$Target = 'C:\Users\ADMIN\Downloads\iee_government_portal (3).html'
$Backup = 'C:\Users\ADMIN\Downloads\iee_government_portal (3).backup-before-live-services.html'

if(Test-Path $Backup){
  $html = [System.IO.File]::ReadAllText($Backup, [System.Text.Encoding]::UTF8)
} else {
  $html = [System.IO.File]::ReadAllText($Target, [System.Text.Encoding]::UTF8)
  [System.IO.File]::WriteAllText($Backup, $html, [System.Text.Encoding]::UTF8)
}

$html = $html.Replace("showPage('gap-analysis-page');setNav(this)"">Gap Analysis", "showPage('live-features-page');setNav(this)"">Live Services")
$html = $html.Replace("<div class=""qa-item"" onclick=""showToast('Upskilling portal loading...')""><span class=""qa-ico"">&#127891;</span><div class=""qa-lbl"">Upskilling Courses</div></div>", "<div class=""qa-item"" onclick=""openFeatureModal('adaptive-learning')""><span class=""qa-ico"">&#127891;</span><div class=""qa-lbl"">Skills Engine</div></div>")
$html = $html.Replace("<div class=""qa-item"" onclick=""showToast('Payment status portal loading...')""><span class=""qa-ico"">&#128184;</span><div class=""qa-lbl"">Payment Status</div></div>", "<div class=""qa-item"" onclick=""openFeatureModal('gst-einvoice')""><span class=""qa-ico"">&#128184;</span><div class=""qa-lbl"">GST Invoice</div></div>")
$html = $html.Replace("<div class=""qa-item"" onclick=""showToast('Grievance portal loading...')""><span class=""qa-ico"">&#128221;</span><div class=""qa-lbl"">Grievance Portal</div></div>", "<div class=""qa-item"" onclick=""openFeatureModal('dispute-chatbot')""><span class=""qa-ico"">&#128221;</span><div class=""qa-lbl"">Dispute Bot</div></div>")
$html = $html.Replace("<div class=""dlink"">Upskilling Courses</div>", "<div class=""dlink"" onclick=""openFeatureModal('adaptive-learning')"">Upskilling Courses</div>")
$html = $html.Replace("<div class=""dlink"">Grievance &amp; Support</div>", "<div class=""dlink"" onclick=""openFeatureModal('dispute-chatbot')"">Grievance &amp; Support</div>")
$html = $html.Replace("<div class=""dlink"">Payroll &amp; Payments</div>", "<div class=""dlink"" onclick=""openFeatureModal('gst-einvoice')"">Payroll, GST &amp; TDS</div>")
$html = $html.Replace("<div class=""dlink"">Analytics &amp; Reports</div>", "<div class=""dlink"" onclick=""showPage('live-features-page')"">Live Services</div>")

$css = @'

/* LIVE SERVICES */
.act-filter{background:var(--blue)!important;color:#fff!important;border-color:var(--blue)!important}
.live-toolbar{background:#fff;border:1px solid var(--border);border-radius:5px;padding:12px 16px;margin-bottom:16px;display:flex;align-items:center;gap:10px;flex-wrap:wrap}
.live-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:12px;margin-bottom:18px}
.live-card{background:#fff;border:1px solid var(--border);border-radius:5px;overflow:hidden;display:flex;flex-direction:column;min-height:230px;transition:box-shadow .18s,transform .18s,border-color .18s}
.live-card:hover{transform:translateY(-2px);box-shadow:0 10px 24px rgba(15,35,65,.12);border-color:#9fb4d1}
.live-card-top{display:flex;gap:10px;padding:12px;border-bottom:1px solid var(--border);align-items:flex-start;background:linear-gradient(180deg,#fff,#f7f9fd)}
.live-ico{width:34px;height:34px;border-radius:5px;background:var(--blue);color:#fff;display:flex;align-items:center;justify-content:center;font-size:17px;flex-shrink:0}
.live-card h3{font-size:12.5px;color:var(--navy);line-height:1.25;margin-bottom:5px}
.live-card p{font-size:11px;color:var(--muted);line-height:1.55}
.live-body{padding:12px;display:flex;flex-direction:column;gap:9px;flex:1}
.live-meta{display:flex;gap:5px;flex-wrap:wrap}
.live-kpis{display:grid;grid-template-columns:1fr 1fr;gap:6px;margin-top:auto}
.live-kpi{border:1px solid var(--border);background:var(--stripe);border-radius:3px;padding:7px}
.live-kpi strong{display:block;color:var(--navy);font-size:13px;line-height:1}
.live-kpi span{font-size:9.5px;color:var(--muted)}
.live-actions{display:flex;gap:7px;padding:0 12px 12px}
.live-actions .btn-o,.live-actions .btn-p{flex:1;text-align:center;justify-content:center}
.service-console{background:#071a33;color:#dbeafe;border-radius:5px;padding:14px;min-height:150px;font-family:Consolas,'Courier New',monospace;font-size:11px;line-height:1.65;border:1px solid #102f58;white-space:pre-wrap}
.feature-form-grid{display:grid;grid-template-columns:1fr 1fr;gap:10px}
.feature-output{background:#f8fafc;border:1px solid var(--border);border-left:4px solid var(--green);border-radius:4px;padding:12px;font-size:11.5px;color:#243044;line-height:1.7;margin-top:12px}
.mini-list{display:grid;gap:7px;margin-top:8px}
.mini-item{border:1px solid var(--border);background:#fff;border-radius:4px;padding:8px;font-size:11px;color:#374151}
.accessible-mode{filter:contrast(1.18)}
.accessible-mode body,.accessible-mode .card,.accessible-mode .live-card{background:#fff}
.accessible-mode .nl,.accessible-mode .btn-p,.accessible-mode .btn-o{outline:2px solid transparent}
@media(max-width:1100px){.live-grid{grid-template-columns:repeat(3,1fr)}}
@media(max-width:820px){.live-grid{grid-template-columns:repeat(2,1fr)}.feature-form-grid{grid-template-columns:1fr}.live-toolbar .fi{width:100%!important}.stat-row{grid-template-columns:1fr 1fr}}
@media(max-width:560px){.live-grid{grid-template-columns:1fr}.live-kpis{grid-template-columns:1fr}.stat-row{grid-template-columns:1fr}}
'@
if($html -notlike '*/* LIVE SERVICES */*'){
  $html = $html.Replace("/* PRINT */", $css + "`r`n/* PRINT */")
}

$liveBlock = @'
<!-- LIVE SERVICES PAGE -->
<div id="live-features-page" class="page">
  <div class="bc"><div class="bci"><a onclick="showPage('home')">Home</a><span class="bc-sep">/</span>Live Platform Services</div></div>
  <div class="content" style="max-width:1180px">
    <div class="dtitle">IEE Live Services &amp; Automation</div>
    <div class="dsub" style="margin-bottom:20px">All advanced IEE features are active here as working portal modules. Use the filters, open any service, enter sample values, and generate live outputs inside the portal.</div>

    <div class="stat-row" style="margin-bottom:18px">
      <div class="sbox"><div class="sval">20</div><div class="slbl">Live Feature Modules</div><div class="schg sup">No gap analysis section</div></div>
      <div class="sbox or"><div class="sval">8</div><div class="slbl">Employer Automations</div><div class="schg sup">GST, TDS, EPFO, HRMS</div></div>
      <div class="sbox gr"><div class="sval">7</div><div class="slbl">Worker Welfare Tools</div><div class="schg sup">Benefits, NPS, safety, health</div></div>
      <div class="sbox sa"><div class="sval">5</div><div class="slbl">AI &amp; Platform Engines</div><div class="schg sup">Screening, alerts, APIs, credentials</div></div>
    </div>

    <div class="live-toolbar">
      <span style="font-size:11px;font-weight:700;color:var(--navy);letter-spacing:.04em;text-transform:uppercase">Services:</span>
      <button class="btn-o btn-sm live-filter act-filter" onclick="filterLiveServices('all',this)">All</button>
      <button class="btn-o btn-sm live-filter" onclick="filterLiveServices('worker',this)">Worker</button>
      <button class="btn-o btn-sm live-filter" onclick="filterLiveServices('employer',this)">Employer</button>
      <button class="btn-o btn-sm live-filter" onclick="filterLiveServices('compliance',this)">Compliance</button>
      <button class="btn-o btn-sm live-filter" onclick="filterLiveServices('safety',this)">Safety</button>
      <button class="btn-o btn-sm live-filter" onclick="filterLiveServices('platform',this)">Platform</button>
      <button class="btn-o btn-sm live-filter" onclick="filterLiveServices('green',this)">Green</button>
      <div style="margin-left:auto"><input class="fi" id="live-search" style="width:230px;margin:0" placeholder="Search services..." oninput="searchLiveServices(this.value)"></div>
    </div>

    <div class="live-grid" id="live-grid"></div>

    <div class="card">
      <div class="card-hd" style="justify-content:space-between">
        <span>Live Service Console</span>
        <button class="btn-w btn-sm" onclick="runLiveFeature('ai-interview')">Run AI Interview Demo</button>
      </div>
      <div class="card-bd">
        <div id="service-console" class="service-console">IEE service console ready.
Select any feature card and click Open Service to generate a live result.</div>
      </div>
    </div>
  </div>
</div>

<!-- LIVE FEATURE MODAL -->
<div class="overlay" id="live-feature-modal" onclick="if(event.target===this)closeModal('live-feature-modal')">
  <div class="modal" style="width:680px;max-width:96vw">
    <div class="modal-hd">
      <h3 id="lf-title">Live Service</h3>
      <button class="mclose" onclick="closeModal('live-feature-modal')">&times;</button>
    </div>
    <div class="modal-bd" id="lf-body"></div>
  </div>
</div>

<!-- LIVE SERVICES SCRIPTS -->
<script>
const liveFeatures=[
  {id:'ai-interview',cat:'platform',role:'AI Screening',ico:'&#129302;',title:'AI Interview Screening Bot',desc:'Voice and text screening for workers with fit score, language checks, availability and employer shortlist routing.',status:'Live',metric:'92%',metricLbl:'screening accuracy',forms:[['select','Role','Mason|Carpenter|Electrician|Welder|General Labour'],['select','Language','Hindi|Tamil|Telugu|English'],['input','Worker ID','IEE-WK-2026-00045821'],['select','Availability','Today|Tomorrow|This Week']],summary:'Shortlists candidates and prepares interview notes.'},
  {id:'adaptive-learning',cat:'worker',role:'Skills',ico:'&#127891;',title:'Adaptive Learning Engine for Skills',desc:'Personalised courses based on worker skill, local demand, certification gaps and acceptance history.',status:'Live',metric:'3',metricLbl:'courses suggested',forms:[['select','Current Skill','Masonry|Painting|Electrical|Plumbing|Site Safety'],['select','City','Chennai|Hyderabad|Bengaluru|Mumbai'],['select','Goal','Higher wage|Safety certificate|Supervisor path|New trade']],summary:'Builds a worker-specific learning path.'},
  {id:'safety-incident',cat:'safety',role:'Safety',ico:'&#9874;',title:'Construction Safety Incident Reporting',desc:'Site incident intake with severity, GPS-ready escalation, inspector alerting and employer safety analytics.',status:'Live',metric:'15m',metricLbl:'critical SLA',forms:[['input','Site Name','OMR Metro Site'],['select','Severity','Low|Medium|High|Critical'],['select','Incident Type','Near miss|Fall|Equipment|Electrical|Medical'],['textarea','Details','Worker slipped near scaffolding zone.']],summary:'Creates a safety ticket and escalation path.'},
  {id:'seasonal-surge',cat:'employer',role:'Hiring',ico:'&#128200;',title:'Seasonal Labour Surge Management',desc:'Predicts harvest, festival and construction demand spikes and activates worker notification pools.',status:'Live',metric:'85%',metricLbl:'forecast score',forms:[['select','Sector','Construction|Agriculture|Events|Logistics'],['input','District','Chennai'],['input','Workers Needed','120'],['select','Window','Next 7 days|Next 14 days|Next 30 days']],summary:'Generates a surge staffing plan.'},
  {id:'gst-einvoice',cat:'compliance',role:'Tax',ico:'&#129534;',title:'GST E-Invoice Auto-Generation',desc:'Generates GST-ready invoice numbers, IRN-style references, tax split and employer download records.',status:'Live',metric:'100%',metricLbl:'invoice coverage',forms:[['input','Employer GSTIN','33AABCS1234Z1Z5'],['input','Taxable Amount','85000'],['select','Supply Type','B2B|B2C|RCM'],['select','GST Rate','5|12|18']],summary:'Calculates tax and produces invoice metadata.'},
  {id:'msme-fast-track',cat:'employer',role:'Onboarding',ico:'&#127970;',title:'MSME Employer Fast-Track Portal',desc:'Three-minute Udyam-led employer onboarding with provisional posting access and KYC queueing.',status:'Live',metric:'3m',metricLbl:'onboarding time',forms:[['input','Udyam Number','UDYAM-TN-02-0012345'],['input','Business Name','Skyline Works'],['input','Mobile','9876500000'],['select','Entity Type','Micro|Small|Medium']],summary:'Creates provisional employer access.'},
  {id:'nps-lite',cat:'worker',role:'Pension',ico:'&#128176;',title:'Worker Pension NPS-Lite Auto-Enrolment',desc:'PRAN-style enrolment simulation with contribution setup, opt-out state and projected worker corpus.',status:'Live',metric:'&#8377;500',metricLbl:'monthly micro-save',forms:[['input','Worker ID','IEE-WK-2026-00045821'],['input','Contribution per Payment','50'],['select','Employer Match','No match|25% match|50% match'],['select','Consent','Enrol now|Opt out']],summary:'Enrols worker into pension workflow.'},
  {id:'benefits-portability',cat:'worker',role:'Welfare',ico:'&#128506;',title:'Cross-State Benefits Portability',desc:'Routes migrant worker benefits across states including ration, insurance and welfare scheme continuity.',status:'Live',metric:'36',metricLbl:'states and UTs',forms:[['input','Worker ID','IEE-WK-2026-00045821'],['select','From State','Tamil Nadu|Bihar|Odisha|Uttar Pradesh'],['select','To State','Karnataka|Maharashtra|Delhi|Tamil Nadu'],['select','Benefit','Ration|Insurance|BOCW Welfare|All']],summary:'Checks portability status and scheme routing.'},
  {id:'api-marketplace',cat:'platform',role:'Integration',ico:'&#128279;',title:'API Marketplace for HRMS Integration',desc:'OAuth-ready sandbox connectors for SAP, Workday, Oracle HCM, Darwinbox, GreytHR and custom HRMS tools.',status:'Live',metric:'6',metricLbl:'connectors',forms:[['select','HRMS','SAP SuccessFactors|Workday|Oracle HCM|Darwinbox|GreytHR|Custom REST'],['select','Scope','Worker verification|Payroll sync|Attendance webhook|Full access'],['input','Callback URL','https://hrms.example.com/iee/webhook']],summary:'Issues sandbox credentials and webhook plan.'},
  {id:'referral-network',cat:'employer',role:'Growth',ico:'&#129309;',title:'Employer Referral Network',desc:'Referral codes, conversion tracking, anti-fraud checks and automatic reward credit after first hire.',status:'Live',metric:'&#8377;1500',metricLbl:'sample reward',forms:[['input','Employer ID','EMP-TN-2026-001248'],['input','Referred Business','MetroBuild MSME'],['select','Expected Hiring','1-10 workers|11-50 workers|51-200 workers']],summary:'Creates referral code and reward tracker.'},
  {id:'accessibility',cat:'worker',role:'Accessibility',ico:'&#9855;',title:'Worker Disability &amp; Accessibility Features',desc:'PwD-aware job filters, high contrast support, screen-reader labels and accessible-site matching.',status:'Live',metric:'AA',metricLbl:'WCAG target',forms:[['select','Accessibility Need','Mobility support|Low vision|Hearing support|Cognitive support'],['select','Job Preference','Accessible construction|Office support|Packaging|Remote verification'],['select','UI Mode','Standard|High contrast']],summary:'Applies accessible job matching and UI preferences.'},
  {id:'women-night-safety',cat:'safety',role:'Women Safety',ico:'&#128680;',title:'Women Worker Safety &amp; Night Shift Module',desc:'Night shift eligibility, transport declaration, POSH routing and SOS escalation for women workers.',status:'Live',metric:'10m',metricLbl:'SOS response',forms:[['input','Worker Name','Priya Devi'],['input','Site','Chennai Port Night Shift'],['select','Transport Provided','Yes|No'],['select','Shift','Day|Night']],summary:'Validates safety and compliance requirements.'},
  {id:'blockchain-credential',cat:'platform',role:'Credentials',ico:'&#128272;',title:'Blockchain Credential Verification',desc:'Verifiable credential proof for PMKVY and skill certificates with tamper-evident hash and QR verification.',status:'Live',metric:'3s',metricLbl:'verification time',forms:[['input','Certificate ID','PMKVY-TN-2026-7782'],['select','Issuer','PMKVY|ITI|NSDC|Employer Academy'],['input','Worker ID','IEE-WK-2026-00045821']],summary:'Verifies credential authenticity.'},
  {id:'dispute-chatbot',cat:'safety',role:'Dispute',ico:'&#128172;',title:'Dispute Resolution Chatbot',desc:'Multilingual complaint intake for payment disputes, misconduct, job cancellation and wage mismatch.',status:'Live',metric:'24h',metricLbl:'first response',forms:[['select','Dispute Type','Payment delay|Wage mismatch|Misconduct|Job cancelled'],['select','Language','English|Hindi|Tamil|Telugu'],['textarea','Message','Employer has not released payment for three days of masonry work.']],summary:'Classifies complaint and creates case.'},
  {id:'dpdpa-compliance',cat:'compliance',role:'Privacy',ico:'&#128274;',title:'Data Anonymisation &amp; DPDPA Compliance',desc:'Consent ledger, data minimisation checks, anonymised exports and privacy impact workflow.',status:'Live',metric:'0',metricLbl:'direct identifiers',forms:[['select','Dataset','Worker profiles|Employer payroll|Dispute cases|Training history'],['select','Action','Anonymise export|Revoke consent|Generate DPIA|View consent log'],['input','Record Count','1250']],summary:'Runs privacy-safe data action.'},
  {id:'tds-form16b',cat:'compliance',role:'Tax',ico:'&#128179;',title:'Employer TDS Deduction &amp; Form 16B Auto',desc:'TDS calculation, deduction record, challan status and Form 16B generation for contracted worker payments.',status:'Live',metric:'7d',metricLbl:'form issue SLA',forms:[['input','Worker PAN','ABCDE1234F'],['input','Payment Amount','50000'],['select','TDS Rate','1|2|5|10'],['select','Quarter','Q1|Q2|Q3|Q4']],summary:'Calculates deduction and form record.'},
  {id:'epfo-esic-filing',cat:'compliance',role:'Payroll',ico:'&#128188;',title:'Automated EPFO / ESIC Filing (Employer)',desc:'Monthly ECR-style filing, UAN generation queue, ESIC coverage and compliance certificate output.',status:'Live',metric:'5m',metricLbl:'filing time',forms:[['input','Employer ID','EMP-TN-2026-001248'],['input','Workers in Filing','148'],['select','Month','April 2026|May 2026|June 2026'],['select','Scheme','EPFO + ESIC|EPFO only|ESIC only']],summary:'Prepares statutory filing output.'},
  {id:'job-alerts',cat:'worker',role:'AI Matching',ico:'&#128276;',title:'Job Alert Personalisation Engine',desc:'Personalised alerts using role, distance, wage floor, availability and worker acceptance signals.',status:'Live',metric:'5',metricLbl:'alerts today',forms:[['select','Role','Mason|Carpenter|Electrician|Painter|Welder'],['input','Max Distance KM','5'],['input','Minimum Wage','800'],['select','Availability','Today|Tomorrow|Weekend']],summary:'Generates a ranked worker job feed.'},
  {id:'mental-health',cat:'worker',role:'Wellbeing',ico:'&#128153;',title:'Worker Mental Health Support Module',desc:'PHQ-4 style check-in, anonymous support option, counselling resource routing and crisis escalation.',status:'Live',metric:'1h',metricLbl:'crisis SLA',forms:[['select','Mood Today','Good|Stressed|Anxious|Very low'],['select','Sleep Quality','Good|Average|Poor'],['select','Support Mode','Anonymous chat|Call counsellor|Self-help resources']],summary:'Creates wellbeing support recommendation.'},
  {id:'carbon-credit',cat:'green',role:'Sustainability',ico:'&#127793;',title:'Carbon Credit for Green Construction',desc:'Green construction metrics, material savings, audit queue and estimated carbon credit generation.',status:'Live',metric:'tCO2e',metricLbl:'credit estimate',forms:[['input','Project Name','Green Metro Depot'],['input','Cement Saved Tonnes','35'],['input','Recycled Waste Tonnes','120'],['select','Energy Source','Grid|Solar mix|Diesel|Hybrid']],summary:'Estimates green construction credit.'}
];

let liveFilter='all';
function escapeHtml(v){return String(v||'').replace(/[&<>"']/g,m=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[m]));}
function featureById(id){return liveFeatures.find(f=>f.id===id)||liveFeatures[0];}
function initLiveServices(){renderLiveServices(liveFeatures);}
function renderLiveServices(list){
  const grid=document.getElementById('live-grid');
  if(!grid) return;
  grid.innerHTML=list.map(f=>`
    <div class="live-card" data-cat="${f.cat}" data-text="${escapeHtml((f.title+' '+f.desc+' '+f.role).toLowerCase())}">
      <div class="live-card-top">
        <div class="live-ico">${f.ico}</div>
        <div><h3>${f.title}</h3><p>${f.desc}</p></div>
      </div>
      <div class="live-body">
        <div class="live-meta"><span class="badge b-green">${f.status}</span><span class="badge b-blue">${f.role}</span><span class="badge b-gray">${f.cat}</span></div>
        <div class="live-kpis"><div class="live-kpi"><strong>${f.metric}</strong><span>${f.metricLbl}</span></div><div class="live-kpi"><strong>Ready</strong><span>${f.summary}</span></div></div>
      </div>
      <div class="live-actions"><button class="btn-p btn-sm" onclick="openFeatureModal('${f.id}')">Open Service</button><button class="btn-o btn-sm" onclick="runLiveFeature('${f.id}')">Run Demo</button></div>
    </div>`).join('');
}
function filterLiveServices(cat,btn){
  liveFilter=cat;
  document.querySelectorAll('.live-filter').forEach(b=>b.classList.remove('act-filter'));
  if(btn) btn.classList.add('act-filter');
  searchLiveServices((document.getElementById('live-search')||{}).value||'');
}
function searchLiveServices(q){
  const term=String(q||'').toLowerCase();
  document.querySelectorAll('.live-card').forEach(card=>{
    const catOk=liveFilter==='all'||card.dataset.cat===liveFilter;
    const textOk=!term||card.dataset.text.includes(term);
    card.style.display=(catOk&&textOk)?'':'none';
  });
}
function openFeatureModal(id){
  const f=featureById(id);
  const body=document.getElementById('lf-body');
  document.getElementById('lf-title').textContent=f.title;
  body.innerHTML=`
    <div class="alert a-info">${f.desc}</div>
    <div class="feature-form-grid">
      ${f.forms.map((x,i)=>{
        const type=x[0], label=x[1], val=x[2], fid=`lf-${f.id}-${i}`;
        if(type==='select'){
          return `<div class="fg"><label class="fl">${label}</label><select class="fs live-input" id="${fid}" data-label="${escapeHtml(label)}">${val.split('|').map(o=>`<option>${escapeHtml(o)}</option>`).join('')}</select></div>`;
        }
        if(type==='textarea'){
          return `<div class="fg" style="grid-column:1/-1"><label class="fl">${label}</label><textarea class="fi live-input" id="${fid}" data-label="${escapeHtml(label)}" rows="3">${escapeHtml(val)}</textarea></div>`;
        }
        return `<div class="fg"><label class="fl">${label}</label><input class="fi live-input" id="${fid}" data-label="${escapeHtml(label)}" value="${escapeHtml(val)}"></div>`;
      }).join('')}
    </div>
    <div style="display:flex;gap:8px;margin-top:12px;flex-wrap:wrap">
      <button class="btn-p" onclick="runLiveFeature('${f.id}',true)">Generate Live Result</button>
      <button class="btn-w" onclick="showToast('${f.title} saved to dashboard.')">Save to Dashboard</button>
      <button class="btn-o" onclick="closeModal('live-feature-modal')">Close</button>
    </div>
    <div id="lf-output" class="feature-output" style="display:none"></div>`;
  openModal('live-feature-modal');
}
function getLiveInputs(){
  const out={};
  document.querySelectorAll('#lf-body .live-input').forEach(el=>out[el.dataset.label]=el.value);
  return out;
}
function makeCode(prefix){return prefix+'-'+Math.random().toString(36).slice(2,7).toUpperCase();}
function runLiveFeature(id,fromModal){
  const f=featureById(id);
  const data=fromModal?getLiveInputs():{};
  const msg=buildFeatureResult(id,data);
  const consoleEl=document.getElementById('service-console');
  if(consoleEl) consoleEl.textContent='['+new Date().toLocaleTimeString('en-IN')+'] '+f.title+'\n'+msg.replace(/<[^>]+>/g,'').replace(/\n{3,}/g,'\n\n');
  const output=document.getElementById('lf-output');
  if(fromModal&&output){output.style.display='block';output.innerHTML=msg;}
  if(typeof showToast==='function') showToast(f.title+' completed.');
}
function buildFeatureResult(id,d){
  const amount=parseFloat(d['Taxable Amount']||d['Payment Amount']||0);
  const rate=parseFloat(d['GST Rate']||d['TDS Rate']||0);
  const tax=Math.round(amount*rate/100);
  const workers=parseInt(d['Workers Needed']||d['Workers in Filing']||0,10);
  const common={
    'ai-interview':`<strong>Screening complete:</strong> ${escapeHtml(d['Worker ID']||'IEE-WK-2026-00045821')} scored <b>87/100</b> for ${escapeHtml(d.Role||'Mason')}. Shortlisted for employer review with ${escapeHtml(d.Language||'Hindi')} interview notes and availability marked ${escapeHtml(d.Availability||'Today')}.<div class="mini-list"><div class="mini-item">Suggested questions: safety practice, wage expectation, previous site experience.</div><div class="mini-item">Employer action: auto-shortlist and schedule 8 minute call.</div></div>`,
    'adaptive-learning':`<strong>Learning path ready:</strong> ${escapeHtml(d['Current Skill']||'Masonry')} worker in ${escapeHtml(d.City||'Chennai')} should take Advanced Safety, Blueprint Reading and Supervisor Basics. Placement uplift estimate: <b>31%</b>.`,
    'safety-incident':`<strong>Incident ticket ${makeCode('SAFE')} created.</strong> Severity ${escapeHtml(d.Severity||'High')} at ${escapeHtml(d['Site Name']||'site')} routed to employer safety officer.${(d.Severity==='Critical'||d.Severity==='High')?' Labour inspector escalation timer started.':''}`,
    'seasonal-surge':`<strong>Surge plan activated:</strong> ${workers||120} ${escapeHtml(d.Sector||'Construction')} workers needed in ${escapeHtml(d.District||'Chennai')}. Forecast demand confidence: <b>85%</b>. Worker pool notified in 3 rings: 5 km, 15 km, cross-district.`,
    'gst-einvoice':`<strong>GST e-invoice generated:</strong> Invoice ${makeCode('INV')}, IRN ${makeCode('IRN')}. Taxable value &#8377;${amount||85000}, GST @ ${rate||18}% = &#8377;${tax||15300}. Supply type: ${escapeHtml(d['Supply Type']||'B2B')}.`,
    'msme-fast-track':`<strong>MSME fast-track approved:</strong> Provisional Employer ID ${makeCode('EMP')} issued for ${escapeHtml(d['Business Name']||'Skyline Works')}. Job posting access enabled while KYC is queued.`,
    'nps-lite':`<strong>NPS-Lite workflow:</strong> ${(d.Consent==='Opt out')?'Opt-out recorded with consent log.':'PRAN '+makeCode('PRAN')+' generated.'} Contribution per payment: &#8377;${escapeHtml(d['Contribution per Payment']||'50')}. Employer match: ${escapeHtml(d['Employer Match']||'No match')}.`,
    'benefits-portability':`<strong>Benefits portability checked:</strong> ${escapeHtml(d['Worker ID']||'Worker')} moving from ${escapeHtml(d['From State']||'Tamil Nadu')} to ${escapeHtml(d['To State']||'Karnataka')}. Ration, insurance and BOCW routing status: <b>portable</b>.`,
    'api-marketplace':`<strong>API sandbox issued:</strong> Key ${makeCode('API')} for ${escapeHtml(d.HRMS||'HRMS')} with scope ${escapeHtml(d.Scope||'Worker verification')}. Webhook subscribed at ${escapeHtml(d['Callback URL']||'callback URL')}.`,
    'referral-network':`<strong>Referral created:</strong> Code REF-${Math.random().toString(36).slice(2,8).toUpperCase()} linked to ${escapeHtml(d['Employer ID']||'EMP')}. Reward estimate: &#8377;1,500 after first verified hire by ${escapeHtml(d['Referred Business']||'referred employer')}.`,
    'accessibility':`<strong>Accessibility profile saved:</strong> ${escapeHtml(d['Accessibility Need']||'Mobility support')} matched with 12 suitable jobs. ${(d['UI Mode']==='High contrast')?'High contrast mode applied.':'Standard UI retained.'}`,
    'women-night-safety':`<strong>Safety validation:</strong> ${escapeHtml(d['Worker Name']||'Worker')} ${d.Shift==='Night'?'requires transport, SOS contact and POSH compliance before approval.':'is cleared for day-shift matching.'} Transport declaration: ${escapeHtml(d['Transport Provided']||'No')}.`,
    'blockchain-credential':`<strong>Credential verified:</strong> ${escapeHtml(d['Certificate ID']||'certificate')} from ${escapeHtml(d.Issuer||'issuer')} anchored with proof hash 0x${Math.random().toString(16).slice(2,14)}. Verification time: 2.4 seconds.`,
    'dispute-chatbot':`<strong>Dispute case ${makeCode('CASE')} opened:</strong> Type ${escapeHtml(d['Dispute Type']||'Payment delay')} classified for ${escapeHtml(d.Language||'English')} response. Bot reply: payment evidence requested; SLA clock started.`,
    'dpdpa-compliance':`<strong>DPDPA action complete:</strong> ${escapeHtml(d.Action||'Anonymise export')} applied to ${escapeHtml(d.Dataset||'dataset')} for ${escapeHtml(d['Record Count']||'1250')} records. Direct identifiers removed and consent log updated.`,
    'tds-form16b':`<strong>TDS calculated:</strong> Payment &#8377;${amount||50000}, rate ${rate||2}%, deduction &#8377;${tax||1000}. Form 16B draft ${makeCode('F16B')} created for PAN ${escapeHtml(d['Worker PAN']||'ABCDE1234F')}.`,
    'epfo-esic-filing':`<strong>Statutory filing prepared:</strong> ${workers||148} workers included for ${escapeHtml(d.Month||'April 2026')}. ECR ${makeCode('ECR')} and challan ${makeCode('CHLN')} ready for ${escapeHtml(d.Scheme||'EPFO + ESIC')}.`,
    'job-alerts':`<strong>Personalised alerts generated:</strong> 5 jobs ranked for ${escapeHtml(d.Role||'Mason')} within ${escapeHtml(d['Max Distance KM']||'5')} km above &#8377;${escapeHtml(d['Minimum Wage']||'800')}/day.<div class="mini-list"><div class="mini-item">1. Metro Works - 96% match - &#8377;950/day</div><div class="mini-item">2. Skyline Site - 91% match - &#8377;875/day</div><div class="mini-item">3. Prestige Builders - 84% match - &#8377;825/day</div></div>`,
    'mental-health':`<strong>Wellbeing check-in complete:</strong> Mood ${escapeHtml(d['Mood Today']||'Stressed')}, sleep ${escapeHtml(d['Sleep Quality']||'Average')}. Recommended support: ${escapeHtml(d['Support Mode']||'Anonymous chat')}. High-risk escalation ${(d['Mood Today']==='Very low'||d['Sleep Quality']==='Poor')?'enabled':'not required'}.`,
    'carbon-credit':`<strong>Green credit estimate:</strong> ${escapeHtml(d['Project Name']||'Project')} can claim approximately <b>${Math.max(1,Math.round((parseFloat(d['Cement Saved Tonnes']||35)*0.8)+(parseFloat(d['Recycled Waste Tonnes']||120)*0.05)))}</b> tCO2e credits. Audit queue ${makeCode('GREEN')} created.`
  };
  if(id==='accessibility' && d['UI Mode']==='High contrast') document.documentElement.classList.add('accessible-mode');
  return common[id]||'<strong>Service completed.</strong>';
}
initLiveServices();
</script>

'@

$pattern = '(?s)<!--[^>]*GAP ANALYSIS PAGE[^>]*-->.*?</script>\s*(?=<!-- SUPER ADMIN HIDDEN LOGIN MODAL -->)'
$newHtml = [System.Text.RegularExpressions.Regex]::Replace($html, $pattern, $liveBlock)
if($newHtml -eq $html){ throw 'Could not locate the gap analysis section to replace.' }

[System.IO.File]::WriteAllText($Target, $newHtml, [System.Text.Encoding]::UTF8)
Write-Output "Updated $Target"
Write-Output "Backup saved to $Backup"
