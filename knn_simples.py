# Algoritmo de Aprendizagem dos Vizinhos Mais Próximos (K-NN)

# Importando Biliotecas Importantes
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# Importando algumas funções para este código
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
from matplotlib.colors import ListedColormap
from sklearn.metrics import confusion_matrix

# Importando a base de dados Social_Networks_Ads
dataset = pd.read_csv('social_networks_ads.csv')

# Definindo as colunas 2 e 3 como atributos descritivos
X = dataset.iloc[:, [2, 3]].values
# Definindo a coluna 4 como atributo Classe (Preditivo)
y = dataset.iloc[:, 4].values

# Separando o conjunto de dados em conjunto de treinamento e deteste
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.25, random_state = 0)

# Normalizando os dados
sc = StandardScaler()
X_train = sc.fit_transform(X_train)
X_test = sc.transform(X_test)

# Gerando o Classificador com os dados de treinamento

classifier = KNeighborsClassifier(n_neighbors = 21)
classifier.fit(X_train, y_train)

# Realizando a Predição das Classes dos dados do conjunto de teste 
y_pred = classifier.predict(X_test)

# Gerando a Matriz de Confusão com os dados de teste
cm = confusion_matrix(y_test, y_pred)

# Vizualização dos Resultados sobre o Conjunto de Treinamento
# Uso da biblioteca Matplotlib
X_set, y_set = X_train, y_train
X1, X2 = np.meshgrid(np.arange(start = X_set[:, 0].min() - 1, stop = X_set[:, 0].max() + 1, step = 0.01),
                     np.arange(start = X_set[:, 1].min() - 1, stop = X_set[:, 1].max() + 1, step = 0.01))
plt.contourf(X1, X2, classifier.predict(np.array([X1.ravel(), X2.ravel()]).T).reshape(X1.shape),
             alpha = 0.75, cmap = ListedColormap(('cyan', 'gray')))
plt.xlim(X1.min(), X1.max())
plt.ylim(X2.min(), X2.max())
for i, j in enumerate(np.unique(y_set)):
    plt.scatter(X_set[y_set == j, 0], X_set[y_set == j, 1],
                c = ListedColormap(('red', 'green'))(i), label = j)
plt.title('Classificador KNN (Dados Treinamento)')
plt.xlabel('Idade')
plt.ylabel('Salário')
plt.legend()
plt.show()