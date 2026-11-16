"""Build a local HTML sheet from `gh issue list --json` on stdin."""

import html
import json
import sys
from pathlib import Path

issues = json.load(sys.stdin)
rows = []
for issue in sorted(issues, key=lambda item: item["number"]):
    labels = ", ".join(html.escape(label["name"]) for label in issue["labels"])
    url = html.escape(issue["url"])
    title = html.escape(issue["title"])
    rows.append(
        f'<tr><td>#{issue["number"]}</td>'
        f'<td><a href="{url}">{title}</a></td>'
        f"<td>{labels}</td><td>abierto</td></tr>"
    )

page = f"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="utf-8">
<title>Issues fase 2</title>
<style>
  body {{ font: 16px/1.4 "Segoe UI", sans-serif; margin: 32px 40px; color: #1a1a1a; background: #fff; }}
  h1 {{ font-size: 26px; margin-bottom: 4px; }}
  p {{ color: #333; max-width: 900px; }}
  table {{ border-collapse: collapse; width: 100%; margin-top: 16px; }}
  th, td {{ border: 1px solid #ccc; padding: 8px; text-align: left; vertical-align: top; }}
  th {{ background: #f3f3f3; }}
  a {{ color: #0b57d0; }}
</style>
</head>
<body>
<h1>Issues abiertos — Chrisvlj/prj2-reservas</h1>
<p>Listado real de <code>gh issue list</code> el 2026-11-16. El repositorio es privado, así que esta captura es local y cada fila enlaza el issue. No es una imagen de github.com.</p>
<table>
<thead><tr><th>Issue</th><th>Título</th><th>Etiquetas</th><th>Estado</th></tr></thead>
<tbody>
{chr(10).join(rows)}
</tbody>
</table>
</body>
</html>
"""
Path(sys.argv[1]).write_text(page, encoding="utf-8")
