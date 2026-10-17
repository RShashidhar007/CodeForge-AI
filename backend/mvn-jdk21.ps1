# PowerShell script to run Maven with JDK 21
# Usage: .\mvn-jdk21.ps1 clean compile
# or: .\mvn-jdk21.ps1 test

$env:JAVA_HOME = "C:\Program Files\Java\latest\jdk-21"
$env:PATH = "C:\Program Files\Java\latest\jdk-21\bin;$env:PATH"

Write-Host "Using Java: $env:JAVA_HOME" -ForegroundColor Green
& java -version

Write-Host "`nRunning Maven with arguments: $args" -ForegroundColor Cyan
& mvn $args
