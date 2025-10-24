#!/usr/bin/env python3
"""
Monday.com Item Duplicator - Main Runner
Interactive menu and CLI interface for workflow-based duplication
"""

import sys
import os
import argparse
from dotenv import load_dotenv
from config_loader import ConfigLoader
from monday_item_duplicator import MondayItemDuplicator

# Load environment variables
load_dotenv()


def print_banner():
    """Print application banner"""
    print("=" * 80)
    print("🚀 Monday.com Item Duplicator - Multi-Workflow Edition")
    print("=" * 80)
    print()


def print_workflow_menu(workflows):
    """Print available workflows as a menu"""
    print("📋 Available Workflows:")
    print()

    for idx, workflow in enumerate(workflows, 1):
        status = "✓" if workflow.enabled else "✗"
        dest_names = ", ".join([d.board_name for d in workflow.destinations])
        print(f"  [{idx}] {workflow.name} {status}")
        print(f"      Source: {workflow.source.board_name}")
        print(f"      Destinations: {dest_names}")
        print()


def select_workflow_interactive(config_loader):
    """Interactive workflow selection"""
    workflows = config_loader.get_enabled_workflows()

    if not workflows:
        print("❌ No enabled workflows found in config/workflows.json")
        print("   Please enable at least one workflow and try again.")
        sys.exit(1)

    print_workflow_menu(workflows)

    while True:
        try:
            choice = input(f"Select workflow [1-{len(workflows)}] or 'q' to quit: ").strip()

            if choice.lower() == 'q':
                print("👋 Goodbye!")
                sys.exit(0)

            idx = int(choice) - 1
            if 0 <= idx < len(workflows):
                return workflows[idx]
            else:
                print(f"❌ Invalid choice. Please enter 1-{len(workflows)}")
        except ValueError:
            print("❌ Invalid input. Please enter a number or 'q'")
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            sys.exit(0)


def get_item_name_interactive():
    """Interactive item name input"""
    print("\n" + "=" * 80)
    print("📝 Item Selection")
    print("=" * 80)
    print()
    print("Options:")
    print("  • Enter an item name to process a single item")
    print("  • Enter 'batch' to process all items from the source group")
    print("  • Enter 'q' to quit")
    print()

    while True:
        try:
            item_name = input("Enter item name or 'batch': ").strip()

            if item_name.lower() == 'q':
                print("👋 Goodbye!")
                sys.exit(0)

            if item_name.lower() == 'batch':
                return None  # None indicates batch mode

            if item_name:
                return item_name

            print("❌ Please enter a valid item name or 'batch'")
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            sys.exit(0)


