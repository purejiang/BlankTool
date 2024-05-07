# -*- coding:utf-8 -*-
    
def bytes2hex(cls, bytes) -> str:
    """ 字节码转16进制 """
    num = len(bytes)
    hexstr = u""
    for i in range(num):
        t = u"%x" % bytes[i]
        if len(t) % 2:
            hexstr += u"0"
        hexstr += t
    return hexstr.upper()