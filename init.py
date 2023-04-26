import re
import sys
import os
import argparse
import codecs
import shutil
import requests
import hashlib

# Class defining methods to edit package's source files given desired Pulsar version
class PackageFilesEditor():
	# Constants
	PACKAGE_SOURCES_PATH = "./pulsar/"
	NUSPEC_FILE = PACKAGE_SOURCES_PATH + "pulsar.nuspec"
	INSTALL_SCRIPT_PATH = PACKAGE_SOURCES_PATH + "tools/chocolateyinstall.ps1"
	TOOLS_PATH = PACKAGE_SOURCES_PATH + "tools/"
	VERIFICATION_FILE_PATH = TOOLS_PATH + "VERIFICATION.txt"
	INSTALLER_CHECKSUM_FILE_NAME = "SHA256SUMS.txt"
	LICENSE_URL = "https://github.com/pulsar-edit/pulsar/blob/master/LICENSE.md"
	LICENSE_URL_RAW = "https://raw.githubusercontent.com/pulsar-edit/pulsar/master/LICENSE.md"
	LICENSE_FILE_PATH = TOOLS_PATH + "LICENSE.txt"
	
	# Class properties
	pulsarVersion_ = ""
	pulsarVersionName_ = ""
	githubReleaseUrl_ = "https://github.com/pulsar-edit/pulsar/releases/tag/"
	assetsDownloadUrl_ = "https://github.com/pulsar-edit/pulsar/releases/download/"
	installerFileName_ = "Windows.Pulsar.Setup"
	installerDownloadUrl_ = ""
	installerChecksumDownloadUrl_ = ""
	
	# Class initializer
	def __init__(self, pulsarVersion):
		# Initialize file names and URLs given required version
		self.pulsarVersion_ = pulsarVersion
		if(self.pulsarVersion_[0] == "v"):
			self.pulsarVersion_ = self.pulsarVersion_[1:]
		self.pulsarVersionName_ = "v" + self.pulsarVersion_
		self.installerFileName_ = "Windows.Pulsar.Setup." + self.pulsarVersion_ + ".exe"
		self.githubReleaseUrl_ = self.githubReleaseUrl_ + self.pulsarVersionName_
		self.assetsDownloadUrl_ = self.assetsDownloadUrl_ + self.pulsarVersionName_
		self.installerDownloadUrl_ = self.assetsDownloadUrl_ + "/" + self.installerFileName_
		self.installerChecksumDownloadUrl_ = self.assetsDownloadUrl_ + "/" + self.INSTALLER_CHECKSUM_FILE_NAME	
	
	# Main function run from main
	def run(self):
		print("Init configuration files to generate package for version " + self.pulsarVersion_)
		
		self.retirieveInstallerChecksum()
		
		self.editNuspecPackage()
		self.editInstallScript()
		self.generateVerificationFile()
		self.downloadLicenseFile()
		
		print("Package sources initialized")
	
	def retirieveInstallerChecksum(self):
		print("Retrieve installer file's checksum for verification")
		
		response = requests.get(self.installerChecksumDownloadUrl_)
		if(response.status_code != 200):
			print("Error " + str(response.status_code) + " while downloading checksum file")
			sys.exit(1)
		
		open(self.INSTALLER_CHECKSUM_FILE_NAME, "wb").write(response.content)
		
		print("DONE")
		
		print("Extract SHA256 checksum for installer file from checksums list")
		
		with open(self.INSTALLER_CHECKSUM_FILE_NAME, "r") as f:
			lines = f.readlines()
			for index, line in enumerate(lines):
				if(self.installerFileName_ in line):
					self.installerChecksum_ = line.split()[0]
					print("Installer file " + self.installerFileName_ + " checksum: " + self.installerChecksum_)
					
		os.remove(self.INSTALLER_CHECKSUM_FILE_NAME)
			
		print("DONE")
	
	def editNuspecPackage(self):
		print("Edit " + self.NUSPEC_FILE + " file...")
		nuspecFileOriginal = codecs.open(self.NUSPEC_FILE, "r", "utf-8")
		nuspecFileNew = codecs.open("tmp", "w", "utf-8")
		for line in nuspecFileOriginal:
			if "<version>" in line:
				nuspecFileNew.write("    <version>" + self.pulsarVersion_ + "</version>" + os.linesep)
			elif "<releaseNotes>" in line:
				nuspecFileNew.write("    <releaseNotes>https://github.com/pulsar-edit/pulsar/blob/master/CHANGELOG.md#" + self.pulsarVersion_.replace(".","") + "</releaseNotes>" + os.linesep)
			elif "<licenseUrl>" in line:
				nuspecFileNew.write("    <licenseUrl>" + self.LICENSE_URL + "</licenseUrl>" + os.linesep)
			else:
				nuspecFileNew.write(line)
		nuspecFileOriginal.close()
		nuspecFileNew.close()
		
		shutil.copy2("tmp", self.NUSPEC_FILE)
		os.remove("tmp")
		
		print("DONE")
		
	def editInstallScript(self):
		print("Edit " + self.INSTALL_SCRIPT_PATH + " file...")
		installScriptOriginal = codecs.open(self.INSTALL_SCRIPT_PATH, "r", "utf-8")
		installScriptNew = codecs.open("tmp", "w", "utf-8")
		for line in installScriptOriginal:
			if "https" in line:
				installScriptNew.write("$url = '" + self.installerDownloadUrl_ + "'" + os.linesep)
			elif "checksum" in line and not "Type" in line:
				installScriptNew.write("  checksum       = '" + self.installerChecksum_ + "'" + os.linesep)
			else:
				installScriptNew.write(line)
		installScriptOriginal.close()
		installScriptNew.close()
		
		shutil.copy2("tmp", self.INSTALL_SCRIPT_PATH)
		os.remove("tmp")
		
		print("DONE")
		
	def generateVerificationFile(self):
		print("Generate verification file...")
		verificationFile = codecs.open(self.VERIFICATION_FILE_PATH, "w", "utf-8")
		
		verificationFile.write("VERIFICATION" + os.linesep)
		verificationFile.write(os.linesep)
		verificationFile.write("Install script will download " + self.installerFileName_ + " from " + self.githubReleaseUrl_ + os.linesep)
		verificationFile.write("Installer checksum (SHA256): " + self.installerChecksum_ + os.linesep)
		verificationFile.write("Checksum will be checked automatically by installer script." + os.linesep)
		
		verificationFile.close()
		
		print("DONE")
		
	def downloadLicenseFile(self):
		print("Download license file...")
		
		response = requests.get(self.LICENSE_URL_RAW)
		if(response.status_code != 200):
			print("Error " + str(response.status_code) + " while downloading license file")
			sys.exit(1)
		
		open(self.LICENSE_FILE_PATH, "wb").write(response.content)
		
		print("DONE")
	
# Main function
if __name__ == '__main__':
	# Command line arguments parsing
	parser = argparse.ArgumentParser(description="Init Chocolatey Pulsar package configuration files", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
	parser.add_argument("version", help="Pulsar version")
	args = parser.parse_args()
	
	# Run files edit
	packageFilesEditor = PackageFilesEditor(args.version)
	packageFilesEditor.run()
	
	print("Navigate to pulsar folder and generate package with 'choco pack' command")
		