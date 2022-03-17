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
        self.hungry = self.manager.list(lista)
        self.num_eating = 0
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
            self.hungry[num] = True
            self.free_fork.wait_for(self.no_comen_lados)
            
            self.eating[num] = True
            self.num_eating += 1
            self.hungry[num] = False
        finally:
            self.mutex.release()

    def wants_think(self, num:int):
        self.mutex.acquire()
        try:
            self.eating[num] = False
            self.num_eating -= 1
            self.free_fork.notify()
        finally:
            self.mutex.release()
            
            
            
class CheatMonitor():
    def __init__(self):
        self.mutex = Lock()
        self.num_cheating = Value('i', 0)
        self.can_stop_eating_02 = Condition(self.mutex)
        
    def is_eating(self, num):
        self.mutex.acquire()
        try:
            self.num_cheating.value += 1
            self.can_stop_eating_02.notify_all()
        finally:
            self.mutex.release()

    def other_eating_02(self):
        return self.num_cheating.value == 2
    
    def wants_think(self, num):
        self.mutex.acquire()
        try:
            self.can_stop_eating_02.wait_for(self.other_eating_02)
            self.num_cheating.value -= 1
        finally:
            self.mutex.release()
            
#class AnticheatTable():