import argparse
import platform
import subprocess
from pathlib import Path

SHELL = platform.system() == "Windows"


def set_up_parser() -> argparse.Namespace:
    """
    Set up the argument parse for this program
    Return:
         The parsed arguments
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("bundle", type=str, help="Assignment bundle directory")
    parser.add_argument("-d", "--done", type=int, default=0,
                        help="Number of already marked assignments")
    parser.add_argument("--ide", nargs="?", type=str, default="code", const="code",
                        help="IDE to be opened, has to be in $PATH")
    parser.add_argument("-m", "--merge", action="store_true",
                        help="Merge mode, all student's files will be accumulated "
                             "into a single file called merged.java"
                             " and that file will be opened.")
    parser.add_argument("-i", "--ignore-merge", nargs="*", action="extend",
                        help="Ignore specified files while merging, useful to "
                             "leave out provided code")
    parser.add_argument("-c", "--confirm-continue", action="store_true",
                        help="Program will ask for your confirmation before"
                             " moving on to next student")
    return parser.parse_args()


def main():
    """
    Opens the scripts
    """
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
        student_style = student_dir / f"{student_dir.name}.style"
        student_checkstyle = student_dir / f"{student_dir.name}.checkstyle"
        files_to_open = [str(student_dir),
                         str(student_style),
                         str(student_checkstyle),
                         "common_mistakes.txt"]

        # Merge file
        if args.merge:
            merged_file = student_dir / "merged.java"
            with merged_file.open("w") as merged_fout:
                for java_file in (student_dir / "src").glob("**/*.java"):
                    if java_file.name in args.ignore_merge:
                        continue
                    with java_file.open() as java_fin:
                        merged_fout.write(java_fin.read())
            files_to_open.append(str(merged_file))

        # Open in IDE
        subprocess.call([args.ide, "-n", "-w", *files_to_open], shell=SHELL)

        # Remove merged file
        if args.merge:
            merged_file.unlink()

        print(f"{marked} students marked, "
              f"{len(student_dirs) - marked} students remainingin bundle.\n")

        if args.confirm_continue:
            input("Press enter to continue.")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        exit(0)
