from toolz import concat, compose, reduce
from os import chdir
from os.path import join
from toolz.curried import filter, map
from helper_functions import curried_takewhile, curried_dropwhile
from toolz.functoolz import curry
from toolz.dicttoolz import assoc

def empty_line(line):
    return line != ""

def read_pkgbuild_file(package_name, base="/home/benjamin/aur"):
    chdir(join(base, package_name))
    with open("PKGBUILD","r") as read_file:
        return read_file.read().replace("'", "").split("\n")

def split_pkgbuild_line(line):
    return line.strip().split("=")

def identity(x):
    return x

def dependency_line(line):
    return (line[0].find("depends") != -1 and
            len(line) == 2 and line[0] != "optdepends")

def format_pkgbuild(pkgbuild):
    return compose(map(split_pkgbuild_line),filter(empty_line))(pkgbuild)

def format_deps_list(deps_list):

    return (deps_list[0],deps_list[1].strip("()").split(" "))

def non_opt_deps(formatted_pkgbuild):

    return compose(dict,map(format_deps_list),
                           filter(dependency_line))(formatted_pkgbuild)

def opt_deps_read(formatted_pkgbuild):

    not_optdeps_line = lambda line : line[0] != "optdepends"
    not_close_brackets_line = lambda line : line[0] != ")"
    return compose(list,
                   curried_takewhile(not_close_brackets_line),
                   curried_dropwhile(not_optdeps_line))(formatted_pkgbuild)

def split_opt_dep(opt_dep):
    return opt_dep[0].split(": ")

def opt_deps(formatted_pkgbuild):

    optional_dependencies = compose(list,
                                    map(split_opt_dep),
                                    opt_deps_read)(formatted_pkgbuild)

    return (optional_dependencies[0][0],optional_dependencies[1:])