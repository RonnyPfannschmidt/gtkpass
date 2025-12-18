"""Test configuration and fixtures."""

import pytest


@pytest.fixture
def sample_data():
    """Provide sample test data."""
    return {"test": "data"}
