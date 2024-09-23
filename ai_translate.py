# AI辅助 翻译训练
# 只需要一个名词、短句、句子、小文章的翻译表格就行

import warnings
warnings.filterwarnings("ignore")

import streamlit as st
import random
import os

from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
# from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

os.environ["OPENAI_API_BASE"] = "https://api.chatanywhere.tech/v1"

col1, col2 = st.columns([2,1])

with col1:
    st.header("模拟即兴口语测试")
with col2:
    button1 = st.button("新话题")

st.markdown("""> 您好！感谢您试用我。由于模型还在开发阶段，以下内容可能需要您注意: 
> * GPT仅根据您输入的文字进行批改和给出范文，它**无法联网搜索也无法知道题目是什么**。所以请务必保持您的输入文字主题明确。
> * GPT4模型调用较慢，请您点击AI批改后耐心等待。
> * AI生成内容仅供参考，这是GPT4的API，Gemini的API不好弄
---
""")

api_in = st.text_input(label="请输入您的api-key")

choose_list = (
    "促进高校毕业生高质量充分就业",
    "保研率屡创新高",
    "美国的中国威胁论",
    "中国计划逐步恢复日本水产品进口",
    "亚运会成功举办",
    "缅甸诈骗园区重大突破",
    "原神、黑神话悟空等游戏实现文化出口",
    "新挖大运河，左右越南国运",
    "中俄关系",
    "中美关系",
    "黎巴嫩电子设备爆炸袭击",
    "巴以冲突",
    "俄乌冲突",
    "日本核污染",
    "美国加息降息",
    "日元贬值",
    "体育饭圈现象",
    "预制菜进校园",
    "石油罐车拉食用油",
    "职业闭店人，帮人卷钱跑路",
    "网红萝卜刀",
    "小孩子玩烟卡（香烟中附赠的）",
    "娱乐圈饭圈乱象",
    "“剩菜盲盒”成为新风潮",
    "公众号短视频为优秀传统文化赋能",
    "杂交水稻新突破",
    "315黑酸菜",
    "娱乐圈综艺倒奶事件",
    "串串房",
    "温州健儿潘展乐游泳夺冠",
    "郑钦文网球单打金牌",
    "跳水金牌全红婵",
    "莎头组合乒乓夺冠",
    "奥运会射击运动员随手获银牌",
    "14天单方面免签之阳谋",
    "哈尔滨冰雪旅游大火",
    "政府大院开放让农民晒粮",
    "中国提出月壤反应取水法",
    "石油人民币结算",
    "人民币国际化",
    "国产大飞机C919完成首飞",
    "国防重要性",
    "一带一路",
    "中美贸易战",
    "菲律宾频繁扰乱南海",
    "台独、港独、疆独分子被打击判刑",
    "无条件退款",
    "外卖、滴滴到医生：人被算法压榨",
    "保护消费者权益",
    "扶贫：授人以鱼不如授人以渔",
    "旅游经济",
    "人口老龄化",
    "生育率持续走低",
    "房地产暴雷",
    "共享自习室",
    "家政、电竞进入本科专业目录",
    "中国电动汽车领先全球",
    "华为5G",
    "社会普遍焦虑，是谁在制造焦虑",
    "大学生进基层",
    "芯片卡脖子",
    "人工智能",
    "AI造假",
    "罗森塔尔效应",
    "当今互联网环境下的社会舆论",
    "短视频兴起",
    "年轻人热衷citywalk",
    "医美乱象",
    "中小学减负：“双减”",
    "内卷",
    "全民抑郁率上升",
    "知识付费",
    "线上教育、B站大学",
    "胖东来员工高福利政策获大收益",
    "“青椒”上课火出圈",
    "淄博烧烤大火",
    "“博物馆游玩”文旅新趋势",
    "义乌小商品连接世界40年",
    "《繁花》",
    "气温反复无常，极端天气增加",
    "黄河治理卓有成效",
    "中国太空空间站实验室正式运行",
    "南极考察站“秦岭站”正式启用",
    "元宇宙",
    "奥运会美国钻空子使用兴奋剂类药物",
    "学生虐猫",
    "从严治党，从严治军",
    "乡村振兴",
    "领导下基层",
    "始终保持党的团结统一",
    "绿水青山就是金山银山",
    "扫黑除恶",
    "全国反腐",
    "林草年碳汇量超过12亿吨二氧化碳当量，居世界首位，碳中和目标将近",
    "中国共产党成立103周年。",
    "国家电器千亿补贴",
    "可控核聚变",
    "中国电车领先世界",
    "在黄埔军校建校100周年暨黄埔军校同学会成立40周年",
    "三明医改",
    "科研与医疗",
    "新医科教育改革",
    "规培制度",
    "专培制度",
    "住培制度",
    "新冠疫情对医疗的影响",
    "开放高端外资私人医疗",
    "医生多点执业",
    "医生收红包",
    "揭榜挂帅科研模式",
    "中国科学院自动化研究团队与其他单位合作设计了新型类脑神经形态系统级芯片Speck，展示了神经形态计算在融合高抽象层次大脑机制时的天然优势，相关研究日前在线发表于国际学术期刊《自然·通讯》。",
    "体制内降薪",
    "外籍院士",
    "学术造假",
    "减肥药爆火",
    "司美格鲁肽",
    "以岭药业连花清瘟治新冠",
    "医闹，李晟医生",
    "医生辞职做副业",
    "韩国医生大罢工",
    "学术打假产业链",
    "鼓励基层医生副业兼职",
    "医护外包，劳务派遣",
    "医疗反腐",
    "集采",
    "仿制药（我不是药神）",
    "AI赋能医疗",
    "家庭共济基金",
    "医疗学历内卷化",
    "医生越老越吃香的论断",
)

