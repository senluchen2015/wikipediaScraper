f = open("vocabList.txt", "r");
s = open("superherolist.txt", "r");

super_hero_list = s.readlines()

i = 0
for hero in super_hero_list:
	hero = hero[0:]
	if(' ' in hero):
		hero = hero.split(' ')
		hero = hero[0]
	else:
		hero = hero[:-1]
	super_hero_list[i] = hero
	i = i + 1

for line in f:
	line = line[2:] #remove front '
	line = line[:-3] #remove , and '
	if line in super_hero_list:
		print line

f.close()
s.close()
