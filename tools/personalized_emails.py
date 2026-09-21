#!/usr/bin/env python3
"""
Personalized cold emails — fresher referral template (Guidance + Referral).
71 entries. Style: <130 words, product-specific, resume attached, referral ask.
Template: Fresher Cold Email Template 2 (Guidance + Referral).
"""

import smtplib
import ssl
import time
import random
import json
import logging
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from pathlib import Path

SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 587
SMTP_USER = os.environ.get("SMTP_USER", "")
SMTP_PASS = os.environ.get("SMTP_PASS", "")
SMTP_FROM = os.environ.get("SMTP_FROM", SMTP_USER)
LOG_DIR = Path("/tmp/cold_email_logs")
LOG_DIR.mkdir(exist_ok=True)
RESUME_PATH = Path("/tmp/resume.pdf")

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.FileHandler(LOG_DIR / "personalized_log.txt"), logging.StreamHandler()])

# (company, email, hr_name, product_label, product_hook)
DATA = [
    ("Google", "yaanchal@google.com", "Yaanchal", "Gemini AI & TensorFlow", "Gemini's multimodal capabilities are pushing the boundaries of what AI can do"),
    ("Google", "smritiverma@google.com", "Smritiverma", "Gemini AI & TensorFlow", "Gemini's multimodal capabilities are pushing the boundaries of what AI can do"),
    ("Microsoft", "rshashank@microsoft.com", "Rshashank", "Azure AI & Copilot", "Copilot stack and Azure AI services are redefining developer productivity"),
    ("Amazon", "s.n@amazon.com", "S N", "AWS AI & Alexa", "Alexa AI and SageMaker are what drew me to production ML at scale"),
    ("Apple", "reshma_kk@apple.com", "Reshma KK", "Apple Intelligence & Core ML", "Apple Intelligence and on-device ML with Core ML align perfectly with my interest in efficient AI"),
    ("Nvidia", "mohammednabe@nvidia.com", "Mohammednabe", "CUDA & GPU-AI", "CUDA ecosystem and GPU-accelerated ML are at the heart of everything I build in deep learning"),
    ("Salesforce", "aman.verma@salesforce.com", "Aman Verma", "Einstein AI", "Einstein AI platform is transforming how businesses leverage predictive analytics"),
    ("LinkedIn", "shjacob@linkedin.com", "Shjacob", "AI feed ranking & recommendations", "recommendation systems and AI-powered hiring tools are a fascinating applied ML challenge"),
    ("Atlassian", "vpandiyan@atlassian.com", "Vpandiyan", "Atlassian Intelligence", "push into AI-powered project intelligence is reshaping team collaboration"),
    ("Workday", "rucha.verma@workday.com", "Rucha Verma", "Workday AI & ML for HR", "ML-driven workforce planning and AI features in HCM are pioneering HR tech"),
    ("Red Hat", "broutray@redhat.com", "Broutray", "OpenShift AI", "OpenShift AI platform for MLOps at enterprise level is exactly the kind of infra I want to work on"),
    ("Coursera", "nkhatter@coursera.org", "Nkhatter", "AI-powered learning recommendations", "ML-driven content recommendations and AI grading systems are transforming edtech"),
    ("Pure Storage", "amogaveera@purestorage.com", "Amogaveera", "AI-ready storage infrastructure", "AI-enabled data infrastructure is critical infrastructure for ML pipelines"),
    ("Nike", "arivoli.sampathkumar@nike.com", "Arivoli Sampathkumar", "AI personalization & fitness", "AI-driven personalization and fitness recommendations combine ML with great user experience"),
    ("TCS", "venkatesh.kadirvel@tcs.com", "Venkatesh Kadirvel", "TCS AI/ML Practice", "investments in AI/ML solutions for enterprise digital transformation are impressive in scale"),
    ("HCL", "shwetang_shukla@hcl.com", "Shwetang Shukla", "HCL AI & ML Solutions", "AI/ML practice and DRYiCE platform for intelligent automation are industry-leading"),
    ("Deloitte", "sosneh@deloitte.com", "Sosneh", "Deloitte AI Institute", "AI Institute and applied ML consulting for enterprises align with my product-building background"),
    ("KPMG", "sr@kpmg.com", "KPMG", "KPMG AI & Data Science", "AI-driven audit analytics and data science practice are at the intersection of ML and business"),
    ("McKinsey", "prateek_taneja@mckinsey.com", "Prateek Taneja", "QuantumBlack", "QuantumBlack's AI-first approach to management consulting is exactly where I want to build my career"),
    ("Visa", "gorajend@visa.com", "Gorajend", "AI fraud detection & payments", "ML-powered fraud detection systems processing billions of transactions are a pinnacle of applied AI"),
    ("Citi Bank", "jyoti.mehta@citi.com", "Jyoti Mehta", "AI banking intelligence", "AI initiatives in fraud detection and personalized banking are transforming financial services"),
    ("IDFC First Bank", "aftin.paul@idfcfirstbank.com", "Aftin Paul", "AI digital banking", "digital-first banking approach with AI-driven customer insights is truly innovative"),
    ("SAP Labs", "a.khandelwal@sap.com", "A Khandelwal", "SAP Business AI & BTP", "Business AI platform integrated with enterprise workflows is an exciting applied ML space"),
    ("ValueLabs", "nagarani.racharla@valuelabs.com", "Nagarani Racharla", "AI-first software development", "focus on AI-powered software engineering aligns with my production ML background"),
    ("Barclays", "himali.gaikwad@barclays.com", "Himali Gaikwad", "AI risk & trading", "AI applications in risk management and algorithmic trading are cutting-edge in finance"),
    ("Ford", "jparmar@ford.com", "Jparmar", "AI autonomous & mobility", "AI work in autonomous driving and predictive maintenance is pushing automotive ML forward"),
    ("Godrej Capital", "deeya.kochhar@dmifinance.in", "Deeya Kochhar", "AI-driven lending & credit", "tech-first approach to lending with AI-powered credit assessment is an exciting space"),
    ("Upstox", "jeevan.kurian@upstox.com", "Jeevan Kurian", "AI-powered trading platform", "ML-driven market insights and personalized trading recommendations are transforming retail investing"),
    ("Groww", "mamatha.cg@groww.in", "Mamatha CG", "AI investment recommendations", "AI-powered mutual fund and investment recommendations are making smart investing accessible"),
    ("Groww", "nisha.tandon@groww.in", "Nisha Tandon", "AI investment recommendations", "AI-powered mutual fund and investment recommendations are making smart investing accessible"),
    ("Cashkaro", "sumi@cashkaro.com", "Sumi", "AI cashback & deals engine", "recommendation engine for deals and cashback is an interesting applied ML problem"),
    ("KreditBee", "poulomi.patra@kreditbee.in", "Poulomi Patra", "AI lending & credit scoring", "ML-first approach to credit assessment and digital lending is reshaping fintech in India"),
    ("Money View", "richa.ranjan@moneyview.in", "Richa Ranjan", "AI credit scoring & lending", "AI-driven credit scoring and personalized loan products are innovative in Indian fintech"),
    ("Moneyview", "roopna.puthiyedath@moneyview.in", "Roopna Puthiyedath", "AI financial insights", "ML-powered financial health insights are helping millions manage money better"),
    ("Fibe", "tejashree.deote@fibe.in", "Tejashree Deote", "AI-powered lending platform", "AI-first credit assessment platform is making lending faster and more inclusive"),
    ("DMI Finance", "deeya.kochhar@dmifinance.in", "Deeya Kochhar", "AI credit risk & lending", "ML-driven credit risk models power inclusive lending at scale in India"),
    ("Motilal Oswal", "priyanka.p@motilaloswal.com", "Priyanka P", "AI wealth management", "AI-powered investment advisory and portfolio management are leading in Indian wealth tech"),
    ("Pagaya", "rohit@pagaya.com", "Rohit", "AI credit & lending infrastructure", "AI-powered credit decisioning infrastructure is fascinating — using ML to expand credit access globally"),
    ("Cashfree Payments", "sunitha@cashfree.com", "Sunitha", "AI payment orchestration", "ML-powered payment routing and fraud detection handle millions of transactions daily"),
    ("Simpl", "ayesha.siddiqua@getsimpl.com", "Ayesha Siddiqua", "AI BNPL & credit", "ML-driven credit underwriting and buy-now-pay-later platform are transforming digital commerce"),
    ("Jar", "snehal@changejar.in", "Snehal", "AI micro-savings & investments", "AI-powered micro-investment recommendations are making saving accessible to millions"),
    ("Slice", "neetika.thakur@sliceit.com", "Neetika Thakur", "AI credit cards & lending", "ML-first credit card platform is redefining how young India accesses credit"),
    ("Stock Edge", "pradipta@stockedge.com", "Pradipta", "AI stock research & analytics", "ML-powered stock analysis and research tools are empowering retail investors"),
    ("Rupeek", "mohd.akhter@rupeek.com", "Mohd Akhter", "AI gold loans & lending", "tech-driven gold loan platform using AI for valuation and risk is an innovative fintech model"),
    ("PagarBook", "shivani.sharma@pagarbook.com", "Shivani Sharma", "AI business accounting", "ML-powered bookkeeping and business insights are digitizing India's small businesses"),
    ("Uni", "aayushi.sharma@uni.club", "Aayushi Sharma", "AI credit card platform", "AI-driven credit card and pay-later platform is creating smart credit products for India"),
    ("Uni", "prateek@uni.club", "Prateek", "AI credit card platform", "AI-driven credit card and pay-later platform is creating smart credit products for India"),
    ("Fi (Epifi)", "maithreyi@epifi.com", "Maithreyi", "AI neobanking platform", "ML-powered spending insights and savings recommendations are redefining digital banking"),
    ("Jupiter", "waseem.shariff@jupiter.money", "Waseem Shariff", "AI personal finance", "AI-driven financial management and smart savings features are building the future of neobanking"),
    ("HappyLocate", "shiwangip@happylocate.com", "Shiwangip", "AI relocation & logistics", "AI-powered relocation platform is solving complex logistics with technology"),
    ("Flobiz", "sukant.singh@flobiz.in", "Sukant Singh", "AI business management", "AI-driven business management platform is digitizing India's SMBs with smart automation"),
    ("Ditto", "deepa@joinditto.in", "Deepa", "AI insurance advisory", "AI-powered insurance advisory platform is simplifying insurance decisions for millions"),
    ("CoinDCX", "shweta.singh@coindcx.com", "Shweta Singh", "AI crypto exchange", "ML-powered trading engine and crypto analytics are the backbone of India's crypto ecosystem"),
    ("WazirX", "raily.g@wazirx.com", "Raily G", "AI crypto trading", "AI-driven trading platform and market insights are leading India's crypto adoption"),
    ("Zomato", "ananya.jain@zomato.com", "Ananya Jain", "AI food recommendations & delivery", "ML-powered food recommendations and delivery optimization serve millions daily"),
    ("Swiggy", "priti.patil_ch@external.swiggy.in", "Priti Patil", "AI delivery & recommendations", "AI-driven delivery logistics and personalized recommendations are best-in-class in food tech"),
    ("Swiggy", "girish.menon@swiggy.in", "Girish Menon", "AI delivery & recommendations", "AI-driven delivery logistics and personalized recommendations are best-in-class in food tech"),
    ("Blinkit", "shruti.anand@blinkit.com", "Shruti Anand", "AI quick commerce", "ML-driven inventory planning and instant delivery logistics are redefining quick commerce"),
    ("Lenskart", "nirbhay.gaur@lenskart.com", "Nirbhay Gaur", "AI eyewear try-on & recommendations", "AI-powered virtual try-on and recommendation engine are transforming eyewear shopping"),
    ("Delhivery", "dalima.gupta@delhivery.com", "Dalima Gupta", "AI logistics & supply chain", "ML-driven logistics optimization and supply chain intelligence power India's e-commerce backbone"),
    ("Acko", "diptiranjan.pradhan@acko.tech", "Diptiranjan Pradhan", "AI insurance", "digital-first, AI-powered insurance platform is making insurance paperless and instant"),
    ("Spinny", "harsh.satija@spinny.com", "Harsh Satija", "AI car buying platform", "AI-driven car inspection and pricing platform is bringing trust to India's used car market"),
    ("PetPooja", "aman.jobanputra@petpooja.com", "Aman Jobanputra", "AI pet care platform", "AI-powered pet care and vet services platform is an innovative pet-tech startup"),
    ("CoinSwitch", "nupur@coinswitch.co", "Nupur", "AI crypto investment", "ML-powered crypto insights and investment platform make crypto accessible to millions"),
    ("Zypp", "jyotsana.singh@zypp.app", "Jyotsana Singh", "AI EV fleet management", "AI-driven EV fleet management and logistics optimization are powering sustainable last-mile delivery"),
    ("Khatabook", "shivani.bareja@khatabook.com", "Shivani Bareja", "AI bookkeeping for SMBs", "ML-powered bookkeeping and business insights are digitizing India's small retailers"),
    ("Astuto.ai", "rajni@astuto.ai", "Rajni", "AI product analytics", "AI-driven product intelligence is a fascinating space in the AI-product-market fit world"),
    ("Unifize", "sakshi.sethia@unifize.com", "Sakshi Sethia", "AI-powered SaaS collaboration", "AI-enhanced collaboration platform for quality management is an interesting SaaS + AI play"),
    ("Jupiter AI Labs", "aishwarya@juppiterailabs.com", "Aishwarya", "AI research & applied ML", "applied ML research across domains is exactly the kind of innovation lab I want to be part of"),
    ("Khatabook", "apurva.shetty@khata.book", "Apurva Shetty", "AI ledger for small businesses", "ML-driven ledger and credit solutions for India's small businesses are digitizing the informal economy"),
    ("VyaparApp", "satpaalsingh@vyaparapp.in", "Satpaalsingh", "AI business management for SMBs", "AI-driven invoicing and business management tools are empowering India's micro-businesses"),
]

