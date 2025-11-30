#!/bin/bash
set -e

echo "🚀 GitHub Setup Script"
echo "====================="
echo ""

# Check if git is installed
if ! command -v git &> /dev/null; then
    echo "❌ Git not found. Install with: brew install git"
    exit 1
fi

# Check if we're in the right directory
if [ ! -f "README.md" ] || [ ! -f "docker-compose.yml" ]; then
    echo "❌ Please run this script from the corporate-actions-demo directory"
    exit 1
fi

# Get GitHub username
echo "📝 Enter your GitHub username:"
read -r GITHUB_USERNAME

if [ -z "$GITHUB_USERNAME" ]; then
    echo "❌ GitHub username is required"
    exit 1
fi

echo ""
echo "Setting up git repository..."

# Initialize git if not already initialized
if [ ! -d ".git" ]; then
    git init
    echo "✅ Git repository initialized"
else
    echo "✅ Git repository already exists"
fi

# Add all files
git add .

# Check if there are changes to commit
if git diff-index --quiet HEAD -- 2>/dev/null; then
    echo "ℹ️  No changes to commit"
else
    # Create initial commit
    git commit -m "Initial commit: Corporate action processing demo

- FastAPI backend with MySQL
- React dashboard with real-time updates
- Docker Compose for local development
- Kubernetes manifests for production
- Complete product roadmap with JIRA-style stories
- 8-minute demo guide for interview"
    echo "✅ Initial commit created"
fi

# Check if remote already exists
if git remote | grep -q "origin"; then
    echo "ℹ️  Remote 'origin' already exists"
    CURRENT_REMOTE=$(git remote get-url origin)
    echo "   Current remote: $CURRENT_REMOTE"
    echo ""
    echo "Do you want to update it to https://github.com/$GITHUB_USERNAME/corporate-actions-demo.git? (y/n)"
    read -r UPDATE_REMOTE
    if [ "$UPDATE_REMOTE" = "y" ]; then
        git remote set-url origin "https://github.com/$GITHUB_USERNAME/corporate-actions-demo.git"
        echo "✅ Remote updated"
    fi
else
    # Add remote
    git remote add origin "https://github.com/$GITHUB_USERNAME/corporate-actions-demo.git"
    echo "✅ Remote added"
fi

# Set main as default branch
git branch -M main

echo ""
echo "📋 Next steps:"
echo ""
echo "1. Create a new repository on GitHub:"
echo "   → Go to: https://github.com/new"
echo "   → Repository name: corporate-actions-demo"
echo "   → Description: Corporate action processing system demo"
echo "   → Make it Public"
echo "   → DO NOT initialize with README (we already have one)"
echo "   → Click 'Create repository'"
echo ""
echo "2. Push your code:"
echo "   → Run: git push -u origin main"
echo ""
echo "3. If you get authentication errors:"
echo "   → Use a Personal Access Token instead of password"
echo "   → Go to: https://github.com/settings/tokens"
echo "   → Generate new token (classic) with 'repo' scope"
echo "   → Use token as password when prompted"
echo ""
echo "Your repository will be at:"
echo "https://github.com/$GITHUB_USERNAME/corporate-actions-demo"
echo ""

# Check if GitHub CLI is installed
if command -v gh &> /dev/null; then
    echo "💡 TIP: You have GitHub CLI installed!"
    echo "   Run this to create repo and push in one command:"
    echo "   gh repo create corporate-actions-demo --public --source=. --remote=origin --push"
    echo ""
fi
