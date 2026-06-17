# PyAppleTree 버전 1.0.0a0.dev8

[![Version](https://img.shields.io/badge/pypi-v1.0.0a0.dev8-orange)](https://pypi.org/project/PyAppleTree)
[![Python Version](https://img.shields.io/badge/python-3.15+-blue)](https://pypi.org/project/PyAppleTree)
[![License](https://img.shields.io/badge/license-MIT-white)](https://pypi.org/project/PyAppleTree)

> **Python Runtime Overall Operating Toolkit**

> Analyze, Prepare, Profile, Log, Explain.

## 특징

- 프로젝트 프로파일링
    - 파이썬 내장 패키지 `profiling.sampling`을 사용함으로써 이 프로그램은 의존성이 없고, 코드 수정이 필요 없으며, 오버헤드가 매우 적습니다.
- 번역
    - 이 프로그램은 뛰어난 번역 기능을 가지고 있습니다.
    - 이 프로그램은 현재 한국어를 지원합니다. (영어는 아직 지원하지 않습니다.)

## 추후 계획

- 영어, 스페인어 등의 지원 추가
- VSCode 확장 제작

## 설치

```
pip install PyAppleTree
```
```
pip install PyAppleTree==1.0.0a0.dev8
```
```
pip install git+https://github.com/seanleeee13/PyAppleTree.git
```

## 사용법

```
# 기본 모드
python -m appletree analyze test.py
```
```
# 상세 분석 모드
python -m appletree analyze -a test.py
```

## 오류 제보 및 기능 제안

불편한 점이나 개선 사항은 https://github.com/seanleeee13/PyAppleTree/issues/new 로 제출해 주세요.