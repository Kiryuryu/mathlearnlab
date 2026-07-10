#!/usr/bin/env python3
"""
Convert Jupyter notebooks to markdown files for the static site.

Extracts markdown cells and code cells, producing readable .md files.
Run once and commit the output to site/content/notebooks/.
"""

import json
import os
import sys


def extract_notebook_to_markdown(nb_path, output_path):
    """Extract content from a .ipynb file and write as .md.

    - Markdown cells: output directly
    - Code cells: wrap in fenced Python code blocks
    - Add a note at the top about interactive execution
    """
    with open(nb_path, 'r', encoding='utf-8') as f:
        nb = json.load(f)

    cells = nb.get('cells', [])
    sections = []
    has_code = False

    # Get notebook title from first heading
    notebook_title = None

    for cell in cells:
        cell_type = cell.get('cell_type', '')
        source = ''.join(cell.get('source', []))

        if cell_type == 'markdown':
            if notebook_title is None and source.strip().startswith('# '):
                notebook_title = source.strip()
            sections.append(source)

        elif cell_type == 'code':
            has_code = True
            source_clean = source.rstrip()
            if source_clean:
                code_block = f"```python\n{source_clean}\n```\n"
                # Add output note if there are outputs
                outputs = cell.get('outputs', [])
                if outputs:
                    has_image = any(
                        o.get('output_type') == 'display_data' and 'image/png' in o.get('data', {})
                        for o in outputs
                    )
                    if has_image:
                        code_block += "\n> 📊 此代码会生成交互式图表。运行 `jupyter lab` 查看完整交互版本。\n"
                    else:
                        # Check for text output
                        text_outputs = [
                            o for o in outputs
                            if o.get('output_type') == 'execute_result' or o.get('output_type') == 'stream'
                        ]
                        if text_outputs:
                            for to in text_outputs[:2]:
                                text = ''.join(to.get('data', {}).get('text/plain', [])) if to.get('output_type') == 'execute_result' else ''.join(to.get('text', []))
                                if text.strip():
                                    code_block += f"\n输出:\n```\n{text.strip()[:300]}\n```\n"

                sections.append(code_block)

    # Build output with header note
    header = ""
    if notebook_title:
        header += notebook_title + "\n\n"

    header += "> 💡 **提示**：本页面由 Jupyter Notebook 自动转换而来。\n"
    header += "> 运行 `jupyter lab` 启动本地环境，可体验完整的**交互式可视化**（拖动滑块、3D旋转、动画播放）。\n"
    if has_code:
        header += "> 下方代码块仅供参考，静态页面无法执行 Python。\n"
    header += "\n---\n\n"

    content = header + '\n\n'.join(sections)

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"✅ {os.path.basename(nb_path)} → {output_path}")


def main():
    repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    notebooks_dir = os.path.join(repo_root, 'notebooks', '01-gaoshu')
    output_dir = os.path.join(repo_root, 'site', 'content', 'notebooks', '01-gaoshu')

    files = sorted(os.listdir(notebooks_dir))
    for fname in files:
        if fname.endswith('.ipynb'):
            nb_path = os.path.join(notebooks_dir, fname)
            # Remove number prefix for cleaner names
            base = fname.replace('.ipynb', '.md')
            output_path = os.path.join(output_dir, base)
            extract_notebook_to_markdown(nb_path, output_path)

    print(f"\n🎉 Done! {len([f for f in files if f.endswith('.ipynb')])} notebooks converted.")


if __name__ == '__main__':
    main()
