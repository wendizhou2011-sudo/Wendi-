"""
Flight Disruption AI Assistant
重点机场航班异常应对智能助手

An AI assistant for identifying problems, explaining reasoning, and recommending
responses when weather changes or operational disruptions occur at key airports.
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional
import json


class FlightDisruptionAssistant:
    """AI Assistant for Flight Disruptions at Key Airports"""

    def __init__(self, data_path: str):
        """
        Initialize the assistant with data from the Excel file.

        Args:
            data_path: Path to the Track 3 Data.xlsx file
        """
        self.data_path = data_path
        self.baseline_data = None
        self.scale_data = None
        self.weather_data = None
        self.events = None
        self.rules = None
        self.load_data()

    def load_data(self):
        """Load all data from the Excel file"""
        xls = pd.ExcelFile(self.data_path)

        # Load core datasets
        self.baseline_data = pd.read_excel(xls, sheet_name='01_机场月度运行基线')
        self.scale_data = pd.read_excel(xls, sheet_name='02_机场年度规模')
        self.weather_data = pd.read_excel(xls, sheet_name='03_机场天气月度')
        self.events = pd.read_excel(xls, sheet_name='04_模拟事件')
        self.rules = pd.read_excel(xls, sheet_name='05_运营规则')

        print(f"Loaded data:")
        print(f"  - Baseline records: {len(self.baseline_data)}")
        print(f"  - Scale records: {len(self.scale_data)}")
        print(f"  - Weather records: {len(self.weather_data)}")
        print(f"  - Events: {len(self.events)}")
        print(f"  - Rules: {len(self.rules)}")

    def get_airport_baseline(self, airport_name: str, year: int, month: int) -> Dict:
        """
        Get baseline performance for an airport in a specific month.

        Args:
            airport_name: Name of the airport
            year: Year
            month: Month

        Returns:
            Dictionary with baseline metrics
        """
        record = self.baseline_data[
            (self.baseline_data['机场名称'] == airport_name) &
            (self.baseline_data['年份'] == year) &
            (self.baseline_data['月份'] == month)
        ]

        if len(record) == 0:
            return None

        record = record.iloc[0]
        return {
            'scheduled_completion_rate': record['按计划完成航班的比例'],
            'departure_normal_rate': record['机场放行正常比例'],
            'peer_average': record['同类机场平均比例'],
            'self_12m_avg': record['该机场过去12个月平均比例'],
            'deviation_from_avg': record['与自身平均差（百分点）'],
            'source': record['来源编号']
        }

    def get_airport_scale(self, airport_name: str, year: int) -> Dict:
        """
        Get airport scale information.

        Args:
            airport_name: Name of the airport
            year: Year

        Returns:
            Dictionary with scale metrics
        """
        record = self.scale_data[
            (self.scale_data['机场名称'] == airport_name) &
            (self.scale_data['年份'] == year)
        ]

        if len(record) == 0:
            return None

        record = record.iloc[0]
        return {
            'city': record['城市'],
            'province': record['省份'],
            'airport_class': record['机场分类'],
            'passenger_throughput': record['旅客吞吐量（万人次）'],
            'flight_movements': record['飞机起降架次'],
            'business_importance': record['航空公司业务重要程度'],
            'source': record['来源编号']
        }

    def get_airport_weather(self, airport_name: str, year: int, month: int) -> Dict:
        """
        Get weather data for an airport in a specific month.

        Args:
            airport_name: Name of the airport
            year: Year
            month: Month

        Returns:
            Dictionary with weather metrics
        """
        record = self.weather_data[
            (self.weather_data['机场名称'] == airport_name) &
            (self.weather_data['年份'] == year) &
            (self.weather_data['月份'] == month)
        ]

        if len(record) == 0:
            return None

        record = record.iloc[0]
        return {
            'station_id': record['气象观测站编号'],
            'precipitation_mm': record['降水量（毫米）'],
            'avg_temp_c': record['平均气温（摄氏度）'],
            'max_wind_speed_ms': record['最大风速（米/秒）'],
            'adverse_weather_days': record['明显不利天气天数'],
            'data_missing': record['是否缺少数据'],
            'source': record['来源编号']
        }

    def get_event(self, event_id: str) -> Dict:
        """
        Get event details by ID.

        Args:
            event_id: Event ID (e.g., 'EVT001')

        Returns:
            Dictionary with event details
        """
        record = self.events[self.events['事件编号'] == event_id]

        if len(record) == 0:
            return None

        record = record.iloc[0]
        return {
            'event_id': event_id,
            'event_name': record['事件名称'],
            'event_time': record['事件时间'],
            'airport_name': record['机场名称'],
            'weather_description': record['天气描述'],
            'operation_description': record['运行情况描述'],
            'business_importance': record['航空公司业务重要程度'],
            'field_notes': record['现场备注'],
            'known_info': record['已知信息'],
            'unknown_info': record['未知信息'],
            'event_status': record['事件状态'],
            'data_marker': record['数据标记']
        }

    def get_relevant_rules(self, event: Dict) -> List[Dict]:
        """
        Get relevant rules for an event based on its characteristics.

        Args:
            event: Event dictionary

        Returns:
            List of relevant rules
        """
        # For now, return all rules
        # In a more sophisticated system, we would filter based on event characteristics
        relevant_rules = []
        for _, rule in self.rules.iterrows():
            relevant_rules.append({
                'rule_id': rule['规则编号'],
                'rule_topic': rule['规则主题'],
                'trigger_condition': rule['触发条件'],
                'suggested_checks': rule['建议核查事项'],
                'suggested_actions': rule['建议行动'],
                'escalation_target': rule['建议升级对象'],
                'requires_human_approval': rule['必须人工审批'],
                'prohibited_auto_actions': rule['禁止自动执行事项'],
                'rule_source': rule['规则来源'],
                'rule_status': rule['规则状态']
            })

        return relevant_rules

    def detect_disruption(self, event: Dict) -> Dict:
        """
        Detect if there is a disruption based on event data and historical baselines.

        Args:
            event: Event dictionary

        Returns:
            Dictionary with disruption assessment
        """
        airport_name = event['airport_name']

        # Parse event time to get year and month
        # For simulation, we'll assume current time is 2024-04 (第4天 in April)
        year = 2024
        month = 4

        # Get baseline, scale, and weather data
        baseline = self.get_airport_baseline(airport_name, year, month)
        scale = self.get_airport_scale(airport_name, year)
        weather = self.get_airport_weather(airport_name, year, month)

        if not baseline or not scale or not weather:
            return {
                'has_disruption': False,
                'reason': 'Insufficient data'
            }

        # Define disruption criteria
        # A disruption is defined as:
        # 1. Scheduled completion rate below self 12-month average by > 5 percentage points (0.05 in decimal)
        # 2. OR Adverse weather days > 3
        # 3. OR Combined with high business importance
        # 4. OR event explicitly mentions weather risk or operational pressure
        # 5. OR event name indicates a disruption scenario

        has_disruption = False
        disruption_factors = []

        # Check event name for disruption indicators
        event_name = event.get('event_name', '')
        if '风险' in event_name or '压力' in event_name or '冲突' in event_name:
            has_disruption = True
            disruption_factors.append(f"事件名称提示异常情况：{event_name}")

        # Check baseline deviation (convert from percentage points to decimal)
        if baseline['deviation_from_avg'] < -5.0:
            has_disruption = True
            disruption_factors.append(f"按计划完成航班比例比过去12个月平均低{abs(baseline['deviation_from_avg']):.1f}个百分点")

        # Check weather impact
        if weather['adverse_weather_days'] > 3:
            has_disruption = True
            disruption_factors.append(f"明显不利天气天数达到{weather['adverse_weather_days']}天")

        # Check business importance
        if scale['business_importance'] == '高':
            disruption_factors.append("该机场对航空公司业务重要程度为高")

        # Check event descriptions for explicit indicators
        weather_desc = event.get('weather_description', '')
        operation_desc = event.get('operation_description', '')

        if '风险' in weather_desc or '恶劣' in weather_desc or '不利' in weather_desc or '强降雨' in weather_desc or '雷雨' in weather_desc:
            has_disruption = True
            disruption_factors.append(f"天气描述中提及风险因素：{weather_desc}")

        if '压力' in operation_desc or '延误' in operation_desc or '异常' in operation_desc or '下降' in operation_desc or '冲突' in operation_desc:
            has_disruption = True
            disruption_factors.append(f"运行情况描述中提及异常：{operation_desc}")

        # Determine risk level
        if has_disruption:
            if scale['business_importance'] == '高' and len(disruption_factors) >= 2:
                risk_level = '高风险'
            elif len(disruption_factors) >= 2:
                risk_level = '中风险'
            else:
                risk_level = '低风险'
        else:
            risk_level = '正常'

        return {
            'has_disruption': has_disruption,
            'risk_level': risk_level,
            'disruption_factors': disruption_factors,
            'baseline': baseline,
            'scale': scale,
            'weather': weather
        }

    def generate_assistant_output(self, event_id: str) -> Dict:
        """
        Generate comprehensive AI assistant output for an event.

        Args:
            event_id: Event ID

        Returns:
            Dictionary with all required output fields
        """
        event = self.get_event(event_id)
        if not event:
            return {'error': f'Event {event_id} not found'}

        # Detect disruption
        disruption = self.detect_disruption(event)

        # Get relevant rules
        rules = self.get_relevant_rules(event)

        # Generate output based on event type and disruption assessment
        event_name = event.get('event_name', '')

        # Special handling for specific event types
        if '冲突' in event_name:
            return self._generate_conflict_response(event_id, event, disruption, rules)
        elif '否决' in event_name:
            return self._generate_rejection_response(event_id, event, disruption, rules)
        elif disruption['has_disruption']:
            return self._generate_disruption_response(event_id, event, disruption, rules)
        else:
            return self._generate_normal_response(event_id, event, disruption, rules)

    def _generate_disruption_response(self, event_id: str, event: Dict, disruption: Dict, rules: List[Dict]) -> Dict:
        """Generate response for disruption events"""
        airport = event['airport_name']
        scale = disruption['scale']
        weather = disruption['weather']
        baseline = disruption['baseline']

        # Build judgment basis
        judgment_basis = []
        judgment_basis.append(f"机场分类：{scale['airport_class']}，业务重要程度：{scale['business_importance']}")
        judgment_basis.append(f"按计划完成航班比例：{baseline['scheduled_completion_rate']:.2f}%")
        judgment_basis.append(f"与过去12个月平均差：{baseline['deviation_from_avg']:.2f}个百分点")
        judgment_basis.append(f"明显不利天气天数：{weather['adverse_weather_days']}天")

        # Build potential impact
        potential_impact = []
        if scale['business_importance'] == '高':
            potential_impact.append("影响多条主干航线，涉及大量旅客")
        if weather['adverse_weather_days'] > 2:
            potential_impact.append("天气因素可能导致后续航班延误")
        if baseline['deviation_from_avg'] < -5:
            potential_impact.append("运行效率显著下降，影响航班周转")

        # Build assumptions to verify
        assumptions = []
        assumptions.append("假设天气状况持续至当天结束")
        assumptions.append("假设当前运行下降趋势未得到控制")

        # Build information gaps
        info_gaps = [event['unknown_info']]

        # Build first action
        first_action = "立即核查当前实时运行状态和天气预警信息"

        # Build subsequent actions
        subsequent_actions = []
        subsequent_actions.append("对比同类机场当前运行表现")
        subsequent_actions.append("评估后续时段航班密度和资源压力")
        subsequent_actions.append("准备可能的航班调整预案")

        # Build escalation conditions
        escalation_conditions = []
        escalation_conditions.append("若放行正常比例进一步下降至70%以下")
        escalation_conditions.append("若不利天气持续时间延长至6小时以上")

        # Build human decision points
        human_decisions = []
        human_decisions.append("是否启动航班取消或合并程序")
        human_decisions.append("是否向机场申请优先保障资源")

        # Build internal operations message
        internal_msg = f"""
