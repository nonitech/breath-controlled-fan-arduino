import csv

def save_data(breath_data, motor_data):
    with open("data.csv", "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Breath", "Motor"])

        for i in range(len(breath_data)):
            writer.writerow([breath_data[i], motor_data[i]])

    print("Data saved successfully")
