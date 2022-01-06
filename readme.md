# Clickfree

Installation!

```sh
poetry install
```

## Backend usage

currently, the backend only reads clickup! it lives [here](clickfree/backend.py). Here is an example usage of the backend, to parse your tasks and conver to Norg format. First, we need an import, and to define a username and API_KEY.

```python
from clickfree.backend import Backend, humanize_time


API_KEY = "none of your business"
username = "dr. bones"
```

Next, we load up the client:

```python
client = Backend(API_KEY, username)
dir(Backend)
```

Now we can do whatever we want with our `.tasks`, `.folders`, `.teams`, `.spaces`, and `.lists`, or use the `.client()` method to get more info (docs at [this repo](https://github.com/Imzachjohnson/clickupython)). For example, say we wanted to parse our tasks as norg files:


```python
from clickfree.backend import Backend, humanize_time


def task_to_norg(cli, task):
    start = humanize_time(task.start_date)
    due = humanize_time(task.due_date)
    lists = [l for l in cli.lists if l.id == task.list.id][0].name
    folders = [f for f in cli.folders if f.id == task.folder.id][0].name

    contexts = " ".join([lists, folders])
    status = task.status.status
    result = []
    result.append(f"  #time.due {due.strftime('%Y-%m-%d')}")
    result.append(f"  #time.start {start.strftime('%Y-%m-%d')}")
    result.append(f"  #contexts {contexts}")
    result.append(f"  #folder {task.folder.id}")
    result.append(f"  #list {task.list.id}")
    result.append
    marker_dict = {
            "completed": "  - [x]",
            "open":"  - [ ]",
            "in progress":"  - [-]",
            "blocked": "  - [=]",
            "rejected":"  - [_]",
            "accepted":"  - [-]",
            "in review":"  - [?]"}
    todo = marker_dict[status] + " " + task.name
    result.append(todo)
    if task.text_content is not None:
        info = "  " + "\n  ".join(task.text_content.splitlines())
        result.append(info)
    return result

def norg_tasks(cli, tasks):
    out = ["* Click Up Tasks"]
    for task in tasks:
        out.extend(task_to_norg(cli, task))
        out.append("\n")
    return out


cli = Backend(API_KEY, username)
tasks = norg_tasks(cli, cli.my_tasks)
tasks = "\n".join(tasks)
with open("../clickup.norg", "a") as f:
    f.write(tasks)
```



