"""
Configuration Loader for Monday.com Item Duplicator
Loads and validates workflow configurations from JSON files
"""

import json
import os
from typing import Dict, List, Optional
from dataclasses import dataclass


@dataclass
class ColumnMapping:
    """Represents a column mapping from source to destination"""
    source: str
    dest: str
    name: str
    type: str = "text"


@dataclass
class Destination:
    """Represents a destination board configuration"""
    board_id: int
    group_id: str
    board_name: str
    template: Optional[str] = None
    overrides: Dict[str, str] = None
    additional_mappings: List[Dict] = None

    def __post_init__(self):
        if self.overrides is None:
            self.overrides = {}
        if self.additional_mappings is None:
            self.additional_mappings = []


@dataclass
class Source:
    """Represents a source board configuration"""
    board_id: int
    group_id: str
    board_name: str = "Source Board"


@dataclass
class Workflow:
    """Represents a complete workflow configuration"""
    id: str
    name: str
    enabled: bool
    source: Source
    destinations: List[Destination]


@dataclass
class Template:
    """Represents a reusable column mapping template"""
    description: str
    column_mappings: List[ColumnMapping]


class ConfigLoader:
    """Loads and validates workflow configurations"""

    def __init__(self, config_path: str = "config/workflows.json"):
        """
        Initialize config loader

        Args:
            config_path: Path to workflows.json file
        """
        self.config_path = config_path
        self.templates: Dict[str, Template] = {}
        self.workflows: List[Workflow] = []

        if os.path.exists(config_path):
            self.load()
        else:
            raise FileNotFoundError(
                f"Configuration file not found: {config_path}\n"
                f"Please create it from config/workflows.template.json"
            )

    def load(self):
        """Load and parse the configuration file"""
        with open(self.config_path, 'r') as f:
            data = json.load(f)

        # Load templates
        templates_data = data.get("templates", {})
        for template_id, template_data in templates_data.items():
            mappings = []
            for mapping in template_data.get("column_mappings", []):
                mappings.append(ColumnMapping(
                    source=mapping["source"],
                    dest=mapping["dest"],
                    name=mapping["name"],
                    type=mapping.get("type", "text")
                ))

            self.templates[template_id] = Template(
                description=template_data.get("description", ""),
                column_mappings=mappings
            )

        # Load workflows
        workflows_data = data.get("workflows", [])
        for workflow_data in workflows_data:
            # Parse source
            source_data = workflow_data["source"]
            source = Source(
                board_id=source_data["board_id"],
                group_id=source_data["group_id"],
                board_name=source_data.get("board_name", "Source Board")
            )

            # Parse destinations
            destinations = []
            for dest_data in workflow_data["destinations"]:
                destinations.append(Destination(
                    board_id=dest_data["board_id"],
                    group_id=dest_data["group_id"],
                    board_name=dest_data.get("board_name", "Destination Board"),
                    template=dest_data.get("template"),
                    overrides=dest_data.get("overrides", {}),
                    additional_mappings=dest_data.get("additional_mappings", [])
                ))

            # Create workflow
            workflow = Workflow(
                id=workflow_data["id"],
                name=workflow_data["name"],
                enabled=workflow_data.get("enabled", True),
                source=source,
                destinations=destinations
            )

            self.workflows.append(workflow)

    def get_workflow(self, workflow_id: str) -> Optional[Workflow]:
        """
        Get a workflow by ID

        Args:
            workflow_id: The workflow ID

        Returns:
            Workflow object or None if not found
        """
        for workflow in self.workflows:
            if workflow.id == workflow_id:
                return workflow
        return None

    def get_enabled_workflows(self) -> List[Workflow]:
        """Get all enabled workflows"""
        return [w for w in self.workflows if w.enabled]

    def resolve_column_mappings(self, destination: Destination) -> Dict[str, str]:
        """
        Resolve column mappings for a destination, applying template and overrides

        Args:
            destination: Destination configuration

        Returns:
            Dictionary mapping source column IDs to destination column IDs
        """
        column_mapping = {}

        # Start with template if specified
        if destination.template and destination.template in self.templates:
            template = self.templates[destination.template]
            for mapping in template.column_mappings:
                column_mapping[mapping.source] = mapping.dest

        # Apply overrides
        if destination.overrides:
            for source_col, dest_col in destination.overrides.items():
                column_mapping[source_col] = dest_col

        # Add additional mappings
        if destination.additional_mappings:
            for mapping in destination.additional_mappings:
                column_mapping[mapping["source"]] = mapping["dest"]

        return column_mapping

    def resolve_column_names(self, destination: Destination) -> Dict[str, str]:
        """
        Resolve column display names for a destination

        Args:
            destination: Destination configuration

        Returns:
            Dictionary mapping column IDs to display names
        """
        column_names = {}

        # Get names from template
        if destination.template and destination.template in self.templates:
            template = self.templates[destination.template]
            for mapping in template.column_mappings:
                # Add both source and destination names
                column_names[mapping.source] = mapping.name
                column_names[mapping.dest] = mapping.name

        # Add names from additional mappings
        if destination.additional_mappings:
            for mapping in destination.additional_mappings:
                name = mapping.get("name", mapping["source"])
                column_names[mapping["source"]] = name
                column_names[mapping["dest"]] = name

        return column_names

    def list_workflows(self) -> List[Dict]:
        """
        List all workflows with basic info

        Returns:
            List of workflow info dictionaries
        """
        return [
            {
                "id": w.id,
                "name": w.name,
                "enabled": w.enabled,
                "source_board": w.source.board_name,
                "destinations": [d.board_name for d in w.destinations]
            }
            for w in self.workflows
        ]
