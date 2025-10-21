# Quick Reference Guide

## 🔍 New Feature: Duplicate Detection

The script now automatically detects duplicates:
- **Checks destination board** for items with the same name
- **Updates existing items** instead of creating duplicates
- **Creates new items** only if they don't exist
- **Clear feedback** showing CREATED vs UPDATED

---

## Setup in 3 Steps (Using UV - Super Fast!)

### Step 1: Install UV
```powershell
# Windows PowerShell
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### Step 2: Setup Project
```bash
cd C:\Users\TC933\Projects\monday-item-duplicator
uv venv .venv
uv pip install -r requirements.txt
```

### Step 3: Run
```bash
.venv\Scripts\activate

# Single item
python monday_item_duplicator.py "Item Name"

# All items (batch mode)
python monday_item_duplicator.py
```

---

## Or Use Batch Files (Easiest!)

```bash
setup.bat    # Run once to setup everything
run.bat      # Run this to process items (prompts you)
```

---

## Interactive Mode

When you run `run.bat`, you'll be prompted:

```
Enter item name to duplicate (or press Enter for ALL items):
```

- **Type a name** = Single item mode (checks for duplicate, updates or creates)
- **Press Enter** = Batch mode (processes all items, updates existing, creates new)

---

## What Gets Copied?

✅ **6 Columns Successfully Mapped:**

| # | Column Name | Source ID | Destination ID |
|---|-------------|-----------|----------------|
| 1 | Name | (automatic) | (automatic) |
| 2 | Focus Keyword | text_mkpvwvnv | text1 |
| 3 | Meta Title | text_mkpv7fek | text_mks07meq |
| 4 | Surfer Editor Link | link_mkpv2ga7 | link0 |
| 5 | Surfer Page ID | text_mkpvv0ws | text_mkwym6gf |
| 6 | Client Pillars | board_relation_mkrcq1m6 | connect_boards__1 |

---

## Board Setup

**FROM:** Content Creation Machine
- Board ID: `8891540298`
- Group: `group_mktas044` (Ready to Upload)

**TO:** [TruLaw] - Workshop
- Board ID: `5422445730`  
- Group: `group_mknzndef` (Requested)

---

## How Duplicate Detection Works

```
For each item:
1. Find item in source board
2. Search destination board for item with same name
3. IF FOUND → Update existing item ✅
4. IF NOT FOUND → Create new item ✅
5. Report action taken (CREATED or UPDATED)
```

---

## Output Examples

### Single Item - Item Exists (Update)
```
🔎 Checking for existing item in destination board...
⚠️  Item already exists in destination!
   Existing Item ID: 18235202768
   → Will UPDATE existing item instead of creating duplicate

📝 Updating existing item 18235202768...
✅ Item updated successfully!

Action: UPDATED
```

### Single Item - Item Doesn't Exist (Create)
```
🔎 Checking for existing item in destination board...
✅ No duplicate found - will create new item

📊 Creating new item...
✅ Item created successfully!

Action: CREATED
```

### Batch Mode Summary
```
📊 BATCH PROCESSING SUMMARY
✅ Successfully processed: 15/15 items
   • Created: 3
   • Updated: 12
```

---

## Common UV Commands

```bash
# Create virtual environment
uv venv .venv

# Install dependencies (super fast!)
uv pip install -r requirements.txt

# Activate environment
.venv\Scripts\activate

# Install a new package
uv pip install package-name

# Update all packages
uv pip install --upgrade -r requirements.txt
```

---

## Common Commands

```bash
# Activate virtual environment
.venv\Scripts\activate

# Run - Single item (checks for duplicate)
python monday_item_duplicator.py "Item Name Here"

# Run - Batch mode (checks all for duplicates)
python monday_item_duplicator.py