def build_email(company, hr_name, product_label, product_hook):
    subject = f"Application \u2014 Remote AI/ML Intern \u2014 {company}"
    greeting = hr_name if hr_name != company else f"{company} Team"
    body = f"""Dear {greeting},

I hope you're doing well. I'm an AI/ML Engineering student at Orchid College of Engineering and Technology, actively building projects in deep learning, MLOps, and production ML systems.

I came across {company}'s work in {product_label} \u2014 {product_hook} \u2014 and I'm writing to express my interest in remote AI/ML internship opportunities at {company}. I've attached my resume for your reference.

I would greatly appreciate it if you could consider my profile for any suitable remote internship positions.

Thank you for your time and consideration.

Best regards,
Aditya Shirsatrao
adityashirsatrao007@gmail.com
linkedin.com/in/adityashirsatrao"""
    return subject, body


def send_email(smtp_conn, to_email, subject, body):
    msg = MIMEMultipart()
    msg["From"] = SMTP_FROM
    msg["To"] = to_email
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))
    if RESUME_PATH.exists():
        with open(RESUME_PATH, "rb") as f:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(f.read())
        encoders.encode_base64(part)
        part.add_header("Content-Disposition", f'attachment; filename="{RESUME_PATH.name}"')
        msg.attach(part)
    try:
        smtp_conn.sendmail(SMTP_FROM, to_email, msg.as_string())
        return True
    except Exception as e:
        logging.error(f"Failed: {str(e)}")
        return False

