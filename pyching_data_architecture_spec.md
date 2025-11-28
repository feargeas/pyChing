# pyChing Data Architecture Specification

**Version:** 1.0  
**Date:** 2025-11-26  
**Purpose:** Comprehensive specification for migrating pyChing from JSON to YAML and adding multi-source I Ching interpretations.

---

## Executive Summary for Quick Start

**Current state:** pyChing uses JSON for Legge 1882 translation (64 files in `data/hexagrams/`)

**Goal:** Migrate to YAML, then add Wilhelm, Richmond (2 versions), and deKorne (2 levels)

**Why YAML?** Human-readable, multiline text without escaping, better for version control

**Migration path:**
1. **Create structure:** `mkdir -p data/sources/{legge,wilhelm,richmond,dekorne}` + add README
2. **Backup:** `cp -r data/hexagrams data/hexagrams.backup`
3. **Convert:** Run `tools/migrate_json_to_yaml.py` (create this script)
4. **Test:** Verify hex 17 YAML matches JSON content
5. **Update loader:** Change `pyching/data/loader.py` from JSON to YAML
6. **Validate:** All tests pass
7. **Delete JSON:** `rm -rf data/hexagrams/` once confident
8. **Add sources:** Drop wilhelm.txt, Richmond PDFs, deKorne .docs into `data/sources/`

**First action (do this now):**
```bash
# Create directory structure
mkdir -p data/sources/{legge,wilhelm,richmond/oracle_1985,richmond/language_of_lines,dekorne}
mkdir -p data/interpretations

# Copy this template to data/sources/README.md (see spec below)

# Then create tools/migrate_json_to_yaml.py
# Test on hexagram 17 only first
# See "Migration Script" section below for code
```

**Directory structure after migration:**
```
data/
├── interpretations/
│   ├── legge/           # Migrated from JSON
│   ├── wilhelm/         # Add later
│   ├── richmond/        # Add later (2 versions)
│   └── dekorne/         # Add later (simple + full)
└── sources_metadata.yaml
```

**Read this document when:**
- Writing migration script → See "Migration Script" section
- Adding new sources → See "Data Formats" and "Extraction Methods"
- Understanding architecture → See "Design Philosophy"

---

## Executive Summary

This document specifies a flexible, source-preserving data architecture for pyChing that:
- Maintains interpretive integrity of each source (no forced normalization)
- Supports multiple presentation levels (simple/full) within sources
- Enables comparative analysis across translations
- Accommodates sources ranging from terse poetic (Richmond) to extensive scholarly synthesis (deKorne)
- Uses YAML for human-readable, version-controllable storage
- Provides Python accessor pattern for programmatic access

## Context

### The Problem

I Ching interpretation sources vary dramatically in:
- **Epistemological approach:** Scholarly philological (Legge) vs. Jungian archetypal (Wilhelm) vs. Gnostic synthetic (deKorne) vs. phenomenological poetic (Richmond)
- **Structural complexity:** 3 sentences (Legge judgment) to 8 pages (deKorne full hexagram)
- **Multi-vocality:** Single translator vs. comparative synthesis of 10+ sources
- **Intertextuality:** Self-contained vs. extensive supporting quotations

### Sources Identified

1. **Legge** - Scholarly, Victorian philological
2. **Wilhelm/Baynes** - Jungian psychological depth, standard reference
3. **Richmond (2 versions)**
   - "The I Ching Oracle" (1985) - photocopy, simple oracle + moving lines
   - "The Language of the Lines" - poetic phenomenology, facing-pages design
4. **deKorne** - "Gnostic Book of Changes" - comparative synthesis of 10 sources + psychological/alchemical commentary

### Design Philosophy

**"Both, and..." epistemology** - Refuse binary reductions. Each source maintains its own structure internally while exposing standardized interface for querying. No forced normalization that obscures source characteristics.

## Directory Structure

**Migration strategy: JSON → YAML, then extend with new sources**

```
pyChing/                     # Your existing root
├── data/
│   ├── sources/             # NEW - raw source materials (staging area)
│   │   ├── wilhelm/
│   │   │   ├── wilhelm.txt           # Plain text web scrape
│   │   │   └── wilhelm_notes.md      # Extraction notes
│   │   │
│   │   ├── richmond/
│   │   │   ├── oracle_1985/
│   │   │   │   ├── page_58.pdf       # OCR source PDFs
│   │   │   │   ├── page_59.pdf
│   │   │   │   └── ... (all pages)
│   │   │   ├── language_of_lines/
│   │   │   │   └── language_of_lines.pdf  # Better quality scan
│   │   │   └── richmond_notes.md
│   │   │
│   │   ├── dekorne/
│   │   │   ├── Hexagram_01.doc       # Original .doc files
│   │   │   ├── Hexagram_02.doc
│   │   │   ├── ... (64 files)
│   │   │   └── dekorne_notes.md
│   │   │
│   │   ├── legge/
│   │   │   └── legge_sources.md      # Web links, references
│   │   │
│   │   └── README.md                 # What goes in sources/
│   │
│   ├── interpretations/     # PROCESSED - all YAML output
│   │   ├── legge/           # MIGRATED from hexagrams/*.json
│   │   │   ├── hexagram_01.yaml
│   │   │   └── ... (64 files)
│   │   │
│   │   ├── wilhelm/         # EXTRACTED from sources/wilhelm/
│   │   │   ├── hexagram_01.yaml
│   │   │   └── ... (64 files)
│   │   │
│   │   ├── richmond/        # EXTRACTED from sources/richmond/
│   │   │   ├── oracle_1985/
│   │   │   │   ├── hexagram_01.yaml
│   │   │   │   └── ...
│   │   │   └── language_of_lines/
│   │   │       ├── hexagram_01.yaml
│   │   │       └── ...
│   │   │
│   │   └── dekorne/         # EXTRACTED from sources/dekorne/
│   │       ├── simple/
│   │       │   ├── hexagram_01.yaml
│   │       │   └── ...
│   │       └── full/
│   │           ├── hexagram_01.yaml
│   │           └── ...
│   │
│   ├── hexagrams/           # DEPRECATED - remove after migration
│   │   └── hexagram_NN.json # Will be deleted after testing
│   │
│   ├── sources_metadata.yaml  # CONVERTED from .json
│   ├── mappings.yaml          # CONVERTED from .json
│   ├── svg/                   # KEEP - unchanged
│   └── README.md              # UPDATE - document YAML migration
│
├── pyching/
│   ├── core/                # UNCHANGED
│   │   ├── engine.py
│   │   ├── hexagram.py
│   │   ├── reading.py
│   │   └── __init__.py
│   │
│   ├── casting/             # UNCHANGED
│   │   ├── base.py
│   │   ├── earth.py, fire.py, metal.py, water.py, wood.py
│   │   └── registry.py
│   │
│   ├── data/
│   │   ├── loader.py        # MODIFIED - YAML only, multi-source
│   │   ├── resolver.py      # MODIFIED - .yaml paths
│   │   ├── sources.py       # NEW - accessor pattern
│   │   └── __init__.py
│   │
│   └── __init__.py
│
├── tools/
│   ├── migrate_json_to_yaml.py  # NEW - migration script
│   ├── extract_wilhelm.py       # EXISTING or NEW
│   ├── extract_richmond_pdf.py  # NEW
│   ├── extract_dekorne.py       # NEW
│   └── validate_yaml.py         # NEW - validate all YAML
│
└── tests/
    ├── test_yaml_migration.py   # NEW - verify JSON→YAML
    ├── test_sources.py          # NEW - multi-source tests
    └── ... (existing tests - update for YAML)
```

### Migration Path

**Phase 0: Backup**
```bash
cp -r data/hexagrams data/hexagrams.backup
git commit -am "Pre-YAML migration backup"
```

**Phase 1: Convert Legge JSON → YAML** (tools/migrate_json_to_yaml.py)
- Read all 64 hexagram_NN.json files
- Convert to YAML in data/interpretations/legge/
- Preserve exact structure, just change format

