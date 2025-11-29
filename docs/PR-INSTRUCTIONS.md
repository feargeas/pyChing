# How to Submit PR to clovemedia/i_ching

This guide walks you through submitting the typo fixes to the upstream repository.

## Quick Summary

You found 2 typos in the clovemedia/i_ching HTML source:
1. **Hexagram 47**: "goof fortune" → "good fortune"
2. **Hexagram 38**: "THE IMAGE." → "THE IMAGE" (extra period)

## Method 1: Using the Patch File (Recommended)

### Step 1: Fork and Clone the Repository

```bash
# Go to https://github.com/clovemedia/i_ching and click "Fork"
# Then clone YOUR fork:
git clone https://github.com/YOUR_USERNAME/i_ching.git
cd i_ching
```

### Step 2: Create a Branch

```bash
git checkout -b fix-typos-hex38-47
```

### Step 3: Apply the Patch

```bash
# Copy the patch file to the i_ching directory, then:
git apply fix-typos-hexagram-38-47.patch

# Or if that doesn't work, try:
patch -p1 < fix-typos-hexagram-38-47.patch
```

### Step 4: Verify the Changes

```bash
# Check what changed:
git diff

# You should see:
# - Line 4732: "THE IMAGE." → "THE IMAGE"
# - Line 5774: "goof fortune" → "good fortune"
```

### Step 5: Commit and Push

```bash
git add I_Ching_Wilhelm_Baynes_Translation.html
git commit -m "Fix typos in hexagrams 38 and 47

- Hexagram 47: 'goof fortune' → 'good fortune'
- Hexagram 38: 'THE IMAGE.' → 'THE IMAGE' (remove extra period)

Both typos found during automated text extraction and verified
against the Wilhelm/Baynes 1950 print edition."

git push origin fix-typos-hex38-47
```

### Step 6: Create Pull Request

1. Go to your fork on GitHub: `https://github.com/YOUR_USERNAME/i_ching`
2. You'll see a banner saying "Compare & pull request" - click it
3. Fill in the PR details:

**Title:**
```
Fix typos in hexagrams 38 and 47
```

**Description:**
```markdown
## Summary
Fixed two typos found during automated extraction and verification:

1. **Hexagram 47, line 5774**: "goof fortune" → "good fortune"
2. **Hexagram 38, line 4732**: "THE IMAGE." → "THE IMAGE" (removed extra period)

## Context
- The "goof fortune" typo appears to be an OCR error from the original scan
- The period in "THE IMAGE." is inconsistent with all other hexagrams and breaks automated parsing

## Testing
- Verified fixes against Wilhelm/Baynes 1950 print edition
- Tested automated YAML extraction pipeline - both issues now resolved
- All 64 hexagrams parse correctly

## Impact
- Corrects text to match original Wilhelm/Baynes translation
- Enables reliable automated parsing and extraction
```

4. Click "Create pull request"

---

## Method 2: Manual Edit via GitHub Web Interface

If you prefer not to use git locally:

### Step 1: Fork the Repository
1. Go to https://github.com/clovemedia/i_ching
2. Click the "Fork" button (top right)

### Step 2: Edit the File
1. In YOUR fork, navigate to `I_Ching_Wilhelm_Baynes_Translation.html`
2. Click the pencil icon (Edit this file)
3. Find and fix line 4732:
   - Search for: `<p>THE IMAGE.</p>` (Ctrl+F)
   - Change to: `<p>THE IMAGE</p>`
4. Find and fix line 5774:
   - Search for: `goof fortune`
   - Change to: `good fortune`

### Step 3: Commit
1. Scroll to bottom
2. Commit message: `Fix typos in hexagrams 38 and 47`
3. Extended description:
```
- Hexagram 47: 'goof fortune' → 'good fortune'
- Hexagram 38: 'THE IMAGE.' → 'THE IMAGE' (remove extra period)
```
4. Select "Create a new branch" and name it `fix-typos-hex38-47`
5. Click "Propose changes"

### Step 4: Create PR
1. GitHub will redirect you to create a PR
2. Use the title and description from Method 1, Step 6 above
3. Click "Create pull request"

---

## After Submitting

- The maintainer may ask questions or request changes
- GitHub will notify you via email
- Once merged, your contribution will be part of the project!

## Files in This Directory

- `fix-typos-hexagram-38-47.patch` - The git patch file
- `PR-INSTRUCTIONS.md` - This file

## Notes

- The patch file line numbers (4732, 5774) are approximate and may vary slightly depending on the version
- If the patch doesn't apply cleanly, use Method 2 (manual edit) instead
- Both methods achieve the same result
