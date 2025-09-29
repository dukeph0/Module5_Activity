# Purpose: Develop a Python program that uses a semaphore to manage process synchronization and prevent deadlocks.
# This includes: 
# - Being able to retrieve semaphore initialization details
# - Enforcing the maximum output of concurrent processes
# - Implementing a structured output pattern

# Expected Result: Displays the use of a semaphore to manage process synchronization and prevent deadlocks

# References: 
# - https://docs.python.org/3/library/threading.html
# - https://www.tutorialspoint.com/python/python_thread_deadlock.htm
# - https://www.baeldung.com/cs/bounded-buffer-problem
# - https://docs.python.org/3/library/queue.html


# Version   Author      Date            Description
# 1         Duke Pham   2025-09-28      Program will attempt to manage process synchronization in a Bounded Buffer problem

import threading 
import time
import random
import queue

# Setup
bufferSize = 5
totalItems = 20

# unsafe buffer (queue)
buffer = []

# Define Synchronization primitives:

# Mutex: Controls access to the shared 'buffer' list (lock for critical section)
mutex = threading.Lock()

# Empty: Counts the number of empty slots
empty = threading.Semaphore(bufferSize)

# Full: Counts the number of items in the buffer
full = threading.Semaphore(0)


# Creates continuous items to be loaded into buffer
def producer():

    # Start with first produced item
    producedItemID = 1

    # Set a continuous production of item following the first item
    while True:

        if len(buffer) >= bufferSize:
            print(f"( + ) Producer: Buffer full (Size {len(buffer)}). Waiting....")
            time.sleep(0.5)
            continue

        producedItem = f"Item-{producedItemID}"

        # Load item into buffer
        print(f"( + ) Producer: Loading {producedItem} into buffer...")
        buffer.append(producedItem)

        print(f"( + ) Producer: Loaded {producedItem} into buffer. Current Load Size: {len(buffer)}")
        producedItemID += 1

        time.sleep(random.uniform(0.5, 1.0))

    print("-" * 100)
    print(f"PRODUCTION HAS ENDED...")
    print("-" * 100)

def consumer(totalItemsToConsume):
    itemsConsumed = 0
    while itemsConsumed < totalItemsToConsume:

        if buffer:
            try:
                consumeItem = buffer.pop(0)

                itemsConsumed += 1
                
                print(f"( - ) Consumer: Ate {consumeItem}. Remaining size to consume: {totalItemsToConsume - itemsConsumed}")
        
            except IndexError:
                print("CONSUMER FAILED: Tried to pop from an empty buffer (IndexError)")
                time.sleep(0.1)
                continue

        else:
            print("( - ) Consumer: Waiting to eat item...")
            time.sleep(0.5)

        time.sleep(random.uniform(0.5, 1.0))

    print("-" * 100)
    print(f"CONSUMER CONSUMED ALL OF THE ITEMS...")
    print("-" * 100)


# Buffer Problem 
if __name__ == "__main__":

    print("-" * 100)
    print("Process Synchronization In Buffer Bound Problem (Press Ctrl+C to stop):")
    print("-" * 100)


    try:
        # Create producer and consumer threads
        producerThread = threading.Thread(target=producer)
        consumerThread = threading.Thread(target=consumer, args={totalItems})  

        print(f"Starting Bounded Buffer Simulation (Max Size: {bufferSize}, Total Items: {totalItems})")
        print("-" * 100)

        producerThread.start()
        consumerThread.start()

        producerThread.join()
        consumerThread.join()

        buffer.join()

        print("\nPROCESS SYNCHRONIZATION COMPLETED...")
        print(f"Final Buffer Size: {len(buffer)}")
    except KeyboardInterrupt:
        # Handle exit on Ctrl+C
        print("\n\nProgram stopped.")