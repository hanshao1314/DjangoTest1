"""
如果a+b+c=1000，且a^2+b^2=c^2 (a,b,c 为自然数)，如何求出所有a、b、c可能的组合?
a
b
C
"""

import time

start_time=time.time()
for a in range(0,1001):
    for b in range(0,1001):
        for c in range(0,1001):
            if a+b+c==1000 and a**2+b**2==c**2:
                print("a,b,c:%d,%d,%d"%(a,b,c))
end_time=time.time()
print("times1:%d"%(end_time-start_time))
print("finished")

start_time=time.time()
for a in range(0,1001):
    for b in range(0,1001):
        if a**2+b**2==(1000-a-b)**2:
            print("a,b,c:%d,%d,%d" % (a, b, (1000-a-b)))
end_time=time.time()
print("times2:%d"%(end_time-start_time))
print("finished")



def t1():
    l=[]
    for i in range(3000):
        l=l+[i]
def t2():
    l=[]
    for i in range(3000):
        l.append(i)
def t3():
    l=[i for i in range(3000)]
def t4():
    l=list(range(3000))
def t5():
    li=[]
    for i in range(3000):
        li.extend([i])

from timeit import Timer

timer1=Timer("t1()","from __main__ import t1")
print("+:",timer1.timeit(500))

timer2=Timer("t2()","from __main__ import t2")
print("append:",timer2.timeit(500))

timer3=Timer("t3()","from __main__ import t3")
print("[i for i in range]:",timer3.timeit(500))

timer4=Timer("t4()","from __main__ import t4")
print("list:",timer4.timeit(500))

timer5=Timer("t5()","from __main__ import t5")
print("extend:",timer5.timeit(500))