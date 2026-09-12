class Task:
    """A single to-do item owned by a User."""

    def __init__(self, title):
        self.title = title
        self.completed = False

    def complete(self):
        if self.completed:
            print(f"ℹ️ Task '{self.title}' is already completed.")
            return
        self.completed = True
        print(f"✅ Task '{self.title}' completed.")


class User:
    """A person who owns a collection of Task objects (composition)."""

    def __init__(self, name):
        self.name = name
        self.tasks = []

    def add_task(self, task):
        self.tasks.append(task)
        print(f"📌 Task '{task.title}' added to {self.name}.")

    def get_task_by_title(self, title):
        for task in self.tasks:
            if task.title == title:
                return task
        return None

    def complete_task(self, title):
        task = self.get_task_by_title(title)
        if not task:
            print("❌ Task not found.")
            return
        task.complete()

    def list_tasks(self):
        if not self.tasks:
            print(f"📭 {self.name} has no tasks.")
            return
        print(f"📋 Tasks for {self.name}:")
        for task in self.tasks:
            status = "✅" if task.completed else "⏳"
            print(f"  {status} {task.title}")
