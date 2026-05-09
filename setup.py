from setuptools import setup

setup(
    name="PyAppleTree",
    version="1.0.0",
    packages=["appletree"],
    python_requires=">=3.15",
    install_requires=[],
    entry_points={
        "console_scripts": [
            "pyappletree=appletree.__main__:main",
            "appletree=appletree.__main__:main",
        ],
    },
    author="seanleeee13",
    description="Python Runtime Overall Operating Toolkit / Analyze, Prepare, Profile, Log, Explain"
)