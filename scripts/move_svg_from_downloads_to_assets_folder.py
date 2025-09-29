# -*- coding: utf-8 -*-

from pathlib_mate import Path
from my_icon_vault.paths import dir_project_root

dir_downloads = Path(
    """
/Users/sanhehu/Downloads/1
""".strip()
)

dir_assets_icons = Path(dir_project_root / "assets" / "icons")
for path in dir_downloads.rglob("*.svg"):
    name = path.fname

    path_dst = dir_assets_icons / name / f"{name}.svg"
    path_dst.parent.mkdir_if_not_exists()
    path.moveto(new_abspath=path_dst)
