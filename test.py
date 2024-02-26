h_0 = 150
h_0_vector = [100,200,300,500]
k_h_vector = [1,0.85,0.75,0.7]
for i in range(len(h_0_vector)-1):
    if h_0_vector[i+1] >= h_0 >= h_0_vector[i]:
        k_h = (k_h_vector[i+1] - k_h_vector[i]) / (h_0_vector[i+1] - h_0_vector[i]) * (h_0 - h_0_vector[i]) + k_h_vector[i]


print(k_h)