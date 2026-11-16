# HANDOFF: si-capstone-doc-srs

## Goal
Final SRS for Capstone Project (Kelompok 1, 22D, SAPA for Bimbel Asentra), due 17 Nov 2026 at 20.00. Rebuilt from Rifqi's v1.0 draft as v1.1: Laravel stack, all diagrams in Visual Paradigm, prose in Agung's writing style, APA 7.

## Done (newest first)
- 2026-11-17 (rev 3): NIDN printed as `NIDN. _____________`; Lampiran C trimmed to 6 technical items; MoM written as of 26 Sep with a separate 'Kebutuhan terkait' column; conflicts fixed (SRS moved from pra-sprint to Sprint 1, hak_akses = lihat/balas/kelola as in the mockup, Kontak/Tim mockup descriptions). `build_srs.py` takes an optional 2nd arg for the output path; `update_word.ps1` never quits a Word instance that still has documents open.
- 2026-11-17 (rev 2): NIDN blank; interview 26 Sep 2026 with MoM tables in Lampiran B; Heroicons in Tabel 5.1; AD/SD-01..12 all in Bab IV (Lampiran D removed); every picture inside a bordered 1x1 table like the template.
- 2026-11-17: SRS v1.1 built: `doc-srs/srs/isi_srs.py` (content), `build_srs.py` (fills P07 template), `update_word.ps1` (Word refreshes TOC/lists, exports PDF). Output goes to Drive, not the repo: `dev/cekula/capstone-project/SRS_SAPA_Kelompok1_v1.1.docx` + `.pdf` (87 pages, 31 tables, 43 figures).
- 2026-11-17: identity data (names, NIM, dosen, NIDN, output path) lives in Drive `dev/cekula/capstone-project/srs-identitas.json` because this repo is PUBLIC.
- 2026-11-17: VP generator runs on Windows: `doc-srs/diagram/generator/run_win.sh [all|srs|uc|cd|sd|ad]`. Plugin extended (deployment nodes/components/artifacts, `<<table>>` classes with PK/FK, `rel` 1 : N links, class stereotypes, activity object flow). New diagrams: deployment (layered architecture), ERD part 1/2, sitemap, Scrum cycle; class diagram split in 2. Terms fixed in all diagrams: Dasbor→Dashboard, kata sandi→password, kueri→query.
- 2026-11-17: writing profile v1.3 (Drive `Cekula/_writing-profile/writing-style.md`): APA 7 is the default citation style when a template allows a choice.

## In progress
- Rev 3 is built in the session scratchpad; copy it over the Drive docx/pdf once Word has closed the file. Lampiran B MoM (26 Sep 2026) was reconstructed from the project plan; Yordan should confirm it with Greta.

## Next
1. After any edit, rebuild: `python -I doc-srs/srs/build_srs.py`, then `powershell -ExecutionPolicy Bypass -File doc-srs/srs/update_word.ps1 "<docx path>"`.
2. Share v1.1 with the group (Rifqi's v1.0 wording was replaced) and submit before 20.00.
3. Sprint 1 follow-up (Lampiran C no. 4): team migrations differ from the ERD (no kontak/percakapan tables; prospek stores nama/nomor_telepon directly).

## Decisions & notes
- 2FA is Won't have (W01). Laravel decision dated 6 Nov 2026, approved by Pak Albert.
- VP's native ERD shapes render without column text in headless export, so the ERD uses class notation (`<<table>>`, `<<PK>>`, `<<FK>>`, 1 : N).
- Word field quirk: template's `TOC \t "Keterangan Gambar,1"` finds nothing on this laptop; build rewrites it to `\t "Keterangan Gambar"`. In PowerShell, loop Word COM collections by index (foreach only hits the first TOC).
- `run.sh` (Mac) still exists; `run_win.sh` exports each diagram to PDF and rasterises at 300 dpi (needs Poppler).
- Old PNGs `AD-07/SD-07 - Melihat Dasbor Pemantauan.png` and `Class Diagram SAPA (MVC).png` are kept because the ASN1 laporan build still references them.
- The repo is public and `doc-srs/group-chat/` already contains WhatsApp history with emails and a demo login. Consider removing it.
