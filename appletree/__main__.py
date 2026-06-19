lazy from .utils import AppleTreeError, AppleTreeVersion
lazy from .utils import AppleTreeEnum
lazy from unittest.mock import patch
lazy from .analyze import _analyze
lazy from .locales import _
lazy import traceback
lazy import argparse
lazy import platform
lazy import sys
lazy import os

def is_file(path):
    if not os.path.isfile(path):
        raise argparse.ArgumentTypeError(_("argp_invalid_file_path") % {"path": path})
    return path

def main(name="appletree"):
    try:
        if "!json" in sys.argv:
            print(json(sys.argv))
            return
        with patch("argparse._") as mocked_gettext:
            mocked_gettext.side_effect = _
            parser = argparse.ArgumentParser(prog=name, description=_("argp_appletree_desc"))
            parser.add_argument("-v", "--version", help=_("argp_version"), action="store_true")
            subparsers = parser.add_subparsers(dest="command", help=_("argp_select_mode"))
            run_parser = subparsers.add_parser("run", help=_("argp_run"))
            run_parser.add_argument("file", help=_("argp_file_path"), type=is_file)
            run_parser.add_argument("-i", "--input", help=_("argp_input_file"), type=is_file)
            run_parser.add_argument("-t", "--timeout", type=float, help=_("argp_timeout"))
            run_parser.add_argument("-U", "--buffered", help=_("argp_buffering"), action="store_true")
            run_parser.add_argument("-C", "--uncolored", help=_("argp_uncolored"), action="store_true")
            run_parser.add_argument("-E", "--no-translate", help=_("argp_no_err_translate"), action="store_true")
            debug_parser = subparsers.add_parser("debug", help=_("argp_debug"))
            debug_parser.add_argument("file", help=_("argp_file_path"), type=is_file)
            debug_parser.add_argument("-i", "--input", help=_("argp_input_file"), type=is_file)
            analyze_parser = subparsers.add_parser("analyze", help=_("argp_analyze"), description=_("argp_analyze_desc"))
            analyze_parser.add_argument("file", help=_("argp_file_path"), type=is_file)
            analyze_parser.add_argument("-i", "--input", help=_("argp_input_file"), type=is_file)
            analyze_parser.add_argument("-C", "--uncolored", help=_("argp_uncolored"), action="store_true")
            analyze_parser.add_argument("-L", "--without-log", help=_("argp_without_log"), action="store_true")
            analyze_parser.add_argument("-a", "--advanced", help=_("argp_advanced_anlz"), action="store_true")
            analyze_parser.add_argument("-m", "--metrics", help=_("argp_metrics"), action="store_true")
            analyze_parser.add_argument("-T", "--min-time", help=_("argp_min_time"), type=float)
            analyze_parser.add_argument("-e", "--include-external", help=_("argp_inc_ext"), action="store_true")
            analyze_parser.add_argument("-l", "--lab", help=_("argp_lab_anlz"), action="store_true")
            args = parser.parse_args()
        if args.command == "run":
            print(f"실행 파일: {args.file}")
            print(f"입력 파일: {args.input}")
            print(f"시간 제한: {args.timeout}")
            print(f"버퍼링: {args.buffered}")
        elif args.command == "debug":
            print(f"디버깅 모드: {args.file}")
            print(f"입력 파일: {args.input}")
        elif args.command == "analyze":
            try:
                adv = args.advanced or args.lab
                arguments = {
                    "input": args.input,
                    "log": not args.without_log,
                    "color": not args.uncolored,
                    "metrics": args.metrics if args.metrics else True if adv else False,
                    "min_time": args.min_time if args.min_time else 10 if adv else 5,
                    "inc_ext": args.include_external if args.include_external else True if adv else False
                }
                print(_analyze(args.file, arguments))
            except KeyboardInterrupt:
                pass
            except AppleTreeError as e:
                if e.user_mistake:
                    print(e.message)
                else:
                    print(_("internal_error_title", not args.uncolored))
                    print(_("internal_error_report", not args.uncolored) % {"url": "https://github.com/seanleeee13/PyAppleTree/issues/new"})
                    print(f"[ERROR] {e.code} / {e.message}")
                    print(f"[OS] {platform.system()} {platform.release()} [Python] {sys.version.split()[0]} [AppleTree] {AppleTreeVersion}")
                    traceback.print_exc()
                    print("[ERROR MESSAGE]")
                    print(e.error_message)
            except Exception:
                print(_("internal_error_title", not args.uncolored))
                print(_("internal_error_report", not args.uncolored) % {"url": "https://github.com/seanleeee13/PyAppleTree/issues/new"})
                print("[ERROR] NO EXCEPT - NOT AppleTreeError")
                print(f"[OS] {platform.system()} {platform.release()} [Python] {sys.version.split()[0]} [AppleTree] {AppleTreeVersion}")
                traceback.print_exc()
        else:
            if args.version:
                print(f"PyAppleTree version {AppleTreeEnum.VERSION}")
            else:
                with patch("argparse._") as mocked_gettext:
                    mocked_gettext.side_effect = _
                    parser.print_help()
    except KeyboardInterrupt:
        pass

def json(args):
    sys.argv = args
    raise NotImplementedError(
        "JSON output is reserved for the upcoming AppleTree extension."
    )

if __name__ == "__main__":
    main(name="python -m appletree")