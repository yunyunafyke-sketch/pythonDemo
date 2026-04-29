t = (1, 2, 3)

t1 = (1, "hello", True)
# ❌ 报错
# t[0] = 100

# ✅ 正确
t2= (1,)

print(t1.count("hello"))

print(t1.index("hello"))


print("=====================")

a = 1
b = 2
c = 3

p = a, b, c
print(p)


l = (1, 2, 3)

d, f, g = l
print(a, b, c)

print("======================")

a=1
b=2
#右边先“组包”
#组包：把多个值装进一个“盒子”（元组）
#解包：把盒子里的值拿出来分给变量
a,b=b,a
print(a, b)

#*b 会接收“剩下的所有元素”
print("======================")
a, *b = [1, 2, 3, 4]
print(b)

print("======================")

students=(("S022","上林",85,92,78),("S092","华积双",92, 88,95))

for s in students:
    print(s)
