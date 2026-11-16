"""Build the tab-separated diagram spec consumed by the sapa.gen Visual Paradigm plugin.

Usage: python3 build_specs.py out.tsv
Diagrams follow the ANSI course style: use case with <<Include>> to Login, sequence with
Actor -> View (boundary) -> Cont (control) -> Ent (entity), class diagram in M-V-C columns,
activity diagrams with Aktor | Sistem swimlanes derived from the use case descriptions.
"""
import math
import sys

CH = 6.4  # approx. pixel width of one character in VP's default font
OUT = []


def emit(*cols):
    OUT.append("\t".join(str(c) for c in cols))


def tw(text):
    return int(len(text) * CH) + 14


# --------------------------------------------------------------------------- use case
def use_case_diagram():
    emit("DIAGRAM", "usecase", "Use Case Diagram SAPA")
    sx, sy, sw = 200, 20, 680
    left = [  # (id, name)
        ("uc02", "Mengirim Pesan WhatsApp"),
        ("uc04", "Mengelola Percakapan"),
        ("uc05", "Mengelola Prospek"),
        ("uc06", "Mengelola Kontak Pelanggan"),
        ("uc07", "Melihat Dashboard Pemantauan"),
        ("uc09", "Mengelola Basis Pengetahuan"),
        ("uc12", "Melihat Log Audit"),
        ("uc08", "Mengelola Nomor WhatsApp"),
        ("uc10", "Mengatur AI dan Anti-ban"),
        ("uc11", "Mengelola Tim dan Hak Akses"),
    ]
    row_h, top = 78, sy + 70
    sh = top + row_h * len(left) + 10 - sy
    emit("SHAPE", "sys", "system", sx, sy, sw, sh, "Sistem Asisten Pelanggan dan Akuisisi (SAPA)\\nBimbingan Belajar Asentra")
    ucw, uch = 250, 52
    pos = {}
    for i, (uid, name) in enumerate(left):
        x, y = sx + 50, top + i * row_h
        emit("SHAPE", uid, "usecase", x, y, ucw, uch, name)
        emit("PARENT", uid, "sys")
        pos[uid] = (x, y)
    emit("SHAPE", "uc03", "usecase", sx + 420, top, 230, uch, "Menjawab Pesan Otomatis dengan AI")
    emit("PARENT", "uc03", "sys")
    ly = top + row_h * 4 + 10
    emit("SHAPE", "uc01", "usecase", sx + 500, ly, 150, uch, "Login")
    emit("PARENT", "uc01", "sys")

    def ycenter(uid):
        return pos[uid][1] + uch // 2

    actors = [  # id, name, y (centred near its use cases)
        ("pel", "Pelanggan", ycenter("uc02") - 40),
        ("agen", "Agen/CS", ycenter("uc05") - 40),
        ("sup", "Supervisor", ycenter("uc09") - 40),
        ("adm", "Administrator", ycenter("uc10") - 40),
    ]
    for aid, name, y in actors:
        emit("SHAPE", aid, "actor", 40, y, 40, 80, name)
    emit("SHAPE", "wa", "actor", sx + sw + 70, top - 10, 40, 80, "WhatsApp Web")
    emit("SHAPE", "ai", "actor", sx + sw + 70, top + 150, 40, 80, "Penyedia AI")

    links = {
        "pel": ["uc02"],
        "agen": ["uc04", "uc05", "uc06"],
        "sup": ["uc07", "uc09", "uc12"],
        "adm": ["uc07", "uc09", "uc12", "uc08", "uc10", "uc11"],
    }
    for aid, ucs in links.items():
        for u in ucs:
            emit("CONN", "assoc", aid, u)
    for u in ("uc03",):
        emit("CONN", "assoc", "wa", u)
    emit("CONN", "assoc", "ai", "uc03")
    emit("CONN", "include", "uc02", "uc03")
    lx, lyc = sx + 500 + 75, ly + uch // 2
    for uid in ("uc04", "uc05", "uc06", "uc07", "uc09", "uc12", "uc08", "uc10", "uc11"):
        x0, y0 = pos[uid][0] + ucw, pos[uid][1] + uch // 2
        # caption 30% along the line so the labels do not pile up near Login
        cx = int(x0 + (lx - 75 - x0) * 0.35) - 10
        cy = int(y0 + (lyc - y0) * 0.35) - 16
        emit("CONN", "include", uid, "uc01", "", "", "", "", f"{cx},{cy}")


# --------------------------------------------------------------------------- sequence
STEREO = {"V": "boundary", "C": "control", "E": "entity"}


