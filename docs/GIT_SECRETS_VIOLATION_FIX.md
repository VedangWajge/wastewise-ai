# Git Push Violation Fix - Remove Secrets from Repository

## Problem

Git push is being rejected with a violation error. This happens when GitHub detects API keys, passwords, or other secrets in your commits.

**Error might look like:**
```
remote: error: GH013: Repository rule violations found
remote: Commit contains secrets or API keys
remote: Push declined due to repository rule violation
```

## Why This Happens

Your repository contains sensitive data in:
1. ✗ `.env` file committed to git
2. ✗ API keys hardcoded in documentation (`.md` files)
3. ✗ Secrets in Postman environment files
4. ✗ Database files with user data

## Quick Fix (Step-by-Step)

### Step 1: Remove Secrets from Documentation

Run the secret removal script:

```bash
cd E:\Vedang\STUDY\Programming\com.vedang.play\V2WEngg\MajorProjsem7and8\wastewise

python remove_secrets.py
```

This will automatically replace all API keys in `.md` files with placeholders.

**What it replaces:**
- ✓ Google Gemini API keys (`AIzaSy...`)
- ✓ OpenAI API keys (`sk-proj-...`, `sk-...`)
- ✓ Hugging Face tokens (`hf_...`)
- ✓ Razorpay keys (`rzp_test_...`, `rzp_live_...`)

### Step 2: Remove Committed .env File

If `.env` file was committed, remove it from git history:

```bash
# Remove .env from git tracking (keeps local file)
git rm --cached backend/.env
git rm --cached backend/.env.example
git rm --cached .env

# Or remove from entire history (more thorough)
git filter-branch --force --index-filter \
  "git rm --cached --ignore-unmatch backend/.env" \
  --prune-empty --tag-name-filter cat -- --all
```

### Step 3: Remove Postman Environment Files

These often contain access tokens:

```bash
git rm --cached WasteWise_Environment.postman_environment.json
git rm --cached FINAL_WasteWise.postman_environment.json
```

### Step 4: Remove Database Files

Database files may contain user data:

```bash
git rm --cached backend/wastewise.db
git rm --cached *.db
```

### Step 5: Verify .gitignore

Ensure `.gitignore` contains:

```gitignore
# Environment files
.env
.env.*
backend/.env
frontend/.env

# Secrets
*.pem
*.key
*secrets*
*credentials*

# Postman environment files
*.postman_environment.json

# Database files
*.db
*.sqlite
wastewise.db
```

Already updated! ✓

### Step 6: Create Safe Commit

```bash
# Add changes
git add .gitignore
git add backend/.env.example
git add *.md
git add remove_secrets.py

# Create commit
git commit -m "Security: Remove secrets and API keys from repository

- Replaced API keys in documentation with placeholders
- Removed .env files from git tracking
- Updated .gitignore to prevent future leaks
- Added secret removal script"
```

### Step 7: Force Push (if needed)

⚠️ **WARNING**: Only do this if you're the only person working on this repository!

```bash
# Force push to overwrite history
git push origin main --force
```

Or safer option:

```bash
# Create a new branch without secrets
git checkout -b clean-main
git push origin clean-main

# Then on GitHub:
# 1. Go to Settings → Branches
# 2. Change default branch to clean-main
# 3. Delete old main branch
```

## Long-Term Fix: Secure Your Secrets

### 1. Environment Variables Only

**Never commit:**
- `.env` files
- API keys in code
- Passwords
- Database connection strings
- Access tokens

**Always use:**
- `.env` for local development
- `.env.example` with placeholder values
- Environment variables in production

### 2. Use .env.example Template

Create/update `backend/.env.example`:

```env
# AI Provider Configuration
GEMINI_API_KEY=your_gemini_api_key_here
OPENAI_API_KEY=your_openai_api_key_here
HUGGINGFACE_API_KEY=your_huggingface_api_key_here

# Payment Gateway
RAZORPAY_KEY_ID=your_razorpay_key_id
RAZORPAY_KEY_SECRET=your_razorpay_key_secret

# Database
DATABASE_URL=sqlite:///wastewise.db

# Flask
SECRET_KEY=your-secret-key-here
JWT_SECRET_KEY=your-jwt-secret-key
```

### 3. Documentation Best Practices

When writing documentation, use placeholders:

```markdown
# ❌ BAD
GEMINI_API_KEY=AIzaSyXXXXXXXXXX[REDACTED_SECRET]

# ✅ GOOD
GEMINI_API_KEY=your_gemini_api_key_here
# Get your key from: https://makersuite.google.com/app/apikey
```

### 4. Set Up Pre-commit Hook

Create `.git/hooks/pre-commit`:

```bash
#!/bin/bash

# Check for secrets before commit
if grep -r "AIzaSy\|sk-proj-\|hf_\|rzp_" --exclude-dir=.git --include="*.md" .; then
    echo "❌ ERROR: Found API keys in files!"
    echo "Run: python remove_secrets.py"
    exit 1
fi

echo "✅ No secrets detected"
exit 0
```

Make it executable:
```bash
chmod +x .git/hooks/pre-commit
```

## Regenerate Compromised Keys

⚠️ **IMPORTANT**: If API keys were pushed to GitHub, they are compromised!

### 1. Google Gemini API Key

