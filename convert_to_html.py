import re

def convert_md_to_html(md_file, html_file):
    with open(md_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    html = """
    <html>
    <head>
        <style>
            body { font-family: Arial, sans-serif; line-height: 1.6; max-width: 800px; margin: 0 auto; padding: 20px; }
            h1 { color: #2c3e50; border-bottom: 2px solid #eee; }
            h2 { color: #34495e; margin-top: 30px; }
            h3 { color: #7f8c8d; }
            table { border-collapse: collapse; width: 100%; margin: 20px 0; }
            th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
            th { background-color: #f2f2f2; }
            code { background-color: #f8f9fa; padding: 2px 5px; border-radius: 3px; font-family: Consolas, monospace; }
            pre { background-color: #f8f9fa; padding: 15px; border-radius: 5px; overflow-x: auto; }
            ul { margin-bottom: 20px; }
            li { margin-bottom: 5px; }
        </style>
    </head>
    <body>
    """

    in_table = False
    in_code_block = False

    for line in lines:
        line = line.rstrip()
        
        # Code Blocks
        if line.startswith('```'):
            if in_code_block:
                html += "</pre>\n"
                in_code_block = False
            else:
                html += "<pre>\n"
                in_code_block = True
            continue
        
        if in_code_block:
            html += line + "\n"
            continue

        # Headers
        if line.startswith('# '):
            html += f"<h1>{line[2:]}</h1>\n"
            continue
        elif line.startswith('## '):
            html += f"<h2>{line[3:]}</h2>\n"
            continue
        elif line.startswith('### '):
            html += f"<h3>{line[4:]}</h3>\n"
            continue

        # Horizontal Rule
        if line.startswith('---'):
            html += "<hr>\n"
            continue

        # Lists
        if line.strip().startswith('* '):
            content = line.strip()[2:]
            # Bold
            content = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', content)
            html += f"<ul><li>{content}</li></ul>\n" # Simplification: separate uls, browser handles it ok-ish or I could fix logic
            continue

        # Tables
        if '|' in line:
            if not in_table:
                html += "<table>\n"
                in_table = True
            
            # Skip separator line
            if '---' in line:
                continue
            
            row = line.strip('|').split('|')
            html += "<tr>"
            tag = "th" if "Estrutura" in line else "td" # Simple heuristic for header
            for cell in row:
                cell_content = cell.strip()
                cell_content = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', cell_content)
                html += f"<{tag}>{cell_content}</{tag}>"
            html += "</tr>\n"
            continue
        else:
            if in_table:
                html += "</table>\n"
                in_table = False

        # Paragraphs
        if line.strip():
            content = line
            content = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', content)
            content = re.sub(r'`(.*?)`', r'<code>\1</code>', content)
            html += f"<p>{content}</p>\n"

    html += "</body></html>"

    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(html)

if __name__ == "__main__":
    convert_md_to_html('report/relatorio_tecnico.md', 'report/relatorio_tecnico.html')
    print("Convertido com sucesso para report/relatorio_tecnico.html")
