import pickle
import os

data = os.listdir("./data")
print(data)
name = input("Which file to plot: ")

file = open("./data/" + name, 'rb')
circles = pickle.load(file)

for c in circles:
    print(c.x)