1. Go to: https://makersuite.google.com/app/apikey
2. Click on compromised key → Delete
3. Create new API key
4. Update `backend/.env`:
   ```env
   GEMINI_API_KEY=new_key_here
   ```

### 2. OpenAI API Key

1. Go to: https://platform.openai.com/api-keys
2. Revoke compromised key
3. Create new secret key
4. Update `backend/.env`:
   ```env
   OPENAI_API_KEY=new_key_here
   ```

### 3. Hugging Face Token

1. Go to: https://huggingface.co/settings/tokens
2. Revoke compromised token
3. Create new access token
4. Update `backend/.env`:
   ```env
   HUGGINGFACE_API_KEY=new_token_here
   ```

### 4. Razorpay Keys

1. Go to: https://dashboard.razorpay.com/app/keys
2. Generate new test/live keys
3. Update `backend/.env`:
   ```env
   RAZORPAY_KEY_ID=new_key_id
   RAZORPAY_KEY_SECRET=new_key_secret
   ```

## Alternative: Use GitHub Secrets

For public repositories, use GitHub Actions with secrets:

1. Go to: Repository → Settings → Secrets and variables → Actions
2. Click "New repository secret"
3. Add each secret:
   - `GEMINI_API_KEY`
   - `OPENAI_API_KEY`
   - `RAZORPAY_KEY_ID`
   - etc.

4. Reference in workflows:
   ```yaml
   env:
     GEMINI_API_KEY: ${{ secrets.GEMINI_API_KEY }}
   ```

## Verify Clean Repository

Check that no secrets remain:

```bash
# Search for API key patterns
git grep "AIzaSy"
git grep "sk-proj-"
git grep "hf_"
git grep "rzp_test_"

# If any results, fix them before committing
```

## Files to Check

Run this checklist:

```bash
# Check these files don't contain secrets
cat backend/.env.example  # Should have placeholders only
cat *.md                  # Should have placeholders only
cat *.postman_collection.json  # Should NOT contain tokens

# These files should NOT be in git
git ls-files | grep ".env$"            # Should be empty
git ls-files | grep "wastewise.db"     # Should be empty
git ls-files | grep "*environment.json" # Should be empty
```

## Summary of Actions

### Immediate Actions (Do Now)

- [x] 1. Run `python remove_secrets.py`
- [ ] 2. Remove `.env` from git: `git rm --cached backend/.env`
- [ ] 3. Remove database: `git rm --cached backend/wastewise.db`
- [ ] 4. Remove Postman envs: `git rm --cached *environment.json`
- [ ] 5. Verify .gitignore updated
- [ ] 6. Commit changes
- [ ] 7. Force push (if needed)

### Security Actions (Do Today)

- [ ] 1. Regenerate all API keys that were exposed
- [ ] 2. Update `backend/.env` with new keys
- [ ] 3. Test application still works
- [ ] 4. Set up pre-commit hook
- [ ] 5. Review GitHub security alerts

### Best Practices (Going Forward)

- [ ] 1. Never commit `.env` files
- [ ] 2. Use placeholders in documentation
- [ ] 3. Use `.env.example` for templates
- [ ] 4. Run `python remove_secrets.py` before commits
- [ ] 5. Use GitHub Secrets for CI/CD

## Quick Reference Commands

```bash
# Remove secrets from docs
python remove_secrets.py

# Remove file from git but keep locally
git rm --cached <file>

# Remove file from entire git history
git filter-branch --force --index-filter \
  "git rm --cached --ignore-unmatch <file>" \
  --prune-empty --tag-name-filter cat -- --all

# Check for secrets
git grep "AIzaSy\|sk-proj-\|hf_\|rzp_"

# Force push (careful!)
git push origin main --force

# Clean up references
git gc --aggressive --prune=now
```

## Getting Help

If you're still stuck:

1. **Check GitHub error message**: It will tell you which file/commit contains secrets
2. **Use BFG Repo-Cleaner**: https://rtyley.github.io/bfg-repo-cleaner/
3. **Contact GitHub Support**: They can help with violations

## Tools & Resources

- **Secret Scanner**: https://github.com/trufflesecurity/trufflehog
- **BFG Repo-Cleaner**: https://rtyley.github.io/bfg-repo-cleaner/
- **Git Filter-Branch**: https://git-scm.com/docs/git-filter-branch
- **GitHub Secrets Docs**: https://docs.github.com/en/actions/security-guides/encrypted-secrets

## Prevention Checklist

Before every commit:

```bash
# 1. Check for secrets
python remove_secrets.py

# 2. Verify .env not staged
git status | grep ".env"

# 3. Review what you're committing
git diff --staged

# 4. Use meaningful commit message
git commit -m "Descriptive message without secrets"

# 5. Push
git push origin main
```

## Emergency: Already Pushed Secrets?

If you already pushed secrets to a public repository:

**Do this IMMEDIATELY:**

1. **Revoke ALL exposed API keys** (within 5 minutes)
2. **Change ALL passwords** mentioned in commits
3. **Rotate ALL secrets** in your application
4. **Monitor API usage** for suspicious activity
5. **Enable billing alerts** to catch unauthorized usage

Then clean the repository as described above.

## Status

After following this guide:

- ✅ Secrets removed from documentation
- ✅ .gitignore updated
- ✅ .env files untracked
- ✅ Secret removal script created
- ✅ Safe to push to GitHub

Good luck! 🔒
