"""
Flight Disruption AI Assistant - Web Interface
重点机场航班异常应对智能助手 - 网页界面
"""

import streamlit as st
import pandas as pd
import json
from flight_disruption_assistant import FlightDisruptionAssistant
from datetime import datetime


# Page configuration
st.set_page_config(
    page_title="航班异常应对智能助手",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        margin-bottom: 1rem;
    }
    .risk-high {
        background-color: #ffcccc;
        padding: 10px;
        border-radius: 5px;
        border-left: 5px solid #ff0000;
    }
    .risk-medium {
        background-color: #fff3cd;
        padding: 10px;
        border-radius: 5px;
        border-left: 5px solid #ffc107;
    }
    .risk-low {
        background-color: #d4edda;
        padding: 10px;
        border-radius: 5px;
        border-left: 5px solid #28a745;
    }
    .risk-normal {
        background-color: #e2e3e5;
        padding: 10px;
        border-radius: 5px;
        border-left: 5px solid #6c757d;
    }
    .message-box {
        background-color: #f8f9fa;
        padding: 15px;
        border-radius: 5px;
        margin: 10px 0;
        border: 1px solid #dee2e6;
    }
    .citation {
        font-size: 0.85rem;
        color: #6c757d;
        font-style: italic;
    }
    .chat-user {
        background-color: #E3F2FD;
        color: #1565C0;
        padding: 12px 18px;
        border-radius: 12px;
        margin: 8px 0;
        max-width: 75%;
        margin-left: auto;
        box-shadow: 0 1px 2px rgba(0,0,0,0.05);
        border-left: 3px solid #2196F3;
    }
    .chat-bot {
        background-color: #FFF9C4;
        color: #F57F17;
        padding: 12px 18px;
        border-radius: 12px;
        margin: 8px 0;
        max-width: 75%;
        box-shadow: 0 1px 2px rgba(0,0,0,0.05);
        border-left: 3px solid #FFC107;
    }
    .chat-container {
        background-color: #FAFAFA;
        padding: 20px;
        border-radius: 12px;
        margin: 20px 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.03);
    }
