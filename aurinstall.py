from json import loads as json_load
from urllib.parse import urljoin
from requests import get
from os import getcwd, chdir, remove, listdir
from os.path import join
from functools import partial
from urllib.request import urlretrieve
import tarfile
from subprocess import check_call, Popen, PIPE
from shutil import rmtree
import csv
import toolz
from toolz.curried import map, reduce, filter, compose, accumulate, pipe
from toolz.functoolz import curry
from toolz.itertoolz import concat
import pacman

class NonAurException(Exception):
	pass

def get_package(package_name,base="/home/benjamin/aur"):
    git_location = urljoin("https://aur.archlinux.org", "{0}.git".format(package_name))
    dpath = "{0}.tar.gz".format(urljoin(base,package_name))

    chdir(base)
    if package_name in listdir():
        rmtree(package_name)

    check_call(["git clone {0}".format(git_location)], shell=True)

def install_package(package_name,base="/home/benjamin/aur"):
	print (package_name)
	try:
		package_info = package_json(package_name)
		a_packages = {_[0] : _[1] for _ in [package_info.split(" ") for package_info in aur_packages()]}
		non_a_packages = [package for package in non_aur_packages() if package not in a_packages]
		package_dependencies = dependencies(package_info)
		
		for package in package_dependencies:
			dep_package_info = package_json(package_name)
			dep_version = package_version(dep_package_info)
			if package in a_packages:
				if a_packages[package] == dep_version:
					continue
				else:
					install_package(package)
			elif package in non_a_packages:
				continue
			else:
				try:
					install_package(package)
				except NonAurException:
					check_call(["sudo pacman -S {}".format(package)],shell=True)
					
		chdir(base)
		get_package(package_name)
		chdir(package_name)
		check_call(["makepkg","-si"])
		rmtree(join(base,package_name))
	except NonAurException:
		check_call(["sudo pacman -S {}".format(package_name)],shell=True)

	return