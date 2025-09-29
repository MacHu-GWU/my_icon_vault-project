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
- Parallel processing: Use multiprocessing to speed up batch operations

Typical use cases include optimizing PNG assets for web deployment, reducing storage
requirements for image archives, or preparing graphics for mobile applications where
file size matters.
"""

import subprocess
import dataclasses
from pathlib import Path

import mpire

from .base import BaseCmd


@dataclasses.dataclass
class PngQuantCmd(BaseCmd):
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

    path_bin: Path = dataclasses.field()
    quality_range: tuple[int, int] = dataclasses.field(default=(80, 95))
    speed: int | None = dataclasses.field(default=None)
    force: bool = dataclasses.field(default=False)
    ncolors: int | None = dataclasses.field(default=None)

    def to_args(self) -> list[str]:
        """
        Convert the dataclass fields to pngquant command line arguments.

        Returns:
            List of command line arguments ready to be passed to subprocess.run().

        Example:
            >>> cmd = PngQuantCmd(
            ...     path_bin=Path("pngquant"),
            ...     path_in=Path("input.png"),
            ...     quality_range=(80, 95),
            ...     speed=4
            ... )
            >>> args = cmd.to_args()
            >>> # Returns: ["pngquant", "--quality", "80-95", "--speed", "4", "input.png"]
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
        Execute pngquant compression on the specified input PNG file.

        This method constructs the command line arguments and runs the pngquant
        subprocess to compress the PNG file according to the specified settings.

        Args:
            verbose: If True, prints the full command line before execution.

        Raises:
            subprocess.CalledProcessError: If pngquant exits with non-zero status.
            FileNotFoundError: If the pngquant binary is not found.

        Example:
            >>> cmd = PngQuantCmd(
            ...     path_bin=Path("pngquant"),
            ...     path_in=Path("large.png"),
            ...     path_out=Path("compressed.png"),
            ...     quality_range=(65, 85)
            ... )
            >>> cmd.run(verbose=True)
            # Outputs: pngquant --quality 65-85 --output compressed.png large.png
        """
        args = self.to_args()
        # if verbose:
        #     print(" ".join(args))
        if verbose:
            self._log_before()
        subprocess.run(args, check=True)
        if verbose:
            self._log_after()

    @classmethod
    def parallel_run(cls, cmds: list["PngQuantCmd"], verbose: bool = False):
        """
        Batch process multiple PNG files in parallel using multiprocessing.

        This method uses the mpire library to distribute PNG compression tasks
        across multiple CPU cores for improved performance when processing
        large numbers of files. Progress is printed for each file processed.

        Args:
            cmds: List of PngQuantCmd instances, each configured for a specific
                  input file and compression settings.

        Returns:
            List of results from each worker process (typically None for each
            successful compression).

        Raises:
            subprocess.CalledProcessError: If any pngquant process fails.
            FileNotFoundError: If pngquant binary is not found.

        Example:
            >>> cmds = [
            ...     PngQuantCmd(path_bin=Path("pngquant"), path_in=Path("img1.png")),
            ...     PngQuantCmd(path_bin=Path("pngquant"), path_in=Path("img2.png")),
            ... ]
            >>> PngQuantCmd.parallel_run(cmds)
            [1] Compressing: img1.png -> img1.png
            [2] Compressing: img2.png -> img2.png
        """

        def main(ith: int, cmd: PngQuantCmd):
            print(f"[{ith}] Compressing: {cmd.path_in} -> {cmd.path_out}")
            cmd.run(verbose=verbose)

        tasks = [{"ith": i, "cmd": cmd} for i, cmd in enumerate(cmds, start=1)]
        with mpire.WorkerPool(start_method="fork") as pool:
            results = pool.map(
                main,
                tasks,
            )
        return results
