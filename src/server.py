from mcp.server.fastmcp import FastMCP
from src.judge import judge
from src.engines.clang_engine import clang_engine
from src.engines.rust_engine import rust_engine
from src.engines.go_engine import go_engine


# Initialize FastMCP server
mcp = FastMCP("Eidos")

@mcp.tool()
async def analyze_assembly_essence(code: str, target: str = "x86_64", language: str = "cpp") -> str:
    """
    Compiles source to Assembly and identifies missed SIMD opportunities.
    Language options: cpp, rust, go.
    """
    if language == "cpp":
        stdout, stderr = await clang_engine.compile_to_assembly(code, target)
    elif language == "rust":
        stdout, stderr = await rust_engine.compile_to_assembly(code)
    elif language == "go":
        stdout, stderr = await go_engine.compile_to_assembly(code)
    else:
        return f"Unsupported language: {language}"

    if stderr and not stdout:
        return f"Compilation Failed:\n{stderr}"

    prompt = f"Map critical loops to Assembly (Target: {target}). Identify missed SIMD opportunities."
    return await judge.reason(code, stdout, prompt)

@mcp.tool()
async def run_sanitizer_suite(code: str) -> str:
    """
    Compiles with sanitizers and detects memory corruption.
    """
    stdout, stderr = await clang_engine.run_with_sanitizers(code)
    
    # If stderr contains sanitizer output (e.g., "AddressSanitizer"), analyze it.
    if "Sanitizer" in stderr or "Sanitizer" in stdout:
        prompt = "Explain the specific memory corruption cause based on this sanitizer output."
        return await judge.reason(code, stderr + "\n" + stdout, prompt)
    
    if stderr and not stdout:
         return f"Compilation/Runtime Error:\n{stderr}"

    return "No sanitizer errors detected."

@mcp.tool()
async def audit_binary_security(code: str) -> str:
    """
    Checks for PIE, NX Bit, and Stack Canaries.
    """
    output = await clang_engine.audit_binary(code)
    prompt = "Analyze the readelf output. Check for PIE, NX Bit, and Stack Canaries. If any are missing, explain the exploit path."
    return await judge.reason(code, output, prompt)

@mcp.tool()
async def explain_ast_logic(code: str) -> str:
    """
    Analyzes AST to find logic bugs.
    """
    output = await clang_engine.dump_ast(code)
    prompt = "Analyze this AST to find logic bugs that syntax checkers might miss."
    return await judge.reason(code, output, prompt)

@mcp.tool()
async def benchmark_implementations(code_a: str, code_b: str) -> str:
    """
    Benchmarks two C++ implementations. 
    Expects code_a and code_b to be function bodies for `void func_a()` and `void func_b()`.
    """
    # TODO: Implement a proper harness generator.
    # For now, returning a placeholder as this requires complex harness generation.
    return "Benchmarking not fully implemented yet. Requires harness generation."

@mcp.tool()
async def inspect_gpu_kernel(code: str) -> str:
    """
    Compiles to PTX and inspects GPU kernel.
    """
    output = await clang_engine.compile_cuda(code)
    prompt = "Analyze the generated PTX/LLVM IR. Identify register pressure or divergence issues."
    return await judge.reason(code, output, prompt)

if __name__ == "__main__":
    mcp.run()
