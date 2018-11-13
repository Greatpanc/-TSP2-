# -*- coding: utf-8 -*-

import random

class GA(object):
	"""
		类名：GA
		类说明：	遗传算法类
	"""
	def __init__(self, aCrossRate, aMutationRage, aUnitCount, aGeneLenght, aMatchFun=lambda : 1):
		""" 构造函数 """
		self.crossRate = aCrossRate  		# 交叉概率 #
		self.mutationRate = aMutationRage  	# 突变概率 #
		self.unitCount = aUnitCount   		# 个体数 #
		self.geneLenght = aGeneLenght  		# 基因长度 #
		self.matchFun = aMatchFun  			# 适配函数
		self.population = []  	# 种群
		self.best = None  		# 保存这一代中最好的个体
		self.generation = 1  	# 第几代 #
		self.crossCount = 0  	# 交叉数量 #
		self.mutationCount = 0  # 突变个数 #
		self.bounds = 0.0  		# 适配值之和，用于选择时计算概率
		self.initPopulation()  	# 初始化种群 #

	def initPopulation(self):
		"""
			函数名：initPopulation(self)
			函数功能：	随机初始化得到一个种群
				输入	1 	self：类自身
				输出	1	无
			其他说明：无
		"""
		self.population = []
		unitCount = self.unitCount
		while unitCount>0:
			gene = [x for x in range(self.geneLenght)]
			random.shuffle(gene)  			# 随机洗牌 #
			unit = GAUnit(gene)
			self.population.append(unit)
			unitCount-=1

	def judge(self):
		"""
			函数名：judge(self)
			函数功能：	重新计算每一个个体单元的适配值
				输入	1 	self：类自身
				输出	1	无
			其他说明：无
		"""
		self.bounds = 0.0
		self.best = self.population[0]
		for unit in self.population:
			unit.value = self.matchFun(unit)
			self.bounds += unit.value
			if self.best.value < unit.value:	# score为距离的倒数 所以越小越好 #
				self.best = unit

	def cross(self, parent1, parent2):
		"""
			函数名：cross(self, parent1, parent2)
			函数功能：	根据parent1和parent2基于序列,随机选取长度为n的片段进行交换(n=index2-index1)
				输入	1 	self：类自身
					2	parent1: 进行交叉的双亲1
					3	parent2: 进行交叉的双亲2
				输出	1	newGene： 通过交叉后的一个新的遗传个体的基因序列号
			其他说明：进行交叉时采用的策略是,将parent2的基因段tempGene保存下来,然后对基因1所有序列号g依次进行判断,
				如果g在tempGene内,则舍去,否则就保存下来,并在第index1的位置插入tempGene
		"""
		index1 = random.randint(0, self.geneLenght - 1)  		# 随机生成突变起始位置 #
		index2 = random.randint(index1, self.geneLenght - 1)  	# 随机生成突变终止位置 #
		tempGene = parent2.gene[index1:index2]  				# 交叉的基因片段
		newGene = []
		p1len = 0
		for g in parent1.gene:
			if p1len == index1:
				newGene.extend(tempGene)  		# 插入基因片段
				p1len += 1
			if g not in tempGene:
				newGene.append(g)
				p1len += 1
		self.crossCount += 1
		return newGene

	def mutation(self, gene):
		"""
			函数名：mutation(self, gene)
			函数功能：	对输入的gene个体进行变异,也就是随机交换两个位置的基因号
				输入	1 	self：类自身
					2	gene: 进行变异的个体基因序列号
				输出	1	newGene： 通过交叉后的一个新的遗传个体的基因序列
			其他说明：无
		"""
		index1 = random.randint(0, self.geneLenght - 1)
		index2 = random.randint(0, self.geneLenght - 1)
		# 随机选择两个位置的基因交换--变异
		newGene = gene[:]  					# 产生一个新的基因序列，以免变异的时候影响父种群
		newGene[index1], newGene[index2] = newGene[index2], newGene[index1]
		self.mutationCount += 1
		return newGene
	
	def getOneUnit(self):
		"""
			函数名：getOneUnit(self)
			函数功能：	通过轮盘赌法,依据个体适应度大小,随机选择一个个体
				输入	1 	self：类自身
				输出	1	unit：所选择的个体
			其他说明：无
		"""
		r = random.uniform(0, self.bounds)
		for unit in self.population:
			r -= unit.value
			if r <= 0:
				return unit
		
		raise Exception("选择错误", self.bounds)
	
	def newChild(self):
		"""
			函数名：newChild(self)
			函数功能：	按照预定的概率进行交叉与变异后产生新的后代
				输入	1 	self：类自身
				输出	1	GAUnit(gene)：所产生的后代
			其他说明：无
		"""
		parent1 = self.getOneUnit()
		rate = random.random()
		
		# 按概率交叉
		if rate < self.crossRate:	# 交叉 
			parent2 = self.getOneUnit()
			gene = self.cross(parent1, parent2)
		else:						# 不交叉 
			gene = parent1.gene
		
		# 按概率突变
		rate = random.random()
		if rate < self.mutationRate:
			gene = self.mutation(gene)
		
		return GAUnit(gene)
	
	def nextGeneration(self):
		"""
			函数名：nextGeneration(self)
			函数功能：	产生下一代
				输入	1 	self：类自身
				输出	1	无
			其他说明：无
		"""
		self.judge()
		newPopulation = []						# 新种群
		newPopulation.append(self.best)  		# 把最好的个体加入下一代 #
		while len(newPopulation) < self.unitCount:
			newPopulation.append(self.newChild())
		self.population = newPopulation
		self.generation += 1

class GAUnit(object):
	"""
		类名：GAUnit
		类说明：	遗传算法个体类
	"""
	def __init__(self, aGene = None,SCORE_NONE = -1):
		""" 构造函数 """
		self.gene = aGene			# 个体的基因序列
		self.value = SCORE_NONE  	# 初始化适配值 