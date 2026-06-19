# PyAppleTree: 유저 친화적 프로파일링 / 디버깅 툴킷

[![PyPI version](https://img.shields.io/pypi/v/PyAppleTree.svg)](https://pypi.org)
[![Supported Python versions](https://img.shields.io/pypi/pyversions/PyAppleTree.svg)](https://pypi.org)
[![License](https://img.shields.io/pypi/l/PyAppleTree)](https://pypi.org)

> **Python Runtime Overall Operating Toolkit**
> Analyze, Prepare, Profile, Log, Explain.
---

**"지루한 숫자 가득한 분석도, 불친절한 에러 로그도 이제 끝났습니다."**  
PyAppleTree는 AI처럼 똑똑한 수학적 알고리즘으로 의미 있는 병목 구간만 동적으로 진단하고, 상세한 유저 친화적 리포트로 보여주는 파이썬 전용 프로파일링 / 디버깅 툴킷입니다.

## 핵심 특징

- 상세한 프로파일링 (코드 분석)
    - 3.15 내장 샘플링 프로파일러 패키지 `profiling.sampling`을 이용해 의존성 설치, 코드 수정, 오버헤드 없이 빠르게 코드를 분석할 수 있습니다.
    - 유저 친화적인 지능형 상세 리포트를 통해 더 쉽고 빠르게 병목을 찾을 수 있습니다.
- 유저 친화적 에러 번역 (예정)
    - 읽기 불편한 영문 에러 메세지를 유저 친화적 문제 해결 방안으로 펼쳐냅니다.

## 왜 PyAppleTree인가요?

- `py-spy`와 대등한 7%의 프로파일링 오버헤드
    - `profiling.sampling`의 C언어 레벨 구현
- **유저 친화적** 리포트와 **지능형** 알고리즘

## 추후 계획

- 영어, 스페인어 등의 지원 추가
- VSCode 익스텐션 제작
- 더욱 많은 계획과 수정 예정 버그, 예정된 기능 등에 대해서는 [추후 계획 문서](./future/future.md)를 확인해 주세요.

## 설치하기

다음 명령어 중 하나를 실행해 PyAppleTree를 설치하세요.

````{tab-set}
```{tab-item} pip
```bash
pip install PyAppleTree
```
```
```{tab-item} pipx
```bash
pipx install PyAppleTree
```
```
```{tab-item} uv
```bash
uv tool install PyAppleTree
```
```
```{tab-item} poetry
```bash
poetry self add PyAppleTree
```
```
````

더욱 자세한 내용은 [시작하기 문서](./start/quickstart.md)를 참고해 주세요.

## 오류 제보 및 기능 제안

불편한 점이나 개선 사항은 https://github.com/seanleeee13/PyAppleTree/issues/new 로 제출해 주세요.

최신 변경사항은 [신규 기능 문서](./update/whatsnew/1.0.0.md)와 [변경 기록 문서](./update/changelog.md)에서 확인할 수 있습니다.

```{toctree}
:maxdepth: 2
:caption: 시작하기
:hidden:
start/quickstart
start/learn
```

```{toctree}
:maxdepth: 2
:caption: 기능 알아보기
:hidden:
성능 분석 (appletree analyze) <api/cli/analyze>
```

```{toctree}
:maxdepth: 2
:caption: 업데이트 소식
:hidden:
update/1.0.0
update/changelog
```