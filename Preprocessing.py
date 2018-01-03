import csv

time = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23]

input_data = ""
output_data = ""
test_input_data = ""
test_output_data = ""
with open('Setting.ini', 'r') as f:
    path = f.read().split('\n')[-1].split(': ')[-1]

with open(path + "train.csv", 'r') as f:
    data = csv.reader(f, delimiter = ',', quotechar = '\n')
    data = list(data)
    # for row, value in range(1, len(data[1:]), 2):
    for row, value in enumerate(data[1:]):
        if row%2 == 1:
            if value[0] != "2014-01-09":
                for idx in time:
                    if value[idx+4] == "":
                        value[idx+4] = 0
                    if data[row+1][idx+4] == "":
                        data[row+1][idx+4] = 0
                    if value[0] != '2014-01-08':
                        input_data += value[1][0] + " " + value[2].split("(")[-1].strip(")") + " " + str(idx) + "\n"
                        if int(value[idx+4]) + int(data[row+1][idx+4]) > 2000:
                            output_data += "1\n"
                        else:
                            output_data += "0\n"
                    else:
                        test_input_data += value[1][0] + " " + value[2].split("(")[-1].strip(")") + " " + str(idx) + "\n"
                        if int(value[idx + 4]) + int(data[row + 1][idx + 4]) > 2000:
                            test_output_data += "1\n"
                        else:
                            test_output_data += "0\n"
            else:
                break

with open(path + "training_set(input).csv", 'w') as f:
    f.write(input_data.strip('\n'))
with open(path + "training_set(output).csv", 'w') as f:
    f.write(output_data.strip('\n'))
with open(path + "test_set(input).csv", 'w') as f:
    f.write(test_input_data.strip('\n'))
with open(path + "test_set(output).csv", 'w') as f:
    f.write(test_output_data.strip('\n'))