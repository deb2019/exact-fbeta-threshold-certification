from pathlib import Path
import json,hashlib,zipfile
root=Path(__file__).resolve().parent.parent
out=root.parent/'Manuscript_Source_Package_Expanded.zip'
files=sorted(p for p in root.rglob('*') if p.is_file() and '__pycache__' not in p.parts and p.name!='SHA256_MANIFEST.json')
manifest={str(p.relative_to(root)):hashlib.sha256(p.read_bytes()).hexdigest() for p in files}
(root/'SHA256_MANIFEST.json').write_text(json.dumps(manifest,indent=2))
with zipfile.ZipFile(out,'w',zipfile.ZIP_DEFLATED) as z:
 for p in files:z.write(p,p.relative_to(root))
 z.write(root/'SHA256_MANIFEST.json','SHA256_MANIFEST.json')
print(out)
