# PowerShell script to fix the Django migration issue
# Run this script in PowerShell as Administrator

Write-Host "Starting Django migration fix..." -ForegroundColor Green

# Navigate to project directory
Set-Location "C:\MTL\AIS Course\CICD\Assignment\Application\RetailShopAPI"

# Step 1: Check current Python installation
Write-Host "Checking Python installation..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version 2>$null
    Write-Host "Python found: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "Python not found in PATH. Trying alternative paths..." -ForegroundColor Red
    $pythonPaths = @(
        "C:\Python311\python.exe",
        "C:\Python310\python.exe", 
        "C:\Python39\python.exe",
        "C:\Users\admin\AppData\Local\Microsoft\WindowsApps\python.exe"
    )
    
    $pythonFound = $false
    foreach ($path in $pythonPaths) {
        if (Test-Path $path) {
            Write-Host "Found Python at: $path" -ForegroundColor Green
            $pythonFound = $true
            break
        }
    }
    
    if (-not $pythonFound) {
        Write-Host "Python not found. Please install Python or add it to PATH." -ForegroundColor Red
        exit 1
    }
}

# Step 2: Check Django installation
Write-Host "Checking Django installation..." -ForegroundColor Yellow
try {
    $djangoVersion = python -c "import django; print(django.get_version())" 2>$null
    Write-Host "Django found: $djangoVersion" -ForegroundColor Green
} catch {
    Write-Host "Django not found. Installing requirements..." -ForegroundColor Yellow
    python -m pip install -r requirements.txt
}

# Step 3: Reset migration state
Write-Host "Resetting migration state..." -ForegroundColor Yellow
python manage.py migrate products 0001 --fake

# Step 4: Apply the new migration
Write-Host "Applying schema cleanup migration..." -ForegroundColor Yellow
python manage.py migrate products

# Step 5: Check final status
Write-Host "Checking final migration status..." -ForegroundColor Yellow
python manage.py showmigrations products

Write-Host "Migration fix completed!" -ForegroundColor Green
