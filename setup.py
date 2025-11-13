from setuptools import setup, find_packages
from pathlib import Path

# Read README.md
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name="glayout",
    version="0.1.3",
    description="A PDK-agnostic layout automation framework for analog circuit design",
    long_description=long_description,
    long_description_content_type="text/markdown", 
    author="OpenFASOC Team",
    author_email="mehdi@umich.edu",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    include_package_data=True,
    install_requires=[
        "gdsfactory>=9.0.0",
        "numpy>1.21.0,<=1.24.0",
        "prettyprint",
        "prettyprinttree",
        "gdstk",
        "svgutils"
    ],
    python_requires=">=3.10",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Electronic Design Automation (EDA)",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.10",
    ],
)
