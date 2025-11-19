# Air Method Setup Guide - RANDOM.ORG True RNG

The Air Element (風/氣) casting method uses RANDOM.ORG's true random number generator, which is based on atmospheric noise measurements. This provides genuine physical randomness rather than algorithmic pseudo-randomness.

## What is RANDOM.ORG?

RANDOM.ORG is a service that generates truly random numbers from atmospheric noise, which is measured by radio receivers tuned to an unused frequency. This is different from the algorithmic randomness used by computers, making it the only pyChing method that provides genuine physical randomness.

**Characteristics:**
- **Element:** Air (風/氣)
- **Source:** Atmospheric noise (physical phenomenon)
- **Quality:** True random (not pseudo-random)
- **Requirements:** Internet connection + API key
- **Speed:** Slower than local methods (network latency)

## When to Use Air Method

**Best For:**
- Users who want the highest quality randomness
- Divination practitioners who value physical randomness
- Important life decisions where you want true cosmic randomness
- Philosophical preference for non-algorithmic randomness

**Consider Alternatives If:**
- No internet connection → Use **Fire** method (cryptographic CSPRNG)
- Need fast casting → Use **Metal** method (OS entropy)
- Need reproducible readings → Use **Earth** method (seeded)
- Want original pyChing algorithm → Use **Wood** method (backward compatible)

## Setup Instructions

### Step 1: Register for API Key

1. Visit the RANDOM.ORG dashboard:
   ```
   https://api.random.org/dashboard
   ```

2. Create an account or log in if you already have one:
   - Email address (for account verification)
   - Choose a password
   - Accept terms of service
   - Complete CAPTCHA

3. Check your email for verification link and click it

4. Log in to your RANDOM.ORG account

5. **Important:** Choose "Developer" account type to get API access
   - This is required to generate and use API keys

6. Navigate to API Keys section and generate/copy your API key
   - It will look something like: `12345678-abcd-ef12-3456-7890abcdef12`

### Step 2: Save API Key to pyChing

**Option A: Configuration File (Recommended)**

1. Create the pyChing configuration directory if it doesn't exist:
   ```bash
   mkdir -p ~/.pyching
   ```

2. Save your API key to the configuration file:
   ```bash
   echo "YOUR_API_KEY_HERE" > ~/.pyching/random_org_api_key
   ```

   Replace `YOUR_API_KEY_HERE` with your actual API key.

3. Verify the file was created correctly:
   ```bash
   cat ~/.pyching/random_org_api_key
   ```

   You should see just your API key on a single line, nothing else.

**Option B: Environment Variable**

Alternatively, you can set an environment variable:

```bash
export RANDOM_ORG_API_KEY="YOUR_API_KEY_HERE"
```

To make this permanent, add it to your shell configuration file (`~/.bashrc`, `~/.zshrc`, etc.).

### Step 3: Test the Connection

**From GUI:**

1. Launch pyChing GUI:
   ```bash
   python pyching.py
   ```

2. Select "Air" from the Method dropdown

3. Click "Cast New Hexagram"

4. If configured correctly, you'll get a hexagram using true random numbers from atmospheric noise

5. If there's an error, check the error message for troubleshooting guidance

**From CLI:**

```bash
python pyching_cli.py -m air -q "Is the Air method working?"
```

If successful, you'll see your reading. If there's an error, you'll get a helpful message explaining what to fix.

## Usage Quota

RANDOM.ORG free API keys have usage quotas:

- **Daily Quota:** 1,000 requests per day (more than enough for personal I Ching use)
- **Rate Limit:** Requests are throttled to prevent abuse
- **Quota Monitoring:** Check your usage at https://api.random.org/dashboard

**For I Ching Casting:**
- Each hexagram requires 6 line casts
- Each line cast uses 1 API request (3 coin flips per request)
- You can cast approximately **166 hexagrams per day** on the free tier
- This is far more than most users need

If you exceed your quota, pyChing will show an error message and suggest using the Fire method as an alternative.

## Troubleshooting

### Error: "RANDOM.ORG API key not configured"

**Problem:** API key file not found or empty

**Solution:**
1. Check if the file exists: `ls -l ~/.pyching/random_org_api_key`
2. Check if it contains your key: `cat ~/.pyching/random_org_api_key`
3. Make sure there are no extra spaces or newlines
4. Verify the key is exactly as shown in your RANDOM.ORG dashboard

