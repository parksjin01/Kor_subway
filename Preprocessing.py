import csv

time = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23]

input_data = ""
output_data = ""

with open("/Users/Knight/Downloads/train.csv", 'r') as f:
    data = csv.reader(f, delimiter = ',', quotechar = '\n')
    data = list(data)
    for row in range(1, len(data[1:]), 2):
        if data[row][0] == "2014-01-01" or data[row][0] == "2014-01-02" or data[row][0] == "2014-01-03" or data[row][0] == "2014-01-04" or data[row][0] == "2014-01-05"\
                or data[row][0] == "2014-01-06" or data[row][0] == "2014-01-07":
            for idx in range(len(time)):
                input_data += data[row][1][0] + " " + data[row][2].split("(")[-1].strip(")") + " " +str(time[idx]) + "\n"
                if data[row][idx+4] == "":
                    data[row][idx+4] = 0
                if data[row+1][idx+4] == "":
                    data[row+1][idx+4] = 0
                if int(data[row][idx+4]) + int(data[row+1][idx+4]) > 2000:
                    output_data += "1\n"
                else:
                    output_data += "0\n"

with open("./training_set(input).csv", 'w') as f:
    f.write(input_data)
with open("./training_set(output).csv", 'w') as f:
    f.write(output_data)

input_data = ""
output_data = ""

with open("/Users/Knight/Downloads/train.csv", 'r') as f:
    data = csv.reader(f, delimiter = ',', quotechar = '\n')
    data = list(data)
    for row in range(1, len(data[1:]), 2):
        if data[row][0] == "2014-01-08":
            for idx in range(len(time)):
                input_data += data[row][1][0] + " " + data[row][2].split("(")[-1].strip(")") + " " +str(time[idx]) + "\n"
                if data[row][idx+4] == "":
                    data[row][idx+4] = 0
                if data[row+1][idx+4] == "":
                    data[row+1][idx+4] = 0
                if int(data[row][idx+4]) + int(data[row+1][idx+4]) > 2000:
                    output_data += "1\n"
                else:
                    output_data += "0\n"

with open("./test_set(input).csv", 'w') as f:
    f.write(input_data)
with open("./test_set(output).csv", 'w') as f:
    f.write(output_data)
