# 더 알아보기

- `appletree -v` `appletree --version`으로 PyAppleTree의 버전을 확인할 수 있습니다.

## 성능 분석 (`appletree analyze`)

### 명령줄 인자

- `-i FILE` `--input FILE`을 통해 입력값을 설정할 수 있습니다. [더 알아보기](../api/cli/analyze#-i-FILE---input-FILE)
- `-C` `--uncolored`를 통해 글자 색이 없는 리포트를 볼 수 있습니다. [더 알아보기](../api/cli/analyze#-C---uncolored)
- `-L` `--without-log`를 통해 실시간 로그를 없앨 수 있습니다. [더 알아보기](../api/cli/analyze#-L---without-log)
- `-a` `--advanced`를 통해 상세 분석 모드를 사용할 수 있습니다. [더 알아보기](../api/cli/analyze#-a---advanced)
- `-m` `--metrics`로 스택 점유율, 증폭률 등 상세 통계를 확인할 수 있습니다. [더 알아보기](../api/cli/analyze#-m---metrics)
- `-T TIME` `--min-time TIME`으로 최소 실행 시간을 설정할 수 있습니다. [더 알아보기](../api/cli/analyze#-T-TIME---min-time-TIME)
- `-e` `--include-external`로 타겟 파일이 있는 디렉토리 외부의 파일에 있는 함수도 분석에 포함시킬 수 있습니다. [더 알아보기](../api/cli/analyze#-e---include-external)
- `-l` `--lab`으로 실험 기능을 체험할 수 있습니다. (아직 실험 기능이 없습니다.) [더 알아보기](../api/cli/analyze#-l---lab)
- 자세한 내용은 [성능 분석 문서](../api/cli/analyze)에서 확인할 수 있습니다.

### 통계 수치

- 점유율 (sample%): 프로그램 총 실행 시간 대비 해당 함수 / 줄이 실행되는 시간입니다.
- 스택 점유율 (culmulative%): 프로그램 총 실행 시간 대비 해당 함수 / 줄이 스택에 있는 시간입니다.
- 증폭률 (magnification): 해당 함수 / 줄의 점유율 대비 스택 점유율입니다.
- 다중 스택 점유율 (multi-culmilative%): 스택 점유율과 같지만 스택에 중복해서 있었을 경우 그 횟수를 스택 점유율에 곱합니다. `100%`를 넘어갈 수 있으며 이는 버그가 아닙니다.
- 스택 증폭률 (stack magnification): 재귀함수를 확인하기 위해 만들어진 수치입니다. 해당 함수 / 줄의 점유율 대비 다중 스택 점유율로 계산됩니다.