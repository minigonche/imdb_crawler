#Script for generating the SQL scripts of insertion into the movie ids (SQL stored procedure is failing)


#Million Loop
total = 10000000
num_files = 50
step = total/num_files

for i in range(1,num_files + 1):
	with open('insert' + str(i) + '.sql', 'w') as f:
		f.write("INSERT INTO movie_ids (id, stat) values\n")
		srat = False
		for index in range(step*(i-1), step*i):
			if(index == step*i -1):				
				f.write("(" + str(index) + ", 'UC');")
			else:	
			 	f.write("(" + str(index) + ", 'UC')," + '\n')

		print('Finished File: ' + str(i))	

print('OK')
