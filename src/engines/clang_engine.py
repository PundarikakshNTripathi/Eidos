import subprocess
import tempfile
import os
import logging
from typing import Tuple

logger = logging.getLogger(__name__)

class ClangEngine:
    async def compile_to_assembly(self, code: str, target: str = "x86_64") -> Tuple[str, str]:
        """
        Compiles C/C++ code to Assembly.
        Returns: (stdout, stderr)
        """
        with tempfile.NamedTemporaryFile(suffix=".cpp", mode="w", delete=False) as source_file:
            source_file.write(code)
            source_path = source_file.name

        try:
            # -O3: Max optimization
            # -S: Emit assembly
            # -mllvm --x86-asm-syntax=intel: Intel syntax for x86
            # --target: Cross-compilation target
            cmd = [
                "clang", "-O3", "-S", 
                "--target=" + target,
                source_path, "-o", "-"
            ]
            
            if "x86" in target:
                cmd.append("-mllvm")
                cmd.append("--x86-asm-syntax=intel")

            result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
            return result.stdout, result.stderr
        except subprocess.TimeoutExpired:
            return "", "Compilation timed out."
        except Exception as e:
            return "", str(e)
        finally:
            if os.path.exists(source_path):
                os.remove(source_path)

    async def run_with_sanitizers(self, code: str) -> Tuple[str, str]:
        """
        Compiles and runs with AddressSanitizer and UndefinedBehaviorSanitizer.
        """
        with tempfile.NamedTemporaryFile(suffix=".cpp", mode="w", delete=False) as source_file:
            source_file.write(code)
            source_path = source_file.name
        
        binary_path = source_path + ".bin"

        try:
            # Compile
            compile_cmd = [
                "clang", "-fsanitize=address,undefined", "-g",
                source_path, "-o", binary_path
            ]
            compile_result = subprocess.run(compile_cmd, capture_output=True, text=True, timeout=10)
            
            if compile_result.returncode != 0:
                return "", f"Compilation Failed:\n{compile_result.stderr}"

            # Run
            run_result = subprocess.run([binary_path], capture_output=True, text=True, timeout=5)
            return run_result.stdout, run_result.stderr # Sanitizer output often goes to stderr
        except subprocess.TimeoutExpired:
            return "", "Execution timed out."
        except Exception as e:
            return "", str(e)
        finally:
            if os.path.exists(source_path):
                os.remove(source_path)
            if os.path.exists(binary_path):
                os.remove(binary_path)

    async def audit_binary(self, code: str) -> str:
        """
        Compiles and runs readelf to check for security features.
        """
        with tempfile.NamedTemporaryFile(suffix=".cpp", mode="w", delete=False) as source_file:
            source_file.write(code)
            source_path = source_file.name
        
        binary_path = source_path + ".bin"

        try:
            # Compile
            compile_cmd = ["clang", source_path, "-o", binary_path] # Default compilation
            subprocess.run(compile_cmd, check=True, capture_output=True)

            # Audit
            # Check for NX (No Execute) - usually implied by 'GNU_STACK' segment with RWE permissions or lack thereof
            # Check for PIE (Position Independent Executable) - Type: DYN
            readelf_cmd = ["readelf", "-l", "-h", binary_path]
            result = subprocess.run(readelf_cmd, capture_output=True, text=True, timeout=5)
            return result.stdout
        except Exception as e:
            return f"Error during audit: {str(e)}"
        finally:
            if os.path.exists(source_path):
                os.remove(source_path)
            if os.path.exists(binary_path):
                os.remove(binary_path)

    async def dump_ast(self, code: str) -> str:
        """
        Dumps the AST.
        """
        with tempfile.NamedTemporaryFile(suffix=".cpp", mode="w", delete=False) as source_file:
            source_file.write(code)
            source_path = source_file.name

        try:
            cmd = ["clang", "-Xclang", "-ast-dump", "-fsyntax-only", source_path]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
            return result.stdout
        except Exception as e:
            return str(e)
        finally:
            if os.path.exists(source_path):
                os.remove(source_path)

    async def compile_cuda(self, code: str) -> str:
        """
        Compiles CUDA to PTX.
        """
        with tempfile.NamedTemporaryFile(suffix=".cu", mode="w", delete=False) as source_file:
            source_file.write(code)
            source_path = source_file.name

        try:
            cmd = ["clang", "--cuda-device-only", "-S", "-emit-llvm", source_path, "-o", "-"]
            # Note: This might require CUDA SDK installed in the container. 
            # For now, we assume clang is enough to emit LLVM IR or PTX if configured.
            # If -emit-llvm is used, it outputs IR. For PTX, we might need nvptx target.
            # Let's try to target nvptx64-nvidia-cuda if possible, or just emit LLVM as requested by prompt "Dumps PTX" (Prompt says "Dumps PTX" but command says "-emit-llvm". I will follow the command in prompt: `clang --cuda-device-only -S -emit-llvm`)
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
            return result.stdout if result.returncode == 0 else result.stderr
        except Exception as e:
            return str(e)
        finally:
            if os.path.exists(source_path):
                os.remove(source_path)

clang_engine = ClangEngine()
