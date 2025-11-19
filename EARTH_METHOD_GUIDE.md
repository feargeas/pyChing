# Earth Method (土) - Personal Foundation Guide

The Earth Element casting method is unique among pyChing's five methods. It combines **your personal foundation** (earth.txt) with **your specific question** to produce readings that are both reproducible and deeply personal.

## The Planting Metaphor 🌱

```
Your earth.txt = The Soil (accumulated wisdom, personal foundation)
Your question  = The Seed (specific inquiry you plant)
Your hexagram  = The Fruit (reading that grows from their union)
```

The same seed planted in different soil produces different fruit.
The same seed planted in the same soil always produces the same fruit.
As your soil evolves, so do your readings.

---

## Philosophy

### Traditional I Ching View
In classical I Ching philosophy, the questioner and the question are not separate from the answer. The reading emerges from the entire context: who you are, what you ask, and when you ask it.

### Earth Method Implementation
The Earth method makes this philosophical principle **literal**:

1. **Your Foundation Matters**: Different people asking the same question receive different readings based on their unique earth.txt content
2. **Consistency for Contemplation**: The same question from the same person produces the same hexagram, allowing deep reflection over time
3. **Evolution Through Growth**: As you update your earth.txt to reflect personal growth, your readings naturally evolve with you

### Contrast with Other Methods

| Method | Question → Hexagram | Personal Foundation |
|--------|-------------------|---------------------|
| **Wood, Metal, Fire** | Random each time | Not considered |
| **Air** | True random (physical) | Not considered |
| **Earth** | Deterministic from question + earth.txt | **Core to the method** |

---

## How It Works

### Technical Process

1. **Read earth.txt**: Your personal foundation file at `~/.pyching/earth.txt`
2. **Combine with question**: `earth.txt + "\n" + question` → oracle seed
3. **Seed PRNG**: Python's random.Random() seeded with combined string
4. **Cast hexagram**: Deterministic "coin flips" generate reproducible hexagram

### Mathematical Property

```python
earth.txt + question → seed → PRNG state → hexagram

# Examples:
"Be cautious" + "Should I take this risk?" → seed_A → hexagram_52
"Be bold" + "Should I take this risk?" → seed_B → hexagram_34
"Be cautious" + "Should I take this risk?" → seed_A → hexagram_52  # Same!
```

The hexagram is a **deterministic function** of earth.txt + question.

---

## Setup and Configuration

### Automatic Setup

**On first use**, pyChing automatically creates `~/.pyching/earth.txt` with default content:

```
大哉乾元，萬物資始
Great is the Creative, the source of all things

The eight trigrams mark out the changes
```

This traditional I Ching passage serves as a neutral foundation until you customize it.

### Customization

**Location**: `~/.pyching/earth.txt`

**Edit with any text editor**:
```bash
nano ~/.pyching/earth.txt
# or
code ~/.pyching/earth.txt
# or
vim ~/.pyching/earth.txt
```

**No restrictions**:
- Any length (though a few paragraphs is ideal conceptually)
- Any text encoding (UTF-8 recommended for unicode)
- Any language (Chinese, English, mixed, etc.)
- Empty file allowed (falls back to question-only seed)

---

## What to Put in earth.txt

Your earth.txt should reflect **your personal foundation** - the accumulated wisdom, values, and philosophy that inform how you approach questions.

### Examples

**Minimalist**:
```
Be like water
```

**Philosophical Foundation**:
```
The Tao that can be told is not the eternal Tao
The name that can be named is not the eternal name
The nameless is the beginning of heaven and earth
The named is the mother of ten thousand things

My path: Seek truth with humility, act with compassion, embrace change
```

**Personal Values**:
```
Core principles I strive to embody:
- Listen more than I speak
- Question assumptions, including my own
- Value process over outcome
- Find balance between planning and spontaneity
- Remember that this too shall pass

Born: 1985-03-15
Current life phase: Learning to lead with wisdom, not force
```

**I Ching Traditional**:
```
元亨利貞 (yuan heng li zhen)
"Sublime success through correctness"

乾：元亨利貞
坤：元亨，利牝馬之貞

The Creative and Receptive, yang and yin,
The source and the form, together they spin.
```

**Mixed Cultural Wisdom**:
```
大哉乾元，萬物資始
Great is the Creative, the source of all things

As above, so below
As within, so without

The middle way between extremes
```

**Personal Journey**:
```
My journey thus far:
- Learned caution from failure
- Learned courage from fear
- Learned compassion from pain
- Now learning wisdom from experience

Questions I hold:
What is the right balance between ambition and acceptance?
How can I serve while still honoring my own needs?
```

### Guidelines

**Do**:
- ✅ Write what genuinely resonates with you
- ✅ Include philosophical principles you value
- ✅ Reference wisdom traditions that inform your worldview
- ✅ Note your current life phase or circumstances
- ✅ Use your native language or mixed languages
- ✅ Update it as you grow and change

