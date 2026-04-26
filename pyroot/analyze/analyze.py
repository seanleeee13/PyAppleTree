lazy from .run import analyze_new
lazy from .metrics import get_metrics
lazy from .report import get_func_report, get_line_report, get_report
lazy from ..utils import PyRootError
lazy import traceback

_run = analyze_new
_metrics = get_metrics

def _report(metrics, code_data, color=True):
    func_report = get_func_report(metrics, code_data, color)
    line_report = get_line_report(metrics, func_report, color)
    return get_report(line_report, color)

def _analyze(filename, input_file=None, detailed=False, log=True, color=True):
    try:
        metrics_data = _metrics(_run(filename, input_file, detailed, log, color), filename, detailed)
        report_data = _report(*metrics_data, color)
        return report_data
    except PyRootError:
        raise
    except Exception:
        raise PyRootError("analyze/analyze#_analyze.1", message="Error while analyze", err_message=traceback.format_exc(), um=False)