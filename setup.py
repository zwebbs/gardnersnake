import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="gardnersnake",
    version="0.2.1",
    author="Zach Weber",
    author_email="zach.weber.813@gmail.com",
    description="Utilities for writing concise snakemake workflows",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/zwebbs/gardnersnake",
    project_urls={
        "Bug Tracker": "https://github.com/zwebbs/gardnersnake/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.7",
    install_requires=['pyyaml==6.0', 'jsonschema==4.4.0'],
    entry_points={'console_scripts': {
        'check_directory=scripts.check_directory:main'}
    }
)