**Phase 2: Update loaders** (pyching/data/loader.py)
- Change from json.load() to yaml.safe_load()
- Update paths: hexagrams/*.json → interpretations/legge/*.yaml
- All tests pass

**Phase 3: Validate** (tests/test_yaml_migration.py)
- Load hexagram 17 from both JSON and YAML
- Verify identical content
- Test all 64 hexagrams
- All existing tests still pass

**Phase 4: Delete JSON** (once confident)
```bash
rm -rf data/hexagrams/
git commit -am "Completed JSON→YAML migration"
```

**Phase 5: Add new sources** (Wilhelm, Richmond, deKorne)
- Extract using tools/extract_*.py
- Add to data/interpretations/
- Extend loader for multi-source support

### data/sources/ Organization

The `data/sources/` directory stores **raw, unprocessed source materials**. Drop your PDFs, .doc files, text files, web links here organized by source.

**Create `data/sources/README.md`:**

```markdown
# I Ching Source Materials

Raw, unprocessed sources for YAML interpretation generation.

## Purpose

- **Archival**: Preserve originals for re-extraction
- **Provenance**: Document interpretation origins
- **Versioning**: Track editions used
- **Reproducibility**: Enable extraction verification

## Structure

### legge/
- `legge_sources.md` - Web links, Sacred Texts Archive
- Document 1882 edition specifics

### wilhelm/
- `wilhelm.txt` - http://www2.unipr.it/~deyoung/I_Ching_Wilhelm_Translation.html
- `wilhelm_baynes_1950.pdf` - Original if available
- `source_url.txt` - Web link

### richmond/oracle_1985/
- `page_*.pdf` - Typewriter photocopies (degraded, OCR + verify)

### richmond/language_of_lines/
- `page_82.png`, `page_83.png` - Better quality scans
- Facing-pages design

### dekorne/
- `Hexagram_01.doc` through `Hexagram_64.doc`
- 2001-2006 vintage Word files
- ~3500 words each

## Adding Sources

1. Create `data/sources/<source_name>/`
2. Add files (preserve original names/formats)
3. Create `<source_name>_notes.md`:
   - Full citation (author, title, year, edition)
   - Source URL/location
   - Format notes
   - Copyright status
   - Known issues
4. Document extraction date and any corrections

## File Naming

- PDFs: `author_title_year.pdf`
- Pages: `page_01.pdf`, `page_02.pdf`
- Text: `source_name.txt`
- Notes: `source_notes.md`
- Links: `source_url.txt`

## Copyright

Personal research/study only. Do not redistribute.

## Source Status

| Source | Year | Format | Extraction Status |
|--------|------|--------|-------------------|
| Legge | 1882 | JSON → YAML | Migrating |
| Wilhelm | 1950 | TXT | Pending |
| Richmond (Oracle) | 1985 | PDF scans | Pending OCR |
| Richmond (Language) | c.1985 | Images | Pending OCR |
| deKorne | 2001-06 | .doc | Pending |

Extract with `tools/extract_*.py` → outputs to `data/interpretations/`
```

## Data Formats (YAML Schemas)

### Legge Schema (Migrated from JSON)

**Target format for JSON→YAML migration:**

```yaml
# data/interpretations/legge/hexagram_17.yaml
# Converted from data/hexagrams/hexagram_17.json

metadata:
  hexagram: 17
  king_wen_sequence: 17
  fu_xi_sequence: 17
  binary: "011001"
  source: legge_1882

name: Souei
english_name: Submission to the Duty
title: "17. Souei / Submission to the Duty"

trigrams:
  upper: dui
  lower: zhen

judgment: |
  Souei indicates that under its conditions there will be great 
  progress and success. But it will be advantageous to be firm 
  and correct. There will then be no error.

image: |
  The trigram for the waters of a marsh and that for thunder 
  hidden in the midst of it, form Souei. The superior person in 
  accordance with this, when it is getting toward dark, enters 
  their house and rests.

lines:
  1:
    position: bottom
    type: nine
    text: |
      shows us one changing the object of their pursuit, but if 
      they are firm and correct, there will be good fortune. 
      Going beyond their own gate to find associates, they will 
      achieve merit.
  
  2:
    position: second
    type: six
    text: |
      shows us one who cleaves to the little child, and lets go 
      the person of age and experience.
  
  3:
    position: third
    type: six
    text: |
      shows us one who cleaves to the person of age and experience, 
      and lets go the little child. Such following will get what it 
      seeks; but it will be advantageous to adhere to what is firm 
      and correct.
  
  4:
    position: fourth
    type: nine
    text: |
      shows us one followed, and obtaining adherents. Though they 
      be firm and correct, there will be evil. If they be sincere 
      however in their course, and make that evident, into what 
      error can they fall?
  
  5:
    position: fifth
    type: nine
    text: |
      shows us the ruler sincere in fostering all that is excellent. 
      There will be good fortune.
  
  6:
    position: topmost
    type: six
    text: |
      shows us sincerity firmly held and clung to, yea, and bound 
      fast. We see the king with this presenting his offerings on 
      the western mountain.
```

**Key differences from JSON:**
- No `hexagram_id` field (redundant with filename)
- No nested `canonical` object (flattened to top level)
- Multiline strings use `|` block literal (no `\n` escaping)
- More readable, less verbose
- Same semantic content

### Minimal Schema (Richmond Oracle 1985, Simple extracts)

```yaml
# interpretations/richmond/oracle_1985/hex_17.yaml
metadata:
  hexagram: 17
  name: Following
  chinese: 隨
  source: Nigel Richmond
  work: The I Ching Oracle
  published: 1985
  
oracle:
  judgment: |
    Following.
    Supreme success.
    Continuance in the way is needed.
    No error.
  
  commentary: |
    Continuing to follow the life force, the tao,
    our circumstances, may sometimes seem to be an
    error of not asserting our individuality enough...

image:
  text: |
    Thunder in the middle of the lake
  
  manifestations:
    pattern: |
      The high is fed from below.
      This is service...
    
    nature: |
      Evolution is the devoted service
      of life to a form...
    
    human: |
      Our energy from inner depths
      supports the highest place...

lines:
  1:
    movement: yin
    text: |
      Line 1 goes yin - life force shows more change.
    
    interpretation: |
      Line 6 being yin we are following this
      emerging life force as it becomes more active...
  
  # ... lines 2-6
```

### Intermediate Schema (Wilhelm)

```yaml
# interpretations/wilhelm/hex_17.yaml
metadata:
  hexagram: 17
  name: Sui
  english: Following
  source: Richard Wilhelm
  translator: Cary F. Baynes

trigrams:
  above:
    name: Tui
    attribute: The Joyous, Lake
  below:
    name: Chên
    attribute: The Arousing, Thunder
  
  relationship: |
    Joy in movement induces following. The Joyous is 
    the youngest daughter, while the Arousing is the 
    eldest son...

judgment:
  text: |
    FOLLOWING has supreme success.
    Perseverance furthers. No blame.
  
  commentary: |
    In order to obtain a following one must first know 
    how to adapt oneself. If a man would rule he must 
    first learn to serve...

image:
  text: |
    Thunder in the middle of the lake:
    The image of FOLLOWING.
    Thus the superior man at nightfall
    Goes indoors for rest and recuperation.
  
  commentary: |
    In the autumn electricity withdraws into the earth 
    again and rests. Here it is the thunder in the middle 
    of the lake...

lines:
  1:
    position: Nine at the beginning
    text: |
      The standard is changing.
      Perseverance brings good fortune.
      To go out of the door in company
      Produces deeds.
    
    commentary: |
      There are exceptional conditions in which the 
      relation between leader and followers changes...
  
  # ... lines 2-6
```

### Complex Schema (deKorne Full)

```yaml
# interpretations/dekorne/full/hex_17.yaml
metadata:
  hexagram: 17
  name: Following
  chinese: 隨
  source: James deKorne
  work: Gnostic Book of Changes
  alternate_titles:
    - According With
    - Acquiring Followers
    - Adapting
    - "Learn to serve in order to rule (Hook)"
  
judgment:
  translations:
    legge: |
      Following indicates successful progress and no 
      error through firm correctness.
    
    wilhelm_baynes: |
      Following has supreme success. Perseverance 
      furthers. No blame.
    
    blofeld:
      text: |
        Following. Sublime success! Righteous persistence 
        brings reward -- no error!
      context: |
        [This sublime success comes, of course, only to 
        those who follow what is right...]
    
    liu: |
      Following. Great success. It is of benefit to 
      continue. No blame.
    
    ritsema_karcher:
      text: Following. Spring Growing Harvesting Trial. Without fault.
      context: |
        [This hexagram describes your situation in terms 
        of being impelled or drawn into moving forward...]
    
    shaughnessy: |
      Following: Prime receipt; beneficial to determine; 
      there is no trouble.
    
    cleary_1: |
      Following is greatly developmental: it is beneficial 
      if correct; then there is no fault.
    
    cleary_2: |
      Following is very successful, etc.
    
    wu: |
      Following is primordial, pervasive, prosperous, and 
      persevering. There will be no blame.
  
  confucian_commentary:
    legge: |
      In Following the dynamic trigram places itself under 
      the magnetic...
    
    wilhelm: |
      ...
  
  synthesis:
    notes_and_paraphrases: |
      Judgment: Following means advancement through willpower.
      
      The Superior Man rests on his inner virtue.
      
      In Following, the trigram of Movement "follows" the 
      trigram of Cheerfulness...
    
    supporting_quotes:
      - source: Fung Yu-Lan -- A Short History of Chinese Philosophy
        text: |
          At seventy ... Confucius allowed his mind to follow 
          whatever it desired, yet everything he did was 
          naturally right of itself...
      
      # ... additional quotes

image:
  translations:
    legge: |
      Thunder in the marsh: the image of Following. The 
      superior man, in accordance with this, at nightfall 
      enters his house and rests.
    
    wilhelm_baynes: |
      Thunder in the middle of the lake: the image of 
      Following. Thus the superior man at nightfall goes 
      indoors for rest and recuperation.
    
    # ... other translations
  
  synthesis:
    # Similar structure to judgment

lines:
  1:
    translations:
      legge: |
        The first line, dynamic, shows us one changing 
        the object of his pursuit...
      
      wilhelm_baynes: |
        The standard is changing. Perseverance brings 
        good fortune...
      
      # ... all 8-10 sources
    
    confucian_commentary:
      legge: |
        ...
      wilhelm: |
        ...
    
    notes_and_paraphrases:
      siu: |
        The man begins to change his allegiance...
      
      wing: |
        You are undergoing a change of standards...
      
      editor: |
        Line one is dynamic, indicating an active impulse 
        toward change...
      
      supporting_quotes:
        - source: Jung -- CW 5
          text: |
            The unconscious is the unwritten history of 
            mankind from time immemorial...
      
      summary: |
        A change in what one follows brings merit through 
        association with others.
  
  # ... lines 2-6

metadata_footer:
  last_revised: "March 26, 2001, 4/23/06"
```

### deKorne Simple (Extracted)

```yaml
# interpretations/dekorne/simple/hex_17.yaml
metadata:
  hexagram: 17
  name: Following
  source: James deKorne (simplified)
  note: Essences extracted from full version summaries

judgment:
  essence: Following means advancement through willpower.

lines:
  1:
    essence: A change in what one follows brings merit.
  2:
    essence: Immature attitudes preclude growth.
  3:
    essence: One exchanges an immature belief for a mature one.
  4:
    essence: Sincerity of motive is essential.
  5:
    essence: Attitude in accordance with advancement of the Work.
  6:
    essence: Devotion to the Work brings unity to the psyche.
```

### Richmond Language of Lines

```yaml
# interpretations/richmond/language_of_lines/hex_17.yaml
metadata:
  hexagram: 17
  name: Following
  source: Nigel Richmond
  work: The Language of the Lines
  published: c.1985
  note: Facing pages design - lines left, manifestations right

theme: Becoming. New form.

trigrams:
  upper: Kên
  lower: Chên
  also_present: [Sun, Tui]
  essence: |
    To fructify (Chên) a high place (Kên) 
    gently and firmly (Sun), awakens (Tui).

manifestations:
  pattern: |
    The high is fed from below.
    This is service,
    undemanding and constant,
    becoming an awakening.
  
  nature: |
    Evolution is the devoted service
    of life to a form.
    It is form in service to life.
  
  human: |
    Our energy from inner depths
    supports the highest place,
    the widest view.
    When established and firm
    there are new realizations.
  
  form: |
    To serve, we follow.
    We move towards that form,
    becoming it.

lines:
  1: |
    He makes new forms on the open plain.
    They are new realities to him;
    Sharing them, they become more real.
  
  2: |
    No new form for his feelings.
    He feels unchanged.
    Unchanging lacks experience.
  
  3: |
    By acting out we change our skin,
    but he holds back new growth,
    not acting out the old.
  
  4: |
    Is he his skin?
    Or is this only the boundary
    of what he thinks he is.
    To distinguish the superficial and the depth
    is his guide.
  
  5: |
    Where are his feelings? Forming his form,
    real to him. He can trust in this.
  
  6: |
    When not in transition he will teach.
    Seeing his quietness they long to learn.
```

## Migration Script (JSON → YAML)

### Phase 1: Convert Existing Legge Data

```python
# tools/migrate_json_to_yaml.py
"""
Migrate existing JSON hexagram data to YAML format

Input:  data/hexagrams/hexagram_NN.json (64 files)
Output: data/interpretations/legge/hexagram_NN.yaml (64 files)

Preserves exact structure, changes format only.
"""

import json
import yaml
from pathlib import Path

def migrate_all_hexagrams(json_dir='data/hexagrams', 
                          yaml_dir='data/interpretations/legge'):
    """Convert all 64 hexagrams from JSON to YAML"""
    
    json_dir = Path(json_dir)
    yaml_dir = Path(yaml_dir)
    yaml_dir.mkdir(parents=True, exist_ok=True)
    
    # Process each hexagram
    for i in range(1, 65):
        migrate_single_hexagram(i, json_dir, yaml_dir)

def migrate_single_hexagram(number, 
                            json_dir='data/hexagrams',
                            yaml_dir='data/interpretations/legge'):
    """Migrate a single hexagram (for testing)"""
    
    json_dir = Path(json_dir)
    yaml_dir = Path(yaml_dir)
    yaml_dir.mkdir(parents=True, exist_ok=True)
    
    json_file = json_dir / f'hexagram_{number:02d}.json'
    yaml_file = yaml_dir / f'hexagram_{number:02d}.yaml'
    
    # Load JSON
    with open(json_file, 'r') as f:
        data = json.load(f)
    
    # Optionally restructure for cleaner YAML
    # (or preserve exact structure)
    clean_data = restructure_if_desired(data)
    
    # Write YAML
    with open(yaml_file, 'w') as f:
        yaml.dump(clean_data, f, 
                 allow_unicode=True,
                 default_flow_style=False,
                 sort_keys=False,
                 width=80)
    
    print(f"Migrated hexagram {number:02d}: {data['canonical']['name']}")
    return yaml_file

def restructure_if_desired(json_data):
    """
    Optional: restructure for cleaner YAML
    Or just return as-is to preserve exact structure
    """
    
    # Option 1: Return as-is
    # return json_data
    
    # Option 2: Flatten/clean structure
    return {
        'metadata': {
            'hexagram': json_data['number'],
            'king_wen_sequence': json_data['king_wen_sequence'],
            'fu_xi_sequence': json_data['fu_xi_sequence'],
            'binary': json_data['binary'],
            'source': json_data['canonical']['source_id']
        },
        
        'name': json_data['canonical']['name'],
        'english_name': json_data['canonical']['english_name'],
        
        'trigrams': json_data['trigrams'],
        
        'judgment': json_data['canonical']['judgment'],
        'image': json_data['canonical']['image'],
        
        'lines': {
            i: {
                'position': line['position'],
                'type': line['type'],
                'text': line['text']
            }
            for i, line in json_data['canonical']['lines'].items()
        }
    }

def verify_migration(json_dir='data/hexagrams',
                    yaml_dir='data/interpretations/legge'):
    """Verify JSON and YAML contain same data"""
    
    json_dir = Path(json_dir)
    yaml_dir = Path(yaml_dir)
    
    errors = []
    
    for i in range(1, 65):
        json_file = json_dir / f'hexagram_{i:02d}.json'
        yaml_file = yaml_dir / f'hexagram_{i:02d}.yaml'
        
        with open(json_file, 'r') as f:
            json_data = json.load(f)
        
        with open(yaml_file, 'r') as f:
            yaml_data = yaml.safe_load(f)
        
        # Compare critical fields
        if not verify_hexagram(json_data, yaml_data):
            errors.append(f"Hexagram {i:02d} mismatch")
    
    if errors:
        print("ERRORS FOUND:")
        for error in errors:
            print(f"  - {error}")
        return False
    else:
        print("✓ All 64 hexagrams verified - JSON matches YAML")
        return True

def verify_hexagram(json_data, yaml_data):
    """Verify single hexagram migration"""
    # Implement field-by-field comparison
    # based on your restructuring choice
    return True  # placeholder

if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser()
    parser.add_argument('--verify', action='store_true',
                       help='Verify migration instead of running it')
    parser.add_argument('--single', type=int,
                       help='Migrate only single hexagram (for testing)')
    args = parser.parse_args()
    
    if args.verify:
        verify_migration()
    elif args.single:
        # Test on single hexagram first
        migrate_single_hexagram(args.single)
        print(f"\nTest hex {args.single} - check YAML manually")
    else:
        migrate_all_hexagrams()
        verify_migration()
```

### Validation Checklist

**After running migration script, verify:**

```bash
# 1. Check YAML was created
ls data/interpretations/legge/hexagram_17.yaml

# 2. View YAML content (should be human-readable)
cat data/interpretations/legge/hexagram_17.yaml

# 3. Compare JSON vs YAML programmatically
python3 << 'EOF'
import json
import yaml

# Load JSON
with open('data/hexagrams/hexagram_17.json') as f:
    json_data = json.load(f)

# Load YAML
with open('data/interpretations/legge/hexagram_17.yaml') as f:
    yaml_data = yaml.safe_load(f)

# Check judgment text matches
json_judgment = json_data['canonical']['judgment']
yaml_judgment = yaml_data['judgment']

if json_judgment.strip() == yaml_judgment.strip():
    print("✓ Judgment matches")
else:
    print("✗ Judgment differs!")
    print(f"JSON: {json_judgment[:50]}...")
    print(f"YAML: {yaml_judgment[:50]}...")

# Check line count
json_lines = len(json_data['canonical']['lines'])
yaml_lines = len(yaml_data['lines'])

if json_lines == yaml_lines == 6:
    print(f"✓ All {yaml_lines} lines present")
else:
    print(f"✗ Line count mismatch: JSON={json_lines}, YAML={yaml_lines}")

# Check metadata
if json_data['number'] == yaml_data['metadata']['hexagram']:
    print("✓ Hexagram number matches")
else:
    print("✗ Metadata mismatch")

print("\nIf all checks pass, migration successful for hex 17")
EOF

# 4. Test with existing loader (before modifying it)
python3 << 'EOF'
import sys
import json

# Load using current JSON loader
sys.path.insert(0, '.')
from pyching.data.loader import load_hexagram_data

try:
    data = load_hexagram_data(17)
    print("✓ Current loader still works with JSON")
    print(f"  Loaded: {data.get('canonical', {}).get('name', 'N/A')}")
except Exception as e:
    print(f"✗ Loader failed: {e}")
EOF

# 5. After updating loader to YAML, test again
python3 << 'EOF'
import sys
sys.path.insert(0, '.')
from pyching.data.loader import HexagramDataLoader

loader = HexagramDataLoader()
data = loader.get_hexagram(17, source='legge')

print("✓ New YAML loader works")
print(f"  Name: {data['name']}")
print(f"  Judgment: {data['judgment'][:60]}...")
print(f"  Lines: {len(data['lines'])}")
EOF
```

**Success criteria:**
- [ ] All 64 YAML files created
- [ ] Judgment text identical between JSON/YAML
- [ ] All 6 lines present in each hexagram
- [ ] Metadata preserved (hexagram number, trigrams, etc.)
- [ ] YAML is human-readable (no escape sequences)
- [ ] Existing tests still pass after loader update
- [ ] Performance acceptable (YAML loads quickly)

**If any check fails:**
1. Don't delete JSON yet
2. Fix migration script
3. Delete YAML output
4. Re-run migration
5. Re-test

**When confident:**
```bash
# Final commit before deleting JSON
git add data/interpretations/legge/
git commit -m "Add YAML interpretations (Legge)"

# Verify tests pass
pytest tests/

# Delete JSON
rm -rf data/hexagrams/
git commit -am "Remove JSON (migration to YAML complete)"

# Keep backup for one week, then:
# rm -rf data/hexagrams.backup
```

### Phase 2: Update Loader for YAML

```python
# pyching/data/loader.py (modified)
"""Updated loader - YAML only, multi-source support"""

import yaml
from pathlib import Path

class HexagramDataLoader:
    """Load hexagram interpretations from YAML sources"""
    
    def __init__(self, data_dir='data'):
        self.data_dir = Path(data_dir)
        self.interpretations_dir = self.data_dir / 'interpretations'
        self.cache = {}
        
        # Load sources metadata
        metadata_file = self.data_dir / 'sources_metadata.yaml'
        with open(metadata_file, 'r') as f:
            self.sources_metadata = yaml.safe_load(f)
    
    def get_hexagram(self, number, source='legge', **kwargs):
        """Load hexagram from specified source
        
        Args:
            number: Hexagram number (1-64)
            source: Source name ('legge', 'wilhelm', 'richmond', 'dekorne')
            **kwargs: Source-specific options (version, level, etc.)
        
        Returns:
            dict: Hexagram data
        """
        
        # Build cache key
        cache_key = f"{source}_{number}"
        if kwargs:
            cache_key += f"_{'_'.join(f'{k}={v}' for k,v in kwargs.items())}"
        
        # Check cache
        if cache_key in self.cache:
            return self.cache[cache_key]
        
        # Determine file path based on source
        file_path = self._resolve_path(source, number, **kwargs)
        
        # Load YAML
        with open(file_path, 'r') as f:
            data = yaml.safe_load(f)
        
        # Cache and return
        self.cache[cache_key] = data
        return data
    
    def _resolve_path(self, source, number, **kwargs):
        """Resolve file path for given source and options"""
        
        base_path = self.interpretations_dir / source
        
        # Handle multi-version sources (Richmond)
        if source == 'richmond':
            version = kwargs.get('version', 'language_of_lines')
            base_path = base_path / version
        
        # Handle multi-level sources (deKorne)
        elif source == 'dekorne':
            level = kwargs.get('level', 'simple')
            base_path = base_path / level
        
        # Standard single-version sources (Legge, Wilhelm)
        # base_path already correct
        
        return base_path / f'hexagram_{number:02d}.yaml'
    
    def list_sources(self):
        """List available sources"""
        return list(self.sources_metadata.keys())

# Backward compatibility wrapper
def load_hexagram_data(number):
    """Legacy function - loads from Legge by default"""
    loader = HexagramDataLoader()
    return loader.get_hexagram(number, source='legge')
```

## Python Accessor Pattern

### Base Interface

```python
# sources/base.py
from abc import ABC, abstractmethod
from pathlib import Path
import yaml

class IChingSource(ABC):
    """Base interface all sources implement"""
    
    def __init__(self, data_dir):
        self.data_dir = Path(data_dir)
        self.data = {}
    
    @abstractmethod
    def get_hexagram(self, number, **kwargs):
        """Return complete hexagram data
        
        Args:
            number: Hexagram number (1-64)
            **kwargs: Source-specific options (level, version, etc.)
        
        Returns:
            dict: Hexagram data
        """
        pass
    
    @abstractmethod
    def get_judgment(self, number, **kwargs):
        """Return judgment text and commentary"""
        pass
    
    @abstractmethod
    def get_line(self, hex_num, line_num, **kwargs):
        """Return specific line interpretation"""
        pass
    
    def _load_yaml(self, filename):
        """Load YAML file, cache in memory"""
        if filename not in self.data:
            filepath = self.data_dir / filename
            with open(filepath, 'r') as f:
                self.data[filename] = yaml.safe_load(f)
        return self.data[filename]
```

### Wilhelm Implementation

```python
# sources/wilhelm.py
from .base import IChingSource

class WilhelmSource(IChingSource):
    """Wilhelm/Baynes translation accessor"""
    
    def __init__(self):
        super().__init__('interpretations/wilhelm')
    
    def get_hexagram(self, number, **kwargs):
        """Return complete hexagram data"""
        filename = f'hex_{number:02d}.yaml'
        return self._load_yaml(filename)
    
    def get_judgment(self, number, **kwargs):
        """Return judgment text and commentary"""
        hex_data = self.get_hexagram(number)
        return {
            'text': hex_data['judgment']['text'],
            'commentary': hex_data['judgment']['commentary']
        }
    
    def get_line(self, hex_num, line_num, **kwargs):
        """Return specific line interpretation"""
        hex_data = self.get_hexagram(hex_num)
        return hex_data['lines'][line_num]
    
    def get_image(self, number, **kwargs):
        """Return image text and commentary"""
        hex_data = self.get_hexagram(number)
        return {
            'text': hex_data['image']['text'],
            'commentary': hex_data['image']['commentary']
        }
```

### Richmond Implementation (Multi-Version)

```python
# sources/richmond.py
from .base import IChingSource

class RichmondSource(IChingSource):
    """Richmond accessor - handles multiple versions"""
    
    def __init__(self):
        super().__init__('interpretations/richmond')
        self.versions = {
            'oracle_1985': 'oracle_1985',
            'language_of_lines': 'language_of_lines'
        }
        self.default_version = 'language_of_lines'
    
    def get_hexagram(self, number, version=None, **kwargs):
        """Return complete hexagram data
        
        Args:
            number: Hexagram number
            version: 'oracle_1985' or 'language_of_lines'
        """
        version = version or self.default_version
        version_dir = self.versions[version]
        filename = f'{version_dir}/hex_{number:02d}.yaml'
        return self._load_yaml(filename)
    
    def get_judgment(self, number, version=None, **kwargs):
        hex_data = self.get_hexagram(number, version=version)
        return hex_data['oracle']  # Richmond uses 'oracle' key
    
    def get_line(self, hex_num, line_num, version=None, **kwargs):
        hex_data = self.get_hexagram(hex_num, version=version)
        return hex_data['lines'][line_num]
    
    def get_manifestations(self, number, version='language_of_lines'):
        """Get Richmond's pattern/nature/human/form manifestations
        Only available in language_of_lines version
        """
        if version != 'language_of_lines':
            raise ValueError("Manifestations only in language_of_lines")
        hex_data = self.get_hexagram(number, version=version)
        return hex_data['manifestations']
```

### deKorne Implementation (Multi-Level)

```python
# sources/dekorne.py
from .base import IChingSource

class DekorneSource(IChingSource):
    """deKorne accessor - handles simple/full levels"""
    
    def __init__(self):
        super().__init__('interpretations/dekorne')
        self.levels = ['simple', 'full']
        self.default_level = 'simple'
    
    def get_hexagram(self, number, level=None, **kwargs):
        """Return hexagram data at specified complexity level
        
        Args:
            number: Hexagram number
            level: 'simple' or 'full'
        """
        level = level or self.default_level
        if level not in self.levels:
            raise ValueError(f"Level must be one of {self.levels}")
        
        filename = f'{level}/hex_{number:02d}.yaml'
        return self._load_yaml(filename)
    
    def get_judgment(self, number, level=None, **kwargs):
        hex_data = self.get_hexagram(number, level=level)
        
        if level == 'full':
            return {
                'translations': hex_data['judgment']['translations'],
                'commentary': hex_data['judgment'].get('confucian_commentary'),
                'synthesis': hex_data['judgment']['synthesis']
            }
        else:
            return {'essence': hex_data['judgment']['essence']}
    
    def get_line(self, hex_num, line_num, level=None, **kwargs):
        hex_data = self.get_hexagram(hex_num, level=level)
        return hex_data['lines'][line_num]
    
    def get_all_translations(self, hex_num, element='judgment'):
        """Get all translation sources for judgment/image/line
        Only available in full level
        """
        hex_data = self.get_hexagram(hex_num, level='full')
        return hex_data[element]['translations']
```

### Source Registry

```python
# sources/__init__.py
from .wilhelm import WilhelmSource
from .richmond import RichmondSource
from .dekorne import DekorneSource

class SourceRegistry:
    """Central registry for all I Ching sources"""
    
    def __init__(self):
        self.sources = {}
        self._register_defaults()
    
    def _register_defaults(self):
        """Register built-in sources"""
        self.sources['wilhelm'] = WilhelmSource()
        self.sources['richmond'] = RichmondSource()
        self.sources['dekorne'] = DekorneSource()
    
    def get_source(self, name):
        """Get source accessor by name"""
        if name not in self.sources:
            raise ValueError(f"Unknown source: {name}")
        return self.sources[name]
    
    def list_sources(self):
        """List available sources"""
        return list(self.sources.keys())

# Usage:
# registry = SourceRegistry()
# wilhelm = registry.get_source('wilhelm')
# judgment = wilhelm.get_judgment(17)
```

## Extraction Methods

### Wilhelm Extraction (Plain Text)

```python
# extraction/extract_wilhelm.py
"""
Extract Wilhelm translation from plain text format

Input: wilhelm.txt (5398 lines)
Structure:
  - Hexagram number and name: "17. Sui / Following"
  - Trigrams: "above TUI...", "below CHêN..."
  - THE JUDGMENT section
  - THE IMAGE section  
  - THE LINES section (Nine/Six at position)
  
Output: 64 YAML files in interpretations/wilhelm/
"""

import re
import yaml
from pathlib import Path

def extract_wilhelm(input_file, output_dir):
    """Extract all hexagrams from Wilhelm text"""
    
    with open(input_file, 'r') as f:
        content = f.read()
    
    # Split into hexagram sections (between "N. Name" patterns)
    pattern = r'(\d+)\.\s+([^/\n]+)\s*/\s*([^\n]+)\n'
    hexagrams = re.split(pattern, content)
    
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Process each hexagram
    i = 1
    while i < len(hexagrams):
        num = int(hexagrams[i])
        chinese_name = hexagrams[i+1].strip()
        english_name = hexagrams[i+2].strip()
        hex_content = hexagrams[i+3] if i+3 < len(hexagrams) else ''
        
        # Extract sections
        hex_data = parse_hexagram_content(
            num, chinese_name, english_name, hex_content
        )
        
        # Write YAML
        output_file = output_dir / f'hex_{num:02d}.yaml'
        with open(output_file, 'w') as f:
            yaml.dump(hex_data, f, allow_unicode=True, 
                     default_flow_style=False, sort_keys=False)
        
        print(f"Extracted hexagram {num}: {chinese_name} / {english_name}")
        i += 4

