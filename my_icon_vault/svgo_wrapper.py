# -*- coding: utf-8 -*-

"""
SVG Optimizer - A Python wrapper for SVGO

This module provides a convenient Python interface for the SVGO (SVG Optimizer) tool,
which is a Node.js-based tool for optimizing SVG files. It supports both single file
optimization and batch processing of multiple SVG files with optional multiprocessing
for improved performance when handling large collections of SVG assets.

SVGO optimization typically reduces file sizes by:

- Removing unnecessary metadata and comments
- Simplifying path data and geometric shapes
- Removing redundant attributes and whitespace
- Converting colors to more compact representations
- Merging similar elements and optimizing transforms

Key features:

- Single SVG file optimization with configurable precision
- Batch processing with multiprocessing support
- Quiet mode for suppressing output during batch operations
- Multi-pass optimization for maximum compression
- Preserves visual quality while minimizing file size

Typical use cases include:

- Optimizing SVG icons for web applications to reduce bundle size
- Preparing SVG assets for mobile applications where bandwidth matters
- Batch optimization of large SVG asset libraries
- Preprocessing SVG files before further conversion or deployment
"""

import subprocess
import dataclasses
from pathlib import Path

import mpire


@dataclasses.dataclass
class SvgoCmd:
    """
    Command configuration for optimizing SVG files using SVGO.

    This dataclass encapsulates all the parameters needed to optimize SVG files
    using the SVGO command-line tool. It provides both individual file optimization
    and batch processing capabilities with multiprocessing support.

    Args:
        path_bin: Path to the SVGO binary executable.
        path_in: Path to the input SVG file to be optimized.
        path_out: Path where the optimized SVG file will be saved.
        precision: Number of decimal places for floating point values in the SVG.
                   Lower values result in smaller files but may reduce visual quality.
                   Typical values: 1-3 for icons, 2-4 for detailed graphics.
        quite: If True, suppresses console output during optimization.
               Useful for batch processing to reduce log verbosity.
        multipass: If True, runs multiple optimization passes for better compression.
                   This may significantly improve optimization but takes more time.

    Example:
        >>> cmd = SvgoCmd(
        ...     path_bin=Path("/usr/local/bin/svgo"),
        ...     path_in=Path("icon.svg"),
        ...     path_out=Path("icon_optimized.svg"),
        ...     precision=2,
        ...     multipass=True
        ... )
        >>> cmd.run()
        # Optimizes icon.svg with 2 decimal precision and multipass

    Note:
        SVGO must be installed separately via npm:
        npm install -g svgo

        The optimization is lossless in terms of visual appearance when using
        appropriate precision values, but the internal structure of the SVG
        may be significantly altered for better compression.
    """

    path_bin: Path = dataclasses.field()
    path_in: Path = dataclasses.field()
    path_out: Path = dataclasses.field()
    precision: int | None = dataclasses.field(default=None)
    quite: bool = dataclasses.field(default=False)
    multipass: bool = dataclasses.field(default=True)

    @property
    def args(self) -> list[str]:
        """
        Generate command line arguments for the SVGO tool.

        Constructs the complete argument list based on the configured options,
        including input/output paths, precision settings, and optimization flags.

        Returns:
            List of command line arguments ready to be passed to subprocess.run().

        Example:
            >>> cmd = SvgoCmd(
            ...     path_bin=Path("svgo"),
            ...     path_in=Path("input.svg"),
            ...     path_out=Path("output.svg"),
            ...     precision=2,
            ...     quite=True,
            ...     multipass=True
            ... )
            >>> args = cmd.args
            >>> # Returns: ["svgo", "--input", "input.svg", "--output", "output.svg",
            >>> #          "--precision", "2", "--quiet", "--multipass"]
        """
        args = [
            str(self.path_bin),
            "--input",
            str(self.path_in),
            "--output",
            str(self.path_out),
        ]
        if self.precision:
            args.extend(["--precision", str(self.precision)])
        if self.quite:
            args.append("--quiet")
        if self.multipass:
            args.append("--multipass")
        return args

    def run(self, verbose: bool = False):
        """
        Execute SVGO optimization on the specified input SVG file.

        This method constructs the command line arguments and runs the SVGO
        subprocess to optimize the SVG file according to the specified settings.
        The optimization process typically reduces file size while preserving
        visual quality.

        Args:
            verbose: If True, prints the full command line before execution.
                     Useful for debugging or understanding the exact SVGO invocation.

        Raises:
            subprocess.CalledProcessError: If SVGO exits with non-zero status,
                typically indicating an invalid SVG file or SVGO configuration error.
            FileNotFoundError: If the SVGO binary is not found in the specified path.
                Make sure SVGO is installed via: npm install -g svgo

        Example:
            >>> cmd = SvgoCmd(
            ...     path_bin=Path("svgo"),
            ...     path_in=Path("large_icon.svg"),
            ...     path_out=Path("optimized_icon.svg"),
            ...     precision=1,
            ...     multipass=True
            ... )
            >>> cmd.run(verbose=True)
            # Outputs: svgo --input large_icon.svg --output optimized_icon.svg --precision 1 --multipass
            # File size typically reduced by 20-60% depending on original optimization
        """
        args = self.args
        if verbose:
            print(" ".join(args))
        subprocess.run(args, check=True)

    @classmethod
    def parallel_run(cls, cmds: list["SvgoCmd"]):
        """
        Batch optimize multiple SVG files in parallel using multiprocessing.

        This method distributes SVG optimization tasks across multiple CPU cores
        using the mpire library for improved performance when processing large
        numbers of files. Each optimization is logged with progress information.

        Args:
            cmds: List of SvgoCmd instances, each configured for a specific
                  input SVG file and optimization settings.

        Returns:
            List of results from each worker process (typically None for each
            successful optimization).

        Raises:
            subprocess.CalledProcessError: If any SVGO process fails, typically
                due to invalid SVG content or configuration errors.
            FileNotFoundError: If SVGO binary is not found. Ensure SVGO is installed:
                npm install -g svgo

        Example:
            >>> cmds = [
            ...     SvgoCmd(Path("svgo"), Path("icon1.svg"), Path("icon1_opt.svg")),
            ...     SvgoCmd(Path("svgo"), Path("icon2.svg"), Path("icon2_opt.svg")),
            ...     SvgoCmd(Path("svgo"), Path("logo.svg"), Path("logo_opt.svg")),
            ... ]
            >>> SvgoCmd.parallel_run(cmds)
            [1] Compressing: icon1.svg -> icon1_opt.svg
            [2] Compressing: icon2.svg -> icon2_opt.svg
            [3] Compressing: logo.svg -> logo_opt.svg

        Note:
            Parallel processing is most beneficial when optimizing many files.
            For small numbers of files, the overhead of multiprocessing may
            outweigh the benefits. Consider using individual run() calls for
            fewer than 10-20 files.

            File size reductions typically range from 20-60% depending on the
            original SVG optimization level and complexity.
        """

        def main(ith: int, cmd: SvgoCmd):
            print(f"[{ith}] Compressing: {cmd.path_in} -> {cmd.path_out}")
            cmd.run(verbose=False)

        tasks = [{"ith": i, "cmd": cmd} for i, cmd in enumerate(cmds, start=1)]
        with mpire.WorkerPool(start_method="fork") as pool:
            results = pool.map(
                main,
                tasks,
            )
        return results
