from typing import List
from pathlib import Path
from datetime import datetime

from ops.ecris.analysis.venus_data import get_file_timestamp

def _list_parquet_files(path: Path) -> List[Path]:
    return sorted(p for p in path.glob('venus_data_*.parquet') if p.is_file())

def all_available_dates(path: Path) -> List[datetime]:
    return [get_file_timestamp(f) for f in _list_parquet_files(path)]