def parse_hexagram_content(num, chinese, english, content):
    """Parse individual hexagram content into structured data"""
    
    data = {
        'metadata': {
            'hexagram': num,
            'name': chinese,
            'english': english,
            'source': 'Richard Wilhelm',
            'translator': 'Cary F. Baynes'
        }
    }
    
    # Extract trigrams
    trigram_pattern = r'above ([A-Z]+) ([^,\n]+), ([A-Z]+)\nbelow ([A-Z]+) ([^,\n]+), ([A-Z]+)'
    trigram_match = re.search(trigram_pattern, content)
    if trigram_match:
        data['trigrams'] = {
            'above': {
                'name': trigram_match.group(1),
                'attribute': f"{trigram_match.group(2)}, {trigram_match.group(3)}"
            },
            'below': {
                'name': trigram_match.group(4),
                'attribute': f"{trigram_match.group(5)}, {trigram_match.group(6)}"
            }
        }
        # Extract relationship text (paragraph after trigrams)
        rel_start = trigram_match.end()
        rel_end = content.find('THE JUDGMENT', rel_start)
        data['trigrams']['relationship'] = content[rel_start:rel_end].strip()
    
    # Extract judgment
    judgment_pattern = r'THE JUDGMENT\n\n(.+?)\n\n(.+?)(?=THE IMAGE|$)'
    judgment_match = re.search(judgment_pattern, content, re.DOTALL)
    if judgment_match:
        data['judgment'] = {
            'text': judgment_match.group(1).strip(),
            'commentary': judgment_match.group(2).strip()
        }
    
    # Extract image
    image_pattern = r'THE IMAGE\n\n(.+?)\n\n(.+?)(?=THE LINES|$)'
    image_match = re.search(image_pattern, content, re.DOTALL)
    if image_match:
        data['image'] = {
            'text': image_match.group(1).strip(),
            'commentary': image_match.group(2).strip()
        }
    
    # Extract lines
    data['lines'] = {}
    line_pattern = r'(Nine|Six) (at the beginning|in the second place|in the third place|in the fourth place|in the fifth place|at the top) means:\n\n(.+?)\n\n(.+?)(?=Nine |Six |index|^\d+\.)'
    
    line_matches = re.finditer(line_pattern, content, re.DOTALL)
    line_num = 1
    for match in line_matches:
        position = f"{match.group(1)} {match.group(2)}"
        text = match.group(3).strip()
        commentary = match.group(4).strip()
        
        data['lines'][line_num] = {
            'position': position,
            'text': text,
            'commentary': commentary
        }
        line_num += 1
    
    return data

