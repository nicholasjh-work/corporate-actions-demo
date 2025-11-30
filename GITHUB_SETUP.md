# GitHub Setup Instructions

## Quick Setup (Recommended)

```bash
cd corporate-actions-demo

# Initialize git repository
git init

# Add all files
git add .

# Create initial commit
git commit -m "Initial commit: Corporate action processing demo"

# Create GitHub repo and push
# (Replace YOUR_USERNAME with your GitHub username)
gh repo create corporate-actions-demo --public --source=. --remote=origin --push
```

## Manual Setup (If you don't have GitHub CLI)

### Step 1: Create Repository on GitHub

1. Go to https://github.com/new
2. Repository name: `corporate-actions-demo`
3. Description: "Corporate action processing system demo - FastAPI, React, MySQL, Docker, Kubernetes"
4. Choose **Public** (or Private if you prefer)
5. **DO NOT** initialize with README, .gitignore, or license (we already have these)
6. Click "Create repository"

### Step 2: Push Code to GitHub

```bash
cd corporate-actions-demo

# Initialize git repository
git init

# Add all files
git add .

# Create initial commit
git commit -m "Initial commit: Corporate action processing demo

- FastAPI backend with MySQL
- React dashboard with real-time updates
- Docker Compose for local development
- Kubernetes manifests for production
- Complete product roadmap with JIRA-style stories
- 8-minute demo guide for interview"

# Add your GitHub repository as remote
# Replace YOUR_USERNAME with your actual GitHub username
git remote add origin https://github.com/YOUR_USERNAME/corporate-actions-demo.git

# Push to GitHub
git branch -M main
git push -u origin main
```

## Verify Upload

After pushing, verify on GitHub:
1. Go to https://github.com/YOUR_USERNAME/corporate-actions-demo
2. Check all folders are present: backend/, frontend/, kubernetes/, roadmap/, scripts/
3. Verify README.md displays correctly
4. Check that .env files are NOT uploaded (only .env.example should be there)

## Repository Settings (Recommended)

### Add Topics
Go to your repo → About (gear icon) → Add topics:
- `fastapi`
- `react`
- `mysql`
- `docker`
- `kubernetes`
- `corporate-actions`
- `demo-project`
- `product-management`

### Add Description
"Corporate action processing system demonstrating event-driven architecture, REST APIs, and product management practices. Built with FastAPI, React, MySQL, Docker, and Kubernetes."

### Update README Badges (Optional)

Add these to the top of your README.md:

```markdown
[![Python](https://img.shields.io/badge/Python-3.11-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-18-61dafb.svg)](https://reactjs.org/)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ed.svg)](https://www.docker.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
```

## Clone on Your Mac Mini

Once pushed to GitHub, clone on your Mac mini:

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/corporate-actions-demo.git

# Navigate into it
cd corporate-actions-demo

# Deploy
./scripts/deploy.sh
```

## Updating the Repository

After making changes:

```bash
# Check what changed
git status

# Add changes
git add .

# Commit with message
git commit -m "Description of changes"

# Push to GitHub
git push
```

## Common Git Commands

```bash
# Check status
git status

# View commit history
git log --oneline

# Create new branch
git checkout -b feature/new-feature

# Switch branches
git checkout main

# Pull latest changes
git pull

# View remote URL
git remote -v
```

## Troubleshooting

### Issue: "remote origin already exists"
```bash
git remote remove origin
git remote add origin https://github.com/YOUR_USERNAME/corporate-actions-demo.git
```

### Issue: Authentication failed
Use Personal Access Token instead of password:
1. Go to GitHub Settings → Developer settings → Personal access tokens → Tokens (classic)
2. Generate new token with `repo` scope
3. Use token as password when pushing

Or use SSH:
```bash
# Generate SSH key (if you don't have one)
ssh-keygen -t ed25519 -C "your_email@example.com"

# Add to GitHub: Settings → SSH and GPG keys → New SSH key
cat ~/.ssh/id_ed25519.pub

# Use SSH URL instead
git remote set-url origin git@github.com:YOUR_USERNAME/corporate-actions-demo.git
```

### Issue: Large files
If you accidentally added large files:
```bash
# Remove from git but keep locally
git rm --cached filename

# Add to .gitignore
echo "filename" >> .gitignore

# Commit the change
git commit -m "Remove large file from git"
```

## Share Your Demo

After pushing, you can share:

**Repository URL:**
```
https://github.com/YOUR_USERNAME/corporate-actions-demo
```

**Clone command for others:**
```bash
git clone https://github.com/YOUR_USERNAME/corporate-actions-demo.git
cd corporate-actions-demo
./scripts/deploy.sh
```

## License (Optional)

If you want to add a license, create a `LICENSE` file. MIT is common for demos:

```bash
# Add MIT license
cat > LICENSE << 'EOF'
MIT License

Copyright (c) 2024 [Your Name]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
EOF

git add LICENSE
git commit -m "Add MIT license"
git push
```

## During Interview

You can reference your GitHub repo:

**Say:**
"I've open-sourced this demo on GitHub at github.com/YOUR_USERNAME/corporate-actions-demo. The entire codebase is there with documentation, tests, and deployment scripts. Anyone can clone it and run it locally in under 2 minutes with Docker."

This shows:
- Comfort with version control
- Open source contribution mindset
- Willingness to share knowledge
- Professional code organization
