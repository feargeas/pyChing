# Line Order Conventions

**Lines array**: Bottom-to-top indexing
- `lines[0]` = line 1 (bottom)
- `lines[5]` = line 6 (top)

**Binary strings**: Top-to-bottom (traditional I Ching table format)
- `binary[0]` = line 6 (top)
- `binary[5]` = line 1 (bottom)

**Translation**: `loader.py:196` uses `reversed()` to bridge conventions