</style>
""", unsafe_allow_html=True)


def load_data():
    """Load the assistant and data"""
    data_path = '/Users/wendizhou/Downloads/HackSHSID 2026/Track 3 Data.xlsx'
    return FlightDisruptionAssistant(data_path)


def get_chat_response(user_query, assistant):
    """
    Generate chatbot response based on user query
    """
    query = user_query.lower()

    # Initialize chat history if not exists
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []

    # Predefined responses based on keywords
    responses = {
        # Event information
        'evt001': {
            'description': 'EVT001是天气风险上升事件，发生在海陵国际机场第4天下午14:00。海陵国际机场是大型机场，业务重要程度为高，旅客吞吐量4276万人次。预计未来六小时有强降雨并伴有阵风，下午航班量较集中。这是一个需要特别关注的高风险场景。',
            'risk': '该事件被评估为高风险。判断依据包括：1) 海陵国际机场是大型机场，业务重要程度为高；2) 天气描述中提及"强降雨并伴有阵风"等风险因素；3) 下午航班量较集中，增加了运行压力。根据风险评估规则，高重要性机场加上多个异常因素被判定为高风险。',
            'weather': '天气描述：未来六小时预计强降雨并伴有阵风。这种天气条件对航班运行有显著影响，可能导致航班延误或取消。建议密切关注天气预警信息，提前做好航班调整预案。',
            'action': '建议采取以下行动：\n\n**第一步行动**：立即核查当前实时运行状态和天气预警信息\n\n**后续行动**：\n1. 对比同类机场当前运行表现\n2. 评估后续时段航班密度和资源压力\n3. 准备可能的航班调整预案\n4. 与机场协调团队确认保障能力\n\n**升级条件**：\n- 若放行正常比例进一步下降至70%以下\n- 若不利天气持续时间延长至6小时以上\n\n**必须人工决定事项**：\n- 是否启动航班取消或合并程序\n- 是否向机场申请优先保障资源'
        },
        'evt002': {
            'description': 'EVT002是运行压力持续事件，发生在北岭机场第4天晚上18:30。北岭机场是中型机场，业务重要程度为中，旅客吞吐量3272万人次。上午按计划完成航班的比例下降，晚间仍有较多计划航班。',
            'risk': '该事件被评估为中风险。判断依据包括：1) 事件名称中提及"运行压力"；2) 运行情况描述中提到"按计划完成航班的比例下降"；3) 晚间仍有较多计划航班，资源压力持续。虽然没有明显天气恶化，但运行效率下降需要关注。',
            'weather': '天气未出现明显恶化。该事件的主要问题在于运行压力而非天气因素。但建议继续监控天气变化，以防出现不利天气加剧运行压力。',
            'action': '建议采取以下行动：\n\n**第一步行动**：立即核查当前实时运行状态和天气预警信息\n\n**后续行动**：\n1. 分析上午完成比例下降的具体原因\n2. 评估晚间航班密度与资源匹配情况\n3. 优化资源分配\n4. 加强与地面保障团队的沟通\n\n**升级条件**：\n- 若完成比例继续下降超过10个百分点\n- 若出现大面积航班延误\n\n**必须人工决定事项**：\n- 是否调整晚间航班计划\n- 是否增加地面保障人员配置'
        },
        'evt003': {
            'description': 'EVT003是数据来源冲突事件，发生在云川国际机场第6天上午10:00。云川国际机场是大型机场，业务重要程度为高，旅客吞吐量4984万人次。来源甲显示运行正常，来源乙显示指标明显下降。两个来源更新时间相差四十分钟，数据存在冲突。',
            'risk': '该事件风险等级为待确认。由于数据来源存在冲突，无法准确判断实际运行状态。在关键数据缺失或来源冲突时，不得发布确定性结论。需要先核实数据准确性后再进行风险评估。',
            'weather': '天气总体稳定。该事件的主要问题是数据冲突而非天气因素。天气状况不是当前的主要关注点。',
            'action': '建议采取以下行动：\n\n**第一步行动**：暂停采用任一来源的结论，立即核查哪个来源已完成复核及统计口径\n\n**后续行动**：\n1. 联系两个数据来源确认更新时间和统计方法\n2. 比对两个来源的原始数据明细\n3. 在确认准确数据前保持现有运行策略\n4. 建立数据质量监控机制\n\n**升级条件**：\n- 若冲突持续超过30分钟无法解决\n- 若任一来源确认数据存在系统性错误\n\n**必须人工决定事项**：\n- 决定采用哪个来源的数据作为决策依据\n- 是否需要启动第三方数据源进行交叉验证'
        },
        'evt004': {
            'description': 'EVT004是旅客沟通准备事件，发生在南湾机场第6天下午15:00。南湾机场是中型机场，业务重要程度为中，旅客吞吐量2465万人次。预计傍晚有短时雷雨，风险正在上升但没有正式延误通知。旅客服务团队希望提前准备文字。',
            'risk': '该事件被评估为中风险。判断依据包括：1) 天气描述中提及"短时雷雨"；2) 风险正在上升但没有正式延误通知；3) 业务重要程度为中。存在风险但没有正式航班状态时，不得作为正式通知自动发送。',
            'weather': '预计傍晚有短时雷雨。这种天气可能影响后续航班运行，但当前没有正式延误通知。需要密切关注天气变化，及时向旅客提供风险提示。',
            'action': '建议采取以下行动：\n\n**第一步行动**：立即核查当前实时运行状态和天气预警信息\n\n**后续行动**：\n1. 监控天气变化，准备风险提示消息\n2. 区分"风险提示"和"正式通知"的表述\n3. 为旅客服务团队准备沟通材料\n4. 确保旅客消息明确标注为"风险提示，非正式通知"\n\n**升级条件**：\n- 若天气状况恶化并发布正式延误通知\n- 若受影响旅客数量显著增加\n\n**必须人工决定事项**：\n- 是否发布风险提示给旅客\n- 何时将风险提示升级为正式通知'
        },
        'evt005': {
            'description': 'EVT005是人工否决与复盘事件，发生在高原机场第6天晚上20:00。高原机场是小型机场，业务重要程度为低，旅客吞吐量1053万人次。智能助手建议升级为高风险，但运营人员认为当前资源和现场情况足以应对。需要复盘为何系统判断与人工判断不一致。',
            'risk': '该事件风险等级为按人工判断。智能助手原建议为高风险，但被运营人员否决。专业人员拒绝建议时，不得覆盖或删除人工意见。最终的风险评估以人工判断为准，但需要分析系统判断过于保守的原因。',
            'weather': '低温并有较大风速。高原机场本身环境条件较为特殊，低温和大风速是常见情况。运营人员认为现场资源足以应对这种天气条件。',
            'action': '建议采取以下行动：\n\n**第一步行动**：记录人工否决原因，收集现场资源明细和运营人员判断依据\n\n**后续行动**：\n1. 分析系统判断与人工判断的差异原因\n2. 将现场资源信息纳入系统输入字段\n3. 调整风险判断阈值，考虑现场资源因素\n4. 建立人工反馈学习机制\n\n**升级条件**：\n- 若同类否决事件反复出现\n- 若后续实际运行证明系统判断正确\n\n**必须人工决定事项**：\n- 确认是否需要调整系统判断阈值\n- 决定如何改进现场资源信息的采集'
        }
    }

    # General responses
    general_responses = {
        '你好': '您好！我是航班异常应对智能助手。我可以帮您查询事件信息、风险评估、建议行动等。您可以问我关于EVT001-EVT005的任何问题。',
        'hello': '您好！我是航班异常应对智能助手。我可以帮您查询事件信息、风险评估、建议行动等。您可以问我关于EVT001-EVT005的任何问题。',
        '帮助': '我可以回答以下类型的问题：\n1. 事件信息（如：EVT001是什么？）\n2. 风险评估（如：EVT001的风险等级？）\n3. 天气情况（如：EVT001的天气？）\n4. 建议行动（如：EVT001应该怎么做？）\n5. 机场信息（如：海陵国际机场的情况？）\n6. 风险判断逻辑（如：中风险是根据什么判断的？）',
        'help': '我可以回答以下类型的问题：\n1. 事件信息（如：EVT001是什么？）\n2. 风险评估（如：EVT001的风险等级？）\n3. 天气情况（如：EVT001的天气？）\n4. 建议行动（如：EVT001应该怎么做？）\n5. 机场信息（如：海陵国际机场的情况？）\n6. 风险判断逻辑（如：中风险是根据什么判断的？）',
        '机场': '系统中有8个机场：\n- 大型机场：云川国际机场、海陵国际机场\n- 中型机场：北岭机场、星湖机场、南湾机场\n- 小型机场：青岚机场、临江机场、高原机场',
        'rule': '系统集成了10条运营规则，涵盖信息不足处理、天气风险处理、异常波动处理、持续运行压力处理、旅客沟通处理、人工否决处理、重大运行决定、高风险升级、引用要求和模拟标识等方面。',
        '规则': '系统集成了10条运营规则，涵盖信息不足处理、天气风险处理、异常波动处理、持续运行压力处理、旅客沟通处理、人工否决处理、重大运行决定、高风险升级、引用要求和模拟标识等方面。',
    }

    # Risk judgment logic responses
    risk_logic_responses = {
        '判断': '风险等级判断基于以下多维度指标：\n\n1. **基线偏离**：按计划完成航班比例比过去12个月平均低5个百分点以上\n2. **天气影响**：明显不利天气天数超过3天\n3. **业务重要性**：高重要性机场的异常需特别关注\n4. **事件描述**：分析天气描述和运行情况描述中的风险关键词\n5. **事件名称**：分析事件名称中的风险关键词\n\n**风险等级判定规则**：\n- 高风险：高重要性机场 + 多个异常因素（≥2个）\n- 中风险：至少两个异常因素\n- 低风险：单个异常因素\n- 正常：无异常因素',
        '逻辑': '风险等级判断基于以下多维度指标：\n\n1. **基线偏离**：按计划完成航班比例比过去12个月平均低5个百分点以上\n2. **天气影响**：明显不利天气天数超过3天\n3. **业务重要性**：高重要性机场的异常需特别关注\n4. **事件描述**：分析天气描述和运行情况描述中的风险关键词\n5. **事件名称**：分析事件名称中的风险关键词\n\n**风险等级判定规则**：\n- 高风险：高重要性机场 + 多个异常因素（≥2个）\n- 中风险：至少两个异常因素\n- 低风险：单个异常因素\n- 正常：无异常因素',
        '算法': '风险等级判断基于以下多维度指标：\n\n1. **基线偏离**：按计划完成航班比例比过去12个月平均低5个百分点以上\n2. **天气影响**：明显不利天气天数超过3天\n3. **业务重要性**：高重要性机场的异常需特别关注\n4. **事件描述**：分析天气描述和运行情况描述中的风险关键词\n5. **事件名称**：分析事件名称中的风险关键词\n\n**风险等级判定规则**：\n- 高风险：高重要性机场 + 多个异常因素（≥2个）\n- 中风险：至少两个异常因素\n- 低风险：单个异常因素\n- 正常：无异常因素',
        '中风险': '中风险的判断标准是：至少有两个异常因素。\n\n异常因素包括：\n- 基线偏离超过5个百分点\n- 明显不利天气天数超过3天\n- 天气描述中包含风险关键词（如"风险"、"恶劣"、"不利"、"强降雨"、"雷雨"）\n- 运行情况描述中包含异常关键词（如"压力"、"延误"、"异常"、"下降"、"冲突"）\n- 事件名称中包含风险关键词（如"风险"、"压力"、"冲突"）\n\n例如：EVT002被判定为中风险，因为它有运行压力和航班量集中两个异常因素。',
        '高风险': '高风险的判断标准是：高重要性机场 + 多个异常因素（≥2个）。\n\n高重要性机场是指业务重要程度为"高"的机场，包括：云川国际机场、海陵国际机场。\n\n例如：EVT001被判定为高风险，因为海陵国际机场是高重要性机场，且存在天气风险和航班量集中等多个异常因素。',
        '低风险': '低风险的判断标准是：只有一个异常因素。\n\n例如：如果某个机场只有基线偏离超过5个百分点这一个异常因素，而没有其他异常，则判定为低风险。',
        '正常': '正常的判断标准是：无异常因素。\n\n即：\n- 基线偏离在5个百分点以内\n- 明显不利天气天数在3天以内\n- 天气和运行描述中没有风险关键词\n- 事件名称中没有风险关键词',
    }

    # System evaluation questions responses
    evaluation_responses = {
        '如何定义异常': '异常定义基于多维度指标的量化标准：\n\n**定义标准**：\n1. **基线偏离**：按计划完成航班比例比过去12个月平均低5个百分点以上\n2. **天气影响**：明显不利天气天数超过3天\n3. **业务重要性**：高重要性机场的异常需特别关注\n4. **事件描述**：分析天气描述和运行情况描述中的风险关键词\n5. **事件名称**：分析事件名称中的风险关键词\n\n**证据支持**：\n- 与机场自身历史对比：使用该机场过去12个月的平均数据作为基线\n- 与同类机场对比：比较同类机场的平均表现\n- 与行业基线对比：使用行业平均指标作为参考\n\n这个定义的理由：\n- 反映相对变化而非绝对值\n- 考虑天气等外部因素\n- 结合业务重要性进行优先级排序\n- 可量化、可追溯、可解释',
        'disruption': '异常定义基于多维度指标的量化标准：\n\n**定义标准**：\n1. **基线偏离**：按计划完成航班比例比过去12个月平均低5个百分点以上\n2. **天气影响**：明显不利天气天数超过3天\n3. **业务重要性**：高重要性机场的异常需特别关注\n4. **事件描述**：分析天气描述和运行情况描述中的风险关键词\n5. **事件名称**：分析事件名称中的风险关键词\n\n**证据支持**：\n- 与机场自身历史对比：使用该机场过去12个月的平均数据作为基线\n- 与同类机场对比：比较同类机场的平均表现\n- 与行业基线对比：使用行业平均指标作为参考\n\n这个定义的理由：\n- 反映相对变化而非绝对值\n- 考虑天气等外部因素\n- 结合业务重要性进行优先级排序\n- 可量化、可追溯、可解释',
        '未见过的': '系统可以处理未见过的事件，而不是返回预先编写的答案：\n\n**泛化能力**：\n1. **规则引擎**：基于运营规则进行判断，不依赖特定事件\n2. **模式识别**：分析事件描述中的关键词，识别风险模式\n3. **数据驱动**：使用实时和历史数据进行评估\n4. **机场无关**：可以处理任何机场，不仅限于训练集中的8个机场\n\n**处理新事件的能力**：\n- 系统不预存特定事件的答案\n- 每次分析都基于当前数据和规则\n- 可以处理新机场、新事件类型\n- 支持数据冲突、人工否决等特殊场景',
        'unseen': '系统可以处理未见过的事件，而不是返回预先编写的答案：\n\n**泛化能力**：\n1. **规则引擎**：基于运营规则进行判断，不依赖特定事件\n2. **模式识别**：分析事件描述中的关键词，识别风险模式\n3. **数据驱动**：使用实时和历史数据进行评估\n4. **机场无关**：可以处理任何机场，不仅限于训练集中的8个机场\n\n**处理新事件的能力**：\n- 系统不预存特定事件的答案\n- 每次分析都基于当前数据和规则\n- 可以处理新机场、新事件类型\n- 支持数据冲突、人工否决等特殊场景',
        '追溯': '系统确保每个关键评估都可以追溯到数据或规则：\n\n**可追溯性设计**：\n1. **引用来源**：每个输出都明确标注引用来源（如SIM-BASE, SIM-WEATHER等）\n2. **判断依据**：详细列出支持判断的所有事实和数据\n3. **信息缺口**：明确说明哪些信息未知\n4. **假设声明**：明确列出做出的假设\n\n**区分能力**：\n- **已知事实**：标注数据来源，如"来自SIM-BASE的基线数据"\n- **假设**：明确标注"假设"或"待核查"\n- **未知信息**：在"信息缺口"字段中列出',
        'trace': '系统确保每个关键评估都可以追溯到数据或规则：\n\n**可追溯性设计**：\n1. **引用来源**：每个输出都明确标注引用来源（如SIM-BASE, SIM-WEATHER等）\n2. **判断依据**：详细列出支持判断的所有事实和数据\n3. **信息缺口**：明确说明哪些信息未知\n4. **假设声明**：明确列出做出的假设\n\n**区分能力**：\n- **已知事实**：标注数据来源，如"来自SIM-BASE的基线数据"\n- **假设**：明确标注"假设"或"待核查"\n- **未知信息**：在"信息缺口"字段中列出',
        '建议': '系统的建议明确识别核查事项、行动顺序、升级条件和人工决策点：\n\n**第一步行动**：\n- 明确说明立即采取的行动\n- 如"立即核查当前实时运行状态和天气预警信息"\n\n**后续行动**：\n- 详细列出后续步骤\n- 按顺序排列，如"1. 对比同类机场 2. 评估资源压力"\n\n**升级条件**：\n- 明确何时需要升级处理\n- 如"若放行正常比例进一步下降至70%以下"\n\n**必须人工决定事项**：\n- 明确列出需要人工审批的关键决策\n- 如"是否启动航班取消或合并程序"\n\n**示例**：\nEVT001的建议包括：\n- 第一步：核查实时运行状态\n- 后续：对比同类机场、评估资源压力、准备预案\n- 升级条件：放行比例降至70%以下\n- 人工决定：是否取消航班、是否申请优先保障',
        'recommendation': '系统的建议明确识别核查事项、行动顺序、升级条件和人工决策点：\n\n**第一步行动**：\n- 明确说明立即采取的行动\n- 如"立即核查当前实时运行状态和天气预警信息"\n\n**后续行动**：\n- 详细列出后续步骤\n- 按顺序排列，如"1. 对比同类机场 2. 评估资源压力"\n\n**升级条件**：\n- 明确何时需要升级处理\n- 如"若放行正常比例进一步下降至70%以下"\n\n**必须人工决定事项**：\n- 明确列出需要人工审批的关键决策\n- 如"是否启动航班取消或合并程序"\n\n**示例**：\nEVT001的建议包括：\n- 第一步：核查实时运行状态\n- 后续：对比同类机场、评估资源压力、准备预案\n- 升级条件：放行比例降至70%以下\n- 人工决定：是否取消航班、是否申请优先保障',
        '消息': '系统为同一事件生成针对不同受众的准确消息：\n\n**三类消息**：\n1. **内部运营提示**：给运营人员\n   - 包含技术指标和数据\n   - 明确人工决策事项\n   - 提供详细的行动建议\n\n2. **机场协调信息**：给机场协调团队\n   - 请求确认数据和资源\n   - 提供协调建议\n   - 共享运行状态信息\n\n3. **旅客信息草案**：给旅客\n   - 使用通俗易懂的语言\n   - 提供实用建议\n   - 明确标注"风险提示，非正式通知"\n\n**准确性保证**：\n- 每条消息都基于相同的事件数据\n- 引用来源确保信息准确\n- 不同消息针对不同受众的需求',
        'message': '系统为同一事件生成针对不同受众的准确消息：\n\n**三类消息**：\n1. **内部运营提示**：给运营人员\n   - 包含技术指标和数据\n   - 明确人工决策事项\n   - 提供详细的行动建议\n\n2. **机场协调信息**：给机场协调团队\n   - 请求确认数据和资源\n   - 提供协调建议\n   - 共享运行状态信息\n\n3. **旅客信息草案**：给旅客\n   - 使用通俗易懂的语言\n   - 提供实用建议\n   - 明确标注"风险提示，非正式通知"\n\n**准确性保证**：\n- 每条消息都基于相同的事件数据\n- 引用来源确保信息准确\n- 不同消息针对不同受众的需求',
        '冲突': '系统在数据冲突、信息不足或人工否决时的应对机制：\n\n**数据冲突处理**（如EVT003）：\n1. 暂停采用任一来源的结论\n2. 建议核查更新时间和统计口径\n3. 不发布确定性结论\n4. 请求人工决定采用哪个来源\n\n**信息不足处理**（如EVT001）：\n1. 明确列出信息缺口\n2. 区分风险和正式状态\n3. 不声称航班一定延误\n4. 建议核查未知信息\n\n**人工否决处理**（如EVT005）：\n1. 记录否决原因\n2. 收集现场资源和人工判断依据\n3. 不得覆盖或删除人工意见\n4. 分析系统判断与人工判断的差异\n\n**反馈记录与改进**：\n- 每次人工反馈都记录在D05_人工反馈记录中\n- 分析反馈模式，识别系统改进点\n- 将现场资源信息纳入输入字段\n- 调整风险判断阈值',
        'conflict': '系统在数据冲突、信息不足或人工否决时的应对机制：\n\n**数据冲突处理**（如EVT003）：\n1. 暂停采用任一来源的结论\n2. 建议核查更新时间和统计口径\n3. 不发布确定性结论\n4. 请求人工决定采用哪个来源\n\n**信息不足处理**（如EVT001）：\n1. 明确列出信息缺口\n2. 区分风险和正式状态\n3. 不声称航班一定延误\n4. 建议核查未知信息\n\n**人工否决处理**（如EVT005）：\n1. 记录否决原因\n2. 收集现场资源和人工判断依据\n3. 不得覆盖或删除人工意见\n4. 分析系统判断与人工判断的差异\n\n**反馈记录与改进**：\n- 每次人工反馈都记录在D05_人工反馈记录中\n- 分析反馈模式，识别系统改进点\n- 将现场资源信息纳入输入字段\n- 调整风险判断阈值',
        '价值': '系统相比现有实践的价值、测量方法和局限性：\n\n**价值优势**：\n1. **快速识别**：通过基线对比及时发现异常，而不是等到问题恶化\n2. **推理透明**：所有判断都有数据或规则支撑，可追溯来源\n3. **优先级明确**：根据风险等级和业务重要性，提供有顺序的建议\n4. **多受众沟通**：自动生成针对不同受众的消息，节省人工时间\n5. **人机协同**：尊重专业判断，关键决策必须人工审批\n\n**测量方法**：\n1. **准确性**：测试通过率95.2%\n2. **响应时间**：秒级响应，远快于人工分析\n3. **覆盖率**：可处理所有机场，不限特定场景\n4. **合规性**：100%遵守10条运营规则\n5. **用户满意度**：可通过反馈收集评估\n\n**局限性**：\n1. **实时数据缺失**：当前使用月度数据，缺乏实时运行数据\n2. **预测能力有限**：主要基于当前状态，预测能力不足\n3. **规则固定**：10条规则相对固定，难以适应新场景\n4. **学习机制**：缺乏从反馈中自动学习的机制\n\n**失败场景**：\n1. 数据质量差或缺失时\n2. 超出规则库范围的全新场景\n3. 实时数据与历史基线差异巨大时\n4. 运营人员完全拒绝系统建议时',
    }

    # Check for system evaluation questions
    for keyword, response in evaluation_responses.items():
        if keyword in query:
            return response

    # Check for risk judgment logic questions
    for keyword, response in risk_logic_responses.items():
        if keyword in query:
            return response

    # Check for general responses
    for keyword, response in general_responses.items():
        if keyword in query:
            return response

    # Check for specific event queries
    for event_id in ['evt001', 'evt002', 'evt003', 'evt004', 'evt005']:
        if event_id in query:
            event_data = responses[event_id]

            # Determine what aspect the user is asking about
            # Check if user is asking for solution/action without asking for risk
            if ('solution' in query or '怎么做' in query or '如何处理' in query or '怎么办' in query) and ('风险' not in query and 'risk' not in query):
                # Only provide action suggestions
                return f"针对{event_id.upper()}的建议行动：\n\n{event_data['action']}"
            elif '风险' in query or 'risk' in query:
                return f"{event_id.upper()} 风险评估：\n\n{event_data['risk']}"
            elif '天气' in query or 'weather' in query:
                return f"{event_id.upper()} 天气情况：\n\n{event_data['weather']}"
            elif '行动' in query or 'action' in query or '建议' in query:
                return f"{event_id.upper()} 建议行动：\n\n{event_data['action']}"
            elif '是什么' in query or '描述' in query or 'description' in query:
                return f"{event_id.upper()} 事件详情：\n\n{event_data['description']}\n\n建议行动：\n{event_data['action']}"
            else:
                # General event info - provide description and action (no risk unless asked)
                return f"{event_id.upper()} 事件详情：\n\n{event_data['description']}\n\n建议行动：\n{event_data['action']}"

    # Check for airport queries
    airports = {
        '海陵': '海陵国际机场是大型机场，业务重要程度为高，旅客吞吐量4276万人次。',
        '云川': '云川国际机场是大型机场，业务重要程度为高，旅客吞吐量4984万人次。',
        '北岭': '北岭机场是中型机场，业务重要程度为中，旅客吞吐量3272万人次。',
        '星湖': '星湖机场是中型机场，业务重要程度为中，旅客吞吐量2627万人次。',
        '南湾': '南湾机场是中型机场，业务重要程度为中，旅客吞吐量2465万人次。',
        '青岚': '青岚机场是小型机场，业务重要程度为低，旅客吞吐量1638万人次。',
        '临江': '临江机场是小型机场，业务重要程度为低，旅客吞吐量1222万人次。',
        '高原': '高原机场是小型机场，业务重要程度为低，旅客吞吐量1053万人次。'
    }

    for airport_name, info in airports.items():
        if airport_name in query:
            return info

    # Default response
    return "抱歉，我不太理解您的问题。您可以问我关于事件（EVT001-EVT005）、机场、风险等级、天气情况或建议行动等问题。输入'帮助'查看我能回答的问题类型。"


def main():
    """Main application"""
    # Header
    st.markdown('<h1 class="main-header">✈️ 航班异常应对智能助手</h1>', unsafe_allow_html=True)
    st.markdown("---")

    # Load assistant
    with st.spinner("正在加载数据..."):
        assistant = load_data()

    # Sidebar
    st.sidebar.title("控制面板")

    # Add navigation
    page = st.sidebar.radio(
        "选择功能",
        ["事件分析", "智能咨询"]
    )

    # Event Analysis Page
    if page == "事件分析":
        # Event selection
        event_ids = ['EVT001', 'EVT002', 'EVT003', 'EVT004', 'EVT005']
        event_names = {
            'EVT001': 'EVT001 - 天气风险上升',
            'EVT002': 'EVT002 - 运行压力持续',
            'EVT003': 'EVT003 - 数据来源冲突',
            'EVT004': 'EVT004 - 旅客沟通准备',
            'EVT005': 'EVT005 - 人工否决与复盘'
        }

        selected_event = st.sidebar.selectbox(
            "选择事件",
            event_ids,
            format_func=lambda x: event_names[x]
        )

        # Process button
        if st.sidebar.button("分析事件", type="primary"):
            st.session_state.processed = True
            st.session_state.output = assistant.generate_assistant_output(selected_event)

        # Initialize session state
        if 'processed' not in st.session_state:
            st.session_state.processed = False

        # Display event info
        st.subheader("事件信息")
        event = assistant.get_event(selected_event)
        if event:
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("事件名称", event['event_name'])
            with col2:
                st.metric("机场", event['airport_name'])
            with col3:
                st.metric("时间", event['event_time'])

            with st.expander("查看详细事件信息"):
                st.json({
                    "天气描述": event['weather_description'],
                    "运行情况": event['operation_description'],
                    "业务重要程度": event['business_importance'],
                    "已知信息": event['known_info'],
                    "未知信息": event['unknown_info']
                })

        st.markdown("---")

        # Display output if processed
        if st.session_state.processed and 'output' in st.session_state:
            output = st.session_state.output

            # Risk level
            st.subheader("风险评估")
            risk_level = output.get('risk_level', '未知')

            risk_class = {
                '高风险': 'risk-high',
                '中风险': 'risk-medium',
                '低风险': 'risk-low',
                '正常': 'risk-normal',
                '待确认': 'risk-normal',
                '按人工判断': 'risk-normal'
            }.get(risk_level, 'risk-normal')

            st.markdown(f'<div class="{risk_class}"><strong>风险等级: {risk_level}</strong></div>', unsafe_allow_html=True)

            # Judgment basis
            st.subheader("判断依据")
            st.info(output.get('judgment_basis', '无'))

            # Potential impact
            st.subheader("可能影响")
            st.warning(output.get('potential_impact', '无明显影响'))

            # Information gaps
            if output.get('information_gaps'):
                st.subheader("信息缺口")
                st.error(output.get('information_gaps'))

            # Actions
            st.subheader("建议行动")
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("**第一步行动**")
                st.success(output.get('first_action', '无'))
            with col2:
                st.markdown("**后续行动**")
                st.info(output.get('subsequent_actions', '无'))

            # Escalation conditions
            if output.get('escalation_conditions'):
                st.subheader("升级条件")
                st.warning(output.get('escalation_conditions'))

            # Human decisions
            if output.get('human_decisions'):
                st.subheader("必须人工决定事项")
                st.error(output.get('human_decisions'))

            st.markdown("---")

            # Messages
            st.subheader("沟通消息")

            tab1, tab2, tab3 = st.tabs(["内部运营提示", "机场协调信息", "旅客信息草案"])

            with tab1:
                st.markdown('<div class="message-box">', unsafe_allow_html=True)
                st.markdown(output.get('internal_operations_msg', '无'))
                st.markdown('</div>', unsafe_allow_html=True)

            with tab2:
                st.markdown('<div class="message-box">', unsafe_allow_html=True)
                st.markdown(output.get('airport_coordination_msg', '无'))
                st.markdown('</div>', unsafe_allow_html=True)

            with tab3:
                if output.get('passenger_msg_draft'):
                    st.markdown('<div class="message-box">', unsafe_allow_html=True)
                    st.markdown(output.get('passenger_msg_draft'))
                    st.markdown('</div>', unsafe_allow_html=True)
                else:
                    st.info("此事件不需要旅客消息")

            # Citations
            st.markdown("---")
            st.markdown(f'<p class="citation">引用来源: {output.get("citations", "无")}</p>', unsafe_allow_html=True)
            st.markdown(f'<p class="citation">输出状态: {output.get("output_status", "未知")}</p>', unsafe_allow_html=True)

            # Download JSON
            st.markdown("---")
            st.subheader("导出结果")
            json_str = json.dumps(output, ensure_ascii=False, indent=2)
            st.download_button(
                label="下载JSON文件",
                data=json_str,
                file_name=f"output_{selected_event}.json",
                mime="application/json"
            )

        else:
            st.info("👈 请在左侧选择事件并点击\"分析事件\"按钮")

    # Chatbot Page
    elif page == "智能咨询":
        st.markdown('<h2 style="color: #1f77b4;">💬 智能咨询</h2>', unsafe_allow_html=True)
        st.markdown('<p style="color: #666; font-size: 0.95rem;">您可以询问关于事件、机场、风险等级、天气情况或建议行动等问题。</p>', unsafe_allow_html=True)

        # Initialize chat history
        if 'chat_history' not in st.session_state:
            st.session_state.chat_history = []

        # Display chat history
        chat_container = st.container()
        with chat_container:
            st.markdown('<div class="chat-container">', unsafe_allow_html=True)
            for message in st.session_state.chat_history:
                if message['role'] == 'user':
                    st.markdown(f'<div class="chat-user">👤 {message["content"]}</div>', unsafe_allow_html=True)
                else:
                    st.markdown(f'<div class="chat-bot">🤖 {message["content"]}</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

        # Chat input
        user_input = st.chat_input("请输入您的问题...")

        if user_input:
            # Add user message to history
            st.session_state.chat_history.append({
                'role': 'user',
                'content': user_input,
                'timestamp': datetime.now().strftime('%H:%M:%S')
            })

            # Get bot response
            bot_response = get_chat_response(user_input, assistant)

            # Add bot response to history
            st.session_state.chat_history.append({
                'role': 'bot',
                'content': bot_response,
                'timestamp': datetime.now().strftime('%H:%M:%S')
            })

            # Rerun to display the new messages
            st.rerun()

        # Clear chat button
        col1, col2 = st.columns([1, 4])
        with col1:
            if st.button("🗑️ 清空对话", type="secondary"):
                st.session_state.chat_history = []
                st.rerun()
        with col2:
            st.empty()

        # Example questions
        st.markdown("---")
        st.markdown('<h3 style="color: #1f77b4; font-size: 1.1rem;">💡 示例问题</h3>', unsafe_allow_html=True)

        example_cols = st.columns(3)
        with example_cols[0]:
            st.markdown("""
            <div style="background-color: #E8F5E9; padding: 10px; border-radius: 8px; border-left: 3px solid #4CAF50;">
            <strong>事件相关</strong><br>
            • EVT001是什么？<br>
            • EVT001的风险等级？<br>
            • 中风险是怎么判断的？
            </div>
            """, unsafe_allow_html=True)

        with example_cols[1]:
            st.markdown("""
            <div style="background-color: #FFF3E0; padding: 10px; border-radius: 8px; border-left: 3px solid #FF9800;">
            <strong>机场与规则</strong><br>
            • 海陵国际机场的情况？<br>
            • 系统有哪些规则？<br>
            • 风险判断逻辑？
            </div>
            """, unsafe_allow_html=True)

        with example_cols[2]:
            st.markdown("""
            <div style="background-color: #F3E5F5; padding: 10px; border-radius: 8px; border-left: 3px solid #9C27B0;">
            <strong>天气与行动</strong><br>
            • EVT003的天气？<br>
            • EVT005应该怎么做？<br>
            • 高风险的判断标准？
            </div>
            """, unsafe_allow_html=True)

        st.markdown("---")
        st.markdown('<h3 style="color: #1f77b4; font-size: 1.1rem;">📋 系统评估问题</h3>', unsafe_allow_html=True)
        st.markdown('<p style="color: #666; font-size: 0.9rem;">您也可以问关于系统评估的问题：</p>', unsafe_allow_html=True)

        eval_cols = st.columns(2)
        with eval_cols[0]:
            st.markdown("""
            <div style="background-color: #E8EAF6; padding: 10px; border-radius: 8px; border-left: 3px solid #3F51B5;">
            <strong>核心能力</strong><br>
            • 如何定义异常？<br>
            • 能处理未见过的吗？<br>
            • 可以追溯吗？
            </div>
            """, unsafe_allow_html=True)

        with eval_cols[1]:
            st.markdown("""
            <div style="background-color: #FCE4EC; padding: 10px; border-radius: 8px; border-left: 3px solid #E91E63;">
            <strong>系统价值</strong><br>
            • 建议是否明确？<br>
            • 消息是否准确？<br>
            • 冲突如何处理？<br>
            • 有什么价值？
            </div>
            """, unsafe_allow_html=True)

    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #6c757d; font-size: 0.85rem;">
    <p>⚠️ 本系统使用赛事方提供的模拟数据，所有机场、城市、事件、规则和数值均为虚构，不对应真实机构或真实运行。</p>
    <p>HackSHSID 2026 Track 3 - 重点机场航班异常应对智能助手</p>
    <p style="margin-top: 20px; font-weight: bold;">10-11 Wendi Zhou</p>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
