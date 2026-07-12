"""Launch script for the AI Resume Analyzer application."""

import subprocess
import sys


def main() -> None:
    """Start the Streamlit application."""
    subprocess.run(
        [sys.executable, "-m", "streamlit", "run", "app/main.py"],
        check=True,
    )


if __name__ == "__main__":
    main()
