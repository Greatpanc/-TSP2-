# -*- encoding: utf-8 -*-

"""
	TSP问题GA求解包
	
	Author:	Greatpan
	Date:	2018.11.21
"""

from Ant import AntList
from MyFuncTool import GetData,ResultShow,draw
import numpy as np

class TSP(object):
	def __init__(self,Position,Dist,CityNum):
		""" 构造函数 """
		self.citys=Position							# 城市坐标
		self.dist=Dist								# 城市距离矩阵
		self.citynum=CityNum						# 城市数量

		self.ant =AntList(numant=25,				# 蚂蚁个数
						 distfunc=self.distance,	# 计算距离的函数
						 getEtatable=self.defEtatable,	# 定义启发式矩阵函数
						 numcity=self.citynum,		# 城市个数
						 alpha=1,					# 信息素重要程度因子
						 rho=0.1,					# 信息素的挥发速度
						 Q=1)						# 品质因子

	def defEtatable(self):
		"""
			函数名：defEtatable(self)
			函数功能：	在蚁群算法中定义的启发式矩阵
				输入	1 	self：类自身
				输出	1	无
			其他说明：无
		"""
		return 1.0/(self.dist+np.diag([1e10]*self.citynum))

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

	def run(self, generate=0):
		"""
			函数名：run(self, n=0)
			函数功能：	遗传算法解旅行商问题的运行函数
				输入	1 	self：类自身
				 	2	generate：种群迭代的代数
				输出	1	self.ant.bestantunit.length:最小路程
					2	self.ga.best.path：最好路径
					3	distance_list：每一代的最好路径列表
			其他说明：无
		"""
		distance_list = []

		while generate > 0:
			self.ant.nextGeneration()
			distance = self.ant.bestantunit.length
			distance_list.append(distance)
			generate -= 1
		
		return self.ant.bestantunit.length,self.ant.bestantunit.path,distance_list

##############################程序入口#########################################
if __name__ == '__main__':
	Position,CityNum,Dist = GetData("./data/TSP25cities.tsp")
	tsp = TSP(Position,Dist,CityNum)
	generate=500
	Min_Path,BestPath,distance_list=tsp.run(generate)
	
	print(BestPath)
	print(tsp.distance(BestPath))
	# 结果打印
	BestPath.append(BestPath[0])
	ResultShow(Min_Path,BestPath,CityNum,"GA")
	draw(BestPath,Position,"GA",True,range(generate), distance_list)
