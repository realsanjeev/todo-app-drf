from base import update_todo_task

if __name__ == "__main__":
    while True:
        try:
            id = int(input("Enter the id of task you want to update: "))
            break
        except ValueError:
            print("Please enter valid id value in (integer type)")

    task = input("Enter the Task title: ")
    description = input("Enter the Task Description: ")
    new_data = {"task": task, "description": description}
    endpoint = f"http://localhost:8000/api/todos/{id}/update/"
    update_todo_task(endpoint=endpoint, json_payload=new_data)
