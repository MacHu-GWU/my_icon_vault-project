# -*- coding: utf-8 -*-

from my_icon_vault.svgo_wrapper import SvgoCmd
from my_icon_vault.paths import dir_tmp, path_test_svg, path_bin_svgo

path_svg = dir_tmp / path_test_svg.name
path_svg.unlink(missing_ok=True)
cmd = SvgoCmd(
    path_bin=path_bin_svgo,
    path_in=path_test_svg,
    path_out=path_svg,
    quite=True,
)
cmds = [cmd]

if __name__ == "__main__":
    SvgoCmd.parallel_run(cmds)
