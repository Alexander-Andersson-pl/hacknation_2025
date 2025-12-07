import time
import platform
import psutil   # pip install psutil
import json
from main import anonymize

# ---------------------------------------------------------
# Benchmark runner
# ---------------------------------------------------------
def benchmark(input_path: str, output_path: str, metrics_path: str):
    # 1. Read file contents
    full_start = time.perf_counter()
    with open(input_path, "r", encoding="utf-8") as f:
        text = f.read()

    # 2. Time the anonymizer
    processing_start = time.perf_counter()
    result = anonymize(text, False)
    processing_elapsed = time.perf_counter() - processing_start

    with open(output_path, "w", encoding="utf-8") as out:
        json.dump(result, out, indent=2, ensure_ascii=False)
    full_elapsed = time.perf_counter() - full_start

    # 3. Collect PC specs
    specs = {
        "os": platform.platform(),
        "cpu": platform.processor() or platform.machine(),
        "cores_physical": psutil.cpu_count(logical=False),
        "cores_logical": psutil.cpu_count(logical=True),
        "memory_total_gb": round(psutil.virtual_memory().total / (1024**3), 2),
        "python_version": platform.python_version()
    }

    # 4. Save output + metrics
    metrics = {
        "input_file": input_path,
        "time_seconds": full_elapsed,
        "time_processing_seconds": processing_elapsed,
        "pc_specs": specs,
    }

    with open(metrics_path, "w", encoding="utf-8") as out:
        json.dump(metrics, out, indent=2, ensure_ascii=False)

    print(f"Finished in {full_elapsed:.6f} seconds")
    print(f"Output written to: {output_path}")
    print(f"Metrics written to: {metrics_path}")



# ---------------------------------------------------------
# Main entry point
# ---------------------------------------------------------
if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Benchmark anonymizer")
    args = parser.parse_args()

    benchmark("input.txt", "output.json", "metrics.json")
