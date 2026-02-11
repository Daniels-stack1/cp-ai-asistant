# Script de prueba para Casa Pepe Backend
# Ejecutar con: .\test_api.ps1

$BaseUrl = "http://localhost:5000/api"

Write-Host "1. Probando Búsqueda (Search)..." -ForegroundColor Cyan
try {
    # Usamos 'burger' que sabemos que existe
    $Response = Invoke-RestMethod -Uri "$BaseUrl/restaurantes/search" -Method Post -ContentType "application/json" -Body '{"query": "burger"}'
    Write-Host "Exito! Respuesta:" -ForegroundColor Green
    $Response | ConvertTo-Json -Depth 5 | Write-Host
} catch {
    Write-Host "Error en Search: $_" -ForegroundColor Red
}

Write-Host "`n------------------`n"

Write-Host "2. Probando Detalle (Detail)..." -ForegroundColor Cyan
try {
    # ID real de Burger House obtenido del debug
    $Body = '{"id": "rec0qZiFkbqvtSHul"}' 
    $Response = Invoke-RestMethod -Uri "$BaseUrl/restaurantes/detail" -Method Post -ContentType "application/json" -Body $Body
    Write-Host "Exito! Respuesta:" -ForegroundColor Green
    $Response | ConvertTo-Json -Depth 5 | Write-Host
} catch {
    Write-Host "Error en Detail: $_" -ForegroundColor Red
}

Write-Host "`n------------------`n"

Write-Host "3. Probando Registro Visita (Checkout)..." -ForegroundColor Cyan
try {
    # Usamos ID real de Burger House y un array de productos dummy (idealmente IDs reales de productos)
    # NOTA: Si 'Productos presentados' es un campo Link, fallará si los IDs no son de la tabla Productos.
    # Usaremos una lista vacía para probar si no conocemos IDs de productos, O IDs falsos si es texto simple.
    # El debug dice que es un array de IDs ["recDHJlCyxCccMCiJ"]. Deberíamos intentar usar IDs válidos.
    # Como no tenemos IDs de productos a mano, enviamos lista vacía para no romper la integridad referencial.
    
    $VisitBody = '{"restauranteId": "rec0qZiFkbqvtSHul", "cart": [], "timestamp": "2026-02-11T12:00:00Z"}'
    
    $Response = Invoke-RestMethod -Uri "$BaseUrl/visita/registrar" -Method Post -ContentType "application/json" -Body $VisitBody
    Write-Host "Exito! Visita registrada:" -ForegroundColor Green
    $Response | ConvertTo-Json -Depth 5 | Write-Host
} catch {
    Write-Host "Error en Registro: $_" -ForegroundColor Red
}

Write-Host "`n------------------`n"

Write-Host "4. Probando Dashboard (Summary)..." -ForegroundColor Cyan
try {
    $Response = Invoke-RestMethod -Uri "$BaseUrl/dashboard/summary" -Method Get
    Write-Host "Exito! Resumen:" -ForegroundColor Green
    $Response | ConvertTo-Json -Depth 5 | Write-Host
} catch {
    Write-Host "Error en Dashboard: $_" -ForegroundColor Red
}
