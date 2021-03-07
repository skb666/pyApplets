import serial
import struct


class SerialPort(object):
    def __init__(self, port="/dev/ttyS0", baudrate=115200, timeout=5.0):
        # print('__init__')
        self.__sp = serial.Serial(port, baudrate, timeout=timeout)
        self.__sendDict = {
            "_byte": [],
            "_short": [],
            "_int": [],
            "_float": [],
            "_longlong": [],
            "_double": [],
        }
        self.__receiveDict = {
            "byte": [],
            "short": [],
            "int": [],
            "float": [],
            "long long": [],
            "double": [],
        }
    
    def __enter__(self):
        # print('__enter__')
        return self

    def __exit__(self, _type, _value, _trace):
        # print('__exit__', _type, _value, _trace)
        if self.__sp.is_open:
            self.__sp.close()

    def __clearReceiveBuffer(self):
        for buf in self.__receiveDict.values():
            buf.clear()

    def clearBuffer(self):
        for buf in self.__sendDict.values():
            buf.clear()

    def setData(self, **vardict):
        for key, value in vardict.items():
            self.__sendDict[key] = value

    def appendData(self, **vardict):
        for key, value in vardict.items():
            if type(value) == list:
                self.__sendDict[key].extend(value)
            else:
                self.__sendDict[key].append(value)

    def getReceive(self):
        return self.__receiveDict

    def sendData(self):
        # 包头
        _message = b'\xa5'
        # 数据数量
        lByte = len(self.__sendDict["_byte"])
        lShort = len(self.__sendDict["_short"])
        lInt = len(self.__sendDict["_int"])
        lFloat = len(self.__sendDict["_float"])
        lLongLong = len(self.__sendDict["_longlong"])
        lDouble = len(self.__sendDict["_double"])
        # 数据格式
        _message += struct.pack('BBBBBB', lByte, lShort, lInt, lFloat, lLongLong, lDouble)
        _format = '>' + 'B'*lByte + 'h'*lShort + 'i'*lInt + 'f'*lFloat + 'q'*lLongLong + 'd'*lDouble
        # 数据本体
        tmpList = [value for key, values in self.__sendDict.items() if values for value in values]
        _message += struct.pack(_format, *tmpList)
        # 校验和
        checksum = sum(_message[1:])
        _message += struct.pack('B', checksum%256)
        # 包尾
        _message += b'\x5a'
        # 发送数据
        self.__sp.write(_message)

    def receiveData(self):
        bt = self.__sp.read()
        # 检测包头
        if bt == b'\xa5':
            # 获取数据数量
            _message = self.__sp.read(6)
            num = sum(map((lambda x, y: x*y), [1, 2, 4, 4, 8, 8], _message))
            # 获取数据本体
            _message += self.__sp.read(num)
            # 检测校验和
            checksum = struct.pack('B', sum(_message)%256)
            if checksum == self.__sp.read():
                # 检测包尾
                bw = self.__sp.read()
                if bw == b'\x5a':
                    # 解包数据数量
                    lByte, lShort, lInt, lFloat, lLongLong, lDouble = struct.unpack('BBBBBB', _message[:6])
                    # 清空接收缓存
                    self.__clearReceiveBuffer()
                    # 解包数据本体
                    _format = '>' + 'B'*lByte + 'h'*lShort + 'i'*lInt + 'f'*lFloat + 'q'*lLongLong + 'd'*lDouble
                    receiveUnpack = struct.unpack(_format, _message[6:])
                    receiveUnpack=list(reversed(receiveUnpack))
                    # print(receiveUnpack)
                    # 将解包后的数据填入接收缓存
                    while lByte:
                        self.__receiveDict["byte"].append(receiveUnpack.pop())
                        lByte -= 1
                    while lShort:
                        self.__receiveDict["short"].append(receiveUnpack.pop())
                        lShort -= 1
                    while lInt:
                        self.__receiveDict["int"].append(receiveUnpack.pop())
                        lInt -= 1
                    while lFloat:
                        self.__receiveDict["float"].append(receiveUnpack.pop())
                        lFloat -= 1
                    while lLongLong:
                        self.__receiveDict["long long"].append(receiveUnpack.pop())
                        lLongLong -= 1
                    while lDouble:
                        self.__receiveDict["double"].append(receiveUnpack.pop())
                        lDouble -= 1
                    return True
        return False


if __name__ == '__main__':
    with SerialPort() as sp:
        sp.setData(_int=[9, 8, 7])
        sp.clearBuffer()
        sp.appendData(_int=[1, 2, 3, 4], _float=3.14159, _byte=ord('s'),)
        sp.sendData()
        while True:
            if sp.receiveData():
                print(sp.getReceive())
