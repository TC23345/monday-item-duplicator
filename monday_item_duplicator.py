#!/usr/bin/env python3
"""
Monday.com Item Duplicator
Duplicates items from one board/group to another with column mapping
Includes duplicate detection - updates existing items instead of creating duplicates
"""

import requests
import json
import sys
import os
from typing import Dict, List, Optional
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class MondayItemDuplicator:
    def __init__(self, api_key: str):
        """Initialize with Monday.com API key"""
        self.api_key = api_key
        self.api_url = "https://api.monday.com/v2"
        self.headers = {
            "Authorization": api_key,
            "Content-Type": "application/json"
        }
    
    def execute_query(self, query: str, variables: Optional[Dict] = None) -> Dict:
        """Execute a GraphQL query against Monday.com API"""
        data = {"query": query}
        if variables:
            data["variables"] = variables
        
        response = requests.post(
            self.api_url,
            headers=self.headers,
            json=data
        )
        
        if response.status_code != 200:
            raise Exception(f"Query failed with status {response.status_code}: {response.text}")
        
        result = response.json()
        if "errors" in result:
            raise Exception(f"GraphQL errors: {result['errors']}")
        
        return result["data"]
    
    def get_item_by_name(self, board_id: int, item_name: str) -> Optional[Dict]:
        """Get an item by name from a board"""
        query = """
        query ($boardId: [ID!]) {
            boards(ids: $boardId) {
                items_page(query_params: {rules: [{column_id: "name", compare_value: ["%s"]}]}) {
                    items {
                        id
                        name
                        group {
                            id
                            title
                        }
                        column_values {
                            id
                            text
                            value
                            type
                        }
                    }
                }
            }
        }
        """ % item_name

        variables = {
            "boardId": [board_id]
        }

        data = self.execute_query(query, variables)
        items = data["boards"][0]["items_page"]["items"]

        return items[0] if items else None
    
    def get_items_from_group(self, board_id: int, group_id: str) -> List[Dict]:
        """Get all items from a specific group in a board"""
        query = """
        query ($boardId: ID!) {
            boards(ids: [$boardId]) {
                items_page(limit: 500) {
                    items {
                        id
                        name
                        group {
                            id
                            title
                        }
                        column_values {
                            id
                            text
                            value
                            type
                        }
                    }
                }
            }
        }
        """
        
        variables = {"boardId": str(board_id)}
        data = self.execute_query(query, variables)
        
        all_items = data["boards"][0]["items_page"]["items"]
        
        # Filter items by group_id
        group_items = [item for item in all_items if item["group"]["id"] == group_id]
        
        return group_items
    
    def create_item_with_values(
        self,
        board_id: int,
        group_id: str,
        item_name: str,
        column_values: Dict
    ) -> Dict:
        """Create a new item with column values"""
        query = """
        mutation ($boardId: ID!, $groupId: String!, $itemName: String!, $columnValues: JSON!) {
            create_item(
                board_id: $boardId,
                group_id: $groupId,
                item_name: $itemName,
                column_values: $columnValues
            ) {
                id
                name
            }
        }
        """
        
        variables = {
            "boardId": str(board_id),
            "groupId": group_id,
            "itemName": item_name,
            "columnValues": json.dumps(column_values)
        }
        
        data = self.execute_query(query, variables)
        return data["create_item"]
    
    def update_item_column_values(
        self,
        board_id: int,
        item_id: str,
        column_values: Dict
    ) -> Dict:
        """Update column values on an existing item"""
        query = """
        mutation ($boardId: ID!, $itemId: ID!, $columnValues: JSON!) {
            change_multiple_column_values(
                board_id: $boardId,
                item_id: $itemId,
                column_values: $columnValues
            ) {
                id
                name
            }
        }
        """
        
        variables = {
            "boardId": str(board_id),
            "itemId": str(item_id),
            "columnValues": json.dumps(column_values)
        }
        
        data = self.execute_query(query, variables)
        return data["change_multiple_column_values"]
    
    def duplicate_item(
        self,
        source_board_id: int,
        source_item_name: str,
        dest_board_id: int,
        dest_group_id: str,
        column_mapping: Dict[str, str]
    ) -> Dict:
        """
        Duplicate an item from source to destination board
        
        Args:
            source_board_id: Source board ID
            source_item_name: Name of item to duplicate
            dest_board_id: Destination board ID
            dest_group_id: Destination group ID
            column_mapping: Dict mapping source column IDs to destination column IDs
                           Format: {"source_col_id": "dest_col_id"}
        
        Returns:
            Dict with duplicate results and mapping summary
        """
        print(f"🔍 Searching for item: '{source_item_name}' in board {source_board_id}...")
        
        # Get source item
        source_item = self.get_item_by_name(source_board_id, source_item_name)
        
        if not source_item:
            raise Exception(f"Item '{source_item_name}' not found in board {source_board_id}")
        
        print(f"✅ Found item (ID: {source_item['id']}) in group: {source_item['group']['title']}")

        return self.duplicate_item_from_data(
            source_item,
            dest_board_id,
            dest_group_id,
            column_mapping,
            column_names={},
            source_board_name="Source",
            dest_board_name="Destination"
        )
    
    def duplicate_item_from_data(
        self,
        source_item: Dict,
        dest_board_id: int,
        dest_group_id: str,
        column_mapping: Dict[str, str],
        column_names: Dict[str, str] = None,
        source_board_name: str = "Source",
        dest_board_name: str = "Destination"
    ) -> Dict:
        """
        Duplicate an item using existing item data
        If item already exists in destination, updates it instead of creating a duplicate
        
        Args:
            source_item: Item data dict with id, name, group, and column_values
            dest_board_id: Destination board ID
            dest_group_id: Destination group ID
            column_mapping: Dict mapping source column IDs to destination column IDs
        
        Returns:
            Dict with duplicate results and mapping summary
        """
        print(f"🔍 Processing item: '{source_item['name']}' (ID: {source_item['id']})")
        print(f"   From group: {source_item['group']['title']}")
        
        # Check if item already exists in destination board
        print(f"\n🔎 Checking for existing item in destination board...")
        existing_item = self.get_item_by_name(dest_board_id, source_item['name'])
        
        if existing_item:
            print(f"⚠️  Item already exists in destination!")
            print(f"   Existing Item ID: {existing_item['id']}")
            print(f"   Group: {existing_item['group']['title']}")
            print(f"   → Will UPDATE existing item instead of creating duplicate")
            is_update = True
            dest_item_id = existing_item['id']
        else:
            print(f"✅ No duplicate found - will create new item")
            is_update = False
            dest_item_id = None
        
        # Extract column values
        source_columns = {col["id"]: col for col in source_item["column_values"]}
        
        # Map columns to destination
        mapped_values = {}
        mapped_summary = []
        unmapped_summary = []

        # Use column names if provided, otherwise use IDs
        if column_names is None:
            column_names = {}

        for source_col_id, dest_col_id in column_mapping.items():
            if source_col_id in source_columns:
                col = source_columns[source_col_id]

                # Skip empty values
                if not col["value"] or col["value"] == "null":
                    continue

                # Get friendly names for display
                source_name = column_names.get(source_col_id, source_col_id)
                dest_name = column_names.get(dest_col_id, dest_col_id)
                mapping_display = f"{source_name} ({source_board_name}) → {dest_name} ({dest_board_name})"

                try:
                    # Parse the value
                    value_data = json.loads(col["value"])

                    # Handle different column types
                    if col["type"] == "text":
                        mapped_values[dest_col_id] = col["text"]
                        mapped_summary.append(f"✅ {mapping_display}: '{col['text']}'")

                    elif col["type"] == "link":
                        # Set URL as both the link and display text
                        url = value_data.get("url", "")
                        mapped_values[dest_col_id] = {
                            "url": url,
                            "text": url
                        }
                        mapped_summary.append(f"✅ {mapping_display}: {url}")

                    elif col["type"] == "board-relation":
                        # Extract linked item IDs
                        linked_items = value_data.get("linkedPulseIds", [])
                        if linked_items:
                            item_ids = [int(item["linkedPulseId"]) for item in linked_items]
                            mapped_values[dest_col_id] = {"item_ids": item_ids}
                            mapped_summary.append(f"✅ {mapping_display}: {len(item_ids)} linked item(s)")

                    else:
                        # For other types, try to use the raw value
                        mapped_values[dest_col_id] = value_data
                        mapped_summary.append(f"✅ {mapping_display}: {col['text']}")

                except json.JSONDecodeError:
                    # If value isn't JSON, use text representation
                    mapped_values[dest_col_id] = col["text"]
                    mapped_summary.append(f"✅ {mapping_display}: '{col['text']}'")
        
        # Print preview summary and get confirmation
        action_text = "UPDATE" if is_update else "CREATE"

        # Build table data first to calculate column widths
        table_rows = []

        # Name row (always mapped)
        table_rows.append(("Name", "Name", source_item['name']))

        # Other columns
        for source_col_id, dest_col_id in column_mapping.items():
            if source_col_id in source_columns:
                col = source_columns[source_col_id]

                # Skip empty values
                if not col["value"] or col["value"] == "null":
                    continue

                # Get friendly names
                source_name = column_names.get(source_col_id, source_col_id)
                dest_name = column_names.get(dest_col_id, dest_col_id)

                # Get display value
                try:
                    value_data = json.loads(col["value"])

                    if col["type"] == "link":
                        display_value = value_data.get("url", "")
                    elif col["type"] == "board-relation":
                        linked_items = value_data.get("linkedPulseIds", [])
                        display_value = f"{len(linked_items)} linked item(s)" if linked_items else ""
                    else:
                        display_value = col["text"] or ""
                except:
                    display_value = col["text"] or ""

                table_rows.append((source_name, dest_name, display_value))

        # Calculate maximum widths for each column
        max_source = max(len(row[0]) for row in table_rows) if table_rows else 20
        max_dest = max(len(row[1]) for row in table_rows) if table_rows else 20
        max_value = max(len(str(row[2])) for row in table_rows) if table_rows else 20

        # Create header text with board names
        source_header = f"Source Column: ({source_board_name})"
        dest_header = f"Destination Column: ({dest_board_name})"

        # Add some padding and account for header text
        max_source = max(max_source, len(source_header))
        max_dest = max(max_dest, len(dest_header))
        max_value = max(max_value, len("Value"))

        total_width = max_source + max_dest + max_value + 6  # 6 for separators

        print("=" * total_width)
        print(f"📋 PREVIEW - Ready to {action_text}")
        print("=" * total_width)

        print(f"\n✅ Will Map ({len(table_rows)} columns):\n")

        # Print table header
        print(f"{source_header:<{max_source}} | {dest_header:<{max_dest}} | Value")
        print(f"{'-' * max_source} | {'-' * max_dest} | {'-' * max_value}")

        # Print table rows
        for source_col, dest_col, value in table_rows:
            print(f"{source_col:<{max_source}} | {dest_col:<{max_dest}} | {value}")

        print("\n" + "=" * total_width)

        # Get user confirmation
        print(f"\n⚠️  Ready to {action_text} this item in the destination board.")
        response = input(f"   Continue with {action_text.lower()}? (y/n): ").strip().lower()

        if response != 'y':
            print(f"❌ {action_text} cancelled by user.")
            return {
                "source_item_id": source_item["id"],
                "dest_item_id": None,
                "item_name": source_item["name"],
                "action": "CANCELLED",
                "was_updated": False,
                "mapped_columns": 0,
                "unmapped_columns": 0
            }

        # Create or update item
        if is_update:
            print(f"\n📝 Updating existing item {dest_item_id} in board {dest_board_id}...")
            result_item = self.update_item_column_values(
                dest_board_id,
                dest_item_id,
                mapped_values
            )
            print(f"✅ Item updated successfully! Item ID: {result_item['id']}\n")
            action = "UPDATED"
        else:
            print(f"\n📊 Creating new item in board {dest_board_id}, group {dest_group_id}...")
            result_item = self.create_item_with_values(
                dest_board_id,
                dest_group_id,
                source_item["name"],
                mapped_values
            )
            print(f"✅ Item created successfully! New Item ID: {result_item['id']}\n")
            action = "CREATED"

        # Print final summary
        print("=" * 70)
        print(f"📋 FINAL SUMMARY ({action})")
        print("=" * 70)

        print(f"\n✅ Successfully Mapped ({len(mapped_summary)} columns):")
        print(f"  • Name: '{result_item['name']}'")
        for item in mapped_summary:
            print(f"  • {item}")

        print("\n" + "=" * 70)
        
        return {
            "source_item_id": source_item["id"],
            "dest_item_id": result_item["id"],
            "item_name": result_item["name"],
            "action": action,
            "was_updated": is_update,
            "mapped_columns": len(mapped_summary),
            "unmapped_columns": len(unmapped_summary)
        }


