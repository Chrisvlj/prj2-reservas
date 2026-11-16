"""Render a markdown subset to a single HTML page for screenshots."""

import html
import re
import sys
from pathlib import Path


def inline(text: str) -> str:
    escaped = html.escape(text)
    escaped = re.sub(r"`([^`]+)`", r"<code>\1</code>", escaped)
    escaped = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", escaped)
    escaped = re.sub(
        r"\[([^\]]+)\]\(([^)]+)\)",
        r'<a href="\2">\1</a>',
        escaped,
    )
    return escaped


def render(md: str, title: str) -> str:
    lines = md.splitlines()
    out = []
    i = 0
    in_code = False
    in_table = False
    in_list = False

    def close_list():
        nonlocal in_list
        if in_list:
            out.append("</ul>")
            in_list = False

    def close_table():
        nonlocal in_table
        if in_table:
            out.append("</tbody></table>")
            in_table = False

    while i < len(lines):
        line = lines[i]
        if line.startswith("```"):
            close_list()
            close_table()
            if not in_code:
                out.append("<pre><code>")
                in_code = True
            else:
                out.append("</code></pre>")
                in_code = False
            i += 1
            continue
        if in_code:
            out.append(html.escape(line) + "\n")
            i += 1
            continue
        if line.startswith("|"):
            close_list()
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            if all(re.fullmatch(r":?-{3,}:?", c.replace(" ", "")) or re.fullmatch(r"-+", c.replace(" ", "")) for c in cells):
                i += 1
                continue
            if not in_table:
                out.append("<table><tbody>")
                in_table = True
                tag = "th"
            else:
                tag = "td"
            out.append("<tr>" + "".join(f"<{tag}>{inline(c)}</{tag}>" for c in cells) + "</tr>")
            i += 1
            continue
        close_table()
        if not line.strip():
            close_list()
            i += 1
            continue
        m = re.match(r"^(#{1,3}) (.+)$", line)
        if m:
            close_list()
            level = len(m.group(1))
            out.append(f"<h{level}>{inline(m.group(2))}</h{level}>")
            i += 1
            continue
        if line.startswith("- "):
            if not in_list:
                out.append("<ul>")
                in_list = True
            out.append(f"<li>{inline(line[2:])}</li>")
            i += 1
            continue
        close_list()
        out.append(f"<p>{inline(line)}</p>")
        i += 1
    close_list()
    close_table()
    body = "\n".join(out)
    return f"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="utf-8">
<title>{html.escape(title)}</title>
<style>
  body {{ font: 16px/1.45 "Segoe UI", sans-serif; margin: 32px 40px; color: #1a1a1a; background: #fff; max-width: 980px; }}
  h1 {{ font-size: 28px; margin-bottom: 8px; }}
  h2 {{ font-size: 20px; margin-top: 28px; border-bottom: 1px solid #ddd; padding-bottom: 4px; }}
  h3 {{ font-size: 17px; margin-top: 20px; }}
  table {{ border-collapse: collapse; width: 100%; margin: 12px 0 20px; }}
  th, td {{ border: 1px solid #ccc; padding: 6px 8px; text-align: left; vertical-align: top; }}
  th {{ background: #f3f3f3; }}
  code {{ font-family: ui-monospace, monospace; font-size: 0.92em; background: #f6f6f6; padding: 0 3px; }}
  pre {{ background: #f6f6f6; padding: 12px; overflow: auto; }}
  pre code {{ background: transparent; padding: 0; }}
  a {{ color: #0b57d0; }}
</style>
</head>
<body>
{body}
</body>
</html>
"""


def main() -> None:
    src = Path(sys.argv[1])
    dest = Path(sys.argv[2])
    dest.write_text(render(src.read_text(), src.name), encoding="utf-8")


if __name__ == "__main__":
    main()
