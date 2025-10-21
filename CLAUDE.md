# Monday.com Item Duplicator - Developer Guide

This guide explains how to extend the column mappings and configure the tool for your Monday.com boards.

## Understanding the .env Configuration

The `.env` file contains all the configuration for the duplicator tool. Here's how to customize it:

### 1. Basic Board Configuration

```bash
# Monday.com API Key
MONDAY_API_KEY=your_api_key_here

# Source Board (where items are copied FROM)
SOURCE_BOARD_ID=8891540298
SOURCE_GROUP_ID=group_mktas044
SOURCE_BOARD_NAME=Content Creation Machine

# Destination Board (where items are copied TO)
DEST_BOARD_ID=5422445730
DEST_GROUP_ID=group_mknzndef
DEST_BOARD_NAME=[TruLaw] - Workshop
```

### 2. Adding Column Mappings

The `COLUMN_MAPPING` maps source column IDs to destination column IDs.

**Format:** Single line JSON object
```bash
COLUMN_MAPPING={"source_col_id": "dest_col_id", "another_source": "another_dest"}
```

**How to Add a New Column Mapping:**

1. **Find the source column ID** (from board SOURCE_BOARD_ID)
   - Press F12 in Monday.com
   - Inspect the column header
   - Look for `data-column-id` attribute
   - Example: `text_mkpvwvnv`

2. **Find the destination column ID** (from board DEST_BOARD_ID)
   - Same process as above
   - Example: `text1`

3. **Add to COLUMN_MAPPING**
   ```bash
   # Before
   COLUMN_MAPPING={"text_mkpvwvnv": "text1"}

   # After adding new mapping
   COLUMN_MAPPING={"text_mkpvwvnv": "text1", "link_mkpv2ga7": "link0"}
   ```

**Current Mappings (7 columns):**
```bash
COLUMN_MAPPING={
  "text_mkpvwvnv": "text1",                    # Focus Keyword
  "text_mkpv7fek": "text_mks07meq",            # Meta Title
  "link_mkpv2ga7": "link0",                    # Surfer Editor Link
  "text_mkpvv0ws": "text_mkwym6gf",            # Surfer Page ID
  "board_relation_mkrcq1m6": "connect_boards__1", # Client Pillars
  "dropdown_mkwy4zej": "dropdown__1",          # Page Types
  "color_mkwyhypq": "color_mksyw5v1"           # Upload Type
}
```

### 3. Adding Friendly Column Names (Optional)

The `COLUMN_NAMES` makes the preview output more readable by showing friendly names instead of column IDs.

**Format:** Single line JSON object mapping column IDs to display names
```bash
COLUMN_NAMES={"col_id": "Display Name", "another_col": "Another Name"}
```

**How to Add Friendly Names:**

For each column mapping, add TWO entries (source and destination):
```bash
COLUMN_NAMES={
  "text_mkpvwvnv": "Focus Keyword",    # Source column
  "text1": "Focus Keyword",            # Destination column
  "link_mkpv2ga7": "Surfer Editor Link",
  "link0": "Surfer Link"
}
```

**Why both?** The tool shows "Source Column → Destination Column" in the preview table, so it needs friendly names for both IDs.

## Column Type Reference

Different Monday.com column types require different data formats:

| Type | Column ID Pattern | Format | Example |
|------|------------------|--------|---------|
| **Text** | `text_*` | Plain string | `"Hello"` |
| **Link** | `link_*` | `{"url": "...", "text": "..."}` | Auto-handled |
| **Status/Color** | `color_*` or `status_*` | `{"label": "Label"}` | Auto-handled |
| **Dropdown** | `dropdown_*` | `{"ids": [1, 2]}` | Auto-handled |
| **Board Relation** | `board_relation_*` or `connect_boards_*` | `{"item_ids": [123]}` | Auto-handled |

**Note:** The tool automatically handles format conversion. You only need to map the column IDs.

## Step-by-Step: Adding a New Column

### Example: Adding "SEO Score" column

1. **Find Column IDs:**
   - Source board: `numbers_abc123`
   - Destination board: `numbers_xyz789`

2. **Update COLUMN_MAPPING:**
   ```bash
   # Add to existing mapping (one line)
   COLUMN_MAPPING={"text_mkpvwvnv": "text1", "numbers_abc123": "numbers_xyz789"}
   ```

3. **Update COLUMN_NAMES (optional but recommended):**
   ```bash
   COLUMN_NAMES={
     "text_mkpvwvnv": "Focus Keyword",
     "text1": "Focus Keyword",
     "numbers_abc123": "SEO Score",
     "numbers_xyz789": "SEO Score"
   }
   ```

4. **Test:**
   - Run `run.bat`
   - Check the preview table shows "SEO Score (Source) → SEO Score (Destination)"
   - Verify the value transfers correctly

## Finding Column IDs - Quick Methods

### Method 1: Browser DevTools (Fastest)
1. Open your Monday.com board
2. Press `F12` to open DevTools
3. Click the "Elements" tab
4. Right-click column header → Inspect
5. Look for `data-column-id="text_mkpvwvnv"`

### Method 2: API Query
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
Run this at: https://developer.monday.com/api-reference

## Troubleshooting

### Column not appearing in preview
**Cause:** Source column is empty
**Solution:** The tool skips empty columns automatically. Ensure source item has a value.

### "missingLabel" error for status columns
**Cause:** Label doesn't exist in destination column
**Solution:** Ensure both boards have the same status label names (e.g., "Done", "Working on it")

### "invalid value" for dropdown
**Cause:** Dropdown IDs don't match between boards
**Solution:** Use the same dropdown options in both boards, or manually adjust after transfer

### Board relation not mapping
**Cause:** Source column is empty
**Solution:** Manually set board relations in source, or column will be skipped

## Testing Changes

After modifying `.env`:

1. **Don't run setup.bat again** - it will overwrite your changes
2. **Run `run.bat`** directly to test
3. **Process one item first** - Type the item name instead of batch mode
4. **Check the preview table** - Verify your new column appears
5. **Type 'n' to cancel** if preview doesn't look right
6. **Fix .env and try again**

## Common JSON Mistakes

❌ **Wrong - Missing quotes:**
```bash
COLUMN_MAPPING={text_abc: text_xyz}
```

✅ **Correct - Double quotes:**
```bash
COLUMN_MAPPING={"text_abc": "text_xyz"}
```

❌ **Wrong - Multiple lines:**
```bash
COLUMN_MAPPING={
  "text_abc": "text_xyz"
}
```

✅ **Correct - Single line:**
```bash
COLUMN_MAPPING={"text_abc": "text_xyz"}
```

❌ **Wrong - Trailing comma:**
```bash
COLUMN_MAPPING={"text_abc": "text_xyz",}
```

✅ **Correct - No trailing comma:**
```bash
COLUMN_MAPPING={"text_abc": "text_xyz"}
```

## Advanced: Board Relations

Board relation columns copy the exact item IDs from source to destination.

**Requirements:**
- Both boards must connect to the SAME third board
- Item IDs must exist in that connected board

**Example:**
```
Source: board_relation_abc → connects to Board X
Destination: connect_boards__1 → must also connect to Board X
```

If source has Item #123 linked, destination will link Item #123 (from Board X).

## Need Help?

- Check the main README.md for user documentation
- Review the Column Type Reference section above
- Test with one item at a time before batch processing
- The preview table shows exactly what will be mapped - use it!

---

**Pro Tip:** Always use the preview and confirmation feature. Type 'n' if anything looks wrong, fix your `.env`, and try again. The tool won't make changes until you confirm with 'y'.
