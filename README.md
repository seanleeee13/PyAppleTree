# PyAppleTree version 1.0.0a0.dev5

[![Version](https://img.shields.io/badge/pypi-v1.0.0a0.dev5-orange)](https://pypi.org/project/PyAppleTree)
[![Python Version](https://img.shields.io/badge/python-3.15+-blue)](https://pypi.org/project/PyAppleTree)
[![License](https://img.shields.io/badge/license-MIT-white)](https://pypi.org/project/PyAppleTree)

> **Python Runtime Overall Operating Toolkit**
> Analyze, Prepare, Profile, Log, Explain.

## Features

- Profiling projects
    - By using python built-in `profiling.sampling` package, this program has no requirements, requires zero modification, and has low overhead.
- Translation
    - This program has outstanding translation.
    - This program supports Korean. (No English yet; sorry)

## Install

```
pip install PyAppleTree --pre
```
```
pip install PyAppleTree==1.0.0a0.dev4
```
```
pip install git+https://github.com/seanleeee13/PyAppleTree.git
```

## Usage

```
# Basic mode
python -m appletree analyze test.py
```
```
# Advanced mode
python -m appletree analyze -a test.py
```

## Issues

Please report issues into https://github.com/seanleeee13/PyAppleTree/issues/new