### Error: "Cannot reach RANDOM.ORG"

**Problem:** Network connection issue

**Solution:**
1. Check your internet connection
2. Verify you can access https://www.random.org in a web browser
3. Check if a firewall is blocking HTTPS requests
4. Try using the Fire method as an offline alternative

### Error: "RANDOM.ORG API error (403): Invalid API key"

**Problem:** API key is incorrect or has been revoked

**Solution:**
1. Log in to https://api.random.org/dashboard
2. Verify your API key is still active
3. Copy the key again (carefully, including all dashes)
4. Update the configuration file with the correct key
5. Make sure there are no spaces before/after the key in the file

### Error: "RANDOM.ORG API error (402): Quota exceeded"

**Problem:** You've used your daily quota

**Solution:**
1. Wait until the quota resets (midnight UTC)
2. Check usage at https://api.random.org/dashboard
3. Consider upgrading to a paid plan if you need more requests
4. Use Fire method as an alternative for unlimited local casting

### Error: "requests library not installed"

**Problem:** Missing Python dependency

**Solution:**
```bash
pip install requests
```

## Command Line Usage Examples

```bash
# Basic usage with Air method
python pyching_cli.py -m air -q "What should I focus on today?"

# Compare Air method with other methods
python pyching_cli.py -m air -q "Question?" --save air_reading.json
python pyching_cli.py -m fire -q "Question?" --save fire_reading.json

# Use Air method with source comparison
python pyching_cli.py -m air --compare canonical,wilhelm_baynes -q "Question?"
```

## GUI Usage

1. Launch pyChing: `python pyching.py`
2. Select **Air** from the Method dropdown at the top
3. Select your preferred source (canonical, wilhelm_baynes, etc.)
4. Click **Cast New Hexagram**
5. Enter your question when prompted
6. Wait a moment for the network request to complete
7. View your reading with true random atmospheric noise

## Technical Details

**API Endpoint:** https://api.random.org/json-rpc/4/invoke

**Protocol:** JSON-RPC 2.0

**Request Format:**
- Method: `generateIntegers`
- Parameters: n=3 (coins), min=2 (yin), max=3 (yang)

**Response Format:**
- JSON object with `result.random.data` array containing [2 or 3, 2 or 3, 2 or 3]

**Conversion to Line Values:**
- Three coins are summed: total of 6-9
- 6 = Old Yin (moving/changing yin line)
- 7 = Young Yang (stable yang line)
- 8 = Young Yin (stable yin line)
- 9 = Old Yang (moving/changing yang line)

## Privacy and Security

- Your API key is stored locally on your computer
- pyChing does not send any personal information to RANDOM.ORG
- Your I Ching questions are not transmitted (only random number requests)
- RANDOM.ORG logs basic usage statistics for quota management
- Read RANDOM.ORG's privacy policy: https://www.random.org/privacy/

## Alternative Methods

If the Air method doesn't suit your needs, pyChing offers four other methods:

| Method | Randomness Source | Internet Required | Quality Level |
|--------|------------------|-------------------|---------------|
| **Wood** | Python PRNG | No | Good (original algorithm) |
| **Metal** | OS entropy (urandom) | No | High quality |
| **Fire** | Cryptographic CSPRNG | No | Cryptographic quality |
| **Earth** | Seeded deterministic | No | Reproducible |
| **Air** | Atmospheric noise | Yes | True random |

See the main documentation for details on each method.

## Support

If you encounter issues:

1. Check this documentation first
2. Verify your API key at https://api.random.org/dashboard
3. Test with Fire method to ensure pyChing is working: `python pyching_cli.py -m fire -q "Test?"`
4. Check pyChing GitHub issues: https://github.com/[your-repo]/pyChing/issues
5. Contact RANDOM.ORG support for API-specific issues: https://www.random.org/contact/

## Acknowledgments

**RANDOM.ORG** - Mads Haahr, Trinity College Dublin
- Providing free true random number service since 1998
- Making physical randomness accessible to everyone
- Supporting scientific research and education

---

**May your readings be guided by true cosmic randomness from the atmosphere itself!** 🌬️ ☁️ ⚛️
