from sqlalchemy import create_engine,Column,Integer,String
from sqlalchemy.orm import declarative_base,sessionmaker
from core.models import Task

Base = declarative_base()

class TaskModel(Base):
    __tablename__ = "tasks"

    task_id = Column(Integer,primary_key=True)
    title = Column(String)
    status = Column(String)
    priority = Column(String)


class DBStorage :
    def __init__(self,db_url="sqlite:///tasks.db"):
        self.engine = create_engine(db_url)
        Base.metadata.create_all(self.engine)
        self.Session =sessionmaker(bind=self.engine)

    def load_tasks(self):
        session = self.Session()
        rows = session.query(TaskModel).all()
        tasks = [Task(r.task_id, r.title, r.status, r.priority) for r in rows]
        session.close()
        return tasks
    
    def save_task(self,task):
        session = self.Session()
        row = TaskModel(
            task_id=task.task_id,
            title=task.title,
            status=task.status,
            priority=task.priority
        )
        session.add(row)
        session.commit()
        session.close()

    def save_all(self,tasks):
        session = self.Session()
        session.query(TaskModel).delete()
        for task in tasks :
            row = TaskModel(
                task_id=task.task_id,
                title=task.title,
                status=task.status,
                priority=task.priority
            )
            session.add(row)
        session.commit()
        session.close()

    def get_next_id (self):
        tasks = self.load_tasks()
        if not  tasks:
            return 1
        return max(t.task_id for t in tasks)+1
    

        


