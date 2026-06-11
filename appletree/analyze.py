lazy from .utils import tempfile_wrapper, clean, AppleTreeError, safe_open
lazy from profiling.sampling.binary_collector import BinaryCollector
lazy from profiling.sampling.cli import _handle_run, COLLECTOR_MAP
lazy from contextlib import redirect_stdout, redirect_stderr
lazy from collections import Counter
lazy from unittest.mock import patch
lazy from .locales import _, _e
lazy import subprocess
lazy import traceback
lazy import time
lazy import sys
lazy import os
lazy import io

class SampleArgs:
    def __init__(self, target, outfile):
        self.command = "run"
        self.target = target
        self.outfile = outfile
        self.format = "binary"
        self.sample_interval_usec = 1000
        self.mode = "wall"
        self.module = False
        self.args = []
        self.live = False
        self.duration = None
        self.all_threads = True
        self.opcodes = False
        self.native = False
        self.gc = True
        self.blocking = False
        self.realtime_stats = False
        self.async_mode = None
        self.async_aware = False
        self.diff_baseline = None

class AppleTreeBinaryCollector(BinaryCollector):
    _appletree_cnt = 0
    _appletree_start_t = 0.0
    _appletree_msg = ""
    _appletree_msg_len = 0
    _appletree_samples = []
    _appletree_log = True
    _appletree_target = ""
    _appletree_inc_ext = False
    _appletree_color = True
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    def collect(self, stack_frames, timestamp_us=None):
        if self._appletree_log:
            self._appletree_cnt += 1
            if self._appletree_cnt % 50 == 0:
                lst = get_m_func_report(get_metrics(
                    self._appletree_samples, self._appletree_target,
                    self._appletree_inc_ext)[0], self._appletree_color
                )
                if lst:
                    self._appletree_msg = " ".join(lst)
            seconds = int(time.perf_counter() - self._appletree_start_t)
            hours, remainder = divmod(seconds, 3600)
            minutes, seconds = divmod(remainder, 60)
            message = "\r" + _("analyze_mfreport_ntitle", self._appletree_color) % {
                "cnt": self._appletree_cnt,
                "time": f"{hours:02d}:{minutes:02d}:{seconds:02d}",
                "slash": " / " if self._appletree_msg.strip() else "",
                "msg_part": self._appletree_msg
            }
            self._appletree_msg_len = len(message)
            sys.__stdout__.write(message)
        try:
            for interp in stack_frames:
                for thread in interp.threads:
                    if not thread.frame_info:
                        continue
                    top = thread.frame_info[0]
                    if top.filename == "~" or top.location is None:
                        continue
                    current_loc = [top.filename, top.location[0], top.funcname]
                    full_stack = []
                    for frame in thread.frame_info:
                        if frame.filename == "~" or frame.location is None:
                            continue
                        full_stack.append([
                            frame.filename,
                            frame.location[0],
                            frame.funcname
                        ])
                    self._appletree_samples.append([*current_loc, full_stack])
        except:
            sys.__stdout__.write(traceback.format_exc() + str(stack_frames))
        return super().collect(stack_frames, timestamp_us)

used_prbc = None
prbc_args = None
prbc_kwargs = None

def get_prbc(log=True, color=True):
    def _get_prbc(*args, **kwargs):
        global used_prbc, prbc_args, prbc_kwargs
        if not used_prbc or prbc_args != args or prbc_kwargs != kwargs:
            _used_prbc = AppleTreeBinaryCollector(*args, **kwargs)
            _used_prbc._appletree_log = log
            _used_prbc._appletree_color = color
            if used_prbc:
                _used_prbc._appletree_cnt = used_prbc._appletree_cnt
                _used_prbc._appletree_start_t = used_prbc._appletree_start_t
                _used_prbc._appletree_msg = used_prbc._appletree_msg
                _used_prbc._appletree_msg_len = used_prbc._appletree_msg_len
                _used_prbc._appletree_samples = used_prbc._appletree_samples
                _used_prbc._appletree_target = used_prbc._appletree_target
                _used_prbc._appletree_inc_ext = used_prbc._appletree_inc_ext
            used_prbc = _used_prbc
            prbc_args = args
            prbc_kwargs = kwargs
        return used_prbc
    return _get_prbc

def clean_prbc():
    global used_prbc, prbc_args, prbc_kwargs
    used_prbc = None
    prbc_args = None
    prbc_kwargs = None

