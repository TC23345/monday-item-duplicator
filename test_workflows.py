#!/usr/bin/env python3
"""
Test script for Monday.com Item Duplicator workflow system
Validates configuration without making any API calls
"""

import os
import sys
from dotenv import load_dotenv
from config_loader import ConfigLoader

# ANSI color codes for pretty output
GREEN = '\033[92m'
YELLOW = '\033[93m'
RED = '\033[91m'
BLUE = '\033[94m'
RESET = '\033[0m'
BOLD = '\033[1m'


def print_header(text):
    """Print a formatted header"""
    print(f"\n{BLUE}{BOLD}{'=' * 80}{RESET}")
    print(f"{BLUE}{BOLD}{text}{RESET}")
    print(f"{BLUE}{BOLD}{'=' * 80}{RESET}\n")


def print_success(text, indent=0):
    """Print success message"""
    prefix = "  " * indent
    print(f"{prefix}{GREEN}✓ {text}{RESET}")


def print_warning(text, indent=0):
    """Print warning message"""
    prefix = "  " * indent
    print(f"{prefix}{YELLOW}⚠ {text}{RESET}")


def print_error(text, indent=0):
    """Print error message"""
    prefix = "  " * indent
    print(f"{prefix}{RED}✗ {text}{RESET}")


def print_info(text, indent=0):
    """Print info message"""
    prefix = "  " * indent
    print(f"{prefix}{text}")


def test_env_file():
    """Test .env file existence and API key"""
    print_header("Testing Environment Configuration")

    # Load .env
    load_dotenv()

    # Check if .env exists
    if not os.path.exists('.env'):
        print_error(".env file not found")
        print_info("Please create .env file with MONDAY_API_KEY", 1)
        return False

    print_success(".env file exists")

    # Check API key
    api_key = os.getenv("MONDAY_API_KEY")
    if not api_key:
        print_error("MONDAY_API_KEY not found in .env")
        return False

    print_success(f"MONDAY_API_KEY found ({len(api_key)} characters)")

    # Check for old configuration (should be removed)
    old_configs = ["SOURCE_BOARD_ID", "DEST_BOARD_ID", "COLUMN_MAPPING"]
    found_old = []

    for config in old_configs:
        if os.getenv(config):
            found_old.append(config)

    if found_old:
        print_warning(f"Found deprecated config in .env: {', '.join(found_old)}")
        print_info("These are no longer needed and can be removed", 1)
        print_info("All workflow config is now in config/workflows.json", 1)
    else:
        print_success("No deprecated configuration found - .env is clean!")

    return True


def test_config_file():
    """Test config/workflows.json existence"""
    print_header("Testing Workflow Configuration Files")

    # Check template file
    template_path = "config/workflows.template.json"
    if os.path.exists(template_path):
        print_success(f"{template_path} exists (documentation)")
    else:
        print_error(f"{template_path} not found")
        return False

    # Check workflows.json
    config_path = "config/workflows.json"
    if not os.path.exists(config_path):
        print_error(f"{config_path} not found")
        print_info(f"Create it from {template_path}", 1)
        return False

    print_success(f"{config_path} exists")

    return True


def test_config_loading():
    """Test configuration loading and parsing"""
    print_header("Testing Configuration Loading")

    try:
        config_loader = ConfigLoader()
        print_success("Configuration loaded successfully")
        return config_loader
    except FileNotFoundError as e:
        print_error(f"Configuration file not found: {e}")
        return None
    except Exception as e:
        print_error(f"Failed to load configuration: {e}")
        import traceback
        traceback.print_exc()
        return None


def test_templates(config_loader):
    """Test template definitions"""
    print_header("Testing Templates")

    if not config_loader.templates:
        print_warning("No templates defined")
        return True

    print_success(f"Found {len(config_loader.templates)} template(s)")
    print()

    for template_id, template in config_loader.templates.items():
        print_info(f"Template: {BOLD}{template_id}{RESET}")
        print_info(f"Description: {template.description}", 1)
        print_info(f"Column Mappings: {len(template.column_mappings)} columns", 1)

        # Show first few mappings as examples
        for i, mapping in enumerate(template.column_mappings[:3], 1):
            print_info(f"{i}. {mapping.name}: {mapping.source} → {mapping.dest} ({mapping.type})", 2)

        if len(template.column_mappings) > 3:
            print_info(f"... and {len(template.column_mappings) - 3} more", 2)

        print()

    return True


def test_workflows(config_loader):
    """Test workflow definitions"""
    print_header("Testing Workflows")

    if not config_loader.workflows:
        print_error("No workflows defined")
        return False

    print_success(f"Found {len(config_loader.workflows)} workflow(s)")
    print()

    enabled_count = 0
    disabled_count = 0

    for workflow in config_loader.workflows:
        status = f"{GREEN}ENABLED{RESET}" if workflow.enabled else f"{YELLOW}DISABLED{RESET}"
        print_info(f"Workflow: {BOLD}{workflow.id}{RESET} ({status})")
        print_info(f"Name: {workflow.name}", 1)

        # Source
        print_info(f"Source:", 1)
        print_info(f"Board: {workflow.source.board_name} (ID: {workflow.source.board_id})", 2)
        print_info(f"Group: {workflow.source.group_id}", 2)

        # Destinations
        print_info(f"Destinations: {len(workflow.destinations)}", 1)
        for i, dest in enumerate(workflow.destinations, 1):
            print_info(f"{i}. {dest.board_name} (ID: {dest.board_id})", 2)
            print_info(f"Group: {dest.group_id}", 3)
            print_info(f"Template: {dest.template or 'None'}", 3)

            if dest.overrides:
                print_info(f"Overrides: {len(dest.overrides)} column(s)", 3)

            if dest.additional_mappings:
                print_info(f"Additional Mappings: {len(dest.additional_mappings)} column(s)", 3)

        print()

        if workflow.enabled:
            enabled_count += 1
        else:
            disabled_count += 1

    print_success(f"Total: {enabled_count} enabled, {disabled_count} disabled")

    if enabled_count == 0:
        print_warning("No enabled workflows - enable at least one to use the tool")

    return enabled_count > 0


