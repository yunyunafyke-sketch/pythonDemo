dict1={"小明":170,"小红":165}
print(dict1)
print(dict1["小明"])
print("============")


del dict1["小红"]
print(dict1)

dict1["小红"]=165
print(dict1)
print("==========")
print(dict1.keys())
print(dict1.values())
print(dict1.items())

print("========")

for e in dict1:
    print(dict1[e])
