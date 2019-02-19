import sc2
from sc2 import run_game, maps, Race, Difficulty, Result
from sc2.player import Bot, Computer, Human
from sc2.constants import *
import random
from random import randint
import time

number_of_games = 15
DEBUG_SHOWGAME = False


def neural_network(obs):  #nn
	file = open("weights.txt","r")
	if(file.readline())!="kontrolni radek\n":
		print("Creating new weights")
		layers = [len(obs),16,8,6]                #<---------------------------------- NEURON NETWORK ------------------------------------------------

	# OUTCOMES(layers[3]):
	#neurons[3][x]:
	#0.	vytvořit workery
	#1.	expandovat zakladnu
	#2. vytvořit Mariny
	#3. vytvořit siege tanky
	#4. pokračovat v tech tree
	#5. ENGAGE


		neurons = []
		column = []
		file.close()
		for j in range(len(obs)):   #INPUT LAYER
			column.append(0)
		neurons.append(column)
		for i in range(len(layers)-2):      #HIDDEN LAYERS
			column = []
			for j in range(layers[i+1]):
				column.append(0)
			neurons.append(column)
		column = []         #OUTPUT LAYER
		for j in range(layers[3]):
			column.append(0)
		neurons.append(column)
		weights = []
		for i in range(len(layers)-1):
			column = []
			for j in range(len(neurons[i+1])):
				columnn = []
				for k in range(len(neurons[i])):
					x = random.uniform(-1,1)
					columnn.append(x)
				column.append(columnn)
			weights.append(column)
		return(layers,neurons,weights)



	else:
	    layers = [len(obs),16,8,6] 
	    neurons = []
	    column = []
	    for j in range(len(obs)):   #INPUT LAYER
	        column.append(0)
	    neurons.append(column)
	    for i in range(len(layers)-2):      #HIDDEN LAYERS
	        column = []
	        for j in range(layers[i+1]):
	            column.append(0)
	        neurons.append(column)
	    column = []         #OUTPUT LAYER
	    for j in range(layers[3]):
	        column.append(0)
	    neurons.append(column)
	    weights = []
	    for i in range(len(layers)-1):
	        column = []
	        for j in range(len(neurons[i+1])):
	            columnn = []
	            for k in range(len(neurons[i])):
	            	x=file.readline()
	            	columnn.append(float(x))
	            column.append(columnn)
	        weights.append(column)
	    file.close()
	    return(layers,neurons,weights)

def nn_mutation(nnl,nnn,nnw):   #MUTATION OF NEURAL NETWORK
		for l in range(len(nnl)-1):
			l+=1
			#print(l)
			for n in range(len(nnn[l])):
				for w in range(len(nnw[l-1][n])):
					a = randint(0,20)
					if(a==3 or a==4):
						nnw[l-1][n][w] += random.uniform(-0.2,0.2)
					elif(a==5):
						nnw[l-1][n][w] = random.uniform(-1,1)
		return nnw

def save_nn(nnl,nnn,nnw):
	f = open("weights.txt","w")
	f.write("kontrolni radek\n")
	for i in range(len(nnl)-1):
			for j in range(len(nnn[i+1])):
				for k in range(len(nnn[i])):
					f.write(str(nnw[i][j][k])+"\n")
	f.close()

def save_nn_special(wins,diffic):
	new_file = "weights_folder\\" + diffic + "\\" + str(wins) + "-" + diffic + "-" + str(int(time.time())) + ".txt"
	f_target = open(new_file ,"w")
	f_source = open("weights.txt","r")
	f_target.write(f_source.read())
	f_target.close()
	f_source.close()

def change_diff(diffic,change):
	if(change==1):
		if(diffic=="Easy"):
			return "Medium"
		if(diffic=="Medium"):
			return "Hard"
		if(diffic=="Hard"):
			return "VeryHard"
		if(diffic=="VeryHard"):
			return "GG"
	else:
		if(diffic=="Easy"):
			return "Easy"
		if(diffic=="Medium"):
			return "Easy"
		if(diffic=="Hard"):
			return "Medium"
		if(diffic=="VeryHard"):
			return "Hard"

def max_counter(diffic):
	if(diffic=="Easy"):
		return 10
	if(diffic=="Medium"):
		return 25
	if(diffic=="Hard"):
		return 75
	if(diffic=="VeryHard"):
		return 1000

