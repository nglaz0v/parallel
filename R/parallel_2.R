# If you are using Windows, mclapply may not work as expected because it
# relies on forking, which is not supported on Windows. Instead, you can
# use parLapply with a cluster setup:

# Load the parallel package
library(parallel)

# Define a function to compute the square of a number
square_function <- function(x) {
  return(x^2)
}

# Create a vector of numbers
numbers <- 1:10

# Create a cluster
cl <- makeCluster(detectCores() - 1)

# Use parLapply to compute squares in parallel
squared_numbers <- parLapply(cl, numbers, square_function)

# Stop the cluster
stopCluster(cl)

# Print the results
print(squared_numbers)
