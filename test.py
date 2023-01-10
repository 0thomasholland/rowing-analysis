from rowing_analysis import *

cox_orb = load_data("GRAPH_10.csv")
gpx = load_data("G_P_S_10.gpx")

# print first 5 rows of two files:

print("COXORB Performance Data")
print("-----------------------")
for i in range(5):
    print(next(cox_orb))
