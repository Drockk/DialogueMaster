import pytest
from main import send_prompt

def test_basic_prompt():
    prompt = "notification: The sun went down and it became dark"
    reply = send_prompt(prompt)
    assert "OK" in reply
