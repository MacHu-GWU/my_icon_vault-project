# -*- coding: utf-8 -*-

from my_icon_vault.svgo_wrapper import SvgoCmd
from my_icon_vault.cairosvg_wrapper import Svg2PngCmd
from my_icon_vault.pngquant_wrapper import PngQuantCmd
from my_icon_vault.structure import IconAsset

svgo_cmds = list()
svg2png_cmds = list()
pngquant_cmds = list()
for icon_asset in IconAsset.list_all():
    svgo_cmds.append(icon_asset.to_svgo_cmd())
    svg2png_cmds.extend(icon_asset.to_svg2png_cmds())
    pngquant_cmds.extend(icon_asset.to_pngquant_cmds())

if __name__ == "__main__":
    """ """
    SvgoCmd.parallel_run(svgo_cmds)
    # Svg2PngCmd.parallel_run(svg2png_cmds)
    # PngQuantCmd.parallel_run(pngquant_cmds)
