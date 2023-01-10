import csv

import gpxpy
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

sns.set_theme(style="whitegrid", palette="bright")

def load_data(data_file):
    # if file type is csv, check if cell A1 starts with "COXORB Performance Data", and if so run load_coxorb_csv()
    if data_file.endswith(".csv"):
        with open(data_file, newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=',', quotechar='"')
            for row in reader:
                if row[0].startswith("COXORB Performance Data"):
                    print("Loading COXORB Performance Data File")
                    _data = pd.read_csv(data_file, skiprows=3)
                    # set columns to columns=["Distance", "Elapsed Time", "Stroke Count", "Rate", "Check", "Speed (mm:ss/500m)", "Speed (m/s)", "Distance/Stroke"]
                    _data.columns = ["Distance", "Elapsed Time", "Stroke Count", "Rate", "Check", "Speed (mm:ss/500m)", "Speed (m/s)", "Distance/Stroke"]
                    return _data
                else:
                    print("Not a COXORB Performance Data file")
                    break
    elif data_file.endswith(".gpx"):
        # load gpx file
        _data = gpx_file = open(data_file, 'r')
        return _data


def cox_orb_analysis(data_input):
    # calculate the moving average of the rate, and "Speed (m/s)"
    data_input["Rate Moving Average"] = data_input["Rate"].rolling(window=10).mean()
    data_input["Speed (m/s) Moving Average"] = data_input["Speed (m/s)"].rolling(window=10).mean()

    # "Time" to be time in sec, from "Elapsed Time" which is in h:mm:ss.tt format
    data_input["Time"] = data_input["Elapsed Time"].str.split(":").apply(lambda x: int(x[0]) * 3600 + int(x[1]) * 60 + float(x[2]))
    return data_input

def cox_orb_graph(data_input):

    
    # "speed-time-rate"
    # plot the "Speed (m/s)" vs "Time" graph, with colour being rate, with a moving average line onto subplot, using colour theme crest
    sns.scatterplot(x="Time", y="Speed (m/s)", hue="Rate", data=data_input)
    sns.lineplot(x="Time", y="Speed (m/s) Moving Average", data=data_input)
    # show only 10 values on x axis using sns.despine()
    
    # x and y axis labels, set the x axis to be in mins
    plt.xlabel("Elapsed Time (mins)")
    plt.ylabel("Speed (m/s)")
    plt.title("Speed of Boat over time, with Rate value as Hue")
    # save plot as png under ./output folder
    plt.savefig("./output/speed-rate-time.png")

    plt.clf()

    # plot rate vs check
    # set the Hue to be chunks of 120 seconds
    sns.scatterplot(x="Rate", y="Check", hue="Time", data=data_input)
    plt.xlabel("Rate")
    plt.ylabel("Check")
    plt.title("Rate vs Check")
    plt.savefig("./output/rate-check.png")

    plt.clf()

    # plot speed vs check
    # set the Hue to be chunks of 120 seconds
    sns.scatterplot(x="Speed (m/s)", y="Check", hue="Time", data=data_input)
    plt.xlabel("Speed (m/s)")
    plt.ylabel("Check")
    plt.title("Speed vs Check")
    plt.savefig("./output/speed-check.png")

    plt.clf()

    # plot distance per stroke vs check
    # set the Hue to be chunks of 120 seconds

    sns.scatterplot(x="Distance/Stroke", y="Check", hue="Time", data=data_input)
    plt.xlabel("Distance/Stroke")
    plt.ylabel("Check")
    plt.title("Distance per Stroke vs Check")
    plt.savefig("./output/distance-stroke-check.png")

    plt.clf()

    # plot distance per stroke through time with check as hue

    sns.scatterplot(x="Time", y="Distance/Stroke", hue="Check", data=data_input)
    plt.xlabel("Elapsed Time (mins)")
    plt.ylabel("Distance/Stroke")
    plt.title("Distance per Stroke through time, with Check as Hue")
    plt.savefig("./output/distance-stroke-time.png")

    plt.clf()


    # distance per stroke vs rate

    sns.scatterplot(x="Distance/Stroke", y="Rate", hue="Time", data=data_input)
    plt.xlabel("Distance/Stroke")
    plt.ylabel("Rate")
    plt.title("Distance per Stroke vs Rate")
    plt.savefig("./output/distance-stroke-rate.png")

    plt.clf()
    

if __name__ == "__main__":
    print("Rowing Analysis")
    print("--------------")
    cox_orb = load_data("GRAPH_10.csv")
    cox_orb = cox_orb_analysis(cox_orb)
    cox_orb_graph(cox_orb)