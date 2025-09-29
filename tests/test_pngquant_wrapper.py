# -*- coding: utf-8 -*-

from my_icon_vault.pngquant_wrapper import PngQuantCmd
from my_icon_vault.paths import path_test_png, dir_tmp, path_bin_pngquant


def test_run():
    dir_tmp.mkdir(parents=True, exist_ok=True)
    path_png = dir_tmp / path_test_png.name
    path_png.unlink(missing_ok=True)

    cmd = PngQuantCmd(
        path_bin=path_bin_pngquant,
        path_in=path_test_png,
        path_out=path_png,
        quality_range=(50, 75),
    )
    cmd.run(verbose=True)


if __name__ == "__main__":
    from my_icon_vault.tests import run_cov_test

    run_cov_test(
        __file__,
        "my_icon_vault.pngquant_wrapper",
        preview=False,
    )