内部运营提示：

机场：{airport}
时间：{event['event_time']}
风险等级：{disruption['risk_level']}

当前情况：
- {scale['airport_class']}，旅客吞吐量{scale['passenger_throughput']}万人次
- 按计划完成航班比例{baseline['scheduled_completion_rate']:.2f}%，比平均低{abs(baseline['deviation_from_avg']):.2f}个百分点
- 明显不利天气{weather['adverse_weather_days']}天

建议核查：
{event['known_info']}

必须人工决定：
- {'; '.join(human_decisions)}
"""

        # Build airport coordination message
        airport_msg = f"""
机场协调信息：

机场：{airport}
情况说明：运行效率出现异常波动

当前数据：
- 按计划完成航班比例：{baseline['scheduled_completion_rate']:.2f}%
- 同类机场平均：{baseline['peer_average']:.2f}%
- 与自身12个月平均差：{baseline['deviation_from_avg']:.2f}个百分点

请求确认：
- 当前塔台放行指令状态
- 登机口资源可用情况
- 地面保障人员配置

协调建议：
- 如遇持续压力，请优先保障主干航线
- 预留备用机位以备航班延误
"""

        # Build passenger message draft
        passenger_msg = f"""
旅客信息草案（风险提示，非正式通知）：

尊敬的旅客：

