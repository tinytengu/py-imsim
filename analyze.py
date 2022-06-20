import json
import os
import argparse
from time import time

from app.images import get_mse_ssim, get_similarity
from app.utils import filter_results, get_files


def analyze_files(files: list[str], verbose: bool = False) -> list[dict]:
    combinations = int(len(files) * ((len(files) - 1) / 2))
    results = []

    fileidx = 0
    for idx, file1 in enumerate(files):
        for file2 in files[idx + 1:]:
            mse, ssim = get_mse_ssim(file1, file2)
            sim = get_similarity(file1, file2)
            fileidx += 1

            if verbose:
                print(
                    f"[{fileidx}/{combinations}] {file1} {file2} | MSE: {mse:.02f} SSIM: {ssim:.02f} SIM: {sim}"
                )

            results.append(
                {
                    "files": (file1, file2),
                    "metrics": {
                        "sim": sim,
                        "mse": mse,
                        "ssim": ssim,
                    },
                }
            )

    return results


def main():
    parser = argparse.ArgumentParser(description="Some description")
    parser.add_argument(
        "-p",
        "--path",
        type=str,
        required=True,
        help="Path to the directory with files to compare",
    )
    parser.add_argument(
        "-d", "--deep", type=int, default=0, help="Deepness of recursive filesearch"
    )
    parser.add_argument(
        "-i",
        "--indent",
        type=int,
        default=None,
        help="Output JSON file indentation (minified if not provided)",
    )
    parser.add_argument(
        "-f",
        "--filter",
        type=str,
        choices=["sim", "mse", "ssim", "none"],
        default="sim",
        help="Filter by basic similarity (sim), mean squared error (mse) or structural similarity (ssim)",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=str,
        default=None,
        help="Output filename (defaults to './reports/FOLDERNAME.json' name)",
    )
    parser.add_argument(
        "-v", "--verbose", action="store_true", help="Show verbose info"
    )
    args = parser.parse_args()

    if not os.path.isdir(args.path):
        print("[Error] Invalid directory:", args.path)

    args.path = os.path.abspath(args.path)

    if not args.output:
        if not os.path.isdir("reports"):
            os.mkdir("reports")
        args.output = os.path.join("reports", os.path.basename(args.path))

    start = time()

    files = get_files(args.path, args.deep)
    if args.verbose:
        print("Total files:", len(files))

    results = analyze_files(files, args.verbose)
    if args.verbose:
        print(f"Writing {len(results)} results...")

    results = filter_results(results, args.filter)

    data = {
        "images_dir": args.path,
        "filter_type": args.filter,
        "results": results
    }

    with open(f"{args.output}.json", "w", encoding="utf-8") as file:
        json.dump(data, file, indent=args.indent)

    if args.verbose:
        print("Finished in {} sec.".format(int(time() - start)))


if __name__ == "__main__":
    main()