def main():
    """Main function to run the duplicator"""

    # ============================================================================
    # Configuration - Load from .env file
    # ============================================================================

    # API Key
    API_KEY = os.getenv("MONDAY_API_KEY")

    # Source Board Configuration
    SOURCE_BOARD_ID = int(os.getenv("SOURCE_BOARD_ID", "0"))
    SOURCE_GROUP_ID = os.getenv("SOURCE_GROUP_ID", "")
    SOURCE_BOARD_NAME = os.getenv("SOURCE_BOARD_NAME", "Source Board")

    # Destination Board Configuration
    DEST_BOARD_ID = int(os.getenv("DEST_BOARD_ID", "0"))
    DEST_GROUP_ID = os.getenv("DEST_GROUP_ID", "")
    DEST_BOARD_NAME = os.getenv("DEST_BOARD_NAME", "Destination Board")

    # Item to duplicate - get from command line argument or default to batch mode
    # Usage: python monday_item_duplicator.py "Item Name"
    # If no argument provided: process all items (batch mode)
    if len(sys.argv) > 1:
        SOURCE_ITEM_NAME = sys.argv[1]
    else:
        SOURCE_ITEM_NAME = ""  # Empty = batch mode (process all items)

    # ============================================================================
    # Column Mapping
    # ============================================================================
    # Load column mapping from environment variable
    # Format in .env: COLUMN_MAPPING={"source_col_id": "dest_col_id", ...}

    column_mapping_str = os.getenv("COLUMN_MAPPING", "{}")
    try:
        COLUMN_MAPPING = json.loads(column_mapping_str)
    except json.JSONDecodeError:
        print("❌ Error: COLUMN_MAPPING in .env file is not valid JSON!")
        print("   Expected format: COLUMN_MAPPING={\"source_col_id\": \"dest_col_id\"}")
        sys.exit(1)

    # ============================================================================
    # Column Display Names (Optional - for better visualization)
    # ============================================================================
    # Maps column IDs to friendly display names for the preview
    # Format in .env: COLUMN_NAMES={"col_id": "Display Name", ...}

    column_names_str = os.getenv("COLUMN_NAMES", "{}")
    try:
        COLUMN_NAMES = json.loads(column_names_str) if column_names_str else {}
    except json.JSONDecodeError:
        COLUMN_NAMES = {}
    
    # ============================================================================
    # Validate Configuration
    # ============================================================================

    validation_errors = []

    if not API_KEY:
        validation_errors.append("MONDAY_API_KEY is missing")

    if SOURCE_BOARD_ID == 0:
        validation_errors.append("SOURCE_BOARD_ID is missing or invalid")

    if not SOURCE_GROUP_ID:
        validation_errors.append("SOURCE_GROUP_ID is missing")

    if DEST_BOARD_ID == 0:
        validation_errors.append("DEST_BOARD_ID is missing or invalid")

    if not DEST_GROUP_ID:
        validation_errors.append("DEST_GROUP_ID is missing")

    if not COLUMN_MAPPING:
        validation_errors.append("COLUMN_MAPPING is missing or empty")

    if validation_errors:
        print("❌ Configuration Error! Missing required values in .env file:")
        for error in validation_errors:
            print(f"   • {error}")
        print("\n   Please check your .env file and ensure all required values are set.")
        print("   See .env.example for the correct format.")
        print("\n   Get your API key from: https://your-account.monday.com/admin/integrations/api")
        sys.exit(1)
    
    print("=" * 80)
    print("🚀 Monday.com Item Duplicator with Duplicate Detection")
    print("=" * 80)
    print(f"\n📋 Configuration:")
    print(f"   API Key: Loaded from .env ✓")
    print(f"   Source: {SOURCE_BOARD_NAME} (Board: {SOURCE_BOARD_ID}, Group: {SOURCE_GROUP_ID})")
    print(f"   Destination: {DEST_BOARD_NAME} (Board: {DEST_BOARD_ID}, Group: {DEST_GROUP_ID})")
    print(f"   Columns to map: {len(COLUMN_MAPPING)} columns")
    print(f"   Duplicate Detection: ENABLED ✓")
    print()
    
    try:
        # Initialize duplicator
        duplicator = MondayItemDuplicator(API_KEY)
        
        # Determine if processing single item or all items from group
        if SOURCE_ITEM_NAME:
            # Single item mode
            print(f"📌 Single Item Mode: Processing '{SOURCE_ITEM_NAME}'")
            print()
            
            result = duplicator.duplicate_item(
                source_board_id=SOURCE_BOARD_ID,
                source_item_name=SOURCE_ITEM_NAME,
                dest_board_id=DEST_BOARD_ID,
                dest_group_id=DEST_GROUP_ID,
                column_mapping=COLUMN_MAPPING
            )
            
            print(f"\n🎉 Process complete!")
            print(f"   Action: {result['action']}")
            print(f"   Source Item ID: {result['source_item_id']}")
            print(f"   Destination Item ID: {result['dest_item_id']}")
            print(f"   Item URL: https://your-account.monday.com/boards/{DEST_BOARD_ID}/pulses/{result['dest_item_id']}")
            
        else:
            # Batch mode - process all items from source group
            print(f"📦 Batch Mode: Processing all items from group '{SOURCE_GROUP_ID}'")
            print()
            
            # Get all items from source group
            print(f"🔍 Fetching items from {SOURCE_BOARD_NAME}...")
            items = duplicator.get_items_from_group(SOURCE_BOARD_ID, SOURCE_GROUP_ID)
            
            if not items:
                print(f"⚠️  No items found in group '{SOURCE_GROUP_ID}'")
                sys.exit(0)
            
            print(f"✅ Found {len(items)} item(s) to process\n")
            
            # Process each item
            results = []
            created_count = 0
            updated_count = 0
            cancelled_count = 0

            for idx, item in enumerate(items, 1):
                print(f"\n{'=' * 80}")
                print(f"Processing Item {idx}/{len(items)}")
                print(f"{'=' * 80}\n")

                try:
                    # Use duplicate_item with the item data directly
                    result = duplicator.duplicate_item_from_data(
                        source_item=item,
                        dest_board_id=DEST_BOARD_ID,
                        dest_group_id=DEST_GROUP_ID,
                        column_mapping=COLUMN_MAPPING,
                        column_names=COLUMN_NAMES,
                        source_board_name=SOURCE_BOARD_NAME,
                        dest_board_name=DEST_BOARD_NAME
                    )
                    results.append(result)

                    if result['action'] == 'CANCELLED':
                        cancelled_count += 1
                    elif result['was_updated']:
                        updated_count += 1
                    else:
                        created_count += 1

                except Exception as e:
                    print(f"❌ Failed to process '{item['name']}': {str(e)}")
                    continue

            # Print summary
            print(f"\n{'=' * 80}")
            print(f"📊 BATCH PROCESSING SUMMARY")
            print(f"{'=' * 80}")
            print(f"\n✅ Successfully processed: {created_count + updated_count}/{len(items)} items")
            print(f"   • Created: {created_count}")
            print(f"   • Updated: {updated_count}")
            if cancelled_count > 0:
                print(f"   • Cancelled: {cancelled_count}")
            
            if results:
                if created_count > 0:
                    print(f"\n📋 Items Created:")
                    for result in results:
                        if result['action'] == 'CREATED':
                            print(f"   • {result['item_name']} (ID: {result['dest_item_id']})")
                            print(f"     URL: https://your-account.monday.com/boards/{DEST_BOARD_ID}/pulses/{result['dest_item_id']}")

                if updated_count > 0:
                    print(f"\n🔄 Items Updated:")
                    for result in results:
                        if result['action'] == 'UPDATED':
                            print(f"   • {result['item_name']} (ID: {result['dest_item_id']})")
                            print(f"     URL: https://your-account.monday.com/boards/{DEST_BOARD_ID}/pulses/{result['dest_item_id']}")

                if cancelled_count > 0:
                    print(f"\n⏭️  Items Cancelled:")
                    for result in results:
                        if result['action'] == 'CANCELLED':
                            print(f"   • {result['item_name']}")
        
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
