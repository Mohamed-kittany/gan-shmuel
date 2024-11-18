
# /billing/app/tests/__init__.py
import pytest
from app import create_app
import argparse


## to run a specific pytest use the following command: "pytest path_to_testFile::func_name"

@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


