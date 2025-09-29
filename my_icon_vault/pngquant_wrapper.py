# -*- coding: utf-8 -*-

"""
PNG Batch Compressor - A Python wrapper for pngquant

This script provides a convenient Python interface for the pngquant PNG compression tool.
It supports both single file compression and batch processing of entire directory trees
with optional multiprocessing for faster batch operations. The script preserves directory
structure when batch processing and allows fine-tuned control over compression settings
including quality ranges, speed/quality trade-offs, and color palette sizes.

Example usage:
- Single file: Compress one PNG with specific quality settings
- Batch processing: Recursively compress all PNGs in a directory tree
- Parallel processing: Use multiprocessing to speed up batch operations

Typical use cases include optimizing PNG assets for web deployment, reducing storage
requirements for image archives, or preparing graphics for mobile applications where
file size matters.
"""

import subprocess
import dataclasses
from pathlib import Path

import mpire


@dataclasses.dataclass
class PngQuantCmd:
    """
    PNG compression arguments for pngquant tool.

    Args:
       quality_range: Quality range (min, max) from 0-100. Files below min quality
                     won't be saved, files above max will use fewer colors.
                     - High quality: (80, 95)
                     - Balanced: (65, 85)
                     - High compression: (50, 75)

       speed: Speed/quality trade-off. Higher values are faster but lower quality.
              - 1: Slow, highest quality
              - 4: Default balance
              - 8-10: Fast processing
              - 11: Fastest, rough quality

       force: If True, overwrites existing output files without prompting.

       ncolors: Number of colors in output image palette. Fewer colors = smaller file.
               - Icons/simple graphics: 64-128
               - General photos: 128-256
               - High quality images: 256

       path_out: Output file path. If None, uses input filename with suffix.
    """

    path_bin: Path = dataclasses.field(default=None)
    path_in: Path = dataclasses.field(default=None)
    path_out: Path | None = dataclasses.field(default=None)
    quality_range: tuple[int, int] = dataclasses.field(default=(80, 95))
    speed: int | None = dataclasses.field(default=None)
    force: bool = dataclasses.field(default=False)
    ncolors: int | None = dataclasses.field(default=None)

    def to_args(self) -> list[str]:
        """
        Convert arguments to command line arguments list.
        """
        args = [
            str(self.path_bin),
        ]
        args.extend(["--quality", f"{self.quality_range[0]}-{self.quality_range[1]}"])
        if self.speed is not None:
            args.extend(["--speed", str(self.speed)])
        if self.force:
            args.append("--force")
        if self.ncolors:
            args.append(str(self.ncolors))
        if self.path_out is not None:
            args.extend(["--output", str(self.path_out)])
        args.append(str(self.path_in))
        return args

    def run(self, verbose: bool = False):
        """
        Execute pngquant compression on a single file.

        Args:
            path_bin: Path to pngquant binary executable
            path_in: Input PNG file path to compress
        """
        args = self.to_args()
        if verbose:
            print(" ".join(args))
        subprocess.run(args, check=True)

    @classmethod
    def parallel_run(cls, cmds: list["PngQuantCmd"]):
        """
        Batch process multiple PNG files in parallel using multiprocessing.

        Args:
            cmds: List of PngQuantCmd instances for each file to compress
        """

        def main(ith: int, cmd: PngQuantCmd):
            print(f"[{ith}] Compressing: {cmd.path_in} -> {cmd.path_out}")
            cmd.run(verbose=False)

        tasks = [{"ith": i, "cmd": cmd} for i, cmd in enumerate(cmds, start=1)]
        with mpire.WorkerPool(start_method="fork") as pool:
            results = pool.map(
                main,
                tasks,
            )
        return results
