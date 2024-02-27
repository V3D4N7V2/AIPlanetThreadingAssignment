# AI Planet: Multi-Threaded Priority Message Queue Assignment

##Execution Steps:
1. Clone the repository
2. Navigate to the repository folder
3. requirement.txt should not be needed as all packages ship with python3 by default.
4. Run the following command to execute the program
```
python3 main.py
```
## Overview

 - Each thread maintains a priority queue of received messages. And processes the messages in the order of priority.
 - A "PriorityMessageQueue" class has all fucntions realted to the priority queue. such as enqueue, dequeue, peek, etc.
 - Each message has a priority and a payload.
 - Each thread on start randomly sends messages to other threads.
 - It also wakes the reciever, so that it can handle the message if it was sleeping.
 - Then processes the messages from other threads.

## General Info
   - Runs 7 threads that send messages to each other.
   - 7 Threads in thread pool that process the messages.
   - main function creates the threads and starts them.
   - Main function also sends one message from thread i to thread 7-i+1. to test each thread sending and recieving messages.

## Data Structures Used
- Priority Queue: To store the messages in order of priority.
- Dictionary: To store the threads and their priority queues.
- Lists
  
## Notes
- numThreads in main function can be changed to any number of threads.
- messagesCount in main function can be changed to any number of messages to send to randmonly picked threads.
