"""Build SRS SAPA v1.1 dari template P07 (Template SRS Capstone Project SI UMBY).

Usage: python build_srs.py [path/ke/srs-identitas.json] [path/keluaran.docx]
  - Template : doc-srs/srs/template/P07 - Template SRS Capstone Project - SI UMBY.docx
  - Isi      : doc-srs/srs/isi_srs.py (Bab I-VI, pustaka, lampiran)
  - Diagram  : doc-srs/diagram/png (Visual Paradigm, dibangun dengan diagram/generator/run_win.sh)
  - Identitas: srs-identitas.json di Google Drive (nama, NIM, dosen); tidak disimpan di repo publik.
Hasil disimpan ke path "output" pada berkas identitas. Daftar isi, gambar, dan tabel diperbarui oleh Word
(lihat update_word.ps1).
"""
import copy
import json
import os
import re
import sys

import docx
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_BREAK
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Pt

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)  # doc-srs
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(ROOT, "diagram", "generator"))
import isi_srs as isi  # noqa: E402
from build_specs import ERD_TABLES  # noqa: E402

ID_PATH = sys.argv[1] if len(sys.argv) > 1 else r"G:\My Drive\dev\cekula\capstone-project\srs-identitas.json"
ID = json.load(open(ID_PATH, encoding="utf-8"))
TEMPLATE = os.path.join(HERE, "template", "P07 - Template SRS Capstone Project - SI UMBY.docx")
TEXT_W = 14.0  # cm: A4 21 cm - margin kiri 4 cm - margin kanan 3 cm
JUDUL = "SAPA (SISTEM ASISTEN PELANGGAN DAN AKUISISI)"
SUBJUDUL = "Chatbot WhatsApp Omnichannel Berbasis Kecerdasan Artifisial dan CRM pada Bimbingan Belajar Asentra"

doc = docx.Document(TEMPLATE)
body = doc.element.body


# ------------------------------------------------------------------ front matter
def set_par_text(p, text):
    runs = p.runs
    if not runs:
        p.add_run(text)
        return
    runs[0].text = text
    for r in runs[1:]:
        r._r.getparent().remove(r._r)


def all_paragraphs():
    for p in doc.paragraphs:
        yield p
    for t in doc.tables:
        for row in t.rows:
            for c in row.cells:
                for p in c.paragraphs:
                    yield p


ketua, ketua_nim = ID["ketua"]
mitra_nama, mitra_jabatan = ID["mitra_penandatangan"]
REPL = {
    "<JUDUL SISTEM / APLIKASI>": JUDUL,
    "<Subjudul singkat, misalnya: Studi Kasus pada Nama Mitra>": SUBJUDUL,
    "<nomor>": ID["kelompok"], "<12D/22D>": ID["kelas"],
    "<nama dosen pengampu>": ID["dosen"], "<nama mitra atau organisasi>": ID["mitra"], "<TAHUN>": ID["tahun"],
    "<judul sistem>": "SAPA (Sistem Asisten Pelanggan dan Akuisisi)",
    "<tanggal bulan tahun>": ID["tanggal_pengesahan"],
    "<nama dosen>": ID["dosen"], "NIDN. <NIDN>": "NIDN. " + ID["nidn"],
    "<nama perwakilan mitra>": mitra_nama, "<jabatan>": mitra_jabatan,
    "<nama ketua kelompok>": ketua,
}
for p in all_paragraphs():
    t = p.text
    if "<" not in t:
        continue
    new = t
    for a, b in REPL.items():
        new = new.replace(a, b)
    if new != t:
        set_par_text(p, new)

# sampul harus muat satu halaman: subjudul SAPA dua baris, jadi rapatkan blok program studi di bagian bawah
cover = doc.paragraphs[:17]
for p in cover:
    if p.text.startswith(("PROGRAM STUDI", "FAKULTAS", "UNIVERSITAS")):
        p.paragraph_format.space_after = Pt(0)
for p in cover[12:16]:
    if p.text == "" and not list(p._p.iter(qn("w:drawing"))):
        p._p.getparent().remove(p._p)
        break

# daftar gambar/tabel: tanpa ",1" (Word di laptop ini tidak menemukan entri dengan format "Gaya,1" bawaan template)
for it in body.iter(qn("w:instrText")):
    for gaya in ("Keterangan Gambar", "Keterangan Tabel"):
        if it.text and gaya in it.text:
            it.text = f' TOC \\h \\z \\t "{gaya}" '

# petunjuk template di bawah DAFTAR ISI/GAMBAR/TABEL tidak ikut dicetak
for p in list(doc.paragraphs):
    if p.text.startswith("[Klik kanan di area ini"):
        p._p.getparent().remove(p._p)

