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

## Assumptions
 - Threads don't know when they have recieved all messages, so let them run for a fixed ammount of time and terminate.
 - This is defined in waitForCompletionTime, which should be sufficient for all threads to recieve and process all messages.
 - stop and join all theads after this interval.
 - Main function tests the code by sending messages from each thread to another thread and then waits for the threads to complete their tasks., 
 - main function  checks if all queues are empty after the threads have completed their tasks.

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
- waitForCompletionTime in main function can be changed to any time to wait for the threads to complete their tasks.

## Test Cases

- Test Case 1: 
  - Total Threads: 7
  - Expected: All threads should send and recieve at least one message to ensure working.

## Good Design and Coding Practices
- Used OOP concepts to create a PriorityMessageQueue class.
- Comments are added to explain the code.
- Used meaningful variable names.
- Used a main function to test the code.
- Mutexes are used to make sure no simultaneous access to the priority queue.