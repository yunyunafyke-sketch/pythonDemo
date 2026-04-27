list=[1,2,3]
print(list[0])
print("================")

list[1]=1
print(list[1])
print(list)

print("================")

del list[1]
print(list[1])
print(list)

print("================")
list1=[1,2,3,4,5,6]
print(list1[1:6:2])

print("================")
list1.append(7)
print(list1)

print("================")
list1.insert(0,92)
print(list1)


print("================")
list1.remove(2)
print(list1)


print("================")
list1.pop()
print(list1)


print("================")
list1.sort()
print(list1)


print("================")
list1.reverse()
print(list1)


print("================")

print(list1)
print("min:"+str(min(list1)))
print("max:"+str(max(list1)))
print("sum:"+str(sum(list1)))
print("len:"+str(len(list1)))

print("================")

list2=list1+list
print(list2)
print("===============")

list3=[*list2,*list1]
print(list3)

print("===============")
print (1 in list3)
print (0 in list3)
print("===============")

list4 = [1, 2, 3, 4, 5, 6]
#[x for x in list3 if x == 3]
# ↑   ↑        ↑
#放入  遍历     条件
result = [x for x in list4 if x == 3]
print(result)

print("===============")
list5 = [1, 2, 3, 5, 92, 6]
result2=[i*2 for i in list4]
print(result2)


