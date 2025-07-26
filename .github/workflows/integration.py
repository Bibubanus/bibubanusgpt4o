"""Integration hooks for external data sources.

This module provides placeholders for integrating data from external APIs,
including GitHub, scientific databases, search engines and proprietary
connectors.  Due to the execution environment, these functions are not
implemented here but serve as stubs for future expansion.

To implement a new integration, create a subclass of `DataSource` and
override the `fetch` method.  Then register the source in the `sources`
dictionary in `get_available_sources()`.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Any, List


@dataclass
class DataSource:
    name: str
    description: str

    def fetch(self, query: str) -> List[Dict[str, Any]]:
        """Fetch results for a given query from this data source.

        This method must be implemented by subclasses.  It should return a list
        of dicts, each containing the extracted data and metadata.  Raise
        NotImplementedError to signal that the integration is not yet
        available.
        """
        raise NotImplementedError


def get_available_sources() -> Dict[str, DataSource]:
    """Return a registry of available data sources."""
    # Example: return {} until integrations are implemented.
    return {}