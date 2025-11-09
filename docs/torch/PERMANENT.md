# TORCH — PERMANENT (stable ground rules)

## Project
Name: 510k-navigator  
Mission: Build an app that walks teams through the 510(k) process end-to-end, generating each document in logical order from user inputs, explaining each input and its consequences, and answering questions on the fly. Backend uses GPT-5 via API; RAG strictly from official FDA sources.

## Working Agreement (Assistant)
- ≤2 steps per round; each step includes: (1) what & why, (2) exact commands/code, (3) how to verify.
- Don’t guess; state assumptions + a one-line check.
- Use Bash over UI; autodev/<topic> branches only.
- Keep me out until CI is green; notify on green only.
- When editing workflows, paste full files.

## CI Loop (installed, do not change unless asked)
- Auto-Fix runs on workflow_run of "CI Manual" (and "CI" if present), only when:
  - head_branch startsWith autodev/ AND conclusion == failure
  - pushes fixes back to the same branch
- Notify-on-Green marks PR ready and assigns @bjwiley8 when CI turns green.

## Ben’s Preferences (stable)
- Explicit, linear, verifiable; quantitative where applicable.
- Cite scientific data from literature; flag quantitative vs qualitative vs speculative.
- Provide full-file overwrites for workflows.
- USA market focus; no moral lectures; concise & technical tone.
