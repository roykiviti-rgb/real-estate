# Review helper: open a COPY of a company workbook (in %TEMP%) with Excel, recalc, dump check/value
# cells and export every sheet to PDF for visual review. Never touches the workspace file.
# Usage: powershell -File tool_excel_check.ps1 -Src <xlsx path> -OutDir <dir>
param([string]$Src, [string]$OutDir)
New-Item -ItemType Directory -Force $OutDir | Out-Null
$copy = Join-Path $OutDir "check_copy.xlsx"
Copy-Item -LiteralPath $Src -Destination $copy -Force
$xl = New-Object -ComObject Excel.Application
$xl.Visible = $false
$xl.DisplayAlerts = $false
$log = @()
try {
    $wb = $xl.Workbooks.Open($copy, 0, $true)
    $xl.CalculateFull()
    foreach ($ws in $wb.Worksheets) {
        $log += "SHEET: " + $ws.Name + " rtl=" + $ws.DisplayRightToLeft + " used=" + $ws.UsedRange.Address()
        $ur = $ws.UsedRange
        $rows = $ur.Rows.Count; $cols = $ur.Columns.Count
        for ($r = 1; $r -le [Math]::Min($rows, 80); $r++) {
            $vals = @()
            for ($c = 1; $c -le [Math]::Min($cols, 12); $c++) {
                $cell = $ws.Cells.Item($r, $c)
                $t = $cell.Text
                if ($cell.HasFormula) { $t = "{F}" + $t }
                $vals += $t
            }
            $log += ("R{0}: {1}" -f $r, ($vals -join " | "))
        }
        $pdf = Join-Path $OutDir ("sheet_" + $ws.Index + ".pdf")
        $ws.ExportAsFixedFormat(0, $pdf)
    }
    $wb.Close($false)
} catch {
    $log += "ERROR: " + $_.Exception.Message
}
$xl.Quit()
[System.Runtime.InteropServices.Marshal]::ReleaseComObject($xl) | Out-Null
$log | Out-File -Encoding utf8 (Join-Path $OutDir "excel_dump.txt")
[System.IO.File]::Delete($copy)
"done"

