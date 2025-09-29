# -*- coding: utf-8 -*-

import dataclasses
from pathlib import Path
from pathlib_mate.mate_tool_box import repr_data_size


@dataclasses.dataclass
class BaseCmd:
    path_in: Path = dataclasses.field()
    path_out: Path | None = dataclasses.field()

    def _log_before(self):
        self._size_before = self.path_in.stat().st_size

    def _log_after(self):
        size_after = self.path_out.stat().st_size
        print(
            f"Size before: {repr_data_size(self._size_before)}, after: {repr_data_size(size_after)}"
        )
