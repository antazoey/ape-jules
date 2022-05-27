#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import find_packages, setup  # type: ignore

extras_require = {
    "test": [  # `test` GitHub Action jobs uses this
        "pytest>=6.0,<7.0",  # Core testing package
        "ape-infura",
    ],
    "lint": [
        "black>=22.3.0,<23.0",  # auto-formatter and linter
        "mypy>=0.950,<1.0",  # Static type analyzer
        "flake8>=4.0.1,<5.0",  # Style linter
        "isort>=5.10.1,<6.0",  # Import sorting linter
    ],
    "dev": [
        "commitizen>=2.19,<2.20",  # Manage commits and publishing releases
        "pre-commit",  # Ensure that linters are run prior to committing
        "pytest-watch",  # `ptw` test watcher/runner
        "IPython",  # Console for interacting
        "ipdb",  # Debugger (Must use `export PYTHONBREAKPOINT=ipdb.set_trace`)
    ],
}

# NOTE: `pip install -e .[dev]` to install package
extras_require["dev"] = extras_require["test"] + extras_require["lint"] + extras_require["dev"]

with open("./README.md") as readme:
    long_description = readme.read()


setup(
    name="ape-jules",
    use_scm_version=True,
    setup_requires=["setuptools_scm"],
    description="""ape-jules: Jules' custom Ethereum tooling""",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="ApeWorX Ltd.",
    author_email="juliya@juliyasmith.com",
    url="https://github.com/unparalleled-js/ape-jules",
    include_package_data=True,
    install_requires=[
        "eth-ape>=0.1.0b5",
        "click>=8.1.3,<9",
        "rich>=10.16.2,<11"
        "importlib-metadata ; python_version<'3.8'",
    ],  # NOTE: Add 3rd party libraries here
    entry_points={
        "ape_cli_subcommands": [
            "ape_jules=ape_jules._cli:cli",
        ],
    },
    python_requires=">=3.7.2,<4",
    extras_require=extras_require,
    py_modules=["ape_jules"],
    license="Apache-2.0",
    zip_safe=False,
    keywords="ethereum",
    packages=find_packages(exclude=["tests", "tests.*"]),
    package_data={"ape_jules": ["py.typed"]},
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: MacOS",
        "Operating System :: POSIX",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
)
