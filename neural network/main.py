import random
import math


class Error(Exception):
    def __init__(self, str: str):
        self.str = str

    def __str__(self):
        return self.str


def sigmoid(x):
    return 1 / (1 + math.e ** x)


class Weight:
    def __init__(self, w):
        self.w = w

    def __repr__(self):
        return f"{round(self.w, 2)}"


class Neuron:
    def __init__(self, input_weights, output_weights):
        self.input = input_weights
        self.output = output_weights

    def __repr__(self):
        return f"Neuron(out:{self.output},\n\t    in:{self.input})"


class Layer:
    def __init__(self, size: int, f_activation=sigmoid, derivative_f=None):
        self.f_activation = f_activation
        self.derivative_f = derivative_f
        self.neurons = [Neuron([], []) for _ in range(size)]

    def __repr__(self):
        _str = "[\n"
        for neuron in self.neurons:
            _str += "\t\t" + str(neuron) + ";\n"
        _str += "\t],\n"
        return _str


class Network:
    def __init__(self, layers: [Layer]):
        for i in range(len(layers)):
            if i != len(layers) - 1:
                next_layer = layers[i + 1]
                now_layer = layers[i]
                for _neuron in now_layer.neurons:
                    weights = [Weight(random.uniform(-1, 1)) for _ in range(len(next_layer.neurons))]
                    _neuron.output = weights
                    for i in range(len(next_layer.neurons)):
                        next_layer.neurons[i].input.append(weights[i])

        self.layers = layers

    def __call__(self, _input: [], more_information=False):
        if len(_input) != len(self.layers[0].neurons):
            raise Error(f"Error, you give {len(_input)} items, but we need only {len(self.layers[0].neurons)}")
        prefab_1 = []  # до функции активации
        prefab_2 = [_input]  # после функции активации
        for i in range(len(self.layers)):
            if i != len(self.layers) - 1:
                prefab_1.append([0 for _ in range(len(self.layers[i + 1].neurons))])
                for z in range(len(self.layers[i].neurons)):
                    neuron = self.layers[i].neurons[z]
                    for j in range(len(neuron.output)):
                        prefab_1[-1][j] += prefab_2[-1][i] * neuron.output[j].w

                prefab_2.append([])
                for number in prefab_1[-1]:
                    prefab_2[-1].append(self.layers[i].f_activation(number))
        if more_information:
            return prefab_1, prefab_2
        else:
            return prefab_2[-1]

    def __repr__(self):
        _str = "[\n"
        for _layer in self.layers:
            _str += "\t" + str(_layer)
        _str += "]"
        return _str


network = Network([
    Layer(2),
    Layer(2)
])
print(network)
print(network([1,12]))

