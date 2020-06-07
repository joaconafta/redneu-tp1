from dataset import load_dataset
from os import path
import numpy as np
import pickle
from plotter import plot_error

B = 1 # para cambiar buckets

# funciones de inicialización
def init_w(S):
  return [
    0 if i == 0 else
      np.random.normal(
      0, S[0]**(-1/2), (S[i-1]+1, S[i])
    )
    for i in range(len(S))
  ]

def init_dw(W):
  return [
    0 if i == 0 else
      np.zeros_like(W[i])
    for i in range(len(W))
  ]

def init_y(S):
  _Y = []
  L = len(S)

  _Y = [np.zeros((B, S[i]+1)) for i in range(L - 1)]

  _Y.append(np.zeros((B, S[L-1])))

  return _Y

# agregar y sacar umbrales
def bias_add(V):
  bias = -np.ones((len(V), 1))
  return np.concatenate((V, bias), axis=1)

def bias_sub(V):
  return V[:,:-1]

# funciones de entrenamiento

# activacion feed forward
def activation(S, Xh, W):
  Y = init_y(S)
  _Y = Xh

  L = len(S)

  for k in range(1, L):
    Y[k-1][:] = bias_add(_Y)
    _Y = np.tanh(np.dot(Y[k-1], W[k])) # función de activación g

  Y[L-1][:] = _Y

  return Y

# correccion backpropagation
def correction(S, Zh, W, Y, lr):
  L = len(S)

  dW = init_dw(W)
  D = init_y(S)
  E = Zh - Y[L-1]
  dY = 1 - np.square(Y[L-1]) # derivada de la función de activación
  D[L-1] = E*dY

  for k in range(L-1, 0, -1):
    dW[k] = lr * np.dot(Y[k-1].T, D[k])
    E = np.dot(D[k], W[k].T)
    dY = 1 - np.square(Y[k-1])
    D[k-1] = bias_sub(E*dY)

  return dW

def adaptation(W, dW):
  for k in range(1, len(W)):
    W[k] += dW[k]
  return W

def estimation(Zh, Y):
  return np.mean(np.sum(np.square(Zh-Y[-1]), axis=1))

def train(X, Z, S, max_epoch, lr):
  # inicialización de matriz de pesos
  W = init_w(S)

  errors = []
  error = 1
  t = 0

  while(error > 0.001 and t < max_epoch):
    # resultado parcial
    if t % 100 == 0:
      print('epoch {} - error {}/{}'.format(t, error, len(X)))

    error = 0

    # mini-lotes - mezcla de orden de instancias
    H = np.random.permutation(len(X))

    for h in H:
      # TODO: if h+B <= P: - para B > 1
      Y = activation(S, X[h:h + B], W)
      dW = correction(S, Z[h:h+B], W, Y, lr)
      W = adaptation(W, dW)
      error += estimation(Z[h:h+B], Y)

    t += 1
    errors.append(error)

  return errors, W

def test(X, Z, S, W):
  Y = [np.sign(activation(S, X[i:i+1], W)[-1][0]) for i in range(len(X))]
  return np.mean(np.where(Y == Z, 1, 0)) # promedio de aciertos

def main(
  argv, input_break, target_break, apply_target,
  S, max_epoch, lr
):
  if (len(argv) != 3):
    print('Error en la entrada')

  [_, model, data] = argv

  # lectura y pre procesamiento de datos
  (input, target) = load_dataset(
    data,
    input_break,
    target_break,
    apply_target
  )

  if (not path.exists(model + '.p')):
    # entrenamiento
    errors, W = train(input, target, S, max_epoch, lr)

    plot_error(errors)
    pickle.dump(errors, open(model + '_errors.p', 'wb'))
    pickle.dump(W, open(model + '.p', 'wb'))
  else:
    # testing

    # carga de modelo entrenado
    W = pickle.load(open(model + '.p', 'rb'))

    # testeo
    r = test(input, target, S, W)

    print('precisión: {}'.format(r))


class Model:
  def __init__(
    self,
    data,
    input_break,
    target_break,
    apply_target
  ):
    (_input, _target) = load_dataset(
      data,
      input_break,
      target_break,
      apply_target
    )

    self.input = _input
    self.target = _target

  def train(self, S, max_epoch, lr, train_break):
    self.S = S
    self.max_epoch = max_epoch
    self.lr = lr

    errors, W = train(
      self.input[train_break[0]:train_break[1]],
      self.target[train_break[0]:train_break[1]],
      self.S, self.max_epoch, self.lr
    )

    self.model = W
    return errors

  def test(self, test_break):
    return test(
      self.input[test_break[0]:test_break[1]],
      self.target[test_break[0]:test_break[1]],
      self.S, self.model
    )

  def exp(self, S, max_epoch, lr, train_break, test_break):
    errors = self.train(S, max_epoch, lr, train_break)
    pres = self.test(test_break)

    plot_error(errors)
    print(pres)
