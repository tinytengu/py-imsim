import os
import string


CHARSET = string.ascii_letters + string.digits + string.punctuation


def filter_results(results: list[dict], filter_type: str = "none") -> list[dict]:
    if filter_type == "none":
        return results

    if filter_type == "sim":
        return list(
            sorted(results, key=lambda result: result["metrics"][filter_type], reverse=True)
        )

    if filter_type == "mse":
        return list(
            sorted(results, key=lambda result: result["metrics"][filter_type])
        )

    return results


def get_files(path: str, deep: int = 0, deepnow: int = 0) -> list[str]:
    for dirpath, dirnames, filenames in os.walk(path):
        files = [
            os.path.join(dirpath, fn) for fn in filenames
            if not [c for c in fn if c not in CHARSET]
        ]

        if deep == deepnow:
            return files

        return [
            file
            for file in (
                files
                + [
                    files.extend(
                        get_files(os.path.join(dirpath, dirname), deep, deepnow + 1)
                    )
                    for dirname in dirnames
                ]
            )
            if file
        ]
    return files
