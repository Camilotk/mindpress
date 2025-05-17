import os
import json
from datetime import date

CONFIG_FILE = "config.json"
CONTENT_DIR = "content/classes"

def load_config():
    if not os.path.exists(CONFIG_FILE):
        return {}
    with open(CONFIG_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_config(config):
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=2, ensure_ascii=False)

def ask(question, default=""):
    prompt = f"{question} [{'Enter' if default else ''}]: "
    value = input(prompt).strip()
    return value or default

def create_new_lesson():
    config = load_config()
    next_weight = config.get("contents", 0) + 1

    print("=== New Lesson ===")
    title = ask("Lesson title")
    slug = ask("Slug (file name, no .md)")
    date_str = ask("Date (YYYY-MM-DD)", date.today().isoformat())
    draft = ask("Is this a draft? (y/n)", "n").lower() in ("y", "yes")

    metadata = {
        "title": title,
        "slug": slug,
        "date": date_str,
        "weight": next_weight,
        "draft": draft
    }

    os.makedirs(CONTENT_DIR, exist_ok=True)
    filepath = os.path.join(CONTENT_DIR, f"{slug}.md")

    with open(filepath, "w", encoding="utf-8") as f:
        f.write("---\n")
        for key, value in metadata.items():
            f.write(f"{key}: {str(value).lower() if isinstance(value, bool) else value}\n")
        f.write("---\n\n")
        f.write(f"# {title}\n\nWrite your content here...\n")

    config["contents"] = next_weight
    save_config(config)

    print(f"Lesson created successfully at {filepath}")

if __name__ == "__main__":
    create_new_lesson()