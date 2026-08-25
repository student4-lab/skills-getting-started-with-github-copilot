from copy import deepcopy

import pytest
from fastapi.testclient import TestClient

from src.app import activities, app


@pytest.fixture(scope="session")
def seed_activities():
    return deepcopy(activities)


@pytest.fixture(autouse=True)
def reset_activities(seed_activities):
    activities.clear()
    activities.update(deepcopy(seed_activities))


@pytest.fixture
def client():
    return TestClient(app)
