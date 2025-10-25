import threading, time
open_tasks = {}

def send_message(target, message):
    # Baileys send logic here
    print(f"Sending to {target}: {message}")

def task_runner(data):
    targets = data['targets']
    message = data['message']
    delay = int(data['delay'])
    task_id = str(time.time())
    open_tasks[task_id] = True

    for target in targets:
        if not open_tasks.get(task_id): break
        send_message(target, message)
        time.sleep(delay)

    open_tasks.pop(task_id, None)

def start_task(data):
    thread = threading.Thread(target=task_runner, args=(data,))
    thread.start()
    return str(time.time())

def stop_task(task_id):
    open_tasks[task_id] = False