if __name__ == '__main__':
    extract_wilhelm('wilhelm.txt', 'interpretations/wilhelm')
```

### Richmond PDF Extraction (OCR)

```python
# extraction/extract_richmond_pdf.py
"""
Extract Richmond from PDF photocopies using OCR

Input: page_58.pdf, page_59.pdf, ... (multiple PDFs per hexagram)
Method: Tesseract OCR + manual structure parsing
Output: YAML files in interpretations/richmond/oracle_1985/

Note: Requires preprocessing and verification due to 1985 typewriter quality
"""

import subprocess
import yaml
from pathlib import Path
from pdf2image import convert_from_path
import pytesseract

def extract_richmond_pdf(pdf_dir, output_dir):
    """Extract Richmond text from PDF photocopies"""
    
    pdf_dir = Path(pdf_dir)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Process PDFs in order
    pdf_files = sorted(pdf_dir.glob('page_*.pdf'))
    
    current_hex = None
    current_data = None
    
    for pdf_file in pdf_files:
        # Convert PDF to image
        images = convert_from_path(pdf_file, dpi=300)
        
        for image in images:
            # OCR with preprocessing
            text = ocr_with_preprocessing(image)
            
            # Parse hexagram structure
            hex_num = extract_hexagram_number(text)
            
            if hex_num and hex_num != current_hex:
                # Save previous hexagram
                if current_data:
                    save_richmond_yaml(current_hex, current_data, output_dir)
                
                # Start new hexagram
                current_hex = hex_num
                current_data = {
                    'metadata': {
                        'hexagram': hex_num,
                        'source': 'Nigel Richmond',
                        'work': 'The I Ching Oracle',
                        'published': 1985
                    },
                    'oracle': {},
                    'lines': {}
                }
            
            # Parse page content
            parse_richmond_page(text, current_data)
    
    # Save last hexagram
    if current_data:
        save_richmond_yaml(current_hex, current_data, output_dir)

