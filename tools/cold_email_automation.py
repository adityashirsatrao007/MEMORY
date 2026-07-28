#!/usr/bin/env python3
"""
Cold Email Automation for Internship Applications
Sends personalized cold emails with resume to HR/recruitment contacts
at 100+ top MNCs including FAANG, finance, consulting, and tech.
"""

import smtplib
import ssl
import time
import random
import os
import json
import logging
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import encoders
from datetime import datetime
from pathlib import Path

# ─── CONFIG ───────────────────────────────────────────────────
SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 587
SMTP_USER = os.environ.get("SMTP_USER", "")
SMTP_PASS = os.environ.get("SMTP_PASS", "")
SMTP_FROM = os.environ.get("SMTP_FROM", SMTP_USER)

RESUME_PATH = "/tmp/resume.pdf"
LOG_DIR = Path("/tmp/cold_email_logs")
LOG_DIR.mkdir(exist_ok=True)

# ─── LOGGING ──────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(LOG_DIR / "email_log.txt"),
        logging.StreamHandler(),
    ],
)

# ─── COMPANIES DATABASE ──────────────────────────────────────
# Format: { "Company Name": { "domains": [...], "hr_emails": [...], "notes": "..." } }

COMPANIES = {
    # ── FAANG / BIG TECH ──
    "Google (Alphabet)": {
        "domains": ["google.com"],
        "emails": ["careers@google.com", "aspirations@google.com"],
        "notes": "AI/ML internships at Google Research & DeepMind"
    },
    "Meta (Facebook)": {
        "domains": ["meta.com", "fb.com"],
        "emails": ["careers@meta.com", "ai-internships@meta.com"],
        "notes": "Meta AI Research internships"
    },
    "Apple": {
        "domains": ["apple.com"],
        "emails": ["applecareers@apple.com", "ai-research@apple.com"],
        "notes": "Apple AI/ML internship program"
    },
    "Amazon": {
        "domains": ["amazon.com"],
        "emails": ["amazon-internships@amazon.com", "aws-ai-intern@amazon.com"],
        "notes": "Amazon Science & AWS AI/ML internships"
    },
    "Netflix": {
        "domains": ["netflix.com"],
        "emails": ["talent@netflix.com", "careers@netflix.com"],
        "notes": "Netflix ML/AI platform internships"
    },
    "Microsoft": {
        "domains": ["microsoft.com"],
        "emails": ["internships@microsoft.com", "americas@microsoft.com"],
        "notes": "Microsoft Research & Azure AI internships"
    },
    "NVIDIA": {
        "domains": ["nvidia.com"],
        "emails": ["careers@nvidia.com", "ai-intern@nvidia.com"],
        "notes": "NVIDIA AI/Deep Learning internships"
    },
    "Tesla": {
        "domains": ["tesla.com", "teslamotors.com"],
        "emails": ["careers@tesla.com", "ai-team@tesla.com"],
        "notes": "Tesla AI & Autopilot internships"
    },
    "OpenAI": {
        "domains": ["openai.com"],
        "emails": ["careers@openai.com", "internships@openai.com"],
        "notes": "OpenAI research internships"
    },
    "Palantir Technologies": {
        "domains": ["palantir.com"],
        "emails": ["careers@palantir.com", "talent@palantir.com"],
        "notes": "Palantir AI/ML deployment internships"
    },
    "Uber": {
        "domains": ["uber.com"],
        "emails": ["careers@uber.com", "ai-labs@uber.com"],
        "notes": "Uber AI Labs & ML infrastructure"
    },
    "Airbnb": {
        "domains": ["airbnb.com"],
        "emails": ["careers@airbnb.com", "tech-talent@airbnb.com"],
        "notes": "Airbnb ML & data science internships"
    },
    "Snowflake": {
        "domains": ["snowflake.com"],
        "emails": ["careers@snowflake.com"],
        "notes": "Snowflake AI/ML internships"
    },
    "Databricks": {
        "domains": ["databricks.com"],
        "emails": ["careers@databricks.com", "university-recruiting@databricks.com"],
        "notes": "Databricks ML/AI platform internships"
    },
    "ServiceNow": {
        "domains": ["servicenow.com"],
        "emails": ["careers@servicenow.com", "talent@servicenow.com"],
        "notes": "ServiceNow AI research internships"
    },
    "Salesforce": {
        "domains": ["salesforce.com"],
        "emails": ["careers@salesforce.com", "salesforce-university@salesforce.com"],
        "notes": "Salesforce AI Research & Einstein internships"
    },
    "Adobe": {
        "domains": ["adobe.com"],
        "emails": ["careers@adobe.com", "talent@adobe.com"],
        "notes": "Adobe AI/ML & Sensei internships"
    },
    "Cisco": {
        "domains": ["cisco.com"],
        "emails": ["careers@cisco.com", "talent@cisco.com"],
        "notes": "Cisco AI/ML internships"
    },
    "IBM": {
        "domains": ["ibm.com"],
        "emails": ["careers@ibm.com", "ibmresearch@ibm.com"],
        "notes": "IBM Research AI internships"
    },
    "Oracle": {
        "domains": ["oracle.com"],
        "emails": ["careers@oracle.com", "talent@oracle.com"],
        "notes": "Oracle AI/ML & OCI internships"
    },
    "Intel": {
        "domains": ["intel.com"],
        "emails": ["careers@intel.com", "talent@intel.com"],
        "notes": "Intel AI/ML internship programs"
    },
    "Qualcomm": {
        "domains": ["qualcomm.com"],
        "emails": ["careers@qualcomm.com", "talent@qualcomm.com"],
        "notes": "Qualcomm AI research internships"
    },
    "AMD": {
        "domains": ["amd.com"],
        "emails": ["careers@amd.com", "talent@amd.com"],
        "notes": "AMD AI/ML internships"
    },
    "Broadcom": {
        "domains": ["broadcom.com"],
        "emails": ["careers@broadcom.com"],
        "notes": "Broadcom AI/ML internships"
    },
    "Spotify": {
        "domains": ["spotify.com"],
        "emails": ["careers@spotify.com", "talent@spotify.com"],
        "notes": "Spotify ML internships"
    },
    "Zoom": {
        "domains": ["zoom.us"],
        "emails": ["careers@zoom.us"],
        "notes": "Zoom AI/ML internships"
    },
    "Twilio": {
        "domains": ["twilio.com"],
        "emails": ["careers@twilio.com"],
        "notes": "Twilio AI/ML internships"
    },
    "Cloudflare": {
        "domains": ["cloudflare.com"],
        "emails": ["careers@cloudflare.com"],
        "notes": "Cloudflare AI/ML internships"
    },
    "CrowdStrike": {
        "domains": ["crowdstrike.com"],
        "emails": ["careers@crowdstrike.com"],
        "notes": "CrowdStrike AI/ML internships"
    },
    "Palo Alto Networks": {
        "domains": ["paloaltonetworks.com"],
        "emails": ["careers@paloaltonetworks.com"],
        "notes": "Palo Alto AI/ML internships in cybersecurity"
    },
    "VMware (Broadcom)": {
        "domains": ["vmware.com"],
        "emails": ["careers@vmware.com"],
        "notes": "VMware AI/ML infrastructure internships"
    },
    "SAP": {
        "domains": ["sap.com"],
        "emails": ["careers@sap.com", "talent@sap.com"],
        "notes": "SAP AI/ML internships"
    },
    "MongoDB": {
        "domains": ["mongodb.com"],
        "emails": ["careers@mongodb.com"],
        "notes": "MongoDB AI/ML internships"
    },
    "Datadog": {
        "domains": ["datadoghq.com"],
        "emails": ["careers@datadoghq.com"],
        "notes": "Datadog ML/platform internships"
    },
    "HP Inc": {
        "domains": ["hp.com"],
        "emails": ["careers@hp.com"],
        "notes": "HP AI/ML internships"
    },
    "Dell Technologies": {
        "domains": ["dell.com"],
        "emails": ["careers@dell.com", "talent@dell.com"],
        "notes": "Dell AI/ML internships"
    },
    "Micron Technology": {
        "domains": ["micron.com"],
        "emails": ["careers@micron.com"],
        "notes": "Micron AI/ML internships"
    },
    "Texas Instruments": {
        "domains": ["ti.com"],
        "emails": ["careers@ti.com"],
        "notes": "Texas Instruments AI/ML internships"
    },

    # ── FINANCE / BANKING ──
    "JPMorgan Chase": {
        "domains": ["jpmorgan.com", "jpmchase.com"],
        "emails": ["careers@jpmorgan.com", "jpmc.careers@jpmorgan.com", "talent@jpmorgan.com"],
        "notes": "JPMorgan AI/ML internships in fintech"
    },
    "Goldman Sachs": {
        "domains": ["goldmansachs.com"],
        "emails": ["careers@goldmansachs.com", "campus.recruitment@gs.com"],
        "notes": "Goldman Sachs AI/ML engineering internships"
    },
    "Morgan Stanley": {
        "domains": ["morganstanley.com"],
        "emails": ["careers@morganstanley.com", "campus.recruit@morganstanley.com"],
        "notes": "Morgan Stanley AI/ML internships"
    },
    "BlackRock": {
        "domains": ["blackrock.com"],
        "emails": ["careers@blackrock.com", "talent@blackrock.com"],
        "notes": "BlackRock AI/ML internships"
    },
    "Citigroup": {
        "domains": ["citigroup.com", "citi.com"],
        "emails": ["careers@citi.com", "talent@citi.com"],
        "notes": "Citi AI/ML internships"
    },
    "Bank of America": {
        "domains": ["bankofamerica.com", "bofa.com"],
        "emails": ["campusrecruiting@bankofamerica.com", "careers@bankofamerica.com"],
        "notes": "BofA AI/ML internships"
    },
    "Wells Fargo": {
        "domains": ["wellsfargo.com"],
        "emails": ["careers@wellsfargo.com"],
        "notes": "Wells Fargo AI/ML internships"
    },
    "American Express": {
        "domains": ["americanexpress.com"],
        "emails": ["careers@aexp.com", "talent@americanexpress.com"],
        "notes": "Amex AI/ML internships"
    },
    "Capital One": {
        "domains": ["capitalone.com"],
        "emails": ["careers@capitalone.com", "talent@capitalone.com"],
        "notes": "Capital One AI/ML internships in fintech"
    },
    "Mastercard": {
        "domains": ["mastercard.com"],
        "emails": ["careers@mastercard.com", "talent@mastercard.com"],
        "notes": "Mastercard AI/ML internships"
    },
    "Visa": {
        "domains": ["visa.com"],
        "emails": ["careers@visa.com", "talent@visa.com"],
        "notes": "Visa AI/ML internships"
    },
    "PayPal": {
        "domains": ["paypal.com"],
        "emails": ["careers@paypal.com", "talent@paypal.com"],
        "notes": "PayPal AI/ML internships"
    },
    "Stripe": {
        "domains": ["stripe.com"],
        "emails": ["careers@stripe.com"],
        "notes": "Stripe ML/AI internships"
    },

    # ── CONSULTING ──
    "McKinsey & Company": {
        "domains": ["mckinsey.com"],
        "emails": ["careers@mckinsey.com", "talent@mckinsey.com"],
        "notes": "McKinsey AI/QuantumBlack internships"
    },
    "Boston Consulting Group": {
        "domains": ["bcg.com"],
        "emails": ["careers@bcg.com", "talent@bcg.com"],
        "notes": "BCG X (AI/tech) internships"
    },
    "Bain & Company": {
        "domains": ["bain.com"],
        "emails": ["careers@bain.com", "talent@bain.com"],
        "notes": "Bain AI/ML internships"
    },
    "Deloitte": {
        "domains": ["deloitte.com"],
        "emails": ["careers@deloitte.com", "talent@deloitte.com"],
        "notes": "Deloitte AI Institute internships"
    },
    "Accenture": {
        "domains": ["accenture.com"],
        "emails": ["careers@accenture.com", "talent@accenture.com"],
        "notes": "Accenture AI/ML internships"
    },
    "PwC": {
        "domains": ["pwc.com"],
        "emails": ["careers@pwC.com", "talent@pwc.com"],
        "notes": "PwC AI/ML & data internships"
    },
    "EY (Ernst & Young)": {
        "domains": ["ey.com"],
        "emails": ["careers@ey.com", "talent@ey.com"],
        "notes": "EY AI/ML internships"
    },
    "KPMG": {
        "domains": ["kpmg.com"],
        "emails": ["careers@kpmg.com", "talent@kpmg.com"],
        "notes": "KPMG AI/ML internships"
    },

    # ── E-COMMERCE / RETAIL ──
    "Walmart": {
        "domains": ["walmart.com"],
        "emails": ["careers@wal-mart.com", "talent@walmart.com"],
        "notes": "Walmart Global Tech AI/ML internships"
    },
    "Shopify": {
        "domains": ["shopify.com"],
        "emails": ["careers@shopify.com"],
        "notes": "Shopify ML/AI internships"
    },
    "eBay": {
        "domains": ["ebay.com"],
        "emails": ["careers@ebay.com"],
        "notes": "eBay AI/ML internships"
    },

    # ── LOGISTICS / TRANSPORT ──
    "DP World": {
        "domains": ["dpworld.com"],
        "emails": ["careers@dpworld.com", "talent@dpworld.com"],
        "notes": "DP World AI/ML internships in logistics"
    },
    "FedEx": {
        "domains": ["fedEx.com"],
        "emails": ["careers@fedEx.com", "talent@fedex.com"],
        "notes": "FedEx AI/ML logistics internships"
    },
    "UPS": {
        "domains": ["ups.com"],
        "emails": ["careers@ups.com"],
        "notes": "UPS AI/ML logistics internships"
    },

    # ── HEALTHCARE / PHARMA ──
    "Johnson & Johnson": {
        "domains": ["jnj.com"],
        "emails": ["careers@jnj.com", "talent@jnj.com"],
        "notes": "J&J AI/ML internships in healthcare"
    },
    "Pfizer": {
        "domains": ["pfizer.com"],
        "emails": ["careers@pfizer.com", "talent@pfizer.com"],
        "notes": "Pfizer AI/ML internships"
    },
    "Moderna": {
        "domains": ["modernatx.com"],
        "emails": ["careers@modernatx.com", "talent@modernatx.com"],
        "notes": "Moderna AI/ML internships"
    },
    "Merck": {
        "domains": ["merck.com"],
        "emails": ["careers@merck.com"],
        "notes": "Merck AI/ML internships"
    },
    "AbbVie": {
        "domains": ["abbvie.com"],
        "emails": ["careers@abbvie.com"],
        "notes": "AbbVie AI/ML internships"

    },

    # ── AUTOMOTIVE ──
     "Toyota": {
        "domains": ["toyota.com", "toyota-industries.com"],
        "emails": ["careers@toyota.com", "talent@toyota.com"],
        "notes": "Toyota AI/ML & autonomous driving internships"
    },
    "Mercedes-Benz": {
        "domains": ["mercedes-benz.com", "daimler.com"],
        "emails": ["careers@mercedes-benz.com"],
        "notes": "Mercedes AI/ML internships"
    },
    "BMW": {
        "domains": ["bmw.com"],
        "emails": ["careers@bmw.com"],
        "notes": "BMW AI/ML internships"
    },
    "Ford Motor": {
        "domains": ["ford.com"],
        "emails": ["careers@ford.com", "talent@ford.com"],
        "notes": "Ford AI/ML internships"
    },
    "General Motors": {
        "domains": ["gm.com"],
        "emails": ["careers@gm.com", "talent@gm.com"],
        "notes": "GM AI/ML & autonomous vehicle internships"
    },
    "Honda": {
        "domains": ["honda.com"],
        "emails": ["careers@honda.com"],
        "notes": "Honda AI/ML internships"
    },
    "Hyundai": {
        "domains": ["hyundai.com"],
        "emails": ["careers@hyundai.com"],
        "notes": "Hyundai AI/ML internships"
    },

    # ── ENERGY ──
    "Shell": {
        "domains": ["shell.com"],
        "emails": ["careers@shell.com", "talent@shell.com"],
        "notes": "Shell AI/ML internships"
    },
    "ExxonMobil": {
        "domains": ["exxonmobil.com"],
        "emails": ["careers@exxonmobil.com"],
        "notes": "ExxonMobil AI/ML internships"
    },
    "Chevron": {
        "domains": ["chevron.com"],
        "emails": ["careers@chevron.com"],
        "notes": "Chevron AI/ML internships"
    },
    "BP": {
        "domains": ["bp.com"],
        "emails": ["careers@bp.com"],
        "notes": "BP AI/ML internships"
    },
    "TotalEnergies": {
        "domains": ["totalenergies.com"],
        "emails": ["careers@totalenergies.com"],
        "notes": "TotalEnergies AI/ML internships"
    },

    # ── INDUSTRIAL / DEFENSE ──
    "Siemens": {
        "domains": ["siemens.com"],
        "emails": ["careers@siemens.com", "talent@siemens.com"],
        "notes": "Siemens AI/ML internships"
    },
    "General Electric": {
        "domains": ["ge.com"],
        "emails": ["careers@ge.com"],
        "notes": "GE AI/ML internships"
    },
    "Honeywell": {
        "domains": ["honeywell.com"],
        "emails": ["careers@honeywell.com"],
        "notes": "Honeywell AI/ML internships"
    },
    "3M": {
        "domains": ["3m.com"],
        "emails": ["careers@3m.com"],
        "notes": "3M AI/ML internships"
    },
    "Boeing": {
        "domains": ["boeing.com"],
        "emails": ["careers@boeing.com", "talent@boeing.com"],
        "notes": "Boeing AI/ML internships"
    },
    "Lockheed Martin": {
        "domains": ["lockheedmartin.com"],
        "emails": ["careers@lockheedmartin.com"],
        "notes": "Lockheed Martin AI/ML internships"
    },
    "Northrop Grumman": {
        "domains": ["northropgrumman.com"],
        "emails": ["careers@northropgrumman.com"],
        "notes": "Northrop Grumman AI/ML internships"
    },
    "RTX (Raytheon)": {
        "domains": ["rtx.com"],
        "emails": ["careers@rtx.com"],
        "notes": "RTX AI/ML internships"
    },
    "Caterpillar": {
        "domains": ["cat.com"],
        "emails": ["careers@cat.com"],
        "notes": "Caterpillar AI/ML internships"
    },
    "John Deere": {
        "domains": ["deere.com"],
        "emails": ["careers@johndeere.com", "talent@johndeere.com"],
        "notes": "Deere AI/ML internships"
    },

    # ── CPG / CONSUMER ──
    "Procter & Gamble": {
        "domains": ["pg.com"],
        "emails": ["careers.im@pg.com", "talent@pg.com"],
        "notes": "P&G AI/ML internships"
    },
    "Unilever": {
        "domains": ["unilever.com"],
        "emails": ["careers@unilever.com"],
        "notes": "Unilever AI/ML internships"
    },
    "Coca-Cola": {
        "domains": ["coca-cola.com"],
        "emails": ["careers@coca-cola.com"],
        "notes": "Coca-Cola AI/ML internships"
    },
    "PepsiCo": {
        "domains": ["pepsico.com"],
        "emails": ["careers@pepsico.com"],
        "notes": "PepsiCo AI/ML internships"
    },
    "Nike": {
        "domains": ["nike.com"],
        "emails": ["careers@nike.com", "talent@nike.com"],
        "notes": "Nike AI/ML internships"
    },
    "Nestlé": {
        "domains": ["nestle.com"],
        "emails": ["careers@nestle.com"],
        "notes": "Nestlé AI/ML internships"
    },

    # ── INDIAN TECH / IT MNCs ──
    "Tata Consultancy Services (TCS)": {
        "domains": ["tcs.com"],
        "emails": ["careers@tcs.com"],
        "notes": "TCS AI/ML internships"
    },
    "Infosys": {
        "domains": ["infosys.com"],
        "emails": ["careers@infosys.com", "talent@infosys.com"],
        "notes": "Infosys AI/ML internships"
    },
    "Wipro": {
        "domains": ["wipro.com"],
        "emails": ["careers@wipro.com"],
        "notes": "Wipro AI/ML internships"
    },
    "HCL Technologies": {
        "domains": ["hcltech.com"],
        "emails": ["careers@hcltech.com"],
        "notes": "HCL AI/ML internships"
    },
    "Tech Mahindra": {
        "domains": ["techmahindra.com"],
        "emails": ["careers@techmahindra.com"],
        "notes": "Tech Mahindra AI/ML internships"
    },
    "Reliance Industries (Jio)": {
        "domains": ["ril.com", "jio.com"],
        "emails": ["careers@ril.com", "talent@ril.com"],
        "notes": "Reliance Jio AI/ML internships"
    },
    "Tata Group": {
        "domains": ["tata.com"],
        "emails": ["careers@tata.com"],
        "notes": "Tata Group AI/ML internships"
    },
    "Samsung": {
        "domains": ["samsung.com"],
        "emails": ["careers@samsung.com", "talent@samsung.com"],
        "notes": "Samsung AI/ML internships"
    },
    "Sony": {
        "domains": ["sony.com"],
        "emails": ["careers@sony.com"],
        "notes": "Sony AI/ML internships"
    },

    # ── ADDITIONAL TOP TECH ──
    "Cohere": {
        "domains": ["cohere.com"],
        "emails": ["careers@cohere.com"],
        "notes": "Cohere AI/LLM internships"
    },
    "Anthropic": {
        "domains": ["anthropic.com"],
        "emails": ["careers@anthropic.com"],
        "notes": "Anthropic AI safety & research internships"
    },
    "Scale AI": {
        "domains": ["scale.com"],
        "emails": ["careers@scale.com"],
        "notes": "Scale AI data & ML internships"
    },
    "Hugging Face": {
        "domains": ["huggingface.co"],
        "emails": ["careers@huggingface.co"],
        "notes": "Hugging Face ML/AI internships"
    },
    "C3.ai": {
        "domains": ["c3.ai"],
        "emails": ["careers@c3.ai"],
        "notes": "C3.ai enterprise AI internships"
    },
    "Mistral AI": {
        "domains": ["mistral.ai"],
        "emails": ["careers@mistral.ai"],
        "notes": "Mistral AI research internships"
    },
    "Stability AI": {
        "domains": ["stability.ai"],
        "emails": ["careers@stability.ai"],
        "notes": "Stability AI generative model internships"
    },
    "Block (Square)": {
        "domains": ["block.xyz", "squareup.com"],
        "emails": ["careers@block.xyz", "talent@squareup.com"],
        "notes": "Block AI/ML fintech internships"
    },
    "Robinhood": {
        "domains": ["robinhood.com"],
        "emails": ["careers@robinhood.com"],
        "notes": "Robinhood AI/ML internships"
    },
    "Coinbase": {
        "domains": ["coinbase.com"],
        "emails": ["careers@coinbase.com"],
        "notes": "Coinbase AI/ML internships in crypto"
    },
    "Rippling": {
        "domains": ["rippling.com"],
        "emails": ["careers@rippling.com"],
        "notes": "Rippling AI/ML internships"
    },
    "Notion": {
        "domains": ["notion.so", "makenotion.com"],
        "emails": ["careers@makenotion.com", "talent@notion.so"],
        "notes": "Notion AI/ML internships"
    },
    "Figma": {
        "domains": ["figma.com"],
        "emails": ["careers@figma.com"],
        "notes": "Figma AI/ML internships"
    },
    "Canva": {
        "domains": ["canva.com"],
        "emails": ["careers@canva.com"],
        "notes": "Canva AI/ML internships"
    },
    "Siemens Healthineers": {
        "domains": ["siemens-healthineers.com"],
        "emails": ["careers@siemens-healthineers.com"],
        "notes": "Siemens Healthineers AI/ML internships"
    },
    "Electronic Arts": {
        "domains": ["ea.com"],
        "emails": ["careers@ea.com"],
        "notes": "EA AI/ML internships in gaming"
    },
    "Unity Technologies": {
        "domains": ["unity3d.com", "unity.com"],
        "emails": ["careers@unity.com"],
        "notes": "Unity AI/ML internships"
    },
}


