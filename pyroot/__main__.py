lazy from .analyze import _analyze
lazy import argparse
lazy import sys
lazy import os

def is_file(path):
    if not os.path.isfile(path):
        raise argparse.ArgumentTypeError(f"'{path}' is not a valid file path.")
    return path

def main():
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
    parser = argparse.ArgumentParser(prog="pyroot", description="Code Testing Program")
    subparsers = parser.add_subparsers(dest="command", help="Select Mode")
    run_parser = subparsers.add_parser("run", help="Run Program")
    run_parser.add_argument("file", help="File Path", type=is_file)
    run_parser.add_argument("-i", "--input", help="Input File", type=is_file)
    run_parser.add_argument("-t", "--timeout", type=float, help="Timeout")
    run_parser.add_argument("-U", "--buffered", help="Activate Buffering")
    debug_parser = subparsers.add_parser("debug", help="Debug Program")
    debug_parser.add_argument("file", help="File Path", type=is_file)
    debug_parser.add_argument("-i", "--input", help="Input File", type=is_file)
    analyze_parser = subparsers.add_parser("analyze", help="Detailed performance analysis")
    analyze_parser.add_argument("file", help="File Path", type=is_file)
    analyze_parser.add_argument("-i", "--input", help="Input File", type=is_file)
    analyze_parser.add_argument("-d", "--detailed", help="Detailed Analyzation", action="store_true")
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
            print(_analyze(args.file, args.input, args.detailed, log=True))
        except:
            print("=== 오류 발생 ===")
            print("다음 오류 메세지를 복사해 ")
    else:
        parser.print_help()

def json(args):
    sys.argv = args
    # parser 코드들

if __name__ == "__main__":
    main()