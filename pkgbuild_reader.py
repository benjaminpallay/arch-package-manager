from collections import defaultdict
from os.path import join
from urllib.parse import urljoin
import re

class PKGBUILDReader():

    def __init__(self, pkgbuild_location):
        self.pkgbuild = self.__read_pkgbuild_file(pkgbuild_location)
        self.wanted_lines = ["pkgname", "pkgver", "pkgbase", "pkgrel", "url",
                        "license","groups", "provides", "depends", "makedepends",
                        "optdepends", "conflicts", "replaces", "arch", "pkgdesc"]
        self.aur_url_base = "https://aur.archlinux.org/packages/"

    def __process_line(self, line):
        return line.strip().replace('"',"").split("=")

    def __read_pkgbuild_file(self, pkgbuild_location):

        with open(pkgbuild_location,"r") as read_file:
            lines = [self.__process_line(line) for line in read_file]
            return [line for line in lines if line[0]]

    def __multiline_option(self, lines):

        lines = [line[0] for line in lines]

        option_details = []

        for line in lines:
            if line == ")":
                break
            matches = re.findall("([^']*):\s([^']*)", line)
            option_details.append(list(matches[0]))

        return option_details

    def __singleline_option(self, line):

        if line[0] == "(":
            return re.findall("'([^']*)'", line)
        return line

    def __option_value(self,i,l):
        if l[1] != "(":
            return self.__singleline_option(l[1])
        else:
            return self.__multiline_option(self.pkgbuild[i + 1:])

    def read(self):

        package_details = defaultdict.fromkeys(self.wanted_lines)

        for i,l in enumerate(self.pkgbuild):
            if l[0].find("()") != -1:
                break
            if l[0] in self.wanted_lines:
                package_details[l[0]] = self.__option_value(i,l)

        package_details["pkgver"] = "{0}-{1}".format(package_details["pkgver"],
                                                     package_details["pkgrel"])

        del package_details["pkgrel"]

        if package_details["pkgbase"]:
            package_details["pkgname"] = package_details["pkgbase"]
            del package_details["pkgbase"]

        package_details["aur"] = urljoin(self.aur_url_base,package_details["pkgname"])

        return {k:(v.replace("'","") if type(v) == str else v) for k,v in package_details.items()}