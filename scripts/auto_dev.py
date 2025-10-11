import argparse, os, subprocess, json, re, sys
from pathlib import Path
from typing import Dict, List

DEFAULT_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
MAX_FILE_BYTES = int(os.getenv("AUTODEV_MAX_FILE_BYTES", "4000"))
WHITELIST = [
    "core/",
    "profiles/",
    "templates/",
    "exporters/",
    "planner/",
    "scripts/",
    "tests/",
    "README.md",
    "AGENT_GUIDE.md",
    "BRANCHING.md",
    "requirements.txt",
]

def sh(cmd: List[str], check: bool=False):
    print("+", " ".join(cmd))
    cp = subprocess.run(cmd, text=True, capture_output=True)
    if check and cp.returncode != 0:
        sys.stderr.write((cp.stdout or "") + (cp.stderr or ""))
        raise SystemExit(cp.returncode)
    return cp

def run_tests():
    if Path("requirements.txt").exists():
        sh(["pip", "install", "-r", "requirements.txt"])
    r = sh(["pytest", "-q"])
    return {"rc": str(r.returncode), "stdout": r.stdout or "", "stderr": r.stderr or ""}

def summarize_pytest(stdout: str):
    blocks = []
    lines = stdout.splitlines()
    capture = False
    for ln in lines:
        if ln.startswith("====") and "short test summary info" in ln:
            capture = True
            continue
        if capture and ln.startswith("===="):
            break
        if capture:
            blocks.append(ln)
    if blocks:
        return "\n".join(blocks[:80])
    return "\n".join(lines[-80:])

def read_lite(path: str):
    p = Path(path)
    if not p.exists() or p.is_dir():
        return ""
    data = p.read_bytes()[:MAX_FILE_BYTES]
    return data.decode("utf-8", errors="replace")

def collect_context():
    key_files = [
        "core/models.py",
        "profiles/ormi.yaml",
        "requirements.txt",
        "tests/test_core_contracts.py",
        "AGENT_GUIDE.md",
        "README.md",
    ]
    ctx = {}
    for f in key_files:
        s = read_lite(f)
        if s:
            ctx[f] = s
    return ctx

def inside_whitelist(path: str) -> bool:
    return any(path == w or path.startswith(w) for w in WHITELIST)

def apply_edits(edits: List[Dict[str,str]]):
    touched = []
    for e in edits:
        path = e.get("path","").strip()
        if not path:
            continue
        if not inside_whitelist(path):
            print(f"! skip non-whitelisted path: {path}")
            continue
        content = e.get("content","")
        p = Path(path)
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(content)
        touched.append(path)
    return touched

def extract_json_block(text: str):
    m = re.search(r"```json\s*(\{[\s\S]*?\})\s*```", text)
    if m:
        return json.loads(m.group(1))
    m = re.search(r"(\{[\s\S]*\})", text)
    if m:
        return json.loads(m.group(1))
    raise ValueError("No JSON object found in model output")

def build_messages(goal: str, failure_summary: str, context: Dict[str,str]):
    system = (
        "You are an expert repo editor. Return STRICT JSON only in this format:\n"
        "{\n"
        '  "edits":[{"path":"...","content":"FULL FILE CONTENT"}]\n'
        "}\n"
        "Rules:\n"
        "- Make the minimal edits needed to fix tests and advance the GOAL.\n"
        "- Do NOT invent files or APIs; prefer editing existing files.\n"
        "- Tests must pass with `pytest -q`.\n"
        "- Keep dependencies minimal; stdlib first.\n"
        "- If you change `core/models.py`, also update tests.\n"
        "- Do not touch .github/workflows.\n"
    )
    user = {
        "goal": goal,
        "failure_summary": failure_summary,
        "context_files": list(context.keys()),
        "context": context,
    }
    return [
        {"role":"system","content": system},
        {"role":"user","content": json.dumps(user)},
    ]

def ensure_openai():
    try:
        from openai import OpenAI
        return OpenAI()
    except Exception:
        print("OpenAI SDK missing; run: pip install openai", file=sys.stderr)
        sys.exit(2)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--goal", required=True)
    ap.add_argument("--iters", type=int, default=int(os.getenv("AUTODEV_MAX_ITERS","2")))
    ap.add_argument("--model", default=DEFAULT_MODEL)
    args = ap.parse_args()

    if not os.getenv("OPENAI_API_KEY"):
        print("OPENAI_API_KEY not set; exiting early.")
        sys.exit(0)

    client = ensure_openai()
    context = collect_context()

    for i in range(1, args.iters+1):
        print(f"=== iteration {i}/{args.iters} ===")
        res = run_tests()
        if res["rc"] == "0":
            print("Tests already green. Done.")
            return
        failure_summary = summarize_pytest((res["stdout"] or "") + "\n" + (res["stderr"] or ""))
        messages = build_messages(args.goal, failure_summary, context)
        resp = client.chat.completions.create(
            model=args.model,
            temperature=0.2,
            messages=messages,
        )
        out = (resp.choices[0].message.content or "").strip()
        try:
            plan = extract_json_block(out)
        except Exception:
            print("Model output not JSON; abort. Raw:", out[:800])
            break

        edits = plan.get("edits", [])
        if not edits:
            print("No edits proposed; stopping.")
            break

        touched = apply_edits(edits)
        print("touched:", touched)

        context = collect_context()

    res = run_tests()
    sys.exit(int(res["rc"]))

if __name__ == "__main__":
    main()
