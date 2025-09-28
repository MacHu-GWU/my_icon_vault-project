# -*- coding: utf-8 -*-

from my_icon_vault.pngquant_wrapper import PngQuantArgs
from my_icon_vault.paths import path_test_png, dir_tmp, path_pngquant


def test_run():
    dir_tmp.mkdir(parents=True, exist_ok=True)
    path_png = dir_tmp / path_test_png.name
    path_png.unlink(missing_ok=True)

    arg = PngQuantArgs(
        quality_range=(50, 75),
        path_out=path_png,
    )
    arg.run(path_bin=path_pngquant, path_in=path_test_png)
    size_before = path_test_png.stat().st_size
    size_after = path_png.stat().st_size
    print(f"Size before: {size_before}, after: {size_after}")


if __name__ == "__main__":
    from my_icon_vault.tests import run_cov_test

    run_cov_test(
        __file__,
        "my_icon_vault.pngquant_wrapper",
        preview=False,
    )
