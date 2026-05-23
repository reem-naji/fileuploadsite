# ☁️ AWS S3 File Upload Web App

A full-stack web application built as part of a **Cloud Computing** course. Users can upload files through a browser-based UI; files are stored in and served directly from an **Amazon S3** bucket using pre-signed URLs for secure, time-limited access.

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python)
![Flask](https://img.shields.io/badge/Flask-3.0-black?logo=flask)
![AWS S3](https://img.shields.io/badge/AWS-S3-orange?logo=amazon-aws)

---

## Overview

This project demonstrates how to integrate AWS S3 into a web application — covering bucket interaction, secure file uploads via a Flask backend, and generating pre-signed URLs so files can be previewed or downloaded without making the bucket public.

---

## Features

- Upload files (`.pdf`, `.jpg`, `.jpeg`, `.png`, `.txt`) through a clean browser UI
- Files are stored directly in an S3 bucket via the AWS SDK (`boto3`)
- Uploaded files are listed automatically after each upload
- Each file is accessible through a **pre-signed URL** (expires in 1 hour) — no public bucket permissions needed
- Filenames are sanitised server-side before upload to prevent path traversal
- AWS credentials loaded securely from a `.env` file — never hardcoded

---

## Project Structure

```
.
├── backend.py          # Flask app — upload & list endpoints
├── requirements.txt    # Python dependencies
├── .gitignore
├── templates/
│   └── index.html      # Main page (served by Flask)
└── static/
    ├── script.js       # Fetch-based upload & file listing logic
    └── css/
        └── styles.css  # Page styles
```

> **Note:** Flask expects HTML templates under a `templates/` folder and static assets (JS, CSS) under `static/`. Move `index.html` to `templates/` and `script.js` / `styles.css` to `static/css/` before running.

---

## How It Works

```
Browser → POST /upload → Flask → boto3 → S3 Bucket
                                              ↓
Browser ← pre-signed URL ← Flask ← boto3 ← S3
```

1. The user picks a file in the browser and clicks **Upload**.
2. `script.js` sends a `multipart/form-data` POST request to `/upload`.
3. Flask validates the file type, sanitises the filename, and streams it to S3 with `upload_fileobj`.
4. S3 returns a **pre-signed URL** (1-hour expiry) that the frontend displays as a download/preview link.
5. `GET /files` lists all objects in the bucket, each with its own fresh pre-signed URL — called automatically on page load and after every successful upload.

---

## Getting Started

### Prerequisites

- Python 3.10+
- An [AWS account](https://aws.amazon.com/) with an S3 bucket created
- An IAM user with `s3:PutObject`, `s3:GetObject`, and `s3:ListBucket` permissions

### 1. Clone the repository

```bash
git clone https://github.com/<your-username>/s3-file-upload.git
cd s3-file-upload
```

### 2. Create and activate a virtual environment

```bash
python -m venv venv
source venv/bin/activate      # macOS / Linux
venv\Scripts\activate         # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project root (this file is git-ignored):

```env
AWS_ACCESS_KEY_ID=your_access_key_here
AWS_SECRET_ACCESS_KEY=your_secret_key_here
BUCKET_NAME=your_bucket_name_here
BUCKET_REGION=your_bucket_region_here   # e.g. us-east-1
```

### 5. Run the app

```bash
python backend.py
```

Open your browser at `http://127.0.0.1:5000`.

---

## AWS Setup (Quick Reference)

1. **Create an S3 bucket** in the [S3 Console](https://s3.console.aws.amazon.com/) — keep *Block all public access* **on** (pre-signed URLs handle access without making the bucket public).
2. **Create an IAM user** with programmatic access and attach a policy granting the three permissions listed above.
3. Copy the generated **Access Key ID** and **Secret Access Key** into your `.env` file.

---

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python, Flask |
| Cloud Storage | Amazon S3 (via `boto3`) |
| Frontend | HTML, CSS, Vanilla JS (Fetch API) |
| Config | `python-dotenv` |
| Security | `werkzeug.utils.secure_filename`, pre-signed URLs |
