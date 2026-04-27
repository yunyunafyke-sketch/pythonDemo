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


a=1
b=2
a,b=b,a
print(a, b)