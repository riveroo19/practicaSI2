import matplotlib.pyplot as plt
import numpy as np
from sklearn import datasets, linear_model
from sklearn.metrics import mean_squared_error, r2_score
import json


f = open('../../devices_IA_clases.json')
data_train = json.load(f)
f.close()
f = open('../../devices_IA_predecir.json')
data_predict = json.load(f)
f.close()

data_x_train = []
data_y_train = []
data_x_predict = []

for user in data_train:
    data_x_train.append([user['servicios_inseguros']])
    data_y_train.append(user['peligroso'])

for user in data_predict:
    data_x_predict.append([user['servicios_inseguros']])
    #data_y_predict.append(user['peligroso'])

data_x_train = data_x_train
data_y_train = data_y_train

print(len(data_x_train))
print(len(data_y_train))

regr = linear_model.LinearRegression()
regr.fit(data_x_train,data_y_train)
print(regr.coef_)
data_y_predict = regr.predict(data_x_predict)

print("Mean squared error: %.2f" % mean_squared_error(data_y_train, data_y_predict))
# Plot outputs
plt.scatter(data_x_predict, data_y_train, color="black")
plt.plot(data_x_predict, data_y_predict, color="blue", linewidth=3)
plt.xticks(())
plt.yticks(())
plt.show()