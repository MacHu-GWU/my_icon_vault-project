# -*- coding: utf-8 -*-

from my_icon_vault.cairosvg_wrapper import Svg2PngCmd
from my_icon_vault.paths import path_test_svg, dir_tmp


def test_svg2png():
    dir_tmp.mkdir(parents=True, exist_ok=True)
    path_png = dir_tmp / (path_test_svg.stem + ".png")
    path_png.unlink(missing_ok=True)
    cmd = Svg2PngCmd(
        path_in=path_test_svg,
        path_out=path_png,
        output_width=128,
        output_height=128,
    )
    cmd.run()
    size_before = path_test_svg.stat().st_size
    size_after = path_png.stat().st_size
    print(f"Size before: {size_before}, after: {size_after}")


if __name__ == "__main__":
    from my_icon_vault.tests import run_cov_test

    run_cov_test(
        __file__,
        "my_icon_vault.cairosvg_wrapper",
        preview=False,
    )
