# -*- coding: utf-8 -*-

import subprocess
import dataclasses
from pathlib import Path

import mpire


@dataclasses.dataclass
class SvgoCmd:
    """ """

    path_bin: Path = dataclasses.field()
    path_in: Path = dataclasses.field()
    path_out: Path = dataclasses.field()
    precision: int | None = dataclasses.field(default=None)
    quite: bool = dataclasses.field(default=False)
    multipass: bool = dataclasses.field(default=True)

    @property
    def args(self) -> list[str]:
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
        args = self.args
        if verbose:
            print(" ".join(args))
        subprocess.run(args, check=True)

    @classmethod
    def parallel_run(cls, cmds: list["SvgoCmd"]):
        """
        Batch optimize multiple SVG files in parallel using multiprocessing.

        Args:
            cmds: List of SvgoCmd instances for each file to optimize
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
