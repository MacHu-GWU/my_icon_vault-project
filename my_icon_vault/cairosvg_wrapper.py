# -*- coding: utf-8 -*-

import dataclasses
from pathlib import Path

import mpire
import cairosvg


@dataclasses.dataclass
class Svg2PngCmd:
    path_in: Path = dataclasses.field()
    path_out: Path = dataclasses.field()
    output_width: int = dataclasses.field()
    output_height: int = dataclasses.field()

    def run(self):
        cairosvg.svg2png(
            bytestring=self.path_in.read_text(encoding="utf-8"),
            write_to=str(self.path_out),
            output_width=self.output_width,
            output_height=self.output_height,
        )

    @classmethod
    def parallel_run(cls, cmds: list["Svg2PngCmd"]):
        """
        Batch process multiple SVG files to PNG in parallel using multiprocessing.

        Args:
            cmds: List of Svg2PngCmd instances for each file to convert
        """

        def main(ith: int, cmd: Svg2PngCmd):
            print(f"[{ith}] Converting: {cmd.path_in} -> {cmd.path_out}")
            cmd.run()

        tasks = [{"ith": i, "cmd": cmd} for i, cmd in enumerate(cmds, start=1)]
        with mpire.WorkerPool(start_method="fork") as pool:
            results = pool.map(
                main,
                tasks,
            )
        return results
