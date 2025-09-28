# -*- coding: utf-8 -*-

import cairosvg
from pathlib import Path


def svg2png(
    path_in: Path,
    path_out: Path,
    output_width: int,
    output_height: int,
):
    cairosvg.svg2png(
        bytestring=path_in.read_text(encoding="utf-8"),
        write_to=str(path_out),
        output_width=output_width,
        output_height=output_height,
    )