def test_column_resolution(config_loader):
    """Test column mapping resolution"""
    print_header("Testing Column Mapping Resolution")

    enabled_workflows = config_loader.get_enabled_workflows()

    if not enabled_workflows:
        print_warning("No enabled workflows to test")
        return True

    for workflow in enabled_workflows:
        print_info(f"Workflow: {BOLD}{workflow.id}{RESET}")

        for i, destination in enumerate(workflow.destinations, 1):
            print_info(f"Destination {i}: {destination.board_name}", 1)

            # Resolve column mappings
            column_mapping = config_loader.resolve_column_mappings(destination)
            column_names = config_loader.resolve_column_names(destination)

            print_success(f"Resolved {len(column_mapping)} column mapping(s)", 2)

            # Show mappings
            for source_col, dest_col in list(column_mapping.items())[:5]:
                source_name = column_names.get(source_col, source_col)
                dest_name = column_names.get(dest_col, dest_col)
                print_info(f"• {source_name} ({source_col}) → {dest_name} ({dest_col})", 3)

            if len(column_mapping) > 5:
                print_info(f"... and {len(column_mapping) - 5} more", 3)

            print()

    return True


def test_workflow_simulation(config_loader):
    """Simulate running a workflow (no API calls)"""
    print_header("Workflow Simulation (Dry Run)")

    enabled_workflows = config_loader.get_enabled_workflows()

    if not enabled_workflows:
        print_warning("No enabled workflows to simulate")
        return True

    # Use first enabled workflow
    workflow = enabled_workflows[0]

    print_info(f"Simulating workflow: {BOLD}{workflow.name}{RESET}")
    print()

    print_info(f"📥 Source:", 1)
    print_info(f"Board: {workflow.source.board_name} (ID: {workflow.source.board_id})", 2)
    print_info(f"Group: {workflow.source.group_id}", 2)
    print()

    print_info(f"📤 Processing {len(workflow.destinations)} destination(s):", 1)
    print()

    for dest_idx, destination in enumerate(workflow.destinations, 1):
        print_info(f"Destination {dest_idx}: {destination.board_name}", 1)
        print_info(f"Board ID: {destination.board_id}", 2)
        print_info(f"Group ID: {destination.group_id}", 2)
        print_info(f"Template: {destination.template or 'None'}", 2)

        # Resolve mappings
        column_mapping = config_loader.resolve_column_mappings(destination)
        column_names = config_loader.resolve_column_names(destination)

        print_info(f"Column Mappings: {len(column_mapping)} columns", 2)

        # Show what would be mapped
        print_info("Would map:", 2)
        for source_col, dest_col in list(column_mapping.items())[:3]:
            source_name = column_names.get(source_col, source_col)
            dest_name = column_names.get(dest_col, dest_col)
            print_info(f"✓ {source_name} → {dest_name}", 3)

        if len(column_mapping) > 3:
            print_info(f"✓ ... and {len(column_mapping) - 3} more columns", 3)

        print()

    print_success("Simulation complete - no API calls made")

    return True


def main():
    """Run all tests"""
    print(f"\n{BOLD}{'=' * 80}{RESET}")
    print(f"{BOLD}Monday.com Item Duplicator - Configuration Test Suite{RESET}")
    print(f"{BOLD}{'=' * 80}{RESET}")
    print(f"\n{YELLOW}This test validates your configuration without making any API calls{RESET}\n")

    # Track results
    tests = []

    # Test 1: Environment
    tests.append(("Environment Configuration", test_env_file()))

    # Test 2: Config files
    tests.append(("Configuration Files", test_config_file()))

    if not tests[-1][1]:
        print_error("\nCannot proceed without config files")
        sys.exit(1)

    # Test 3: Config loading
    config_loader = test_config_loading()
    tests.append(("Configuration Loading", config_loader is not None))

    if not config_loader:
        print_error("\nCannot proceed without valid configuration")
        sys.exit(1)

    # Test 4: Templates
    tests.append(("Template Definitions", test_templates(config_loader)))

    # Test 5: Workflows
    tests.append(("Workflow Definitions", test_workflows(config_loader)))

    # Test 6: Column resolution
    tests.append(("Column Mapping Resolution", test_column_resolution(config_loader)))

    # Test 7: Simulation
    tests.append(("Workflow Simulation", test_workflow_simulation(config_loader)))

    # Print summary
    print_header("Test Summary")

    passed = sum(1 for _, result in tests if result)
    total = len(tests)

    for test_name, result in tests:
        if result:
            print_success(f"{test_name}")
        else:
            print_error(f"{test_name}")

    print()
    print(f"{BOLD}Results: {passed}/{total} tests passed{RESET}")

    if passed == total:
        print_success("\n🎉 All tests passed! Your configuration is ready to use.")
        print_info("\nTo run the tool:")
        print_info("  python run.py              # Interactive mode", 1)
        print_info("  python run.py --list       # List all workflows", 1)
        print_info("  python run.py --workflow=trulaw --item='Item Name'", 1)
    else:
        print_error("\n❌ Some tests failed. Please fix the issues above.")
        sys.exit(1)


if __name__ == "__main__":
    main()
