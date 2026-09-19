chcp 65001 > $null
$OutputEncoding = [System.Text.Encoding::UTF8

$headers = @{ "User-Agent" = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36" }

$categoryUrl = "https://hodhod.com/product-category/%DA%AF%D8%B1%D9%88%D9%87-%D8%A2%D9%85%D9%88%D8%B2%D8%B4%DB%8C-%DA%A9%D8%AA%D8%A7%D8%A8/%DA%A9%D8%AA%D8%A7%D8%A8%D9%87%D8%A7%DB%8C-%D8%A7%D9%88%D9%84-%D8%AF%D9%88%D9%85-%D9%88-%D8%B3%D9%88%D9%85-%D8%AF%D8%A8%D8%B3%D8%AA%D8%A7%D9%86"

$resp = Invoke-WebRequest -Uri $categoryUrl -Headers $headers
$target = "جمایما اردکه"
$link = $resp.Links | Where-Object { $_.outerHTML -match [regex]::Escape($target) } | Select-Object -First 1 -ExpandProperty href

if (-not $link) {
    Write-Host "لینک پیدا نشد - باید دستی از سایت هدهد گرفته شود" -ForegroundColor Red
    Write-Host "تعداد لینک�jهای پیدا شده در صفحه: $($resp.Links.Count)"
} else {
    Write-Host "لینک پیدا شد: $link" -ForegroundColor Cyan
    $productResp = Invoke-WebRequest -Uri $link -Headers $headers
    if ($productResp.Content -match '<meta[^>]+property="og:image"[^>]+content="([^"]+)"') {
        $imgUrl = $matches[1]
        $dest = "C:\Users\pc\Desktop\kidhub\media\books\ID_32_jemima-puddle-duck.jpg"
        Invoke-WebRequest -Uri $imgUrl -Headers $headers -OutFile $dest
        Write-Host "دانلود شد: $dest" -ForegroundColor Green
    } else {
        Write-Host "og:image پیدا نشد توی صفحه محصول" -ForegroundColor Red
    }
}
