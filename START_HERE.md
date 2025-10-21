# 🚀 Quick Start Guide

Welcome! Your Monday.com Item Duplicator with **Duplicate Detection** is ready to go with UV (super fast!).

## ✨ What's New: Duplicate Detection!

The script now **automatically checks for duplicates**:
- If an item with the same name exists in the destination → **Updates it**
- If no duplicate found → **Creates new item**

This means you can run the script multiple times safely - it won't create duplicates! 🎉

---

## ⚡ Super Quick Start (Windows)

1. **Double-click `setup.bat`** - This will:
   - Install UV if needed (or remind you to install it)
   - Create a virtual environment with UV
   - Install all dependencies (blazingly fast!)
   - Verify your .env file

2. **Double-click `run.bat`** - This will:
   - Activate the virtual environment
   - Prompt you for an item name
   - **Press Enter** for batch mode (all items)
   - **Type a name** for single item mode

That's it! 🎉

---

## 📋 Manual Setup (if you prefer)

### First, install UV:
```powershell
# PowerShell (Windows)
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### Then setup the project:
```bash
# 1. Navigate to the project
cd C:\Users\TC933\Projects\monday-item-duplicator

# 2. Create virtual environment with UV
uv venv .venv

# 3. Install dependencies with UV (super fast!)
uv pip install -r requirements.txt

# 4. Activate environment
.venv\Scripts\activate

# 5. Run the script
# For single item:
python monday_item_duplicator.py "Item Name Here"

# For batch mode (all items):
python monday_item_duplicator.py
```

---

## ✅ What's Already Configured

- ✅ API Key is set in `.env`
- ✅ Source Board: 8891540298 (Content Creation Machine)
- ✅ Source Group: group_mktas044 (Ready to Upload)
- ✅ Destination Board: 5422445730 ([TruLaw] - Workshop)
- ✅ Destination Group: group_mknzndef (Requested)
- ✅ All 6 columns mapped and ready
- ✅ **Duplicate detection enabled** ⚡

---

## 🎯 Interactive Mode

When you run `run.bat`, you'll see:

```
Enter item name to duplicate (or press Enter for ALL items):
```

**Option 1: Single Item**
- Type: `Who Qualifies to File a Roblox Child Predator Lawsuit Claim?`
- Press Enter
- Script checks if it exists in destination
- **If exists**: Updates it with latest data
- **If not**: Creates new item

**Option 2: Batch Mode (All Items)**
- Just press Enter (leave blank)
- ALL items from the source group will be processed
- Each item is checked for duplicates
- Existing items are updated, new ones are created

---

## 🔧 What Gets Processed

The script will map these 6 fields:

1. **Name** (the item title)
2. **Focus Keyword**
3. **Meta Title**
4. **Surfer Editor Link** (with URL as display text)
5. **Surfer Page ID**
6. **Client Pillars** (board relation)

**With duplicate detection**, you'll see:
- ✅ "Item created" for new items
- 🔄 "Item updated" for existing items

---

## 💡 Why UV?

UV is a blazingly fast Python package manager (10-100x faster than pip!):
- Written in Rust for maximum performance
- Drop-in replacement for pip
- Better dependency resolution
- Works with existing requirements.txt

---

## 🎭 How Duplicate Detection Works

```
1. Script finds item in source board
2. Checks if item with same name exists in destination
3a. IF EXISTS → Updates existing item with new data ✅
3b. IF NOT EXISTS → Creates new item ✅
4. Shows clear action taken (CREATED or UPDATED)
```

**Benefits:**
- Run the script as many times as you want
- No duplicate items cluttering your board
- Always have the latest data from source
- Clear summary of what was created vs updated

---

## 🆘 Need Help?

**"UV not found"**
```powershell
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

**"MONDAY_API_KEY not found"**
- Check that `.env` file exists
- Verify it contains: `MONDAY_API_KEY=your_key_here`

**"Item not found"**
- Check the item name is exactly correct (case-sensitive)
- Verify it exists in the source board

**"Duplicate not detected when it should be"**
- Item names must match **exactly** (including case, spaces, punctuation)
- Check both boards to verify the names match

---

## 📚 Documentation

- `README.md` - Full detailed documentation
- `QUICK_REFERENCE.md` - Quick command reference
- This file - Getting started guide

---

## 🎉 You're All Set!

**Easiest way:**
1. Run `setup.bat` (first time only)
2. Run `run.bat` 
3. Enter item name or press Enter for all
4. Watch it detect duplicates and update smartly! 🚀

**Manual way:**
```bash
uv venv .venv
uv pip install -r requirements.txt
.venv\Scripts\activate
python monday_item_duplicator.py "Item Name"
```

---

## 🌟 Pro Tips

💡 Run batch mode regularly to keep destination board in sync  
💡 Duplicate detection means you can't "over-sync" - safe to run anytime  
💡 Updates preserve the destination item ID (won't break any links)  
💡 Clear summary shows exactly what was created vs updated  
💡 Perfect for workflows where source data changes frequently  

Happy duplicating (without the duplicates)! 🎯
