import multiprocessing.dummy as multiprocessing
from time import sleep
import queue
import uuid
import random


input = multiprocessing.Queue()
stop_event = multiprocessing.Event()
stored_data = []
uuid_to_index = {}


def generate_data(id):
    value = 1
    while True:
        if stop_event.is_set():
            break
        input.put((id, value))
        value += 1


def persist_data(stored_data, uuid_to_index):
    while True:
        try:
            data = input.get(True, 1)
            guid = uuid.uuid4().hex
            uuid_to_index[guid] = len(stored_data)
            stored_data.append(data + (guid,))
        except queue.Empty:
            break


def main():
    data_persister = multiprocessing.Process(target=persist_data, args=(stored_data, uuid_to_index))
    data_persister.start()
    generators = [0] * 8
    for i in range(8):
        generators[i] = multiprocessing.Process(target=generate_data, args=(i,))
        generators[i].start()
    sleep(4)
    stop_event.set()
    data_persister.join()
    print('time to find data out of {} entries'.format(len(stored_data)))
    i = random.randrange(len(stored_data))
    print('finding index {}: {}'.format(i, stored_data[i]))
    print(stored_data[uuid_to_index[stored_data[i][2]]])

    print('done')


if __name__ == '__main__':
    main()
