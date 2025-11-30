import subprocess
import tempfile
import os
import logging
from typing import Tuple

logger = logging.getLogger(__name__)

class GoEngine:
    async def compile_to_assembly(self, code: str) -> Tuple[str, str]:
        """
        Compiles Go code to Assembly.
        """
        with tempfile.NamedTemporaryFile(suffix=".go", mode="w", delete=False) as source_file:
            source_file.write(code)
            source_path = source_file.name

        try:
            # go tool compile -S
            cmd = ["go", "tool", "compile", "-S", source_path]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
            return result.stdout, result.stderr
        except Exception as e:
            return "", str(e)
        finally:
            if os.path.exists(source_path):
                os.remove(source_path)

go_engine = GoEngine()
