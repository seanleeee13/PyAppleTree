lazy from collections import Counter
lazy from ..utils import PyRootError
lazy import traceback
lazy import os

def filter_samples(samples, target_file=None, detailed=False):
    if not target_file and not detailed:
        raise PyRootError(
            "analyze/metrics#filter_samples.1", message="Missing target file while not detailed",
            err_message="TypeError", um=False
        )
    target_abs_path = os.path.abspath(target_file) if target_file else None
    clean_samples = []
    for loc in samples:
        if detailed or loc[0] == target_abs_path:
            clean_samples.append(tuple(loc[:3]))
        for subloc in loc[3]:
            if not detailed and subloc[0] == target_abs_path:
                clean_samples.append(tuple(subloc))
    return clean_samples

def count_filter_samples(samples, target_file=None, detailed=False):
    if not target_file and not detailed:
        raise PyRootError(
            "analyze/metrics#count_filter_samples.1", message="Missing target file while not detailed",
            err_message="TypeError", um=False
        )
    target_abs_path = os.path.abspath(target_file) if target_file else None
    normal_count = Counter()
    stack_count = Counter()
    normal_count_func = Counter()
    stack_count_func = Counter()
    for loc in samples:
        if detailed or loc[0] == target_abs_path:
            normal_count[tuple(loc[:3])] += 1
            normal_count_func[tuple(loc)[::2]] += 1
            stack_count[tuple(loc[:3])] += 1
            stack_count_func[tuple(loc)[::2]] += 1
        for subloc in set(map(tuple, loc[3])) - set([tuple(loc[:3])]):
            if not detailed and subloc[0] == target_abs_path:
                stack_count[tuple(subloc[:3])] += 1
                stack_count_func[tuple(subloc)[::2]] += 1
    return frozendict({"normal cnt": normal_count, "stack cnt": stack_count, "normal fcnt": normal_count_func, "stack fcnt": stack_count_func})

def get_sample_percent(sample_counter, loc):
    return 100 * sample_counter["normal cnt"].get(loc, 0) / sum(sample_counter["normal cnt"].values()) if sum(sample_counter["normal cnt"].values()) else 2147483647 if sample_counter["normal cnt"].get(loc, 0) else 0

def get_cumulative_percent(sample_counter, loc):
    return 100 * sample_counter["stack cnt"].get(loc, 0) / sum(sample_counter["normal cnt"].values()) if sum(sample_counter["normal cnt"].values()) else 2147483647 if sample_counter["stack cnt"].get(loc, 0) else 0

def get_fsample_percent(sample_counter, floc):
    return 100 * sample_counter["normal fcnt"].get(floc, 0) / sum(sample_counter["normal fcnt"].values()) if sum(sample_counter["normal fcnt"].values()) else 2147483647 if sample_counter["normal fcnt"].get(floc, 0) else 0

def get_fcumulative_percent(sample_counter, floc):
    return 100 * sample_counter["stack fcnt"].get(floc, 0) / sum(sample_counter["normal fcnt"].values()) if sum(sample_counter["normal fcnt"].values()) else 2147483647 if sample_counter["stack fcnt"].get(floc, 0) else 0

def get_magnification(sample_counter, floc):
    return sample_counter["stack fcnt"].get(floc, 0) / sample_counter["normal fcnt"].get(floc, 0) if sample_counter["normal fcnt"].get(floc) else 2147483647 if sample_counter["stack fcnt"].get(floc, 0) else 0

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

def get_metrics(samples, target_file=None, detailed=False):
    try:
        sample_counter = count_filter_samples(samples, target_file, detailed)
        filtered = filter_samples(samples, target_file, detailed)
        locs = set(filtered)
        metrics = {"lines": {}, "functions": {}}
        code_data = {"sample_cnt": sum(sample_counter["normal cnt"].values())}
        for loc in locs:
            metrics["lines"][loc] = {
                "samples": sample_counter["normal cnt"].get(loc, 0),
                "cumulatives": sample_counter["stack cnt"].get(loc, 0),
                "sample%": get_sample_percent(sample_counter, loc),
                "cumulative%": get_cumulative_percent(sample_counter, loc)
            }
            metrics["functions"][loc[::2]] = {
                "samples": sample_counter["normal fcnt"].get(loc[::2], 0),
                "cumulatives": sample_counter["stack fcnt"].get(loc[::2], 0),
                "sample%": get_fsample_percent(sample_counter, loc[::2]),
                "cumulative%": get_fcumulative_percent(sample_counter, loc[::2]),
                "magnification": get_magnification(sample_counter, loc[::2])
            }
            metrics["functions"][loc[::2]]["type"] = get_ftype(metrics["functions"][loc[::2]])
    except PyRootError:
        raise
    except Exception:
        raise PyRootError(
            "analyze/metrics#get_metrics.1", message="Error while calculating metrics",
            err_message=traceback.format_exc(), um=False
        )
    return metrics, code_data