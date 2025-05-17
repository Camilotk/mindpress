# Mindpress

This is a lightweight static site generator designed for educators to create interactive lessons using Markdown. The generated pages are styled in a clean, with support to themes and support rich interactivity like quizzes and matching exercises.

---

## Features

- Write lessons in Markdown with YAML metadata
- Interactive **multiple choice quizzes**
- **Matching pairs** exercises click
- Clean, semantic HTML output
- Customizable themes (`simplepage`, `darkbook`, or your own)
- Supports table rendering, code blocks, and headers
- Auto-generated index in lessons
- Configurable via `config.json`
- Python-based, no internet required

---

## Project Structure

```bash
.
├── content/
│   └── classes/         # Your Markdown lesson files
├── src/
│   ├── css/             # Global styles (e.g., quiz.css)
│   ├── js/              # Global scripts (e.g., quiz.js)
│   ├── templates/       # HTML templates (if not using a theme)
│   └── themes/
│       └── darkbook/    # Theme folders (CSS, JS, template.html)
├── public/              # Auto-generated static website
├── config.json          # Site configuration
├── generator.py         # Static site generator
├── new.py               # Tool to scaffold new lesson
└── run.py               # Local web server for preview
```

---

## How to Use

1. **Write Markdown lesson**
   - Place in `content/classes/`
   - Start with YAML frontmatter:
     ```yaml
     ---
     title: Sample Lesson
     slug: sample
     date: 2025-06-01
     weight: 1
     draft: false
     ---
     ```

2. **Use Quiz Syntax**:
   - Multiple choice:
     ````markdown
     ```quiz
     type: single
     question: What is 2 + 2?
     options:
     - 3
     - 4
     - 5
     answer: 1
     explanation: 2 + 2 = 4
     ```
     ````
   - Matching:
     ````markdown
     ```pair
     [Loop]-[for]
     [Condition]-[if]
     ```
     ````

3. **Generate Site**
   ```bash
   python generator.py
   ```

4. **Preview Site**
   ```bash
   python run.py
   ```

---

## Configuration (config.json)

```json
{
  "site_title": "My Course",
  "content_dir": "content/classes",
  "output_dir": "public",
  "theme": "rustbook",
  "template_file": "template.html",
  "lang": "pt-br"
}
```

---

## 🧪 Dependencies

```
markdown
pyyaml
jinja2
```

Install with:

```bash
pip install -r requirements.txt
```

---

## Contributing Themes

Create a folder in `src/themes/your_theme` with:

- `css/theme.css`
- `js/theme.js`
- `templates/template.html`

---

## License

GPL-3. Free as in freedom.

---

> “It is not because things are difficult that we do not dare; it is because we do not dare that they are difficult.” — *Seneca*
