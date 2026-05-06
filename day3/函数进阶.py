#不定长参数
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