# anggota (template punya 6 baris; buang yang tidak terpakai)
tbl_anggota = doc.tables[0]
rows = tbl_anggota.rows
for i, (nama, nim) in enumerate(ID["anggota"], 1):
    set_par_text(rows[i].cells[1].paragraphs[0], nama)
    set_par_text(rows[i].cells[2].paragraphs[0], nim)
for r in list(rows)[len(ID["anggota"]) + 1:]:
    r._tr.getparent().remove(r._tr)
# NIM ketua
for p in doc.tables[2].rows[1].cells[0].paragraphs:
    if "<NIM>" in p.text:
        set_par_text(p, p.text.replace("<NIM>", ketua_nim))

# riwayat revisi
nama = {n.split()[0]: n for n, _ in ID["anggota"]}
REV = [
    ["1.0", "16/11/2026", "Seluruh dokumen", "Draf awal SRS disusun dari laporan ASN1 dan perencanaan sprint Scrum.",
     nama["Rifqi"]],
    ["1.1", "17/11/2026", "Seluruh dokumen", "Penyesuaian ke Laravel 12 dan WA Gateway; diagram arsitektur "
     "berlapis, deployment diagram, ERD, dan sitemap baru; seluruh diagram dibangun ulang di Visual Paradigm; 2FA ditetapkan "
     "Won't have; activity dan sequence diagram kedua belas use case di Bab IV; "
     "kebutuhan non-fungsional ditambah; sitasi APA 7.", nama["Agung"]],
]
trev = doc.tables[3]
for i, vals in enumerate(REV, 1):
    for j, v in enumerate(vals):
        set_par_text(trev.rows[i].cells[j].paragraphs[0], v)
for r in list(trev.rows)[len(REV) + 1:]:
    r._tr.getparent().remove(r._tr)

# ------------------------------------------------------------------ hapus isi contoh template mulai BAB I
kids = list(body)
start = next(i for i, k in enumerate(kids) if k.tag == qn("w:p") and "BAB I" in "".join(
    t.text or "" for t in k.iter(qn("w:t"))) and "PENDAHULUAN" in "".join(t.text or "" for t in k.iter(qn("w:t"))))
final_sect = kids[-1]
for k in kids[start:]:
    if k is not final_sect:
        body.remove(k)


# ------------------------------------------------------------------ label & nomor tabel/gambar (pass 1)
BLOCKS = list(isi.B) + [("pustaka",)] + [("h1", "LAMPIRAN", None, None)] + list(isi.LAMPIRAN)
NUM = {}
chap, cnt = None, {"tab": 0, "fig": 0}
for blk in BLOCKS:
    kind = blk[0]
    if kind == "h1" and blk[3]:
        chap, cnt = blk[3], {"tab": 0, "fig": 0}
    elif kind == "h2app":
        chap, cnt = blk[2], {"tab": 0, "fig": 0}
    elif kind in ("table", "kv", "kamus"):
        cnt["tab"] += 1
        NUM["tab:" + blk[1]] = f"Tabel {chap}.{cnt['tab']}"
    elif kind == "fig":
        cnt["fig"] += 1
        NUM["fig:" + blk[1]] = f"Gambar {chap}.{cnt['fig']}"


def refs(text):
    def sub(m):
        key = m.group(1)
        if key not in NUM:
            raise SystemExit(f"rujukan tidak dikenal: {key}")
        return NUM[key]
    return re.sub(r"\{((?:tab|fig):[a-z0-9]+)\}", sub, text)


# ------------------------------------------------------------------ helpers (pass 2)
def new_par(style="Normal", align=None):
    p = OxmlElement("w:p")
    final_sect.addprevious(p)
    para = docx.text.paragraph.Paragraph(p, doc._body)
    para.style = doc.styles[style]
    if align is not None:
        para.alignment = align
    return para


def keep_next(para):
    para._p.get_or_add_pPr().append(OxmlElement("w:keepNext"))


def page_break_before(para):
    para._p.get_or_add_pPr().insert(0, OxmlElement("w:pageBreakBefore"))


def add_text(para, text, size=None, bold=False):
    """**tebal**, *miring*, dan [ISI: ...] berstabilo kuning."""
    text = refs(text)
    for tok in re.split(r"(\*\*[^*]+\*\*|\*[^*]+\*|\[ISI[^\]]*\])", text):
        if not tok:
            continue
        b, i, hl = bold, False, False
        if tok.startswith("**") and tok.endswith("**"):
            tok, b = tok[2:-2], True
        elif tok.startswith("*") and tok.endswith("*") and len(tok) > 2:
            tok, i = tok[1:-1], True
        elif tok.startswith("[ISI"):
            hl = True
        r = para.add_run(tok)
        r.bold, r.italic = b or None, i or None
        if size:
            r.font.size = Pt(size)
        if hl:
            h = OxmlElement("w:highlight"); h.set(qn("w:val"), "yellow"); r._r.get_or_add_rPr().append(h)


