# Redes neuronales artificiales - Trabajo práctico 1

Implementación de modelos de _perceptrón simple_ y _perceptrón multicapa_.

## Ejercicio 1

Problema de clasificación: predecir el diagnóstico final de cáncer de mamas.

Dataset: resultados de un examen especifico que es utilizado en el diagnostico de
cáncer de mamas.

Cada entrada correspondiente a los datos obtenidos para distintos pacientes y
contiene 10 características provenientes de imágenes digitalizadas de muestras de
células, y el diagnostico final en donde se indica si la muestra analizada
pertenecía a un tumor maligno o benigno.

La estimación con el modelo ya entrenado se ejecuta con

```
python ej1.py models/model_ej1 DATASET
```

## Ejercicio 2

Problema de regresión: predecir los valores de carga energética para la calefacción y
refrigeración de edificios.

Dataset: análisis energético de edificios de distintas formas que difieren con
respecto a la superficie y distribución de las áreas de reflejo, la orientación y
otros parámetros.

Cada entrada en el conjunto de datos corresponde a las características de un edificio
distinto junto a dos valores reales que representan la cantidad de energía necesaria
para realizar una calefacción y refrigeración adecuadas.

La estimación con el modelo ya entrenado se ejecuta con

```
python ej2.py models/model_ej2 DATASET
```


## Correr

```
python ej1.py MODELO DATASET
```

o

```
python ej2.py MODELO DATASET
```

Para entrenar usar:

- `MODELO` path donde se guarda el modelo. Este archivo no debe existir.
- `DATASET` path al dataset de entrenamiento

Para testar usar:

- `MODELO` path al modelo entrenado. Este archivo debe existir.
- `DATASET` path al dataset de testing

## Setup

Python: v3.6.5

Para instalar version de Python

1. Instalar `pyenv` - https://github.com/pyenv/pyenv#installation

  En mac:

  ```
  brew update
  brew install pyenv
  ```

2. Instalar v3.6.5

  ```
  pyenv install 3.6.5
  ```

3. Activar v3.6.5 en terminal

  ```
  eval "$(pyenv init -)"
  pyenv global 3.6.5
  ```

4. Verificar version

  ```
  python --version
  > Python 3.6.5
  ```

5. Instalar dependencias

  ```
  pip install -r requirements.txt
  ```

## Experimentación

1. Abrir `jupyter`

  ```
  jupyter lab
  ```

2. Abrir archivo `exp_ej1.ipynb` o `exp_ej2.ipynb`

> Otros notebooks también tienen experimentaciones.

La clase `Model` se puede usar para experimentar y no recargar los datos.
