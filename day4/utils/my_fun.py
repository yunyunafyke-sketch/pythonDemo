# __all__是一个模块级别的特殊变量，用于指定 from 模块名 import * 时会导入哪些功能（*通配了哪些功能
__all__=["log_separator1"]

def log_separator1():
    print("-"*30)

def log_separator2():
    print("*" * 30)

#__name__ ：Python中内理变量，我示的当前優处的名字（政接运行当前優处，__name__的监为“__main__”；当该模处被导入时，__name__的监就是模块名
if __name__ == '__main__':
    print(__name__)
    log_separator2()

#1


#11111
