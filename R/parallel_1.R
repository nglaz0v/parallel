# Load the parallel package
library(parallel)

# Define a function to compute the square of a number
square_function <- function(x) {
  return(x^2)
}

# Create a vector of numbers
numbers <- 1:10

# Use mclapply to compute squares in parallel
# Note: On Windows, use parLapply instead of mclapply
squared_numbers <- mclapply(numbers, square_function, mc.cores = detectCores() - 1)

# Print the results
print(squared_numbers)
