"""
Storage Persistence Layer

Handles JSON file persistence with atomic write patterns to prevent partial
data corruption. Provides serialization helpers for application models.
"""

import json
import os
import shutil
from pathlib import Path
from typing import List, Dict, Any


DEFAULT_DATA_DIR = Path(__file__).resolve().parent.parent / "data"


class StorageManager:
    """Manages reading and writing data records to JSON flat files safely."""

    def __init__(self, data_dir: Path = DEFAULT_DATA_DIR):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.students_file = self.data_dir / "students.json"
        self.courses_file = self.data_dir / "courses.json"
        self.enrollments_file = self.data_dir / "enrollments.json"

        self._initialize_empty_files()

    def _initialize_empty_files(self) -> None:
        """Creates empty JSON array files if they do not already exist."""
        for target_file in [self.students_file, self.courses_file, self.enrollments_file]:
            if not target_file.exists():
                self._safe_write(target_file, [])

    def _safe_write(self, filepath: Path, payload: Any) -> None:
        """
        Atomic write pattern: writes to a temporary file in the same directory,
        then replaces the target file atomically. This prevents half-written
        corrupted data if the terminal is killed mid-operation.
        """
        temp_file = filepath.with_suffix(".tmp")
        try:
            with open(temp_file, "w", encoding="utf-8") as f:
                json.dump(payload, f, indent=2, ensure_ascii=False)
            os.replace(temp_file, filepath)
        except Exception:
            if temp_file.exists():
                try:
                    os.remove(temp_file)
                except OSError:
                    pass
            raise

    def _safe_read(self, filepath: Path) -> List[Dict[str, Any]]:
        """Reads JSON data with recovery for empty or malformed files."""
        if not filepath.exists():
            return []
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read().strip()
                if not content:
                    return []
                data = json.loads(content)
                if isinstance(data, list):
                    return data
                return []
        except (json.JSONDecodeError, OSError):
            backup_path = filepath.with_suffix(".corrupted")
            try:
                shutil.copyfile(filepath, backup_path)
            except OSError:
                pass
            return []

    # Student operations
    def load_students(self) -> List[Dict[str, Any]]:
        return self._safe_read(self.students_file)

    def save_students(self, data: List[Dict[str, Any]]) -> None:
        self._safe_write(self.students_file, data)

    # Course operations
    def load_courses(self) -> List[Dict[str, Any]]:
        return self._safe_read(self.courses_file)

    def save_courses(self, data: List[Dict[str, Any]]) -> None:
        self._safe_write(self.courses_file, data)

    # Enrollment operations
    def load_enrollments(self) -> List[Dict[str, Any]]:
        return self._safe_read(self.enrollments_file)

    def save_enrollments(self, data: List[Dict[str, Any]]) -> None:
        self._safe_write(self.enrollments_file, data)
