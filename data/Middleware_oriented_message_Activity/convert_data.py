import os
import pandas as pd
from datetime import datetime

path_file = os.path.dirname(os.path.realpath(__file__))

df = pd.read_csv(f'{path_file}/monitoring_metrics_1.csv')

# Conversion timestamp en format datetime
df['timestamp'] = pd.to_datetime(df['timestamp'], unit='s')

#  YYYY-MM-DD HH:MM:SS
df['timestamp'] = df['timestamp'].dt.strftime('%Y-%m-%d %H:%M:%S')

# enregistrement d'un nouveau fichier CSV
df.to_csv(f'{path_file}/monitoring_metrics_1bis.csv', index=False)