def create_email_body(company_name, hr_name=None):
    """Create personalized cold email body."""
    name_greeting = f"Hi {hr_name}," if hr_name else f"Hi {company_name} Recruitment Team,"

    body = f"""
{name_greeting}

I'm an AI/ML Engineering student (B.Tech, 8.5 CGPA) and I'd love to intern at {company_name}.

Quick highlights:
• Won 2 national hackathons (1st Place out of 600+ & 1st Runner-Up 2x out of 800+ teams)
• Published IEEE first-author paper at ICCTWC 2026
• 50+ merged PRs to Google, Microsoft, Apache, Hedera Hashgraph
• GDG AI/ML Lead mentoring 200+ students
• Built 3 production AI products (cybersecurity, observability, legal NLP)
• 366+ LeetCode problems solved

Tech stack: PyTorch, HuggingFace, LangChain, FastAPI, Docker, PostgreSQL, Redis.

My resume is attached — I'd love a quick chat if there's a fit.

Best,
Aditya Shirsatrao
adityashirsatrao007@gmail.com | +91-7387-384655
linkedin.com/in/adityashirsatrao
"""

    return body.strip()


def send_email(smtp_conn, to_email, company_name, hr_name=None):
    """Send a single cold email with resume attachment."""
    msg = MIMEMultipart()
    msg["From"] = SMTP_FROM
    msg["To"] = to_email
    msg["Subject"] = f"AI/ML Internship Application - Aditya Shirsatrao ({company_name})"

    body = create_email_body(company_name, hr_name)
    msg.attach(MIMEText(body, "plain"))

    # Attach resume
    try:
        with open(RESUME_PATH, "rb") as attachment:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(attachment.read())
            encoders.encode_base64(part)
            part.add_header(
                "Content-Disposition",
                f"attachment; filename=Aditya_Shirsatrao_AI_ML_Resume.pdf",
            )
            msg.attach(part)
    except FileNotFoundError:
        logging.warning(f"Resume file not found, sending without attachment")

    try:
        smtp_conn.sendmail(SMTP_FROM, to_email, msg.as_string())
        return True
    except Exception as e:
        logging.error(f"Failed to send to {to_email}: {str(e)}")
        return False