def nn_output(nn_l,nn_n,nn_w,obs):  #OUTPUT NEURAL NETWORK
		for i in range(len(obs)):
			nn_n[0][i]=obs[i]
		for l in range(len(nn_l)):
			if(l==0):
				l=1
			for n in range(len(nn_n[l])):
				nn_n[l][n]=0
				for w in range(len(nn_w[l-1][n])):
					nn_n[l][n] += nn_n[l-1][w]*nn_w[l-1][n][w]
		#print(nn_n[len(nn_l)-1])
		#return int(random.uniform(0,6))
		return nn_n[len(nn_l)-1].index(max(nn_n[len(nn_l)-1]))

#----------------------------TERRAN------------------------


class SrBoTerran(sc2.BotAI):
	def __init__(self,mutate):
		self.ITERATION_PER_MINUTE = 165 					#165 ticku za minutu. ASI
		inputy = [1,2,3,4,5,6,7,8,9]               		    #delka arraye s inputama
		self.nnl,self.nnn,self.nnw=neural_network(inputy)   #volam vytvoreni NN				
		if(mutate==1):                                                     #Z mainu volam s mutací nebo bez
			print("mutuju")
			x = nn_mutation(self.nnl,self.nnn,self.nnw)   #<-------------- ZMENIT PODLE INPUTU!!!!!
			print("mutace dokoncena")
		print("inic")
		self.debugorder=-1

	def on_end(self, game_result):
		if(self.iteration/self.ITERATION_PER_MINUTE>90):            #!! pokud bude hra trvat více jak 90 minut tak bot do svého learningu píše že prohrál nezáležíc na výsledku
			game_result=Result.Defeat


		with open("score.txt","a") as f:
			f.write("{}".format(game_result))
			if(self.iteration/self.ITERATION_PER_MINUTE>90):
				f.write(".Time")
			f.write("\n")
		a = open("time.txt","r")
		games = int(a.readline())
		time = int(a.readline())
		a.close()
		b = open("time.txt","w")
		b.write(str(games+1)+"\n")
		b.write(str(time+int(self.iteration/self.ITERATION_PER_MINUTE*60))+"\n")
		print(game_result)
		if(game_result==Result.Victory):
			save_nn(self.nnl,self.nnn,self.nnw)
			print("vyhra")
		else:
			print("prohra")
		b.close()

	def select_target(self):
		#if(self.known_enemy_units(CHANGELINGMARINE).exists):

			#print("JJJJJJJJJJJAJAJ")
		target = (self.known_enemy_units-self.known_enemy_units(CHANGELINGMARINE)) #- self.known_enemy_units.name(CHANGELINGMARINE)
		#print(target)
		if target.exists:
			return target.random.position


		target = self.known_enemy_structures
		if target.exists:
			return target.random.position



		if min([u.position.distance_to(self.enemy_start_locations[0]) for u in self.units]) < 5:
			return self.enemy_start_locations[0].position

		return self.state.mineral_field.random.position


	async def on_step(self, iteration):
		self.iteration=iteration
		

		#pokrok calculator
		pokrok = 0
		if(self.units(BARRACKS).exists):
			pokrok+=1
			if(self.units(FACTORY).exists):
				pokrok+=1
				if(self.units(FACTORYTECHLAB).exists):
					pokrok+=1
					if(self.units(STARPORT).exists):
						pokrok+=1
						if(self.units(FUSIONCORE).exists):
							pokrok+=1
							if(self.units(STARPORTTECHLAB).exists):
								pokrok+=1
							
		#inputy: 0=čas(minuty),1=minerály(po 100),2= vespene(po 50),3= pokrok, 4+ jendotky
		inputs = [self.iteration/self.ITERATION_PER_MINUTE,self.minerals/100,self.vespene/50,pokrok,len(self.units(SCV)),len(self.units(MARINE)),len(self.units(SIEGETANK))+len(self.units(SIEGETANKSIEGED)),len(self.units(BATTLECRUISER)),len(self.units(COMMANDCENTER))]
		order = nn_output(self.nnl,self.nnn,self.nnw,inputs)
		if(order!=self.debugorder):
			print(order)
			self.debugorder=order
		#print(inputs)
		# OUTCOMES(layers[3]):
			#neurons[3][x]:
			#0.	vytvořit workery
			#1.	expandovat zakladnu
			#2. vytvořit Mariny
			#3. vytvořit siege tanky
			#4. pokračovat v tech tree
			#5. ENGAGE
		await self.create_vespine_collector()
		await self.army_management()
		await self.distribute_workers()
		await self.build_supply()
		if(order==0):
			await self.create_scv()
		elif(order==1):
			await self.create_new_commandcenter()
		
		elif(order==2):
			await self.build_barracks()
			await self.create_marine()
		elif(order==3):
			await self.create_siege()
		elif(order==4):
			await self.build_barracks()
			await self.rush_battlecruisers()
		elif(order==5):
			await self.ENGAGE()
		#await self.create_army_beta()
		
		
		
		
		





	async def build_supply(self):        #automaticke supply depoty
		if self.supply_left < 8 and self.can_afford(SUPPLYDEPOT) and (len(self.units(SUPPLYDEPOT))+self.already_pending(SUPPLYDEPOT))<24 and self.already_pending(SUPPLYDEPOT)<=2 and self.units(COMMANDCENTER).exists:
			await self.build(SUPPLYDEPOT, near=self.units(COMMANDCENTER)[0].position.towards(self.game_info.map_center, 8))

	async def create_scv(self):            #vytvarim workery
			if self.can_afford(SCV) and self.units(COMMANDCENTER).ready.noqueue.exists:
				await self.do(random.choice(self.units(COMMANDCENTER).ready.noqueue).train(SCV))   

	async def create_new_commandcenter(self):           #expanduju
			if self.can_afford(COMMANDCENTER) and not self.already_pending(COMMANDCENTER):
				await self.expand_now()


	async def build_barracks(self):           #stavim barracky
		if (len(self.units(BARRACKS)) + self.already_pending(BARRACKS)) <2 and self.can_afford(BARRACKS) and self.townhalls.exists:
			await self.build(BARRACKS, near = self.townhalls.random.position.towards(self.game_info.map_center, 10))

	async def create_vespine_collector(self):         #Vespene collectory
		for hatch in self.units(COMMANDCENTER):
			vespenes = self.state.vespene_geyser.closer_than(10.0, hatch)
			for vespene in vespenes:
				if not self.units(REFINERY).closer_than(1.0, vespene).exists:
					if len(self.units(REFINERY))<len(self.units(COMMANDCENTER))*2 and self.can_afford(REFINERY) and self.units(SCV).exists:
						await self.do(self.units(SCV).random.build(REFINERY, vespene))
						break

	async def rush_battlecruisers(self):						#Funkce ktera je technology tree   Barracks->Factory->FactoryTechLab->Starport->Fusioncore
		number_of_starports = 3
		if self.units(BARRACKS).ready.exists and self.can_afford(FACTORY) and (len(self.units(BATTLECRUISER))==0 or len(self.units(STARPORTTECHLAB))!=number_of_starports) and self.townhalls.exists:
			if len(self.units(FACTORY))==0 and not self.already_pending(FACTORY):
				await self.build(FACTORY, near = self.townhalls.random.position)
			if self.units(FACTORY).ready.exists:
				if not self.units(FACTORY)[0].has_add_on and self.can_afford(FACTORYTECHLAB):
					await self.do(self.units(FACTORY)[0].build(FACTORYTECHLAB))
				if len(self.units(STARPORT))<=number_of_starports and not self.already_pending(STARPORT) and self.can_afford(STARPORT):
					await self.build(STARPORT, near=self.townhalls.random.position.towards(self.game_info.map_center, 18))
				if self.units(STARPORT).ready.exists:
					if len(self.units(FUSIONCORE))==0 and not self.already_pending(FUSIONCORE) and self.can_afford(FUSIONCORE):
						await self.build(FUSIONCORE, near = self.units(COMMANDCENTER)[0])
					if self.units(FUSIONCORE).ready.exists:
						counter = 0
						for sp in self.units(STARPORT).ready:
							if sp.add_on_tag == 0:
								await self.do(sp.build(STARPORTTECHLAB))

		if self.units(STARPORT).exists:                                     #pokud vše mame tak tvořime battlecruisery!!!
			for sp in self.units(STARPORT):
				if sp.has_add_on and sp.noqueue:
					if self.can_afford(BATTLECRUISER) and self.can_feed(BATTLECRUISER):
						await self.do(sp.train(BATTLECRUISER))







	async def create_marine(self):														#vytvarim mariny
		if self.units(BARRACKS).ready.noqueue.exists and self.can_afford(MARINE):
				await self.do(self.units(BARRACKS).ready.noqueue.random.train(MARINE))







	async def create_siege(self):                                                      #Vytvrařim siegetanky
		if self.units(FACTORY).ready.exists:
			for fact in self.units(FACTORY).noqueue:
				if fact.has_add_on and self.can_afford(SIEGETANK):
					await self.do(fact.train(SIEGETANK))
		elif(not self.units(FACTORY).exists and not self.already_pending(FACTORY)):
			await self.build_barracks()  #Pokud ještě nejsme u factory tak je rushnem v technology tree
			await self.rush_battlecruisers()


	async def army_management(self):     
		#if(self.known_enemy_units(CHANGELINGMARINE).exists):

			#print("JJJJJJJJJJJAJAJ")
			          #inteligence vojaku - defují a brání okolo sebe
		#MARINE
		if (self.known_enemy_units-self.known_enemy_units(CHANGELINGMARINE)).exists:
					for marine in self.units(MARINE).idle:
						if((self.known_enemy_units-self.known_enemy_units(CHANGELINGMARINE)).closer_than(70.0,marine).exists):
							await self.do(marine.attack((self.known_enemy_units-self.known_enemy_units(CHANGELINGMARINE)).closest_to(marine)))
		#BATTLECRUISERS
		
		if self.units(BATTLECRUISER).idle.exists:
			for bc in self.units(BATTLECRUISER).idle:
						if (self.known_enemy_units-self.known_enemy_units(CHANGELINGMARINE)).closer_than(35.0,bc).exists:
							await self.do(bc.attack((self.known_enemy_units-self.known_enemy_units(CHANGELINGMARINE)).closest_to(bc)))
							await self.do(bc.move((self.known_enemy_units-self.known_enemy_units(CHANGELINGMARINE)).closest_to(bc).position))

		#SIEGE TANKS
		if self.units(SIEGETANK).exists:
			for sg in self.units(SIEGETANK):
				if (self.known_enemy_units-self.known_enemy_units(CHANGELINGMARINE)).closer_than(50.0,sg).exists:
					if not (self.known_enemy_units-self.known_enemy_units(CHANGELINGMARINE)).closer_than(12.5,sg).exists:
						if sg.is_idle:
							await self.do(sg.move((self.known_enemy_units-self.known_enemy_units(CHANGELINGMARINE)).closest_to(sg).position)) # blizi se kdyz je blizko nepritel
					else:
						await self.do(sg(AbilityId.SIEGEMODE_SIEGEMODE))  #Siegne kdyz je blizko nepritel

		if self.units(SIEGETANKSIEGED).idle.exists:  
			for sgs in (self.units(SIEGETANKSIEGED).idle):
				if not (self.known_enemy_units-self.known_enemy_units(CHANGELINGMARINE)).closer_than(13.5,sgs).exists:
					await self.do(sgs(AbilityId.UNSIEGE_UNSIEGE))    #Unsiegne kdyz neni pobliz nepritel
				elif (self.known_enemy_units-self.known_enemy_units(CHANGELINGMARINE)).closer_than(13.0,sgs).exists:
					await self.do(sgs.attack((self.known_enemy_units-self.known_enemy_units(CHANGELINGMARINE)).closest_to(sgs)))  #Utoci na nepritele v Rangi (13)

	async def ENGAGE(self):                                        #Posílám všechny jednotky na nejbližší jednotky(pokud neexistuji jdou na nepřátelskou zakladnu)

		#  if len(self.units(BATTLECRUISER))>0:
		# 	for bc in self.units(BATTLECRUISER).idle:
		# 		if self.known_enemy_units.closer_than(65.0,bc).exists:
		# 			await self.do(bc.attack(self.known_enemy_units.closest_to(bc)))
		# 			await self.do(bc.move(self.known_enemy_units.closest_to(bc).position))
		# 		else:
		# 			await self.do(bc(AbilityId.EFFECT_TACTICALJUMP, self.enemy_start_locations[0].position))         #battlecruisery warpují

		# if len(self.units(MARINE))>0:
		# 	for bc in self.units(MARINE).idle:
		# 		if self.known_enemy_units.closer_than(65.0,bc).exists:
		# 			await self.do(bc.attack(self.known_enemy_units.closest_to(bc)))
		# 			await self.do(bc.move(self.known_enemy_units.closest_to(bc).position))
		# 		else:
		# 			await self.do(bc.move(self.enemy_start_locations[0].position))


		# if len(self.units(SIEGETANK))>0:
		# 	for bc in self.units(SIEGETANK).idle:
		# 		if self.known_enemy_units.closer_than(65.0,bc).exists:
		# 			await self.do(bc.attack(self.known_enemy_units.closest_to(bc)))
		# 			await self.do(bc.move(self.known_enemy_units.closest_to(bc).position))
		# 		else:
		# 			await self.do(bc.move(self.enemy_start_locations[0].position))

		army = self.units(BATTLECRUISER).idle | self.units(MARINE).idle | self.units(SIEGETANK).idle
		target = self.select_target()
		for unit in army:
			await self.do(unit.attack(target))













