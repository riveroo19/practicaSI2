import matplotlib.pyplot as plt
from sklearn import tree
import json

def checkPrediction(predict, data):
    aciertos= 0
    fallos= 0
    for i in range(0,len(predict)):
        if predict[i]==data[i]: aciertos+=1
        else: fallos +=1
    return aciertos,fallos

f = open('../../devices_IA_clases.json')
data_train = json.load(f)
f.close()
f = open('../../devices_IA_predecir_v2.json')
data_predict = json.load(f)
f.close()

data_x_train = []
data_y_train = []
data_x_predict = []
data_y = []

for user in data_train:
    coeficiente = user['servicios_inseguros']/user['servicios'] if user['servicios']!=0 else 0
    data_x_train.append([coeficiente])
    data_y_train.append(user['peligroso'])

for user in data_predict:
    coeficiente = user['servicios_inseguros']/user['servicios'] if user['servicios']!=0 else 0
    data_x_predict.append([coeficiente])
    data_y.append(user['peligroso'])

clf = tree.DecisionTreeClassifier()
clf = clf.fit(data_x_train, data_y_train)

data_y_predict = clf.predict(data_x_predict)
aciertos,fallos = checkPrediction(data_y_predict,data_y)
print("ACIERTOS => " + str(aciertos))
print("FALLOS => " + str(fallos))


tree.plot_tree(clf,filled=True,feature_names=["coeficiente"],fontsize=7,class_names=["no peligroso","peligroso"])
plt.show()