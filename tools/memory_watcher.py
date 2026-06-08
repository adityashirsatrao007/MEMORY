import os
import time
import subprocess
import chromadb
import google.generativeai as genai
from datetime import datetime

# Configure Gemini
API_KEY = os.environ.get("GEMINI_API_KEY")
if not API_KEY:
    print("Warning: GEMINI_API_KEY not found in environment. Please export it.")
else:
    genai.configure(api_key=API_KEY)

MODEL = genai.GenerativeModel('gemini-2.5-flash')

HISTORY_FILE = os.path.expanduser("~/.bash_history")
PROGRESS_FILE = os.path.expanduser("~/Desktop/Projects/MEMORY/memory-bank/progress.md")
VECTOR_DB_PATH = os.path.expanduser("~/Desktop/Projects/MEMORY/vector_db")

# Initialize ChromaDB
chroma_client = chromadb.PersistentClient(path=VECTOR_DB_PATH)
collection = chroma_client.get_or_create_collection(name="antigravity_memory")

BATCH_TIME_LIMIT = 60 # wait 60 seconds of inactivity before summarizing
COMMAND_BUFFER = []
LAST_COMMAND_TIME = time.time()

def summarize_commands(commands):
    if not API_KEY:
        return "*(Gemini API Key missing, could not summarize)*\nRaw commands:\n" + "\n".join(commands)
    
    prompt = """
    You are the Antigravity Supermemory collector. 
    I ran the following terminal commands. 
    Please summarize what I was trying to accomplish in a single, short bullet point.
    Ignore trivial commands (like ls, cd, cat) unless they give context.
    Keep it in third person ("Aditya did X" or "User did X").
    If it's just random navigating, return 'SKIP'.
    
    Commands:
    """ + "\n".join(commands)
    
    try:
        response = MODEL.generate_content(prompt)
        text = response.text.strip()
        if text.upper() == 'SKIP' or text.startswith('SKIP'):
            return None
        return text
    except Exception as e:
        print(f"Error summarizing: {e}")
        return None

def append_to_memory(summary):
    if not summary:
        return
    now_dt = datetime.now()
    date_str = now_dt.strftime("%Y-%m-%d")
    time_str = now_dt.strftime("%H:%M")
    timestamp = int(now_dt.timestamp())
    
    entry = f"- **{time_str}**: {summary}\n"
    print(f"Adding memory: {entry.strip()}")
    
    # 1. Append to Markdown (progress.md)
    try:
        with open(PROGRESS_FILE, 'a') as f:
            f.write(entry)
    except Exception as e:
        print(f"Error writing to {PROGRESS_FILE}: {e}")
        
    # 2. Insert into Vector DB (ChromaDB)
    try:
        collection.add(
            documents=[summary],
            metadatas=[{"date": date_str, "time": time_str}],
            ids=[str(timestamp)]
        )
        print("Successfully indexed memory into ChromaDB.")
    except Exception as e:
        print(f"Error writing to Vector DB: {e}")

def follow(thefile):
    thefile.seek(0, 2)
    while True:
        line = thefile.readline()
        if not line:
            time.sleep(0.5)
            yield None
        else:
            yield line

def main():
    print(f"Starting Supermemory Watcher... monitoring {HISTORY_FILE}")
    
    global COMMAND_BUFFER, LAST_COMMAND_TIME
    
    if not os.path.exists(HISTORY_FILE):
        print(f"{HISTORY_FILE} does not exist.")
        return

    with open(HISTORY_FILE, "r") as f:
        loglines = follow(f)
        for line in loglines:
            now = time.time()
            
            # If we have commands in buffer and time limit passed since last command
            if COMMAND_BUFFER and (now - LAST_COMMAND_TIME) > BATCH_TIME_LIMIT:
                print(f"Batch time limit reached. Summarizing {len(COMMAND_BUFFER)} commands...")
                summary = summarize_commands(COMMAND_BUFFER)
                append_to_memory(summary)
                COMMAND_BUFFER = []
                
            if line:
                cmd = line.strip()
                if cmd:
                    COMMAND_BUFFER.append(cmd)
                    LAST_COMMAND_TIME = now
                    print(f"Captured: {cmd}")

if __name__ == "__main__":
    main()
