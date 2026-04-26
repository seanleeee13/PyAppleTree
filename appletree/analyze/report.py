lazy from ..utils import AppleTreeError, Color
lazy import traceback

def get_func_report(metrics, code_data, color=True):
    report = [{}, {}, []]
    if code_data["sample_cnt"] < 1000:
        report[2].append([
            f"{Color.YELLOW if color else ""}데이터의 수가 작아 분석의 정확도가 떨어지거나 틀린 분석을 할 수 있습니다.",
            f"만약 데이터의 용량이 작다면 더 큰 데이터로 다시 실행해 보셔도 좋겠습니다.{Color.END if color else ""}"
        ])
    for key in metrics["functions"].keys():
        match metrics["functions"][key]["type"]:
            case (1, 1):
                report[0][key] = [
                    f"{Color.RED + Color.BOLD if color else ""}연산 폭탄 - 순수 연산량이 많습니다. 우선적으로 수정해 주세요.",
                    f"함수가 호출되는 횟수를 줄이는 것도 방법입니다.{Color.END if color else ""}"
                ]
            case (2, 1):
                report[0][key] = [
                    f"{Color.ORANGE if color else ""}복합적 병목 - 순수 연산량도 많고, 다른 함수 호출 횟수도 많습니다. 간단한 재귀함수일 가능성이 있습니다.",
                    f"메모이제이션 등을 이용해 호출 횟수를 줄이거나 최적화를 통해 연산량을 줄여 주세요.{Color.END if color else ""}"
                ]
            case (2, 2):
                report[0][key] = [
                    f"{Color.ORANGE if color else ""}실행의 입구 - 다른 무거운 함수들을 실행시키는 입구 역할의 함수입니다.",
                    f"이 함수가 다른 함수를 호출하는 횟수를 줄이거나 이 함수가 호출하는 함수를 최적화해주세요.{Color.END if color else ""}"
                ]
            case (2, 3):
                report[0][key] = [
                    f"{Color.ORANGE if color else ""}재귀함수 - 자기 자신을 계속해서 호출하는 무거운 재귀함수일 가능성이 높습니다.",
                    f"메모이제이션이나 백트래킹 등으로 증폭도를 낮춰 보세요.{Color.END if color else ""}"
                ]
            case (3, 1):
                report[0][key] = [
                    f"{Color.YELLOW if color else ""}일꾼 - 이 코드의 대부분의 부하가 되는 핵심 함수입니다.",
                    f"만약 총 실행 시간이 오래걸린다면 이 함수도 수정해보세요.{Color.END if color else ""}"
                ]
            case (3, 2):
                report[0][key] = [
                    f"{Color.YELLOW if color else ""}잠재적 과부하 - 현재로써는 별다른 문제가 되지 않습니다.",
                    f"더 큰 데이터로 실행했을 때 문제가 생기게 될 수도 있는 함수입니다.{Color.END if color else ""}"
                ]
            case (4, 1):
                report[0][key] = [
                    f"{Color.GREEN if color else ""}정상 - 별다른 부하를 주지 않는 정상적인 함수입니다.",
                    f"데이터의 크기가 커지면 부하가 커질 수 있습니다.{Color.END if color else ""}"
                ]
    return report

def get_m_func_report(metrics, color=True):
    try:
        report = [f"{Color.PURPLE if color else ""}현재 분석된 점유율 1위:{Color.END if color else ""}", "", ""]
        top = [0, ()]
        for key in metrics["functions"].keys():
            if top[0] < metrics["functions"][key]["sample%"]:
                top = [metrics["functions"][key]["sample%"], key]
        if top == [0, ()]:
            return
        report[1] = (Color.BLUE if color else "") + key[1] + \
            (f" 함수{Color.CYAN if color else ""} /" if not key[1].startswith("<") else f"{Color.CYAN if color else ""} /")
        match metrics["functions"][key]["type"]:
            case (1, 1):
                report[2] = f"{Color.RED + Color.BOLD if color else ""}연산 폭탄 - 순수 연산량이 많습니다. " + \
                    f"우선적으로 수정해 주세요.{Color.END if color else ""}"
            case (2, 1):
                report[2] = f"{Color.RED + Color.BOLD if color else ""}복합적 병목 - 순수 연산량도 많고, " + \
                    f"다른 함수 호출 횟수도 많습니다. 간단한 재귀함수일 가능성이 있습니다.{Color.END if color else ""}"
            case (2, 2):
                report[2] = f"{Color.ORANGE if color else ""}실행의 입구 - 다른 무거운 함수들을 실행시키는 함수로, " + \
                    f"이 함수가 호출하는 함수를 수정해야 합니다.{Color.END if color else ""}"
            case (2, 3):
                report[2] = f"{Color.ORANGE if color else ""}재귀함수 - 자기 자신을 계속해서 호출하는 " + \
                    f"무거운 재귀함수일 가능성이 높습니다.{Color.END if color else ""}"
            case (3, 1):
                report[2] = f"{Color.YELLOW if color else ""}일꾼 - 이 코드의 대부분의 부하가 " + \
                    f"되는 핵심 일꾼 함수입니다.{Color.END if color else ""}"
            case (3, 2):
                report[2] = f"{Color.YELLOW if color else ""}잠재적 과부하 - 현재로써는 별다른 문제가 되지 않지만, " + \
                    f"더 큰 데이터에서 문제가 될 수 있습니다.{Color.END if color else ""}"
            case (4, 1):
                report[2] = f"{Color.GREEN if color else ""}정상 - 별다른 부하를 주지 않는 정상적인 함수입니다. " + \
                    f"데이터의 크기가 커지면 부하가 커질 수 있습니다.{Color.END if color else ""}"
        return report
    except Exception as e:
        raise AppleTreeError(
            "analyze/report#get_m_func_report.1", message="Error while func report",
            err_message=traceback.format_exc(), um=False
        ) from e

