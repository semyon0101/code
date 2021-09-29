import random
import math


class Error(Exception):
    def __init__(self, str: str):
        self.str = str

    def __str__(self):
        return self.str


def sigmoid(x):
    return 1 / (1 + math.e ** x)


def derivative_function(x):
    return sigmoid(x) * (1 - sigmoid(x))


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
    def __init__(self, size: int, f_activation=sigmoid, derivative_f=derivative_function):
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

    def train(self, _input: [], _output: [], n=0.1):
        if len(_input) != len(self.layers[0].neurons):
            raise Error(
                f"Error in input, you give {len(_input)} items, but we need only {len(self.layers[0].neurons)}")
        if len(_output) != len(self.layers[-1].neurons):
            raise Error(
                f"Error in output, you give {len(_output)} items, but we need only {len(self.layers[-1].neurons)}")

        prefab_1, prefab_2 = self(_input, True)
        local_g_arr = []
        for i in range(len(self.layers)):
            i = len(self.layers) - 1 - i
            if i == 0:
                break
            layer = self.layers[i]
            local_g_arr_copy = local_g_arr.copy()
            local_g_arr = []
            for j in range(len(layer.neurons)):
                if i == len(self.layers) - 1:
                    local_g = (prefab_2[i-1][j] - _output[j]) * layer.derivative_f(prefab_1[i-1][j])
                    for w in range(len(layer.neurons[j].input)):
                        layer.neurons[j].input[w].w -= n * local_g * _input[w]
                else:
                    q = sum([layer.neurons[j].output[z].w * local_g_arr_copy[z] for z in range(len(local_g_arr_copy))])
                    local_g = q * layer.derivative_f(prefab_1[i-1][j])
                    for w in range(len(layer.neurons[j].input)):
                        layer.neurons[j].input[w].w -= n * local_g * prefab_2[i - 2][w]
                local_g_arr.append(local_g)

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
                        prefab_1[-1][j] += prefab_2[-1][z] * neuron.output[j].w

                prefab_2.append([])
                for number in prefab_1[-1]:
                    prefab_2[-1].append(self.layers[i].f_activation(number))
        if more_information:
            return prefab_1, prefab_2[1:]
        else:
            return prefab_2[-1]

    def __repr__(self):
        _str = "[\n"
        for _layer in self.layers:
            _str += "\t" + str(_layer)
        _str += "]"
        return _str


network = Network([
    Layer(3),
    Layer(1)
])
print(network)
print(network([1, 0, 0]))
_input = [
    [0, 1, 1],
    [1, 0, 0],
    [0, 0, 0],
    [1, 0, 1],
    [1, 1, 0]
]
_output = [
    [0],
    [1],
    [0],
    [1],
    [1]
]
for _ in range(5):
    n = random.randint(0, len(_output) - 1)
    network.train(_input[2], _output[2], 0.1)
    print(_)
print(network)
print(network([1, 0, 0]))
