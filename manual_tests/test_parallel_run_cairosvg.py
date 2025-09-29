# -*- coding: utf-8 -*-

from my_icon_vault.cairosvg_wrapper import Svg2PngCmd
from my_icon_vault.paths import dir_tmp, path_test_svg

path_png = dir_tmp / (path_test_svg.stem + ".png")
path_png.unlink(missing_ok=True)
cmd = Svg2PngCmd(
    path_in=path_test_svg,
    path_out=path_png,
    output_width=128,
    output_height=128,
)
cmds = [cmd]

if __name__ == "__main__":
    Svg2PngCmd.parallel_run(cmds)
