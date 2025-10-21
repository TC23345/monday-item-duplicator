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

### 3. Adding Display Column Names

The `COLUMN_NAMES` makes the preview output more readable by showing friendly names instead of column IDs.

**Format:** Single line JSON object mapping column IDs to display names
```bash
COLUMN_NAMES={"col_id": "Display Name", "another_col": "Another Name"}
```

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

---

## Testing Changes

After modifying `.env`:

1. **Don't run setup.bat again** - it will overwrite your changes
2. **Run `run.bat`** directly to test
3. **Process one item first** - Type the item name instead of batch mode
4. **Check the preview table** - Verify your new column appears
5. **Type 'n' to cancel** if preview doesn't look right
6. **Fix .env and try again**

---

