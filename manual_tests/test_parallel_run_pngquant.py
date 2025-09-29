# -*- coding: utf-8 -*-

from my_icon_vault.pngquant_wrapper import PngQuantCmd
from my_icon_vault.paths import dir_tmp, path_test_png, path_bin_pngquant

path_png = dir_tmp / path_test_png.name
path_png.unlink(missing_ok=True)
cmd = PngQuantCmd(
    path_bin=path_bin_pngquant,
    path_in=path_test_png,
    path_out=path_png,
    quality_range=(50, 75),
)
cmds = [cmd]

if __name__ == "__main__":
    PngQuantCmd.parallel_run(cmds)