**Don't**:
- ❌ Copy something that doesn't mean anything to you
- ❌ Overthink it - start simple, evolve over time
- ❌ Include sensitive personal information (it's a text file on your system)
- ❌ Worry about "getting it right" - there's no wrong answer

---

## Usage Examples

### Command Line

```bash
# Basic usage (uses question as seed + earth.txt)
python pyching_cli.py -m earth -q "What should I focus on today?"

# Custom seed (overrides question)
python pyching_cli.py -m earth -q "Question?" --seed "custom_seed_text"

# Compare readings with different earth.txt
# (Try editing earth.txt between casts)
python pyching_cli.py -m earth -q "Should I take this risk?"
# Edit earth.txt
python pyching_cli.py -m earth -q "Should I take this risk?"  # Different result!
```

### GUI

1. Launch pyChing: `python pyching.py`
2. Select **"earth"** from Method dropdown
3. **Seed field appears** showing "Seed (optional): [____] (defaults to question)"
4. Leave seed field empty to use question (recommended)
5. Click **"Cast New Hexagram"**
6. Enter your question
7. Receive your reading

**Note**: The seed field is for advanced users who want to test different seeds. For normal use, leave it empty and the question will automatically be used.

---

## Use Cases

### 1. Long-term Contemplation

**Scenario**: You have an important life question that deserves deep reflection.

**Practice**:
```bash
# Today
python pyching_cli.py -m earth -q "Should I change careers?"
> Hexagram 3 (Difficulty at the Beginning)

# Six months later, same question
python pyching_cli.py -m earth -q "Should I change careers?"
> Hexagram 3 (Difficulty at the Beginning)  # Same reading!

# Reflect: How has your understanding of this hexagram deepened?
# What new insights have you gained from living with this answer?
```

### 2. Personal vs Universal

**Scenario**: Compare how different people receive guidance on the same question.

**Alice's earth.txt**:
```
I value careful deliberation and caution in all things.
```

**Bob's earth.txt**:
```
Fortune favors the bold. Seize opportunities when they arise.
```

**Same question for both**:
```bash
# Alice
python pyching_cli.py -m earth -q "Should I take this business risk?"
> Hexagram 52 (Keeping Still, Mountain)

# Bob
python pyching_cli.py -m earth -q "Should I take this business risk?"
> Hexagram 34 (The Power of the Great)
```

Different foundations, different guidance! ✨

### 3. Tracking Personal Evolution

**Scenario**: Update earth.txt as you grow, see how readings evolve.

```bash
# Year 1: earth.txt contains "I seek security above all"
python pyching_cli.py -m earth -q "What is my purpose?"
> Hexagram 52 (Keeping Still)

# Year 3: You've grown, earth.txt now contains "I embrace change and growth"
python pyching_cli.py -m earth -q "What is my purpose?"
> Hexagram 32 (Duration) or similar

# The same question, but you've changed, so the reading changes with you
```

### 4. Reproducible Study

**Scenario**: Academic study of I Ching interpretation.

**Benefit**: You can share readings with others exactly:
```
Hexagram: 61 → 26
Question: "Should I pursue this path?"
Earth: [include earth.txt content]

Anyone can reproduce this exact reading for study and discussion.
```

### 5. Group Practice

**Scenario**: I Ching study group with shared foundation.

**Practice**:
```bash
# Everyone in the group uses the same earth.txt
# Creates shared "soil" while honoring individual questions

# Group earth.txt might contain:
# "We seek wisdom together, honoring both tradition and personal experience.
#  Our practice values: honesty, openness, mutual support."
```

---

## Testing and Verification

### Test Reproducibility

```bash
# Cast twice with same question
python pyching_cli.py -m earth -q "Test question A" > reading1.txt
python pyching_cli.py -m earth -q "Test question A" > reading2.txt
diff reading1.txt reading2.txt
# Should be identical (except timestamps)
```

### Test Personalization

```bash
# Save current earth.txt
cp ~/.pyching/earth.txt ~/.pyching/earth.txt.backup

# Test with different earth.txt content
echo "Foundation A" > ~/.pyching/earth.txt
python pyching_cli.py -m earth -q "Test question" > result_A.txt

echo "Foundation B" > ~/.pyching/earth.txt
python pyching_cli.py -m earth -q "Test question" > result_B.txt

# Compare - should be different hexagrams
grep "YOUR READING" result_A.txt
grep "YOUR READING" result_B.txt

# Restore original
mv ~/.pyching/earth.txt.backup ~/.pyching/earth.txt
```

### Test Empty Earth

```bash
# Test backward compatibility
echo -n "" > ~/.pyching/earth.txt
python pyching_cli.py -m earth -q "Question with empty earth"
# Should work - falls back to question-only seed
```

---

## Advanced Topics

### Multiple Earth Files

You might maintain different earth.txt files for different contexts:

```bash
# Personal divination
cp ~/.pyching/earth_personal.txt ~/.pyching/earth.txt

# Professional decisions
cp ~/.pyching/earth_professional.txt ~/.pyching/earth.txt

# Spiritual practice
cp ~/.pyching/earth_spiritual.txt ~/.pyching/earth.txt
```

### Shared Foundations

Study groups or families might share an earth.txt:

```bash
# Use a shared foundation file
cp /shared/family_iching_foundation.txt ~/.pyching/earth.txt
```

### Version Control

Track evolution of your earth.txt:

```bash
cd ~/.pyching
git init
git add earth.txt
git commit -m "Initial foundation"

# Later, after updating
git add earth.txt
git commit -m "Updated after major life transition"

# View history
git log --oneline earth.txt
```

### Unicode and Multilingual

Earth.txt fully supports unicode:

```
易經
周易
乾坤震巽坎離艮兌

☯️ Yin and Yang ☯️

The Tao ☯ The Way
```

---

## Comparison with Other Methods

| Aspect | Wood/Metal/Fire | Air | Earth |
|--------|----------------|-----|-------|
| **Randomness** | Algorithmic | True physical | Deterministic |
| **Reproducible** | No | No | Yes |
| **Personal** | No | No | Yes |
| **Network** | No | Yes | No |
| **Philosophy** | Oracle as random | Oracle as nature | Oracle as mirror |
| **Best for** | Daily divination | Maximum randomness | Long-term study |

### When to Use Each

**Use Wood/Metal/Fire/Air when**:
- You want fresh guidance each time
- You're doing daily divination
- You value unpredictability
- You see I Ching as external wisdom source

**Use Earth when**:
- You want to contemplate one reading deeply over time
- You value reproducibility for study
- You see I Ching as reflecting your own wisdom
- You want personalized readings
- You're working with same question across long timeframe

---

## Philosophical Depth

### The Mirror Metaphor

Other methods treat I Ching as a window to external wisdom.
Earth method treats I Ching as a **mirror** reflecting yourself.

Your earth.txt = who you are
Your question = what you're grappling with
Your hexagram = the wisdom that emerges from their union

### The Garden Metaphor

Think of your earth.txt as a garden:
- You tend it over time
- You plant seeds (questions) in it
- Each seed grows according to the soil
- The same seed grows differently in different gardens
- Your garden evolves as you evolve

### The Teacher Metaphor

Imagine I Ching as a teacher who:
- Knows your foundation (earth.txt)
- Hears your question
- Provides guidance tailored to **both**

Same question from beginner vs master → different guidance.

---

## Frequently Asked Questions

### Q: Can I use the default earth.txt?
**A**: Yes! It's a beautiful traditional passage. But personalizing it makes the method more powerful.

### Q: How often should I update earth.txt?
**A**: Whenever you feel you've significantly grown or changed. Could be monthly, yearly, or after major life events.

### Q: What if I make earth.txt too long?
**A**: Technically no limit, but conceptually a few paragraphs is ideal. If it's 10 pages, maybe distill the essence.

### Q: Can earth.txt be empty?
**A**: Yes - falls back to question-only seed (backward compatible). But you lose the personalization feature.

### Q: Will editing earth.txt change old readings?
**A**: Yes! If you recast the same question with new earth.txt, you'll get a different hexagram. This is intentional - you've grown, your readings evolve.

### Q: Can two people have the same hexagram with Earth method?
**A**: Only if they have identical earth.txt AND ask identical questions. Very unlikely!

### Q: Is this deterministic approach "legitimate" I Ching?
**A**: I Ching has been practiced many ways for 3000+ years. Earth method honors the principle that the questioner and question are not separate from the answer.

### Q: How is this different from just using the same seed each time?
**A**: earth.txt is your personal foundation that ALL your questions draw from. Each question is still unique (different seed), but all are informed by your foundation.

---

## Troubleshooting

### earth.txt not being read
```bash
# Check file exists and is readable
ls -la ~/.pyching/earth.txt
cat ~/.pyching/earth.txt

# Check encoding if unicode isn't displaying
file ~/.pyching/earth.txt
# Should say "UTF-8 Unicode text"
```

### Readings not reproducible
```bash
# Ensure exact same question text (including punctuation, case)
# Ensure earth.txt hasn't changed between casts
# Verify you're using Earth method

# Debug: Check what's being read
python -c "from pathlib import Path; print(Path.home() / '.pyching' / 'earth.txt').read_text())"
```

### Unicode/encoding issues
```bash
# Ensure earth.txt is UTF-8
file ~/.pyching/earth.txt

# Re-save as UTF-8
iconv -f ISO-8859-1 -t UTF-8 ~/.pyching/earth.txt > ~/.pyching/earth.txt.utf8
mv ~/.pyching/earth.txt.utf8 ~/.pyching/earth.txt
```

---

## Poetic Closing

```
The seed you plant contains your question
The earth you plant it in contains yourself
The fruit that grows contains your answer

Not random, not fixed
Not external, not internal
But emerging from the union

The same seed in different soil → different fruit
The same seed in the same soil → same fruit
Change the soil and watch your garden transform

This is the Way of Earth (土)
Grounded, personal, evolving
```

---

## Further Reading

- See `pyching/casting/earth.py` for technical implementation
- See `PROJECT_COMPLETE.md` for overview of all five methods
- See main README for general pyChing documentation

**May your questions take root in fertile soil, and may the fruits of wisdom nourish your path!** 🌱 🌍 ✨
