# Monday.com Item Duplicator

A Python tool to duplicate items between Monday.com boards with column mapping support and duplicate detection.

## ✨ Features

- ✅ **Duplicate Detection** - Automatically detects existing items and updates them instead of creating duplicates
- 🔄 **Batch Processing** - Process all items from a group or individual items
- 🎯 **Column Mapping** - Map columns from source to destination boards with different column IDs
- ⚡ **User Confirmation** - Preview changes before creating/updating items
- 📊 **Detailed Logging** - Clear output showing what was mapped and the results
- 🔒 **Secure Configuration** - All sensitive data stored in `.env` file

## Supported Column Types

- Text columns
- Link columns
- Board relation columns
- Status columns
- Date columns
- And more (the tool attempts to handle all column types)

## Prerequisites

- Python 3.7 or higher
- Monday.com account with API access
- API key from Monday.com

## Installation

### Windows

1. Clone this repository:
```bash
git clone https://github.com/yourusername/monday-item-duplicator.git
cd monday-item-duplicator
```

2. Run the setup script:
```bash
setup.bat
```

This will:
- Create a Python virtual environment
- Install required dependencies
- Help you create a `.env` file

### Linux/Mac

1. Clone this repository:
```bash
git clone https://github.com/yourusername/monday-item-duplicator.git
cd monday-item-duplicator
```

2. Create and activate a virtual environment:
```bash
python3 -m venv .venv
source .venv/bin/activate  # On Mac/Linux
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create your `.env` file (see Configuration below)

## Configuration

### 1. Get Your Monday.com API Key

1. Go to your Monday.com account
2. Click on your profile picture → Admin
3. Navigate to **API** section
4. Generate or copy your API token

### 2. Configure the .env File

Copy `.env.example` to `.env`:
```bash
cp .env.example .env
```

Edit `.env` with your configuration:

```bash
# Monday.com API Key
MONDAY_API_KEY=your_actual_api_key_here

# Source Board (where items are copied FROM)
SOURCE_BOARD_ID=1234567890
SOURCE_GROUP_ID=group_abc123
SOURCE_BOARD_NAME=Content Creation Machine

# Destination Board (where items are copied TO)
DEST_BOARD_ID=0987654321
DEST_GROUP_ID=group_xyz789
DEST_BOARD_NAME=Workshop Board

# Column Mapping (JSON format)
COLUMN_MAPPING={"text_source": "text_dest", "link_source": "link_dest"}
```

### 3. Finding Board and Group IDs

**Board ID:**
- Open your board in Monday.com
- Look at the URL: `https://yourcompany.monday.com/boards/1234567890`
- The number at the end is your Board ID

**Group ID:**
- Open your browser's Developer Tools (F12)
- Inspect a group title element
- Look for `data-id` attribute (e.g., `group_abc123`)

**Column IDs:**
- Use Monday.com's API explorer: https://api.developer.monday.com/docs
- Or inspect column elements in Developer Tools

### 4. Column Mapping Format

The `COLUMN_MAPPING` must be valid JSON on a single line:

```json
{"source_column_id": "destination_column_id", "another_source": "another_dest"}
```

Example:
```bash
COLUMN_MAPPING={"text_mkpvwvnv": "text1", "link_mkpv2ga7": "link0", "board_relation_mkrcq1m6": "connect_boards__1"}
```

## Usage

### Batch Mode (Process All Items)

Process all items from the source group:

**Windows:**
```bash
run.bat
```

**Linux/Mac:**
```bash
source .venv/bin/activate
python monday_item_duplicator.py
```

### Single Item Mode

Process a specific item by name:

**Windows:**
```bash
run.bat "Item Name Here"
```

**Linux/Mac:**
```bash
source .venv/bin/activate
python monday_item_duplicator.py "Item Name Here"
```

## How It Works

1. **Fetches Items** - Gets items from the source board/group
2. **Checks for Duplicates** - Searches destination board for items with the same name
3. **Shows Preview** - Displays what columns will be mapped
4. **User Confirmation** - Asks "Continue with create/update? (y/n)"
5. **Creates or Updates** - If confirmed:
   - Creates new item if it doesn't exist
   - Updates existing item if it already exists
6. **Displays Summary** - Shows what was created/updated

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

### "MONDAY_API_KEY is missing"
- Make sure you created a `.env` file
- Check that `MONDAY_API_KEY` is set in `.env`
- Ensure there are no quotes around the API key value

### "COLUMN_MAPPING is not valid JSON"
- Ensure the mapping is on a single line
- Use double quotes `"` not single quotes `'`
- Escape any special characters if needed

### "Item not found"
- Verify the item name is spelled exactly as it appears in Monday.com
- Check that you're looking in the correct board and group

### GraphQL Errors
- Verify your API key has the correct permissions
- Check that Board IDs and Group IDs are correct
- Ensure column IDs exist in both source and destination boards
- See "Column Type Reference" above for column-specific formatting issues

## Security Notes

- ⚠️ **Never commit your `.env` file** - It contains your API key
- The `.gitignore` file is configured to exclude `.env` automatically
- Share `.env.example` with others, not `.env`

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

MIT License - feel free to use this tool for your projects!

## Support

If you encounter any issues or have questions:
1. Check the Troubleshooting section
2. Review your `.env` configuration
3. Open an issue on GitHub

## Author

Created to help teams automate Monday.com board management.

---

**Made with ❤️ for the Monday.com community**  
