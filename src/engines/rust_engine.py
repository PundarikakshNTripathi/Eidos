import subprocess
import tempfile
import os
import logging
from typing import Tuple

logger = logging.getLogger(__name__)

class RustEngine:
    async def compile_to_assembly(self, code: str) -> Tuple[str, str]:
        """
        Compiles Rust code to Assembly.
        """
        with tempfile.NamedTemporaryFile(suffix=".rs", mode="w", delete=False) as source_file:
            source_file.write(code)
            source_path = source_file.name

        try:
            # --emit asm
            cmd = ["rustc", "--emit", "asm", "-O", source_path, "-o", "-"]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
            return result.stdout, result.stderr
        except Exception as e:
            return "", str(e)
        finally:
            if os.path.exists(source_path):
                os.remove(source_path)

rust_engine = RustEngine()
