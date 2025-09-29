# -*- coding: utf-8 -*-

"""
SVG to PNG Converter - A Python wrapper for CairoSVG

This module provides a convenient Python interface for converting SVG files to PNG format
using the CairoSVG library. It supports both single file conversion and batch processing
of multiple SVG files with optional multiprocessing for improved performance.

The converter preserves the original SVG content while allowing precise control over
output dimensions, making it suitable for generating PNG assets at specific resolutions
for web applications, mobile apps, or print media.

Key features:

- Single SVG to PNG conversion with custom dimensions
- Batch processing with multiprocessing support
- Preserves SVG quality and vector graphics fidelity
- Configurable output dimensions for different use cases

Typical use cases include:

- Converting vector icons to raster format for legacy browser support
- Generating PNG thumbnails from SVG graphics
- Creating multiple resolution variants of the same SVG asset
- Preparing graphics for platforms that don't support SVG format
"""

import dataclasses
from pathlib import Path

import mpire
import cairosvg


@dataclasses.dataclass
class Svg2PngCmd:
    """
    Command configuration for converting SVG files to PNG format.

    This dataclass encapsulates all the parameters needed to convert a single SVG
    file to PNG format using CairoSVG. It provides both individual conversion
    and batch processing capabilities with multiprocessing support.

    Args:
        path_in: Path to the input SVG file to be converted.
        path_out: Path where the output PNG file will be saved.
        output_width: Width of the output PNG image in pixels.
        output_height: Height of the output PNG image in pixels.

    Example:
        >>> cmd = Svg2PngCmd(
        ...     path_in=Path("icon.svg"),
        ...     path_out=Path("icon.png"),
        ...     output_width=128,
        ...     output_height=128
        ... )
        >>> cmd.run()
        # Converts icon.svg to 128x128 PNG

    Note:
        The output dimensions determine the resolution of the final PNG.
        Larger dimensions will result in higher quality but larger file sizes.
        Common sizes include:
        - Icons: 16x16, 32x32, 64x64, 128x128
        - Thumbnails: 200x200, 300x300
        - High-res graphics: 512x512, 1024x1024
    """
    path_in: Path = dataclasses.field()
    path_out: Path = dataclasses.field()
    output_width: int = dataclasses.field()
    output_height: int = dataclasses.field()

    def run(self):
        """
        Execute SVG to PNG conversion for the configured input file.

        This method reads the SVG content from the input file and uses CairoSVG
        to render it as a PNG image with the specified output dimensions.
        The SVG content is read as UTF-8 text and passed to CairoSVG as a byte string.

        Raises:
            FileNotFoundError: If the input SVG file does not exist.
            UnicodeDecodeError: If the SVG file contains invalid UTF-8 content.
            ValueError: If the SVG content is malformed or cannot be parsed.
            OSError: If there are permission issues writing the output file.

        Example:
            >>> cmd = Svg2PngCmd(
            ...     path_in=Path("logo.svg"),
            ...     path_out=Path("logo_64x64.png"),
            ...     output_width=64,
            ...     output_height=64
            ... )
            >>> cmd.run()
            # Creates logo_64x64.png with 64x64 pixel dimensions
        """
        cairosvg.svg2png(
            bytestring=self.path_in.read_text(encoding="utf-8"),
            write_to=str(self.path_out),
            output_width=self.output_width,
            output_height=self.output_height,
        )

    @classmethod
    def parallel_run(cls, cmds: list["Svg2PngCmd"]):
        """
        Batch convert multiple SVG files to PNG in parallel using multiprocessing.

        This method distributes SVG to PNG conversion tasks across multiple CPU cores
        using the mpire library for improved performance when processing large numbers
        of files. Each conversion is logged with progress information.

        Args:
            cmds: List of Svg2PngCmd instances, each configured for a specific
                  input SVG file and target PNG output with desired dimensions.

        Returns:
            List of results from each worker process (typically None for each
            successful conversion).

        Raises:
            FileNotFoundError: If any input SVG file does not exist.
            UnicodeDecodeError: If any SVG file contains invalid UTF-8 content.
            ValueError: If any SVG content is malformed.
            OSError: If there are permission issues with any output files.

        Example:
            >>> cmds = [
            ...     Svg2PngCmd(Path("icon1.svg"), Path("icon1.png"), 64, 64),
            ...     Svg2PngCmd(Path("icon2.svg"), Path("icon2.png"), 128, 128),
            ...     Svg2PngCmd(Path("logo.svg"), Path("logo.png"), 256, 256),
            ... ]
            >>> Svg2PngCmd.parallel_run(cmds)
            [1] Converting: icon1.svg -> icon1.png
            [2] Converting: icon2.svg -> icon2.png
            [3] Converting: logo.svg -> logo.png

        Note:
            The multiprocessing approach is most beneficial when converting
            many files or when working with complex SVG graphics that require
            significant rendering time.
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
