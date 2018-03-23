import numpy as np

# Load the stats
stats = np.loadtxt("stats.txt")

# Calculate the variance of the Laplacians and the ERRs
lap_var = np.var(stats[:,0])
err_var = np.var(stats[:,1])

# Calculate the means
lap_mean = np.mean(stats[:,0])
err_mean = np.mean(stats[:,0])

# Calculate the standard deviations from the variances
lap_sd = np.sqrt(lap_var)
err_sd = np.sqrt(err_var)