def body_par(text):
    p = new_par("Normal", WD_ALIGN_PARAGRAPH.JUSTIFY)
    add_text(p, text)
    return p


def list_item(marker, text, indent=0.75):
    p = new_par("Normal", WD_ALIGN_PARAGRAPH.JUSTIFY)
    pf = p.paragraph_format
    pf.left_indent, pf.first_line_indent = Cm(indent), Cm(-indent)
    pf.tab_stops.add_tab_stop(Cm(indent))
    pf.space_after = Pt(2)
    p.add_run(marker + "\t")
    add_text(p, text)
    return p


def bullet(text):
    p = new_par("List Bullet", WD_ALIGN_PARAGRAPH.JUSTIFY)
    p.paragraph_format.space_after = Pt(2)
    add_text(p, text)
    return p


def caption(style, label, title):
    p = new_par(style)
    p.add_run(f"{label} {title}")
    if style == "Keterangan Tabel":
        keep_next(p)
    return p


def shade(cell, fill):
    tcPr = cell._tc.get_or_add_tcPr()
    s = OxmlElement("w:shd"); s.set(qn("w:val"), "clear"); s.set(qn("w:color"), "auto"); s.set(qn("w:fill"), fill)
    tcPr.append(s)


def cell_write(cell, text, bold=False, center=False, size=10):
    parts = refs(text).split("\n")
    first = cell.paragraphs[0]
    for k, part in enumerate(parts):
        p = first if k == 0 else cell.add_paragraph()
        p.style = doc.styles["Normal"]
        pf = p.paragraph_format
        pf.space_before, pf.space_after, pf.line_spacing = Pt(0), Pt(2), 1.0
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER if center else WD_ALIGN_PARAGRAPH.LEFT
        add_text(p, part, size=size, bold=bold)


def make_table(header, rows, widths):
    tot = sum(widths)
    widths = [w * TEXT_W / tot for w in widths]
    t = doc.add_table(rows=1 + len(rows), cols=len(header))
    final_sect.addprevious(t._tbl)
    t.style = doc.styles["Table Grid"]
    tblPr = t._tbl.tblPr
    lay = OxmlElement("w:tblLayout"); lay.set(qn("w:type"), "fixed"); tblPr.append(lay)
    for gc, w in zip(t._tbl.tblGrid.findall(qn("w:gridCol")), widths):
        gc.set(qn("w:w"), str(int(w * 567)))
    for row in t.rows:
        for c, w in zip(row.cells, widths):
            c.width = Cm(w)
    for j, h in enumerate(header):
        cell_write(t.rows[0].cells[j], h, bold=True, center=True)
        shade(t.rows[0].cells[j], "D9E2F3")
    trPr = t.rows[0]._tr.get_or_add_trPr(); trPr.append(OxmlElement("w:tblHeader"))
    for i, r in enumerate(rows, 1):
        for j, v in enumerate(r):
            cell_write(t.rows[i].cells[j], v)
    gap = new_par("Normal")
    gap.paragraph_format.space_after = Pt(6)
    return t


def picture(path, title, label, after):
    from docx.image.image import Image
    full = os.path.join(ROOT, path)
    if not os.path.exists(full):
        raise SystemExit(f"gambar tidak ada: {full}")
    img = Image.from_file(full)
    # gambar diletakkan di dalam tabel satu sel bergaris, seperti kotak "[Sisipkan gambar di sini]" pada template
    max_w, max_h = Cm(TEXT_W - 0.6), Cm(19.5)
    scale = min(max_w / img.px_width, max_h / img.px_height)
    t = doc.add_table(rows=1, cols=1)
    final_sect.addprevious(t._tbl)
    t.style = doc.styles["Table Grid"]
    t.alignment = 1  # tengah
    t._tbl.tblGrid.findall(qn("w:gridCol"))[0].set(qn("w:w"), str(int(TEXT_W * 567)))
    cell = t.rows[0].cells[0]
    cell.width = Cm(TEXT_W)
    trPr = t.rows[0]._tr.get_or_add_trPr()
    trPr.append(OxmlElement("w:cantSplit"))
    p = cell.paragraphs[0]
    p.style = doc.styles["Normal"]
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    pf = p.paragraph_format
    pf.space_before, pf.space_after, pf.line_spacing = Pt(4), Pt(4), 1.0
    keep_next(p)  # tabel gambar tetap satu halaman dengan keterangannya
    p.add_run().add_picture(full, width=int(img.px_width * scale))
    caption("Keterangan Gambar", label, title).paragraph_format.space_before = Pt(4)
    if after:
        body_par(after)