def main():
    import argparse
    parser = argparse.ArgumentParser(description="Personalized cold email sender")
    parser.add_argument("--send", action="store_true", help="Send via SMTP")
    parser.add_argument("--preview", action="store_true", default=True, help="Preview (default)")
    parser.add_argument("--company", help="Filter by company name")
    parser.add_argument("--list", action="store_true", help="List all entries")
    parser.add_argument("--limit", type=int, help="Max emails to send")
    parser.add_argument("--offset", type=int, default=0, help="Skip first N entries")
    args = parser.parse_args()

    entries = []
    for c, e, h, pl, ph in DATA:
        subject, body = build_email(c, h, pl, ph)
        entries.append({"company": c, "email": e, "hr_name": h, "subject": subject, "body": body})

    if args.company:
        q = args.company.lower()
        entries = [e for e in entries if q in e["company"].lower()]
        if not entries:
            print(f"No matches for '{args.company}'")
            return

    if args.list:
        for i, e in enumerate(entries, 1):
            print(f"{i:3d}. {e['company']:25s} {e['email']:35s} | {e['hr_name']}")
        return

    if args.offset:
        entries = entries[args.offset:]
    if args.limit:
        entries = entries[:args.limit]

    if args.send:
        logging.info("Connecting to SMTP...")
        context = ssl.create_default_context()
        smtp_conn = smtplib.SMTP(SMTP_HOST, SMTP_PORT)
        smtp_conn.starttls(context=context)
        smtp_conn.login(SMTP_USER, SMTP_PASS)
        logging.info("Connected!")
        results = {"sent": [], "failed": []}
        for entry in entries:
            logging.info(f"Sending to {entry['company']} ({entry['email']})...")
            ok = send_email(smtp_conn, entry["email"], entry["subject"], entry["body"])
            if ok:
                results["sent"].append(entry["company"])
                logging.info("  Sent")
            else:
                results["failed"].append(entry["company"])
                logging.info("  Failed")
            time.sleep(random.uniform(15, 25))
        smtp_conn.quit()
        logging.info(f"Done. Sent: {len(results['sent'])}, Failed: {len(results['failed'])}")
        with open(LOG_DIR / "report.json", "w") as f:
            json.dump(results, f, indent=2)
    else:
        for i, e in enumerate(entries, 1):
            print(f"\n{'='*60}")
            print(f"EMAIL {i}: {e['company']}")
            print(f"To: {e['email']}")
            print(f"Subject: {e['subject']}")
            print(f"{'='*60}")
            print(e['body'])
            wc = len(e['body'].split())
            print(f"\n[Word count: ~{wc}]")
        print(f"\n{'='*60}")
        print(f"Total: {len(entries)} email(s)")
        print("Run with --send to send via SMTP")
        print(f"{'='*60}")

if __name__ == "__main__":
    main()
