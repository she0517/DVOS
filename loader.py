"""
这个模块用于加载算例
"""

import os
from math import floor,ceil
import numbers
import pandas as pd

class DataLoader:
    """
    这个模块唯一的接口，其他类和函数都是用于算例文件解析的。
    当你想要使用算例，请直接使用这个类！！！
    """
    def __init__(self,src):
        loader = Loader.getFromFile(src)
        self.V = loader.ip.V
        self.T = loader.ip.T
        self.Tsupp = loader.ip.Tsupp
        self.E = loader.ip.E
        self.Ev = loader.ip.Ev
        self.R = loader.ip.R
        self.P = loader.ip.P
        self.Pask = loader.ip.Pask
        self.Jtide = loader.ip.Jtide
        self.Oin = loader.ip.Oin
        self.Oout = loader.ip.Oout
        self.n = loader.ip.n
        self.a = loader.ip.a
        self.f = loader.ip.f
        self.s = loader.ip.s
        self.b = loader.ip.b
        self.gmode = loader.ip.gmode
        self.tprep = loader.ip.tprep
        self.tdep = loader.ip.tdep
        self.l = loader.ip.l
        self.gamma = loader.ip.gamma
        self.vo = loader.ip.vo
        self.oin = loader.ip.oin
        self.oout = loader.ip.oout
        self.gentrin = loader.ip.gentrin
        self.gentrout = loader.ip.gentrout
        self.gbreakin = loader.ip.gbreakin
        self.gbreakout = loader.ip.gbreakout
        self.bneed = loader.ip.bneed
        self.btidelb = loader.ip.btidelb
        self.btideub = loader.ip.btideub
        self.DeltaPrime = loader.channel.Delta_prime
        self.Xi = loader.mp.Xi
        self.psiin = loader.channel.psiin
        self.psiout = loader.channel.psiout
        self.kappalb = loader.mp.kappalb
        self.kappaub = loader.mp.kappaub
        self.varthetacan = loader.mp.varthetacan
        self.varthetaneed = loader.mp.varthetaneed

