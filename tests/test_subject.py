import pytest

from subject import add


@pytest.fixture
def mock_adder(mocker):
    mocker.patch("subject.real_adder", autospec=True, return_value=42)


def test_adder(mock_adder):
    assert add(1, 1) == 42
