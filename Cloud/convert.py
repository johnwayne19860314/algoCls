import os
import csv

def convert(input_file_path, output_file_path):

    output_data = []
    with open(input_file_path, "r") as data:
        for row in data:
            row = row.split(",")
            tmp_str = ""
            tmp_str += (row[0] + " " + row[1])
            tmp_str+=","
            lastname_email = row[2].split("0")
            tmp_str += lastname_email[0]
            tmp_str+=","
            email = lastname_email[len(lastname_email)-1]
            tmp_str += email 
            output_data.append(tmp_str)
    
    with open(output_file_path, "w") as file:
        output_str = ""
        for i in range(len(output_data)):
            output_str+=output_data[i]
        file.write(output_str)

if __name__ == "__main__":
    convert("input.csv", "output_1.csv")