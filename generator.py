import os
import re
import json
import yaml
import shutil
import markdown
from jinja2 import Template
from datetime import datetime
from pathlib import Path

CONFIG_FILE = 'config.json'

def load_config():
    with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def load_template(config):
    theme_template = Path('src/themes') / config['theme'] / 'templates' / config['template_file']
    with open(theme_template, 'r', encoding='utf-8') as f:
        return Template(f.read())

def extract_frontmatter_and_content(md_text):
    if md_text.startswith('---'):
        parts = md_text.split('---', 2)
        frontmatter = yaml.safe_load(parts[1])
        content = parts[2].lstrip()
        return frontmatter, content
    return {}, md_text

def generate_minimap(html):
    headers = re.findall(r'<h([2-3])>(.*?)</h[2-3]>', html)
    if not headers:
        return ''
    nav = '<nav class="minimap"><ul>'
    for level, text in headers:
        anchor = re.sub(r'\W+', '-', text.lower()).strip('-')
        html = html.replace(f"<h{level}>{text}</h{level}>", f'<h{level} id="{anchor}">{text}</h{level}>')
        nav += f'<li class="lvl{level}"><a href="#{anchor}">{text}</a></li>'
    nav += '</ul></nav>'
    return nav + html

def generate_sidebar(pages, config):
    sidebar = f"""<aside>
  <header><h1>{config.get('site_title')}</h1></header>
  <nav aria-label="Conteúdo do curso">
    <ul>
      <li><a href="index.html">📚 {get_translated_text('General Index', config)}</a></li>"""
    for page in pages:
        sidebar += f'\n      <li><a href="{page["slug"]}.html">{page["title"]}</a></li>'
    sidebar += "\n    </ul>\n  </nav>\n</aside>"
    return sidebar

def get_translated_text(text, config):
    """
    Retorna a versão traduzida do texto de acordo com a configuração de idioma.
    """
    translations = {
        "General Index": {
            "en-en": "General Index",
            "pt-br": "Índice Geral"
        },
        "Back to index": {
            "en-en": "Back to index",
            "pt-br": "Voltar para o índice"
        },
        "Match the following pairs": {
            "en-en": "Match the following pairs",
            "pt-br": "Associe os pares a seguir"
        },
        "Submit": {
            "en-en": "Submit",
            "pt-br": "Enviar"
        }
    }
    
    language = config.get('language', 'en-en')
    
    if text in translations and language in translations[text]:
        return translations[text][language]
    return text

def process_and_copy_images(content, output_dir):
    """
    Processa imagens no conteúdo Markdown e copia os arquivos de imagem para o diretório de saída.
    
    Args:
        content: O conteúdo Markdown
        output_dir: O diretório de saída onde as imagens serão copiadas
        
    Returns:
        O conteúdo Markdown atualizado com caminhos corretos para as imagens
    """
    # Criar diretório de imagens no destino se não existir
    img_output_dir = Path(output_dir) / "images"
    img_output_dir.mkdir(parents=True, exist_ok=True)
    
    # Procurar por padrões de imagem no Markdown: ![alt](caminho/para/imagem.jpg)
    img_patterns = re.findall(r'!\[(.*?)\]\((.*?)\)', content)
    
    for alt_text, img_path in img_patterns:
        # Verificar se o caminho da imagem é relativo (não é uma URL externa)
        if not img_path.startswith(('http://', 'https://', '/')):
            # Construir caminhos de origem e destino
            src_img_path = Path("content/imgs") / img_path
            if not src_img_path.exists():
                print(f"Aviso: Imagem não encontrada: {src_img_path}")
                continue
                
            # Nome do arquivo da imagem
            img_filename = Path(img_path).name
            
            # Construir caminho de destino
            dst_img_path = img_output_dir / img_filename
            
            # Copiar a imagem para o diretório de saída
            try:
                shutil.copy2(src_img_path, dst_img_path)
                print(f"Imagem copiada: {src_img_path} -> {dst_img_path}")
                
                # Atualizar o caminho da imagem no conteúdo
                content = content.replace(
                    f'![{alt_text}]({img_path})', 
                    f'![{alt_text}](images/{img_filename})'
                )
            except Exception as e:
                print(f"Erro ao copiar imagem {src_img_path}: {str(e)}")
    
    return content

def parse_quiz_blocks(md_text, config):
    quiz_blocks = re.findall(r'```quiz\n(.*?)```', md_text, re.DOTALL)
    for block in quiz_blocks:
        quiz_data = parse_quiz_block(block)
        html_block = render_quiz_html(quiz_data, config)
        md_text = md_text.replace(f'```quiz\n{block}```', html_block)
    return md_text

def parse_quiz_block(block):
    lines = block.strip().split('\n')
    quiz = {}
    state = None
    for line in lines:
        if line.startswith('type:'):
            quiz['type'] = line.replace('type:', '').strip()
        elif line.startswith('question:'):
            quiz['question'] = line.replace('question:', '').strip()
        elif line.startswith('options:'):
            quiz['options'] = []
            state = 'options'
        elif line.startswith('- ') and state == 'options':
            quiz['options'].append(line[2:])
        elif line.startswith('answer:'):
            quiz['answer'] = int(line.replace('answer:', '').strip())
        elif line.startswith('starter_code:'):
            quiz['starter_code'] = ''
            state = 'starter_code'
        elif line.startswith('solution:'):
            quiz['solution'] = ''
            state = 'solution'
        elif line.startswith('explanation:'):
            quiz['explanation'] = line.replace('explanation:', '').strip()
            state = None
        else:
            if state == 'starter_code':
                quiz['starter_code'] += line + '\n'
            elif state == 'solution':
                quiz['solution'] += line + '\n'
    return quiz

