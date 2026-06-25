#!/usr/bin/env python3
"""
Google Docs updater for study question answers.
Dynamically resolves each question's endIndex from the live document
so insertion points are always correct.

Usage:
  python3 update_doc_content.py           # full run
  python3 update_doc_content.py --dry-run # preview only
  python3 update_doc_content.py --verify  # print doc structure
"""

import json
import os
import re
import sys
from pathlib import Path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = [
    "https://www.googleapis.com/auth/documents",
    "https://www.googleapis.com/auth/drive.file",
]

TOKEN_DIR = Path.home() / ".config" / "google-docs-notes"
TOKEN_PATH = TOKEN_DIR / "token.json"
CREDENTIALS_PATH = TOKEN_DIR / "credentials.json"

DOC_ID = "1pbcPNLSq1ZsLAaGKgE3U_F8C-qhTghXi0uCsbImB7vk"


def _get_services():
    if TOKEN_PATH.exists():
        creds = Credentials.from_authorized_user_file(str(TOKEN_PATH), SCOPES)
    else:
        creds = None

    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    elif not creds or not creds.valid:
        if not CREDENTIALS_PATH.exists():
            print(
                "No credentials.json found.\n"
                "  1. Go to https://console.cloud.google.com/apis/credentials\n"
                "  2. Enable Google Docs API + Google Drive API\n"
                "  3. Create OAuth 2.0 Client ID → Desktop app → Download JSON\n"
                "  4. Save to " + str(CREDENTIALS_PATH)
            )
            sys.exit(1)
        flow = InstalledAppFlow.from_client_secrets_file(str(CREDENTIALS_PATH), SCOPES)
        creds = flow.run_local_server(port=0)
        TOKEN_DIR.mkdir(parents=True, exist_ok=True)
        with open(TOKEN_PATH, "w") as f:
            f.write(creds.to_json())
        print(f"Token saved to {TOKEN_PATH}")

    return build("docs", "v1", credentials=creds), build("drive", "v3", credentials=creds)


# ---------------------------------------------------------------------------
# Question data:  (start_index, [bullet_points], reference_or_None)
#
# start_index is the position where the question paragraph BEGINS in the doc.
# The script looks up the actual endIndex at runtime for correct insertion.
# Ordered from HIGHEST start to LOWEST so backwards processing works.
# ---------------------------------------------------------------------------