class IP:
    """
    提供集合
    V,T,Tsupp,E,Ev,R,P,Pask,Jtide,Oin,Oout

    提供参数
    n,a,f,s,b,l,gamma,vo,oin,oout,gentrin,gentrout,gbreakin,gbreakout,bneed,btidelb,btideub,gmode
    """
    def __init__(self,src):
        df_time,df_berth,df_silo,df_ship = self.getfromsrc(src)
        self.V = [int(v) for v in df_ship['船舶编号'].values]
        self.Oin = self.V
        self.Oout = [o+len(self.V) for o in self.Oin]
        self.E = [int(e) for e in df_berth['泊位等级'].values]
        self.Ev = {}
        self._setEv(df_ship)
        self.R = [r for r in range(1,int(df_silo['筒仓运输线数量'].iloc[0])+1)] 
        self.P = [int(p) for p in df_silo['原煤种类'].values[:-1]]
        self.Pask = {}
        self.a = {}
        self._setPask_a(df_ship)
        self.f = df_silo['额定速度'].iloc[0]
        self.b = {int(e): int(num) for e,num in df_berth.values.tolist()}
        self.l = {v:int(l) for v,l in enumerate(df_ship['到港时间'].values,start=1)}
        self.gamma = {v:int(gamma) for v,gamma in enumerate(df_ship['权重等级'].values,start=1)}
        self.vo = {}
        self.oin = {}
        self.oout ={}
        self._set_vo_oin_oout()
        self.n = {v:n for v,n in enumerate(df_ship['航道航速（海里每小时）'].values,start=1)}
        self.gentrin = {v:0 for v in self.V}
        self.gbreakin = {v:floor(23/self.n[v]) for v in self.V}
        self.gentrout = {v:floor(23/self.n[v]) for v in self.V}
        self.gbreakout = {v:0 for v in self.V}
        self.T = [t for t in range(1,int(df_time["总时间步长"].iloc[0])+1)]
        self.Tsupp = [t for t in range(1,int(df_time["总时间步长"].iloc[0])+1,int(df_time["补给时间间隔"].iloc[0]))]
        self.Jtide = {}
        self.bneed = {}
        self.btidelb,self.btideub = {},{}
        self._setJtide_btide_lb_ub(df_time,df_ship)
        self.s ={}
        self._set_s(df_silo)
        self.gmode = {}
        for v,dwt in enumerate(df_ship['吨位（dwt）'],start=1):
            if dwt > 68000:
                self.gmode[v] = 1
            else:
                self.gmode[v] = 0
        self.tprep = {}
        self.tdep = {}
        for v in self.V:
            self.tprep[v]=2
            self.tdep[v] =1

    def getfromsrc(self,src):
        df_time = pd.read_excel(src,sheet_name="时间信息",engine="openpyxl")
        df_berth = pd.read_excel(src,sheet_name="泊位信息",engine="openpyxl")
        df_silo = pd.read_excel(src,sheet_name="筒仓运输线信息",engine="openpyxl")
        df_ship = pd.read_excel(src,sheet_name="船舶信息",engine="openpyxl")
        return df_time,df_berth,df_silo,df_ship

    def _setEv(self,df_ship):
        for v,info in enumerate(df_ship['可用泊位等级'].values,start=1):
            if isinstance(info, str):
                if len(info)>1:
                    info = list(map(int,info.split(',')))
                else:
                    info = [int(info)]
            else:
                info = [int(info)]
            self.Ev[v]=info

    def _setPask_a(self,df_ship):
        for v in self.V:
            self.Pask[v] = []
            for p in self.P:
                self.a[v,p] = df_ship.loc[v-1:,'煤种类{}'.format(p)].iloc[0]
                if self.a[v,p]>1e-3:
                    self.Pask[v].append(p)

    def _set_vo_oin_oout(self):
        for o in self.Oin + self.Oout:
            if o in self.Oin:
                self.vo[o] = o
            else:
                self.vo[o] = o - len(self.V)
        for v in self.V:
            self.oin[v] = v
            self.oout[v] = v+len(self.V)

    def _set_s(self,df_silo):
        for r in self.R:
            for p in self.P:
                self.s[r,p] = df_silo['初始库存量（吨）'].iloc[:-1].values[p-1]

    def _setJtide_btide_lb_ub(self,df_time,df_ship):
        for v,info in enumerate(df_ship['可通行潮汐窗口种类'].values,start=1):
            if not isinstance(info,str):
                info = str(int(info))
            if info.strip().lower() == 'do not need':
                self.bneed[v] = 0
            else:
                self.bneed[v] = 1
                H = int(df_time["总时间步长"].iloc[0])
                if int(info) == 1:
                    tide1_start = int(df_time["潮汐窗口种类1第一个时间步"].iloc[0])
                    tide1_duration = int(df_time["潮汐窗口种类1持续时间步"].iloc[0])
                    tide1_interval = int(df_time["潮汐窗口种类1时间间隔"].iloc[0])
                    counter = 1
                    for j,lb in enumerate(range(tide1_start,H+1,tide1_duration+tide1_interval),start=1):
                        self.btidelb[v,j]=lb
                        self.btideub[v,j]=min(H,lb+tide1_duration-1)
                        counter +=1
                    self.Jtide[v] = [j for j in range(1,counter)]
                if int(info) == 2:
                    tide2_start = int(df_time["潮汐窗口种类2第一个时间步"].iloc[0])
                    tide2_duration = int(df_time["潮汐窗口种类2持续时间步"].iloc[0])
                    tide2_interval = int(df_time["潮汐窗口种类2时间间隔"].iloc[0])
                    counter = 1
                    for j,lb in enumerate(range(tide2_start,H+1,tide2_duration+tide2_interval),start=1):
                        self.btidelb[v,j]=lb
                        self.btideub[v,j]=min(H,lb+tide2_duration-1)
                        counter +=1
                    self.Jtide[v] = [j for j in range(1,counter)]
                if int(info) == 3:
                    tide3_start = int(df_time["潮汐窗口种类3第一个时间步"].iloc[0])
                    tide3_duration = int(df_time["潮汐窗口种类3持续时间步"].iloc[0])
                    tide3_interval = int(df_time["潮汐窗口种类3时间间隔"].iloc[0])
                    counter = 1
                    for j,lb in enumerate(range(tide3_start,H+1,tide3_duration+tide3_interval),start=1):
                        self.btidelb[v,j]=lb
                        self.btideub[v,j]=min(H,lb+tide3_duration-1)
                        counter+=1
                    self.Jtide[v] = [j for j in range(1,counter)]