def get_line_report(metrics, report, color=True):
    top_5 = [[0, ()]] * 5
    for key in metrics["lines"].keys():
        top_5.append([metrics["lines"][key]["sample%"], key])
        top_5.sort(key=lambda k: k[0])
        top_5 = top_5[1:]
    ctop = []
    for i in top_5:
        if i != [0, []]:
            ctop.append(i)
    ctop.reverse()
    if not ctop:
        return
    for i, p in enumerate(ctop):
        match metrics["functions"][p[1][::2]]["type"]:
            case (1, 1) | (3, 1) | (3, 2):
                report[1][i + 1] = [
                    p[1],
                    f"{Color.RED + Color.BOLD if color else ""}연산 폭탄 - 이 줄의 연산량이 많습니다. 최적화를 통해 연산량을 줄여 주세요."
                ]
            case (2, 1) | (2, 2):
                report[1][i + 1] = [
                    p[1],
                    f"{Color.ORANGE if color else ""}병목 - 이 줄의 연산량이 많거나, 다른 무거운 함수를 많이 호출할 수 있습니다."
                ]
            case (2, 3):
                report[1][i + 1] = [
                    p[1],
                    f"{Color.YELLOW if color else ""}재귀함수 - 재귀함수에서 자기자신을 호출하거나 큰 연산을 하는 곳으로 예상됩니다."
                ]
            case (4, 1):
                report[1][i + 1] = [
                    p[1],
                    f"{Color.GREEN if color else ""}정상 - 이 줄은 비교적 정상적이나, 연산량이 다소 많을 수 있습니다."
                ]
    return report

def get_report(report_data, color=True):
    try:
        report = f"{Color.PURPLE + Color.BOLD if color else ""}===== PyAppleTree 분석 결과 ====={Color.END if color else ""}\n\n"
        report_overall = "\n\n".join(map(lambda k: "\n".join(k), report_data[2]))
        report += report_overall
        if report_overall.strip():
            report += "\n\n"
        report += f"{Color.CYAN + Color.BOLD if color else ""}=== 함수 분석 ==={Color.END if color else ""}\n\n"
        for key in report_data[0].keys():
            report += (Color.PURPLE if color else "") + key[1] + (" 함수:\n" if not key[1].startswith("<") else ":\n") + \
                (Color.END if color else "")
            for i in report_data[0][key]:
                report += "  " + i + "\n"
            report += "\n"
        report += f"{Color.CYAN + Color.BOLD if color else ""}=== 줄 분석 ==={Color.END if color else ""}\n\n"
        for key in report_data[1].keys():
            report += f"{Color.PURPLE if color else ""}점유율 {key}위: {Color.CYAN if color else ""}" + \
                ", ".join(map(str, report_data[1][key][0][:2])) + \
                f"번 줄 ({report_data[1][key][0][2]}{(" 함수" if not report_data[1][key][0][2].startswith("<") else "")})" + \
                (Color.END if color else "") + "\n"
            for i in report_data[1][key][1:]:
                report += "  " + i + "\n"
            report += "\n"
        report += Color.YELLOW if color else ""
        report += "코드의 종류와 목적에 따라 분석의 기준은 달라질 수 있습니다.\n"
        report += "더욱 전문적인 분석을 위해서는 전문가에게 분석받는 것을 추천드립니다.\n"
        report += Color.END if color else ""
    except Exception as e:
        raise AppleTreeError(
            "analyze/report#get_report.1", message="Error while get report",
            err_message=traceback.format_exc(), um=False
        ) from e
    return report