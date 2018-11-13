# -*- encoding: utf-8 -*-
from GA import GA
from MyFuncTool import GetData,ResultShow,draw

class TSP(object):
	def __init__(self,Position,Dist,CityNum):
		""" 构造函数 """
		self.citys=Position							# 城市坐标
		self.dist=Dist								# 城市距离矩阵
		self.citynum=CityNum						# 城市数量

		self.ga = GA(aCrossRate=0.7,				# 交叉率
					aMutationRage=0.02,				# 突变概率
					aUnitCount=100,					# 一个种群中的个体数
					aGeneLenght=self.citynum,		# 基因长度（城市数）
					aMatchFun=self.matchFun())		# 适配函数

	def distance(self, path):
		"""
			函数名：distance(self, path)
			函数功能：	根据路径求出总路程
				输入	1 	self：类自身
				输入 2	path：路径
				输出	1	无
			其他说明：无
		"""
		# 计算从初始城市到最后一个城市的路程
		distance = sum([self.dist[city1][city2] for city1,city2 in 
							zip(path[:self.citynum], path[1:self.citynum+1])])
		# 计算从初始城市到最后一个城市再回到初始城市所经历的总距离
		distance += self.dist[path[-1]][0]

		return distance

	def matchFun(self):
		"""
			函数名：matchFun(self)
			函数功能：	定义适配函数,并返回函数句柄
				输入	1 	self：类自身
				输出	1	所定义的适配函数的函数句柄
			其他说明：无
		"""
		return lambda life: 1.0 / self.distance(life.gene)

	def run(self, generate=0):
		"""
			函数名：run(self, n=0)
			函数功能：	遗传算法解旅行商问题的运行函数
				输入	1 	self：类自身
				 	2	generate：种群迭代的代数
				输出	1	distance:最小路程
					2	self.ga.best.gene：最好路径
					3	distance_list：每一代的最好路径列表
			其他说明：无
		"""
		distance_list = []

		while generate > 0:
			self.ga.nextGeneration()
			distance = self.distance(self.ga.best.gene)
			distance_list.append(distance)
			generate -= 1
		
		return distance,self.ga.best.gene,distance_list

##############################程序入口#########################################
if __name__ == '__main__':
	Position,CityNum,Dist = GetData("./data/TSP25cities.tsp")
	tsp = TSP(Position,Dist,CityNum)
	generate=100
	Min_Path,BestPath,distance_list=tsp.run(generate)
	
	# 结果打印
	BestPath.append(BestPath[0])
	ResultShow(Min_Path,BestPath,CityNum,"GA")
	draw(BestPath,Position,"GA",True,range(generate), distance_list)

