# Wendi-AirportAIAGENT
An intelligent assistant designed for a fictional Chinese domestic airline to identify problems, explain reasoning, and recommend responses when weather changes or operational disruptions occur at key airports, helping aviation professionals make informed decisions.
## Features

- **Anomaly Detection**: Multi-dimensional assessment based on historical baselines, airport scale, and weather data
- **Risk Assessment**: Automated risk level determination (High/Medium/Low/Normal) with clear judgment basis
- **Targeted Messaging**: Generates separate messages for operations staff, airport coordination teams, and passengers
- **Rule-Based Engine**: Complies with 10 operational rules ensuring safe and responsible decision-making
- **Interactive Web Interface**: Streamlit-based web application with event analysis and intelligent chatbot
- **Traceability**: All assessments traceable to data sources with clear distinction between known facts, assumptions, and unknown information
- **Human-AI Collaboration**: Critical decisions require human approval; respects professional judgment

## Demo

A live demo is available at: [Streamlit Cloud URL] (to be deployed)

## Quick Start

### Installation

```bash
pip install -r requirements.txt
```

### Command Line Usage

```bash
python3 flight_disruption_assistant.py
```

### Web Interface

```bash
streamlit run app.py
```

The web interface provides:
- Event analysis with detailed risk assessment
- Intelligent chatbot for Q&A about events, airports, and system logic
- Visual risk level indicators
- Message templates for different audiences

## Testing

Run the test suite:

```bash
python3 test_assistant.py
```

Test coverage: 95.2% (20/21 tests passed)

## Project Structure

```
├── flight_disruption_assistant.py   # Core AI assistant implementation
├── test_assistant.py               # Test suite
├── app.py                          # Streamlit web interface
├── requirements.txt                # Python dependencies
├── Track 3 Data.xlsx               # Simulated data (provided)
├── D01-D08/                        # Documentation and reports
└── README.md                       # This file
```

## Key Design Decisions

- **Disruption Definition**: Based on baseline deviation (>5% from 12-month average), weather impact (>3 adverse days), business importance, and event descriptions
- **Generalization**: Handles any airport, not limited to training set; based on rules and data rather than pre-written answers
- **Transparency**: All judgments backed by data or rules with traceable citations
- **Safety First**: Critical decisions (cancellations, dispatch, maintenance, compensation) require human approval

## Evaluation

The assistant addresses key evaluation questions:
- Can handle previously unseen events through rule-based and data-driven analysis
- Every key assessment is traceable to data or rules
- Recommendations clearly identify verification needs, action order, escalation conditions, and human decision points
- Messages are tailored for different audiences (operations, airport coordination, passengers)
- Adapts to data conflicts, insufficient information, and human rejection with feedback recording

## Documentation

- D01: Client presentation materials
- D03: Event test report
- D04: Data and rules documentation
- D05: Human feedback records
- D06: Risk card
- D07: Implementation roadmap
- D08: Project reproduction guide

## Author

10-11 Wendi Zhou

## License

This project is a competition submission for HackSHSID 2026 Track 3. All data, airports, cities, events, rules, and values are simulated for educational purposes and do not correspond to real institutions or operations.

## 项目结构

```
HackSHSID 2026/
├── Track 3 Data.xlsx                    # 赛事方提供的数据文件
├── flight_disruption_assistant.py       # 智能助手主程序
├── test_assistant.py                    # 测试套件
├── D01_客户汇报材料.md                   # 客户汇报材料
├── D03_事件测试报告.md                   # 事件测试报告
├── D04_数据与规则说明.md                 # 数据与规则说明
├── D05_人工反馈记录.md                   # 人工反馈记录
├── D06_风险卡.md                         # 风险卡
├── D07_实施路线图.md                     # 实施路线图
├── D08_项目复现包.md                     # 项目复现指南
└── README.md                            # 本文件
```

## 快速开始

### 环境要求

- Python 3.8+
- pandas
- openpyxl
- PyPDF2
- numpy

### 安装依赖

```bash
pip3 install pandas openpyxl PyPDF2 numpy
```

### 运行智能助手（命令行版本）

```bash
python3 flight_disruption_assistant.py
```

### 运行测试套件

```bash
python3 test_assistant.py
```

### 运行网页版本（推荐）

```bash
streamlit run app.py
```

网页版本将在浏览器中打开，提供可视化界面来选择和分析事件。

## 核心功能

### 1. 异常检测

基于多维度指标检测机场运行异常：
- 基线偏离：与历史平均差超过5个百分点
- 天气影响：明显不利天气天数超过3天
- 业务重要性：高重要性机场的异常需特别关注
- 事件描述：分析风险关键词

