# pulsar-chocolatey

Pulsar editor Chocolatey package's source files.

## Content

The package contains:

- init.py: a python script to automatically initialize/update some package's files given the desired Pulsar editor version
- pulsar: the main package sources' folder

## Usage

### init.py

The script will download the Pulsar installer given the input version, and edit a couple of source files accordingly.

Example usage:

```python 1.103.0```

One must input the last version available on the website, otherwise the script will fail (it won't be able to download the installer).

Once the script terminates, tha package is ready to be generated.

Note: python `requests` module is required (install with `pip install requests`)

### Package generation

Once the sources are updated, navigate to pulsar folder and run

```choco pack```

Chocolatey will generate the file `pulsar\pulsar.<version>.nupkg`.

Test the package locally

```choco install pulsar --source .\pulsar\pulsar.<version>.nupkg```

If everything is ok, request to publish it on Chocolatey website.

## To do

- update package with 'latest' release; wait for a tatic URL to download installer; no more input parameter (version) needed
- parse version of 'latest' installer (from filename or from embedded data)
