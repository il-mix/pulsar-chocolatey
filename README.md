# pulsar-chocolatey

Pulsar editor Chocolatey package's source files.

## Content

The package contains:

- init.py: a python script to automatically initialize/update some package's files given the desired Pulsar editor version
- pulsar: the main package sources' folder


## Prerequisites

### Chocolatey package manager

Chocolatey is needed to generate and test the package locally. To install it (if not already installed), start Windows PowerShell as administrator and run the command

```
Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))
```

### Python

The initialization script is written in Python. Python3 for Windows is needed to run it. If not already installed, download latest release from [Python website](https://www.python.org/downloads/windows/) and install it.

Once installed, add `requests` module using PIP

```
pip install requests
````

## Usage

### init.py

The script will download the Pulsar installer given the input version, and edit a couple of source files accordingly.

Example usage:

```
python 1.103.0
```

One must input the last version available on the website, otherwise the script will fail (it won't be able to download the installer).

Once the script terminates, tha package is ready to be generated.

### Package generation

Once the sources are updated, navigate to pulsar folder and run

```
choco pack
```

Chocolatey will generate the file `pulsar\pulsar.<version>.nupkg`.

Test the package locally

```
choco install pulsar --source .\pulsar\pulsar.<version>.nupkg
```

If everything is ok, request to publish it on Chocolatey website.

## To do

- update package with 'latest' release; wait for a tatic URL to download installer; no more input parameter (version) needed
- parse version of 'latest' installer (from filename or from embedded data)
