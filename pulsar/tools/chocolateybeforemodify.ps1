# Terminate running processes
$process = Get-Process "Pulsar" -ea 0
if ($process) {
  Write-Host "Found running instances of Pulsar. Stopping processes..."
  $process | Stop-Process
}
