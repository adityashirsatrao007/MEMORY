#!/usr/bin/env python3
"""Google Docs Note-Taking — standalone OAuth + Docs API wrapper."""

import argparse
import json
import os
import sys
from datetime import datetime
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


def _get_service():
    if TOKEN_PATH.exists():
        creds = Credentials.from_authorized_user_file(str(TOKEN_PATH), SCOPES)
    else:
        creds = None

    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    elif not creds or not creds.valid:
        if not CREDENTIALS_PATH.exists():
            print(
                "No credentials.json found. Create a Google Cloud OAuth client:\n"
                "  1. Go to https://console.cloud.google.com/apis/credentials\n"
                "  2. Create a project → Enable Google Docs API + Google Drive API\n"
                "  3. Credentials → Create OAuth 2.0 Client ID → Desktop app → Download JSON\n"
                "  4. Save it to: " + str(CREDENTIALS_PATH)
            )
            sys.exit(1)
        flow = InstalledAppFlow.from_client_secrets_file(str(CREDENTIALS_PATH), SCOPES)
        creds = flow.run_local_server(port=0)
        TOKEN_DIR.mkdir(parents=True, exist_ok=True)
        with open(TOKEN_PATH, "w") as f:
            f.write(creds.to_json())
        print(f"Token saved to {TOKEN_PATH}")

    return build("docs", "v1", credentials=creds), build("drive", "v3", credentials=creds)


def create(title, body_text):
    docs, drive = _get_service()
    doc = docs.documents().create(body={"title": title}).execute()
    doc_id = doc["documentId"]
    print(f"Created doc: {doc_id} — {doc['title']}")

    requests = [
        {
            "insertText": {
                "location": {"index": 1},
                "text": body_text,
            }
        }
    ]
    docs.documents().batchUpdate(documentId=doc_id, body={"requests": requests}).execute()

    link = f"https://docs.google.com/document/d/{doc_id}/edit"
    print(f"URL: {link}")
    return doc_id, link


def append(doc_id, body_text):
    docs, _ = _get_service()
    doc = docs.documents().get(documentId=doc_id).execute()
    end_index = doc["body"]["content"][-1]["endIndex"] - 1

    requests = [
        {
            "insertText": {
                "location": {"index": end_index},
                "text": "\n\n" + body_text,
            }
        }
    ]
    docs.documents().batchUpdate(documentId=doc_id, body={"requests": requests}).execute()
    link = f"https://docs.google.com/document/d/{doc_id}/edit"
    print(f"Appended to doc {doc_id}")
    print(f"URL: {link}")
    return doc_id, link


def search(query, max_results=5):
    _, drive = _get_service()
    results = (
        drive.files()
        .list(
            q=f"name contains '{query}' and mimeType='application/vnd.google-apps.document'",
            pageSize=max_results,
            fields="files(id, name, createdTime, webViewLink)",
        )
        .execute()
    )
    files = results.get("files", [])
    if not files:
        print("No docs found.")
    for f in files:
        print(f"  {f['name']} — {f['id']} — {f['webViewLink']}")
    return files


def list_docs(max_results=10):
    _, drive = _get_service()
    results = (
        drive.files()
        .list(
            q="mimeType='application/vnd.google-apps.document'",
            pageSize=max_results,
            fields="files(id, name, createdTime, webViewLink)",
            orderBy="createdTime desc",
        )
        .execute()
    )
    files = results.get("files", [])
    if not files:
        print("No docs found.")
    for f in files:
        print(f"  {f['name']} — {f['id']} — {f['webViewLink']}")
    return files


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Google Docs Notes")
    sub = parser.add_subparsers(dest="command", required=True)

    p_create = sub.add_parser("create", help="Create a new doc")
    p_create.add_argument("title", help="Document title")
    p_create.add_argument("--body", default="", help="Body text")

    p_append = sub.add_parser("append", help="Append to existing doc")
    p_append.add_argument("doc_id", help="Document ID")
    p_append.add_argument("--body", required=True, help="Text to append")

    p_search = sub.add_parser("search", help="Search docs by name")
    p_search.add_argument("query", help="Search query")
    p_search.add_argument("--max", type=int, default=5)

    p_list = sub.add_parser("list", help="List recent docs")
    p_list.add_argument("--max", type=int, default=10)

    args = parser.parse_args()

    if args.command == "create":
        create(args.title, args.body)
    elif args.command == "append":
        append(args.doc_id, args.body)
    elif args.command == "search":
        search(args.query, args.max)
    elif args.command == "list":
        list_docs(args.max)
