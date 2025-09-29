# -*- coding: utf-8 -*-

import dataclasses
from pathlib import Path
from functools import cached_property

from s3pathlib import S3Path

from .constants import size_list
from .paths import dir_project_root, dir_tmp, path_bin_svgo, path_bin_pngquant
from .svgo_wrapper import SvgoCmd
from .cairosvg_wrapper import Svg2PngCmd
from .pngquant_wrapper import PngQuantCmd

dir_assets_icons = dir_project_root.joinpath("assets", "icons")


@dataclasses.dataclass
class IconAsset:
    name: str

    @cached_property
    def dir_asset(self) -> Path:
        return dir_assets_icons.joinpath(self.name)

    @cached_property
    def path_svg(self) -> Path:
        return self.dir_asset.joinpath(f"{self.name}.svg")

    @cached_property
    def path_readme(self) -> Path:
        return self.dir_asset.joinpath("README.rst")

    def get_path_png(self, width: int = 96, height: int = 96) -> Path:
        return self.dir_asset.joinpath(f"{self.name}-{width}x{height}.png")

    @classmethod
    def list_all(cls) -> list["IconAsset"]:
        assets = list()
        for path in dir_assets_icons.rglob("*.svg"):
            if len(path.relative_to(dir_assets_icons).parts) == 2:
                asset = cls(name=path.parent.name)
                assets.append(asset)
        return assets

    def to_svgo_cmd(self):
        return SvgoCmd(
            path_bin=path_bin_svgo,
            path_in=self.path_svg,
            path_out=self.path_svg,
            precision=1,
            quite=True,
            multipass=True,
        )

    def to_svg2png_cmds(self):
        cmds = list()
        for size in size_list:
            cmd = Svg2PngCmd(
                path_in=self.path_svg,
                path_out=dir_tmp / self.get_path_png(size, size).name,
                output_width=size,
                output_height=size,
            )
            cmds.append(cmd)
        return cmds

    def to_pngquant_cmds(self):
        cmds = list()
        for size in size_list:
            path_out = self.get_path_png(size, size)
            path_out.unlink(missing_ok=True)
            cmd = PngQuantCmd(
                path_bin=path_bin_pngquant,
                path_in=dir_tmp / self.get_path_png(size, size).name,
                path_out=path_out,
                quality_range=(25, 50),
                # quality_range=(50, 75),
            )
            cmds.append(cmd)
        return cmds

    def get_local_and_s3_pairs(
        self,
        s3dir_root: S3Path,
    ) -> list[tuple[Path, S3Path]]:
        pairs = [
            (
                self.path_svg,
                s3dir_root.joinpath(*self.path_svg.relative_to(dir_project_root).parts),
            ),
        ]
        for size in size_list:
            path_png = self.get_path_png(size, size)
            pairs.append(
                (
                    path_png,
                    s3dir_root.joinpath(*path_png.relative_to(dir_project_root).parts),
                )
            )
        return pairs

    def upload_to_cloudflare_r2(
        self,
        s3_client,
        s3dir_root: S3Path,
    ):
        pairs = self.get_local_and_s3_pairs(s3dir_root)
        for path, s3path in pairs:
            s3path.write_bytes(path.read_bytes(), bsm=s3_client)

    def to_icon_list_bullet(self) -> str:
        try:
            description = self.path_readme.read_text("utf-8").splitlines()[0].strip()
            identifier = self.name
            return f"- {identifier}: {description}"
        except FileNotFoundError:
            return ""

    def generate_icon_list_md(self):
        self.dir_asset
