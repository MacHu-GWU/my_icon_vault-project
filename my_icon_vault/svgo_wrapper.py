# -*- coding: utf-8 -*-

import shutil
import subprocess
import dataclasses
from pathlib import Path


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
