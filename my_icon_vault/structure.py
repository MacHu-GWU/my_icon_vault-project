# -*- coding: utf-8 -*-

import dataclasses
from pathlib import Path
from functools import cached_property

from .paths import dir_project_root, path_bin_svgo, path_bin_pngquant
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
        size_list = [96, 256, 512]
        cmds = list()
        for size in size_list:
            cmd = Svg2PngCmd(
                path_in=self.path_svg,
                path_out=self.get_path_png(size, size),
                output_width=size,
                output_height=size,
            )
            cmds.append(cmd)
        return cmds

    def to_pngquant_cmds(self):
        size_list = [96, 256, 512]
        cmds = list()
        for size in size_list:
            cmd = PngQuantCmd(
                path_bin=path_bin_pngquant,
                path_in=self.get_path_png(size, size),
                path_out=self.get_path_png(size, size),
                quality_range=(50, 75),
            )
            cmds.append(cmd)
        return cmds

    @cached_property
    def path_png_96x96(self) -> Path:
        return self.get_path_png(96, 96)

    @cached_property
    def path_png_256x256(self) -> Path:
        return self.get_path_png(256, 256)

    @cached_property
    def path_png_512x512(self) -> Path:
        return self.get_path_png(512, 512)

    @cached_property
    def path_png_1024x1024(self) -> Path:
        return self.get_path_png(1024, 1024)

    def generate_png_96x96(self):
        path = self.path_png_96x96
        path.unlink(missing_ok=True)
        svg2png(self.path_svg, path, 96, 96)

    def generate_png_256x256(self):
        path = self.path_png_256x256
        path.unlink(missing_ok=True)
        svg2png(self.path_svg, path, 256, 256)

    def generate_png_512x512(self):
        path = self.path_png_512x512
        path.unlink(missing_ok=True)
        svg2png(self.path_svg, path, 512, 512)

    def generate_png_1024x1024(self):
        path = self.path_png_1024x1024
        path.unlink(missing_ok=True)
        svg2png(self.path_svg, path, 1024, 1024)
