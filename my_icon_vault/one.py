# -*- coding: utf-8 -*-

import typing as T
import itertools
import dataclasses
from functools import cached_property

import boto3
from s3pathlib import S3Path
from home_secret.api import hs

from .paths import path_icon_list_md
from .svgo_wrapper import SvgoCmd
from .cairosvg_wrapper import Svg2PngCmd
from .pngquant_wrapper import PngQuantCmd
from .structure import IconAsset


@dataclasses.dataclass
class Config:
    cloudflare_r2_endpoint: str
    cloudflare_r2_access_key: str
    cloudflare_r2_secret_key: str
    cloudflare_r2_bucket_name: str


@dataclasses.dataclass
class One:
    @cached_property
    def config(self) -> Config:
        p1 = "providers.cloudflare.accounts.sh.secrets.read_and_write_all_r2_bucket.creds.endpoint"
        p2 = "providers.cloudflare.accounts.sh.secrets.read_and_write_all_r2_bucket.creds.access_key"
        p3 = "providers.cloudflare.accounts.sh.secrets.read_and_write_all_r2_bucket.creds.secret_key"
        return Config(
            cloudflare_r2_endpoint=hs.t(p1).v,
            cloudflare_r2_access_key=hs.t(p2).v,
            cloudflare_r2_secret_key=hs.t(p3).v,
            cloudflare_r2_bucket_name="sh-img-cdn",
        )

    @cached_property
    def s3_client(self):
        return boto3.client(
            service_name="s3",
            endpoint_url=self.config.cloudflare_r2_endpoint,
            aws_access_key_id=self.config.cloudflare_r2_access_key,
            aws_secret_access_key=self.config.cloudflare_r2_secret_key,
            region_name="auto",
        )

    @cached_property
    def s3dir_root(self) -> S3Path:
        return S3Path(
            f"s3://{self.config.cloudflare_r2_bucket_name}/projects/my_icon_vault/"
        )

    @cached_property
    def icon_assets(self):
        return IconAsset.list_all()

    def compress_svg(self):
        cmds = [asset.to_svgo_cmd() for asset in self.icon_assets]
        SvgoCmd.parallel_run(cmds, verbose=True)

    def generate_png(self):
        cmds = list(
            itertools.chain(*(asset.to_svg2png_cmds() for asset in self.icon_assets))
        )
        Svg2PngCmd.parallel_run(cmds, verbose=True)

    def compress_png(self):
        cmds = list(
            itertools.chain(*(asset.to_pngquant_cmds() for asset in self.icon_assets))
        )
        PngQuantCmd.parallel_run(cmds, verbose=True)

    def upload_to_cloudflare_r2(self):
        icon_assets = IconAsset.list_all()
        for icon_asset in icon_assets:
            icon_asset.upload_to_cloudflare_r2(
                s3_client=self.s3_client,
                s3dir_root=self.s3dir_root,
            )

    def generate_icon_list_md(self):
        lines = [
            "# Icon List",
            "",
        ]
        for asset in self.icon_assets:
            s = asset.to_icon_list_bullet()
            if s:
                lines.append(s)
        content = "\n".join(lines) + "\n"
        path_icon_list_md.write_text(content, encoding="utf-8")


one = One()
