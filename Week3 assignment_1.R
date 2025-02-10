library(geosphere)
library(readxl)

# Read dataset
df <- read_excel("clinics.xls")

# Convert latitude & longitude to numeric
df$locLat <- as.numeric(df$locLat)
df$locLong <- as.numeric(df$locLong)

# Clean data: Remove NA and filter valid lat/lon ranges
df <- df[!is.na(df$locLat) & !is.na(df$locLong), ]
df <- df[df$locLat >= -90 & df$locLat <= 90, ]   
df <- df[df$locLong >= -180 & df$locLong <= 180, ]

# Define Haversine function (returns distance in miles)
haversine <- function(lat1, lon1, lat2, lon2) {
  distHaversine(c(lon1, lat1), c(lon2, lat2)) / 1609.34
}

# Approach 1: For-loop
start <- Sys.time()
distances <- numeric(nrow(df))
for (i in 1:nrow(df)) {
  distances[i] <- haversine(40.671, -73.985, df$locLat[i], df$locLong[i])
}
df$distance <- distances
time_for_loop <- Sys.time() - start
print(paste("For-loop time:", time_for_loop))

# Approach 2: Apply function
start <- Sys.time()
df$distance <- apply(df, 1, function(row) {
  haversine(40.671, -73.985, as.numeric(row["locLat"]), as.numeric(row["locLong"]))
})
time_apply <- Sys.time() - start
print(paste("Apply function time:", time_apply))

# Approach 3: Vectorized Calculation (Fastest)
start <- Sys.time()
df$distance <- distHaversine(cbind(df$locLong, df$locLat), c(-73.985, 40.671)) / 1609.34
time_vectorized <- Sys.time() - start
print(paste("Vectorized method time:", time_vectorized))


summary(df$distance)

# Print execution times in a table
times <- data.frame(
  Method = c("For-loop", "Apply function", "Vectorized method"),
  ExecutionTime = c(time_for_loop, time_apply, time_vectorized)
)
print(times)