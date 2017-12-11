# -*- encoding: utf-8 -*-

from math import *
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class Model():
    def __init__(self, input_size, hidden_size, output_size,  learning_rate):

        self.input_size = input_size
        self.hidden_size = hidden_size
        self.output_size = output_size
        self.learing_rate = learning_rate

        self.delta_weight1 = []
        self.delta_weight2 = []
        self.weight1 = []
        self.weight2 = []

        for i in range(1000):
            self.delta_weight1.append([0]*1000)
            self.delta_weight2.append([0]*1000)
            self.weight1.append([0.5]*1000)
            self.weight2.append([0.5]*1000)

        self.hidden_output = [0]*1000
        self.final_output = [0]*1000

    def sigmoid(self, value, deriv = False):
        if deriv == True:
            return (1-value)*value
        return value/(value+exp(-value))

    def mat_mul(self, oper1, oper2, size1, size2, total_result, in_hid):
        result = 0
        if in_hid == True:
            for i in range(size1):
                result = 0
                for j in range(size2):
                    if j == 1:
                        result += 1*oper2[oper1[j]][i]
                    elif j == 2:
                        result += 1 * oper2[oper1[j] + 1][i]
                    else:
                        result += oper1[j] * oper2[j][i]
            total_result[i] = self.sigmoid(result, False)
            return

        for i in range(size2):
            result = 0
            for j in range(size1):
                result += oper1[j]*oper2[j][i]
            total_result[i] = self.sigmoid(result, False)

    def forward(self, input_data):
        self.mat_mul(input_data, self.weight1, self.input_size, self.hidden_size, self.hidden_output, 1)
        self.mat_mul(self.hidden_output, self.weight2, self.hidden_size, self.output_size, self.final_output, 0)

    def back_propagation(self, output_data):

        for i in range(self.output_size):
            delta = output_data[i] - self.final_output[i]
            self.delta_weight2 = delta*self.sigmoid(self.final_output[i], True)

        for i in range(self.hidden_size):
            delta = 0
            for j in range(self.output_size):
                delta += self.delta_weight2[j] * self.weight2[i][j]
            self.delta_weight1[i] = delta * self.sigmoid(self.hidden_output[i], True)

    def training(self, input_data):

        for i in range(self.hidden_size):
            for j in range(self.output_size):
                change = self.delta_weight2[j] * self.hidden_output[i]
                self.weight2[i][j] = self.learing_rate * change

        for i in range(self.input_size):
            for j in range(self.hidden_size):
                if i == 1:
                    change = self.delta_weight1[j] * 1
                    self.weight1[input_data[i]][j] = self.learing_rate * change
                elif i == 2:
                    change = self.delta_weight1[j] * 1
                    self.weight1[input_data[i]+1][j] = self.learing_rate * change
                else:
                    change = self.delta_weight1[j] * input_data[i]
                    self.weight1[i][j] = self.learing_rate * change

    def test(self, test_input, result):
        self.mat_mul(test_input, self.weight1, self.hidden_output, 1)
        self.mat_mul(self.hidden_output, self.weight2, result, 0)

def preprocessing(data):
    result = []
    for line in data:
        result.append(map(int, line.strip(' ').split(' ')))
    return result

if __name__ == '__main__':
    training_num = 1000

    with open("./training_set(input).csv", 'r') as f:
        training_input = f.read()
    with open("./training_set(output).csv", 'r') as f:
        training_output = f.read()

    training_input = preprocessing(training_input.strip('\n').split("\n"))
    training_output = preprocessing(training_output.strip('\n').split('\n'))

    model = Model(3, 3, 1, 0.1)

    for i in range(training_num):
        for idx in range(len(training_input)):
            model.forward(training_input[idx])
            model.back_propagation(training_output[idx])
            model.training(training_input[idx])

    for idx in range(len(training_input)):
        model.forward(training_input[idx])
        print training_input[idx], model.final_output[idx]
