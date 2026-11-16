#!/bin/bash
# Windows (Git Bash) version of run.sh: rebuild SAPA.vpp and the diagram PNGs with Visual Paradigm CE 18.1.
# Usage: bash run_win.sh [all|uc|cd|sd|ad|srs]
# Needs: Visual Paradigm CE 18.1 in "C:\Program Files", Poppler (pdftoppm), Python with Pillow.
# Result: ../SAPA.vpp and ../png/<diagram name>.png (300 dpi, cropped).
set -e
HERE="$(cd "$(dirname "$0")" && pwd)"
DIAG="$HERE/.."
VP="/c/Program Files/Visual Paradigm CE 18.1"
PLUGINS="$APPDATA/VisualParadigm/plugins/sapa.gen"
WORK="${TMP:-/tmp}/sapa-vp"
mkdir -p "$WORK/api" "$WORK/classes" "$DIAG/png"

# 1. Open API classes (the bundled JDK cannot read openapi.jar directly), compile and install the plugin.
[ -d "$WORK/api/com" ] || python -I -c "import zipfile,sys; zipfile.ZipFile(sys.argv[1]).extractall(sys.argv[2])" "$VP/lib/openapi.jar" "$WORK/api"
rm -rf "$WORK/classes"/*
"$VP/jre/bin/javac" -nowarn -encoding UTF-8 -cp "$WORK/api" -d "$WORK/classes" "$HERE/plugin/src/sapa/gen/GenPlugin.java"
mkdir -p "$PLUGINS"
cp "$HERE/plugin/plugin.xml" "$PLUGINS/"
rm -rf "$PLUGINS/classes" && cp -r "$WORK/classes" "$PLUGINS/"

# 2. Spec, then build the project (the CLI needs an existing project of this version: use VP's system project).
python -I "$HERE/build_specs.py" "$WORK/sapa.tsv" "${1:-all}"
rm -f "$WORK"/SAPA*.vpp* "$WORK"/base.vpp*
cp "$APPDATA/VisualParadigm/ws/.vpprefdata/.systemproject.vpp" "$WORK/base.vpp"
W="$(cygpath -w "$WORK")"
cd "$VP/bin"
CP=".;../lib/vpplatform.jar;../lib/jniwrap.jar;../lib/winpack.jar;../ormlib/orm.jar;../ormlib/orm-core.jar$(for i in $(seq -w 1 20); do printf ';../lib/lib%s.jar' $i; done)"
JAVA() { ../jre/bin/java -Xmx2048m -Djava.awt.headless=true -cp "$CP" "$@" 2>&1 | grep -E "sapa.gen|Exception: [^C]" || true; }
JAVA com.vp.cmd.Plugin -project "$W\\base.vpp" -pluginid sapa.gen -pluginargs "'$W\\sapa.tsv' '$W\\SAPA.vpp'"

# 3. Export every diagram as PDF (sharper than VP's PNG export), rasterise at 300 dpi and crop.
rm -rf "$WORK/pdf" && mkdir -p "$WORK/pdf"
# the CLI exports one diagram per call when the output is a PDF file
grep '^DIAGRAM' "$WORK/sapa.tsv" | cut -f3 | tr -d '' | while IFS= read -r d; do
  JAVA com.vp.cmd.ExportDiagramImage -project "$W\\SAPA.vpp" -out "$W\\pdf\\$d.pdf" -diagram "$d" -type pdf
done
cd "$WORK/pdf"
for f in *.pdf; do
  [ -e "$f" ] || continue
  n="${f%.pdf}"
  pdftoppm -png -r 300 -singlefile "$f" "$WORK/pdf/_hi"
  python -I -c "
import sys
from PIL import Image, ImageOps
im = Image.open(sys.argv[1]).convert('RGB'); bb = ImageOps.invert(im).getbbox()
im.crop((max(bb[0]-30,0), max(bb[1]-30,0), min(bb[2]+30,im.width), min(bb[3]+30,im.height))).save(sys.argv[2], dpi=(300, 300))" "$WORK/pdf/_hi.png" "$DIAG/png/$n.png"
  echo "png: $n"
done
cp "$WORK/SAPA.vpp" "$DIAG/SAPA.vpp"
