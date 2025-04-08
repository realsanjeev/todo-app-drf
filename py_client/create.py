from base import post_todo_task

if __name__ == "__main__":
    task = input("Enter the Task title: ")
    description = input("Enter the Task Description (optional): ")
    completed = input("Mark as completed? (y/n): ").lower() == "y"
    public = input("Make task public? (y/n): ").lower() == "y"

    new_data = {
        "task": task,
        "description": description if description else None,
        "completed": completed,
        "public": public,
    }

    endpoint = "http://localhost:8000/api/todos/"
    response = post_todo_task(endpoint=endpoint, json_payload=new_data)
    print("Task created successfully!")
