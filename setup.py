from pathlib import Path

from setuptools import find_packages, setup


README = Path(__file__).with_name("README.md").read_text(encoding="utf-8")


setup(
    name="kyota-cli",
    version="0.1.0",
    description="Local-first coordination CLI for the KYOTA workspace.",
    long_description=README,
    long_description_content_type="text/markdown",
    author="KYOTA",
    python_requires=">=3.9",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    package_data={"kyota": ["*.css"]},
    include_package_data=True,
    install_requires=[],
    extras_require={
        "test": ["pytest>=8.0", "textual>=8.2.0", "pytest-textual-snapshot>=1.1.0"],
        "tui": ["textual>=8.2.0"],
    },
    entry_points={
        "console_scripts": [
            "kyota=kyota.cli:main",
        ]
    },
)
