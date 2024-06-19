import pandas as pd
from datetime import datetime

df = pd.read_csv('monitoring_metrics_1.csv')

# Conversion timestamp en format datetime
df['timestamp'] = pd.to_datetime(df['timestamp'], unit='s')

#  YY-MM-DD HH:MM:SS
df['timestamp'] = df['timestamp'].dt.strftime('%y-%m-%d %H:%M:%S')

# enrigstrement d'un nouveau fichier CSV
df.to_csv('monitoring_metrics_1bis.csv', index=False)

