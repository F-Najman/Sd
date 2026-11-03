"""Create the final file manifest only after the complete package audit passes.

Run once with ordinary Python after finishing the presentation text. This
does not certify the mathematics: it freezes the files that were reviewed
and computationally checked. It refuses drafts and incomplete replay sets.
"""
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys

FOLDER = Path(__file__).resolve().parent


def main():
    if sys.flags.optimize:
        raise SystemExit('Run without -O or PYTHONOPTIMIZE: verification requires assertions')
    destination = FOLDER/'PACKAGE_MANIFEST.json'
    if destination.exists():
        raise SystemExit('A package manifest already exists; no files were changed')
    result = subprocess.run([sys.executable,str(FOLDER/'verify.py'),'--development'],
                            env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1'))
    if result.returncode:
        return result.returncode
    proof = (FOLDER/'classification.tex').read_text()
    audit = (FOLDER/'REAUDIT.md').read_text()
    assert 'working re-audit draft' not in proof.lower(),'presentation text is still a draft'
    assert 're-audit pending' not in proof.lower(),'theorem is still labelled pending'
    assert '- [ ]' not in audit,'completion checklist has unfinished requirements'
    excluded = {'PACKAGE_MANIFEST.json','classification.log','classification.aux',
                'classification.out','classification.synctex.gz'}
    files = {}
    for path in sorted(FOLDER.rglob('*')):
        relative = path.relative_to(FOLDER)
        if not path.is_file() or '__pycache__' in relative.parts:
            continue
        if path.suffix in {'.pyc','.pyo'} or str(relative) in excluded:
            continue
        assert not path.is_symlink(),('external or ambiguous symlink',relative)
        files[str(relative)] = hashlib.sha256(path.read_bytes()).hexdigest()
    manifest = dict(status='SEALED_REAUDITED_PRESENTATION_PACKAGE',
                    scope='Reviewed proof, tables, code and evidence; not a formal proof-assistant certificate',
                    files=files)
    destination.write_text(json.dumps(manifest,indent=2)+'\n')
    subprocess.run([sys.executable,str(FOLDER/'verify.py')],
                   env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1'),check=True)
    print('SEALED',len(files),'files',flush=True)
    return 0


if __name__=='__main__':
    sys.exit(main())
