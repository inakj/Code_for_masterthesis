

x1 = 32 * (0.3-0.39) / (0.3-0.4) + 25 * (0.39-0.4) / (0.3-0.4)
x2 = 20 * (0.3-0.39) / (0.3-0.4) + 16 * (0.39-0.4) / (0.3-0.4)
max_bar_diameter = x1 * (240-235.11) / (240-200) + x2 * (235.11-200) / (240-200)

print(max_bar_diameter)


def funskjon(w_max,sigma):
        Ø = ([[40, 32, 20, 16, 12, 10, 8, 6],[32, 25, 16, 12, 10, 8, 6, 5],[25, 16, 12, 8, 6, 5, 4, 0]])  #  Bar diameter matrix
        a = [160, 200, 240, 280, 320, 360, 400, 450]  #  Reinforcement tension vector
        w = [0.4, 0.3, 0.2]  #  Crack width vector
        
        for k in range(0,len(w)-1,1):
            if w[k] >= w_max > w[k+1]:
                for i in range(len(a) - 1):
                    x1 = Ø[k][i] * (w[k+1]-w_max)/(w[k+1]-w[k]) + Ø[k+1][i]* (w_max-w[k])/(w[k+1]-w[k]) 
                    x2 = Ø[k][i+1] * (w[k+1]-w_max)/(w[k+1]-w[k]) + Ø[k+1][i+1]* (w_max-w[k])/(w[k+1]-w[k]) 
                    if a[i] <= sigma < a[i + 1]:
                        max_bar_diameter = x1 * (a[i+1]-sigma) / (a[i+1]-a[i]) + x2 * (sigma-a[i]) / (a[i+1] - a[i])
        return max_bar_diameter


print(funskjon(0.22,323))