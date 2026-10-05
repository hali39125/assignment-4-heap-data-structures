"""Empirical comparison of Heapsort, Quicksort, and Merge Sort."""

import csv
import random
import time
from heapsort import heap_sort


def merge_sort(arr):
    if len(arr) <= 1:
        return arr
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result


def quick_sort(arr):
    """Iterative in-place quicksort using a middle-element pivot."""
    if len(arr) < 2:
        return arr
    stack = [(0, len(arr) - 1)]
    while stack:
        lo, hi = stack.pop()
        i, j = lo, hi
        pivot = arr[(lo + hi) // 2]
        while i <= j:
            while arr[i] < pivot:
                i += 1
            while arr[j] > pivot:
                j -= 1
            if i <= j:
                arr[i], arr[j] = arr[j], arr[i]
                i += 1
                j -= 1
        if lo < j:
            stack.append((lo, j))
        if i < hi:
            stack.append((i, hi))
    return arr


def timed_run(sort_func, values):
    data = values.copy()
    start = time.perf_counter()
    result = sort_func(data)
    elapsed = time.perf_counter() - start
    # Some implementations return a new list and others sort in place.
    final = data if result is None else result
    assert final == sorted(values)
    return elapsed


def run_benchmarks(sizes=(1000, 5000, 10000), trials=3, seed=42):
    random.seed(seed)
    algorithms = {
        "Heapsort": heap_sort,
        "Quicksort": quick_sort,
        "Merge Sort": merge_sort,
    }
    rows = []

    for n in sizes:
        base_random = [random.randint(0, n * 10) for _ in range(n)]
        distributions = {
            "sorted": sorted(base_random),
            "reverse-sorted": sorted(base_random, reverse=True),
            "random": base_random,
        }

        for distribution, values in distributions.items():
            for name, func in algorithms.items():
                samples = [timed_run(func, values) for _ in range(trials)]
                avg = sum(samples) / trials
                rows.append({
                    "size": n,
                    "distribution": distribution,
                    "algorithm": name,
                    "average_seconds": avg,
                })
    return rows


if __name__ == "__main__":
    rows = run_benchmarks()
    with open("benchmark_results.csv", "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)

    print(f"Wrote {len(rows)} benchmark rows to benchmark_results.csv")
    for row in rows:
        print(f"n={row['size']:5d} | {row['distribution']:14s} | {row['algorithm']:10s} | {row['average_seconds']:.6f} s")
