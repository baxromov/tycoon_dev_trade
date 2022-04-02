import pathlib

from setuptools import setup, find_packages

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()
with open('requirements.txt') as f:
    required = f.read().splitlines()
# This call to setup() does all the work

setup(
    name="tycoon-dev-trade",
    version='0.0.2',
    author="Baxromov",
    description="Don't use it in a real account.",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "trade_iqoption"},
    packages=find_packages(where="trade_iqoption"),
    dependency_links=[
        'https://github.com/iqoptionapi/iqoptionapi/archive/refs/heads/master.zip#egg=iqoptionapi',
    ],
    install_requires=['iqoptionapi'],
    python_requires=">=3.6",
    include_package_data=True,
    long_description_content_type="text/markdown",
    long_description="Don't use it in a real account.",
)
