# Assignment 4: Heap Data Structures

This repository contains a complete implementation and analysis of Heapsort and an array-based max-heap priority queue.

## Files

- `heapsort.py` - Heapsort implementation using a max heap.
- `priority_queue.py` - `Task` class, max-heap priority queue, key updates, and scheduler demonstration.
- `benchmark.py` - Empirical comparison of Heapsort, Quicksort, and Merge Sort.
- `benchmark_results.csv` - Timing results generated from the benchmark.
- `report.docx` - Detailed report covering design, complexity analysis, benchmark results, and applications.
- `report.pdf` - PDF copy of the report.

## Requirements

- Python 3.10 or newer is recommended.
- No third-party Python packages are required to run the source code.

## How to Run

### 1. Run Heapsort

```bash
python heapsort.py
```

This prints an example list before and after sorting.

### 2. Run the Priority Queue / Scheduler

```bash
python priority_queue.py
```

This creates several tasks, updates one task's priority, and removes tasks from highest priority to lowest priority.

### 3. Run the Benchmark

```bash
python benchmark.py
```

The program compares Heapsort, Quicksort, and Merge Sort for input sizes 1,000, 5,000, and 10,000 using sorted, reverse-sorted, and random input distributions. Each case is run three times and the average time is recorded in `benchmark_results.csv`.

## Summary of Findings

Heapsort has O(n log n) time complexity in the best, average, and worst cases. It sorts in place and therefore uses O(1) auxiliary array space, although the recursive `heapify` function uses O(log n) call-stack space in the worst case.

The priority queue uses an array-based max heap. Insertion, extraction of the maximum element, and changing a priority all take O(log n) time. Checking whether the queue is empty takes O(1) time.

In the benchmark on this machine, Quicksort was generally fastest, followed by Merge Sort, while Heapsort was slower because of its repeated heapify operations and less cache-friendly memory access. The benchmark still supports the theoretical conclusion that Heapsort grows predictably as O(n log n) across all tested input distributions.