QUESTIONS = [
    # =====================================================================
    # UNIT 5 — Problem Solving Techniques
    # =====================================================================
    (
        7165,
        [
            "Critical thinking — analyse facts without bias",
            "Creativity — think of new ideas and solutions",
            "Active listening — understand the problem fully",
            "Decision-making — choose the best option confidently",
            "Teamwork — work with others to solve complex issues",
            "Adaptability — adjust your approach when things change",
        ],
        "Reference: Problem Solving Skills - GeeksforGeeks",
    ),
    (
        7113,
        [
            "Step 1 — Identify and define the problem clearly",
            "Step 2 — Gather relevant information and data",
            "Step 3 — Generate multiple possible solutions",
            "Step 4 — Evaluate alternatives and select the best one",
            "Step 5 — Implement the chosen solution",
            "Step 6 — Review results and refine if needed",
        ],
        "Reference: Problem Solving Model - GeeksforGeeks",
    ),
    (
        7045,
        [
            "Identify the problem — know exactly what is wrong",
            "Analyse the root cause — find why the problem occurred",
            "Brainstorm solutions — list all possible ways to fix it",
            "Select the best solution — compare pros and cons",
            "Apply the solution — put your plan into action",
            "Review the outcome — check if the problem is solved",
        ],
        None,
    ),
    (
        6983,
        [
            "Define the problem — be clear about what needs to be solved",
            "Analyse the situation — collect facts and data",
            "Identify alternatives — think of different approaches",
            "Evaluate options — weigh the advantages and disadvantages",
            "Implement the plan — take action on the chosen option",
            "Monitor and adjust — check progress and make changes if needed",
        ],
        None,
    ),
    (
        6848,
        [
            "Produces many creative ideas in a short time",
            "Encourages team participation and diverse viewpoints",
            "Helps break free from routine thinking patterns",
            "Builds team spirit and collaboration",
            "Leads to unexpected and innovative solutions",
        ],
        "Reference: Brainstorming - GeeksforGeeks",
    ),
    (
        6739,
        [
            "Reduces misunderstandings and errors at work",
            "Improves teamwork and collaboration between colleagues",
            "Increases productivity and efficiency",
            "Builds trust and positive relationships in the workplace",
            "Helps in resolving conflicts quickly and smoothly",
        ],
        "Reference: Importance of Communication at Workplace - GeeksforGeeks",
    ),
    (
        6653,
        [
            "Physical barriers — noise, poor network, bad phone connection",
            "Language barriers — using jargon or unfamiliar words",
            "Emotional barriers — stress, anger, or nervousness",
            "Cultural barriers — different customs and norms",
            "Overcome by — speaking clearly, listening carefully, asking for feedback",
        ],
        "Reference: Barriers to Effective Communication - GeeksforGeeks",
    ),
    (
        6562,
        [
            "Interpersonal skills are the abilities we use to interact with others daily",
            "Examples include communication, empathy, patience, and teamwork",
            "Role in teamwork — helps resolve conflicts and build trust",
            "Good interpersonal skills lead to better collaboration and shared success",
            "They create a positive and productive work environment",
        ],
        "Reference: Interpersonal Skills - GeeksforGeeks",
    ),
    (
        6253,
        [
            "A problem is any situation where there is a gap between what is and what should be",
            "A problem challenges us to find a solution using our skills and knowledge",
            "Problems can be simple (easy to solve) or complex (need deep analysis)",
            "Viewing a problem as an opportunity helps in growth and learning",
        ],
        None,
    ),
    (
        6118,
        [
            "A problem is a situation that needs a solution or decision",
            "It arises when there is a difference between the current state and the goal",
            "Problems can be personal, professional, technical, or social",
            "Solving problems requires analysis, creativity, and logical thinking",
        ],
        "Reference: What is a Problem? - GeeksforGeeks",
    ),
    (
        6045,
        [
            "Decision-making is choosing the best option from available alternatives",
            "Importance — affects personal and professional success",
            "Good decisions save time, money, and resources",
            "Involves steps — identify goal, gather info, evaluate options, choose, act",
            "Helps in solving problems and achieving objectives efficiently",
        ],
        "Reference: Decision Making - GeeksforGeeks",
    ),

    # =====================================================================
    # UNIT 4 — Skills for Interviews
    # =====================================================================
    (
        5740,
        [
            "Maintain good posture — sit straight and face the interviewer",
            "Use appropriate hand gestures — do not cross arms",
            "Keep eye contact — shows confidence and honesty",
            "Avoid fidgeting — do not tap fingers or shake legs",
            "Smile naturally — creates a friendly impression",
        ],
        None,
    ),
    (
        5671,
        [
            "Shows confidence — a firm handshake and upright posture",
            "Conveys interest — leaning forward slightly shows engagement",
            "Mirroring — subtly matching the interviewer's posture builds rapport",
            "Avoid negative signals — crossed arms, looking away, slouching",
            "Use open gestures — keep palms visible and avoid pointing",
        ],
        "Reference: Body Language in Interview - GeeksforGeeks",
    ),
    (
        5549,
        [
            "Facial expressions — show interest and enthusiasm naturally",
            "Eye contact — look at the interviewer, not at the floor",
            "Posture — sit straight and avoid slouching",
            "Gestures — use hands moderately to explain points",
            "Tone of voice — speak clearly with a steady, confident tone",
        ],
        "Reference: Non-Verbal Communication - GeeksforGeeks",
    ),
    (
        5446,
        [
            "Pay full attention — do not let your mind wander",
            "Do not interrupt — let the speaker finish before replying",
            "Show that you are listening — nod and give small verbal cues",
            "Ask clarifying questions — ensures you understood correctly",
            "Provide feedback — summarise what you heard to confirm",
        ],
        None,
    ),
    (
        5337,
        [
            "Pay full attention to the speaker without distractions",
            "Show that you are listening through body language (nodding, eye contact)",
            "Provide feedback by summarising or asking relevant questions",
            "Do not interrupt — let the person finish speaking",
            "Respond thoughtfully after understanding the complete message",
        ],
        "Reference: Active Listening - GeeksforGeeks",
    ),
    (
        5196,
        [
            "Prepare well — research the topic before the discussion",
            "Listen actively — understand others before responding",
            "Speak clearly and confidently — make your points short and relevant",
            "Respect different opinions — do not interrupt or dominate",
            "Stay on topic — do not drift away from the subject",
        ],
        None,
    ),
    (
        5011,
        [
            "Debate — two sides argue opposite views; there is a winner and loser",
            "Group Discussion — multiple people share views to reach a common understanding",
            "Debate is competitive; GD is collaborative",
            "In debate, participants challenge each other; in GD, they build on each other's ideas",
            "GD focuses on teamwork; debate focuses on winning an argument",
        ],
        "Reference: Debate vs Group Discussion - GeeksforGeeks",
    ),
    (
        4886,
        [
            "Types — Factual GD (based on facts), Opinion-based GD (personal views), Case-study GD (solve a problem)",
            "Knowledge — be well-informed about the topic",
            "Communication — speak clearly and listen actively",
            "Team spirit — respect others and cooperate",
            "Logic — support your points with reasoning",
            "Leadership — help guide the discussion forward positively",
        ],
        None,
    ),
    (
        4782,
        [
            "Types — Factual (news/current events), Opinion-based (abstract topics), Case-based (business problems)",
            "Principle 1 — everyone gets a fair chance to speak",
            "Principle 2 — listen before you speak",
            "Principle 3 — keep contributions short and relevant",
            "Principle 4 — respect differing viewpoints",
        ],
        "Reference: Group Discussion - GeeksforGeeks",
    ),
    (
        4699,
        [
            "Be prepared — read about the topic beforehand",
            "Start strong — initiate the discussion if you are confident",
            "Listen more — understand what others say before jumping in",
            "Be concise — do not speak for too long; let others contribute",
            "Stay polite — do not shout, interrupt, or get aggressive",
        ],
        None,
    ),
    (
        4562,
        [
            "Communication skills — speaking and listening clearly",
            "Confidence — presenting yourself with self-assurance",
            "Teamwork — collaborating well with others",
            "Adaptability — adjusting to different situations",
            "Problem-solving — handling unexpected questions calmly",
            "Professionalism — dressing appropriately and being punctual",
        ],
        "Reference: Soft Skills for Interview - GeeksforGeeks",
    ),
    (
        4434,
        [
            "Research the company and the job role thoroughly",
            "Prepare answers for common interview questions",
            "Dress professionally and arrive on time",
            "Bring copies of your resume, certificates, and ID proof",
            "Practice confident body language and eye contact",
            "Prepare questions to ask the interviewer about the role",
        ],
        "Reference: Interview Preparation - GeeksforGeeks",
    ),
    (
        4309,
        [
            "An interview is a formal conversation between an employer and a candidate",
            "Types — Structured (fixed questions), Unstructured (open conversation), Semi-structured (mix of both)",
            "Types by mode — Face-to-face, Telephonic, Video call, Panel interview",
            "Types by purpose — Stress interview, Technical interview, HR interview",
            "The goal is to assess if the candidate is a good fit for the job",
        ],
        None,
    ),
    (
        4248,
        [
            "An interview is a formal meeting where an employer evaluates a job applicant",
            "Types — Personal interview, Telephonic interview, Video interview, Panel interview",
            "Types by format — Structured (same questions for all), Unstructured (open-ended), Stress interview (tests pressure handling)",
            "The interviewer assesses skills, personality, and suitability for the role",
        ],
        "Reference: Types of Interview - GeeksforGeeks",
    ),

    # =====================================================================
    # UNIT 3 — Grammar & Comprehension
    # =====================================================================
    (
        4084,
        [
            "Subject: Acceptance of Job Offer — Infosys",
            "Dear HR Team,",
            "I am writing to formally accept the offer for the position at Infosys.",
            "I am grateful for this opportunity and look forward to joining the team.",
            "I confirm my joining date and will complete all joining formalities on time.",
            "Thank you for selecting me. I am excited to begin my journey with Infosys.",
            "Sincerely, [Your Name]",
        ],
        "Reference: Job Acceptance Email - GeeksforGeeks",
    ),
    (
        4009,
        [
            "Subject: Application for [Job Title] Position",
            "Dear HR Manager,",
            "I am writing to apply for the [Job Title] position at your company.",
            "I have attached my resume and cover letter for your review.",
            "I believe my skills and experience make me a suitable candidate for this role.",
            "I look forward to the opportunity to discuss my application with you.",
            "Thank you for your time and consideration.",
            "Sincerely, [Your Name]",
        ],
        "Reference: Job Application Email - GeeksforGeeks",
    ),
    (
        3810,
        [
            "Your Name and Address (top left)",
            "Date",
            "Recipient's Name, Designation, Company Name, Company Address",
            "Subject — Application for the Post of [Job Title]",
            "Salutation — Dear Mr./Ms. [Last Name]",
            "Body paragraph 1 — Introduce yourself and state the position you are applying for",
            "Body paragraph 2 — Highlight your qualifications, skills, and experience",
            "Body paragraph 3 — Express enthusiasm and request an interview",
            "Closing — Sincerely / Yours faithfully",
            "Signature — Your name and contact details",
        ],
        "Reference: Cover Letter - GeeksforGeeks",
    ),
    (
        3706,
        [
            "Sender's Address — Your complete address with PIN code",
            "Date — The day you are writing the letter",
            "Receiver's Address — Company name, department, and full address",
            "Subject — Application for the Post of Junior Engineer",
            "Salutation — Dear Sir/Madam,",
            "Body — Introduce yourself, mention your qualifications (B.E./B.Tech), and relevant skills",
            "Explain why you are a good fit — technical knowledge, projects, internships",
            "Closing — Thank the reader and mention that you look forward to their response",
            "Complimentary Close — Yours faithfully,",
            "Signature — Your full name, phone number, and email",
        ],
        "Reference: Job Application Letter - GeeksforGeeks",
    ),
    (
        3506,
        [
            "Story writing is the art of creating a narrative with characters, plot, and setting",
            "Components — Characters (people in the story), Plot (sequence of events), Setting (time and place), Conflict (the problem), Theme (the main message)",
            "A good story has a beginning, middle, and end",
            "Use descriptive language to make the story interesting",
            "The story should teach a lesson or convey a moral",
        ],
        "Reference: Story Writing - GeeksforGeeks",
    ),
    (
        3425,
        [
            "A tortoise and a hare lived in a forest. The hare always boasted about how fast he could run.",
            "One day, the hare challenged the tortoise to a race. The tortoise accepted calmly.",
            "The hare ran very fast and got far ahead. He was so confident that he stopped to take a nap.",
            "The tortoise kept moving slowly but steadily. He never stopped or gave up.",
            "When the hare woke up, the tortoise was near the finish line. The tortoise won the race.",
            "Moral — Slow and steady wins the race. Overconfidence can lead to failure.",
        ],
        None,
    ),
    (
        3324,
        [
            "NEP 2020 was launched by the Government of India to transform the education system",
            "It focuses on holistic, flexible, and multidisciplinary learning",
            "Key changes — 5+3+3+4 school structure instead of 10+2",
            "Emphasis on critical thinking, vocational training, and digital literacy",
            "Aims to make India a global knowledge superpower by 2040",
        ],
        "Reference: National Education Policy 2020 - GeeksforGeeks",
    ),
    (
        3271,
        [
            "VLSI (Very Large Scale Integration) is the process of creating integrated circuits with millions of transistors on a single chip",
            "The future of VLSI is driven by smaller transistor sizes and higher performance",
            "AI and machine learning chips are a major growth area for VLSI design",
            "Internet of Things (IoT) devices rely on low-power VLSI chips",
            "VLSI technology will continue to advance with 3D chip stacking and new materials",
        ],
        "Reference: Future of VLSI - GeeksforGeeks",
    ),
    (
        3146,
        [
            "College life offers more freedom and independence than school life",
            "Students can choose their own subjects and schedule",
            "College encourages critical thinking and self-learning",
            "There are more opportunities for social events, clubs, and networking",
            "College prepares students for real-world challenges and careers",
            "School life is more structured with strict rules and guidance from teachers",
        ],
        "Reference: College Life Essay - GeeksforGeeks",
    ),

    # =====================================================================
    # UNIT 2 — Arithmetic, Reasoning & Quantitative Ability
    # =====================================================================
    (
        2870,
        [
            "Expand → Contract",
            "Mortal → Immortal",
            "Artificial → Natural",
            "Antonyms are words that have opposite meanings to each other",
        ],
        "Reference: Antonyms - GeeksforGeeks",
    ),
    (
        2776,
        [
            "Vent → Opening, outlet, exit, release",
            "Alert → Watchful, attentive, aware, vigilant",
            "Distant → Far, remote, faraway, isolated",
            "Synonyms are words that have similar meanings to each other",
        ],
        "Reference: Synonyms - GeeksforGeeks",
    ),
    (
        2514,
        [
            "Step 1 — Distance = 600 metres, Time = 5 minutes = 5 x 60 = 300 seconds",
            "Step 2 — Speed = Distance / Time = 600 / 300 = 2 metres per second",
            "Step 3 — Convert to km/h: multiply by 18/5",
            "Step 4 — 2 x 18/5 = 36/5 = 7.2 km/h",
            "Answer — The person walks at a speed of 7.2 km/h",
        ],
        "Reference: Speed Distance Time - GeeksforGeeks",
    ),
    (
        2371,
        [
            "Step 1 — Find the differences: 91 - 43 = 48, 183 - 91 = 92",
            "Step 2 — Find the HCF of 48 and 92",
            "Step 3 — 48 = 2 x 2 x 2 x 2 x 3, 92 = 2 x 2 x 23",
            "Step 4 — Common factors = 2 x 2 = 4",
            "Answer — The greatest number that divides 43, 91, and 183 leaving the same remainder is 4",
        ],
        "Reference: LCM and HCF - GeeksforGeeks",
    ),
    (
        2309,
        [
            "Step 1 — Write 0.000216 as a fraction: 216 / 1,000,000",
            "Step 2 — Simplify: 216 = 6 x 6 x 6 = 6 cubed",
            "Step 3 — 1,000,000 = 100 x 100 x 100 = 100 cubed",
            "Step 4 — Cube root of 216 / 1,000,000 = 6 / 100",
            "Answer — The cube root of 0.000216 is 0.06",
        ],
        None,
    ),
    (
        2193,
        [
            "Mental arithmetic is the ability to perform calculations in your head without using paper, calculator, or devices",
            "It improves speed and accuracy in everyday math tasks",
            "Skills include — addition, subtraction, multiplication, division, percentages, and square roots",
            "Regular practice strengthens memory and concentration",
            "Useful in competitive exams, interviews, and daily life situations",
        ],
        "Reference: Mental Arithmetic - GeeksforGeeks",
    ),
    (
        2073,
        [
            "Proposed by Howard Gardner, the theory says intelligence is not a single ability",
            "It identifies 8 types of intelligence",
            "Linguistic — good with words and languages (poets, writers)",
            "Logical-Mathematical — good with logic and numbers (scientists, engineers)",
            "Spatial — good with images and space (architects, artists)",
            "Bodily-Kinesthetic — good with physical movement (dancers, athletes)",
            "Musical — sensitive to sound and rhythm (musicians, composers)",
            "Interpersonal — understands others well (teachers, leaders)",
            "Intrapersonal — understands oneself deeply (philosophers, psychologists)",
            "Naturalistic — connected to nature (biologists, farmers)",
        ],
        "Reference: Multiple Intelligence Theory - GeeksforGeeks",
    ),
    (
        1949,
        [
            "Higher order thinking skills (HOTS) go beyond simple recall of facts",
            "Analysing — breaking information into parts to understand it better",
            "Evaluating — judging the value of information based on criteria",
            "Creating — combining ideas to form something new",
            "HOTS help in critical thinking, problem solving, and innovation",
        ],
        "Reference: Bloom's Taxonomy - GeeksforGeeks",
    ),
    (
        1902,
        [
            "Bloom's Taxonomy is a framework for classifying different levels of thinking",
            "It has 6 levels, from lowest to highest",
            "Remember — recall facts and basic concepts (e.g., list the months of the year)",
            "Understand — explain ideas and concepts (e.g., summarise a paragraph)",
            "Apply — use information in new situations (e.g., solve a math problem)",
            "Analyse — draw connections between ideas (e.g., compare two characters)",
            "Evaluate — justify a decision or position (e.g., argue for a solution)",
            "Create — produce new or original work (e.g., write a short story)",
        ],
        None,
    ),
    (
        1782,
        [
            "Emotional intelligence (EQ) is the ability to recognise, understand, and manage emotions",
            "Components — Self-awareness, Self-regulation, Motivation, Empathy, Social skills",
            "EQ is as important as IQ for success in life and work",
            "High EQ helps in teamwork, leadership, and handling stress",
            "EQ can be improved with practice — mindfulness, listening, and reflecting",
        ],
        "Reference: Emotional Intelligence - GeeksforGeeks",
    ),
    (
        1750,
        [
            "Intelligence is the ability to learn, understand, and apply knowledge",
            "It includes logical reasoning, problem solving, and adapting to new situations",
            "Intelligence can be analytical (book smart), creative, or practical (street smart)",
            "It is measured through IQ tests, but intelligence is more than just a number",
            "Theories like Gardner's Multiple Intelligence show there are many kinds of intelligence",
        ],
        "Reference: What is Intelligence? - GeeksforGeeks",
    ),

    # =====================================================================
    # UNIT 1 — Soft Skills & Communication Basics
    # =====================================================================
    (
        1552,
        [
            "Builds better relationships between colleagues and managers",
            "Increases efficiency and reduces mistakes in tasks",
            "Encourages teamwork and a positive work culture",
            "Helps in resolving conflicts and avoid misunderstandings",
            "Improves customer satisfaction and professional reputation",
        ],
        None,
    ),
    (
        1466,
        [
            "Semantic barriers — words with different meanings for different people",
            "Psychological barriers — stress, anger, or bias that blocks understanding",
            "Organisational barriers — unclear hierarchy or too many management levels",
            "Personal barriers — shyness, lack of confidence, or fear of speaking",
            "To overcome — use simple language, listen actively, ask for feedback",
        ],
        None,
    ),
    (
        1389,
        [
            "NEP 2020 replaced the old 10+2 system with a 5+3+3+4 structure covering ages 3 to 18",
            "It emphasises early childhood education, which was not compulsory before",
            "Students can choose subjects across streams — science, commerce, arts — no rigid divisions",
            "Vocational training and internships are introduced from Class 6 onwards",
            "The policy promotes digital learning, critical thinking, and Indian languages",
        ],
        None,
    ),
    (
        1336,
        [
            "VLSI technology allows billions of transistors to fit on a tiny silicon chip",
            "Future trends include AI accelerators, quantum computing chips, and 3D ICs",
            "Chips are becoming faster, smaller, and more energy-efficient",
            "VLSI is critical for smartphones, self-driving cars, medical devices, and space technology",
            "India is investing in VLSI design to become a global semiconductor hub",
        ],
        "Reference: Future of VLSI Technology - GeeksforGeeks",
    ),
    (
        1139,
        [
            "Start with your contact details and the date at the top",
            "Add the HR Manager's name, company name, and address",
            "Subject line — Application for the Position of [Job Title]",
            "Paragraph 1 — Introduce yourself and state the position you are applying for",
            "Paragraph 2 — Highlight your qualifications, experience, and key achievements",
            "Paragraph 3 — Explain why you are interested in the company and the role",
            "Closing — Request an interview and thank the reader for their time",
            "End with Yours sincerely, your name, and contact information",
        ],
        "Reference: Cover Letter Writing - GeeksforGeeks",
    ),
    (
        984,
        [
            "Sender's address at the top left corner",
            "Date below the address",
            "Receiver's address — The HR Manager, Company Name, Company Address",
            "Subject — Application for the Post of Junior Engineer",
            "Salutation — Dear Sir or Madam,",
            "Body — Introduce yourself, your engineering degree, technical skills, and any internship experience",
            "Explain why you are suitable — mention problem-solving, teamwork, and technical knowledge",
            "Closing — Thank the reader and express hope for an interview opportunity",
            "Complimentary close — Yours faithfully,",
            "Enclosure — mention attached resume and certificates",
        ],
        None,
    ),
    (
        908,
        [
            "Chronological — lists work experience in reverse date order (most recent first). Best for steady career growth.",
            "Functional — focuses on skills and achievements, not job titles or dates. Best for career changers or gaps.",
            "Hybrid (Combination) — mixes chronological and functional. Best for most job seekers.",
            "Chronological is the most common format preferred by recruiters",
            "Hybrid is useful when you have both relevant skills and some work experience",
        ],
        "Reference: Resume Formats - GeeksforGeeks",
    ),
    (
        715,
        [
            "A resume is a short document that summarises education, work experience, skills, and achievements",
            "Types — Chronological (work history by date), Functional (focus on skills), Hybrid (mix of both)",
            "Targeted Resume — customised for a specific job role",
            "Mini Resume — short summary used for networking events",
            "The goal of a resume is to get an interview call",
        ],
        None,
    ),
    (
        649,
        [
            "Contact Information — name, phone number, email, and LinkedIn profile",
            "Career Objective — a short statement about your career goals",
            "Education — degrees, institutions, years, and grades",
            "Work Experience — job titles, companies, duration, and key responsibilities",
            "Skills — relevant technical and soft skills",
            "Achievements — awards, certifications, and notable accomplishments",
            "References — names of people who can vouch for your work (optional)",
        ],
        "Reference: Resume Components - GeeksforGeeks",
    ),
    (
        445,
        [
            "Brings together knowledge from different fields to solve complex problems",
            "Encourages creative thinking by combining diverse perspectives",
            "Improves communication and teamwork across departments",
            "Leads to more innovative and well-rounded solutions",
            "Example — a software project needs engineers, designers, marketers, and managers",
        ],
        "Reference: Interdisciplinary Collaboration - GeeksforGeeks",
    ),
    (
        336,
        [
            "Set small, achievable goals and celebrate when you reach them",
            "Practice positive self-talk — replace doubts with encouraging thoughts",
            "Learn new skills — competence builds confidence",
            "Face your fears — step out of your comfort zone gradually",
            "Surround yourself with supportive and positive people",
            "Take care of your health — exercise, sleep well, and eat properly",
        ],
        "Reference: How to Build Self-Confidence - GeeksforGeeks",
    ),
    (
        186,
        [
            "Soft skills are personal traits like communication, teamwork, and attitude",
            "Hard skills are technical abilities like coding, accounting, or operating machinery",
            "Soft skills are hard to measure but essential for career growth",
            "Hard skills can be taught and tested through exams and certifications",
            "Both are needed — hard skills get you the job, soft skills help you keep it",
        ],
        None,
    ),
    (
        127,
        [
            "Hard skills are teachable technical abilities (e.g., programming, data analysis)",
            "Soft skills are interpersonal qualities (e.g., communication, leadership)",
            "Hard skills are learned through formal education and training",
            "Soft skills are developed through life experience and practice",
            "Hard skills vary by job; soft skills are valuable in every profession",
        ],
        "Reference: Hard Skills vs Soft Skills - GeeksforGeeks",
    ),
    (
        80,
        [
            "Soft skills are personal attributes that help you work well with others",
            "Hard skills are specific technical abilities needed for a job",
            "Example of hard skill — writing Python code or using Excel",
            "Example of soft skill — communicating clearly or working in a team",
            "Hard skills can be measured by tests; soft skills are shown through behaviour",
            "Employers look for a balance of both hard and soft skills",
        ],
        None,
    ),
]

