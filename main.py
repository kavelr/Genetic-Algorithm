import random as r


key = {
    '0000': 0, '0001': 1, '0010': 2, '0011': 3, '0100': 4, '0101': 5, '0110': 6, '0111': 7, '1000': 8, '1001': 9
}
opskey = {
    '1010': '+', '1011': '-', '1100': '*', '1101': '/'
}

chromolength = 100		# must be a multiple of 4

def gettarget():
	targettype = input('Input target or randomize? (i/r)')
	if targettype == 'i':
		global target
		target = float(input('Target: '))
	else:
		target = 0
		while len(str(target)) < 7:
			targetchromosome = ''
			chromosome = ''
			for i in range(chromolength):
				chromosome = chromosome + str((r.randint(0, 1)))
			global targetchromosome
			targetchromosome = chromosome
			
			n = 0
			op = 'first'
			while n <= chromolength:
				    i = n + 4
				    if chromosome[n : i] in key:
				        num = key[chromosome[n : i]]
				        if chromosome[n : i] in key:
				            if op == 'first':
				                dna = num
				                num = 0
				                op = ''
				            elif op != '':
				                if op != '/' or num != 0:
				                    dna = eval(str(dna) + op + str(num)) 
				                    num = 0
				                    op = ''
		
				    elif chromosome[n : i] in opskey:
				        if op != 'first':
				            op = opskey[chromosome[n : i]]
				    n += 4
		    
			global target
			target = dna
	
class Organism:
	def __init__(self, chromosome):
		if chromosome == '':
		    for i in range(chromolength):
		        chromosome = chromosome + str((r.randint(0, 1)))
		self.chromosome = chromosome
		
		self.pretty_print = ''

		n = 0
		op = 'first'
		dna = 0
		while n <= chromolength:
		    i = n + 4
		    if chromosome[n : i] in key:
		        num = key[chromosome[n : i]]
		        if chromosome[n : i] in key:
		            if op == 'first':
		                dna = num
		                self.pretty_print += str(num)
		                num = 0
		                op = ''
		            elif op != '':
		                if op != '/' or num != 0:
		                    dna = eval(str(dna) + op + str(num)) 
		                    self.pretty_print += op + str(num) 
		                    num = 0
		                    op = ''
	                            
	                    
		    elif chromosome[n : i] in opskey:
		        if op != 'first':
		            op = opskey[chromosome[n : i]]
		    n += 4
		self.dna = dna
        
		self.fitness = -0.5 * ((target)/10.0 - (self.dna)/10) ** 2

def mutate(chromosome):
    new_chr = ''
    for bit in chromosome:
        mutate = r.randint(0, r.randint(0, 200)) == 0
        if mutate:
            new_chr += str(1 - int(bit))

        else:
            new_chr += bit
    
    return new_chr

def roulette(chromosomes):
    total_fitness = 0
    counter = 0 

    for ch in chromosomes:
        total_fitness += ch.fitness 
    
    roulette = r.randint(0, int(total_fitness) - 3)

    for ch in chromosomes:
        counter += ch.fitness 
        if counter > roulette:
            return ch

def eval_gen(gen):
    best = None
    worst = None

    best_fitness = 0
    worst_fitness = 1000000
    avg_fitness = 0 

    for ch in gen:
        if ch.fitness > best_fitness:
            best = ch 
            best_fitness = ch.fitness 
        elif ch.fitness < worst_fitness:
            worst = ch 
            worst_fitness = ch.fitness
        
        avg_fitness += ch.fitness 
    
    return best, worst, best_fitness, worst_fitness, avg_fitness/float(len(gen))

def nextgen(gen):
    oldgen = gen
    newgen = []

    best, _, _, _, _ = eval_gen(gen)

    for i in range (49):
        newchromosome = ''
        
        parent1 = roulette(gen)
        parent2 = roulette(gen)
 
        switchpoint = r.randint(1, chromolength)
        newchromosome += parent1.chromosome[: switchpoint] + \
                            parent2.chromosome[switchpoint :]
        
        mutatedchromosome = mutate(newchromosome)

        newgen.append(Organism(mutatedchromosome))

    newgen.append(Organism(mutate(best.chromosome)))            
    
    return newgen

def main():
	gettarget()

	print ('Target: %s \n' % target)
	gen = []
	print ('Generation 0: ')
	for i in range(100):
	    gen.append(Organism(''))

	n = 1
	targetachieved = False
	
	while not targetachieved:
	    
	    worst_fitness = 10000000
	    for ch in gen:
	        if ch.fitness < worst_fitness:
	            worst_fitness = ch.fitness 
	    
	    for ch in gen:
	        ch.fitness -= worst_fitness 
	        ch.fitness += 1
	
	    b, w, bf, wf, af = eval_gen(gen)

	    if b.dna == target:
	        targetachieved = True
	        print ('Solution found at generation ' + str(n + 1))
	        print ('Best chromosome: ' + str(b.chromosome) + ' ( ' + str(b.pretty_print) + ' = ' + str(b.dna) + ' )  -> ' + str(round(bf, 3)))
	        print ('Worst chromosome: ' + str(w.chromosome) + ' ( ' + str(w.pretty_print) + ' = ' + str(w.dna) + ' )  -> ' + str(round(wf, 3)))
	        print ('Avg fitness: ' + str(round(af, 3))) 
	        print ('----------------------------------------')
	
	    if (n % 100) == 0:
	
	        print ('Target: ' + str(target) + '\n')
	        print ('Generation ' + str(n + 1))
	        print ('Best chromosome: ' + str(b.chromosome) + ' ( ' + str(b.pretty_print) + ' = ' + str(b.dna) + ' )  -> ' + str(round(bf, 3)))
	        print ('Worst chromosome: ' + str(w.chromosome) + ' ( ' + str(w.pretty_print) + ' = ' + str(w.dna) + ' )  -> ' + str(round(wf, 3)))
	        print ('Avg fitness: ' + str(round(af, 3))) 
	        print ('----------------------------------------')
	
	    gen = nextgen(gen)
	    
	    n += 1

main()
