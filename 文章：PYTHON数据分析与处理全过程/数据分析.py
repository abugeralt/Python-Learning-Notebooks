#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
#设置画图风格与图片中文字体
from matplotlib import pyplot as plt
plt.style.use("ggplot")
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False
#显示所有列
pd.set_option('display.max_columns', None)
#显示所有行
pd.set_option('display.max_rows', None)
#设置value的显示长度为100，默认为50
pd.set_option('max_colwidth',100)


# # 导入数据与描述统计

# In[2]:


data=pd.read_csv("data.csv")
#一般有两种编码模式，默认为utf-8,也可以用gbk
data=pd.read_csv("data.csv",encoding="utf-8")


# In[3]:


data.shape


# In[4]:


data.head()


# In[5]:


#groupby
data[["年份","通过与否"]].groupby("年份").count()
#这里也可以将count()改成你想要的函数，比如sum、median


# In[6]:


data[["年份","通过与否"]].groupby("年份").count().T


# In[7]:


data.describe()
#同样也可以用.T进行转置操作


# # 数据清洗

# In[8]:


#删除空值太多的行（这里是每行空值大于等于2个）
isdrop=[]
for index,row in data.iterrows():
    if row.isna().sum()>=2:
        isdrop.append(1)
    else:
        isdrop.append(0)
data.insert(loc=0,column="isdrop",value=pd.array(isdrop))


# In[9]:


#通过选择isdrop为0的行，就可以提取对应空值少的数据。
data.head()


# In[74]:


#按KEY去重
datacln=data.drop_duplicates("KEY")
datacln


# In[75]:


#去空
datadropna=data.dropna()
datadropna


# In[76]:


#填充空值(可以把0换成对应中位数、均值)
datafillna=data.fillna(0)
datafillna


# # 数据缩尾

# In[95]:


#x是列，a,b是想要进行切分的位置
def cap(x,a,b):
    qa=x.quantile(a)
#     print(qa)
    qb=x.quantile(b)
#     print(qb)
    for i in x:
        if i <=qa :
            x.replace(i,qa,inplace = True)
        if i >=qb:
            x.replace(i,qb,inplace = True)
#     print(pd.DataFrame(x).describe())
    return x


# In[96]:


data=pd.read_csv("data.csv")


# In[97]:


#直接进行缩尾处理
datacap=pd.DataFrame.copy(data)
cols=datacap.describe().columns
for cols in cols:
    datacap.replace(datacap[cols],cap(datacap[cols],0.1,0.9),inplace=True)
print(data.max(),datacap.max(),sep="\n\n")


# In[99]:


#显示所有数据形状
print(data.shape)
#提取通过的数据
datapass=pd.DataFrame.copy(data[data["通过与否"]=="通过"])
print(datapass.shape)
#提取未通过的数据
datafail=pd.DataFrame.copy(data[data["通过与否"]=="未通过"])
print(datafail.shape)
#分组进行缩尾
cols=datapass.describe().columns
for cols in cols:
    datapass.replace(datapass[cols],cap(datapass[cols],0.1,0.9),inplace=True)
    datafail.replace(datafail[cols],cap(datafail[cols],0.1,0.9),inplace=True)


# # 数据分布

# In[107]:


#找到数字相关的指标所在列
data.describe().columns


# In[111]:


#查看数字分布，用直方图绘制，range可以通过quantile函数来排除极端点
for columns in data.describe().columns:
    plt.figure()
    plt.title(columns)
    plt.hist(data[columns],range=(data[columns].quantile(0.1),data[columns].quantile(0.9)),label=columns,alpha=0.7)
    plt.legend()


# # 对比画图

# In[118]:


#分组画图
#企业年龄
for columns in ["年龄" ]:
    plt.figure()
#     plt.title(columns+"分布\n",loc="center",fontsize=18)
    plt.hist(data[data["通过与否"]=="通过"][columns],label="通过",alpha=0.7)
#     plt.figure()
    plt.hist(data[data["通过与否"]=="未通过"][columns],label="未通过",alpha=0.7)
    plt.legend()


# # 导出表格

# In[112]:


data[["年份","通过与否"]].groupby("年份").count().T.to_csv("按年汇总.csv",encoding="gbk")


# # 数据检验

# In[113]:


#均值检验结果
meantest=[]
np.array(meantest)
#中位数检验结果
mediantest=[]
np.array(mediantest)
from scipy import stats as st
#检验
cols=["年龄","储蓄"]
for cols in cols:
    meantest.append
    t,p=st.ttest_ind(datapass[cols].dropna(),datafail[cols].dropna())[0:2]
    meantest.append([cols,t,p])
    t,p=st.median_test(datapass[cols].dropna(),datafail[cols].dropna())[0:2]
    mediantest.append([cols,t,p])


# In[114]:


#显示结果
print(meantest)
print(mediantest)
#python均值检验与中位数检验,P值小于0.05显著，说明两组数据均值与中位数存在差异
#导出结果
pd.DataFrame(meantest).to_csv("meantest.csv",encoding="gbk")
pd.DataFrame(mediantest).to_csv("mediantest.csv",encoding="gbk")   


# In[115]:


data[["通过与否","年龄","储蓄"]].groupby("通过与否").mean()


# # 区间统计

# In[60]:


# 区间统计
classdata=data["年龄"]
classdata=np.array(classdata)
a=pd.cut(classdata,3)
b=pd.cut(classdata,[0,5,10,15,20,25])
print(a)
print(b)
pd.DataFrame(a).to_csv("classa.csv")
pd.DataFrame(b).to_csv("classb.csv")

