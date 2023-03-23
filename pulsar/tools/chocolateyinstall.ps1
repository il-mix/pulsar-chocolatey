
$ErrorActionPreference = 'Stop'
$toolsDir   = "$(Split-Path -parent $MyInvocation.MyCommand.Definition)"
$fileLocation = Join-Path $toolsDir 'Windows.Pulsar.Setup.1.103.0.exe'

$packageArgs = @{
  packageName    = $env:ChocolateyPackageName
  unzipLocation  = $toolsDir
  fileType       = 'exe'
  file           = $fileLocation
  softwareName   = 'Pulsar'
  checksum       = 'E63C7C33C1D98762331CE3964EAF208BD868AE20F0642D119FE9E257EAFB9E72'
  checksumType   = 'sha256'
  silentArgs     = '/S'
  validExitCodes = @(0)
}

Install-ChocolateyInstallPackage @packageArgs
