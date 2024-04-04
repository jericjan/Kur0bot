import argparse
import re
import subprocess


def popen(coms):
    with subprocess.Popen(
        coms, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding="utf-8"
    ) as p:
        out, err = p.communicate()

    return out


def main():
    # Create the parser
    parser = argparse.ArgumentParser(description="Pylint but lines are sorted")

    # Add arguments
    parser.add_argument("file_path", help="file path")

    # Parse the arguments
    args = parser.parse_args()

    if not args.file_path:
        print("No file path given.")
        return

    pylint_out = popen(["pylint", args.file_path, "--score", "false"])

    lines_dict = {}

    reg = re.compile(r".+:(\d+):\d+:.+")

    for line in pylint_out.split("\n"):
        if reg.search(line):
            lines_dict[line] = reg.findall(line)[0]

    sorted_list = sorted(lines_dict.keys(), key=lambda f: int(lines_dict[f]))
    with open("pylint_sorted.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(sorted_list))

    print("Done! check pylint_sorted.txt")


if __name__ == "__main__":
    main()
