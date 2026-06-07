.PHONY: test

test:
	python scripts/run_pytest.py


.PHONY: streamlit-e2e-smoke
streamlit-e2e-smoke:
	python scripts/run_streamlit_e2e_smoke.py


.PHONY: reproduce-public-release
reproduce-public-release:
	python scripts/check_public_only_boundary.py
	python scripts/build_public_source_snapshot.py
	python scripts/check_public_source_snapshot.py
	python scripts/check_public_source_retrieval_plan.py
	python scripts/check_public_source_transform_scripts.py
	python scripts/check_transformed_schemas.py
	python scripts/check_parameter_traceability.py
	python scripts/run_public_aggregate_calibration.py --check-only
	python scripts/run_voi.py --check-only
	python scripts/render_public_model_report.py
	python scripts/run_visual_regression.py --check-only
	python scripts/run_accessibility_audit.py --check-only
	python scripts/run_streamlit_e2e_smoke.py
	python scripts/generate_release_model_card.py --check-only
	python scripts/generate_release_manifest.py --check-only


.PHONY: check-conductor-parallel
check-conductor-parallel:
	python scripts/check_conductor_parallel_tracks.py