def sample(target_file, input_file, output_file="output.prof", log=True, color=True):
    if not os.path.exists(target_file):
        raise AppleTreeError(
            "analyze/run#sample.2", message=_("analyze_run_no_target") % {"target_file": target_file},
            err_message="FileNotFoundError", um=True
        )
    if not os.path.exists(output_file):
        raise AppleTreeError(
            "analyze/run#sample.3", message=f"Output File No Exist",
            err_message="FileNotFoundError", um=False
        )
    if input_file and not os.path.exists(input_file):
        raise AppleTreeError(
            "analyze/run#sample.4", message=_("analyze_run_no_input") % {"input_file": input_file},
            err_message="FileNotFoundError", um=True
        )
    target_file = target_file.replace("/", "\\")
    Popen = subprocess.Popen
    with patch("subprocess.Popen") as mocked_popen, safe_open(input_file, "r") as in_f:
        r, w = os.pipe()
        def popen_side_effect(cmd, **kw):
            kw["stdout"] = subprocess.DEVNULL
            kw["stderr"] = w
            kw["stdin"] = in_f if in_f else subprocess.DEVNULL
            return Popen(cmd, **kw)
        mocked_popen.side_effect = popen_side_effect
        COLLECTOR_MAP["binary"] = get_prbc(log, color)
        try:
            f = io.StringIO()
            with redirect_stdout(f), redirect_stderr(f):
                _handle_run(SampleArgs(target_file, output_file))
            os.close(w)
            error_bytes = os.read(r, 1024 * 1024)
            os.close(r)
            error_msg = error_bytes.decode("utf-8", errors="ignore")
            if error_msg.strip():
                raise AppleTreeError(
                    "analyze/run#sample.5", message=_("analyze_error") % {"error_message": _e(error_msg, color=True)},
                    err_message=_e(error_msg, color=True), um=True
                )
            if "Interrupted by user." in f.getvalue():
                raise KeyboardInterrupt
        except KeyboardInterrupt:
            raise
        except SystemExit:
            pass
        except AppleTreeError:
            raise
        except Exception as e:
            raise AppleTreeError(
                "analyze/run#sample.1", message="Error while sample _handle_run",
                err_message=traceback.format_exc(), um=False
            ) from e
        finally:
            COLLECTOR_MAP["binary"] = BinaryCollector
            try:
                os.close(w)
            except:
                pass
            try:
                os.close(r)
            except:
                pass
    return output_file

def sample_tempfile(target_file, input_file=None, log=True, color=True):
    return tempfile_wrapper(sample, target_file, input_file, log, color, index=2)

def analyze_new(filename, input_file, inc_ext=False, log=True, color=True, min_time=5):
    try:
        start = time.perf_counter()
        AppleTreeBinaryCollector._appletree_start_t = start
        AppleTreeBinaryCollector._appletree_target = filename
        AppleTreeBinaryCollector._appletree_inc_ext = inc_ext
        error_count = 0
        while time.perf_counter() - start <= min_time:
            ret = None
            try:
                ret = sample_tempfile(filename, input_file, log, color)
            finally:
                clean(ret)
            if len(used_prbc._appletree_samples) == 0:
                error_count += 1
                if error_count >= 50:
                    break
        if log:
            print("\r" + " " * 175 + "\r", end="")
        return used_prbc._appletree_samples
    except KeyboardInterrupt:
        if log:
            print("\r" + " " * 175 + "\r", end="")
        return used_prbc._appletree_samples
    except AppleTreeError:
        print("\r" + " " * 175 + "\r", end="")
        raise
    except Exception as e:
        print("\r" + " " * 175 + "\r", end="")
        raise AppleTreeError("analyze/run#analyze_new.1", message="Error while sampling", err_message=traceback.format_exc(), um=False) from e
    finally:
        clean_prbc()

def filter_samples(samples, inc_ext=False):
    cwd = os.getcwd()
    normal_count = Counter()
    stack_count = Counter()
    normal_count_func = Counter()
    stack_count_func = Counter()
    for loc in samples:
        if inc_ext or loc[0].startswith(cwd):
            lloc = tuple(loc[:3])
            floc = tuple(loc[::2])
            normal_count[lloc] += 1
            normal_count_func[floc] += 1
            stack_count[lloc] += 1
            stack_count_func[floc] += 1
        for subloc in set(map(tuple, loc[3])) - set([tuple(loc[:3])]):
            if inc_ext or subloc[0].startswith(cwd):
                lsloc = tuple(subloc[:3])
                fsloc = tuple(subloc[::2])
                stack_count[lsloc] += 1
                stack_count_func[fsloc] += 1
    return frozendict({
            "normal cnt": normal_count, "stack cnt": stack_count,
            "normal fcnt": normal_count_func, "stack fcnt": stack_count_func
        })