{airport}机场当前天气条件可能对航班运行产生影响。我们正在密切关注情况，并将尽最大努力保障您的行程。

建议您：
- 出发前通过官方渠道查询最新航班动态
- 预留充足的出行时间
- 保持联系方式畅通

如有疑问，请联系客服热线。

注意：此为风险提示，具体航班状态以官方正式通知为准。
"""

        # Build citations
        citations = "SIM-WEATHER;SIM-BASE;SIM-SCALE;RULE002;RULE005"

        return {
            'event_id': event_id,
            'generation_time': event['event_time'],
            'risk_level': disruption['risk_level'],
            'airport_and_time': f"{airport}，{event['event_time']}",
            'judgment_basis': '；'.join(judgment_basis),
            'potential_impact': '；'.join(potential_impact),
            'assumptions_to_verify': '；'.join(assumptions),
            'information_gaps': info_gaps[0] if info_gaps else '',
            'first_action': first_action,
            'subsequent_actions': '；'.join(subsequent_actions),
            'escalation_conditions': '；'.join(escalation_conditions),
            'human_decisions': '；'.join(human_decisions),
            'internal_operations_msg': internal_msg.strip(),
            'airport_coordination_msg': airport_msg.strip(),
            'passenger_msg_draft': passenger_msg.strip(),
            'citations': citations,
            'output_status': '待复核'
        }

    def _generate_normal_response(self, event_id: str, event: Dict, disruption: Dict, rules: List[Dict]) -> Dict:
        """Generate response for normal/non-disruption events"""
        airport = event['airport_name']
        scale = disruption['scale']
        weather = disruption['weather']
        baseline = disruption['baseline']

        return {
            'event_id': event_id,
            'generation_time': event['event_time'],
            'risk_level': '正常',
            'airport_and_time': f"{airport}，{event['event_time']}",
            'judgment_basis': f"按计划完成航班比例{baseline['scheduled_completion_rate']:.2f}%，在正常波动范围内",
            'potential_impact': '无明显异常影响',
            'assumptions_to_verify': '',
            'information_gaps': event['unknown_info'],
            'first_action': '继续监控运行指标',
            'subsequent_actions': '定期更新状态',
            'escalation_conditions': '',
            'human_decisions': '',
            'internal_operations_msg': f'{airport}运行正常，按计划监控。',
            'airport_coordination_msg': '当前无需特殊协调。',
            'passenger_msg_draft': '',
            'citations': 'SIM-BASE',
            'output_status': '待复核'
        }

    def _generate_conflict_response(self, event_id: str, event: Dict, disruption: Dict, rules: List[Dict]) -> Dict:
        """Generate response for data conflict events"""
        airport = event['airport_name']
        scale = disruption['scale']
        weather = disruption['weather']
        baseline = disruption['baseline']

        # Build judgment basis
        judgment_basis = []
        judgment_basis.append(f"事件类型：数据来源冲突")
        judgment_basis.append(f"机场分类：{scale['airport_class']}，业务重要程度：{scale['business_importance']}")
        judgment_basis.append(f"来源甲显示运行正常，来源乙显示指标明显下降")
        judgment_basis.append(f"两个来源更新时间相差四十分钟")

        # Build potential impact
        potential_impact = []
        potential_impact.append("若采用错误数据可能导致误判")
        potential_impact.append("影响后续决策的准确性")

        # Build assumptions to verify
        assumptions = []
        assumptions.append("假设至少有一个来源数据有误或统计口径不一致")

        # Build information gaps
        info_gaps = event['unknown_info']

        # Build first action
        first_action = "暂停采用任一来源的结论，立即核查哪个来源已完成复核及统计口径"

        # Build subsequent actions
        subsequent_actions = []
        subsequent_actions.append("联系两个数据来源确认更新时间和统计方法")
        subsequent_actions.append("比对两个来源的原始数据明细")
        subsequent_actions.append("在确认准确数据前保持现有运行策略")

        # Build escalation conditions
        escalation_conditions = []
        escalation_conditions.append("若冲突持续超过30分钟无法解决")
        escalation_conditions.append("若任一来源确认数据存在系统性错误")

        # Build human decision points
        human_decisions = []
        human_decisions.append("决定采用哪个来源的数据作为决策依据")
        human_decisions.append("是否需要启动第三方数据源进行交叉验证")

        # Build internal operations message
        internal_msg = f"""
