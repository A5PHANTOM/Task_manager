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
        "Search Tasks",
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

# ---------------- SEARCH TASKS ----------------
elif menu == "Search Tasks":
    st.header("🔍 Search Tasks")

    # Get all titles for autocomplete/suggestions
    all_titles = manager.get_all_titles()
    
    if not all_titles:
        st.info("No tasks available")
    else:
        # Searchable dropdown - type to filter, just like Google
        selected_title = st.selectbox(
            "Search and select a task (start typing to filter):",
            options=[""] + all_titles,
            index=0,
            key="search_dropdown"
        )
        
        # Show task details when selected
        if selected_title:
            results = manager.search_tasks(selected_title)
            if results:
                task = results[0]
                st.write("---")
                st.write("**Task Details:**")
                st.write(f"**ID:** {task.task_id}")
                st.write(f"**Title:** {task.title}")
                st.write(f"**Status:** {task.status}")
                st.write(f"**Priority:** {task.priority}")
                st.write(f"**Created:** {task.created_at}")

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
        except TaskNotFount as e:
            st.error(str(e))

# ---------------- DELETE TASK ----------------
elif menu == "Delete Task":
    st.header("❌ Delete Task")

    title = st.text_input("Task Title")

    if st.button("Delete Task"):
        try:
            manager.delete_task(title)
            st.success(f"Task {title} deleted")
        except TaskNotFount as e:
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