# =====================================================================
# Helpers
# =====================================================================


def build_index_map(doc):
    """Build a dict: startIndex -> {endIndex, text} for every paragraph."""
    index_map = {}
    for elem in doc.get("body", {}).get("content", []):
        ps = elem.get("paragraph")
        if not ps:
            continue
        si = elem.get("startIndex")
        ei = elem.get("endIndex")
        text = "".join(
            r.get("textRun", {}).get("content", "")
            for r in ps.get("elements", [])
        )
        index_map[si] = {"endIndex": ei, "text": text}
    return index_map


def resolve_end_indices(docs, questions):
    """Given (start_index, ...) tuples, return (end_index, ...) tuples by
    looking up each start_index in the live document.

    Falls back to the next paragraph's startIndex - 1 if exact match fails.
    """
    doc = docs.documents().get(documentId=DOC_ID).execute()
    imap = build_index_map(doc)

    resolved = []
    for start_idx, bullets, ref in questions:
        if start_idx in imap:
            end_idx = imap[start_idx]["endIndex"]
        else:
            # fallback: find nearest paragraph
            starts = sorted(imap.keys())
            for s in reversed(starts):
                if s < start_idx:
                    end_idx = imap[s]["endIndex"]
                    break
            else:
                print(f"  ERROR: cannot resolve start_index {start_idx}")
                sys.exit(1)
        resolved.append((end_idx, bullets, ref))
    return resolved


