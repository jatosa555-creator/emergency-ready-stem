"""Render public human-readable views from the canonical knowledge JSON."""
from pathlib import Path
import json
R=Path(__file__).resolve().parents[1]
for x in json.loads((R/'remote-mcp/data/catalog.json').read_text(encoding='utf-8')):
 text=f"# {x['id']} — {x['title']}\n\nประเภท: {x['source_type']} | เวอร์ชัน {x['version']} | Snapshot: {x['snapshot_date']}\n\n{x['text']}\n\nเขียนขึ้นสำหรับ Emergency-Ready STEM Learning Design for Well-being and Resilience ไม่ใช่ประกาศทางการหรือสำเนาเช็กลิสต์จากโครงการอื่น\n"
 (R/'knowledge'/f"{x['id']}.md").write_text(text,encoding='utf-8')
print('Rendered public knowledge views from canonical catalog.')
