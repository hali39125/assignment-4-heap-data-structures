"""Array-based max-heap priority queue and a small task-scheduler simulation."""

from dataclasses import dataclass


@dataclass
class Task:
    task_id: str
    priority: int
    arrival_time: int = 0
    deadline: int | None = None


class MaxHeapPriorityQueue:
    def __init__(self):
        self.heap = []
        self.positions = {}  # task_id -> current array index

    def is_empty(self):
        return len(self.heap) == 0

    def _swap(self, i, j):
        self.heap[i], self.heap[j] = self.heap[j], self.heap[i]
        self.positions[self.heap[i].task_id] = i
        self.positions[self.heap[j].task_id] = j

    def _sift_up(self, index):
        while index > 0:
            parent = (index - 1) // 2
            if self.heap[index].priority <= self.heap[parent].priority:
                break
            self._swap(index, parent)
            index = parent

    def _sift_down(self, index):
        n = len(self.heap)
        while True:
            left = 2 * index + 1
            right = 2 * index + 2
            largest = index

            if left < n and self.heap[left].priority > self.heap[largest].priority:
                largest = left
            if right < n and self.heap[right].priority > self.heap[largest].priority:
                largest = right

            if largest == index:
                break
            self._swap(index, largest)
            index = largest

    def insert(self, task):
        if task.task_id in self.positions:
            raise ValueError(f"Task {task.task_id} already exists")
        self.heap.append(task)
        index = len(self.heap) - 1
        self.positions[task.task_id] = index
        self._sift_up(index)

    def extract_max(self):
        if self.is_empty():
            raise IndexError("extract_max from empty priority queue")

        maximum = self.heap[0]
        last = self.heap.pop()
        del self.positions[maximum.task_id]

        if self.heap:
            self.heap[0] = last
            self.positions[last.task_id] = 0
            self._sift_down(0)

        return maximum

    def change_priority(self, task_id, new_priority):
        if task_id not in self.positions:
            raise KeyError(f"Unknown task: {task_id}")

        index = self.positions[task_id]
        old_priority = self.heap[index].priority
        self.heap[index].priority = new_priority

        if new_priority > old_priority:
            self._sift_up(index)
        elif new_priority < old_priority:
            self._sift_down(index)

    def increase_key(self, task_id, new_priority):
        index = self.positions.get(task_id)
        if index is None:
            raise KeyError(f"Unknown task: {task_id}")
        if new_priority < self.heap[index].priority:
            raise ValueError("New priority must be greater than or equal to current priority")
        self.change_priority(task_id, new_priority)

    def decrease_key(self, task_id, new_priority):
        index = self.positions.get(task_id)
        if index is None:
            raise KeyError(f"Unknown task: {task_id}")
        if new_priority > self.heap[index].priority:
            raise ValueError("New priority must be less than or equal to current priority")
        self.change_priority(task_id, new_priority)


def scheduler_demo():
    queue = MaxHeapPriorityQueue()
    tasks = [
        Task("T1", 3, arrival_time=0, deadline=10),
        Task("T2", 8, arrival_time=1, deadline=6),
        Task("T3", 5, arrival_time=2, deadline=12),
        Task("T4", 10, arrival_time=3, deadline=5),
        Task("T5", 4, arrival_time=4, deadline=15),
    ]

    for task in tasks:
        queue.insert(task)

    # A task becomes more urgent before scheduling begins.
    queue.increase_key("T1", 9)

    order = []
    while not queue.is_empty():
        order.append(queue.extract_max())

    return order


if __name__ == "__main__":
    print("Execution order (highest priority first):")
    for task in scheduler_demo():
        print(task)
