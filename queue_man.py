class QueueMan():
    """docstring for AllQueues."""
    def __init__(self):
        self.real_time = []
        self.prioridade_1 = []
        self.prioridade_2 = []
        self.prioridade_3 = []
        self.threshold = 5

    def size_of_all_queues(self):
        return len(self.real_time) + len(self.prioridade_1) + \
               len(self.prioridade_2) + len(self.prioridade_3)

    def put_in_queue(self, process):
        if self.size_of_all_queues() < 1000:
            if process.prioridade == 0:
                self.real_time.append(process)
            elif process.prioridade == 1:
                self.prioridade_1.append(process)
            elif process.prioridade == 2:
                self.prioridade_2.append(process)
            else:
                self.prioridade_3.append(process)
        else:
            raise Exception("Capacidade maxima de processos atingida (1000).")

    def get_from_queue(self):
        if len(self.real_time) != 0:
            process = self.real_time.pop(0)
        elif len(self.prioridade_1) != 0:
            process = self.prioridade_1.pop(0)
            for p2 in self.prioridade_2:
                p2.age += 1
            for p3 in self.prioridade_3:
                p3.age += 1
        elif len(self.prioridade_2) != 0:
            process = self.prioridade_2.pop(0)
            for p3 in self.prioridade_3:
                p3.age += 1
        else:
            process = self.prioridade_3.pop(0)
        return process

    def print_ages(self):
        print("Prioridade 1:")
        for elem in self.prioridade_1:
            print("PID:", elem.pid)
        print("Prioridade 2:")
        for elem in self.prioridade_2:
            print(elem.pid, "age:", elem.age)
        print("Prioridade 3:")
        for elem in self.prioridade_3:
            print(elem.pid, "age:", elem.age)

    def age(self):
        aumentar_1 = [proc for proc in self.prioridade_2 if proc.age >= self.threshold]
        for proc in aumentar_1:
            proc.age = 0
            proc.prioridade = 1
        self.prioridade_2 = [proc for proc in self.prioridade_2 if proc not in aumentar_1]
        aumentar_2 = [proc for proc in self.prioridade_3 if proc.age >= self.threshold]
        for proc in aumentar_2:
            proc.age = 0
            proc.prioridade = 2
        self.prioridade_3 = [proc for proc in self.prioridade_3 if proc not in aumentar_2]
        self.prioridade_2.extend(aumentar_2)
        self.prioridade_1.extend(aumentar_1)
