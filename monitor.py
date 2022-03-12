from multiprocessing import Value, Array
from multiprocessing import Lock, Manager, Condition

class Table():
    def __init__(self, num:int, manager):
        self.mutex = Lock()
        self.num = num
        self.manager = Manager()
        self.current_phil = None
        lista = []
        for i in range(self.num):
            lista.append(False)
        self.eating = self.manager.list(lista)
        self.free_fork = Condition(self.mutex)
        
    def set_current_phil(self, num:int):
        self.current_phil = num
    
    def no_comen_lados(self):
        derecha = (self.current_phil + 1) % self.num
        izquierda = (self.current_phil - 1) % self.num
        return (not(self.eating[derecha]) and not(self.eating[izquierda]))
        
    def wants_eat(self, num:int):
        self.mutex.acquire()
        try:
            self.free_fork.wait_for(self.no_comen_lados)
            self.eating[num] = True
        finally:
            self.mutex.release()

    def wants_think(self, num:int):
        self.mutex.acquire()
        try:
            self.eating[num] = False
            self.free_fork.notify()
        finally:
            self.mutex.release()