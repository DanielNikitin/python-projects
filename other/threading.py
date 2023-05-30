import threading

def count_up():
    for i in range(10):
        print(f"Counting up: {i}")

def count_down():
    for i in range(10, 0, -1):
        print(f"Counting down: {i}")

t1 = threading.Thread(target=count_up)
t2 = threading.Thread(target=count_down)

t1.start()
t2.start()

t1.join()
t2.join()

print("Finished counting.")