# Deactivate virtual environment
deactivate
```

---

## Common Issues

### "UV not found"
```powershell
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```
Then restart your terminal.

### "MONDAY_API_KEY not found"
- Check that `.env` file exists in the project root
- Verify the API key is set correctly in `.env`
- Make sure you're running from the project directory

### "Item not found"
- Check that the item name is **exact** (case-sensitive)
- Verify the item exists in the source board
- Try copying the name directly from Monday.com

### "Duplicate not detected"
- Item names must match **exactly** (case, spaces, punctuation)
- Check item exists in destination board with exact same name
- If names differ slightly, script will create new item

### "Items not in connected boards"
- The Client Pillars column must be configured to connect to board `6355987170`
- Go to board settings → column settings → ensure board relation is set up

### "Query failed"
- Check your API key is correct
- Ensure you have access to both boards
- Verify Monday.com API is working

---

## File Structure

```
monday-item-duplicator/
├── .env                        # API key (DO NOT commit!)
├── .venv/                      # Virtual environment (created by UV)
├── .gitignore                  # Protects .env from being committed
├── requirements.txt            # Python dependencies
├── monday_item_duplicator.py   # Main script (with duplicate detection!)
├── setup.bat                   # Setup wizard
├── run.bat                     # Run wizard (with prompt)
├── README.md                   # Full documentation
├── START_HERE.md               # Getting started
└── QUICK_REFERENCE.md          # This file
```

---

## Command Line Arguments

```bash
# No arguments = batch mode (all items, checks duplicates)
python monday_item_duplicator.py

# With item name = single item mode (checks duplicate)
python monday_item_duplicator.py "Who Qualifies to File a Roblox Child Predator Lawsuit Claim?"

# The run.bat handles this for you interactively!
```

---

## Why UV?

🚀 **10-100x faster** than pip
⚡ Written in Rust for maximum performance  
🔄 Drop-in replacement for pip  
📦 Better dependency resolution  
✅ Works with existing requirements.txt  

---

## Why Duplicate Detection?

✅ **Run safely multiple times** - Won't create duplicates  
✅ **Keep data in sync** - Latest source data always updates destination  
✅ **Clear feedback** - Know exactly what was created vs updated  
✅ **Preserves relationships** - Updates keep the same item ID (links don't break)  
✅ **Batch friendly** - Process entire groups without worry  

---

## Security Note

⚠️ **Never commit the `.env` file to git!** It contains your API key.
The `.gitignore` file is set up to prevent this automatically.

---

## Quick Examples

### Single Item (With Duplicate Check)
```bash
run.bat
# Prompt: Enter item name to duplicate (or press Enter for ALL items):
# Type: My Article Title
# Press Enter
# Output: Checks for duplicate, then CREATEs or UPDATEs
```

### Batch Processing (With Duplicate Check)
```bash
run.bat
# Prompt: Enter item name to duplicate (or press Enter for ALL items):
# Just press Enter (leave blank)
# Output: Processes all items, shows summary of CREATED vs UPDATED
```

### Direct Command Line
```bash
.venv\Scripts\activate
python monday_item_duplicator.py "Specific Item Name"
# Checks for duplicate, then creates or updates
```

---

## Pro Tips

💡 Use batch mode regularly to keep boards in sync  
💡 Duplicate detection means it's safe to run anytime  
💡 Updated items keep same ID (preserves links/relations)  
💡 Watch the summary to see what changed  
💡 Item names must match exactly for duplicate detection  
💡 Run after making changes in source to sync to destination  

---

## Workflow Example

```
Morning:
1. Create/edit articles in Content Creation Machine board
2. Move them to "Ready to Upload" group

Afternoon:
1. Double-click run.bat
2. Press Enter (batch mode)
3. Script checks each item:
   - New articles → Created in TruLaw Workshop
   - Existing articles → Updated with latest data
4. All done! No duplicates, all synced ✅
```

---

## Need Help?

1. Check the full README.md for detailed documentation
2. Verify your API key has proper permissions
3. Ensure both boards exist and you have access
4. Check that column IDs match in both boards
5. For duplicate detection issues, verify item names match exactly
