"""Encode a walkthrough from real CUA screenshots of the live MCP demo."""
from pathlib import Path
import shutil,subprocess
R=Path(__file__).resolve().parents[1];frames=R/'remote-mcp/artifacts/demo';out=R/'remote-mcp/service-public/emergency-ready-stem-walkthrough.mp4'
for i in range(1,7):
 if not (frames/f'step-{i}.png').is_file():raise SystemExit('Capture all actual browser states first; no synthetic screenshots')
seq=frames/'frames.txt';seq.write_text(''.join(f"file 'step-{i}.png'\nduration 9\n" for i in range(1,7))+"file 'step-6.png'\n",encoding='utf-8')
subprocess.run([shutil.which('ffmpeg')or'ffmpeg','-y','-f','concat','-safe','0','-i',str(seq),'-vf','pad=ceil(iw/2)*2:ceil(ih/2)*2','-r','24','-c:v','libx264','-pix_fmt','yuv420p','-movflags','+faststart',str(out)],check=True,stdout=subprocess.DEVNULL,stderr=subprocess.PIPE)
print('Created actual live-response walkthrough:',out,'bytes:',out.stat().st_size)
