import streamlit as st
from core.manager import TaskManager
from storage.json_storage import JSONStorage
from utils.file_ops import import_tasks_from_json, export_tasks_to_csv
from core.exceptions import TaskNotFount

# Initialize manager
storage = JSONStorage("data/tasks.json")
manager = TaskManager(storage)

st.set_page_config(page_title="Smart Task Tracker", layout="centered")

st.title("📝 Smart Task & Activity Tracker")

# Sidebar navigation
menu = st.sidebar.selectbox(
    "Menu",
    [
        "Add Task",
        "View Tasks",
        "Update Task",
        "Delete Task",
        "Import Tasks",
        "Export Tasks",
    ]
)

# ---------------- ADD TASK ----------------
if menu == "Add Task":
    st.header("➕ Add New Task")

    title = st.text_input("Task Title")
    priority = st.selectbox("Priority", ["low", "medium", "high"])

    if st.button("Add Task"):
        if title:
            task = manager.add_task(title, priority)
            st.success(f"Task added: [{task.task_id}] {task.title}")
        else:
            st.error("Title cannot be empty")

# ---------------- VIEW TASKS ----------------
elif menu == "View Tasks":
    st.header("📋 View Tasks")

    status_filter = st.selectbox(
        "Filter by status",
        ["all", "pending", "in-progress", "completed"]
    )

    tasks = (
        manager.list_tasks(status_filter)
        if status_filter != "all"
        else manager.list_tasks()
    )

    if not tasks:
        st.info("No tasks found")
    else:
        for task in tasks:
            st.write(
                f"**[{task.task_id}] {task.title}** "
                f"| {task.status} | {task.priority}"
            )

# ---------------- UPDATE TASK ----------------
elif menu == "Update Task":
    st.header("🔄 Update Task Status")

    task_id = st.number_input("Task ID", min_value=1, step=1)
    new_status = st.selectbox(
        "New Status",
        ["pending", "in-progress", "completed"]
    )

    if st.button("Update Task"):
        try:
            task = manager.update_task_status(task_id, new_status)
            st.success(f"Task {task.task_id} updated to {task.status}")
        except TaskNotFoundError as e:
            st.error(str(e))

# ---------------- DELETE TASK ----------------
elif menu == "Delete Task":
    st.header("❌ Delete Task")

    task_id = st.number_input("Task ID", min_value=1, step=1)

    if st.button("Delete Task"):
        try:
            manager.delete_task(task_id)
            st.success(f"Task {task_id} deleted")
        except TaskNotFoundError as e:
            st.error(str(e))

# ---------------- IMPORT TASKS ----------------
elif menu == "Import Tasks":
    st.header("📥 Import Tasks from JSON")

    uploaded_file = st.file_uploader("Upload JSON file", type=["json"])

    if uploaded_file:
        with open("data/import_temp.json", "wb") as f:
            f.write(uploaded_file.getbuffer())

        import_tasks_from_json("data/import_temp.json", manager)
        st.success("Tasks imported successfully")

# ---------------- EXPORT TASKS ----------------
elif menu == "Export Tasks":
    st.header("📤 Export Tasks to CSV")

    if st.button("Export"):
        export_tasks_to_csv("data/activity_log.csv", manager.list_tasks())
        st.success("Tasks exported to data/activity_log.csv")
