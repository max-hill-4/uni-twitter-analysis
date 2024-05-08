from NaiveBayes import NaiveBayes
import matplotlib.pyplot as plt

a = NaiveBayes()
data = [0.01,0.02,0.03,0.05,0.07,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.9,]
accuracy = []
for i in data:
    accuracy.append(a._trainmodel(i))
    print(f'finished {i}')

print(data)
print(accuracy)
plt.plot(data, accuracy)  
plt.xlabel("Percetage of train data")
plt.ylabel("Accuracy")
plt.title("Accuracy against test data!")

plt.grid(True)
plt.show()    