import pandas as pd
import uuid, base64
from io import BytesIO
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Function for neeeded for platform

# File reading csv
def read_csv(file):

    data = pd.read_csv(file)

    df = pd.DataFrame(data)

    return df

# Reading colunm Datum from csv file
def data_from_csv(df):
    n={}

    for index, row in df.iterrows():
        n[(row[0])[0:10]] = float(row[1])

    return n

# Function for encoding and decoding matplotlib graph
def get_graph():
    buffer = BytesIO()
    plt.savefig(buffer, facecolor='#2d2d39', format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    graph = base64.b64encode(image_png)
    graph = graph.decode('utf-8')
    buffer.close()
    return graph

# Displayed chart
def get_chart(data_x, data_y, **kwargs):
    plt.switch_backend('AGG')
    plt.figure(figsize=(16, 12))
    ax = plt.axes()
    ax.set_facecolor('#3f4156')
    plt.plot(data_x, data_y, linewidth=3, color='#71c6dd')
    plt.title(str(*kwargs.values()), fontsize=20, fontweight='bold', color='white', pad=15)
    plt.xlabel('Date', fontsize=18, fontweight='bold', color='white', labelpad=15)
    plt.ylabel('Groundwater level [m.a.m.s.l.]', fontsize=18, fontweight='bold', color='white', labelpad=15)
    # Iterate trough everey 100th element because x-axis get full of dates
    plt.xticks([i for i in data_x[::80]], rotation=90, fontsize=14, color='white')
    plt.yticks(fontsize=16, color='white')
    plt.grid(linewidth=0.5)
    plt.tight_layout()
    chart = get_graph()

    return chart

# Modifying chart for selected range (from page). x1->start date x->end date n-dictionary
def chart_range(x1, x2, data):
    
    n={}
    for key, value in list(data.items())[x1:x2+1]:
        n[key] = float(value)

    return n
