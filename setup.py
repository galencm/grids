from setuptools import find_packages, setup

setup(
    name="grids",
    version="0.1",
    description="",
    author="Galen Curwen-McAdams",
    author_email="",
    platforms=["any"],
    license="Mozilla Public License 2.0 (MPL 2.0)",
    include_package_data=True,
    url="",
    packages=find_packages(),
    install_requires=["Kivy", "Pillow", "xdg", "redis", "pre-commit"],
    entry_points={
        "console_scripts": ["gg = grids.grid:main", "grids = grids.grid:main"]
    },
)
