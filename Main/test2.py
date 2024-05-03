
'''
b1 = Beam(Input(400,200,6,'C20','R','XC2',3,16,20,True,False))
b2 = Beam(Input(500,250,7,'C20','N','XC1',4,12,24,True,False))
b3 = Beam(Input(600,400,10,'C20','S','XC3',5,20,28,False,False))
b4 = Beam(Input(700,300,13,'C30','R','XS1',6,25,32,True,True))
b5 = Beam(Input(1000,650,11,'C30','N','XC4',7,16,26,True,False))
b6 = Beam(Input(650,350,8,'C35','R','XC3',8,12,30,False,False))
b7 = Beam(Input(800,450,5,'C35','N','XD2',4,10,22,True,True))
b8 = Beam(Input(900,500,9,'C35','S','XS2',6,20,34,True,False))
b9 = Beam(Input(950,600,12,'C40','R','XD1',5,16,18,False,False))
b10 = Beam(Input(750,550,14,'C40','S','X0',7,25,36,True,False))



b11 = Beam(Input(600,250,7,'C20','R','XD3',4,16,26))
b12 = Beam(Input(700,300,7.5,'C20','N','XC1',4,12,28))
b13 = Beam(Input(800,200,8,'C20','S','X0',5,20,28))
b14 = Beam(Input(900,300,6,'C30','R','XS2',8,25,32))
b15 = Beam(Input(650,250,9,'C30','N','XC4',4,16,30))
b16 = Beam(Input(950,300,8.5,'C35','R','XC1',6,12,24))
b17 = Beam(Input(850,400,9.5,'C35','N','XD1',6,10,22))
b18 = Beam(Input(700,200,10,'C35','S','XS2',8,20,20))
b19 = Beam(Input(900,350,8.5,'C40','R','XD2',7,16,36))
b110 = Beam(Input(1000,250,11,'C40','S','XC3',6,25,34))

b111 = Beam(Input(500,300,8,'C20','N','XD1',6,20,28))
b112 = Beam(Input(600,200,9.5,'C20','S','X0',5,16,24))
b113 = Beam(Input(700,350,7,'C20','S','XD2',5,25,30))
b114 = Beam(Input(1000,200,8,'C30','N','XS1',6,20,22))
b115 = Beam(Input(550,350,8.5,'C30','S','XC2',7,12,26))
b116 = Beam(Input(750,200,9.5,'C35','R','XC3',6,16,28))
b117 = Beam(Input(950,200,7.5,'C35','S','XD3',5,12,28))
b118 = Beam(Input(900,300,11,'C35','N','XS3',8,10,30))
b119 = Beam(Input(800,350,10.5,'C40','R','XD1',6,16,32))
b1110 = Beam(Input(900,450,9,'C40','N','X0',7,20,34))


#x = [b1.total_emission,b2.total_emission,b3.total_emission,b4.total_emission,b5.total_emission,b6.total_emission,b7.total_emission,b8.total_emission,b9.total_emission,b10.total_emission,b11.total_emission,b12.total_emission,b13.total_emission,b14.total_emission,b15.total_emission,b16.total_emission,b17.total_emission,b18.total_emission,b19.total_emission,b110.total_emission,b111.total_emission,b112.total_emission,b113.total_emission,b114.total_emission,b115.total_emission,b116.total_emission,b117.total_emission,b118.total_emission,b119.total_emission,b1110.total_emission]
#y = [b1.total_cost,b2.total_cost,b3.total_cost,b4.total_cost,b5.total_cost,b6.total_cost,b7.total_cost,b8.total_cost,b9.total_cost,b10.total_cost,b11.total_cost,b12.total_cost,b13.total_cost,b14.total_cost,b15.total_cost,b16.total_cost,b17.total_cost,b18.total_cost,b19.total_cost,b110.total_cost,b111.total_cost,b112.total_cost,b113.total_cost,b114.total_cost,b115.total_cost,b116.total_cost,b117.total_cost,b118.total_cost,b119.total_cost,b1110.total_cost]





#print(x_2)
#print(beam_12.ULS_instance.alpha,beam_13.ULS_instance.alpha,beam_14.ULS_instance.alpha,beam_15.ULS_instance.alpha,beam_16.ULS_instance.alpha)
#print(beam_22.ULS_instance.alpha,beam_23.ULS_instance.alpha,beam_24.ULS_instance.alpha,beam_25.ULS_instance.alpha,beam_26.ULS_instance.alpha)
#print(beam_12.ULS_instance.M_Rd,beam_13.ULS_instance.M_Rd,beam_14.ULS_instance.M_Rd,beam_15.ULS_instance.M_Rd,beam_16.ULS_instance.M_Rd)
#print(beam_22.ULS_instance.M_Rd,beam_23.ULS_instance.M_Rd,beam_24.ULS_instance.M_Rd,beam_25.ULS_instance.M_Rd,beam_26.ULS_instance.M_Rd)

# Create scatter plot
plt.figure(figsize=(10, 6))
plt.scatter(x,y, color='blue',marker = 'o',label= 'Case 1: Ordinary reinforcement')  # Plot points
#plt.plot(x_4,y_4, color='orange',marker = 'o',label= 'C40')  # Plot points

#for i in range(len(diameter)):
#   plt.annotate(f'{diameter[i]}', (x_4[i], y_4[i]), textcoords="offset points", xytext=(5,5), ha='right')
#for i in range(len(concrete)):
#   plt.annotate(f'{concrete[i]}', (x_2[i], y_2[i]), textcoords="offset points", xytext=(5,5), ha='right')
#plt.plot(x_3,y_3, color='red', marker='o',label = 'Case 3: Ordinary reinforced in top and prestressed in bottom')  # Plot points
#for i in range(len(concrete)):
   #plt.annotate(f'{concrete[i]}', (x_3[i], y_3[i]), textcoords="offset points", xytext=(5,5), ha='right')
plt.title('Cost vs. Emissions')
plt.xlabel('Cost [NOK]')
plt.ylabel('Emissions [kg C02 eq.]')
plt.legend()
plt.grid(True)
plt.show()
'''
