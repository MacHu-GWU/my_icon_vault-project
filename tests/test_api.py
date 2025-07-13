# -*- coding: utf-8 -*-

from my_icon_vault import api


def test():
    _ = api


if __name__ == "__main__":
    from my_icon_vault.tests import run_cov_test

    run_cov_test(
        __file__,
        "my_icon_vault.api",
        preview=False,
    )