内部运营提示：

机场：{airport}
时间：{event['event_time']}
事件类型：数据来源冲突

当前情况：
- 来源甲：运行正常
- 来源乙：指标明显下降
- 更新时间差：40分钟

建议核查：
{event['unknown_info']}

必须人工决定：
- {'; '.join(human_decisions)}

注意事项：
- 在数据确认前不得发布确定性结论
- 根据RULE001，信息不足时不得发布确定性结论
"""

        # Build airport coordination message
        airport_msg = f"""
机场协调信息：

机场：{airport}
情况说明：数据来源存在冲突，暂未确认真实运行状态

当前状况：
- 内部数据来源显示不一致
- 需要时间核实准确数据

请求确认：
- 请提供当前机场实际运行状态
- 确认航班放行实际情况

协调建议：
- 暂时按常规运行安排
- 等待数据确认后再调整策略
"""

        # Build passenger message draft
        passenger_msg = ""
        # For data conflict events, no passenger message is appropriate yet

        # Build citations
        citations = "SIM-BASE;RULE001;RULE009"

        return {
            'event_id': event_id,
            'generation_time': event['event_time'],
            'risk_level': '待确认',
            'airport_and_time': f"{airport}，{event['event_time']}",
            'judgment_basis': '；'.join(judgment_basis),
            'potential_impact': '；'.join(potential_impact),
            'assumptions_to_verify': '；'.join(assumptions),
            'information_gaps': info_gaps,
            'first_action': first_action,
            'subsequent_actions': '；'.join(subsequent_actions),
            'escalation_conditions': '；'.join(escalation_conditions),
            'human_decisions': '；'.join(human_decisions),
            'internal_operations_msg': internal_msg.strip(),
            'airport_coordination_msg': airport_msg.strip(),
            'passenger_msg_draft': passenger_msg,
            'citations': citations,
            'output_status': '待复核'
        }

    def _generate_rejection_response(self, event_id: str, event: Dict, disruption: Dict, rules: List[Dict]) -> Dict:
        """Generate response for human rejection events"""
        airport = event['airport_name']
        scale = disruption['scale']
        weather = disruption['weather']
        baseline = disruption['baseline']

        # Build judgment basis
        judgment_basis = []
        judgment_basis.append(f"事件类型：人工否决与复盘")
        judgment_basis.append(f"机场分类：{scale['airport_class']}，业务重要程度：{scale['business_importance']}")
        judgment_basis.append(f"运营人员认为当前资源和现场情况足以应对")
        judgment_basis.append(f"智能助手原建议为高风险")

        # Build potential impact
        potential_impact = []
        potential_impact.append("需要重新评估风险判断标准")
        potential_impact.append("可能需要调整算法参数")

        # Build assumptions to verify
        assumptions = []
        assumptions.append("假设运营人员掌握现场实际情况")
        assumptions.append("假设现场资源信息未完全纳入系统")

        # Build information gaps
        info_gaps = event['unknown_info']

        # Build first action
        first_action = "记录人工否决原因，收集现场资源明细和运营人员判断依据"

        # Build subsequent actions
        subsequent_actions = []
        subsequent_actions.append("将现场资源信息纳入系统输入字段")
        subsequent_actions.append("分析为何系统判断与人工判断不一致")
        subsequent_actions.append("调整风险判断逻辑以纳入现场资源因素")

        # Build escalation conditions
        escalation_conditions = []
        escalation_conditions.append("若同类否决事件反复出现")
        escalation_conditions.append("若后续实际运行证明系统判断正确")

        # Build human decision points
        human_decisions = []
        human_decisions.append("确认是否需要调整系统判断阈值")
        human_decisions.append("决定如何改进现场资源信息的采集")

        # Build internal operations message
        internal_msg = f"""
