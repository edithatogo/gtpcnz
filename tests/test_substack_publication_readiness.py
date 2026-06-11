from __future__ import annotations

from scripts.check_substack_publication_readiness import LiveDraft, load_rows, score_row


def test_post_07_publication_readiness_scores_near_maximum() -> None:
    [row] = load_rows({"07"})
    score = score_row(row)

    assert score.series >= 45, score.failures
    assert score.substack >= 45, score.failures
    assert score.images >= 9, score.failures


def test_post_10_publication_readiness_scores_near_maximum() -> None:
    [row] = load_rows({"10"})
    score = score_row(row)

    assert score.series >= 45, score.failures
    assert score.substack >= 45, score.failures
    assert score.images >= 9, score.failures


def test_live_score_reaches_full_points_for_current_cached_post() -> None:
    [row] = load_rows({"07"})
    live_draft = LiveDraft(
        title=str(row["title"]),
        text=(
            "When a hospital is full, everyone can see the problem. "
            "public_aggregate_validated empirically_supported_if_gated"
        ),
        image_count=1,
    )
    score = score_row(row, live_draft=live_draft)

    assert score.live == 30, score.failures
