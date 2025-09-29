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
# - https://docs.python.org/3/library/asyncio-sync.html


# Version   Author      Date            Description
# 1         Duke Pham   2025-09-28      Program will attempt to manage process synchronization in a Bounded Buffer problem

import threading 
import time

# Setup
bufferSize = 5
totalItems = 20

# unsafe buffer (queue)
buffer = []

# ====Synchronization primitives======

# Mutex: Controls access to the shared 'buffer' list (lock for critical section)
mutex = threading.Lock()

# Empty: Counts the number of empty slots
empty = threading.Semaphore(bufferSize)

# Full: Counts the number of items in the buffer
full = threading.Semaphore(0)


# Creates continuous items and uses semaphores to block when buffer is full
def producer():

    # Start with first produced item
    producedItemID = 1

    # Set a continuous production of item following the first item
    while True:

        # Assign ID to current item
        producedItem = f"Item-{producedItemID}"

        # Wait for an empty slot. Block if buffer is full 
        empty.acquire()

        # Have mutex lock retrieve the critical section
        mutex.acquire()

        # Load item into buffer (CRITICAL SECTION)
        buffer.append(producedItem)
        print(f"( + ) Producer: Loaded {producedItem} into buffer. Current Load Size: {len(buffer)}")

        # Release mutex lock
        mutex.release()

        # Release one full slot for consumer
        full.release()
        
        # Produce another item, deadlock will occur after consumer finishes
        producedItemID += 1

        # Simulate work being done
        time.sleep(1)

# Consumes items and uses semaphores to block when the buffer is empty
def consumer(totalItemsToConsume):
    itemsConsumed = 0
    while itemsConsumed < totalItemsToConsume:

        # Wait for a full slot to be available
        print("( - ) Consumer: Waiting to eat item...")
        full.acquire()

        # Have mutex lock retrieve the critical section
        mutex.acquire()

        # Remove item from buffer (CRITICAL SECTION)
        consumeItem = buffer.pop(0)

        # Release mutex lock
        mutex.release()

        # Release one empty slot for producer
        empty.release()

        itemsConsumed += 1
        print(f"( - ) Consumer: Ate {consumeItem}. Remaining size to consume: {totalItemsToConsume - itemsConsumed}")


    print("-" * 100)
    print(f"CONSUMER CONSUMED ALL OF THE ITEMS. FINAL BUFFER SIZE: {len(buffer)}. (Press Ctrl+C to stop):")
    print("-" * 100)


# Buffer Problem 
if __name__ == "__main__":

    print("-" * 100)
    print("Process Synchronization In Buffer Bound Problem (Press Ctrl+C to stop):")
    print("-" * 100)


    try:
        # Create producer and consumer threads
        producerThread = threading.Thread(target=producer)
        consumerThread = threading.Thread(target=consumer, args={totalItems,})  

        print(f"Starting Bounded Buffer Simulation (Max Size: {bufferSize}, Total Items: {totalItems})")
        print("-" * 100)

        # Set producer as daemon for clean exit
        producerThread.daemon = True

        producerThread.start()
        consumerThread.start()

        producerThread.join()
        consumerThread.join()

        buffer.join()

        # Apparently you will never see this unless you press Ctrl+C
        print("\nPROCESS SYNCHRONIZATION COMPLETED...")
        print(f"Final Buffer Size: {len(buffer)}")
    except KeyboardInterrupt:
        # Handle exit on Ctrl+C
        print("\n\nProgram stopped.")
        