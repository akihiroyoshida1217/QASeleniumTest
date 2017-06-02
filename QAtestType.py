# -*- coding: utf-8 -*-
import time, multiprocessing

#連続操作命令
def serialRun(preFunc, Func, afterFunc = lambda : ()):
    preFuncRun = [ f() for f in preFunc ]
    FuncRun =[ [ f() for f in Func] for i in range(0, 20) ]
    afterFunc()

#重複操作命令
def parallelRun(Ins1, Ins2, Func1, afterFunc1, Func2, afterFunc2):
    mgr = multiprocessing.Manager()
    d = mgr.dict()
    event1 = multiprocessing.Event()
    event2 = multiprocessing.Event()
    waitFunc1 = Func1[-1].__name__
    waitFunc2 = Func2[-1].__name__
    print(waitFunc1)
    print(waitFunc2)

    ps = [ 
        multiprocessing.Process(target=Ins1.parallelRunChild, args=(d, 'Func1', waitFunc1, event1, event2, Func1, afterFunc1)),
        multiprocessing.Process(target=Ins2.parallelRunChild, args=(d, 'Func2', waitFunc2, event1, event2, Func2, afterFunc2))
    ]

    for p in ps:
        p.start()

    while 'Func1' not in d:
        print("Results:", d)
        time.sleep(1)

    event1.set()

    while 'Func1' not in d or 'Func2' not in d:
        print("Results:", d)
        time.sleep(1)

    event2.set()

    for p in ps:
        p.join()

    print("Results:", d)