def get_ftype(fdata):
    if fdata["sample%"] >= 75 and fdata["magnification"] <= 1.1:
        return (1, 1)
    elif 75 > fdata["sample%"] >= 60 and fdata["magnification"] <= 1.15:
        return (1, 1)
    elif 60 > fdata["sample%"] >= 25 and fdata["magnification"] <= 1.25:
        return (3, 1)
    elif 25 > fdata["sample%"] >= 10 and 1.25 >= fdata["magnification"] > 1.15:
        return (3, 2)
    elif fdata["sample%"] >= 75 and 1.25 >= fdata["magnification"] > 1.1:
        return (2, 1)
    elif fdata["sample%"] >= 60 and 1.225 >= fdata["magnification"] > 1.15:
        return (2, 1)
    elif fdata["sample%"] >= 40 and 1.5 > fdata["magnification"] > 1.25:
        return (2, 1)
    elif fdata["sample%"] < 40 and fdata["magnification"] > 1.25:
        return (2, 2)
    elif fdata["sample%"] >= 40 and fdata["magnification"] >= 1.5:
        return (2, 3)
    elif fdata["sample%"] >= 60 and fdata["magnification"] >= 1.225:
        return (2, 3)
    elif fdata["sample%"] >= 75 and fdata["magnification"] >= 1.25:
        return (2, 3)
    else:
        return (4, 1)

def get_metrics(samples, inc_ext=False):
    try:
        sample_counter = filter_samples(samples, inc_ext)
        metrics = {"lines": {}, "functions": {}}
        code_data = {"sample_cnt": sum(sample_counter["normal cnt"].values())}
        sum_ncnt = sum(sample_counter["normal cnt"].values())
        sum_fncnt = sum(sample_counter["normal fcnt"].values())
        for loc in sample_counter["stack cnt"].keys():
            loc2 = loc[::2]
            ncnt = sample_counter["normal cnt"].get(loc, 0)
            scnt = sample_counter["stack cnt"].get(loc, 0)
            fncnt = sample_counter["normal fcnt"].get(loc2, 0)
            fscnt = sample_counter["stack fcnt"].get(loc2, 0)
            metrics["lines"][loc] = {
                "samples": ncnt,
                "cumulatives": scnt,
                "sample%": 100 * ncnt / sum_ncnt if sum_ncnt else 2147483647.0 if ncnt else 0.0,
                "cumulative%": 100 * scnt / sum_ncnt if sum_ncnt else 2147483647.0 if scnt else 0.0
            }
            metrics["functions"][loc2] = {
                "samples": fncnt,
                "cumulatives": fscnt,
                "sample%": 100 * fncnt / sum_fncnt if sum_fncnt else 2147483647.0 if fncnt else 0.0,
                "cumulative%": 100 * fscnt / sum_fncnt if sum_fncnt else 2147483647.0 if fscnt else 0.0,
                "magnification": fscnt / fncnt if fncnt else 2147483647.0 if fscnt else 0.0
            }
            metrics["functions"][loc2]["type"] = get_ftype(metrics["functions"][loc2])
    except KeyboardInterrupt:
        raise
    except AppleTreeError:
        raise
    except Exception as e:
        raise AppleTreeError(
            "analyze/metrics#get_metrics.1", message="Error while calculating metrics",
            err_message=traceback.format_exc(), um=False
        ) from e
    return metrics, code_data

def get_func_report(metrics, code_data, color=True):
    report = [{}, {}, []]
    if code_data["sample_cnt"] < 1000:
        report[2].append(_("analyze_data_count", color))
    keys = list(metrics["functions"].keys())
    keys.sort(key=lambda k: metrics["functions"][k]["sample%"], reverse=True)
    for idx, key in enumerate(keys):
        data = metrics["functions"][key]["type"]
        report[0][key] = [_(f"analyze_freport_{data[0]}_{data[1]}", color), idx + 1, metrics["functions"][key]["sample%"], data[0]]
        report[0][key].append(metrics["functions"][key]["cumulative%"])
        report[0][key].append(metrics["functions"][key]["magnification"])
    return report

def get_m_func_report(metrics, color=True):
    try:
        report = [_("analyze_mfreport_title", color), "", ""]
        top = [0, ()]
        for key in metrics["functions"].keys():
            if top[0] < metrics["functions"][key]["sample%"]:
                top = [metrics["functions"][key]["sample%"], key]
        if top == [0, ()]:
            return
        data = metrics["functions"][key]["type"]
        report[1] = _("analyze_mfreport_func", color) % {"func": key[1], "br": key[1]}
        report[2] = _(f"analyze_mfreport_{data[0]}_{data[1]}", color) % {"rate": float(metrics["functions"][key]["sample%"])}
        return report
    except KeyboardInterrupt:
        raise
    except Exception as e:
        raise AppleTreeError(
            "analyze/report#get_m_func_report.1", message="Error while func report",
            err_message=traceback.format_exc(), um=False
        ) from e

