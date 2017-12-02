class AllQueues():
    """docstring for AllQueues."""
    def __init__(self, arg):
        super(AllQueues, self).__init__()
        self.real_time = Queue()
        self.priority_1 = Queue()
        self.priority_2 = Queue()
        self.priority_3 = Queue()

    def sizeOfAllQueues():
        return real_time.qsize() + priority_1.qsize() + priority_2.qsize() + priority_3.qsize()


    def putInQueue(process):
        if sizeOfAllQueues()<1000:
            if process.priority == 0:
                real_time.put()
            elif process.priority == 1:
                priority_1.put()
            elif process.priority == 2:
                priority_2.put()
            else:
                priority_3.put()
        else:
            print("já tem mil")

        def getFromQueue():
            if real_time.qsize() != 0:
                return real_time.get()
            elif priority_1.qsize() != 0:
                process = priority_1.get()
                process.priority+=1
                return process
            elif priority_2.qsize() != 0:
                process = priority_2.get()
                process.priority+=1
                return process
            else:
                process = priority_3.get()
                return process
