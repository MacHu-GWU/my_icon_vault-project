# -*- coding: utf-8 -*-

from my_icon_vault.svgo_wrapper import SvgoCmd
from my_icon_vault.paths import path_test_svg, dir_tmp, path_bin_svgo


def test_run():
    dir_tmp.mkdir(parents=True, exist_ok=True)
    path_svg = dir_tmp / path_test_svg.name
    path_svg.unlink(missing_ok=True)

    cmd = SvgoCmd(
        path_bin=path_bin_svgo,
        path_in=path_test_svg,
        path_out=path_svg,
        precision=1,
        quite=True,
        multipass=True,
    )
    cmd.run()
    size_before = path_test_svg.stat().st_size
    size_after = path_svg.stat().st_size
    print(f"Size before: {size_before}, after: {size_after}")


if __name__ == "__main__":
    from my_icon_vault.tests import run_cov_test

    run_cov_test(
        __file__,
        "my_icon_vault.svgo_wrapper",
        preview=False,
    )
