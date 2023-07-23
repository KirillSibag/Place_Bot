import pickle

#размер поля
l = 1000
# создаём массив
data = []
data = [0] * (l * l)

# сохраняем
try:
    with open("data.pickle", "wb") as f:
        pickle.dump(data, f, protocol=pickle.HIGHEST_PROTOCOL)
except Exception as ex:
    print("Error during pickling object (Possibly unsupported):", ex)
