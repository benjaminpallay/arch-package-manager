from collections import defaultdict

class PKGBUILDReader():

    def __init__(self, pkgbuild_location):
        self.pkgbuild = self.__read_pkgbuild_file(pkgbuild_location)
        self.wanted_lines = ["pkgname", "pkgver", "pkgbase", "pkgrel", "url",
                        "license","groups", "provides", "depends", "makedepends",
                        "optdepends", "conflicts", "replaces", "arch", "pkgdesc"]

    def __process_line(self, line):
        return line.strip().replace("'", "").split("=")

    def __read_pkgbuild_file(self, pkgbuild_location):

        with open(pkgbuild_location,"r") as read_file:
            lines = [self.__process_line(line) for line in read_file]
            return [line for line in lines if line[0]]

    def __multiline_option(self, l):

        option_details = []

        for line in l:
            if line[0] == ")":
                break
            option_details.append(line)

        return option_details

    def read(self):

        package_details = defaultdict(list)

        for i,l in enumerate(self.pkgbuild):
            if l[0] in self.wanted_lines:
                if l[1] != "(":
                    package_details[l[0]] = l[1]
                else:
                    package_details[l[0]] = self.__multiline_option(self.pkgbuild[i:])

        return package_details