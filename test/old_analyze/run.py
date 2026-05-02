lazy from ...appletree.utils import tempfile_wrapper, clean, AppleTreeError, Color
lazy from profiling.sampling.binary_collector import BinaryCollector
lazy from profiling.sampling.cli import _handle_run, COLLECTOR_MAP
lazy from contextlib import redirect_stdout, redirect_stderr
lazy from .report import get_m_func_report
lazy from .metrics import get_metrics
lazy from unittest.mock import patch
lazy from ...appletree.locales import _
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
    _appletree_detailed = False
    _appletree_color = True
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    def collect(self, stack_frames, timestamp_us=None):
        if self._appletree_log:
            self._appletree_cnt += 1
            if self._appletree_cnt % 50 == 0:
                lst = get_m_func_report(get_metrics(
                    self._appletree_samples, self._appletree_target, 
                    self._appletree_detailed)[0], self._appletree_color
                )
                if lst:
                    self._appletree_msg = " ".join(lst)
            seconds = int(time.perf_counter() - self._appletree_start_t)
            hours, remainder = divmod(seconds, 3600)
            minutes, seconds = divmod(remainder, 60)
            message = f"\r{Color.BLUE if self._appletree_color else ""}#{self._appletree_cnt} {hours:02d}:{minutes:02d}:{seconds:02d}" + \
                f"{Color.CYAN if self._appletree_color else ""}{" / " if self._appletree_msg.strip() else ""}{self._appletree_msg}"
            message_length = len(message)
            message += " " * (max(0, self._appletree_msg_len - len(message)) + 3)
            self._appletree_msg_len = message_length
            sys.__stdout__.write(message)
        try:
            for interp in stack_frames:
                for thread in interp.threads:
                    if not thread.frame_info:
                        continue
                    top = thread.frame_info[0]
                    current_loc = [top.filename, top.location[0], top.funcname]
                    full_stack = []
                    for frame in thread.frame_info:
                        full_stack.append([
                            frame.filename,
                            frame.location[0],
                            frame.funcname
                        ])
                    self._appletree_samples.append([*current_loc, full_stack])
        except:
            pass
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
                _used_prbc._appletree_detailed = used_prbc._appletree_detailed
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

class None_open:
    def __enter__(self):
        pass
    def __exit__(self, *args):
        pass
    def __bool__(self):
        return False

def safe_open(filename, mode):
    if not filename or not os.path.exists(filename):
        return None_open()
    else:
        return open(filename, mode=mode)

def sample(target_file, input_file, output_file="output.prof", log=True, color=True):
    if not os.path.exists(target_file):
        raise AppleTreeError(
            "analyze/run#sample.2", message=f"타겟 파일 {target_file}이 존재하지 않습니다.",
            err_message="FileNotFoundError", um=True
        )
    if not os.path.exists(output_file):
        raise AppleTreeError(
            "analyze/run#sample.3", message=f"Output File No Exist",
            err_message="FileNotFoundError", um=False
        )
    if input_file and not os.path.exists(input_file):
        raise AppleTreeError(
            "analyze/run#sample.4", message=f"입력 파일 {input_file}이 존재하지 않습니다.",
            err_message="FileNotFoundError", um=True
        )
    target_file = target_file.replace("/", "\\")
    Popen = subprocess.Popen
    with patch("subprocess.Popen") as mocked_popen, safe_open(input_file, "r") as in_f:
        def popen_side_effect(cmd, **kw):
            kw["stdout"] = subprocess.DEVNULL
            kw["stderr"] = subprocess.PIPE
            kw["stdin"] = in_f if in_f else subprocess.DEVNULL
            return Popen(cmd, **kw)
        mocked_popen.side_effect = popen_side_effect
        COLLECTOR_MAP["binary"] = get_prbc(log, color)
        try:
            f = io.StringIO()
            with redirect_stdout(f), redirect_stderr(f):
                _handle_run(SampleArgs(target_file, output_file))
        except SystemExit:
            pass
        except AppleTreeError:
            raise
        except Exception as e:
            if log:
                print()
            raise AppleTreeError(
                "analyze/run#sample.1", message="Error while sample _handle_run",
                err_message=traceback.format_exc(), um=False
            ) from e
        finally:
            COLLECTOR_MAP["binary"] = BinaryCollector
    return output_file

def sample_tempfile(target_file, input_file=None, log=True, color=True):
    return tempfile_wrapper(sample, target_file, input_file, log, color, index=2)

def analyze_new(filename, input_file, detailed=False, log=True, color=True):
    try:
        start = time.perf_counter()
        AppleTreeBinaryCollector._appletree_start_t = start
        AppleTreeBinaryCollector._appletree_target = filename
        AppleTreeBinaryCollector._appletree_detailed = detailed
        while time.perf_counter() - start <= (5 if not detailed else 10):
            ret = None
            try:
                ret = sample_tempfile(filename, input_file, log, color)
            except AppleTreeError:
                raise
            finally:
                clean(ret)
        if log:
            print("\n")
        return used_prbc._appletree_samples
    except AppleTreeError:
        raise
    except Exception as e:
        raise AppleTreeError("analyze/run#analyze_new.1", message="Error while sampling", err_message=traceback.format_exc(), um=False) from e
    finally:
        clean_prbc()

if __name__ == "__main__":
    print(analyze_new("test/a.py", input_file="test/a.txt")[0])