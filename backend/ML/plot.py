from NeuralNetwork import NeuralNetwork
import matplotlib.pyplot as plt

a = NeuralNetwork()

x, y = [], []
b = a._trainmodel(epochs=10)
falsep, truep = b['FalsePositives'], b['TruePositives']
falsen, truen = b['FalseNegatives'], b['TrueNegatives']

for value in range(9):
    tpr = truep[value] / (truep[value] + falsen[value])
    fpr = falsep[value] / (falsep[value] + truen[value])
    x.append(tpr)
    y.append(fpr)

print(falsep, truep)
print(x,y)





plt.plot(x, y)  
plt.xlabel("False Positive rate")
plt.ylabel("True Positive rate")
plt.title("ROC curve")

plt.grid(True)
plt.show()    