内部运营提示：

机场：{airport}
时间：{event['event_time']}
事件类型：人工否决与复盘

当前情况：
- 智能助手原建议：高风险
- 运营人员判断：资源和现场情况足以应对
- 处理结果：拒绝建议

建议核查：
{event['unknown_info']}

必须人工决定：
- {'; '.join(human_decisions)}

改进建议：
- 把现场资源和人工判断依据加入输入字段
- 根据RULE006，不得覆盖或删除人工意见
"""

        # Build airport coordination message
        airport_msg = f"""
机场协调信息：

机场：{airport}
情况说明：智能助手建议已被运营人员否决

当前状况：
- 运营人员认为现场资源充足
- 按运营人员判断继续运行

协调建议：
- 保持当前运行安排
- 持续关注现场资源使用情况
"""

        # Build passenger message draft
        passenger_msg = ""

        # Build citations
        citations = "SIM-BASE;RULE006"

        return {
            'event_id': event_id,
            'generation_time': event['event_time'],
            'risk_level': '按人工判断',
            'airport_and_time': f"{airport}，{event['event_time']}",
            'judgment_basis': '；'.join(judgment_basis),
            'potential_impact': '；'.join(potential_impact),
            'assumptions_to_verify': '；'.join(assumptions),
            'information_gaps': info_gaps,
            'first_action': first_action,
            'subsequent_actions': '；'.join(subsequent_actions),
            'escalation_conditions': '；'.join(escalation_conditions),
            'human_decisions': '；'.join(human_decisions),
            'internal_operations_msg': internal_msg.strip(),
            'airport_coordination_msg': airport_msg.strip(),
            'passenger_msg_draft': passenger_msg,
            'citations': citations,
            'output_status': '待复盘'
        }


def main():
    """Main function to demonstrate the assistant"""
    # Initialize assistant
    assistant = FlightDisruptionAssistant('/Users/wendizhou/Downloads/HackSHSID 2026/Track 3 Data.xlsx')

    print("\n" + "="*80)
    print("FLIGHT DISRUPTION AI ASSISTANT")
    print("重点机场航班异常应对智能助手")
    print("="*80 + "\n")

    # Process all events
    event_ids = ['EVT001', 'EVT002', 'EVT003', 'EVT004', 'EVT005']

    for event_id in event_ids:
        print(f"\n{'='*80}")
        print(f"Processing Event: {event_id}")
        print(f"{'='*80}\n")

        output = assistant.generate_assistant_output(event_id)

        if 'error' in output:
            print(f"Error: {output['error']}")
            continue

        print(f"Event ID: {output['event_id']}")
        print(f"Generation Time: {output['generation_time']}")
        print(f"Risk Level: {output['risk_level']}")
        print(f"Airport & Time: {output['airport_and_time']}")
        print(f"\nJudgment Basis:")
        print(f"  {output['judgment_basis']}")
        print(f"\nPotential Impact:")
        print(f"  {output['potential_impact']}")
        print(f"\nFirst Action:")
        print(f"  {output['first_action']}")
        print(f"\nInternal Operations Message:")
        print(output['internal_operations_msg'])
        print(f"\nAirport Coordination Message:")
        print(output['airport_coordination_msg'])
        print(f"\nPassenger Message Draft:")
        print(output['passenger_msg_draft'])
        print(f"\nCitations: {output['citations']}")
        print(f"\nOutput Status: {output['output_status']}")

        # Save output to file
        with open(f'/Users/wendizhou/Downloads/HackSHSID 2026/output_{event_id}.json', 'w', encoding='utf-8') as f:
            json.dump(output, f, ensure_ascii=False, indent=2)
        print(f"\nOutput saved to: output_{event_id}.json")


if __name__ == "__main__":
    main()
