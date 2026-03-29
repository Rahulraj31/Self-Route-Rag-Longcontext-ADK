import os

def load_docs(folder_path: str) -> str:
    if not os.path.exists(folder_path):
        return "No docs folder found."

    parts = []
    for fname in os.listdir(folder_path):
        fpath = os.path.join(folder_path, fname)

        if os.path.isdir(fpath):
            continue

        if fname.lower().endswith(".txt"):
            with open(fpath, "r", encoding="utf-8") as f:
                parts.append(f"\n\n===== FILE: {fname} =====\n")
                parts.append(f.read())

    return "\n".join(parts) if parts else "No documents found."
