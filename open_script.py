import subprocess
from pathlib import Path
import platform
import argparse

SHELL = platform.system() == "Windows"

def set_up_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("bundle", type=str)
    parser.add_argument("-d", "--done", type=int, default=0)
    parser.add_argument("--ide", type=str, default="code", const="code")
    parser.add_argument("-m", "--merge", action="store_true")
    parser.add_argument("-i", "--ignore-merge", nargs="*", action="extend")
    return parser.parse_args()

def main():
    args = set_up_parser()
    bundle_dir = Path(args.bundle)
    if not args.merge and args.ignore_merge:
        raise argparse.ArgumentError("--ignore-merge argument"
                                     " specified but --merge isn't")
    # Convert to list to get length
    student_dirs = list(filter(lambda child: child.is_dir(),
                                sorted(bundle_dir.iterdir())))
    
    for marked, student_dir in enumerate(student_dirs, start=1):
        if marked <= args.done:
            continue
        if args.merge:
            merged_file = student_dir / "merged.java"
            with merged_file.open("w") as merged_fout:
                for java_file in (student_dir / "src").glob("**/*.java"):
                    if java_file.name in args.ignore_merge:
                        continue
                    with java_file.open() as java_fin:
                        merged_fout.write(java_fin.read())
        student_style = student_dir / f"{student_dir.name}.style"
        student_checkstyle = student_dir / f"{student_dir.name}.checkstyle"
        subprocess.call([args.ide, "-n", "-w",
                         str(student_dir),
                         str(student_style),
                         str(student_checkstyle),
                         "common_mistakes.txt",
##                         str(merged_file)
                         ], shell=SHELL)
        print(f"{marked} students marked, "
              f"{len(student_dirs) - marked} students remainingin bundle.")


if __name__ == "__main__":
    main()