class Channel:
    """
    提供集合
    Delta_prime：航道点集合，包含虚拟航道点
    
    提供参数
    psiin,psiout：船舶进港到各个航道点的时间，船舶出港到各个航道点的时间
    """
    def __init__(self,n):
        """
        Args：
            n：船舶航速参数
        """
        self.entrance_x = 23
        self.breakwater_x = 0
        self.slowest_n = min([nval for nval in n.values()])
        self.num = (self.entrance_x-self.breakwater_x)//self.slowest_n+2
        self.num_prime = 2*self.num-1
        self.Delta_prime = [delta for delta in range(1,self.num_prime+1)]
        self.psiin,self.psiout = {},{}
        self._setpsi(n)

    def _setpsi(self,n):
        interval = (self.entrance_x-self.breakwater_x)/(self.num-1)
        for v in n.keys():
            for delta in self.Delta_prime:
                dist = interval*((self.num_prime-delta+1)//2)
                time = round(dist/n[v])
                self.psiin[v,delta] = time
            for delta in self.Delta_prime:
                dist = interval*(delta//2)
                time = round(dist/n[v])
                self.psiout[v,delta] = time

class MP:
    """
    提供集合
    Xi：库存补给周期的集合
    提供参数
    kappalb：库存补给周期下界
    kappaub：库存补给周期上界
    varthetacan：单周期可装载时间步
    varthetaneed：总共需要装载的时间步
    """
    def __init__(self,V,Tsupp,P,Pask,a,f,s):
        cycle_num, cycle_interval = len(Tsupp), Tsupp[-1] - Tsupp[-2]
        self.Xi = [xi for xi in range(1, cycle_num + 1)]
        self.kappalb,self.kappaub = {},{}
        for xi in self.Xi:
            self.kappalb[xi] = (xi - 1) * cycle_interval + 1
            self.kappaub[xi] = xi * cycle_interval
        self.varthetacan,self.varthetaneed ={},{}
        self._set_varthetacan_varthetaneed(V,cycle_interval,P,Pask,a,f,s)

    def _set_varthetacan_varthetaneed(self,V,cycle_interval,P,Pask,a,f,s):
        xspeed = {}
        for v in V:
            xspeed[v] = {}
            for p in P:
                xspeed[v][p] = floor(a[v, p] * f / max([a[v, pp] for pp in Pask[v]]))
        for v in V:
            self.varthetaneed[v] = max([ceil(a[v, p] / xspeed[v][p]) for p in Pask[v]])
            self.varthetacan[v]= cycle_interval
            flag = True
            while flag:
                for p in Pask[v]:
                    if self.varthetacan[v] * xspeed[v][p] > s[1,p]:
                        self.varthetacan[v] -= 1
                        break
                else:
                    flag = False

class Loader:
    @classmethod
    def getFromFile(cls,src):
        loader = cls()
        loader.ip = IP(src)
        loader.channel = Channel(loader.ip.n)
        loader.mp = MP(
            loader.ip.V,
            loader.ip.Tsupp,
            loader.ip.P,
            loader.ip.Pask,
            loader.ip.a,
            loader.ip.f,
            loader.ip.s)
        return loader
    

