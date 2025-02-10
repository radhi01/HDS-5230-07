import numpy as np
import pandas as pd
import time

# Read the dataset
df = pd.read_excel("C:/Users/91849/Desktop/Assignments/Week 3 HDS/clinics.xls")

# Define Haversine function
def haversine(lat1, lon1, lat2, lon2):
    MILES = 3959  # Earth's radius in miles
    lat1, lon1, lat2, lon2 = map(np.deg2rad, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1 
    dlon = lon2 - lon1 
    a = np.sin(dlat/2)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon/2)**2
    c = 2 * np.arcsin(np.sqrt(a)) 
    return MILES * c

# Define different approaches and time them
times = {}

# **Approach 1: For-loop**
start = time.time()
distances = []
for i in range(len(df)):
    distances.append(haversine(40.671, -73.985, df.iloc[i]['locLat'], df.iloc[i]['locLong']))
df['distance'] = distances
times["For-loop"] = time.time() - start

# **Approach 2: apply()**
start = time.time()
df['distance'] = df.apply(lambda row: haversine(40.671, -73.985, row['locLat'], row['locLong']), axis=1)
times["apply()"] = time.time() - start

# **Approach 3: Vectorized**
start = time.time()
df['distance'] = haversine(40.671, -73.985, df['locLat'], df['locLong'])
times["Vectorized (Pandas Series)"] = time.time() - start


# Print execution times
print(pd.DataFrame(times, index=["Execution Time (s)"]))