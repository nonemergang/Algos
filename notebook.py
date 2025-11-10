def notebook(tasks):
    new_pull = []
    tasks = sorted(tasks, key = lambda x: x[1])
    prev_task = 0
    for task in tasks:
        if task[0] >= prev_task:
            new_pull.append(task)
            prev_task = task[1]
    return new_pull


def scheduler_2(tasks: list[tuple[int, int]]) -> list[tuple[int, int]]:
    picked_tasks: list[tuple[int, int]] = []

    durs_and_tasks = [(end - start, (start, end)) for start, end in tasks]
    durs_and_tasks.sort(key=lambda x: x[0])
    print('Durations:', durs_and_tasks)

    for duration, task in durs_and_tasks:
        is_collision = False
        for picked_task in picked_tasks:
            if (
                    (task[0] < picked_task[1] and task[0] > picked_task[0]) or
                    (task[1] > picked_task[0] and task[1] < picked_task[1]) or
                    (task[0] < picked_task[0] and task[1] > picked_task[1])
            ):
                is_collision = True
                break

        if not is_collision:
            picked_tasks.append(task)

    return picked_tasks


tasks = [(1, 5), (2, 4), (1, 8), (3, 15), (3, 5), (4, 8), (4, 7), (7, 15), (16, 22)]
print(notebook(tasks))
print(scheduler_2(tasks))