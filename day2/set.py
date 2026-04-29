s1={1,2,3,4,5,"1"}
print(s1)
s2={1,2,3,4,5,"2"}
print(s2)

#定义集合名
s3=set()
s3.add(1)
s3.add("3")
s3.remove("3")
s3.add(2)
s3.pop()
print(s3)
s3.clear()
print(s3)

#交、并、差集
s1.intersection(s2)
print(s1)
s1.union(s2)
print(s1)
s1.difference(s2)
print(s1)

s3=s1 & s2
print(s3)
s3=s1|s2
print(s3)
s3=s1-s2
print(s3)

print("s1" +str(s1))
a={i*2 for i in s1}
print(a)

