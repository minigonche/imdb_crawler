#Script for generating the SQL scripts of insertion into the movie ids (SQL stored procedure is failing)

#Million Loop
for i in range(1,10):
	with open('insert' + str(i) + '.sql', 'w') as f:
		for index in range(1000000*(i-1), 1000000*i):
			f.write("INSERT INTO movie_ids (id, stat) values (" + str(index) + ", 'UC');" + '\n')

		print('Finished File: ' + str(i))	

print('OK')
