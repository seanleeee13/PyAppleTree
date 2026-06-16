translate_data = {
    "analyze_data_count": [
        "<yellow>데이터의 수가 적어 분석의 정확도가 떨어지거나 틀린 분석을 할 수 있습니다.<end>",
        "<yellow>만약 데이터의 용량이 작다면 더 큰 데이터로 다시 실행해 보셔도 좋겠습니다.<end>"
    ],
    "analyze_freport_1_1": [
        "<red><bold>연산 폭탄 - 순수 연산량이 많습니다. 우선적으로 수정해 주세요.<end>",
        "<red><bold>함수가 호출되는 횟수를 줄이는 것도 방법입니다.<end>"
    ],
    "analyze_freport_2_1": [
        "<orange><bold>복합적 병목 - 순수 연산량도 많고, 다른 함수 호출 횟수도 많습니다. 간단한 재귀함수일 가능성이 있습니다.<end>",
        "<orange><bold>메모이제이션 등을 이용해 호출 횟수를 줄이거나 최적화를 통해 연산량을 줄여 주세요.<end>"
    ],
    "analyze_freport_2_2": [
        "<orange><bold>실행의 입구 - 다른 무거운 함수들을 실행시키는 입구 역할의 함수입니다.<end>",
        "<orange><bold>이 함수가 다른 함수를 호출하는 횟수를 줄이거나 이 함수가 호출하는 함수를 최적화해주세요.<end>"
    ],
    "analyze_freport_2_3": [
        "<orange><bold>재귀함수 - 자기 자신을 계속해서 호출하는 무거운 재귀함수일 가능성이 높습니다.<end>",
        "<orange><bold>메모이제이션이나 백트래킹 등으로 증폭도를 낮춰 보세요.<end>"
    ],
    "analyze_freport_3_1": [
        "<yellow>일꾼 - 이 코드의 25~60% 정도의 부하가 되는 핵심 함수입니다.<end>",
        "<yellow>만약 총 실행 시간이 오래걸린다면 이 함수도 수정해보세요.<end>"
    ],
    "analyze_freport_3_2": [
        "<yellow>잠재적 과부하 - 현재로써는 별다른 문제가 되지 않습니다.<end>",
        "<yellow>더 큰 데이터로 실행했을 때 문제가 생기게 될 수도 있는 함수입니다.<end>"
    ],
    "analyze_freport_4_1": [
        "<green>정상 - 별다른 부하를 주지 않는 정상적인 함수입니다.<end>",
        "<green>데이터의 크기가 커지면 부하가 커질 수 있습니다.<end>"
    ],
    "analyze_mfreport_title": "<purple>현재 분석된 점유율 1위:<end>",
    "analyze_mfreport_func": "<blue>%(func)s<!br= 함수><end>",
    "analyze_mfreport_1_1": "<red><bold>(점유율: %(rate).1f%%)<end> <cyan>/<end> " + \
        "<red><bold>연산 폭탄 - 순수 연산량이 많습니다. 우선적으로 수정해 주세요.<end>",
    "analyze_mfreport_2_1": "<orange><bold>(점유율: %(rate).1f%%)<end> <cyan>/<end> " + \
        "<orange><bold>복합적 병목 - 순수 연산량도 많고, 다른 함수 호출 횟수도 많습니다. 간단한 재귀함수일 가능성이 있습니다.<end>",
    "analyze_mfreport_2_2": "<orange><bold>(점유율: %(rate).1f%%)<end> <cyan>/<end> " + \
        "<orange><bold>실행의 입구 - 다른 무거운 함수들을 실행시키는 함수로, 이 함수가 호출하는 함수를 수정해야 합니다.<end>",
    "analyze_mfreport_2_3": "<orange><bold>(점유율: %(rate).1f%%)<end> <cyan>/<end> " + \
        "<orange><bold>재귀함수 - 자기 자신을 계속해서 호출하는 무거운 재귀함수일 가능성이 높습니다.<end>",
    "analyze_mfreport_3_1": "<yellow>(점유율: %(rate).1f%%)<end> <cyan>/<end> " + \
        "<yellow>일꾼 - 이 코드의 25~60%% 정도의 부하가 되는 핵심 일꾼 함수입니다.<end>",
    "analyze_mfreport_3_2": "<yellow>(점유율: %(rate).1f%%)<end> <cyan>/<end> " + \
        "<yellow>잠재적 과부하 - 현재로써는 별다른 문제가 되지 않지만, 더 큰 데이터에서 문제가 될 수 있습니다.<end>",
    "analyze_mfreport_4_1": "<green>(점유율: %(rate).1f%%)<end> <cyan>/<end> " + \
        "<green>정상 - 별다른 부하를 주지 않는 정상적인 함수입니다. 데이터의 크기가 커지면 부하가 커질 수 있습니다.<end>",
    "analyze_lreport_overload": "<red><bold>연산 폭탄 - 이 줄의 연산량이 많습니다. 최적화를 통해 연산량을 줄여 주세요.<end>",
    "analyze_lreport_large": "<orange><bold>병목 - 이 줄의 연산량이 많거나, 다른 무거운 함수를 많이 호출하고 있습니다. 재귀함수일 수도 있습니다.<end>",
    "analyze_lreport_recursion": "<yellow>일꾼 - 적당한 정도의 부하가 되는 줄입니다. '연산 폭탄'과 '병목'을 고친 후에도 느리다면 고쳐 보세요.<end>",
    "analyze_lreport_normal": "<green>정상 - 이 줄은 비교적 정상적이나, 연산량이 다소 많을 수 있습니다.<end>",
    "analyze_report_title": "<purple><bold>===== PyAppleTree 분석 결과 =====<end>\n\n",
    "analyze_freport_title": "<cyan><bold>=== 함수 분석 ===<end>\n\n",
    "analyze_freport_func": "<purple>점유율 %(rank)d위: <cyan>%(location)s, %(func)s<!br= 함수><end>",
    "analyze_lreport_title": "<cyan><bold>=== 줄 분석 ===<end>\n\n",
    "analyze_lreport_line_rank": "<purple>점유율 %(rank)d위:<cyan> ",
    "analyze_lreport_line": "%(line)d번 줄 ",
    "analyze_lreport_line_func": "(%(func)s<!br= 함수>)<end>\n",
    "analyze_sample_rate_1": "<red><bold>점유율: %(sample_rate).1f%%<end>",
    "analyze_sample_rate_2": "<orange><bold>점유율: %(sample_rate).1f%%<end>",
    "analyze_sample_rate_3": "<yellow>점유율: %(sample_rate).1f%%<end>",
    "analyze_sample_rate_4": "<green>점유율: %(sample_rate).1f%%<end>",
    "analyze_cumulative_rate_1": "<red><bold>, 스택 점유율: %(cumulative_rate).1f%%<end>",
    "analyze_cumulative_rate_2": "<orange><bold>, 스택 점유율: %(cumulative_rate).1f%%<end>",
    "analyze_cumulative_rate_3": "<yellow>, 스택 점유율: %(cumulative_rate).1f%%<end>",
    "analyze_cumulative_rate_4": "<green>, 스택 점유율: %(cumulative_rate).1f%%<end>",
    "analyze_mcumulative_rate_1": "<red><bold>, 다중 스택 점유율: %(mcumulative_rate).1f%%<end>",
    "analyze_mcumulative_rate_2": "<orange><bold>, 다중 스택 점유율: %(mcumulative_rate).1f%%<end>",
    "analyze_mcumulative_rate_3": "<yellow>, 다중 스택 점유율: %(mcumulative_rate).1f%%<end>",
    "analyze_mcumulative_rate_4": "<green>, 다중 스택 점유율: %(mcumulative_rate).1f%%<end>",
    "analyze_magnification_1": "<red><bold>, 증폭률: %(magnification).1f<end>",
    "analyze_magnification_2": "<orange><bold>, 증폭률: %(magnification).1f<end>",
    "analyze_magnification_3": "<yellow>, 증폭률: %(magnification).1f<end>",
    "analyze_magnification_4": "<green>, 증폭률: %(magnification).1f<end>",
    "analyze_smagnification_1": "<red><bold>, 스택 증폭률: %(smagnification).1f<end>",
    "analyze_smagnification_2": "<orange><bold>, 스택 증폭률: %(smagnification).1f<end>",
    "analyze_smagnification_3": "<yellow>, 스택 증폭률: %(smagnification).1f<end>",
    "analyze_smagnification_4": "<green>, 스택 증폭률: %(smagnification).1f<end>",
    "analyze_report_warning": [
        "<yellow>코드의 종류와 목적에 따라 분석의 기준은 달라질 수 있습니다.<end>\n",
        "<yellow>더욱 전문적인 분석을 위해서는 전문가에게 분석받는 것을 추천드립니다.<end>\n"
    ],
    "analyze_mfreport_ntitle": "<blue>#%(cnt)d %(time)s<cyan>%(slash)s<end>%(msg_part)s",
    "analyze_run_no_target": "타겟 파일 %(target_file)s가 존재하지 않습니다.",
    "analyze_run_no_input": "입력 파일 %(input_file)s가 존재하지 않습니다.",
    "analyze_run_no_data": "각각의 실행이 너무 빨리 끝나 데이터가 모이지 않았습니다. 더 큰 입력값으로 시도해 보아도 좋을 것 같습니다.",
    "analyze_error": "분석 도중 타겟 코드에서 에러가 일어났습니다:\n%(error_message)s",
    "analyze_data_count_show": "<blue>샘플 개수: %(cnt)d개<end>"
}