import os
import subprocess
import sys
from unittest.mock import MagicMock, patch

# Add the root directory to sys.path so we can import scripts
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from scripts.check_dash_browser_smoke import main


def test_dash_browser_smoke_timeout_error():
    """
    Tests that when the server process times out during the wait() call,
    the TimeoutExpired exception is caught, process.kill() is called, and then process.wait() is called.
    """
    with (
        patch("scripts.check_dash_browser_smoke._free_port", return_value=12345),
        patch("scripts.check_dash_browser_smoke._start_server") as mock_start_server,
        patch("scripts.check_dash_browser_smoke._wait_for_server"),
        patch("scripts.check_dash_browser_smoke.run_browser_smoke", return_value=[]),
    ):
        # Create a mock process
        mock_process = MagicMock(spec=subprocess.Popen)
        mock_start_server.return_value = mock_process

        # Make the first call to wait() raise a TimeoutExpired exception
        mock_process.wait.side_effect = [subprocess.TimeoutExpired(cmd=["fake_cmd"], timeout=5), None]

        main([])

        # The mock process should be terminated first
        mock_process.terminate.assert_called_once()

        # After terminate, it should have called kill() due to TimeoutExpired
        mock_process.kill.assert_called_once()

        # We also check that wait() was called again after kill()
        assert mock_process.wait.call_count == 2