if button1:
    st.session_state.problem_now = random.choice(choose_list)

st.markdown("---")

# with col2:
if "problem_now" not in st.session_state:
    st.session_state.problem_now = random.choice(choose_list)

problem = st.session_state.problem_now

st.markdown("##### 请谈一谈你对")
st.header(problem)
st.markdown("##### 的看法")

st.markdown("---")

template_trans_teach1 = """
You are a very skilled English teacher, and now your student has written an article. Please read this article and provide suggestions for revision. Your suggestion should be written in Chinese and include at least the following content:

1. Simply retell the content of the article
2. Rate this article with a maximum score of 10 and a minimum score of 0, and roughly explain why
3. Describe whether there are any errors or grammatical errors in the wording of the article
4. Is there any logical problem with the text in the article
5. Where can I make modifications to the article if I want to make it better

Article written by the student:{user_question}
"""

template_trans_teach2 = """
You are a very skilled English teacher, and now your student has written an argumentative essay. Please read this article and polish it to make it more coherent, logically rigorous, and turn it into a better English article. Provide the revised English article and briefly list the areas that have been modified

Article written by the student:{user_question}
"""


txt = st.text_area(height=300, label="请输入你的回答，建议语音输入")
if_pigai = st.button("AI批改")
if if_pigai:
    st.markdown("已收到回答，AI批改中...")
    st.markdown("---")
    st.markdown("AI评价: ")

    llm = ChatOpenAI(model="gpt-4o-2024-08-06", api_key=api_in)

    prompt_tea1 = ChatPromptTemplate.from_template(template_trans_teach1)
    chain_tea1 = prompt_tea1 | llm | StrOutputParser()
    st.write_stream(
        chain_tea1.stream({
            "user_question": txt
        })
    )

    st.markdown("  ")
    st.markdown("---")
    st.markdown("AI修改后的范文: ")

    prompt_tea2 = ChatPromptTemplate.from_template(template_trans_teach2)
    chain_tea2 = prompt_tea2 | llm | StrOutputParser()
    st.write_stream(
        chain_tea2.stream({
            "user_question": txt
        })
    )

    st.markdown("---")
    if st.button("OK，我知道了，下一题"):
        st.session_state.problem_now = random.choice(choose_list)
        
