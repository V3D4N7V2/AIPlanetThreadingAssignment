import random
import time
import threading
from queue import PriorityQueue
from concurrent.futures import ThreadPoolExecutor

class PriorityMessageQueue:
    def __init__(self):
        self.queue = PriorityQueue()
        self.lock = threading.Lock()

    # Add a message with a given priority
    def enqueue_msg(self, priority, message):
        with self.lock:
            self.queue.put((priority, message))

    # Pop the message with the highest priority
    def dequeue_msg(self):
        with self.lock:
            if self.queue.empty():
                return None
            return self.queue.get()[1]
    # Get Top Message
    def peek(self):
        with self.lock:
            if self.queue.empty():
                return None
            return self.queue.queue[0][1]

    def is_empty(self):
        with self.lock:
            return self.queue.empty()


class MsgQThreaded(threading.Thread):
    def __init__(self, tid, msg_queues, executor, randomMessagesCount=0, number_of_threads=0):
        threading.Thread.__init__(self)
        # for sending random messages.
        self.randomMessagesCount = randomMessagesCount
        self.number_of_threads = number_of_threads

        # set up current thread.
        self.tid = tid
        self.message_queue = msg_queues[tid]
        self.message_queues = msg_queues
        self.executor = executor

        # for thread control sleep and termination.
        self.terminate = threading.Event() # for terminating program to end exec in specified time.
        self.canwake = threading.Event() # for sleeping and waking up
        self.sleeping = False

    def run(self):
        #  Send few messages to randomly picked nodes.
        for _ in range(self.randomMessagesCount):
            if self.number_of_threads == 1: raise ValueError("Number of threads should be greater than 1")
            sendToThreadID = random.randint(0, self.number_of_threads - 1)
            while sendToThreadID == self.tid: # Ensure sender and receiver are different
                sendToThreadID = random.randint(0, self.number_of_threads - 1)
            priority = random.randint(1, 5)
            msg = f"Random message from Thread {self.tid} to Thread {sendToThreadID} with priority {priority}"
            self.msg_send(sendToThreadID, priority, msg)

        # Main loop read and process recieved messages.
        while not self.terminate.is_set():
            print(f"[THREADSTATUS] Thread {self.tid} is running")
            if not self.message_queue.is_empty():
                msg = self.message_queue.dequeue_msg() # read message from queue
                self.executor.submit(self.msg_process, msg) # process message in thread pool
            else:
                print(f"[THREADSTATUS] Thread {self.tid} is going to sleep")
                self.sleeping = True
                self.canwake.clear()  # Clear wake event
                self.canwake.wait()   # Sleep until wake event is set
                print(f"[THREADSTATUS] Thread {self.tid} is awake")
                self.sleeping = False
        print(f"[THREADSTATUS] Thread {self.tid} is terminating")

    # Process the message
    def msg_process(self, msg):
        print(f"[PROCESSING] T{self.tid} received & will process: {msg}")
        time.sleep(random.random()) # doing something wiht data... wait for some time...
        print(f"[PROCESSING] T{self.tid} processing {msg} done")

    # send message to another thread
    def msg_send(self, r_tid, priority, msg):
        if r_tid in self.message_queues.keys():
            self.message_queues[r_tid].enqueue_msg(priority, msg)
            print(f"T{self.tid} sent {msg} to T{r_tid}")
            for thread in threading.enumerate():
                if isinstance(thread, MsgQThreaded) and thread.tid == r_tid: # Wake up the recipient thread if it's sleeping
                    thread.wake_up()
    # Stop the thread
    def stop(self):
        self.terminate.set()  # for terminating program
        if self.sleeping:
            self.canwake.set()  # Set wake event
    # Wake up the thread
    def wake_up(self):
        if self.sleeping:
            self.canwake.set()  # Set wake event


def main():
    numThreads = 7
    msg_queues = {}
    threadsList = []
    executor = ThreadPoolExecutor(max_workers=7)
    # Initialize threads and their respective message queues
    for i in range(numThreads):
        msg_queues[i] = PriorityMessageQueue()
        messagesCount = random.randint(1, 5) # set random messages for each thread., can be set to a static value randomMessagesCountto set a fixed number of messages to random hosts. 
        thread = MsgQThreaded(i, msg_queues, executor, messagesCount, numThreads)
        threadsList.append(thread)
        thread.start()

    # Devault Messages, to avoid no messages sent.
    threadsList[0].msg_send(r_tid=6, priority=2, msg="Default Message T0 -> T6 Priority 2")
    threadsList[1].msg_send(r_tid=5, priority=1, msg="Default Message T1 -> T5 Priority 1")
    threadsList[2].msg_send(r_tid=4, priority=3, msg="Default Message T2 -> T4 Priority 3")
    threadsList[3].msg_send(r_tid=3, priority=2, msg="Default Message T3 -> T3 Priority 2")
    threadsList[4].msg_send(r_tid=2, priority=1, msg="Default Message T4 -> T2 Priority 1")
    threadsList[5].msg_send(r_tid=1, priority=2, msg="Default Message T5 -> T1 Priority 2")
    threadsList[6].msg_send(r_tid=0, priority=2, msg="Default Message T6 -> T0 Priority 2")
    

    time.sleep(10)  # Allow some time for messages to be processed

    # Stop threads
    for thread in threadsList:
        thread.stop()
        thread.join()
    # clpse Thread Pool.
    executor.shutdown()


if __name__ == "__main__":
    main()
