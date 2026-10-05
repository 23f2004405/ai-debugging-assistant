from pathlib import Path

CODE_ROOT = Path("sample_project")
ALLOWED = {".py", ".md", ".txt"}

def search_codebase(query: str, max_hits: int = 8) -> list[str]:
    terms = [x.lower() for x in query.split() if len(x) > 2]
    hits = []

    for path in CODE_ROOT.rglob("*"):
        if not path.is_file() or path.suffix not in ALLOWED:
            continue
        try:
            lines = path.read_text(encoding="utf-8").splitlines()
        except UnicodeDecodeError:
            continue

        for i, line in enumerate(lines, 1):
            score = sum(term in line.lower() for term in terms)
            if score:
                start, end = max(0, i - 2), min(len(lines), i + 2)
                snippet = "\n".join(
                    f"{j+1}: {lines[j]}" for j in range(start, end)
                )
                hits.append((score, f"{path}:{i}\n{snippet}"))

    hits.sort(key=lambda x: x[0], reverse=True)
    return [item for _, item in hits[:max_hits]]
