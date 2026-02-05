import argparse
from core.manager import TaskManager
from storage.json_storage import JSONStorage
from core.exceptions import TaskNotFount

def get_manager():
    storage = JSONStorage('data/tasks.json')
    return TaskManager(storage)

def add_task(args):
    manager = get_manager()
    task = manager.add_task(args.title, args.priority)
    print(f"Task added :[{task.task_id}] {task.title}")

def list_tasks(args):
    manager = get_manager()
    tasks = manager.list_tasks(args.status)

    if not tasks:
        print("No tasks found")
        return 
    for task in tasks:
         print(f"[{task.task_id}] {task.title} | {task.status} | {task.priority}")


def update_task(args):
    manager = get_manager()
    try :
        task = manager.update_task_status(args.id,args.status)
        print(f"Task {task.task_id} updated to {task.status}")
    except TaskNotFount as e :
        print(e)


def delete_task(args):
    manager = get_manager()
    try:
        manager.delete_task(args.id)
        print(f"Task {args.id} deteled")
    except TaskNotFount as e:
        return(e)
    


def main () :
    parser = argparse.ArgumentParser(description="Smart Task Tracker")
    subparsers = parser.add_subparsers(dest="command")

    #add
    add_parser = subparsers.add_parser("add")
    add_parser.add_argument("--title",required=True)
    add_parser.add_argument("--priority",default="medium")
    add_parser.set_defaults(func=add_task)

    #list
    list_parser = subparsers.add_parser("list")
    list_parser.add_argument("--status",choices=["pending","in-progress","completed"])
    list_parser.set_defaults(func=list_tasks)

    #update 
    update_parser = subparsers.add_parser("update")
    update_parser.add_argument("--id",type= int ,required=True)
    update_parser.add_argument("--status",required=True)
    update_parser.set_defaults(func=update_task)
    
    #delete
    delete_parser = subparsers.add_parser("delete")
    delete_parser.add_argument("--id",type=int,required=True)
    delete_parser.set_defaults(func=delete_task)

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return 
    
    args.func(args)

if __name__ == "__main__":
    main()