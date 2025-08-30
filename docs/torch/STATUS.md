# TORCH — STATUS (update this before handing off)

As of: <fill-date-here>

## Repo / CI
- main: green ("1 passed")
- Auto-Fix + Notify: on main and working
- Secrets/vars: OPENAI_API_KEY=present; OPENAI_MODEL=gpt-4o-mini; AUTODEV_MAX_ITERS=2

## Active Branches
- autodev/T1.1-reg-graph-schema: ORM skeleton ticket
  - Goal: DB schema + ORM models for: Device, Indication, ProductCode, Regulation, SpecialControl, RecognizedStandard, TestMethod, Artifact, eSTARField, Route, Milestone.
  - Acceptance: migrations run; CRUD + core relations pass tests.

## Next Actions for the Assistant
1) Make tests red → green via ORM skeleton (core/db.py, core/orm.py) on autodev/T1.1-reg-graph-schema.  
2) Add richer T1.1 tests: CRUD + relationships (Device↔ProductCode↔Regulation, Device↔Indications), then implement to green.

## Reference Links (FDA, official)
- eSTAR overview: https://www.fda.gov/medical-devices/how-study-and-market-your-device/electronic-submissions-medical-devices
- Product Classification: https://www.accessdata.fda.gov/scripts/cdrh/cfpcd/classification.cfm
- Recognized Standards: https://www.fda.gov/medical-devices/standards-and-conformity-assessment-program/recognized-consensus-standards
- openFDA 510(k): https://open.fda.gov/apis/device/510k/
