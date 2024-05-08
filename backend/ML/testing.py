from NaiveBayes import NaiveBayes
import matplotlib.pyplot as plt

a = NaiveBayes()
data = [0.2]
accuracy = []
for i in data:
    accuracy.append(a._trainmodel(i))
    print(f'finished {i}')

"""
print(data)
print(accuracy)
plt.plot(data, accuracy)  
plt.xlabel("Percetage of train data")
plt.ylabel("Accuracy")
plt.title("Accuracy against test data!")

plt.grid(True)
plt.show()    
"""