def render_quiz_html(quiz, config):
    if quiz['type'] == 'single':
        options_html = ''.join(
            f'<li data-index="{i}" data-correct={"true" if i == quiz["answer"] else "false"}>{opt}</li>'
            for i, opt in enumerate(quiz['options'])
        )
        return f"""<div class='quiz' data-type='single'>
  <p class='question'>{quiz['question']}</p>
  <ul class='options'>{options_html}</ul>
  <p class='explanation' style='display:none;'>{quiz.get('explanation', '')}</p>
</div>"""
    elif quiz['type'] == 'code':
        return f"""<div class='quiz code-quiz'>
  <p class='question'>{quiz['question']}</p>
  <pre><code class='starter'>{quiz['starter_code'].strip()}</code></pre>
  <textarea class='answer-area' placeholder='// seu código aqui'></textarea>
  <button class='check-answer'>{get_translated_text('Submit', config)}</button>
  <pre class='solution' style='display:none;'><code>{quiz['solution'].strip()}</code></pre>
  <p class='explanation' style='display:none;'>{quiz.get('explanation', '')}</p>
</div>"""
    return ''

def copy_theme_assets(config):
    theme = config['theme']
    src_path = Path("src/themes") / theme
    dst_path = Path(config['output_dir']) / "themes" / theme

    if dst_path.exists():
        shutil.rmtree(dst_path)

    shutil.copytree(src_path / "css", dst_path / "css")
    shutil.copytree(src_path / "js", dst_path / "js")

    # Criar diretórios para CSS e JS
    js_out = Path(config['output_dir']) / "js"
    css_out = Path(config['output_dir']) / "css"
    js_out.mkdir(parents=True, exist_ok=True)
    css_out.mkdir(parents=True, exist_ok=True)
    
    # Copiar os arquivos corretamente
    shutil.copyfile("src/js/quiz.js", js_out / "quiz.js")
    # Copiar match.js para match.js, não sobrescrever quiz.js
    shutil.copyfile("src/js/match.js", js_out / "match.js")
    shutil.copyfile("src/css/quiz.css", css_out / "quiz.css")

def parse_pair_blocks(md_text, config):
    import random
    pair_blocks = re.findall(r'```pair\n(.*?)```', md_text, re.DOTALL)
    for block in pair_blocks:
        lines = [line.strip() for line in block.strip().split('\n') if '-' in line]
        pairs = [line.split('-', 1) for line in lines]
        left_items = [f'<li draggable="true" data-id="l{i}">{a.strip()}</li>' for i, (a, b) in enumerate(pairs)]
        right_items = [f'<li draggable="true" data-id="r{i}">{b.strip()}</li>' for i, (a, b) in enumerate(pairs)]
        random.shuffle(right_items)
        html_block = f"""
<div class='quiz pair-quiz'>
  <p>{get_translated_text('Match the following pairs', config)}:</p>
  <div class='pair-columns'>
    <ul class='pair-left'>{"".join(left_items)}</ul>
    <ul class='pair-right'>{"".join(right_items)}</ul>
  </div>
</div>"""
        md_text = md_text.replace(f'```pair\n{block}```', html_block)
    return md_text

def convert_md_to_html(md_path, output_dir, config):
    with open(md_path, 'r', encoding='utf-8') as f:
        raw = f.read()
        metadata, content = extract_frontmatter_and_content(raw)
        
        # Processar e copiar imagens
        content = process_and_copy_images(content, output_dir)
        
        # Processar blocos especiais
        content = parse_quiz_blocks(content, config)
        content = parse_pair_blocks(content, config)
        
        # Converter para HTML
        html = markdown.markdown(content, extensions=['fenced_code', 'tables'])
        html = generate_minimap(html)
        return metadata, html

def save_html(filepath, content):
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

def main():
    config = load_config()
    template = load_template(config)
    output_dir = Path(config['output_dir'])
    content_dir = Path(config['content_dir'])
    os.makedirs(output_dir, exist_ok=True)

    copy_theme_assets(config)

    pages = []

    for md_file in sorted(content_dir.glob("*.md")):
        metadata, html_content = convert_md_to_html(md_file, output_dir, config)
        if metadata.get('draft', False):
            continue
        title = metadata.get('title', md_file.stem)
        slug = metadata.get('slug', md_file.stem)
        date = metadata.get('date', '1900-01-01')
        pages.append({'title': title, 'slug': slug, 'date': date, 'html': html_content})

    pages.sort(key=lambda x: int(x.get("weight", 1000)))
    sidebar = generate_sidebar(pages, config)

    for page in pages:
        html = template.render(content=page['html'], title=page['title'], config=config, sidebar=sidebar)
        save_html(output_dir / f"{page['slug']}.html", html)

    if pages:
        # CORREÇÃO: Não usar <h2> no índice para evitar duplicação com o <h1> do template
        index_title = get_translated_text('General Index', config)
        index_body = "<ul>"
        for page in pages:
            index_body += f"<li><a href='{page['slug']}.html'>{page['title']}</a></li>"
        index_body += "</ul>"
        index_html = template.render(content=index_body, title=index_title, config=config, sidebar=sidebar)
        save_html(output_dir / "index.html", index_html)

if __name__ == "__main__":
    main()
