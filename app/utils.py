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