def sequence(name, lifelines, msgs):
    """lifelines: [(id, label, kind)] kind in A (actor), V, C, E.
    msgs: [(kind, from, to, label, seq)] kind in msg/ret/self."""
    emit("DIAGRAM", "sequence", name)
    xs, x = {}, 30
    widths = {}
    for i, (lid, label, kind) in enumerate(lifelines):
        w = max(110, tw(label))
        widths[lid] = w
    # spacing driven by the longest label of messages between neighbouring lifelines
    order = [l[0] for l in lifelines]
    gap = {}
    for kind, a, b, label, seq in msgs:
        if kind == "self":
            continue
        i, j = sorted((order.index(a), order.index(b)))
        need = tw(f"{seq}: {label}") // (j - i) + 30
        for k in range(i, j):
            gap[k] = max(gap.get(k, 0), need)
    y_top, step = 40, 32
    n = len(msgs)
    height = 120 + n * step + 60
    for i, (lid, label, kind) in enumerate(lifelines):
        w = widths[lid]
        if i > 0:
            prev = lifelines[i - 1][0]
            x = xs[prev] + widths[prev] // 2 + max(170, gap.get(i - 1, 0)) - w // 2
        xs[lid] = x
        if kind == "A":
            emit("SHAPE", lid, "iactor", x + w // 2 - 20, y_top, 40, height, label)
            xs[lid] = x + w // 2 - 20
            widths[lid] = 40
        else:
            emit("SHAPE", lid, "lifeline", x, y_top, w, height, label, STEREO[kind])
    # message y positions
    ys = []
    y = 130
    for kind, a, b, label, seq in msgs:
        ys.append(y)
        y += step + (20 if kind == "self" else 0)
    # activations per top-level step for every non-actor lifeline involved
    kinds = {l[0]: l[2] for l in lifelines}
    groups = {}
    for (kind, a, b, label, seq), yy in zip(msgs, ys):
        g = seq.split(".")[0]
        for lid in (a, b):
            if kinds[lid] == "A":
                continue
            lo, hi = groups.get((g, lid), (yy, yy))
            hi2 = yy + (24 if kind == "self" else 0)
            groups[(g, lid)] = (min(lo, yy), max(hi, hi2))
    k = 0
    for (g, lid), (lo, hi) in sorted(groups.items(), key=lambda t: t[1][0]):
        k += 1
        emit("ACT", f"act{k}", lid, lo - 6, hi + 10)
    for (kind, a, b, label, seq), yy in zip(msgs, ys):
        emit("CONN", kind, a, b, label, seq, yy)


def sequences():
    S = sequence
    S("SD-01 - Login",
      [("U", "Pengguna", "A"), ("V", "View : Login", "V"), ("C", "Cont : Login", "C"),
       ("E1", "Ent : Pengguna", "E"), ("E2", "Ent : AksesNomor", "E"), ("E3", "Ent : LogAudit", "E")],
      [("msg", "U", "V", "Isi email & password, klik Masuk", "1"),
       ("msg", "V", "C", "login(email, password)", "1.1"),
       ("msg", "C", "E1", "cariPengguna(email)", "1.1.1"),
       ("ret", "E1", "C", "dataPengguna", "1.1.2"),
       ("self", "C", "C", "verifikasiPassword()", "1.1.3"),
       ("msg", "C", "E2", "ambilAksesNomor(idPengguna)", "1.1.4"),
       ("ret", "E2", "C", "daftarNomor", "1.1.5"),
       ("msg", "C", "E3", "catatLog(\"login\")", "1.1.6"),
       ("ret", "C", "V", "tampilkanHalamanSesuaiPeran", "1.2")])
    S("SD-02 - Mengirim Pesan WhatsApp",
      [("P", "Pelanggan", "A"), ("V", "View : WhatsAppGateway", "V"), ("C", "Cont : Percakapan", "C"),
       ("E1", "Ent : Kontak", "E"), ("E2", "Ent : Prospek", "E"), ("E3", "Ent : Percakapan", "E"),
       ("E4", "Ent : Pesan", "E"), ("AI", "Cont : AIEngine", "C")],
      [("msg", "P", "V", "Kirim pesan", "1"),
       ("msg", "V", "C", "terimaPesan(nomor, isi)", "1.1"),
       ("msg", "C", "E1", "cariAtauBuatKontak(nomor)", "1.1.1"),
       ("ret", "E1", "C", "dataKontak", "1.1.2"),
       ("msg", "C", "E2", "buatProspek(\"baru\")", "1.1.3"),
       ("msg", "C", "E3", "bukaPercakapan(idKontak, idNomor)", "1.1.4"),
       ("msg", "C", "E4", "simpanPesan(masuk)", "1.1.5"),
       ("msg", "C", "AI", "prosesBalasan(pesan)", "1.1.6"),
       ("ret", "AI", "C", "balasan", "1.1.7"),
       ("msg", "C", "V", "kirimBalasan(balasan)", "1.2"),
       ("ret", "V", "P", "Balasan diterima", "1.3")])
    S("SD-03 - Menjawab Pesan Otomatis dengan AI",
      [("C", "Cont : AIEngine", "C"), ("E1", "Ent : Kontak", "E"), ("E2", "Ent : Prospek", "E"),
       ("E3", "Ent : ArtikelPengetahuan", "E"), ("AI", "Penyedia AI", "A"), ("E4", "Ent : PengaturanAI", "E"),
       ("AB", "Cont : AntiBan", "C"), ("E5", "Ent : AntreanKeluar", "E"), ("WA", "WhatsApp Web", "A")],
      [("self", "C", "C", "klasifikasiMaksud() & ekstrakEntitas()", "1"),
       ("msg", "C", "E1", "perbaruiKontak(entitas)", "1.1"),
       ("msg", "C", "E2", "hitungSkor()", "1.2"),
       ("msg", "C", "E3", "cariArtikel(query)", "1.3"),
       ("ret", "E3", "C", "artikelRelevan", "1.4"),
       ("msg", "C", "AI", "susunJawaban(artikel)", "1.5"),
       ("ret", "AI", "C", "jawaban", "1.6"),
       ("msg", "C", "E4", "ambilAmbang()", "1.7"),
       ("ret", "E4", "C", "ambang", "1.8"),
       ("self", "C", "C", "hitungKeyakinan()", "1.9"),
       ("msg", "C", "AB", "nilaiPesan(jawaban)", "1.10"),
       ("msg", "AB", "E5", "simpanAntrean(keputusan)", "1.10.1"),
       ("msg", "AB", "WA", "kirimPesan()", "1.10.2"),
       ("ret", "WA", "AB", "terkirim", "1.10.3"),
       ("ret", "AB", "C", "statusKirim", "1.11")])
    S("SD-04 - Mengelola Percakapan",
      [("U", "Agen/CS", "A"), ("V", "View : KotakMasuk", "V"), ("C", "Cont : Percakapan", "C"),
       ("E1", "Ent : AksesNomor", "E"), ("E2", "Ent : Percakapan", "E"), ("E3", "Ent : Pesan", "E"),
       ("AB", "Cont : AntiBan", "C"), ("E4", "Ent : LogAudit", "E")],
      [("msg", "U", "V", "Klik menu Kotak Masuk", "1"),
       ("msg", "V", "C", "muatPercakapan(idPengguna)", "1.1"),
       ("msg", "C", "E1", "ambilAksesNomor()", "1.1.1"),
       ("msg", "C", "E2", "ambilPercakapan(daftarNomor)", "1.1.2"),
       ("ret", "E2", "C", "daftarPercakapan", "1.1.3"),
       ("ret", "C", "V", "tampilkanDaftar", "1.2"),
       ("msg", "U", "V", "Pilih percakapan", "2"),
       ("msg", "V", "C", "muatPesan(idPercakapan)", "2.1"),
       ("msg", "C", "E3", "ambilPesan()", "2.1.1"),
       ("ret", "E3", "C", "riwayat & jejak AI", "2.1.2"),
       ("ret", "C", "V", "tampilkanRiwayat", "2.2"),
       ("msg", "U", "V", "Ambil alih & kirim balasan", "3"),
       ("msg", "V", "C", "kirimBalasan(isi)", "3.1"),
       ("msg", "C", "E2", "setPenangan(\"manusia\")", "3.1.1"),
       ("msg", "C", "AB", "nilaiPesan()", "3.1.2"),
       ("ret", "AB", "C", "keputusan", "3.1.3"),
       ("msg", "C", "E3", "simpanPesan(keluar)", "3.1.4"),
       ("msg", "C", "E4", "catatLog(\"ambil alih\")", "3.1.5"),
       ("ret", "C", "V", "balasanTerkirim", "3.2")])
    S("SD-05 - Mengelola Prospek",
      [("U", "Agen/CS", "A"), ("V", "View : Prospek", "V"), ("C", "Cont : Prospek", "C"),
       ("E1", "Ent : Prospek", "E"), ("E2", "Ent : AktivitasProspek", "E"), ("E3", "Ent : LogAudit", "E")],
      [("msg", "U", "V", "Klik menu Prospek", "1"),
       ("msg", "V", "C", "muatProspek()", "1.1"),
       ("msg", "C", "E1", "ambilProspek()", "1.1.1"),
       ("ret", "E1", "C", "daftarProspek", "1.1.2"),
       ("ret", "C", "V", "tampilkanPapan", "1.2"),
       ("msg", "U", "V", "Ubah tahap & isi catatan, klik Simpan", "2"),
       ("msg", "V", "C", "simpanPerubahan(tahap, catatan, tgl)", "2.1"),
       ("self", "C", "C", "validasi()", "2.1.1"),
       ("msg", "C", "E1", "ubahTahap()", "2.1.2"),
       ("msg", "C", "E2", "tambahAktivitas()", "2.1.3"),
       ("msg", "C", "E1", "hitungUlangSkor()", "2.1.4"),
       ("msg", "C", "E3", "catatLog()", "2.1.5"),
       ("ret", "C", "V", "tampilkanProspekTersimpan", "2.2")])
    S("SD-06 - Mengelola Kontak Pelanggan",
      [("U", "Agen/CS", "A"), ("V", "View : Kontak", "V"), ("C", "Cont : Kontak", "C"),
       ("E1", "Ent : Kontak", "E"), ("E2", "Ent : LogAudit", "E")],
      [("msg", "U", "V", "Ketik kata kunci pencarian", "1"),
       ("msg", "V", "C", "cariKontak(kataKunci)", "1.1"),
       ("msg", "C", "E1", "cari()", "1.1.1"),
       ("ret", "E1", "C", "hasil", "1.1.2"),
       ("ret", "C", "V", "tampilkanDaftar", "1.2"),
       ("msg", "U", "V", "Ubah data & klik Simpan", "2"),
       ("msg", "V", "C", "simpanKontak(data)", "2.1"),
       ("self", "C", "C", "validasiData()", "2.1.1"),
       ("msg", "C", "E1", "perbarui()", "2.1.2"),
       ("msg", "C", "E2", "catatLog()", "2.1.3"),
       ("ret", "C", "V", "tampilkanTersimpan", "2.2")])
    S("SD-07 - Melihat Dashboard Pemantauan",
      [("U", "Supervisor/Administrator", "A"), ("V", "View : Dashboard", "V"), ("C", "Cont : Dashboard", "C"),
       ("E1", "Ent : AksesNomor", "E"), ("E2", "Ent : MetrikHarian", "E"), ("E3", "Ent : NomorWhatsApp", "E")],
      [("msg", "U", "V", "Klik menu Dashboard", "1"),
       ("msg", "V", "C", "muatDashboard()", "1.1"),
       ("msg", "C", "E1", "ambilAksesNomor()", "1.1.1"),
       ("msg", "C", "E2", "ambilMetrik(nomor, periode)", "1.1.2"),
       ("ret", "E2", "C", "metrik", "1.1.3"),
       ("msg", "C", "E3", "ambilStatusNomor()", "1.1.4"),
       ("ret", "E3", "C", "status", "1.1.5"),
       ("ret", "C", "V", "tampilkanDashboard", "1.2"),
       ("msg", "U", "V", "Pilih filter nomor & periode", "2"),
       ("msg", "V", "C", "filterPeriode(nomor, periode)", "2.1"),
       ("self", "C", "C", "hitungMetrik()", "2.1.1"),
       ("ret", "C", "V", "tampilkanHasilFilter", "2.2")])
    S("SD-08 - Mengelola Nomor WhatsApp",
      [("U", "Administrator", "A"), ("V", "View : NomorWhatsApp", "V"), ("C", "Cont : NomorWA", "C"),
       ("E1", "Ent : NomorWhatsApp", "E"), ("WA", "WhatsApp Web", "A"), ("E2", "Ent : LogAudit", "E")],
      [("msg", "U", "V", "Isi form & klik Tautkan", "1"),
       ("msg", "V", "C", "tambahNomor(label, nomor, tujuan)", "1.1"),
       ("msg", "C", "E1", "simpanNomor(\"menunggu\")", "1.1.1"),
       ("msg", "C", "WA", "buatSesi()", "1.1.2"),
       ("ret", "WA", "C", "kodeQR", "1.1.3"),
       ("ret", "C", "V", "tampilkanQR", "1.2"),
       ("msg", "U", "WA", "Pindai kode QR dari ponsel", "2"),
       ("msg", "WA", "C", "konfirmasiTertaut()", "2.1"),
       ("msg", "C", "E1", "ubahStatus(\"tersambung\")", "2.1.1"),
       ("msg", "C", "E2", "catatLog()", "2.1.2"),
       ("ret", "C", "V", "tampilkanStatusTersambung", "2.2")])
    S("SD-09 - Mengelola Basis Pengetahuan",
      [("U", "Supervisor/Administrator", "A"), ("V", "View : BasisPengetahuan", "V"),
       ("C", "Cont : BasisPengetahuan", "C"), ("E1", "Ent : ArtikelPengetahuan", "E"), ("E2", "Ent : LogAudit", "E")],
      [("msg", "U", "V", "Klik menu Basis Pengetahuan", "1"),
       ("msg", "V", "C", "muatArtikel()", "1.1"),
       ("msg", "C", "E1", "ambilArtikel()", "1.1.1"),
       ("ret", "E1", "C", "daftarArtikel", "1.1.2"),
       ("ret", "C", "V", "tampilkanDaftar", "1.2"),
       ("msg", "U", "V", "Isi form artikel & klik Simpan", "2"),
       ("msg", "V", "C", "simpanArtikel(data)", "2.1"),
       ("self", "C", "C", "validasi()", "2.1.1"),
       ("msg", "C", "E1", "simpan()", "2.1.2"),
       ("msg", "C", "E1", "indeksUlangFTS()", "2.1.3"),
       ("msg", "C", "E2", "catatLog()", "2.1.4"),
       ("ret", "C", "V", "tampilkanTersimpan", "2.2")])
    S("SD-10 - Mengatur AI dan Anti-ban",
      [("U", "Administrator", "A"), ("V", "View : PengaturanAI", "V"), ("C", "Cont : PengaturanAI", "C"),
       ("AI", "Penyedia AI", "A"), ("E1", "Ent : PengaturanAI", "E"), ("E2", "Ent : PengaturanAntiBan", "E"),
       ("E3", "Ent : LogAudit", "E")],
      [("msg", "U", "V", "Klik menu Pengaturan AI", "1"),
       ("msg", "V", "C", "muatPengaturan()", "1.1"),
       ("msg", "C", "E1", "ambilPengaturanAI()", "1.1.1"),
       ("msg", "C", "E2", "ambilPengaturanAntiBan()", "1.1.2"),
       ("ret", "E2", "C", "pengaturan", "1.1.3"),
       ("ret", "C", "V", "tampilkanPengaturan", "1.2"),
       ("msg", "U", "V", "Ubah nilai & klik Simpan", "2"),
       ("msg", "V", "C", "simpanPengaturan(data)", "2.1"),
       ("self", "C", "C", "validasiNilai()", "2.1.1"),
       ("msg", "C", "AI", "ujiKoneksi(kunciAPI)", "2.1.2"),
       ("ret", "AI", "C", "koneksiOK", "2.1.3"),
       ("self", "C", "C", "enkripsiKunci()", "2.1.4"),
       ("msg", "C", "E1", "simpan()", "2.1.5"),
       ("msg", "C", "E2", "simpan()", "2.1.6"),
       ("msg", "C", "E3", "catatLog()", "2.1.7"),
       ("ret", "C", "V", "tampilkanTersimpan", "2.2")])
    S("SD-11 - Mengelola Tim dan Hak Akses",
      [("U", "Administrator", "A"), ("V", "View : TimAkses", "V"), ("C", "Cont : TimAkses", "C"),
       ("E1", "Ent : Pengguna", "E"), ("E2", "Ent : AksesNomor", "E"), ("E3", "Ent : LogAudit", "E")],
      [("msg", "U", "V", "Klik menu Tim & Akses", "1"),
       ("msg", "V", "C", "muatPengguna()", "1.1"),
       ("msg", "C", "E1", "ambilPengguna()", "1.1.1"),
       ("ret", "E1", "C", "daftarPengguna", "1.1.2"),
       ("ret", "C", "V", "tampilkanDaftar", "1.2"),
       ("msg", "U", "V", "Isi form & akses nomor, klik Simpan", "2"),
       ("msg", "V", "C", "simpanPengguna(data, akses)", "2.1"),
       ("msg", "C", "E1", "cekEmailUnik(email)", "2.1.1"),
       ("ret", "E1", "C", "unik", "2.1.2"),
       ("msg", "C", "E1", "simpan()", "2.1.3"),
       ("msg", "C", "E2", "simpanAkses()", "2.1.4"),
       ("msg", "C", "E3", "catatLog()", "2.1.5"),
       ("ret", "C", "V", "tampilkanTersimpan", "2.2")])
    S("SD-12 - Melihat Log Audit",
      [("U", "Supervisor/Administrator", "A"), ("V", "View : LogAudit", "V"), ("C", "Cont : LogAudit", "C"),
       ("E1", "Ent : LogAudit", "E")],
      [("msg", "U", "V", "Klik menu Log Audit", "1"),
       ("msg", "V", "C", "muatLog()", "1.1"),
       ("msg", "C", "E1", "ambilTerbaru()", "1.1.1"),
       ("ret", "E1", "C", "daftarLog", "1.1.2"),
       ("ret", "C", "V", "tampilkanLog", "1.2"),
       ("msg", "U", "V", "Isi filter pelaku, aksi & tanggal", "2"),
       ("msg", "V", "C", "filterLog(pelaku, aksi, tanggal)", "2.1"),
       ("msg", "C", "E1", "cari()", "2.1.1"),
       ("ret", "E1", "C", "hasil", "2.1.2"),
       ("ret", "C", "V", "tampilkanHasil", "2.2")])


# --------------------------------------------------------------------------- class (MVC)
UI = [
    ("UI:Login", ["Email", "Password"]),
    ("UI:Dashboard", ["NomorTerpilih", "Periode"]),
    ("UI:KotakMasuk", ["PercakapanTerpilih", "IsiBalasan"]),
    ("UI:Prospek", ["TahapFilter", "ProspekTerpilih", "Catatan"]),
    ("UI:Kontak", ["KataKunci", "DataKontak"]),
    ("UI:NomorWhatsApp", ["Label", "Nomor", "Tujuan"]),
    ("UI:BasisPengetahuan", ["Judul", "Kategori", "Isi", "Label"]),
    ("UI:PengaturanAI", ["Penyedia", "KunciAPI", "AmbangKeyakinan", "KataKunciEskalasi", "BatasPerJam"]),
    ("UI:TimAkses", ["Nama", "Email", "Peran", "AksesNomor"]),
    ("UI:LogAudit", ["FilterPelaku", "FilterAksi", "RentangTanggal"]),
    ("UI:WhatsAppGateway", ["NomorPengirim", "IsiPesan"]),
]
CONT = [
    ("Cont:Login", ["validasiLogin", "ambilAksesNomor", "catatLogin"]),
    ("Cont:Dashboard", ["muatDashboard", "filterPeriode", "hitungMetrik"]),
    ("Cont:Percakapan", ["terimaPesan", "muatPercakapan", "kirimBalasan", "ambilAlih", "selesaikan"]),
    ("Cont:Prospek", ["muatProspek", "ubahTahap", "tambahAktivitas", "hitungSkor"]),
    ("Cont:Kontak", ["cariKontak", "simpanKontak"]),
    ("Cont:NomorWA", ["tambahNomor", "buatQR", "cekStatus", "putuskan"]),
    ("Cont:BasisPengetahuan", ["simpanArtikel", "indeksUlang", "ujiPencarian"]),
    ("Cont:PengaturanAI", ["simpanPengaturan", "enkripsiKunci", "ujiKeputusan"]),
    ("Cont:TimAkses", ["simpanPengguna", "aturAksesNomor", "nonaktifkan"]),
    ("Cont:LogAudit", ["muatLog", "filterLog"]),
    ("Cont:AIEngine", ["klasifikasiMaksud", "ekstrakEntitas", "cariArtikel", "susunJawaban", "hitungKeyakinan", "eskalasi"]),
    ("Cont:AntiBan", ["nilaiPesan", "antrekan", "kirimAntrean", "catatInsiden"]),
]
ENT = [
    ("Ent:Pengguna", ["idPengguna", "nama", "email", "passwordHash", "peran", "status"]),
    ("Ent:AksesNomor", ["idPengguna", "idNomor", "level"]),
    ("Ent:MetrikHarian", ["idNomor", "tanggal", "pesanMasuk", "pesanKeluar", "balasanAI", "balasanManusia", "belumDibalas", "rataWaktuBalas", "prospekBaru", "konversi"]),
    ("Ent:Percakapan", ["idPercakapan", "idKontak", "idNomor", "status", "penangan", "idAgen", "belumDibaca", "waktuBalasPertama"]),
    ("Ent:Pesan", ["idPesan", "idPercakapan", "arah", "jenisPengirim", "isi", "status", "metaAI"]),
    ("Ent:Prospek", ["idProspek", "idKontak", "tahap", "skor", "rincianSkor", "idPemilik", "tindakLanjutBerikut"]),
    ("Ent:AktivitasProspek", ["idAktivitas", "idProspek", "idPengguna", "jenis", "catatan", "waktu"]),
    ("Ent:Kontak", ["idKontak", "nomor", "nama", "jenjang", "kelas", "mapel", "kota", "sumber", "label"]),
    ("Ent:NomorWhatsApp", ["idNomor", "label", "nomor", "tujuan", "status", "modeAI", "skorKesehatan"]),
    ("Ent:ArtikelPengetahuan", ["idArtikel", "judul", "kategori", "isi", "label", "aktif"]),
    ("Ent:PengaturanAI", ["idNomor", "penyedia", "kunciAPITerenkripsi", "persona", "ambangKeyakinan", "kataKunciEskalasi"]),
    ("Ent:LogAudit", ["idLog", "idPengguna", "aksi", "entitas", "idEntitas", "detail", "waktu"]),
    ("Ent:PengaturanAntiBan", ["batasPerMenit", "batasPerJam", "batasPerHari", "jedaMin", "jedaMaks", "jamAktif"]),
    ("Ent:AntreanKeluar", ["idAntrean", "idPesan", "prioritas", "status", "skorRisiko", "keputusan", "jadwalKirim"]),
    ("Ent:Insiden", ["idInsiden", "idNomor", "jenis", "tingkat", "rencanaPemulihan", "status"]),
]
UI_CONT = {
    "UI:Login": ["Cont:Login"], "UI:Dashboard": ["Cont:Dashboard"], "UI:KotakMasuk": ["Cont:Percakapan"],
    "UI:Prospek": ["Cont:Prospek"], "UI:Kontak": ["Cont:Kontak"], "UI:NomorWhatsApp": ["Cont:NomorWA"],
    "UI:BasisPengetahuan": ["Cont:BasisPengetahuan"], "UI:PengaturanAI": ["Cont:PengaturanAI"],
    "UI:TimAkses": ["Cont:TimAkses"], "UI:LogAudit": ["Cont:LogAudit"], "UI:WhatsAppGateway": ["Cont:Percakapan"],
}
CONT_ENT = {
    "Cont:Login": ["Ent:Pengguna", "Ent:AksesNomor", "Ent:LogAudit"],
    "Cont:Dashboard": ["Ent:MetrikHarian", "Ent:NomorWhatsApp"],
    "Cont:Percakapan": ["Ent:Kontak", "Ent:Percakapan", "Ent:Pesan", "Ent:Prospek"],
    "Cont:Prospek": ["Ent:Prospek", "Ent:AktivitasProspek"],
    "Cont:Kontak": ["Ent:Kontak"],
    "Cont:NomorWA": ["Ent:NomorWhatsApp"],
    "Cont:BasisPengetahuan": ["Ent:ArtikelPengetahuan"],
    "Cont:PengaturanAI": ["Ent:PengaturanAI", "Ent:PengaturanAntiBan"],
    "Cont:TimAkses": ["Ent:Pengguna", "Ent:AksesNomor"],
    "Cont:LogAudit": ["Ent:LogAudit"],
    "Cont:AIEngine": ["Ent:ArtikelPengetahuan", "Ent:PengaturanAI", "Ent:Prospek"],
    "Cont:AntiBan": ["Ent:AntreanKeluar", "Ent:PengaturanAntiBan", "Ent:Insiden"],
}
ROW = 15  # VP row height for attributes/operations
HEAD = 24


CD_PARTS = [
    ("Class Diagram SAPA (MVC) Bagian 1 - Layanan Percakapan dan CRM",
     ["UI:Login", "UI:Dashboard", "UI:KotakMasuk", "UI:WhatsAppGateway", "UI:Prospek", "UI:Kontak"],
     ["Cont:Login", "Cont:Dashboard", "Cont:Percakapan", "Cont:Prospek", "Cont:Kontak", "Cont:AIEngine", "Cont:AntiBan"]),
    ("Class Diagram SAPA (MVC) Bagian 2 - Pengelolaan Sistem",
     ["UI:NomorWhatsApp", "UI:BasisPengetahuan", "UI:PengaturanAI", "UI:TimAkses", "UI:LogAudit"],
     ["Cont:NomorWA", "Cont:BasisPengetahuan", "Cont:PengaturanAI", "Cont:TimAkses", "Cont:LogAudit"]),
]


def class_diagrams():
    """The full MVC diagram is too tall for one page, so it is split by module."""
    for name, uis, conts in CD_PARTS:
        ents = []
        for c in conts:
            for e in CONT_ENT[c]:
                if e not in ents:
                    ents.append(e)
        order = [e for e, _ in ENT]
        ents.sort(key=order.index)
        class_diagram(name, [u for u in UI if u[0] in uis], [c for c in CONT if c[0] in conts],
                      [e for e in ENT if e[0] in ents])


def class_diagram(title="Class Diagram SAPA (MVC)", UI=UI, CONT=CONT, ENT=ENT):
    emit("DIAGRAM", "class", title)
    ids = {}

    def column(items, x, kind, gap):
        y = 20
        for name, members in items:
            cid = "c" + str(len(ids))
            ids[name] = cid
            if kind == "UI":
                lines = [m for m in members] + [f"getX" for m in members] * 2
                w = max(tw(name) + 20, max(tw(f"+set{m}({m}) : void") for m in members) + 10)
                h = HEAD + ROW * 3 * len(members) + 6
            elif kind == "Cont":
                w = max(tw(name) + 20, max(tw(f"+{m}()") for m in members) + 10)
                h = HEAD + ROW * len(members) + 10
            else:
                w = max(tw(name) + 20, max(tw(f"-{m}") for m in members) + 10)
                h = HEAD + ROW * len(members) + 10
            emit("SHAPE", cid, "class", x, y, w, h, name)
            for m in members:
                if kind == "UI":
                    emit("ATTR", cid, m)
                elif kind == "Ent":
                    emit("ATTR", cid, m)
            if kind == "UI":
                for m in members:
                    emit("OP", cid, f"get{m}", "", "")
                    emit("OP", cid, f"set{m}", m, "void")
            elif kind == "Cont":
                for m in members:
                    emit("OP", cid, m, "", "")
            y += h + gap

    column(UI, 20, "UI", 22)
    column(CONT, 520, "Cont", 48)
    column(ENT, 920, "Ent", 20)
    for ui, conts in UI_CONT.items():
        for c in conts:
            if ui in ids and c in ids:
                emit("CONN", "assoc", ids[ui], ids[c])
    for c, ents in CONT_ENT.items():
        for e in ents:
            if c in ids and e in ids:
                emit("CONN", "assoc", ids[c], ids[e])


# --------------------------------------------------------------------------- activity
LANE_A_W, LANE_S_W = 320, 560
ACT_W = 190


class Node:
    def __init__(self, nid, lane, row, col, kind, text):
        self.id, self.lane, self.row, self.col, self.kind, self.text = nid, lane, row, col, kind, text
        if kind == "action":
            lines = max(1, math.ceil(tw(text) / (ACT_W - 16)))
            self.w, self.h = ACT_W, max(40, lines * 15 + 16)
        elif kind == "decision":
            self.w = self.h = 34
        else:
            self.w = self.h = 24
        if lane == "A":
            cx = 20 + LANE_A_W // 2 + col * 200
        else:
            cx = 20 + LANE_A_W + (170 if col == 0 else 420)
        cy = 90 + row * 82
        self.cx, self.cy = cx, cy
        self.x, self.y = cx - self.w // 2, cy - self.h // 2

    @property
    def right(self):
        return self.x + self.w

    @property
    def bottom(self):
        return self.y + self.h


def activity(name, lane_a, nodes, edges, lane_s="Sistem SAPA"):
    emit("DIAGRAM", "activity", name)
    N = {}
    for nid, lane, row, col, kind, text in nodes:
        N[nid] = Node(nid, lane, row, col, kind, text)
    height = max(n.bottom for n in N.values()) + 50
    emit("SHAPE", "pa", "partition", 20, 20, LANE_A_W, height, lane_a)
    emit("SHAPE", "ps", "partition", 20 + LANE_A_W, 20, LANE_S_W, height, lane_s)
    for n in N.values():
        emit("SHAPE", n.id, n.kind, n.x, n.y, n.w, n.h, n.text)
    for e in edges:
        a, b, guard = e[:3]
        s, t = N[a], N[b]
        pts, cap = route(s, t)
        if len(e) > 3:  # explicit route for loops that would otherwise cross boxes
            pts = e[3]
            cap = (pts[0][0] + 6, pts[0][1] - 18)
        emit("CONN", "flow", a, b, guard, "", "", ";".join(f"{x},{y}" for x, y in pts),
             f"{cap[0]},{cap[1]}" if guard else "")


def route(s, t):
    if t.row == s.row:  # side branch on the same row
        if t.cx > s.cx:
            pts = [(s.right, s.cy), (t.x, t.cy)]
            cap = (s.right + 6, s.cy - 18)
        else:
            pts = [(s.x, s.cy), (t.right, t.cy)]
            cap = (t.right + 6, s.cy - 18)
    elif t.row > s.row:
        if abs(s.cx - t.cx) < 4:
            pts = [(s.cx, s.bottom), (t.cx, t.y)]
            cap = (s.cx + 6, s.bottom + 2)
        elif t.row > s.row + 1 and (s.col == 1 or (s.kind == "decision" and t.col == 1)):
            # long drop: run down the outer edge of the Sistem lane so no box is crossed
            dec = s.kind == "decision"
            xr = 20 + LANE_A_W + LANE_S_W - (12 if dec else 30)
            sy, ty = s.cy + (0 if dec else 8), t.cy - (8 if dec else 0)
            pts = [(s.right, sy), (xr, sy), (xr, ty), (t.right, ty)]
            cap = (s.right + 6, s.cy - 18)
        elif s.kind == "decision" and t.cx > s.cx:
            # branch: leave the decision sideways, then drop into the target top
            pts = [(s.right, s.cy), (t.cx, s.cy), (t.cx, t.y)]
            cap = (s.right + 6, s.cy - 18)
        else:
            # leave the source downward, then run horizontally into the target side
            tx = t.x if t.cx > s.cx else t.right
            pts = [(s.cx, s.bottom), (s.cx, t.cy), (tx, t.cy)]
            cap = (s.cx + 6, s.bottom + 2)
    else:  # loop back upward along the right of both nodes
        # loop back upward and enter the target from above so it never merges with another arrow
        xr = max(s.right, t.right) + 22
        ty = t.y - 14
        pts = [(s.right, s.cy), (xr, s.cy), (xr, ty), (t.cx + 40, ty), (t.cx + 40, t.y)]
        cap = (s.right + 6, s.cy - 18)
    return pts, cap


def activities():
    A = activity
    A("AD-01 - Login", "Pengguna", [
        ("i", "A", 0, 0, "initial", ""),
        ("a1", "A", 1, 0, "action", "Membuka halaman Login"),
        ("s1", "S", 2, 0, "action", "Menampilkan form email dan password"),
        ("a2", "A", 3, 0, "action", "Mengisi email dan password, klik Masuk"),
        ("s2", "S", 4, 0, "action", "Memvalidasi kredensial"),
        ("d1", "S", 5, 0, "decision", ""),
        ("e1", "S", 5, 1, "action", "Menampilkan \"Email atau password salah\""),
        ("d2", "S", 6, 0, "decision", ""),
        ("e2", "S", 6, 1, "action", "Menampilkan \"Akun Anda dinonaktifkan\""),
        ("f2", "S", 7, 1, "final", ""),
        ("s3", "S", 7, 0, "action", "Mengambil peran dan akses nomor"),
        ("s4", "S", 8, 0, "action", "Mencatat log audit login"),
        ("s5", "S", 9, 0, "action", "Menampilkan halaman sesuai peran"),
        ("f", "S", 10, 0, "final", ""),
    ], [("i", "a1", ""), ("a1", "s1", ""), ("s1", "a2", ""), ("a2", "s2", ""), ("s2", "d1", ""),
        ("d1", "d2", "kredensial valid"), ("d1", "e1", "kredensial salah"), ("e1", "a2", ""),
        ("d2", "s3", "akun aktif"), ("d2", "e2", "akun nonaktif"), ("e2", "f2", ""),
        ("s3", "s4", ""), ("s4", "s5", ""), ("s5", "f", "")])
    A("AD-02 - Mengirim Pesan WhatsApp", "Pelanggan", [
        ("i", "A", 0, 0, "initial", ""),
        ("a1", "A", 1, 0, "action", "Mengirim pesan ke nomor WhatsApp Asentra"),
        ("s1", "S", 2, 0, "action", "Menerima pesan melalui gerbang WhatsApp Web"),
        ("s2", "S", 3, 0, "action", "Mencari kontak berdasarkan nomor pengirim"),
        ("d1", "S", 4, 0, "decision", ""),
        ("s3", "S", 4, 1, "action", "Membuat kontak dan prospek tahap \"baru\""),
        ("s4", "S", 5, 0, "action", "Membuka percakapan dan menyimpan pesan"),
        ("d2", "S", 6, 0, "decision", ""),
        ("s5", "S", 6, 1, "action", "Menandai percakapan \"belum dibalas\" untuk agen"),
        ("f2", "S", 7, 1, "final", ""),
        ("s6", "S", 7, 0, "action", "Menjalankan UC-03 Menjawab Pesan Otomatis dengan AI"),
        ("a2", "A", 8, 0, "action", "Menerima balasan di WhatsApp"),
        ("f", "A", 9, 0, "final", ""),
    ], [("i", "a1", ""), ("a1", "s1", ""), ("s1", "s2", ""), ("s2", "d1", ""),
        ("d1", "s4", "kontak sudah ada"), ("d1", "s3", "kontak baru"), ("s3", "s4", ""),
        ("s4", "d2", ""), ("d2", "s6", "ditangani AI"), ("d2", "s5", "ditangani manusia"), ("s5", "f2", ""),
        ("s6", "a2", ""), ("a2", "f", "")])
    A("AD-03 - Menjawab Pesan Otomatis dengan AI", "Penyedia AI / WhatsApp Web", [
        ("i", "S", 0, 0, "initial", ""),
        ("s1", "S", 1, 0, "action", "Mengklasifikasi maksud dan mengekstrak entitas"),
        ("s2", "S", 2, 0, "action", "Memperbarui kontak dan skor prioritas"),
        ("s3", "S", 3, 0, "action", "Mencari artikel basis pengetahuan (FTS5)"),
        ("d1", "S", 4, 0, "decision", ""),
        ("x1", "A", 5, 0, "action", "Penyedia AI menyusun jawaban dari artikel"),
        ("d2", "S", 6, 0, "decision", ""),
        ("s4", "S", 6, 1, "action", "Menyusun jawaban dengan mode aturan bawaan"),
        ("s5", "S", 7, 0, "action", "Menghitung nilai keyakinan"),
        ("d3", "S", 8, 0, "decision", ""),
        ("esc", "S", 8, 1, "action", "Mengalihkan percakapan ke agen dan mengirim pemberitahuan"),
        ("s6", "S", 9, 0, "action", "Menilai pesan dengan mesin anti-ban"),
        ("d4", "S", 10, 0, "decision", ""),
        ("s7", "S", 10, 1, "action", "Menyimpan di antrean dan mencatat di Pusat Risiko"),
        ("x2", "A", 11, 0, "action", "WhatsApp Web mengirim balasan beserta sumber"),
        ("s8", "S", 12, 0, "action", "Mencatat jejak keputusan AI dan metrik harian"),
        ("f", "S", 13, 0, "final", ""),
    ], [("i", "s1", ""), ("s1", "s2", ""), ("s2", "s3", ""), ("s3", "d1", ""),
        ("d1", "x1", "artikel ditemukan"), ("d1", "esc", "tidak ada artikel"), ("x1", "d2", ""),
        ("d2", "s5", "berhasil"), ("d2", "s4", "gagal/timeout"), ("s4", "s5", ""),
        ("s5", "d3", ""), ("d3", "s6", "yakin"), ("d3", "esc", "di bawah ambang"),
        ("esc", "s8", ""), ("s6", "d4", ""), ("d4", "x2", "kirim"), ("d4", "s7", "tunda/tahan"),
        ("s7", "s8", ""), ("x2", "s8", ""), ("s8", "f", "")])
    A("AD-04 - Mengelola Percakapan", "Agen/CS", [
        ("i", "A", 0, 0, "initial", ""),
        ("a1", "A", 1, 0, "action", "Memilih menu Kotak Masuk"),
        ("s1", "S", 2, 0, "action", "Menampilkan daftar percakapan dari nomor yang diizinkan"),
        ("a2", "A", 3, 0, "action", "Memilih percakapan"),
        ("d1", "S", 4, 0, "decision", ""),
        ("s2", "S", 4, 1, "action", "Menolak: \"Anda tidak memiliki akses ke nomor ini\""),
        ("f2", "S", 5, 1, "final", ""),
        ("s3", "S", 5, 0, "action", "Menampilkan riwayat, jawaban AI, dan jejak keputusan"),
        ("a3", "A", 6, 0, "action", "Mengambil alih, menulis balasan, klik Kirim"),
        ("s4", "S", 7, 0, "action", "Menghentikan AI untuk percakapan ini"),
        ("s5", "S", 8, 0, "action", "Menilai pesan dengan mesin anti-ban"),
        ("d2", "S", 9, 0, "decision", ""),
        ("s6", "S", 9, 1, "action", "Menampilkan \"Pesan ditunda oleh pengaman pengiriman\""),
        ("s7", "S", 10, 0, "action", "Mengirim balasan melalui antrean keluar"),
        ("s8", "S", 11, 0, "action", "Memperbarui status, metrik, dan log audit"),
        ("f", "S", 12, 0, "final", ""),
    ], [("i", "a1", ""), ("a1", "s1", ""), ("s1", "a2", ""), ("a2", "d1", ""),
        ("d1", "s3", "akses diizinkan"), ("d1", "s2", "tidak diizinkan"), ("s2", "f2", ""),
        ("s3", "a3", ""), ("a3", "s4", ""), ("s4", "s5", ""), ("s5", "d2", ""),
        ("d2", "s7", "kirim"), ("d2", "s6", "tunda/tahan"), ("s6", "s8", ""), ("s7", "s8", ""), ("s8", "f", "")])
    A("AD-05 - Mengelola Prospek", "Agen/CS", [
        ("i", "A", 0, 0, "initial", ""),
        ("a1", "A", 1, 0, "action", "Memilih menu Prospek"),
        ("s1", "S", 2, 0, "action", "Menampilkan papan prospek per tahap urut skor"),
        ("a2", "A", 3, 0, "action", "Memilih kartu prospek"),
        ("s2", "S", 4, 0, "action", "Menampilkan detail, rincian skor, dan riwayat aktivitas"),
        ("a3", "A", 5, 0, "action", "Mengubah tahap, mengisi catatan dan tanggal tindak lanjut, klik Simpan"),
        ("d1", "S", 6, 0, "decision", ""),
        ("s3", "S", 6, 1, "action", "Menampilkan \"Catatan wajib diisi\""),
        ("s4", "S", 7, 0, "action", "Menyimpan perubahan dan menghitung ulang skor"),
        ("d2", "S", 8, 0, "decision", ""),
        ("s5", "S", 8, 1, "action", "Menambah hitungan konversi"),
        ("s6", "S", 9, 0, "action", "Mencatat log audit"),
        ("f", "S", 10, 0, "final", ""),
    ], [("i", "a1", ""), ("a1", "s1", ""), ("s1", "a2", ""), ("a2", "s2", ""), ("s2", "a3", ""),
        ("a3", "d1", ""), ("d1", "s4", "catatan terisi"), ("d1", "s3", "catatan kosong"), ("s3", "a3", ""),
        ("s4", "d2", ""), ("d2", "s6", "tahap lain"), ("d2", "s5", "tahap = daftar"), ("s5", "s6", ""),
        ("s6", "f", "")])
    A("AD-06 - Mengelola Kontak Pelanggan", "Agen/CS", [
        ("i", "A", 0, 0, "initial", ""),
        ("a1", "A", 1, 0, "action", "Memilih menu Kontak dan mengetik kata kunci"),
        ("s1", "S", 2, 0, "action", "Mencari kontak"),
        ("d1", "S", 3, 0, "decision", ""),
        ("s2", "S", 3, 1, "action", "Menampilkan \"Kontak tidak ditemukan\""),
        ("f2", "S", 4, 1, "final", ""),
        ("s3", "S", 4, 0, "action", "Menampilkan daftar kontak"),
        ("a2", "A", 5, 0, "action", "Memilih kontak, klik Ubah"),
        ("s4", "S", 6, 0, "action", "Menampilkan form data dan riwayat percakapan"),
        ("a3", "A", 7, 0, "action", "Memperbarui data, klik Simpan"),
        ("d2", "S", 8, 0, "decision", ""),
        ("s5", "S", 8, 1, "action", "Menandai kolom yang salah"),
        ("s6", "S", 9, 0, "action", "Menyimpan perubahan dan mencatat log audit"),
        ("f", "S", 10, 0, "final", ""),
    ], [("i", "a1", ""), ("a1", "s1", ""), ("s1", "d1", ""), ("d1", "s3", "ditemukan"),
        ("d1", "s2", "tidak ditemukan"), ("s2", "f2", ""), ("s3", "a2", ""), ("a2", "s4", ""),
        ("s4", "a3", ""), ("a3", "d2", ""), ("d2", "s6", "data valid"), ("d2", "s5", "tidak valid"),
        ("s5", "a3", ""), ("s6", "f", "")])
    A("AD-07 - Melihat Dashboard Pemantauan", "Supervisor / Administrator", [
        ("i", "A", 0, 0, "initial", ""),
        ("a1", "A", 1, 0, "action", "Memilih menu Dashboard"),
        ("s1", "S", 2, 0, "action", "Mengambil metrik harian dan status nomor yang diizinkan"),
        ("s2", "S", 3, 0, "action", "Menampilkan kartu ringkasan, grafik, dan status nomor"),
        ("a2", "A", 4, 0, "action", "Memilih filter nomor dan periode"),
        ("s3", "S", 5, 0, "action", "Menghitung ulang metrik sesuai filter"),
        ("d1", "S", 6, 0, "decision", ""),
        ("s4", "S", 6, 1, "action", "Menampilkan \"Belum ada data pada periode ini\""),
        ("s5", "S", 7, 0, "action", "Menampilkan hasil filter"),
        ("f", "S", 8, 0, "final", ""),
    ], [("i", "a1", ""), ("a1", "s1", ""), ("s1", "s2", ""), ("s2", "a2", ""), ("a2", "s3", ""),
        ("s3", "d1", ""), ("d1", "s5", "ada data"), ("d1", "s4", "tidak ada data"), ("s4", "f", ""),
        ("s5", "f", "")])
    A("AD-08 - Mengelola Nomor WhatsApp", "Administrator", [
        ("i", "A", 0, 0, "initial", ""),
        ("a1", "A", 1, 0, "action", "Memilih menu Nomor WhatsApp, klik Tambah Nomor"),
        ("s1", "S", 2, 0, "action", "Menampilkan form label, nomor, dan tujuan"),
        ("a2", "A", 3, 0, "action", "Mengisi form, klik Tautkan"),
        ("s2", "S", 4, 0, "action", "Membuat sesi WhatsApp Web dan menampilkan kode QR"),
        ("a3", "A", 5, 0, "action", "Memindai kode QR dari ponsel"),
        ("d1", "S", 6, 0, "decision", ""),
        ("s3", "S", 6, 1, "action", "Menampilkan \"QR kedaluwarsa\" dan tombol Buat ulang"),
        ("d2", "S", 7, 0, "decision", ""),
        ("s4", "S", 7, 1, "action", "Status \"gagal tertaut\" dan dicatat di Pusat Risiko"),
        ("f2", "S", 8, 1, "final", ""),
        ("s5", "S", 8, 0, "action", "Menyimpan sesi, status \"tersambung\", dan log audit"),
        ("f", "S", 9, 0, "final", ""),
    ], [("i", "a1", ""), ("a1", "s1", ""), ("s1", "a2", ""), ("a2", "s2", ""), ("s2", "a3", ""),
        ("a3", "d1", ""), ("d1", "d2", "QR berlaku"), ("d1", "s3", "kedaluwarsa"), ("s3", "s2", ""),
        ("d2", "s5", "tertaut"), ("d2", "s4", "gagal"), ("s4", "f2", ""), ("s5", "f", "")])
    A("AD-09 - Mengelola Basis Pengetahuan", "Supervisor / Administrator", [
        ("i", "A", 0, 0, "initial", ""),
        ("a1", "A", 1, 0, "action", "Memilih menu Basis Pengetahuan"),
        ("s1", "S", 2, 0, "action", "Menampilkan daftar artikel per kategori"),
        ("a2", "A", 3, 0, "action", "Klik Tambah Artikel atau memilih artikel"),
        ("s2", "S", 4, 0, "action", "Menampilkan form artikel"),
        ("a3", "A", 5, 0, "action", "Mengisi judul, kategori, isi, label, klik Simpan"),
        ("d1", "S", 6, 0, "decision", ""),
        ("s3", "S", 6, 1, "action", "Menampilkan \"Judul dan isi wajib diisi\""),
        ("s4", "S", 7, 0, "action", "Menyimpan artikel dan mengindeks ulang FTS5"),
        ("s5", "S", 8, 0, "action", "Mencatat log audit"),
        ("f", "S", 9, 0, "final", ""),
    ], [("i", "a1", ""), ("a1", "s1", ""), ("s1", "a2", ""), ("a2", "s2", ""), ("s2", "a3", ""),
        ("a3", "d1", ""), ("d1", "s4", "lengkap"), ("d1", "s3", "kosong"), ("s3", "a3", ""),
        ("s4", "s5", ""), ("s5", "f", "")])
    A("AD-10 - Mengatur AI dan Anti-ban", "Administrator", [
        ("i", "A", 0, 0, "initial", ""),
        ("a1", "A", 1, 0, "action", "Memilih menu Pengaturan AI"),
        ("s1", "S", 2, 0, "action", "Menampilkan pengaturan AI, anti-ban, antrean, dan Pusat Risiko"),
        ("a2", "A", 3, 0, "action", "Mengubah penyedia, kunci API, ambang, kata kunci, dan batas kirim"),
        ("a3", "A", 4, 0, "action", "Klik Simpan"),
        ("d1", "S", 5, 0, "decision", ""),
        ("s2", "S", 5, 1, "action", "Menolak dan menandai kolom yang salah"),
        ("s3", "S", 6, 0, "action", "Menguji koneksi penyedia AI"),
        ("d2", "S", 7, 0, "decision", ""),
        ("s4", "S", 7, 1, "action", "Menampilkan \"Kunci API ditolak penyedia\""),
        ("s5", "S", 8, 0, "action", "Mengenkripsi kunci API (enkripsi Laravel)"),
        ("s6", "S", 9, 0, "action", "Menyimpan pengaturan dan mencatat log audit"),
        ("f", "S", 10, 0, "final", ""),
    ], [("i", "a1", ""), ("a1", "s1", ""), ("s1", "a2", ""), ("a2", "a3", ""), ("a3", "d1", ""),
        ("d1", "s3", "nilai wajar"), ("d1", "s2", "tidak wajar"), ("s2", "a2", ""),
        ("s3", "d2", ""), ("d2", "s5", "diterima"), ("d2", "s4", "ditolak"), ("s4", "a2", ""),
        ("s5", "s6", ""), ("s6", "f", "")])
    A("AD-11 - Mengelola Tim dan Hak Akses", "Administrator", [
        ("i", "A", 0, 0, "initial", ""),
        ("a1", "A", 1, 0, "action", "Memilih menu Tim & Akses"),
        ("s1", "S", 2, 0, "action", "Menampilkan daftar pengguna, peran, dan akses nomor"),
        ("a2", "A", 3, 0, "action", "Klik Tambah Pengguna atau memilih pengguna"),
        ("s2", "S", 4, 0, "action", "Menampilkan form dan matriks akses per nomor"),
        ("a3", "A", 5, 0, "action", "Mengisi data, memilih level akses, klik Simpan"),
        ("d1", "S", 6, 0, "decision", ""),
        ("s3", "S", 6, 1, "action", "Menampilkan \"Email sudah digunakan\""),
        ("s4", "S", 7, 0, "action", "Menyimpan pengguna dan akses nomor"),
        ("s5", "S", 8, 0, "action", "Mencatat log audit"),
        ("f", "S", 9, 0, "final", ""),
    ], [("i", "a1", ""), ("a1", "s1", ""), ("s1", "a2", ""), ("a2", "s2", ""), ("s2", "a3", ""),
        ("a3", "d1", ""), ("d1", "s4", "email unik"), ("d1", "s3", "sudah terdaftar"), ("s3", "a3", ""),
        ("s4", "s5", ""), ("s5", "f", "")])
    A("AD-12 - Melihat Log Audit", "Supervisor / Administrator", [
        ("i", "A", 0, 0, "initial", ""),
        ("a1", "A", 1, 0, "action", "Memilih menu Log Audit"),
        ("s1", "S", 2, 0, "action", "Menampilkan log terbaru"),
        ("a2", "A", 3, 0, "action", "Mengisi filter pelaku, aksi, dan tanggal"),
        ("s2", "S", 4, 0, "action", "Mencari log sesuai filter"),
        ("d1", "S", 5, 0, "decision", ""),
        ("s3", "S", 5, 1, "action", "Menampilkan \"Tidak ada aktivitas pada filter ini\""),
        ("s4", "S", 6, 0, "action", "Menampilkan daftar log"),
        ("f", "S", 7, 0, "final", ""),
    ], [("i", "a1", ""), ("a1", "s1", ""), ("s1", "a2", ""), ("a2", "s2", ""), ("s2", "d1", ""),
        ("d1", "s4", "ada hasil"), ("d1", "s3", "tidak ada"), ("s3", "f", ""), ("s4", "f", "")])


# --------------------------------------------------------------------------- SRS additions
def scrum_activity():
    """Scrum cycle of the SAPA project as an activity diagram (PO/stakeholder lane vs development team)."""
    def c(lane, row, col=0):  # centre of a node, same formula as Node
        cx = 20 + LANE_A_W // 2 + col * 200 if lane == "A" else 20 + LANE_A_W + (170 if col == 0 else 420)
        return cx, 90 + row * 82
    d1x, d1y = c("S", 5)
    s2x, s2y = c("S", 3)
    d2x, d2y = c("S", 9)
    a1x, a1y = c("A", 1)
    activity("AD-Scrum - Siklus Scrum Proyek SAPA", "Product Owner dan Stakeholder", [
        ("i", "A", 0, 0, "initial", ""),
        ("a1", "A", 1, 0, "action", "Menyusun dan mengurutkan Product Backlog"),
        ("s1", "S", 2, 0, "action", "Sprint Planning: memilih PBI dan menyusun Sprint Backlog"),
        ("s2", "S", 3, 0, "action", "Mengerjakan PBI dan menguji fitur"),
        ("s3", "S", 4, 0, "action", "Daily Scrum 15 menit"),
        ("d1", "S", 5, 0, "decision", ""),
        ("s4", "S", 6, 0, "action", "Menyiapkan Increment sesuai Definition of Done"),
        ("a2", "A", 7, 0, "action", "Sprint Review: demo Increment dan memberi masukan"),
        ("s5", "S", 8, 0, "action", "Sprint Retrospective"),
        ("d2", "S", 9, 0, "decision", ""),
        ("a3", "A", 10, 0, "action", "Demo akhir dan serah terima kepada mitra"),
        ("f", "A", 11, 0, "final", ""),
    ], [("i", "a1", ""), ("a1", "s1", ""), ("s1", "s2", ""), ("s2", "s3", ""), ("s3", "d1", ""),
        ("d1", "s2", "sprint berjalan", [(d1x + 17, d1y), (d1x + 130, d1y), (d1x + 130, s2y), (s2x + 95, s2y)]),
        ("d1", "s4", "akhir sprint"), ("s4", "a2", ""), ("a2", "s5", ""), ("s5", "d2", ""),
        ("d2", "a1", "sprint berikutnya", [(d2x - 17, d2y), (355, d2y), (355, a1y), (a1x + 95, a1y)]),
        ("d2", "a3", "Sprint 3 selesai"), ("a3", "f", "")],
        lane_s="Tim Pengembang")


def deployment_diagram():
    """System architecture as nested UML nodes, layered like the course example (hardware -> VM -> server -> app)."""
    emit("DIAGRAM", "deployment", "Deployment Diagram Arsitektur SAPA")
    S = lambda *a: emit("SHAPE", *a)
    # clients and external services (top row)
    S("pc", "node", 20, 20, 250, 110, "Perangkat Pengguna (Laptop/PC)", "<<device>>")
    S("br", "component", 40, 70, 210, 44, "Peramban Web")
    emit("PARENT", "br", "pc")
    S("hp", "node", 300, 20, 250, 110, "Ponsel Pelanggan", "<<device>>")
    S("wapp", "component", 320, 70, 210, 44, "Aplikasi WhatsApp")
    emit("PARENT", "wapp", "hp")
    S("wasrv", "node", 600, 20, 250, 110, "Server WhatsApp (Meta)", "<<external>>")
    S("ai", "node", 880, 20, 250, 110, "Penyedia AI (OpenAI / Gemini)", "<<external>>")
    # infrastructure stack
    S("hw", "node", 20, 190, 1110, 510, "Infrastruktur Perangkat Keras Penyedia VPS", "<<device>>")
    S("vps", "node", 40, 240, 1070, 440, "VPS Ubuntu 24.04 LTS (2 vCPU, RAM 2 GB, SSD 40 GB)", "<<virtual machine>>")
    emit("PARENT", "vps", "hw")
    S("web", "node", 60, 290, 600, 370, "Web Server: Nginx + PHP-FPM 8.2", "<<execution environment>>")
    emit("PARENT", "web", "vps")
    S("app", "component", 80, 340, 560, 300, "Aplikasi SAPA (Laravel 12)")
    emit("PARENT", "app", "web")
    mods = [("m1", "Antarmuka Blade + Tailwind CSS"), ("m2", "Autentikasi dan RBAC per Nomor"),
            ("m3", "Modul OLTP: Kotak Masuk, Prospek, Kontak"), ("m4", "Modul OLAP: Dashboard Metrik Harian"),
            ("m5", "Mesin AI (RAG, FTS5) dan Eskalasi"), ("m6", "Mesin Anti-ban dan Queue Worker")]
    for k, (mid, name) in enumerate(mods):
        S(mid, "component", 100 + (k % 2) * 270, 390 + (k // 2) * 90, 250, 60, name)
        emit("PARENT", mid, "app")
    S("node", "node", 690, 290, 400, 200, "Runtime Node.js 22", "<<execution environment>>")
    emit("PARENT", "node", "vps")
    S("gw", "component", 720, 350, 340, 70, "WA Gateway (Baileys)")
    emit("PARENT", "gw", "node")
    S("db", "artifact", 720, 540, 340, 70, "database.sqlite (SQLite + FTS5)", "<<database>>")
    emit("PARENT", "db", "vps")
    C = lambda a, b, label, cap: emit("CONN", "assoc", a, b, label, "", "", "", cap)
    C("pc", "web", "HTTPS", "150,150")
    C("hp", "wasrv", "Internet", "553,50")
    C("gw", "wasrv", "WebSocket WhatsApp Web", "735,150")
    C("app", "gw", "HTTP lokal (JSON)", "646,425")
    C("app", "db", "PDO", "660,555")
    C("app", "ai", "HTTPS REST (JSON)", "930,150")


ERD_TABLES = [  # (id, table, x, y, [(column, type, pk, nullable)])
    ("kontak", "kontak", 20, 20, [("id", "BIGINT", 1, 0), ("nomor_telepon", "VARCHAR(20)", 0, 0), ("nama", "VARCHAR(255)", 0, 1),
        ("jenjang", "VARCHAR(20)", 0, 1), ("kelas", "VARCHAR(20)", 0, 1), ("mapel", "VARCHAR(100)", 0, 1),
        ("kota", "VARCHAR(100)", 0, 1), ("sumber", "VARCHAR(50)", 0, 1), ("label", "VARCHAR(100)", 0, 1)]),
    ("prospek", "prospek", 20, 260, [("id", "BIGINT", 1, 0), ("kontak_id", "BIGINT", 0, 0), ("penanggung_jawab", "BIGINT", 0, 1),
        ("tahap", "VARCHAR(20)", 0, 0), ("skor", "INTEGER", 0, 0), ("rincian_skor", "TEXT", 0, 1),
        ("program", "VARCHAR(100)", 0, 1), ("tindak_lanjut_berikut", "DATE", 0, 1)]),
    ("aktv", "aktivitas_prospek", 20, 490, [("id", "BIGINT", 1, 0), ("prospek_id", "BIGINT", 0, 0), ("user_id", "BIGINT", 0, 0),
        ("jenis", "VARCHAR(30)", 0, 0), ("catatan", "TEXT", 0, 0), ("waktu", "TIMESTAMP", 0, 0)]),
    ("perc", "percakapan", 300, 20, [("id", "BIGINT", 1, 0), ("kontak_id", "BIGINT", 0, 0), ("nomor_whatsapp_id", "BIGINT", 0, 0),
        ("agen_id", "BIGINT", 0, 1), ("status", "VARCHAR(20)", 0, 0), ("penangan", "VARCHAR(10)", 0, 0),
        ("belum_dibaca", "INTEGER", 0, 0), ("waktu_balas_pertama", "INTEGER", 0, 1)]),
    ("pesan", "pesan_whatsapp", 300, 260, [("id", "BIGINT", 1, 0), ("percakapan_id", "BIGINT", 0, 0), ("arah", "VARCHAR(10)", 0, 0),
        ("jenis_pengirim", "VARCHAR(10)", 0, 0), ("isi", "TEXT", 0, 0), ("status", "VARCHAR(20)", 0, 0), ("meta_ai", "TEXT", 0, 1)]),
    ("art", "artikel_pengetahuan", 300, 490, [("id", "BIGINT", 1, 0), ("judul", "VARCHAR(255)", 0, 0), ("kategori", "VARCHAR(50)", 0, 0),
        ("isi", "TEXT", 0, 0), ("label", "VARCHAR(255)", 0, 1), ("aktif", "BOOLEAN", 0, 0)]),
    ("users", "users", 580, 20, [("id", "BIGINT", 1, 0), ("name", "VARCHAR(255)", 0, 0), ("email", "VARCHAR(255)", 0, 0),
        ("password", "VARCHAR(255)", 0, 0), ("role", "VARCHAR(20)", 0, 0), ("status", "VARCHAR(20)", 0, 0)]),
    ("uwa", "user_whatsapp_access", 580, 230, [("id", "BIGINT", 1, 0), ("user_id", "BIGINT", 0, 0),
        ("nomor_whatsapp_id", "BIGINT", 0, 0), ("hak_akses", "VARCHAR(20)", 0, 0)]),
    ("log", "log_audit", 580, 400, [("id", "BIGINT", 1, 0), ("user_id", "BIGINT", 0, 1), ("aksi", "VARCHAR(50)", 0, 0),
        ("entitas", "VARCHAR(50)", 0, 0), ("entitas_id", "BIGINT", 0, 1), ("detail", "TEXT", 0, 1), ("created_at", "TIMESTAMP", 0, 0)]),
    ("nomor", "nomor_whatsapp", 860, 20, [("id", "BIGINT", 1, 0), ("label", "VARCHAR(100)", 0, 0), ("nomor", "VARCHAR(20)", 0, 0),
        ("tujuan", "VARCHAR(10)", 0, 0), ("status", "VARCHAR(20)", 0, 0), ("mode_ai", "VARCHAR(20)", 0, 0),
        ("skor_kesehatan", "INTEGER", 0, 0)]),
    ("pai", "pengaturan_ai", 860, 230, [("id", "BIGINT", 1, 0), ("nomor_whatsapp_id", "BIGINT", 0, 1), ("penyedia", "VARCHAR(50)", 0, 0),
        ("model", "VARCHAR(100)", 0, 0), ("api_key", "TEXT", 0, 1), ("instruksi_persona", "TEXT", 0, 1),
        ("ambang_keyakinan", "DECIMAL", 0, 0), ("kata_kunci_eskalasi", "TEXT", 0, 1), ("jeda_min", "INTEGER", 0, 0),
        ("jeda_max", "INTEGER", 0, 0), ("batas_per_menit", "INTEGER", 0, 0), ("batas_per_jam", "INTEGER", 0, 0),
        ("batas_pesan_harian", "INTEGER", 0, 0), ("jam_mulai", "TIME", 0, 0), ("jam_selesai", "TIME", 0, 0)]),
    ("met", "metrik_harian", 860, 550, [("id", "BIGINT", 1, 0), ("nomor_whatsapp_id", "BIGINT", 0, 0), ("tanggal", "DATE", 0, 0),
        ("pesan_masuk", "INTEGER", 0, 0), ("pesan_keluar", "INTEGER", 0, 0), ("balasan_ai", "INTEGER", 0, 0),
        ("balasan_manusia", "INTEGER", 0, 0), ("belum_dibalas", "INTEGER", 0, 0), ("rata_waktu_balas", "INTEGER", 0, 0),
        ("prospek_baru", "INTEGER", 0, 0), ("konversi", "INTEGER", 0, 0)]),
    ("antre", "antrean_pesan", 1140, 20, [("id", "BIGINT", 1, 0), ("nomor_whatsapp_id", "BIGINT", 0, 0),
        ("pesan_whatsapp_id", "BIGINT", 0, 1), ("penerima", "VARCHAR(20)", 0, 0), ("isi_pesan", "TEXT", 0, 0),
        ("skor_risiko", "INTEGER", 0, 0), ("keputusan", "VARCHAR(10)", 0, 0), ("percobaan", "INTEGER", 0, 0),
        ("jadwal_kirim", "TIMESTAMP", 0, 1), ("terkirim_pada", "TIMESTAMP", 0, 1), ("alasan_penahanan", "TEXT", 0, 1)]),
    ("riw", "riwayat_antrean", 1140, 320, [("id", "BIGINT", 1, 0), ("antrean_pesan_id", "BIGINT", 0, 0),
        ("status_sebelumnya", "VARCHAR(20)", 0, 1), ("status_baru", "VARCHAR(20)", 0, 0), ("keterangan", "TEXT", 0, 1),
        ("diubah_pada", "TIMESTAMP", 0, 0)]),
    ("ins", "insiden_risiko", 1140, 510, [("id", "BIGINT", 1, 0), ("nomor_whatsapp_id", "BIGINT", 0, 0),
        ("jenis_insiden", "VARCHAR(50)", 0, 0), ("tingkat_risiko", "VARCHAR(10)", 0, 0), ("deskripsi", "TEXT", 0, 0),
        ("status", "VARCHAR(20)", 0, 0), ("terjadi_pada", "TIMESTAMP", 0, 0)]),
]
ERD_FK = [("users", "uwa"), ("nomor", "uwa"), ("nomor", "pai"), ("kontak", "perc"), ("nomor", "perc"), ("users", "perc"),
          ("perc", "pesan"), ("kontak", "prospek"), ("users", "prospek"), ("prospek", "aktv"), ("users", "aktv"),
          ("nomor", "antre"), ("pesan", "antre"), ("antre", "riw"), ("nomor", "ins"), ("nomor", "met"), ("users", "log")]


FK_COLS = {"kontak_id", "nomor_whatsapp_id", "agen_id", "percakapan_id", "penanggung_jawab", "prospek_id",
           "user_id", "pesan_whatsapp_id", "antrean_pesan_id"}
ERD_PARTS = [  # (title, grid rows of table ids, relations parent -> child); neighbours in the grid keep lines short
    ("ERD SAPA Bagian 1 - Percakapan dan CRM",
     [["nomor", "perc", "pesan"], ["kontak", "users", None], ["prospek", "aktv", None]],
     [("kontak", "perc"), ("nomor", "perc"), ("users", "perc"), ("perc", "pesan"), ("kontak", "prospek"),
      ("users", "prospek"), ("prospek", "aktv"), ("users", "aktv")]),
    ("ERD SAPA Bagian 2 - Pengelolaan Sistem dan Pengiriman",
     [["log", "users", "pai", "pesan"], [None, "uwa", "nomor", "antre"], ["art", "met", "ins", "riw"]],
     [("users", "uwa"), ("nomor", "uwa"), ("nomor", "pai"), ("nomor", "met"), ("nomor", "antre"),
      ("pesan", "antre"), ("antre", "riw"), ("nomor", "ins"), ("users", "log")]),
]


def erd():
    """Physical data model in class notation (<<table>>, PK/FK, 1 : N relations), split in two for page size.
    VP's native ERD shapes render without column text in headless export, so class notation is used."""
    T = {t[0]: t for t in ERD_TABLES}
    keys = lambda c: ",".join(k for k, ok in (("PK", c == "id"), ("FK", c in FK_COLS)) if ok)

    def size(tid):
        _, name, _, _, cols = T[tid]
        w = max(tw(name) + 40, max(tw(f"+<<{keys(c)}>> {c} : {t}") for c, t, *_ in cols) + 16)
        return w, HEAD + ROW * len(cols) + 12

    for title, grid, fks in ERD_PARTS:
        emit("DIAGRAM", "class", title)
        ncol = max(len(r) for r in grid)
        colw = [max((size(r[j])[0] for r in grid if j < len(r) and r[j]), default=0) for j in range(ncol)]
        y = 20
        for row in grid:
            x, rowh = 20, 0
            for j, tid in enumerate(row):
                if tid:
                    w, h = size(tid)
                    _, name, _, _, cols = T[tid]
                    emit("SHAPE", tid, "class", x, y, w, h, name, "<<table>>")
                    for c, t, pk, nul in cols:
                        emit("TATTR", tid, c, t, keys(c))
                    rowh = max(rowh, h)
                x += colw[j] + 110
            y += rowh + 70
        for a, b in fks:
            emit("CONN", "rel", a, b, "1 : N")


SITEMAP = [  # (id, page, functional requirement code and roles, parent)
    ("login", "Login", "F01", None),
    ("main", "Halaman Utama (menu samping sesuai role)", "F01, F14", "login"),
    ("dash", "Dashboard Pemantauan", "F10: Supervisor, Administrator", "main"),
    ("inbox", "Kotak Masuk", "F02, F04, F05, F07: Agen/CS", "main"),
    ("pros", "Prospek", "F08: Agen/CS", "main"),
    ("kont", "Kontak", "F03, F09: Agen/CS", "main"),
    ("nomor", "Nomor WhatsApp", "F11: Administrator", "main"),
    ("kb", "Basis Pengetahuan", "F12: Supervisor, Administrator", "main"),
    ("ai", "Pengaturan AI dan Konsol Uji", "F13: Administrator", "main"),
    ("risk", "Antrean Keluar dan Pusat Risiko", "F06: Administrator", "main"),
    ("tim", "Tim dan Akses", "F14: Administrator", "main"),
    ("log", "Log Audit", "F15: Supervisor, Administrator", "main"),
    ("inbox2", "Detail Percakapan", "F07", "inbox"),
    ("pros2", "Detail Prospek", "F08", "pros"),
    ("kont2", "Form Ubah Kontak", "F09", "kont"),
    ("nomor2", "Tautkan Nomor (Kode QR)", "F11", "nomor"),
    ("kb2", "Form Artikel dan Uji Pencarian", "F12", "kb"),
    ("tim2", "Form Pengguna dan Matriks Akses", "F14", "tim"),
]


def sitemap():
    """Sitemap as a class diagram of <<page>> classes (web application extension notation)."""
    emit("DIAGRAM", "class", "Sitemap SAPA")
    # left-to-right tree so the figure fits a portrait page: Login -> Halaman Utama -> pages -> sub-pages
    kids = [s for s in SITEMAP if s[3] == "main"]
    step, bh = 74, 56
    mid = 20 + (len(kids) - 1) * step // 2
    emit("SHAPE", "login", "class", 20, mid, 150, bh, "Login\\n[F01]", "<<page>>")
    emit("SHAPE", "main", "class", 220, mid, 230, bh, "Halaman Utama\\n(menu samping sesuai role)", "<<page>>")
    emit("CONN", "assoc", "login", "main", "")
    ys = {}
    for k, (pid, name, code, _) in enumerate(kids):
        y = 20 + k * step
        ys[pid] = y
        emit("SHAPE", pid, "class", 520, y, 290, bh, f"{name}\\n[{code}]", "<<page>>")
        emit("CONN", "assoc", "main", pid, "")
    for pid, name, code, parent in SITEMAP:
        if parent not in ys:
            continue
        emit("SHAPE", pid, "class", 870, ys[parent], 270, bh, f"{name}\\n[{code}]", "<<page>>")
        emit("CONN", "assoc", parent, pid, "")


if __name__ == "__main__":
    which = sys.argv[2] if len(sys.argv) > 2 else "all"
    if which in ("all", "srs"):
        deployment_diagram()
        erd()
        sitemap()
        scrum_activity()
    if which in ("all", "uc"):
        use_case_diagram()
    if which in ("all", "cd"):
        class_diagrams()
    if which in ("all", "sd"):
        sequences()
    if which in ("all", "ad"):
        activities()
    with open(sys.argv[1], "w", encoding="utf-8") as fh:
        fh.write("\n".join(OUT) + "\n")
    print(f"{len(OUT)} spec lines -> {sys.argv[1]}")
