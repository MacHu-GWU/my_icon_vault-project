# -*- coding: utf-8 -*-

import shutil
from pathlib import Path

from my_icon_vault.pngquant_png_batch_compressor import PngQuantArgs, batch_compress

dir_here = Path(__file__).absolute().parent
dir_input = dir_here / "tmp" / "input"
dir_output = dir_here / "tmp" / "output"

args = PngQuantArgs(
    quality_range=(50, 75),
)

shutil.rmtree(dir_output, ignore_errors=True)
batch_compress(
    dir_in=dir_input,
    dir_out=dir_output,
    path_bin=Path.home() / "pngquant" / "pngquant",
    args=args,
    multi_process=True,
)
