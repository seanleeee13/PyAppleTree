lazy from .utils import AppleTreeError, AppleTreeVersion
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
        raise argparse.ArgumentTypeError(_("argp_invalid_file_path") % path)
    return path

def main(name="appletree"):
    commands = ["run", "debug", "analyze"]
    if len(sys.argv) > 1 and not any(cmd in sys.argv for cmd in commands):
        for arg in sys.argv[1:]:
            if arg.startswith(("-h", "--help")):
                break
        else:
            sys.argv.insert(1, "run")
    if "!json" in sys.argv:
        print(json(sys.argv))
        return
    with patch("argparse._") as mocked_gettext:
        mocked_gettext.side_effect = _
        parser = argparse.ArgumentParser(prog=name, description=_("argp_appletree_desc"))
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
        analyze_parser = subparsers.add_parser("analyze", help=_("argp_analyze"))
        analyze_parser.add_argument("file", help=_("argp_file_path"), type=is_file)
        analyze_parser.add_argument("-i", "--input", help=_("argp_input_file"), type=is_file)
        analyze_parser.add_argument("-d", "--detailed", help=_("argp_detailed_anlz"), action="store_true")
        analyze_parser.add_argument("-C", "--uncolored", help=_("argp_uncolored"), action="store_true")
        analyze_parser.add_argument("-L", "--without-log", help=_("argp_without_log"), action="store_true")
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
            print(_analyze(args.file, args.input, args.detailed, log=not args.without_log, color=not args.uncolored))
        except KeyboardInterrupt:
            pass
        except AppleTreeError as e:
            if e.user_mistake:
                print(e.message)
            else:
                print(_("internal_error_title", not args.uncolored))
                print(_("internal_error_report", not args.uncolored))
                print(f"[ERROR] {e.code} / {e.message}")
                print(f"[OS] {platform.system()} {platform.release()} [Python] {sys.version.split()[0]} [AppleTree] {AppleTreeVersion}")
                traceback.print_exc()
        except Exception:
            print(_("internal_error_title", not args.uncolored))
            print(_("internal_error_report", not args.uncolored))
            print("[ERROR] NO EXCEPT - NOT AppleTreeError")
            print(f"[OS] {platform.system()} {platform.release()} [Python] {sys.version.split()[0]} [AppleTree] {AppleTreeVersion}")
            traceback.print_exc()
    else:
        parser.print_help()

def json(args):
    sys.argv = args
    # parser 코드들

if __name__ == "__main__":
    main(name="python -m appletree")