def kamus(label, title):
    T = {t[1]: t for t in ERD_TABLES}
    rows, spans = [], []
    for name in isi.KAMUS_TABEL:
        cols = T[name][4]
        spans.append((len(rows) + 1, len(cols)))
        for k, (c, typ, pk, nul) in enumerate(cols):
            ket = isi.KET.get(c, "")
            if nul:
                ket += "; boleh kosong"
            rows.append([name if k == 0 else "", c, typ, ket])
    caption("Keterangan Tabel", label, title)
    t = make_table(["Tabel", "Kolom", "Tipe data", "Keterangan"], rows, [3.4, 3.6, 2.6, 5.4])
    for first, n in spans:  # gabungkan sel nama tabel
        if n > 1:
            a = t.cell(first, 0)
            name = a.text
            m = a.merge(t.cell(first + n - 1, 0))
            for p in m.paragraphs[1:]:
                p._p.getparent().remove(p._p)
            m.paragraphs[0].runs[0].text = name if m.paragraphs[0].runs else name


# ------------------------------------------------------------------ render (pass 2)
for blk in BLOCKS:
    kind = blk[0]
    if kind == "h1":
        p = new_par("Heading 1", WD_ALIGN_PARAGRAPH.CENTER)
        page_break_before(p)
        p.add_run(blk[1])
        if blk[2]:
            r = p.add_run(); r.add_break(); r.add_text(blk[2])
        keep_next(p)
    elif kind in ("h2", "h2app"):
        p = new_par("Heading 2")
        p.add_run(blk[1])
        if kind == "h2app" and blk[2] != "A":
            page_break_before(p)
        keep_next(p)
    elif kind == "h3":
        p = new_par("Heading 3")
        p.add_run(blk[1])
        keep_next(p)
    elif kind == "p":
        body_par(blk[1])
    elif kind == "ol":
        for i, item in enumerate(blk[1], 1):
            list_item(f"{i}.", item)
    elif kind == "ul":
        for item in blk[1]:
            bullet(item)
    elif kind == "table":
        _, key, title, header, rows, widths = blk
        caption("Keterangan Tabel", NUM["tab:" + key], title)
        make_table(header, rows, widths)
    elif kind == "kv":
        _, key, title, rows = blk
        caption("Keterangan Tabel", NUM["tab:" + key], title)
        t = make_table(["Elemen", "Keterangan"], rows, [3.4, 11.6])
        for i in range(1, len(rows) + 1):
            shade(t.rows[i].cells[0], "F2F2F2")
            for r in t.rows[i].cells[0].paragraphs[0].runs:
                r.bold = True
    elif kind == "kamus":
        kamus(NUM["tab:" + blk[1]], blk[2])
    elif kind == "fig":
        _, key, title, path, after = blk
        picture(path, title, NUM["fig:" + key], after)
    elif kind == "pustaka":
        p = new_par("Heading 1", WD_ALIGN_PARAGRAPH.CENTER)
        page_break_before(p)
        p.add_run("DAFTAR PUSTAKA")
        for entry in isi.PUSTAKA:
            q = new_par("Normal", WD_ALIGN_PARAGRAPH.LEFT)
            pf = q.paragraph_format
            pf.left_indent, pf.first_line_indent = Cm(1.0), Cm(-1.0)
            pf.line_spacing, pf.space_after = 1.0, Pt(10)
            add_text(q, entry)
    else:
        raise SystemExit(f"blok tidak dikenal: {kind}")

# pemeriksaan gaya: tanpa em dash, tanpa istilah terlarang di teks isi
words = " ".join(t.text or "" for t in body.iter(qn("w:t")))
if "\u2014" in words:
    raise SystemExit("ada em dash di dokumen")
for bad in ("kata sandi", "dasbor ", "kueri", "surel", "peladen", "purwarupa", "akan tetapi", "Dengan demikian",
            "tidak hanya"):
    if bad in words.lower() if bad.islower() else bad in words:
        print("PERINGATAN istilah:", bad)
out = sys.argv[2] if len(sys.argv) > 2 else ID["output"]  # argumen ke-2: path keluaran lain
doc.save(out)
print("tersimpan:", out)
print("tabel:", sum(1 for k in NUM if k.startswith("tab:")), "gambar:", sum(1 for k in NUM if k.startswith("fig:")))
print("placeholder [ISI]:", sorted(set(re.findall(r"\[ISI:[^\]]*\]", words))))
