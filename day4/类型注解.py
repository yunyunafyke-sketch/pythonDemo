a: int=695
score: float=100.1
c: str="10"



def calc(scores: list[int])->float:
    return sum(scores)/len(scores)

list1: list[int]=[1,2,3,4,5]
avg :float=calc(list1)
print(avg)