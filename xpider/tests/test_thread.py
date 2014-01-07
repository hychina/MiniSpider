from collections import deque
import threading
import time

class MyIter:
    def __init__(self, list_):
        self.list_ = list_
        self.index = 0

    def __iter__(self):
        return self

    def next(self):
        try:
            value = self.list_[self.index]
        except IndexError:
            raise StopIteration
        else:
            self.index += 1
            return value

class Counter(threading.Thread):
    def __init__(self, it):
        threading.Thread.__init__(self)
        self.num_seen = 0
        self.lock = threading.Lock()
        self.it = it

    def run(self):
        global result
        for x in self.it:
            self.num_seen += 1
        print('{0} {1}'.format(self.name, self.num_seen))
        with self.lock:
            result += self.num_seen

def main():
    global result
    # list iterator
    li = [i for i in xrange(1000000)]
    idata = iter(li)
    result = 0
    nthreads = 5

    start_time = time.time()
    threads = [Counter(idata) for n in xrange(nthreads)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    end_time = time.time()
    print('total ' + str(result))
    print('time ' + str(end_time - start_time))

    # race condition
    start_time = end_time
    result = 0
    it = MyIter(li)
    threads = [Counter(it) for n in xrange(nthreads)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    end_time = time.time()
    print('total ' + str(result))
    print('time ' + str(end_time - start_time))

    # deque
    start_time = end_time
    result = 0
    it = iter(deque(li))
    threads = [Counter(it) for n in xrange(nthreads)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    end_time = time.time()
    print('total ' + str(result))
    print('time ' + str(end_time - start_time))

main()
