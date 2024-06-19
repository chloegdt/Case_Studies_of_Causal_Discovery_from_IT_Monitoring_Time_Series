import pandas as pd
from datetime import datetime

df = pd.read_csv('monitoring_metrics_2.csv')

# Conversion timestamp en format datetime
df['timestamp'] = pd.to_datetime(df['timestamp'], unit='s')

#  YY-MM-DD HH:MM:SS
df['timestamp_formatted'] = df['timestamp'].dt.strftime('%y-%m-%d %H:%M:%S')

# enrigstrement d'un nouveau fichier CSV
df.to_csv('monitoring_metrics_2bis.csv', index=False)

