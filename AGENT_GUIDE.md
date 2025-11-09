# Agent guardrails
- Do not change `core/models.py` without updating `tests/test_core_contracts.py`.
- Only import across modules via `core.models`.
- Add tests for every new function; CI must pass.
- eSTAR structure lives in `estar/sections.map.yaml`; exporters read only from that map.
- Constants/URLs go in `connectors/config.py`.
