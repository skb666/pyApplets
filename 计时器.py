import time
class Timer():
    def __init__(self):
        self.__begin=0
        self.__end=0
        self.t_long=0
        self.__string="未开始计时"
    def __str__(self):
        return self.__string
    __repr__=__str__
    def __add__(self,other):
        tmp=self.t_long+other.t_long
        m, s = divmod(tmp, 60)
        h, m = divmod(m, 60)
        print("时长：%02d:%02d:%02d" % (h, m, s))
    def start(self):
        if self.__begin==0:
            self.__string="计时中"
            self.__begin=time.time()
            print('计时开始')
        else:
            print("已经开始计时")
    def stop(self):
        if self.__end==0:
            self.__end=time.time()
            print('计时结束')
            self.__cale()
        else:
            print("请先开始计时")
    def __cale(self):
        self.t_long=int(self.__end-self.__begin)
        m, s = divmod(self.t_long, 60)
        h, m = divmod(m, 60)
        self.__start=0
        self.__begin=0
        self.__string=("时长：%02d:%02d:%02d" % (h, m, s))

        
