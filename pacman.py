from subprocess import check_call, Popen, PIPE
from toolz import map

def aur_packages():
	cmd = Popen("pacman -Qm", stdout=PIPE, shell=True)
	cmd_out = cmd.communicate()[0]
	return cmd_out.decode("utf-8").split("\n")[:-1]

def non_aur_packages():
	cmd = Popen("pacman -Qq", stdout=PIPE, shell=True)
	cmd_out = cmd.communicate()[0]
	return cmd_out.decode("utf-8").split("\n")[:-1]

def remove_unneeded_packages():
    cmd = Popen("pacman -Qdt", stdout=PIPE, shell=True)
    cmd_out = cmd.communicate()[0]
    orphaned_packages = cmd_out.decode("utf-8").split("\n")[:-1]
    orphaned_packages = map(lambda package : package.split(" ")[0], orphaned_packages)
    if not orphaned_packages:
        print ("There are no orphaned packages to uninstall")
        return
    print ("Uninstalling orphaned packages")
    for package in orphaned_packages:
        uninstall = input("Would you like to uninstall the orphaned package {0}? [Y/n]".format(package))
        if not uninstall or uninstall == "Y":
            output = check_call(["sudo -S pacman -Rsn {0}".format(package)], shell=True)
            if output == 0:
                print ("{0} uninstalled successfully".format(package))
        else:
            continue
    return
