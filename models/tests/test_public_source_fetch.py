from __future__ import annotations

import subprocess
import sys
from io import BytesIO

import pytest

from models.primarycare_model.data import public_source_fetch
from models.primarycare_model.data.public_source_fetch import (
    PublicSourceFetchError,
    check_source_fetch_readiness,
    download_public_source,
    expected_raw_artifact_path,
    verify_public_source_fetch_scripts,
)
from models.primarycare_model.data.public_source_retrieval import load_public_source_retrieval_plans


def test_public_source_fetch_scripts_exist_for_every_plan() -> None:
    assert verify_public_source_fetch_scripts() == ()


def test_public_source_fetch_check_is_readiness_compatible() -> None:
    for plan in load_public_source_retrieval_plans():
        result = check_source_fetch_readiness(plan.source_id)
        assert result.ok
        assert result.target_url == (plan.download_url or plan.landing_page_url)
        assert result.status in {"reference_pinned_pending_download", "raw_available_pending_checksum_verification"}


def test_public_source_fetch_strict_mode_reports_missing_raw_files() -> None:
    results = [check_source_fetch_readiness(plan.source_id, require_raw=True) for plan in load_public_source_retrieval_plans()]
    missing_raw_issues = [
        issue
        for result in results
        for issue in result.issues
        if "no raw public source files" in issue or "expected raw artifact missing" in issue
    ]
    if missing_raw_issues:
        assert any("no raw public source files" in issue for issue in missing_raw_issues)
        assert any("expected raw artifact missing" in issue for issue in missing_raw_issues)
    else:
        assert all(result.status == "raw_available_pending_checksum_verification" for result in results)


def test_expected_raw_artifact_paths_are_under_public_raw() -> None:
    for plan in load_public_source_retrieval_plans():
        path = expected_raw_artifact_path(plan.source_id)
        assert f"data/public_raw/{plan.source_id}/" in path.as_posix()
        assert path.name == plan.expected_raw_artifact


def test_public_source_fetch_script_cli_passes_in_readiness_mode() -> None:
    result = subprocess.run(
        [sys.executable, "scripts/check_public_source_fetch_scripts.py"],
        text=True,
        capture_output=True,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert "public source fetch script contract passed" in result.stdout


def test_source_specific_fetch_entrypoint_is_checkable() -> None:
    result = subprocess.run(
        [sys.executable, "scripts/fetch_statsnz_population.py", "--check-only"],
        text=True,
        capture_output=True,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert "src_statsnz_population fetch readiness" in result.stdout


def test_download_response_reader_rejects_empty_payloads() -> None:
    with pytest.raises(PublicSourceFetchError, match="empty response"):
        public_source_fetch._read_bounded_response(BytesIO(b""))


def test_download_response_reader_rejects_oversized_payloads() -> None:
    with pytest.raises(PublicSourceFetchError, match="safety limit"):
        public_source_fetch._read_bounded_response(BytesIO(b"abcd"), limit_bytes=3)


def test_download_public_source_rejects_empty_responses(monkeypatch: pytest.MonkeyPatch) -> None:
    class EmptyResponse:
        def __enter__(self) -> EmptyResponse:
            return self

        def __exit__(self, *_args: object) -> None:
            return None

        def read(self, _size: int = -1) -> bytes:
            return b""

    monkeypatch.setattr(public_source_fetch.urllib.request, "urlopen", lambda *_args, **_kwargs: EmptyResponse())
    with pytest.raises(PublicSourceFetchError, match="empty response"):
        download_public_source("src_statsnz_population")