def ocr_with_preprocessing(image):
    """Apply preprocessing to improve OCR accuracy"""
    import cv2
    import numpy as np
    
    # Convert PIL to cv2
    img = np.array(image)
    
    # Grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Deskew
    gray = deskew(gray)
    
    # Threshold (binarize)
    _, binary = cv2.threshold(gray, 0, 255, 
                              cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    
    # Denoise
    denoised = cv2.fastNlMeansDenoising(binary)
    
    # OCR
    custom_config = r'--oem 3 --psm 6'
    text = pytesseract.image_to_string(denoised, config=custom_config)
    
    return text

def parse_richmond_page(text, hex_data):
    """Parse Richmond page structure"""
    
    # Check for section headers
    if 'HEXAGRAM' in text:
        # Extract name
        name_match = re.search(r'HEXAGRAM.*?(\d+).*?MOVING LINES', text)
        if name_match:
            hex_data['metadata']['name'] = extract_name(text)
    
    if 'oracle' in text.lower() or 'judgment' in text.lower():
        # Extract oracle/judgment text
        hex_data['oracle']['judgment'] = extract_oracle_judgment(text)
        hex_data['oracle']['commentary'] = extract_oracle_commentary(text)
    
    if 'Line' in text:
        # Extract moving lines
        lines = extract_moving_lines(text)
        hex_data['lines'].update(lines)
    
    return hex_data

# Additional helper functions for Richmond parsing...
```

### deKorne DOC Extraction

```python
# extraction/extract_dekorne.py
"""
Extract deKorne from .doc files

Input: Hexagram_01.doc through Hexagram_64.doc
Method: 
  1. Convert .doc to .docx using LibreOffice
  2. Extract text using pandoc
  3. Parse multi-source structure
  4. Generate both simple and full YAML files

Output: 
  - interpretations/dekorne/simple/hex_NN.yaml
  - interpretations/dekorne/full/hex_NN.yaml
"""

import subprocess
import yaml
import re
from pathlib import Path

def extract_dekorne(doc_dir, output_dir):
    """Extract all deKorne hexagrams"""
    
    doc_dir = Path(doc_dir)
    output_dir = Path(output_dir)
    
    simple_dir = output_dir / 'simple'
    full_dir = output_dir / 'full'
    simple_dir.mkdir(parents=True, exist_ok=True)
    full_dir.mkdir(parents=True, exist_ok=True)
    
    # Process each .doc file
    doc_files = sorted(doc_dir.glob('Hexagram_*.doc'))
    
    for doc_file in doc_files:
        print(f"Processing {doc_file.name}...")
        
        # Convert to .docx
        docx_file = doc_file.with_suffix('.docx')
        convert_doc_to_docx(doc_file, docx_file)
        
        # Extract text
        txt_file = doc_file.with_suffix('.txt')
        extract_text_pandoc(docx_file, txt_file)
        
        # Parse structure
        with open(txt_file, 'r') as f:
            text = f.read()
        
        hex_num = extract_hexagram_number_dekorne(text)
        
        # Parse full structure
        full_data = parse_dekorne_full(text)
        
        # Extract simple essences
        simple_data = extract_dekorne_simple(full_data)
        
        # Save both versions
        with open(full_dir / f'hex_{hex_num:02d}.yaml', 'w') as f:
            yaml.dump(full_data, f, allow_unicode=True, 
                     default_flow_style=False, sort_keys=False)
        
        with open(simple_dir / f'hex_{hex_num:02d}.yaml', 'w') as f:
            yaml.dump(simple_data, f, allow_unicode=True,
                     default_flow_style=False, sort_keys=False)

def parse_dekorne_full(text):
    """Parse complete deKorne structure with all translations"""
    
    data = {
        'metadata': {
            'source': 'James deKorne',
            'work': 'Gnostic Book of Changes'
        },
        'judgment': {
            'translations': {},
            'synthesis': {}
        },
        'image': {
            'translations': {},
            'synthesis': {}
        },
        'lines': {}
    }
    
    # Extract judgment section
    judgment_section = extract_section(text, 'Judgment', 'The Image')
    
    # Parse all translations
    translators = ['Legge', 'Wilhelm/Baynes', 'Blofeld', 'Liu', 
                   'Ritsema/Karcher', 'Shaughnessy', 
                   'Cleary (1)', 'Cleary (2)', 'Wu']
    
    for translator in translators:
        trans_text = extract_translator_text(judgment_section, translator)
        if trans_text:
            key = translator.lower().replace('/', '_').replace(' ', '_')
            
            # Check for bracketed context
            if '[' in trans_text:
                main, context = split_text_and_context(trans_text)
                data['judgment']['translations'][key] = {
                    'text': main,
                    'context': context
                }
            else:
                data['judgment']['translations'][key] = trans_text
    
    # Extract synthesis
    notes_section = extract_section(judgment_section, 'NOTES AND PARAPHRASES', 'Line-')
    data['judgment']['synthesis']['notes_and_paraphrases'] = notes_section
    
    # Extract supporting quotes
    quotes = extract_quotes(notes_section)
    data['judgment']['synthesis']['supporting_quotes'] = quotes
    
    # Similar process for image and each line...
    
    return data

def extract_dekorne_simple(full_data):
    """Extract simple essences from full deKorne data"""
    
    simple_data = {
        'metadata': {
            'hexagram': full_data['metadata']['hexagram'],
            'name': full_data['metadata']['name'],
            'source': 'James deKorne (simplified)',
            'note': 'Essences extracted from full version summaries'
        },
        'judgment': {},
        'lines': {}
    }
    
    # Extract judgment essence
    # Look for "A." summary in synthesis
    synthesis = full_data['judgment']['synthesis']['notes_and_paraphrases']
    essence = extract_summary_line(synthesis)
    simple_data['judgment']['essence'] = essence
    
    # Extract line essences
    for line_num, line_data in full_data['lines'].items():
        line_synthesis = line_data['notes_and_paraphrases']
        line_essence = extract_summary_line(line_synthesis)
        simple_data['lines'][line_num] = {'essence': line_essence}
    
    return simple_data

def extract_summary_line(text):
    """Extract 'A.' summary line from synthesis"""
    match = re.search(r'^A\.\s*(.+?)$', text, re.MULTILINE)
    if match:
        return match.group(1).strip()
    return None

# Additional helper functions...
```

## Testing Strategy

```python
# tests/test_sources.py
"""Test source accessor functionality"""

import pytest
from sources import SourceRegistry

@pytest.fixture
def registry():
    return SourceRegistry()

def test_wilhelm_hexagram_17(registry):
    """Test Wilhelm source returns complete hexagram 17"""
    wilhelm = registry.get_source('wilhelm')
    hex_data = wilhelm.get_hexagram(17)
    
    assert hex_data['metadata']['hexagram'] == 17
    assert hex_data['metadata']['name'] == 'Sui'
    assert hex_data['metadata']['english'] == 'Following'
    assert 'trigrams' in hex_data
    assert 'judgment' in hex_data
    assert 'image' in hex_data
    assert 'lines' in hex_data
    assert len(hex_data['lines']) == 6

def test_richmond_versions(registry):
    """Test Richmond multi-version support"""
    richmond = registry.get_source('richmond')
    
    # Test oracle_1985 version
    oracle_data = richmond.get_hexagram(17, version='oracle_1985')
    assert 'oracle' in oracle_data
    
    # Test language_of_lines version
    lines_data = richmond.get_hexagram(17, version='language_of_lines')
    assert 'manifestations' in lines_data
    assert 'theme' in lines_data

def test_dekorne_levels(registry):
    """Test deKorne simple/full levels"""
    dekorne = registry.get_source('dekorne')
    
    # Test simple level
    simple = dekorne.get_hexagram(17, level='simple')
    assert 'essence' in simple['judgment']
    
    # Test full level
    full = dekorne.get_hexagram(17, level='full')
    assert 'translations' in full['judgment']
    assert len(full['judgment']['translations']) >= 8

def test_comparative_query(registry):
    """Test accessing same hexagram across multiple sources"""
    wilhelm = registry.get_source('wilhelm')
    richmond = registry.get_source('richmond')
    dekorne = registry.get_source('dekorne')
    
    w_judg = wilhelm.get_judgment(17)
    r_judg = richmond.get_judgment(17)
    d_judg = dekorne.get_judgment(17, level='simple')
    
    # All should return judgment data
    assert w_judg is not None
    assert r_judg is not None
    assert d_judg is not None
```

## Usage Examples

### Simple Divination

```python
from core.casting import cast_hexagram
from sources import SourceRegistry

# Cast hexagram
reading = cast_hexagram(method='coins')
print(f"Primary: {reading.primary}, Changing: {reading.changing}")

# Get interpretation from Richmond (default simple format)
registry = SourceRegistry()
richmond = registry.get_source('richmond')

print("\n" + "="*60)
print(f"HEXAGRAM {reading.primary}")
print("="*60)

judgment = richmond.get_judgment(reading.primary)
print(judgment['judgment'])

if reading.changing:
    print(f"\nChanging line {reading.changing[0]}:")
    line = richmond.get_line(reading.primary, reading.changing[0])
    print(line['text'])
```

### Comparative Study

```python
from sources import SourceRegistry

registry = SourceRegistry()

# Study hexagram 17 across all sources
hex_num = 17

print("="*60)
print(f"COMPARATIVE STUDY: HEXAGRAM {hex_num}")
print("="*60)

sources = ['wilhelm', 'richmond', 'dekorne']

for source_name in sources:
    source = registry.get_source(source_name)
    
    # Get appropriate level/version
    if source_name == 'richmond':
        data = source.get_hexagram(hex_num, version='language_of_lines')
    elif source_name == 'dekorne':
        data = source.get_hexagram(hex_num, level='simple')
    else:
        data = source.get_hexagram(hex_num)
    
    print(f"\n{source_name.upper()}")
    print("-"*60)
    
    # Print judgment
    if source_name == 'dekorne':
        print(data['judgment']['essence'])
    elif source_name == 'richmond':
        print(data['oracle']['judgment'])
    else:
        print(data['judgment']['text'])
```

### Deep Research (deKorne Full)

```python
from sources import SourceRegistry

registry = SourceRegistry()
dekorne = registry.get_source('dekorne')

# Get complete scholarly apparatus for hexagram 17, line 3
hex_data = dekorne.get_hexagram(17, level='full')
line_3 = hex_data['lines'][3]

print("LINE 3 - ALL TRANSLATIONS:")
print("="*60)

for translator, text in line_3['translations'].items():
    print(f"\n{translator.upper()}:")
    if isinstance(text, dict):
        print(text['text'])
        if 'context' in text:
            print(f"  [{text['context']}]")
    else:
        print(text)

print("\n\nSYNTHESIS:")
print("="*60)
print(line_3['notes_and_paraphrases']['editor'])

print("\n\nSUPPORTING QUOTES:")
for quote in line_3['notes_and_paraphrases']['supporting_quotes']:
    print(f"\n{quote['source']}:")
    print(f"  {quote['text']}")
```

## Implementation Roadmap

### Phase 0: Backup and Prepare (Day 1)
- [ ] `git commit -am "Pre-YAML migration checkpoint"`
- [ ] `cp -r data/hexagrams data/hexagrams.backup`
- [ ] Create directory structure:
  ```bash
  mkdir -p data/sources/{legge,wilhelm,richmond/oracle_1985,richmond/language_of_lines,dekorne}
  mkdir -p data/interpretations/{legge,wilhelm,richmond,dekorne}
  ```
- [ ] Copy sources README template to `data/sources/README.md`
- [ ] Add any existing source files to `data/sources/` (wilhelm.txt, Richmond PDFs, etc.)
- [ ] Install PyYAML if not present: `pip install pyyaml`

### Phase 1: JSON → YAML Migration (Days 2-3)
- [ ] Write `tools/migrate_json_to_yaml.py` script
- [ ] Run migration on all 64 hexagrams
- [ ] Verify output: compare JSON vs YAML for hex 17
- [ ] Run verification script on all 64
- [ ] Manual spot-check: hexagrams 1, 17, 32, 64

### Phase 2: Update Loader (Days 4-5)
- [ ] Modify `pyching/data/loader.py` for YAML
- [ ] Update `pyching/data/resolver.py` paths (.json → .yaml)
- [ ] Add backward compatibility wrapper (if needed temporarily)
- [ ] Run existing tests - all should pass
- [ ] Test GUI - verify display unchanged

### Phase 3: Validate Migration (Day 6)
- [ ] Create `tests/test_yaml_migration.py`
- [ ] Test all 64 hexagrams load correctly
- [ ] Compare output: old JSON loader vs new YAML loader
- [ ] Performance check: YAML load times acceptable
- [ ] All existing functionality works

### Phase 4: Delete JSON (Day 7)
- [ ] Final verification all tests pass
- [ ] `rm -rf data/hexagrams/` (JSON directory)
- [ ] Update `data/README.md` - document YAML format
- [ ] `git commit -am "Completed JSON→YAML migration"`
- [ ] Keep backup for one more week, then delete

### Phase 5: Extract Wilhelm (Weeks 2-3)
- [ ] Check existing `tools/extract_wilhelm.py` - what does it do?
- [ ] Write or update Wilhelm extractor from wilhelm.txt
- [ ] Extract hexagram 17 as proof-of-concept
- [ ] Validate Wilhelm YAML structure
- [ ] Extract all 64 hexagrams
- [ ] Test multi-source loading: Legge vs Wilhelm

### Phase 6: Add Richmond (Weeks 4-5)
- [ ] Richmond Oracle 1985: OCR + manual verification
  - [ ] Set up Tesseract OCR pipeline
  - [ ] Process PDF pages (2 pages per hexagram)
  - [ ] Manual correction pass
  - [ ] Extract hexagrams 1, 17, 32, 64 first
  - [ ] Batch process remaining 60
- [ ] Richmond Language of Lines: better quality source
  - [ ] Same OCR pipeline
  - [ ] Compare with Oracle 1985 for differences
- [ ] Implement multi-version accessor

### Phase 7: Add deKorne (Weeks 6-8)
- [ ] Convert .doc to .docx (all 64 files)
- [ ] Extract text via pandoc
- [ ] Parse multi-source structure (10 translators)
- [ ] Extract hexagram 17 full version
- [ ] Create simple essence extraction
- [ ] Validate quotes attribution
- [ ] Batch process all 64
- [ ] Test simple vs full level access

### Phase 8: Integration and Testing (Weeks 9-10)
- [ ] Update CLI: `pyching --cast --source wilhelm`
- [ ] Update GUI: source selection dropdown
- [ ] Comparative display: side-by-side sources
- [ ] Write comprehensive tests
- [ ] Performance optimization if needed
- [ ] Documentation and examples
- [ ] Release notes

### Phase 9: Future Expansion (Ongoing)
- [ ] Add other translations (Blofeld, Ritsema/Karcher standalone)
- [ ] Cross-reference system
- [ ] Personal readings journal
- [ ] Audio integration (Wilhelm audiobook timestamps)
- [ ] Chinese original text

## Critical Notes

### Source Integrity Preservation

**DO NOT** normalize across sources. Each maintains its own:
- Terminology (Chên vs Zhen, Jun zi vs Superior Man)
- Structure (judgment/image/lines vs oracle/manifestations/lines)
- Complexity level (terse vs. extensive)

The accessor pattern provides **uniform interface** while **preserving internal diversity**.

### OCR Verification Required

Richmond 1985 photocopies need manual review:
- Typewriter artifacts (inconsistent spacing)
- Photocopy degradation
- Context-dependent corrections (is that "m" or "rn"?)

Budget ~2 hours per hexagram for OCR + verification.

### deKorne Complexity

Each hexagram = ~3500 words, 10 translation sources, multiple quotes. Plan for:
- Automated extraction of structure
- Manual verification of quote attribution
- Testing synthesis parsing

### Version Control Strategy

Use git to track:
- YAML data files (interpretations/)
- Extraction scripts (extraction/)
- Source code (sources/, core/)

This enables:
- Tracking corrections/improvements
- Comparing source versions (Richmond 1985 vs Language of Lines)
- Collaborative verification

### Future Extensions

Architecture supports:
- Audio recordings (Wilhelm audiobook → timestamped YAML)
- Images (hexagram diagrams, trigram illustrations)
- Cross-references (hex 17 line 6 → compare hex 46 line 4)
- User annotations (personal readings journal)
- Multiple languages (Chinese original, various translations)

## Conclusion

This specification provides a complete blueprint for migrating pyChing from JSON to YAML and extending to multi-source I Ching interpretation database.

### Migration Strategy Summary

1. **Convert existing Legge JSON to YAML** - Preserve structure, change format
2. **Update loaders and tests** - All existing functionality continues working
3. **Validate and delete JSON** - Clean transition, no legacy code
4. **Add new sources progressively** - Wilhelm, Richmond, deKorne
5. **Maintain source integrity** - Each source keeps its own structure/epistemology

### Why This Approach Works

- **Minimal disruption** - Existing code/tests work throughout migration
- **Clear rollback path** - JSON backup exists until confidence established
- **Incremental validation** - Test each phase before proceeding
- **Source preservation** - Richmond's poetic essence ≠ deKorne's scholarly synthesis
- **Unix philosophy** - Small, verifiable steps; test at each stage

### The Goal

- **Richmond** (Language of Lines) for daily consultation - poetic immediacy
- **Wilhelm** for contemplative depth - psychological understanding
- **deKorne** for serious study - comparative scholarship
- **Legge** as foundation - philological rigor

All accessible through consistent interface, each maintaining its own voice.

### First Action (Next Session)

**Priority 1: Migration Script**

Create `tools/migrate_json_to_yaml.py` and run it on hexagram 17 as proof-of-concept:

```bash
# In next session or with Claude Code:
python tools/migrate_json_to_yaml.py --single 17
cat data/interpretations/legge/hexagram_17.yaml
# Verify: does YAML contain same data as JSON?
```

Validate:
- Judgment text identical
- All 6 lines present
- Metadata preserved
- YAML human-readable

Once hex 17 works, process all 64.

**Priority 2: Update Loader**

Modify `pyching/data/loader.py` to use YAML:
- Change `json.load()` → `yaml.safe_load()`
- Update paths
- Test: `python -c "from pyching.data.loader import load_hexagram_data; print(load_hexagram_data(17))"`

**Priority 3: Run Tests**

Your existing test suite should pass with YAML backend:
```bash
pytest tests/
```

If all pass → delete JSON, commit migration complete.

### Handoff to Future Session

This specification is complete and self-contained. Future Claude instance needs:
1. This document (`pyching_data_architecture_spec.md`)
2. Access to your pyChing repository
3. Source files (wilhelm.txt, Richmond PDFs, deKorne .doc files)

No additional context required - spec contains all architectural decisions, code templates, and implementation plan.

---

## Quick Reference: Source File Placement

**Where to drop your source materials:**

```bash
# Wilhelm text file
data/sources/wilhelm/wilhelm.txt

# Richmond Oracle 1985 PDF pages
data/sources/richmond/oracle_1985/page_58.pdf
data/sources/richmond/oracle_1985/page_59.pdf
# ... etc

# Richmond Language of Lines scans
data/sources/richmond/language_of_lines/page_82.png
data/sources/richmond/language_of_lines/page_83.png
# ... etc

# deKorne Word documents
data/sources/dekorne/Hexagram_01.doc
data/sources/dekorne/Hexagram_02.doc
# ... through Hexagram_64.doc

# Any Legge source references
data/sources/legge/legge_sources.md  # Web links, citations

# Create notes for each source
data/sources/wilhelm/wilhelm_notes.md
data/sources/richmond/richmond_notes.md
data/sources/dekorne/dekorne_notes.md
```

**Then extract with:**
```bash
python tools/extract_wilhelm.py        # → data/interpretations/wilhelm/
python tools/extract_richmond_pdf.py   # → data/interpretations/richmond/
python tools/extract_dekorne.py        # → data/interpretations/dekorne/
```

**The golden rule:** 
- `data/sources/` = Raw materials (PDFs, .doc, .txt, images)
- `data/interpretations/` = Processed YAML (extracted and structured)

Keep sources archived - you may need to re-extract if structure changes or errors found.
