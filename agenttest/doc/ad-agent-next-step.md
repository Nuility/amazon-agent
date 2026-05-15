## Ad Agent Starter Upgrade

This repository now includes a first-step ad analysis slice in addition to the original user-management demo.

### What was added

- `src/common/ad_types.py`
  - Ad report records
  - Summary metrics
  - Optimization recommendation objects

- `src/repositories/ad_report_repository.py`
  - Reads and writes ad report records through the existing storage adapter

- `src/services/ad_agent_service.py`
  - Seeds a small starter dataset
  - Calculates summary metrics such as CTR, CVR, ACOS, and ROAS
  - Produces simple optimization recommendations

- `src/api/server.py`
  - `GET /api/ad-insights/summary`
  - `GET /api/ad-insights/campaigns`
  - `GET /api/ad-insights/recommendations`

### Why this helps

This keeps the project in a safe starter phase while shifting the codebase toward the actual target:

- ad analysis agent
- automatic optimization agent
- recommendation workflows
- future prompt-driven reasoning

### Suggested next step

Replace the seeded records with imported Amazon ad report data and add one workflow:

1. ingest report
2. compute metrics
3. detect weak campaigns
4. generate recommended actions
5. require human approval before execution
