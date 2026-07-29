import sys
import subprocess

if __name__ == '__main__':
    result = subprocess.run(["/home/jules/.pyenv/versions/3.12.13/bin/pytest", "gs_quant/test/analytics/"], capture_output=True, text=True)
    print(result.stdout)
    if result.returncode != 0:
        print(f"Error running tests! Return code: {result.returncode}")
