# Generate data
generate_data <- function(sz){
  set.seed(30) # Ensure reproducibility
  X1 <- rnorm(sz, mean = 120, sd = 23)
  X2 <- rgamma(sz, shape = 23, scale = 5)
  X3 <- rbinom(sz, size = floor(sz*.1), prob = .8) # Use floor for integer size
  X4 <- runif(sz, min = -2000, max = 30000)
  # Complex relationship including interaction and non-linearity
  Y <- 2.3*X1 + X2^1.4 + 50*log(X3 + 1) + 0.01*X4 + X3*(.04*X4) + rnorm(sz, mean = 100, sd = 23) # Slightly modified Y for more reasonable scale and interaction effects
  # Original Y: Y <- 2.3*X1 + X2^3.4 + X3 + X4 + X3*(.4*X4) + rnorm(sz, mean = 100, sd = 23) -> X2^3.4 can lead to huge numbers
  return(data.frame(X1, X2, X3, X4, Y))
}

# Generate and save 1k dataset
dfk1 <- generate_data(1000)
write.csv(dfk1, "data_1k.csv", row.names = FALSE)
print("Generated data_1k.csv")
summary(dfk1)

# Generate and save 10k dataset
dfk10 <- generate_data(10000)
write.csv(dfk10, "data_10k.csv", row.names = FALSE)
print("Generated data_10k.csv")
summary(dfk10)

# Generate and save 100k dataset
dfk100 <- generate_data(100000)
write.csv(dfk100, "data_100k.csv", row.names = FALSE)
print("Generated data_100k.csv")
summary(dfk100)
