from unittest.mock import patch, MagicMock
from sixid import SixID


def test_import():
    """SixID class is importable from the top-level package."""
    assert SixID is not None


def test_constructor():
    """SixID can be instantiated with required arguments."""
    client = SixID(
        api_url="http://localhost:3000",
        private_key_hex=None,
        agent_id="agent:test_01",
    )
    assert client.api_url == "http://localhost:3000"
    assert client.agent_id == "agent:test_01"


@patch("sixid.client.requests")
def test_certify_network_error(mock_requests):
    """certify_machinehood returns ERROR on network failure."""
    mock_requests.post.side_effect = ConnectionError("refused")
    client = SixID(
        api_url="http://localhost:3000",
        private_key_hex=None,
        agent_id="agent:test_01",
    )
    result = client.certify_machinehood()
    assert result["status"] == "ERROR"
