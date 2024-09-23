import streamlit as st
import random

st.header("模拟问答测试")

st.markdown("""
> **本页还在开发中，请不要使用本页。**

* 原理：通过简单的排列组合进行快速测试
* 特点：会存储练习历史，使用艾宾浩斯方法进行重复（暂未实现）
* 问题：暂时木有答案
---            
**按R键来随机**
""")

# col1, col2, col3 = st.columns([1,2,1])

illness_list = (
    "青光眼", 
    "白内障", 
    "近视", 
    "视网膜中央静脉阻塞", 
    "远视", 
)

ques_list = (
    "主要特点", 
    "主要症状", 
    "诊断方式",  
    "诊疗思路", 
    "治疗", 
    "治疗注意点", 
    "预防", 
    "并发症", 
    "治疗过程注意点"
)

st.markdown("---")

# with col2:
ill = random.choice(illness_list)
ques = random.choice(ques_list)
st.header(ill+" 的 "+ques)
