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

## Example Output

```
================================================================================
Processing Item 1/1
================================================================================

🔍 Processing item: 'My Article' (ID: 12345)
   From group: Ready to Upload

🔎 Checking for existing item in destination board...
✅ No duplicate found - will create new item

======================================================================
📋 PREVIEW - Ready to CREATE
======================================================================

✅ Will Map (5 columns):
  • Name: 'My Article'
  • ✅ text_mkpvwvnv → text1: 'keyword example'
  • ✅ text_mkpv7fek → text_mks07meq: 'Article Title'
  • ✅ link_mkpv2ga7 → link0: https://example.com
  • ✅ text_mkpvv0ws → text_mkwym6gf: '12345'
  • ✅ board_relation_mkrcq1m6 → connect_boards__1: 2 linked item(s)

======================================================================

⚠️  Ready to CREATE this item in the destination board.
   Continue with create? (y/n): y

📊 Creating new item in board 0987654321, group group_xyz789...
✅ Item created successfully! New Item ID: 67890
```

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

#### Issue: Columns not appearing in preview table
**Problem:** Source column is empty or null
**Solution:** The script automatically skips empty columns. Ensure your source items have values in the columns you want to map.

### How to Debug Column Mapping Issues

1. **Check the column type:**
   - Open Monday.com Developer Tools (F12)
   - Inspect the column element
   - Look for the `data-column-type` attribute

2. **Find the correct column ID:**
   ```bash
   # In browser console, on the board page:
   # Look for data-column-id attributes
   ```

3. **Test the API format:**
   Use the Monday.com API explorer at https://developer.monday.com/api-reference to test column value formats

4. **Check the error message:**
   - `missingLabel`: Status column label doesn't exist in destination
   - `ColumnValueException`: Wrong format for the column type
   - `invalid value`: The value doesn't match the column's expected format

### Finding Column IDs

**Method 1: Browser Developer Tools**
1. Open your Monday.com board
2. Press F12 to open Developer Tools
3. Right-click on a column header → Inspect
4. Look for `data-column-id` in the HTML

**Method 2: API Query**
```graphql
{
  boards(ids: [YOUR_BOARD_ID]) {
    columns {
      id
      title
      type
    }
  }
}
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| "MONDAY_API_KEY is missing" | Run `setup.bat` again to create `.env` file |
| "Item not found" | Check item name spelling (case-sensitive) |
| GraphQL errors | Verify Board IDs, Group IDs, and API key permissions |
| Column not mapping | See Advanced Configuration → Column Type Reference |

## Advanced Configuration

<details>
<summary>Click to expand advanced topics</summary>

### Finding Board and Group IDs

**Board ID:**
- Open your board in Monday.com
- Look at the URL: `https://yourcompany.monday.com/boards/1234567890`
- The number is your Board ID

**Group ID:**
- Press F12 on the board
- Inspect a group title element
- Look for `data-id` attribute (e.g., `group_abc123`)

**Column IDs:**
- Use Developer Tools (F12) and inspect column headers
- Or use Monday.com API explorer: https://developer.monday.com/api-reference

### Column Mapping Format

Edit `.env` file manually. `COLUMN_MAPPING` must be valid JSON on one line:

```bash
COLUMN_MAPPING={"source_col_id": "dest_col_id", "another_source": "another_dest"}
```

Example:
```bash
COLUMN_MAPPING={"text_mkpvwvnv": "text1", "link_mkpv2ga7": "link0"}
```

### Supported Column Types

| Type | Format | Example |
|------|--------|---------|
| Text | `"text"` | `"Hello"` |
| Link | `{"url": "...", "text": "..."}` | `{"url": "https://example.com"}` |
| Status/Color | `{"label": "Label"}` | `{"label": "Done"}` |
| Dropdown | `{"ids": [1, 2]}` | `{"ids": [2]}` |
| Board Relation | `{"item_ids": [123]}` | `{"item_ids": [789]}` |

</details>

---

## Security Note

⚠️ **Never commit your `.env` file** - it contains your API key!

---

**Made with ❤️ for the Monday.com community**  
