from NeuralNetwork import NeuralNetwork
import matplotlib.pyplot as plt

a = NeuralNetwork()
x = [1,2]
y = []

for epoch in x:
    y.append(a._trainmodel(epoch)['val_accuracy'][-1])

print(x,y)

plt.plot(x, y)  
plt.xlabel("Epochs")
plt.ylabel("Accuracy")
plt.title("Accuracy against amount of Epochs!")

plt.grid(True)
plt.show()    