def main():
    logging.info("=" * 60)
    logging.info("COLD EMAIL AUTOMATION STARTED")
    logging.info(f"Total companies in database: {len(COMPANIES)}")
    logging.info(f"Resume: {RESUME_PATH}")
    logging.info("=" * 60)

    # Connect to SMTP
    logging.info("Connecting to Gmail SMTP...")
    context = ssl.create_default_context()
    smtp_conn = smtplib.SMTP(SMTP_HOST, SMTP_PORT)
    smtp_conn.starttls(context=context)
    smtp_conn.login(SMTP_USER, SMTP_PASS)
    logging.info("Connected to SMTP successfully!")

    results = {
        "sent": [],
        "failed": [],
        "total_emails": 0,
    }

    company_list = list(COMPANIES.items())
    random.shuffle(company_list)

    for idx, (company_name, info) in enumerate(company_list, 1):
        emails = info["emails"]
        notes = info.get("notes", "")

        logging.info(f"\n[{idx}/{len(company_list)}] {company_name}")
        logging.info(f"  Notes: {notes}")

        for email in emails:
            logging.info(f"  → Sending to {email}...")
            success = send_email(smtp_conn, email, company_name)

            if success:
                results["sent"].append({"company": company_name, "email": email})
                logging.info(f"    ✓ Sent successfully!")
            else:
                results["failed"].append({"company": company_name, "email": email})
                logging.info(f"    ✗ Failed!")

            results["total_emails"] += 1

            # Rate limiting: 5-15 seconds between each email
            delay = random.uniform(8, 20)
            logging.info(f"  Waiting {delay:.1f}s to avoid rate limits...")
            time.sleep(delay)

        # Extra delay between companies
        if idx % 5 == 0 and idx < len(company_list):
            extra_delay = random.uniform(30, 60)
            logging.info(f"\n--- Batch {idx//5} complete. Cooling down for {extra_delay:.0f}s ---")
            time.sleep(extra_delay)

    smtp_conn.quit()

    # ─── SUMMARY ───
    logging.info("\n" + "=" * 60)
    logging.info("FINAL SUMMARY")
    logging.info("=" * 60)
    logging.info(f"Total companies targeted: {len(COMPANIES)}")
    logging.info(f"Total emails sent: {results['total_emails']}")
    logging.info(f"Successful: {len(results['sent'])}")
    logging.info(f"Failed: {len(results['failed'])}")

    # Save results
    report = {
        "timestamp": datetime.now().isoformat(),
        "summary": {
            "companies": len(COMPANIES),
            "total_emails": results["total_emails"],
            "successful": len(results["sent"]),
            "failed": len(results["failed"]),
        },
        "sent": results["sent"],
        "failed": results["failed"],
        "company_details": {
            name: info["emails"]
            for name, info in COMPANIES.items()
        }
    }

    report_path = LOG_DIR / "email_report.json"
    with open(report_path, "w") as f:
        json.dump(report, f, indent=2)

    logging.info(f"\nFull report saved to: {report_path}")
    logging.info("COLD EMAIL AUTOMATION COMPLETE!")


if __name__ == "__main__":
    main()