def get_line_report(metrics, report, color=True):
    data = []
    for key in metrics["lines"].keys():
        data.append([metrics["lines"][key]["sample%"], key])
    data.sort(key=lambda k: k[0], reverse=True)
    if len(data) == 0:
        raise AppleTreeError(
            "analyze/run#get_line_report.1", message=_("analyze_run_no_data"),
            err_message="Exception", um=True
        )
    elif len(data) < 5:
        top_5 = data
    else:
        top_5 = data[:5]
    for i, p in enumerate(top_5):
        match metrics["functions"][p[1][::2]]["type"]:
            case (1, 1) | (3, 1) | (3, 2):
                report[1][i + 1] = [p[1], _("analyze_lreport_overload", color), metrics["functions"][p[1][::2]]["sample%"], 1]
            case (2, 1) | (2, 2):
                report[1][i + 1] = [p[1], _("analyze_lreport_large", color), metrics["functions"][p[1][::2]]["sample%"], 2]
            case (2, 3):
                report[1][i + 1] = [p[1], _("analyze_lreport_recursion", color), metrics["functions"][p[1][::2]]["sample%"], 3]
            case (4, 1):
                report[1][i + 1] = [p[1], _("analyze_lreport_normal", color), metrics["functions"][p[1][::2]]["sample%"], 4]
        report[1][i + 1].append(metrics["functions"][p[1][::2]]["cumulative%"])
    return report

def get_report(report_data, code_data, color=True, show_metrics=False):
    try:
        report = _("analyze_report_title", color)
        if show_metrics:
            report += _("analyze_data_count_show", color) % {"cnt": code_data["sample_cnt"]} + "\n\n"
        report_overall = "\n\n".join(map(lambda k: "\n".join(k), report_data[2]))
        report += report_overall
        if report_overall.strip():
            report += "\n\n"
        report += _("analyze_freport_title", color)
        for key in report_data[0].keys():
            report += _("analyze_freport_func", color) % {"rank": report_data[0][key][1], "func": key[1], "br": key[1]} + "\n"
            for i in report_data[0][key][0]:
                report += "  " + i + "\n"
            report += "  " + _(f"analyze_sample_rate_{report_data[0][key][3]}", color) % {"sample_rate": report_data[0][key][2]}
            if show_metrics:
                report += _(f"analyze_cumulative_rate_{report_data[0][key][3]}", color) % {"cumulative_rate": report_data[0][key][4]}
                report += _(f"analyze_magnification_{report_data[0][key][3]}", color) % {"magnification": report_data[0][key][5]}
            report += "\n\n"
        report += _("analyze_lreport_title", color)
        for key in report_data[1].keys():
            report += _("analyze_lreport_line_rank", color) % {"rank": key} + str(report_data[1][key][0][:2][0]) + ", "
            report += _("analyze_lreport_line", color) % {"line": report_data[1][key][0][:2][1]}
            report += _("analyze_lreport_line_func", color) % \
                {"func": report_data[1][key][0][2], "br": report_data[1][key][0][2]}
            for i in report_data[1][key][1:-3]:
                report += "  " + i + "\n"
            report += "  " + _(f"analyze_sample_rate_{report_data[1][key][-2]}", color) % \
                {"sample_rate": report_data[1][key][-3]}
            if show_metrics:
                report += _(f"analyze_cumulative_rate_{report_data[1][key][-2]}", color) % {"cumulative_rate": report_data[1][key][-1]}
            report += "\n\n"
        report += "".join(_("analyze_report_warning", color))
    except AppleTreeError:
        raise
    except KeyboardInterrupt:
        raise
    except Exception as e:
        raise AppleTreeError(
            "analyze/report#get_report.1", message="Error while get report",
            err_message=traceback.format_exc(), um=False
        ) from e
    return str(report)

_run = analyze_new
_metrics = get_metrics

def _report(metrics, code_data, color=True, show_metrics=False):
    func_report = get_func_report(metrics, code_data, color)
    line_report = get_line_report(metrics, func_report, color)
    return get_report(line_report, code_data, color, show_metrics)

def _analyze(filename, arguments):
    # input_file=None, advanced=False, lab=False, log=True, color=True
    try:
        metrics_data = _metrics(
            _run(filename, arguments["input"], arguments["inc_ext"], arguments["log"], arguments["color"], arguments["min_time"]),
            arguments["inc_ext"]
        )
        report_data = _report(*metrics_data, arguments["color"], arguments["metrics"])
        return report_data
    except AppleTreeError:
        raise
    except KeyboardInterrupt:
        raise
    except Exception as e:
        raise AppleTreeError("analyze/analyze#_analyze.1", message="Error while analyze", err_message=traceback.format_exc(), um=False) from e

__all__ = [
    "_run",
    "_metrics",
    "_report",
    "_analyze"
]