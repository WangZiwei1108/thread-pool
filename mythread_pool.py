#@author:WangZiwei
import threading
import queue

class FunctionHandle():
    def __init__(self,funcname,*args):
        self.funcname = funcname
        self.args = args

class MyThreadPool(threading.Thread):
    def __init__(self,thread_num):
        super().__init__()
        self.thread_num = thread_num
        self.thread_list = []
        self.q = queue.Queue()
        self.status = 'start'
        for i in range(self.thread_num):
            new_thread = WorkThread(self.q,self)
            new_thread.start()
            self.thread_list.append(new_thread)

    def handle_threads(self,funcname,*args):
        t = FunctionHandle(funcname,args)
        self.q.put(t)
        #print(self.q.qsize())

    def kill_threadpool(self):
        self.status = 'stop'

class WorkThread(threading.Thread):
    def __init__(self,q,thread_pool):
        super().__init__()
        self.q = q
        self.thread_pool = thread_pool

    def run(self):
        while True:
            if self.thread_pool.status == 'stop':
                break
                print(self.thread_pool.status)
            try:
                t = self.q.get(timeout=1)
                print('it is t',t)
                if not t == None:
                    print(self.thread_pool.status)
                    t.funcname(t.args)
            except Exception as e:
                print(e)

def write(str):
    print(str, threading.current_thread().name)

if __name__ == '__main__':
    test = MyThreadPool(5)
    for i in range(1000):
        test.handle_threads(write, 'hi'+str(i))

    test.kill_threadpool()


