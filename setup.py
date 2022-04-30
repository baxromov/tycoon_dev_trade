import pathlib

from setuptools import setup, find_packages

HERE = pathlib.Path(__file__).parent

README = (HERE / "README.md").read_text()

setup(
    name="tycoon-dev-trade",
    version='0.0.7',
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
