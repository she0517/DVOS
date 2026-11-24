"""
这个模块用于调用copt求解器求解IP模型，输入DataLoader的实例，返回IP模型的最优值和求解时长
"""

import os,shutil,tempfile
from math import floor
from coptpy import COPT,Envr,quicksum
from frfs import FRFS

class IPSolver:
	def __init__(self,dataloader):
		self.data = dataloader
		self.model = Envr().createModel('IP')
		self.eps = 0.1 
		gmax = max(list(self.data.gentrin.values())+list(self.data.gbreakin.values())\
			+list(self.data.gentrout.values())+list(self.data.gbreakout.values()))
		self.M = 2*self.data.T[-1]+gmax+self.eps+1 # M：足够大的正数
		self.yoper = self.model.addVars(self.data.Oin+self.data.Oout,vtype=COPT.INTEGER,lb=self.data.T[0],ub=self.data.T[-1],nameprefix='yoper')
		self.yberth = self.model.addVars(self.data.V,vtype=COPT.INTEGER,lb=self.data.T[0],ub=self.data.T[-1],nameprefix='yberth')
		self.yroute = self.model.addVars(self.data.V,vtype=COPT.INTEGER,lb=self.data.T[0],ub=self.data.T[-1],nameprefix='yroute')
		self.zberth = self.model.addVars(self.data.V,vtype=COPT.INTEGER,lb=self.data.T[0],ub=self.data.T[-1],nameprefix='zberth')
		self.zroute = self.model.addVars(self.data.V,vtype=COPT.INTEGER,lb=self.data.T[0],ub=self.data.T[-1],nameprefix='zroute')
		self.xclass = self.model.addVars([(v,e) for v in self.data.V for e in self.data.Ev[v]],vtype=COPT.BINARY,nameprefix='xclass')
		self.xberth = self.model.addVars([(v,t,e) for v in self.data.V for t in self.data.T for e in self.data.Ev[v]],\
			vtype=COPT.BINARY,nameprefix='xberth')
		self.xroute = self.model.addVars([(v,r) for v in self.data.V for r in self.data.R],vtype=COPT.BINARY,nameprefix='xroute')
		self.xtide = self.model.addVars([(v,j) for v in self.data.V for j in self.data.Jtide.get(v,[])],vtype=COPT.BINARY,nameprefix='xtide')
		self.uline = self.model.addVars([(v1,v2,r) for v1 in self.data.V for v2 in self.data.V if v1!=v2 for r in self.data.R],\
			vtype=COPT.BINARY,nameprefix='uline')
		self.ubefore = self.model.addVars([(o1,o2) for o1 in self.data.Oin+self.data.Oout for o2 in self.data.Oin+self.data.Oout],\
			vtype=COPT.BINARY,nameprefix='ubefore')
		self.m = self.model.addVars([(v,t) for v in self.data.V for t in self.data.T],vtype=COPT.BINARY,nameprefix='m')
		self.varsigma_bef = self.model.addVars([(v,t) for v in self.data.V for t in self.data.T],vtype=COPT.BINARY,nameprefix='varsigma_bef')
		self.varsigma_aft = self.model.addVars([(v,t) for v in self.data.V for t in self.data.T],vtype=COPT.BINARY,nameprefix='varsigma_aft')
		self.w = self.model.addVars([(r,t,p) for r in self.data.R for t in self.data.T for p in self.data.P],\
			vtype=COPT.INTEGER,lb=0,ub=max(self.data.s.values()),nameprefix='w')
		self.xspeed = self.model.addVars([(v,r,p) for v in self.data.V for r in self.data.R for p in self.data.P],\
			vtype=COPT.INTEGER,lb=0,ub=self.data.f,nameprefix='xspeed')
		self.alpha = self.model.addVars([(v,t,r,p) for v in self.data.V for t in self.data.T for r in self.data.R for p in self.data.P],\
			vtype=COPT.INTEGER,lb=0,ub=self.data.f,nameprefix='alpha')

	def _write(self,writer,filename):
		fd,tmp = tempfile.mkstemp(suffix=os.path.splitext(filename)[1],prefix='ip_write_')
		os.close(fd)
		writer(tmp)
		os.makedirs(os.path.dirname(filename) or '.',exist_ok=True)
		shutil.move(tmp,filename)

	def _warm_start(self):
		# 调用frfs求一个快速可行解注入模型作为热启动，加速IP模型的求解
		try:
			frfs = FRFS(self.data)
			frfs.run()
		except RuntimeError as e:
			print('[IPSolver warning] frfs热启动失败，本次求解不使用热启动：{}'.format(e))
			return
		startvars,startvals = [],[]
		for o in self.data.Oin+self.data.Oout:
			v = self.data.vo[o]
			startvars.append(self.yoper[o])
			startvals.append(frfs.yoperin[v] if o in self.data.Oin else frfs.yoperout[v])
		for v in self.data.V:
			startvars += [self.yberth[v],self.yroute[v],self.zberth[v],self.zroute[v]]
			startvals += [frfs.yberth[v],frfs.yroute[v],frfs.zberth[v],frfs.zroute[v]]
			for e in self.data.Ev[v]:
				startvars.append(self.xclass[v,e])
				startvals.append(1 if e==frfs.xclass[v] else 0)
			for r in self.data.R:
				startvars.append(self.xroute[v,r])
				startvals.append(1 if r==frfs.xroute[v] else 0)
			for t in self.data.T:
				startvars.append(self.m[v,t])
				startvals.append(frfs.m.get((v,t),0))
		self.model.setMipStart(startvars,startvals) # 设置热启动值
		self.model.loadMipStart() # 导入热启动值
		self.model.setParam(COPT.Param.MipStartMode,2) # 只注入frfs给出的决策变量，其余辅助变量由copt自动补全

	def runModel(self,output='./solutions/IP_solution.sol'):
		self._warm_start() # 自动注入frfs的求解结果作为热启动
		self.model.solve()
		if self.model.status == COPT.INFEASIBLE: # 仅当模型真的不可行时才求IIS；达到时限等情形是可行的，直接返回当前最好解
			self.model.computeIIS()
			self._write(self.model.writeIIS,'./IP_infeasible.ilp')
			return None,self.model.solvingtime
		if output:
			self._write(self.model.write,output)
		return self.model.objval,self.model.solvingtime

	def buildModel(self):
		self.model.setObjective(
			quicksum(self.data.gamma[v]*(self.yoper[self.data.oout[v]]+self.data.gentrout[v]-self.data.l[v]) for v in self.data.V)
			,sense = COPT.MINIMIZE
			)
		# 航道与潮汐窗口约束
		self.model.addConstrs(
			(self.yoper[o]>=self.data.l[self.data.vo[o]] for o in self.data.Oin)
			,nameprefix = '(1)'
			)
		self.model.addConstrs(
			(self.ubefore[o1,o2]+self.ubefore[o2,o1]==1\
				for o1 in self.data.Oin+self.data.Oout for o2 in self.data.Oin+self.data.Oout if o1!=o2)
			,nameprefix = '(2)'
			)
		self.model.addConstrs(
			(self.ubefore[o1,o2]+self.ubefore[o2,o1]==0\
				for o1 in self.data.Oin+self.data.Oout for o2 in self.data.Oin+self.data.Oout if o1==o2)
			,nameprefix = '(3)'
			)
		self.model.addConstrs(
			(self.yoper[o1]+self.data.gentrin[self.data.vo[o1]]\
				<= self.yoper[o2]+self.data.gentrin[self.data.vo[o2]]+self.M*(1-self.ubefore[o1,o2])\
				for o1 in self.data.Oin for o2 in self.data.Oin if o1!=o2 and self.data.n[self.data.vo[o1]]>=self.data.n[self.data.vo[o2]])
			,nameprefix = '(4)'
			)
		self.model.addConstrs(
			(self.yoper[o1]+self.data.gbreakin[self.data.vo[o1]]\
				<= self.yoper[o2]+self.data.gbreakin[self.data.vo[o2]]+self.M*(1-self.ubefore[o1,o2])\
				for o1 in self.data.Oin for o2 in self.data.Oin if o1!=o2 and self.data.n[self.data.vo[o1]]<self.data.n[self.data.vo[o2]])
			,nameprefix = '(5)'
			)
		self.model.addConstrs(
			(self.yoper[o1]+self.data.gbreakout[self.data.vo[o1]]\
				<= self.yoper[o2]+self.data.gbreakout[self.data.vo[o2]]+self.M*(1-self.ubefore[o1,o2])\
				for o1 in self.data.Oout for o2 in self.data.Oout if o1!=o2 and self.data.n[self.data.vo[o1]]>=self.data.n[self.data.vo[o2]])
			,nameprefix = '(6)'
			)
		self.model.addConstrs(
			(self.yoper[o1]+self.data.gentrout[self.data.vo[o1]]\
				<= self.yoper[o2]+self.data.gentrout[self.data.vo[o2]]+self.M*(1-self.ubefore[o1,o2])\
				for o1 in self.data.Oout for o2 in self.data.Oout if o1!=o2 and self.data.n[self.data.vo[o1]]<self.data.n[self.data.vo[o2]])
			,nameprefix = '(7)'
			)
		self.model.addConstrs(
			(self.yoper[o1]+self.data.gbreakin[self.data.vo[o1]]\
				<= self.yoper[o2]+self.data.gbreakout[self.data.vo[o2]]+self.M*(1-self.ubefore[o1,o2])\
				for o1 in self.data.Oin for o2 in self.data.Oout if self.data.gmode[self.data.vo[o1]]+self.data.gmode[self.data.vo[o2]]>=1)
			,nameprefix = '(8)'
			)
		self.model.addConstrs(
			(self.yoper[o2]+self.data.gentrout[self.data.vo[o2]]\
				<= self.yoper[o1]+self.data.gentrin[self.data.vo[o1]]+self.M*(1-self.ubefore[o2,o1])\
				for o1 in self.data.Oin for o2 in self.data.Oout if self.data.gmode[self.data.vo[o1]]+self.data.gmode[self.data.vo[o2]]>=1)
			,nameprefix = '(9)'
			)
		self.model.addConstrs(
			(quicksum(self.xtide[self.data.vo[o],j] for j in self.data.Jtide[self.data.vo[o]])==1\
				for o in self.data.Oout if self.data.bneed[self.data.vo[o]])
			,nameprefix = '(10)'
			)
		self.model.addConstrs(
			(quicksum(self.data.btidelb[self.data.vo[o],j]*self.xtide[self.data.vo[o],j] for j in self.data.Jtide[self.data.vo[o]])<=self.yoper[o]\
				for o in self.data.Oout if self.data.bneed[self.data.vo[o]])
			,nameprefix = '(11)'
			)
		self.model.addConstrs(
			(self.yoper[o]<=quicksum(self.data.btideub[self.data.vo[o],j]*self.xtide[self.data.vo[o],j] for j in self.data.Jtide[self.data.vo[o]])\
				-self.data.gentrout[self.data.vo[o]]\
				for o in self.data.Oout if self.data.bneed[self.data.vo[o]])
			,nameprefix = '(12)'
			)
		# 泊位分配约束
		self.model.addConstrs(
			(self.yberth[v]==self.yoper[self.data.oin[v]]+self.data.gbreakin[v] for v in self.data.V)
			,nameprefix = '(13)'
			) # 这里是不是应该==?对，是得用等号，用>=可能会让船提前跑进去了
		self.model.addConstrs(
			(self.yberth[v]+self.zberth[v]<=self.yoper[self.data.oout[v]] for v in self.data.V)
			,nameprefix = '(14)'
			)
		self.model.addConstrs(
			(self.yberth[v]-self.eps>=t-self.M*self.varsigma_bef[v,t] for v in self.data.V for t in self.data.T)
			,nameprefix = '(15)'
			)
		self.model.addConstrs(
			(self.yberth[v]<=t+self.M*(1-self.varsigma_bef[v,t]) for v in self.data.V for t in self.data.T)
			,nameprefix = '(16)'
			)
		self.model.addConstrs(
			(self.yberth[v]+self.zberth[v]+self.eps<=t+self.M*self.varsigma_aft[v,t] for v in self.data.V for t in self.data.T)
			,nameprefix = '(17)'
			)
		self.model.addConstrs(
			(self.yberth[v]+self.zberth[v]>=t-self.M*(1-self.varsigma_aft[v,t]) for v in self.data.V for t in self.data.T)
			,nameprefix = '(18)'
			)
		self.model.addConstrs(
			(quicksum(self.xclass[v,e] for e in self.data.Ev[v])==1 for v in self.data.V)
			,nameprefix = '(19)'
			)
		self.model.addConstrs(
			(self.xberth[v,t,e]<=self.xclass[v,e] for v in self.data.V for t in self.data.T for e in self.data.Ev[v])
			,nameprefix = '(20)'
			)
		self.model.addConstrs(
			(quicksum(self.xberth[v,t,e] for e in self.data.Ev[v])==self.varsigma_bef[v,t]+self.varsigma_aft[v,t]-1\
				for v in self.data.V for t in self.data.T)
			,nameprefix = '(21)'
			)
		self.model.addConstrs(
			(quicksum(self.xberth[v,t,e] for v in self.data.V if e in self.data.Ev[v])<=self.data.b[e]\
				for t in self.data.T for e in self.data.E)
			,nameprefix = '(22)'
			)
		# 筒仓运输线与库存约束
		self.model.addConstrs(
			(quicksum(self.xroute[v,r] for r in self.data.R)==1 for v in self.data.V)
			,nameprefix = '(23)'
			)
		self.model.addConstrs(
			(self.xroute[v1,r]+self.xroute[v2,r]-1<=self.uline[v1,v2,r]+self.uline[v2,v1,r]\
				for v1 in self.data.V for v2 in self.data.V if v1!=v2 for r in self.data.R)
			,nameprefix = '(24)'
			)
		self.model.addConstrs(
			(self.uline[v1,v2,r]+self.uline[v2,v1,r]<=self.xroute[v1,r]\
				for v1 in self.data.V for v2 in self.data.V if v1!=v2 for r in self.data.R)
			,nameprefix = '(25)'
			)
		self.model.addConstrs(
			(self.yroute[v1]+self.zroute[v1]<=self.yroute[v2]+self.M*(1-self.uline[v1,v2,r])\
				for v1 in self.data.V for v2 in self.data.V if v1!=v2 for r in self.data.R)
			,nameprefix = '(26)'
			)
		self.model.addConstrs(
			(self.yberth[v]+self.data.tprep[v]<=self.yroute[v] for v in self.data.V)
			,nameprefix = '(27)'
			) # 靠泊之后要做一个准备的操作
		self.model.addConstrs(
			(self.yroute[v]+self.zroute[v]+self.data.tdep[v]<=self.yberth[v]+self.zberth[v] for v in self.data.V)
			,nameprefix = '(28)'
			) # 筒仓运输线使用结束后要有一个准备操作
		self.model.addConstrs(
			(t>=self.yroute[v]-self.M*(1-self.m[v,t]) for v in self.data.V for t in self.data.T)
			,nameprefix = '(29)'
			)
		self.model.addConstrs(
			(self.alpha[v,t,r,p]<=self.w[r,t,p] for v in self.data.V for t in self.data.T for r in self.data.R for p in self.data.P)
			,nameprefix = '(30)'
			)
		self.model.addConstrs(
			(quicksum(self.alpha[v,t,r,p] for t in self.data.T for r in self.data.R)>=self.data.a[v,p]\
				for v in self.data.V for p in self.data.Pask[v])
			,nameprefix = '(31)'
			)
		self.model.addConstrs(
			(self.yroute[v]+self.zroute[v]-1>=t*self.m[v,t] for v in self.data.V for t in self.data.T)
			,nameprefix = '(32)'
			)
		self.model.addConstrs(
			(self.zroute[v]<=self.zberth[v] for v in self.data.V)
			,nameprefix = '(33)'
			)
		self.model.addConstrs(
			(self.xspeed[v,r,p]==floor(self.data.a[v,p]*self.data.f/max(self.data.a[v,pp] for pp in self.data.Pask[v]))*self.xroute[v,r]\
				for v in self.data.V for r in self.data.R for p in self.data.P)
			,nameprefix = '(34)'
			)
		self.model.addConstrs(
			(self.alpha[v,t,r,p]<=self.data.f*self.m[v,t] for v in self.data.V for t in self.data.T for r in self.data.R for p in self.data.P)
			,nameprefix = '(35)'
			)
		self.model.addConstrs(
			(self.alpha[v,t,r,p]<=self.xspeed[v,r,p] for v in self.data.V for t in self.data.T for r in self.data.R for p in self.data.P)
			,nameprefix = '(36)'
			)
		self.model.addConstrs(
			(self.alpha[v,t,r,p]>=self.xspeed[v,r,p]-self.data.f*(1-self.m[v,t])\
				for v in self.data.V for t in self.data.T for r in self.data.R for p in self.data.P)
			,nameprefix = '(37)'
			)
		self.model.addConstrs(
			(self.w[r,t,p]==self.data.s[r,p] for r in self.data.R for t in self.data.Tsupp for p in self.data.P)
			,nameprefix = '(38)'
			)
		self.model.addConstrs(
			(self.w[r,t+1,p]<=self.w[r,t,p]-quicksum(self.alpha[v,t,r,p] for v in self.data.V)\
				for r in self.data.R for t in self.data.T for p in self.data.P\
				if (t+1) in self.data.T and (t+1) not in self.data.Tsupp)
			,nameprefix = '(39)'
			)
		# 有效割，加速IP的求解，删了也可以
		self.model.addConstrs(
				(quicksum(self.alpha[v, t, r, p]
					for v in self.data.V for t in self.data.T if self.data.kappalb[xi] <= t <= self.data.kappaub[xi])
					<= self.data.s[r, p]
					for xi in self.data.Xi for r in self.data.R for p in self.data.P),
				nameprefix='enhance1',
			)
		self.model.addConstrs(
				(self.zroute[v] >= self.data.varthetaneed[v] for v in self.data.V),
				nameprefix='enhance2',
			)
		self.model.addConstrs(
				(self.yoper[self.data.oout[v]] >= self.data.l[v] + self.data.gbreakin[self.data.oin[v]] + self.data.varthetaneed[v]
					for v in self.data.V),
				nameprefix='enhance3',
			)
		self._write(self.model.write,'./models/IP_model.lp')

if __name__ == '__main__':
	from loader import DataLoader
	dataloader = DataLoader(os.path.join(os.path.dirname(os.path.abspath(__file__)),'data','INS1_V5C10.xlsx'))
	ip_solver = IPSolver(dataloader)
	ip_solver.buildModel()
	objval,solvetime = ip_solver.runModel()
	print('IP模型最优值：{}'.format(objval))
	print('求解时长：{}秒'.format(solvetime))
