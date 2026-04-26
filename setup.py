from setuptools import setup, find_packages

setup(
    name="PyRoot",
    version="1.0.0",
    packages=find_packages(exclude=[".vscode", "test"]),
    python_requires=">=3.15",
    install_requires=[],
    entry_points={
        "console_scripts": [
            "pyroot=pyroot.__main__:main",
            "PyRoot=pyroot.__main__:main"
        ],
    },
    author="seanleeee13",
    description="Python Runtime Overall Operating Toolkit"
)