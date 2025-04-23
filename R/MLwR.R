## Measuring execution time ----

system.time(rnorm(1000000))

## Working in parallel ----

library(parallel)
detectCores()

# note: the following will only work on non-Windows systems (i.e., MacOSX or Unix/Linux)
# you will also need enough cores to complete each task!

# random number generation using multicore
# one core
system.time(l1 <- unlist(mclapply(1:10, function(x) {
  rnorm(1000000)}, mc.cores = 1)))

# two cores
system.time(l2 <- unlist(mclapply(1:10, function(x) {
  rnorm(1000000)}, mc.cores = 2)))

# four cores
system.time(l4 <- unlist(mclapply(1:10, function(x) {
  rnorm(1000000) }, mc.cores = 4)))

# eight cores
system.time(l8 <- unlist(mclapply(1:10, function(x) {
  rnorm(1000000) }, mc.cores = 8)))

# creating a 4-node cluster with snow
cl1 <- makeCluster(4)

# confirm that the cluster is functioning
clusterCall(cl1, function() { Sys.info()["nodename"] })

# running the same function on each node (not shown in book)
clusterCall(cl1, function() { print("ready!") })

# running a different operation on each node
clusterApply(cl1, c('A', 'B', 'C', 'D'),
             function(x) { paste("Cluster", x, "ready!") })

# close the cluster (IMPORTANT STEP!)
stopCluster(cl1)

## Parallel loops with foreach ----

library(foreach)

system.time(l1 <- rnorm(100000000))
system.time(l4 <- foreach(i = 1:4, .combine = 'c')
            %do% rnorm(25000000))

library(doParallel)
detectCores()
registerDoParallel(cores = 4)
system.time(l4p <- foreach(i = 1:4, .combine = 'c')
            %dopar% rnorm(25000000))

stopImplicitCluster()
