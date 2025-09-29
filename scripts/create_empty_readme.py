# -*- coding: utf-8 -*-

from pathlib_mate import Path
from my_icon_vault.paths import dir_project_root

dir_assets_icons = Path(dir_project_root / "assets" / "icons")
for path in dir_assets_icons.select_dir(recursive=False):
    path_readme = path / "README.rst"
    if path_readme.exists() is False:
        path_readme.write_text("", encoding="utf-8")
