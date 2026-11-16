# Open the built SRS in Word, update the table of contents and figure/table lists, save, and export a PDF.
# Usage: powershell -ExecutionPolicy Bypass -File update_word.ps1 "G:\My Drive\...\SRS_SAPA_Kelompok1_v1.1.docx"
param([Parameter(Mandatory = $true)][string]$Docx)
$ErrorActionPreference = "Stop"
$path = (Resolve-Path -LiteralPath $Docx).Path
$pdf = [System.IO.Path]::ChangeExtension($path, ".pdf")
$word = New-Object -ComObject Word.Application
$word.Visible = $false
$word.DisplayAlerts = 0
try {
    $doc = $word.Documents.Open($path, $false, $false)
    # page numbers settle only after a full repagination, so update twice
    foreach ($i in 1..2) {
        $doc.Repaginate()
        # index the COM collections: PowerShell foreach only reaches the first item
        for ($k = 1; $k -le $doc.TablesOfContents.Count; $k++) { $doc.TablesOfContents.Item($k).Update() }
        for ($k = 1; $k -le $doc.TablesOfFigures.Count; $k++) { $doc.TablesOfFigures.Item($k).Update() }
    }
    $doc.Save()
    $doc.ExportAsFixedFormat($pdf, 17)  # 17 = wdExportFormatPDF
    "pages: " + $doc.ComputeStatistics(2)
    $doc.Close($false)
    "pdf: $pdf"
} finally {
    $word.Quit()
    [System.Runtime.InteropServices.Marshal]::ReleaseComObject($word) | Out-Null
}
