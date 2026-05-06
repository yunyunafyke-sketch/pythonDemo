#不定长参数（参数个数不确定，此时就可以使用不定长参数解决这类问题）
#不定长位置参数，函数调用时，通过位置参数传递多个参数封装到一个元组（tuple）中
#不定长关键字参数，函数调用时，通过关键字参数传递多个参数封装到一个字典（dict）
def cacl_data(*args):
    min_data=min(args)
    max_data=max(args)
    return max_data,min_data
print(cacl_data(1,2,3,4))


def cacl_data2(*args,**kwargs):
    min_data=min(args)
    max_data=max(args)
    round1 =1
    if kwargs.get('digits'):
        round1= kwargs.get('digits')
    return max_data,min_data,round1
print(cacl_data2(1,2,3,4,digits=2))


#函数作为参数
def add (x,y):
    return x+y

def mul (x,y,oper):
    return oper(x,y)

c=mul(1,2,add)
print(c)


#匿名函数
addDemo= lambda x,y : x+y
print(addDemo(3,4))


print("======================")


data_list=['C','C++','JAVA','C#']
data_list.sort(key=lambda item: len(item),reverse=True)
print(data_list)


