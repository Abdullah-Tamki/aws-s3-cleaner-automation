# AWS S3 Cleaner Automation

This project demonstrates how to automate Amazon S3 bucket management using **Terraform** and **Python (boto3)**.  

It combines **Infrastructure as Code (IaC)** with **custom scripting** to show both cloud automation and programming skills.

---

## 🚀 Features

### Terraform
- Creates an S3 bucket (`my-s3-cleaner-demo-bucket`).
- Adds identifying tags.
- Configures a **lifecycle rule** to automatically delete files older than **3 days**.

### Python (boto3)
- Ensures the bucket exists.
- Uploads local files from `test_uploads/`.
- Lists files in the bucket.
- Includes a **manual cleanup function** for deleting old files (⚠️ commented out, since Terraform already handles cleanup).  
  - Left for demonstration purposes to show custom logic.

---
