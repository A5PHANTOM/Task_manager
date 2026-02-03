from abc import ABC , abstractmethod

class Storage(ABC):

    @abstractmethod
    def load_task(self):
        pass

    @abstractmethod
    def save_tasks(self, task ):
        pass

    @abstractmethod
    def save_all(self , tasks):
        pass

    @abstractmethod
    def get_next_id(self):
        pass

    