def run_workflow(
    duplicator,
    workflow,
    destination,
    column_mapping,
    column_names,
    item_name=None
):
    """
    Run duplication workflow for a single destination

    Args:
        duplicator: MondayItemDuplicator instance
        workflow: Workflow configuration
        destination: Destination configuration
        column_mapping: Resolved column mapping dict
        column_names: Resolved column names dict
        item_name: Item to process (None for batch mode)
    """
    source = workflow.source

    if item_name:
        # Single item mode
        print(f"\n📌 Processing: '{item_name}'")
        print(f"   Source: {source.board_name}")
        print(f"   Destination: {destination.board_name}")
        print()

        # Get source item
        source_item = duplicator.get_item_by_name(source.board_id, item_name)

        if not source_item:
            print(f"❌ Item '{item_name}' not found in {source.board_name}")
            return

        # Duplicate the item
        result = duplicator.duplicate_item_from_data(
            source_item=source_item,
            dest_board_id=destination.board_id,
            dest_group_id=destination.group_id,
            column_mapping=column_mapping,
            column_names=column_names,
            source_board_name=source.board_name,
            dest_board_name=destination.board_name
        )

        print(f"\n🎉 Process complete!")
        print(f"   Action: {result['action']}")
        if result['dest_item_id']:
            print(f"   Item URL: https://your-account.monday.com/boards/{destination.board_id}/pulses/{result['dest_item_id']}")

    else:
        # Batch mode
        print(f"\n📦 Batch Mode")
        print(f"   Source: {source.board_name} / {source.group_id}")
        print(f"   Destination: {destination.board_name} / {destination.group_id}")
        print()

        # Get all items from source group
        print(f"🔍 Fetching items from {source.board_name}...")
        items = duplicator.get_items_from_group(source.board_id, source.group_id)

        if not items:
            print(f"⚠️  No items found in group '{source.group_id}'")
            return

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
                result = duplicator.duplicate_item_from_data(
                    source_item=item,
                    dest_board_id=destination.board_id,
                    dest_group_id=destination.group_id,
                    column_mapping=column_mapping,
                    column_names=column_names,
                    source_board_name=source.board_name,
                    dest_board_name=destination.board_name
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


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="Monday.com Item Duplicator - Multi-Workflow Edition"
    )
    parser.add_argument(
        "--workflow",
        type=str,
        help="Workflow ID to use (skips interactive menu)"
    )
    parser.add_argument(
        "--item",
        type=str,
        help="Item name to process (omit for batch mode)"
    )
    parser.add_argument(
        "--batch",
        action="store_true",
        help="Process all items in batch mode"
    )
    parser.add_argument(
        "--list",
        action="store_true",
        help="List all available workflows and exit"
    )

    args = parser.parse_args()

    # Load configuration
    try:
        config_loader = ConfigLoader()
    except FileNotFoundError as e:
        print(f"❌ {e}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error loading configuration: {e}")
        sys.exit(1)

    # List workflows if requested
    if args.list:
        print_banner()
        workflows = config_loader.list_workflows()
        for workflow in workflows:
            status = "✓" if workflow["enabled"] else "✗"
            print(f"{workflow['id']:20s} {status} {workflow['name']}")
            print(f"  Source: {workflow['source_board']}")
            print(f"  Destinations: {', '.join(workflow['destinations'])}")
            print()
        sys.exit(0)

    # Get API key
    api_key = os.getenv("MONDAY_API_KEY")
    if not api_key:
        print("❌ MONDAY_API_KEY not found in .env file")
        sys.exit(1)

    # Initialize duplicator
    duplicator = MondayItemDuplicator(api_key)

    # Select workflow
    if args.workflow:
        workflow = config_loader.get_workflow(args.workflow)
        if not workflow:
            print(f"❌ Workflow '{args.workflow}' not found")
            sys.exit(1)
        if not workflow.enabled:
            print(f"❌ Workflow '{args.workflow}' is disabled")
            sys.exit(1)
    else:
        print_banner()
        workflow = select_workflow_interactive(config_loader)

    # Determine item name (single or batch mode)
    if args.batch:
        item_name = None
    elif args.item:
        item_name = args.item
    else:
        item_name = get_item_name_interactive()

    # Process each destination
    print(f"\n{'=' * 80}")
    print(f"🚀 Running Workflow: {workflow.name}")
    print(f"{'=' * 80}")

    for dest_idx, destination in enumerate(workflow.destinations, 1):
        print(f"\n{'=' * 80}")
        print(f"📍 Destination {dest_idx}/{len(workflow.destinations)}: {destination.board_name}")
        print(f"{'=' * 80}")

        # Resolve column mappings and names
        column_mapping = config_loader.resolve_column_mappings(destination)
        column_names = config_loader.resolve_column_names(destination)

        print(f"\n✓ Template: {destination.template or 'None'}")
        print(f"✓ Column Mappings: {len(column_mapping)} columns")

        # Run workflow for this destination
        try:
            run_workflow(
                duplicator=duplicator,
                workflow=workflow,
                destination=destination,
                column_mapping=column_mapping,
                column_names=column_names,
                item_name=item_name
            )
        except Exception as e:
            print(f"\n❌ Error processing destination '{destination.board_name}': {e}")
            import traceback
            traceback.print_exc()
            continue

    print(f"\n{'=' * 80}")
    print("🎉 All destinations processed!")
    print(f"{'=' * 80}")


if __name__ == "__main__":
    main()