def make_answer_requests(end_index, bullets, reference=None):
    """Build batchUpdate requests for one question insertion.

    Inserts at end_index - 1 (just before the paragraph-ending \n),
    then applies createParagraphBullets to the bullet paragraphs only.
    """
    insert_at = end_index - 1

    lines = ["", "Answer:"] + bullets + [""]
    text = "\n".join(lines)
    if reference:
        text += "\n" + reference + "\n"

    prefix = "\n\nAnswer:\n"
    bullet_start = insert_at + len(prefix)
    bullet_text = "\n".join(bullets)
    bullet_end = bullet_start + len(bullet_text)

    return [
        {
            "insertText": {
                "location": {"index": insert_at},
                "text": text,
            }
        },
        {
            "createParagraphBullets": {
                "range": {
                    "startIndex": bullet_start,
                    "endIndex": bullet_end,
                },
                "bulletPreset": "BULLET_DISC_CIRCLE_SQUARE",
            }
        },
    ]


def verify_document_structure(docs):
    """Fetch and print the current document structure for reference."""
    doc = docs.documents().get(documentId=DOC_ID).execute()
    content = doc.get("body", {}).get("content", [])
    print(f"\n=== Document: {doc.get('title', 'Untitled')} ===")
    print(f"Total content elements: {len(content)}")
    print(f"Document end index: {content[-1].get('endIndex', '?')}\n")

    for elem in content:
        ps = elem.get("paragraph", {})
        if not ps:
            continue
        text = "".join(
            r.get("textRun", {}).get("content", "")
            for r in ps.get("elements", [])
        )
        clean = text.replace("\n", "\\n").strip()
        if clean:
            si = elem.get("startIndex", "?")
            ei = elem.get("endIndex", "?")
            style = ps.get("paragraphStyle", {}).get("namedStyleType", "")
            print(f"  [{si:>5}–{ei:<5}] {style:20s} {clean[:120]}")


