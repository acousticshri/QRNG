import numpy as np

# Load your random number text file
data = np.loadtxt("C:/Users/Rajat/Desktop/Project/Python Project/data to test/Entangled_Photon.txt")

# Save as binary file
data.astype('uint32').tofile("C:/Users/Rajat/Desktop/Project/Python Project/data to test/Entangled_Photon.bin")
