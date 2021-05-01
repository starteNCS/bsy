import numpy as np
import matplotlib.pyplot as plt

from numpy.random import default_rng
from enum import Enum


class waitingroom_strategy_type(Enum):
    fifo = 1
    lifo = 2


class task_type:
    id: int
    duration: float
    arrival_offset: float
    waiting_time: float


waitingroom_strategy = waitingroom_strategy_type.fifo.value
task_count = 300
waitingroom: list[task_type] = []
finished_tasks: list[task_type] = []
rng = default_rng()
m = 0.5

# for i in range(task_count):
#     new_task = task_type()

#     new_task.id = i + 1
#     new_task.arrival_offset = rng.exponential(5)
#     new_task.duration = 1 - np.exp(-m * new_task.arrival_offset) # rng.exponential(3), 3

#     # print('id =', new_task.id, ', arrival_offset =',
#     #       new_task.arrival_offset, ', duration =', new_task.duration)

#     waitingroom.append(new_task)
    
# waitingroom[0].arrival_offset = 0

new_task = task_type()
new_task.duration = 10
new_task.arrival_offset = 0
waitingroom.append(new_task) # wating: 0, arrival: 0

new_task2 = task_type()
new_task2.duration = 20
new_task2.arrival_offset = 7
waitingroom.append(new_task2) # wating: 3, arrival: 7

new_task3 = task_type()
new_task3.duration = 10
new_task3.arrival_offset = 50
waitingroom.append(new_task3) # wating: 0, arrival: 57


def work_on_task(task: task_type):
    # print('Working on task', task.id)
    pass


def get_new_task() -> task_type:
    if len(waitingroom) == 0:
        return None

    if waitingroom_strategy == waitingroom_strategy_type.fifo.value:
        return get_new_task_fifo()
    elif waitingroom_strategy == waitingroom_strategy_type.lifo.value:
        return get_new_task_lifo()
    else:
        raise NameError('unhandled waiting room strategy: ',
                        waitingroom_strategy)


def get_new_task_fifo():
    return_task = waitingroom[0]
    waitingroom.remove(return_task)
    return return_task


def get_new_task_lifo():
    return_task = waitingroom[len(waitingroom) - 1]
    waitingroom.remove(return_task)
    return return_task


def get_summed_up_arrival_times(current_task: task_type) -> float:
    summed_arrival_time: float = 0
    for i in range(len(finished_tasks)):
        summed_arrival_time = summed_arrival_time + finished_tasks[i].arrival_offset

    summed_arrival_time += current_task.arrival_offset

    return summed_arrival_time


def get_summed_working_time(current_task: task_type) -> float:
    summed_working_time: float = 0
    # if(len(finished_tasks) == 0):
    #     summed_working_time = current_task.duration
    for i in range(len(finished_tasks)):
        summed_working_time = summed_working_time + finished_tasks[i].duration

    return summed_working_time

overall_timer = 0.0
current_task: task_type = get_new_task()
while current_task is not None:
    work_on_task(current_task)

    waiting_time = get_summed_working_time(current_task)
    arrival_time = get_summed_up_arrival_times(current_task)

    overall_timer += arrival_time + current_task.duration
    tmp_time = overall_timer - arrival_time
    if tmp_time < 0:
        tmp_time = 0

    current_task.waiting_time = tmp_time

    finished_tasks.append(current_task)
    current_task = get_new_task()


waiting_time_arr = list(map(lambda task: task.waiting_time, finished_tasks))
waiting_time_arr.sort()

dwell_time_arr = list(
    map(lambda task: task.waiting_time + task.duration, finished_tasks))
dwell_time_arr.sort()

fig, (ax1, ax2) = plt.subplots(nrows=1, ncols=2)

ax1.set_title('Verweilzeit')
ax1.hist(dwell_time_arr, 50)

ax2.set_title('Wartezeit')
ax2.hist(waiting_time_arr, 50)

print("Wartezeit: Varianz: ", np.var(waiting_time_arr),
      ", Mittelwert: ", np.average(waiting_time_arr))
print("Verweilzeit: Varianz: ", np.var(dwell_time_arr),
      ", Mittelwert: ", np.average(dwell_time_arr))

plt.show()