# =====================================================================
# Main
# =====================================================================


def main():
    args = set(sys.argv[1:])

    docs, drive = _get_services()

    if "--verify" in args:
        verify_document_structure(docs)
        return

    # resolve start -> end indices from live document
    print("Resolving end indices from document...")
    resolved = resolve_end_indices(docs, QUESTIONS)
    print(f"  Resolved {len(resolved)} questions")

    # verify descending order
    indices = [e for e, _, _ in resolved]
    assert indices == sorted(indices, reverse=True), "Not in descending order!"

    # build all requests
    all_requests = []
    for end_index, bullets, ref in resolved:
        reqs = make_answer_requests(end_index, bullets, ref)
        all_requests.append((end_index, reqs))

    total_req_atoms = sum(len(r) for _, r in all_requests)
    print(f"Total request atoms: {total_req_atoms}\n")

    if "--dry-run" in args:
        print("DRY RUN — insertions (highest to lowest):\n")
        for end_index, reqs in all_requests:
            text = reqs[0]["insertText"]["text"]
            first_line = [
                l for l in text.split("\n")
                if l.strip() and l.strip() != "Answer:"
            ]
            preview = (first_line[0][:80] + "..") if first_line else "(empty)"
            print(f"  endIndex={end_index:>5}  →  {preview}")
        print(f"\nTotal: {len(all_requests)} insertions, {total_req_atoms} API requests")
        return

    # execute in batches of 100
    MAX_BATCH = 100
    flat = [r for _, reqs in all_requests for r in reqs]

    print(f"Executing {len(all_requests)} insertions ({len(flat)} API requests)...")
    for i in range(0, len(flat), MAX_BATCH):
        batch = flat[i : i + MAX_BATCH]
        try:
            result = docs.documents().batchUpdate(
                documentId=DOC_ID,
                body={"requests": batch},
            ).execute()
            replies = result.get("replies", [])
            print(f"  Batch {i // MAX_BATCH + 1}: {len(batch)} requests OK "
                  f"({len(replies)} replies)")
        except HttpError as e:
            print(f"  Batch {i // MAX_BATCH + 1} FAILED: {e}")
            details = json.loads(e.content.decode()) if e.content else {}
            print(json.dumps(details, indent=2)[:2000])
            sys.exit(1)

    link = f"https://docs.google.com/document/d/{DOC_ID}/edit"
    print(f"\nDone — {len(all_requests)} questions updated.")
    print(f"Open: {link}")


if __name__ == "__main__":
    main()