### 2. 风险等级判定

- 高风险：高重要性机场 + 多个异常因素
- 中风险：至少两个异常因素
- 低风险：单个异常因素
- 正常：无异常因素

### 3. 标准化输出

生成17个字段的标准化输出，包括：
- 风险等级
- 判断依据
- 可能影响
- 信息缺口
- 行动建议
- 多受众消息（运营人员、机场协调、旅客）
- 引用来源

### 4. 规则引擎

集成10条核心运营规则：
- RULE001: 信息不足处理
- RULE002: 天气风险处理
- RULE003: 异常波动处理
- RULE004: 持续运行压力处理
- RULE005: 旅客沟通处理
- RULE006: 人工否决处理
- RULE007: 重大运行决定
- RULE008: 高风险升级
- RULE009: 引用要求
- RULE010: 模拟标识

## 测试结果

运行10个测试用例，覆盖：
- 信息不足处理
- 事实引用
- 数据冲突处理
- 因果边界
- 人工审批
- 沟通对象区分
- 新机场泛化
- 未知信息处理
- 模拟标识
- 人工否决反馈

**测试通过率：95.2%**（21个测试项中20个通过，1个部分通过）

## 提交材料

### D01 客户汇报材料
- 项目概述和价值主张
- 解决方案架构
- 关键设计决策
- 测试结果
- 局限性与改进方向
- 实施建议

### D02 智能助手原型
- flight_disruption_assistant.py
- 完整功能实现
- 5个模拟事件处理

### D03 事件测试报告
- 测试概述和范围
- 测试结果汇总
- 事件处理详情
- 规则合规性检查
- 改进建议

### D04 数据与规则说明
- 数据来源说明
- 算法逻辑详解
- 输出格式定义
- 数据质量说明

### D05 人工反馈记录
- 反馈记录模板
- 模拟反馈记录
- 反馈分析
- 改进措施

### D06 风险卡
- 技术风险识别
- 业务风险识别
- 运营风险识别
- 外部风险识别
- 风险应对策略

### D07 实施路线图
- 项目阶段规划
- 技术架构演进
- 关键里程碑
- 资源需求
- 风险管理
- 成功指标

### D08 项目复现包
- 环境配置
- 安装步骤
- 运行步骤
- 结果验证
- 常见问题
- 扩展开发

## 关键特性

### 透明性
- 所有判断均有数据或规则支撑
- 明确标注引用来源
- 区分已知事实、假设和未知信息

### 可追溯性
- 完整的判断依据说明
- 信息缺口明确列出
- 引用来源可追溯

### 人机协同
- 关键决策必须由人工审批
- 尊重专业人员的判断
- 不得覆盖或删除人工意见

### 泛化能力
- 可处理任何机场（不仅限于训练集）
- 不依赖预编写的答案
- 基于规则和数据动态判断

## 设计原则

1. **不虚构数据**：不得由模型虚构补齐未知信息
2. **谨慎因果**：天气数据仅作关联背景，不能证明延误因果关系
3. **模拟标识**：明确说明所有数据为模拟，不对应真实机构
4. **安全边界**：重大运行决定必须由人工审批
5. **持续改进**：建立反馈闭环，从人工反馈中学习

## 局限性

1. **实时数据缺失**：当前使用月度数据，缺乏实时运行数据
2. **预测能力有限**：主要基于当前状态，预测能力不足
3. **规则固定**：10条规则相对固定，难以适应新场景
4. **学习机制**：缺乏从反馈中自动学习的机制

## 改进方向

### 短期
- 优化旅客消息格式
- 增加现场资源信息采集
- 明确引用RULE007和RULE008

### 中期
- 接入实时数据
- 扩展规则库
- 建立反馈闭环机制

### 长期
- 引入机器学习模型
- 建立持续学习机制
- 扩展到更多机场

## 数据说明

本项目使用赛事方提供的模拟数据，包括：
- 8个机场（云川、海陵、北岭、星湖、南湾、青岚、临江、高原）
- 24个月的月度数据
- 5个模拟事件
- 10条运营规则

**重要声明**：所有机场、城市、事件、规则和数值均为赛事方生成的教学模拟内容，不对应真实机构或真实运行。

## 技术栈

- **语言**：Python 3.8+
- **数据处理**：pandas, numpy
- **文件读取**：openpyxl, PyPDF2
- **测试**：自定义测试框架

## 许可

本项目为赛事提交作品，仅供学习和评估使用。

## 联系方式

如有问题或建议，请参考D08_项目复现包.md中的详细说明。

---

**版本**：v1.0
**最后更新**：2026-10-20
**赛事**：HackSHSID 2026 Track 3
