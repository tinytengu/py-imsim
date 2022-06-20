import json
import os
import argparse

from flask import Flask, render_template

from app.utils import filter_results

report_data = {}
report_path = ""


def index():
    global report_data
    global report_path

    for idx, item in enumerate(report_data["results"]):
        report_data["results"][idx]["files"][0] = os.path.basename(item["files"][0])
        report_data["results"][idx]["files"][1] = os.path.basename(item["files"][1])

    return render_template("index.html", data=report_data, report_path=report_path, metrics={
        "sim": ("SIM", "Image hashes similarity in percents"),
        "ssim": ("SSIM", "Image Structural Similarity, between -1 and 1, the closer to 1 the more similar images are"),
        "mse": ("MSE", "Mean Squared Error, the lower error the more similar images are"),
    })


def main():
    parser = argparse.ArgumentParser(description="Some description")
    parser.add_argument(
        "-r",
        "--report",
        type=str,
        required=True,
        help="Path to the report file",
    )
    parser.add_argument(
        "-f",
        "--filter",
        type=str,
        choices=["sim", "mse", "ssim", "none"],
        default="sim",
        help="Filter by basic similarity (sim), mean squared error (mse) or structural similarity (ssim)",
    )
    args = parser.parse_args()

    global report_data
    global report_path

    report_path = os.path.abspath(args.report)

    if not os.path.exists(report_path):
        print("[Error] Invalid report file:", report_path)
        return

    with open(args.report, "r", encoding="utf-8") as file:
        report_data = json.load(file)

    if not os.path.isdir(report_data["images_dir"]):
        print("[Error] Invalid report images_dir:", report_data["images_dir"])
        return

    report_data["results"] = filter_results(report_data["results"], args.filter)
    report_data["filter_type"] = report_data["filter_type"] if args.filter == "none" else args.filter

    app = Flask(__name__, static_folder=report_data["images_dir"])
    app.add_url_rule("/", None, index, {})
    app.run(debug=True)


if __name__ == '__main__':
    main()
