import json
import urllib.request
import subprocess
import shutil
import os
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from threading import Lock
from pathlib import Path

# Files/Directories
target_dir = Path("/home/aditya/Desktop/Projects/MEMORY/.agents/skills")
tmp_dir = Path("/tmp/starred_repos_all")
tmp_dir.mkdir(exist_ok=True)

PROCESSED_FILE = Path("/tmp/processed_repos.json")
processed_lock = Lock()
processed_repos = set()

if PROCESSED_FILE.exists():
    try:
        processed_repos = set(json.loads(PROCESSED_FILE.read_text()))
    except Exception:
        pass

# Fetch the list of all starred repositories
repos = []
page = 1
while True:
    url = f"https://api.github.com/users/adityashirsatrao007/starred?per_page=100&page={page}"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    try:
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode())
            if not data:
                break
            repos.extend(data)
            page += 1
    except Exception as e:
        print(f"Error fetching page {page}: {e}")
        break

print(f"Total repositories to check: {len(repos)}. Previously processed: {len(processed_repos)}")

def process_repo(r, idx):
    name = r["full_name"]
    if name in processed_repos:
        print(f"[{idx}/{len(repos)}] {name} - Already processed (skipped)")
        return name, True

    clone_url = r["clone_url"]
    folder_name = r["name"]
    
    # We create a unique temporary folder name per thread to prevent collision
    repo_tmp = tmp_dir / f"{folder_name}_{os.getpid()}_{idx}"
    
    print(f"[{idx}/{len(repos)}] Cloning {name}...")
    if repo_tmp.exists():
        shutil.rmtree(repo_tmp)

    try:
        # Clone with --depth 1 and limit to 45 seconds
        subprocess.run(["git", "clone", "--depth", "1", clone_url, str(repo_tmp)], 
                       check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=45)
    except Exception as e:
        print(f"Failed to clone/download {name}: {e}")
        if repo_tmp.exists():
            shutil.rmtree(repo_tmp)
        return name, False

    try:
        # Find all SKILL.md files
        skills = list(repo_tmp.rglob("SKILL.md"))
        if skills:
            for skill_file in skills:
                skill_src_dir = skill_file.parent
                skill_name = skill_src_dir.name
                if skill_name == folder_name or not skill_name or skill_name == "skills":
                    skill_name = f"{folder_name}-skill"
                
                dest = target_dir / skill_name
                print(f"-> Installing skill: {dest.name} from {name}")
                shutil.copytree(skill_src_dir, dest, dirs_exist_ok=True)
        else:
            # Create a wrapper skill if README or AGENTS file exists
            readme = repo_tmp / "README.md"
            agents_md = repo_tmp / "AGENTS.md"
            docs_file = None
            if agents_md.exists():
                docs_file = agents_md
            elif readme.exists():
                docs_file = readme
                
            if docs_file:
                safe_name = name.replace("/", "-")
                dest = target_dir / safe_name
                if not dest.exists():
                    dest.mkdir(parents=True, exist_ok=True)
                    try:
                        content = docs_file.read_text(errors="ignore")
                        skill_content = f"---\nname: {safe_name}\ndescription: Documentation and guidelines for {name}\n---\n\n" + content
                        (dest / "SKILL.md").write_text(skill_content)
                        print(f"-> Created wrapper skill for {name}")
                    except Exception as e:
                        print(f"Failed to write skill file for {name}: {e}")
                else:
                    print(f"-> Skill {safe_name} already exists, skipping wrapper.")
    except Exception as e:
        print(f"Error processing files in {name}: {e}")
    finally:
        if repo_tmp.exists():
            shutil.rmtree(repo_tmp)

    with processed_lock:
        processed_repos.add(name)
        try:
            PROCESSED_FILE.write_text(json.dumps(list(processed_repos)))
        except Exception:
            pass
            
    return name, True

# Run up to 16 threads concurrently (we tuned the TCP/NIC layers earlier to support high concurrency)
max_workers = 16
completed_count = 0
failed_count = 0

with ThreadPoolExecutor(max_workers=max_workers) as executor:
    futures = {executor.submit(process_repo, r, i+1): r for i, r in enumerate(repos)}
    for future in as_completed(futures):
        repo_name, success = future.result()
        if success:
            completed_count += 1
        else:
            failed_count += 1

print(f"Finished processing. Success: {completed_count}, Failed: {failed_count}")
