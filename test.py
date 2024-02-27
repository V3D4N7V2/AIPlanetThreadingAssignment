# Import the unittest module
import time
import unittest
# Import the threading module
import threading
# Import your main module
import main

# Define a subclass of unittest.TestCase
class TestMsgQThreaded(unittest.TestCase):

    # Define a test method
    def test_msgqthreaded(self):
        # Set the number of threads and messages
        number_of_threads = 5
        number_of_messages = 10
        waitForCompletionTime = 10
        # Create a dictionary to store the message queues
        message_queues = {}
        # Create a list to store the threads
        threads = []
        # Create a ThreadPoolExecutor to execute the tasks
        executor = main.ThreadPoolExecutor(max_workers=10)
        # Initialize the threads and their respective message queues
        for i in range(number_of_threads):
            message_queues[i] = main.PriorityMessageQueue()
            thread = main.MsgQThreaded(i, message_queues, executor, number_of_messages, number_of_threads)
            threads.append(thread)
            thread.start()
        # Wait for all the threads to finish
        time.sleep(waitForCompletionTime)  # Allow some time for messages to be processed

    # Stop threads
        for thread in threads:
            thread.stop()
            thread.join()
        # Check that all the threads have terminated
        for thread in threads:
            self.assertFalse(thread.is_alive())
        # Check that all the messages have been processed
        for i in range(number_of_threads):
            self.assertTrue(message_queues[i].is_empty())
        # Check that no exceptions have been raised
        for thread in threads:
            self.assertIsNone(thread._exc_info)
        # Shut down the executor
        executor.shutdown()

# Run the tests
if __name__ == '__main__':
    main()
