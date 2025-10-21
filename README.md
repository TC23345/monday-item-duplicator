# Monday.com Item Duplicator

Duplicate items between Monday.com boards with column mapping and automatic duplicate detection.

## Features

- ✅ Duplicate Detection - Updates existing items instead of creating duplicates
- 🔄 Batch Processing - Process all items or one at a time
- 🎯 Column Mapping - Map columns between different boards
- ⚡ User Confirmation - Preview before creating/updating

## Quick Start (Windows)

### 1. Clone the Repository

Open Command Prompt or Git Bash and run:

```bash
git clone https://github.com/TC23345/monday-item-duplicator.git
cd monday-item-duplicator
```

### 2. Run Setup

Right-click `setup.bat` → **Show in File Explorer** → Double-click `setup.bat`

This will:
- Create Python virtual environment
- Install dependencies
- Guide you through creating your `.env` configuration file

### 3. Run the Tool

Right-click `run.bat` → **Show in File Explorer** → Double-click `run.bat`

- Press **Enter** to process ALL items (batch mode)
- Or type an item name to process just that one item

That's it! 🎉

## Configuration

The `setup.bat` script will guide you through configuration. You'll need:

1. **Monday.com API Key**
   - Go to Monday.com → Profile → Admin → API
   - Copy your API token

2. **Board IDs** (found in the URL)
   - Source: `https://yourcompany.monday.com/boards/SOURCE_BOARD_ID`
   - Destination: `https://yourcompany.monday.com/boards/DEST_BOARD_ID`

3. **Group IDs** (press F12 on board, inspect group element for `data-id`)

4. **Column Mappings** (see Advanced Configuration below)

Setup creates a `.env` file with all these settings.

---

## Column Type Reference

Understanding how different Monday.com column types are mapped:

### Supported Column Types

| Column Type | Format | Example | Notes |
|------------|--------|---------|-------|
| **Text** | Plain text string | `"Column text here"` | Simple text fields |
| **Link** | `{"url": "...", "text": "..."}` | `{"url": "https://example.com", "text": "https://example.com"}` | URL is used for both url and display text |
| **Status/Color** | `{"label": "Label Name"}` | `{"label": "Done"}` | Uses the label text, not index |
| **Dropdown** | `{"ids": [1, 2, 3]}` | `{"ids": [2]}` | Uses numeric IDs, not labels array |
| **Board Relation** | `{"item_ids": [123, 456]}` | `{"item_ids": [789]}` | Links to items in other boards |

### Common Column Mapping Issues

#### Issue: "missingLabel" error for Status/Color columns
**Problem:** The label doesn't exist in the destination column
**Solution:** Ensure both source and destination status columns have the same label names (e.g., "Done", "Working on it", etc.)

**Example:**
```bash
# ❌ Wrong - Using index format
{"index": 2}

# ✅ Correct - Using label format
{"label": "Done"}
```

---

#### Issue: Dropdown values not transferring

**Problem:** Using wrong key name in the data structure
**Solution:** Dropdown columns use `"ids"` not `"labels"`

**Example:**
```bash
# ❌ Wrong - Using labels key
{"labels": [2]}

# ✅ Correct - Using ids key
{"ids": [2]}
```

### How to Debug Column Mapping Issues
1. **Test the API format:**
   - Use the Monday.com API explorer at https://developer.monday.com/api-reference

2. **Check the error message:**
   - `missingLabel`: Status column label doesn't exist in destination
   - `ColumnValueException`: Wrong format for the column type
   - `invalid value`: The value doesn't match the column's expected format

3. **Check the column type:**
   - Use the Monday.com API explorer at https://developer.monday.com/api-reference/reference/column-types-reference


---