#realtime=true -> hra běží v reálném čase; false-> hra běží rychle

#run_game(maps.get("CatalystLE"), [Bot(Race.Zerg, SrBotZerg()),Bot(Race.Terran, SrBoTerran())], realtime=False)  #Muj Zerg vs muj Terran

#run_game(maps.get("CatalystLE"), [Human(Race.Terran),Bot(Race.Terran, SrBoTerran())], realtime=True)  #Hráč Terran vs muj Terran

#run_game(maps.get("CatalystLE"), [Human(Race.Terran),Bot(Race.Zerg, SrBotZerg())], realtime=True) #Hráč Terran vs muj Zerg
for i in range(number_of_games):
	print("-- Hra "+str(i+1)+" z "+str(number_of_games)+" --")
	time.sleep(5)                       #aby se stihla ukončit pposlední hra (nemuzou byt 2 instance hry zapnute najednou)
	if(DEBUG_SHOWGAME):
		if(i%3==0):
			result = run_game(maps.get("CatalystLE"), [Bot(Race.Terran, SrBoTerran(0)),Computer(Race.Zerg, Difficulty.Easy)], realtime=False) 
		elif(i%3==1): 
			result = run_game(maps.get("CatalystLE"), [Bot(Race.Terran, SrBoTerran(0)),Computer(Race.Zerg, Difficulty.Easy)], realtime=False)
		elif(i%3==2):
			result = run_game(maps.get("CatalystLE"), [Bot(Race.Terran, SrBoTerran(0)),Computer(Race.Zerg, Difficulty.Easy)], realtime=False)
		print("HRA SKONCILA : "+str(result))







	else:
		#---------------CTU------------

		ranking = open("ranking.txt","r")
		is_ranking = int(ranking.readline())
		top_score = int(ranking.readline())
		current_wins = int(ranking.readline())
		current_games = int(ranking.readline())
		counter = int(ranking.readline())
		difficulty_level = str(ranking.readline())
		ranking.close()
		print("Rankedova hra / Difficulty : " + str(is_ranking) + " / " + difficulty_level )
		print("vyhry/celkem her/musi presahnout : " + str(current_wins) + " / " + str(current_games) + " / " + str(top_score) )
		print("Counter: " + str(counter))

		#-------------SYSTEM LEARNINGU-------------
		if(is_ranking==1 or counter==0):
			mutate=0
		else:
			mutate=1

		if(difficulty_level=="Easy"):
			if(i%3==0):
				result = run_game(maps.get("CatalystLE"), [Bot(Race.Terran, SrBoTerran(mutate)),Computer(Race.Terran, Difficulty.Easy)], realtime=False) 
			elif(i%3==1): 
				result = run_game(maps.get("CatalystLE"), [Bot(Race.Terran, SrBoTerran(mutate)),Computer(Race.Zerg, Difficulty.Easy)], realtime=False)
			elif(i%3==2):
				result = run_game(maps.get("CatalystLE"), [Bot(Race.Terran, SrBoTerran(mutate)),Computer(Race.Protoss, Difficulty.Easy)], realtime=False)

		if(difficulty_level=="Medium"):
			if(i%3==0):
				result = run_game(maps.get("CatalystLE"), [Bot(Race.Terran, SrBoTerran(mutate)),Computer(Race.Terran, Difficulty.Medium)], realtime=False) 
			elif(i%3==1): 
				result = run_game(maps.get("CatalystLE"), [Bot(Race.Terran, SrBoTerran(mutate)),Computer(Race.Zerg, Difficulty.Medium)], realtime=False)
			elif(i%3==2):
				result = run_game(maps.get("CatalystLE"), [Bot(Race.Terran, SrBoTerran(mutate)),Computer(Race.Protoss, Difficulty.Medium)], realtime=False)

		if(difficulty_level=="Hard"):
			if(i%3==0):
				result = run_game(maps.get("CatalystLE"), [Bot(Race.Terran, SrBoTerran(mutate)),Computer(Race.Terran, Difficulty.Hard)], realtime=False) 
			elif(i%3==1): 
				result = run_game(maps.get("CatalystLE"), [Bot(Race.Terran, SrBoTerran(mutate)),Computer(Race.Zerg, Difficulty.Hard)], realtime=False)
			elif(i%3==2):
				result = run_game(maps.get("CatalystLE"), [Bot(Race.Terran, SrBoTerran(mutate)),Computer(Race.Protoss, Difficulty.Hard)], realtime=False)

		if(difficulty_level=="VeryHard"):
			if(i%3==0):
				result = run_game(maps.get("CatalystLE"), [Bot(Race.Terran, SrBoTerran(mutate)),Computer(Race.Terran, Difficulty.VeryHard)], realtime=False) 
			elif(i%3==1): 
				result = run_game(maps.get("CatalystLE"), [Bot(Race.Terran, SrBoTerran(mutate)),Computer(Race.Zerg, Difficulty.VeryHard)], realtime=False)
			elif(i%3==2):
				result = run_game(maps.get("CatalystLE"), [Bot(Race.Terran, SrBoTerran(mutate)),Computer(Race.Protoss, Difficulty.VeryHard)], realtime=False)


		with open('score.txt', 'r') as f:
			lines = f.read().splitlines()
			last_line = lines[-1]
			if(str(last_line)=="Result.Defeat.Time"):
				result=Result.Defeat

		if(is_ranking==1):
			if(result==Result.Victory):
				result=1
			else:
				result=0
			current_wins+=result
			current_games+=1
			if(top_score>=3-current_games+current_wins): #jestli skore muzu vubec jeste prebit
				counter+=1
				is_ranking=0
				current_games=0
				current_wins=0

			if(current_games==3):                  #dohraje rankedy
				if(current_wins<=top_score):	   #dopadl hur nebo stejne
					counter+=1
					is_ranking=0
					current_games=0
					current_wins=0

				elif(current_wins==3):		#vyhral vše
					save_nn_special(current_wins,difficulty_level)
					difficulty_level = change_diff(difficulty_level,1)
					counter=0
					is_ranking=0
					current_games=0
					current_wins=0
					top_score=0
				else:					
					save_nn_special(current_wins,difficulty_level)		#dopadl lepe
					top_score=current_wins
					counter=0
					is_ranking=0
					current_games=0
					current_wins=0

		else:
			if(result==Result.Victory):
				is_ranking=1
				current_games=1
				current_wins=1
			else:
				if(top_score==0 and difficulty_level=="Easy"):            #Pokud prohraje při uplne nove mutaci v easy modu nema cenu zvysovat counter -> zbytecne by ubiral sance nasledujicim viteznym mutacim 
					counter=0
					f = open("weights.txt","w")
					f.close()
				else:
					counter+=1

		if(counter>=int(max_counter(difficulty_level))):
			if(difficulty_level=="Easy"):       #Uplne resetovani NN
				f = open("weights.txt","w")
				f.close()
			difficulty_level = change_diff(difficulty_level,-1)
			counter=0
			is_ranking=0
			current_games=0
			current_wins=0
			top_score=0



		ranking = open("ranking.txt","w")
		ranking.write(str(is_ranking)+"\n")
		ranking.write(str(top_score)+"\n")
		ranking.write(str(current_wins)+"\n")
		ranking.write(str(current_games)+"\n")
		ranking.write(str(counter)+"\n")
		ranking.write(difficulty_level)
		ranking.close()

		if(difficulty_level=="GG"):
			break









