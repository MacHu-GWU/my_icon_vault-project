# -*- coding: utf-8 -*-

if __name__ == "__main__":
    from my_icon_vault.tests import run_cov_test

    run_cov_test(
        __file__,
        "my_icon_vault",
        is_folder=True,
        preview=False,
    )
