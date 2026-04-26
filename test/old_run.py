lazy from profiling.sampling.binary_collector import BinaryCollector
lazy from profiling.sampling.cli import _handle_run, COLLECTOR_MAP
lazy from profiling.sampling.binary_reader import BinaryReader
lazy from contextlib import redirect_stdout, redirect_stderr
lazy from ..utils import tempfile_wrapper, clean
lazy from unittest.mock import patch
lazy import subprocess
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

class PyRootCollector:
    def __init__(self):
        self.samples = []
    def collect(self, sample, *args):
        try:
            for interp in sample:
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
                    self.samples.append([*current_loc, full_stack])
        except Exception:
            pass
    def __getattr__(self, name):
        return lambda *args, **kwargs: None

class PyRootBinaryCollector(BinaryCollector):
    _pyroot_cnt = 0
    _pyroot_start_t = 0.0
    _pyroot_msg = ""
    _pyroot_msg_len = 0
    _pyroot_samples = []
    _pyroot_log = True
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    def collect(self, stack_frames, timestamp_us=None): ##################### sample 여기서
        if self._pyroot_log:
            self._pyroot_cnt += 1
            if self._pyroot_cnt % 50 == 0:
                pass
            seconds = int(time.perf_counter() - self._pyroot_start_t)
            hours, remainder = divmod(seconds, 3600)
            minutes, seconds = divmod(remainder, 60)
            message = f"\r#{self._pyroot_cnt} {hours:02d}:{minutes:02d}:{seconds:02d} / {self._pyroot_msg}"
            message_length = len(message)
            message += " " * max(0, self._pyroot_msg_len - len(message))
            self._pyroot_msg_len = message_length
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
                    self._pyroot_samples.append([*current_loc, full_stack])
        except:
            pass
        return super().collect(stack_frames, timestamp_us)

used_prbc = None
prbc_args = None
prbc_kwargs = None

def get_prbc(log=True): ################ lastest 넣고
    def _get_prbc(*args, **kwargs):
        global used_prbc, prbc_args, prbc_kwargs
        if not used_prbc or prbc_args != args or prbc_kwargs != kwargs:
            _used_prbc = PyRootBinaryCollector(*args, **kwargs)
            if used_prbc:
                _used_prbc._pyroot_cnt = used_prbc._pyroot_cnt
                _used_prbc._pyroot_start_t = used_prbc._pyroot_start_t
                _used_prbc._pyroot_msg = used_prbc._pyroot_msg
                _used_prbc._pyroot_msg_len = used_prbc._pyroot_msg_len
                _used_prbc._pyroot_samples = used_prbc._pyroot_samples
                _used_prbc._pyroot_log = log
            used_prbc = _used_prbc
            prbc_args = args
            prbc_kwargs = kwargs
        return used_prbc
    return _get_prbc

def get_prbc_now():
    return used_prbc

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
    if not filename:
        return None_open()
    else:
        return open(filename, mode=mode)

def sample(target_file, input_file, output_file="output.prof", log=True):
    if not os.path.exists(target_file):
        print(f"Target file {target_file} doesn't exist.")
        return "!ERROR"
    if not os.path.exists(output_file):
        print(f"Output file {output_file} doesn't exist.")
        return "!ERROR"
    if input_file and not os.path.exists(input_file):
        print(f"Input file {input_file} doesn't exist.")
        return "!ERROR"
    target_file = target_file.replace("/", "\\")
    Popen = subprocess.Popen
    with patch("subprocess.Popen") as mocked_popen, safe_open(input_file, "r") as in_f:
        def popen_side_effect(cmd, **kw):
            kw["stdout"] = subprocess.DEVNULL
            kw["stderr"] = subprocess.PIPE
            kw["stdin"] = in_f if in_f else subprocess.DEVNULL
            return Popen(cmd, **kw)
        mocked_popen.side_effect = popen_side_effect
        COLLECTOR_MAP["binary"] = get_prbc(log)
        try:
            f = io.StringIO()
            with redirect_stdout(f), redirect_stderr(f):
                _handle_run(SampleArgs(target_file, output_file))
        except SystemExit:
            pass
        # except Exception as e:
        #     if log:
        #         print()
        #     print(f"Critical Error: {e}")
        #     return "!ERROR"
        finally:
            COLLECTOR_MAP["binary"] = BinaryCollector
    return output_file

def sample_tempfile(target_file, input_file=None, log=True):
    return tempfile_wrapper(sample, target_file, input_file, log, index=2)

def analyze(output_file):
    try:
        if output_file == "!ERROR" or not os.path.exists(output_file):
            return "!ERROR"
        collector = PyRootCollector()
        with BinaryReader(output_file) as reader:
            reader.replay_samples(collector)
        samples = collector.samples
        if len(samples) == 0:
            print("No data found.")
            sys.exit(1)
        return samples
    finally:
        clean(output_file)

if __name__ == "__main__":
    print(analyze(*sample_tempfile("test/a.py", input_file="test/a.txt"))[:1])