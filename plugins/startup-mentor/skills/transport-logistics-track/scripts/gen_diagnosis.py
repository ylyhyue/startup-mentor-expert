#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
交通/智慧物流赛道 创业项目诊断与赋能报告生成器

读取项目输入（JSON 或命令行参数），输出 Markdown 诊断与赋能报告。
可作为「大众创业导师」专家 skills/transport-logistics-track 模块的产出脚本。

用法:
  # 生成空白模板
  python3 gen_diagnosis.py --template

  # 基于 JSON 输入生成报告
  python3 gen_diagnosis.py --project "华豫冷链" --track 冷链 --stage 试产上市 --json info.json --output report.md

  # 仅给基本信息，其余留待填写
  python3 gen_diagnosis.py --project "平煤多式联运" --track 多式联运
"""
import argparse
import json
import sys
import datetime


# ---------- 内置知识库（领域锚定，非经营建议） ----------
LOGISTICS_STANDARDS = [
    ("GB/T 28577", "冷链物流分类与基本要求", "冷链企业基础合规框架"),
    ("GB/T 24616", "冷藏、冷冻食品物流包装、标志、运输和储存", "冷链运输/储存作业合规"),
    ("GB/T 19480", "肉与肉制品物流规范", "生鲜/肉制品冷链"),
    ("GB/T 21070", "通用仓库及库区规划设计参数", "仓储设施规划"),
    ("GB/T 21334", "物流园区统计", "物流园区/枢纽建设"),
    ("GB/T 18354", "物流术语", "统一话语体系"),
    ("GB/T 30332", "仓单要素与格式规范", "存货/仓单数字化"),
]

GS1_APPLICATIONS = [
    ("GTIN / 商品条码", "产品的数字身份证，进入商超、电商、供应链的准入前提"),
    ("GS1-128 / 箱码 (ITF-14)", "物流单元（箱/托盘）标识，支撑出入库与分拣自动化"),
    ("EPCIS 事件追溯", "记录交接、温控、位置等事件，支撑冷链'一物一码'可追溯"),
    ("统一标识 + 数据主键", "多式联运场景下以 GS1 标识打通铁路/公路/水运节点数据，沉淀数据资产"),
]

TRACK_SPECIAL_DIMS = [
    "标准化符合性", "条码/追溯就绪度", "多式联运数据贯通", "冷链温控合规", "绿色低碳（绿色城配）",
]

GENERIC_DIMS = ["技术与产品", "商业模式", "行业与市场", "团队", "财务与可行性", "差异化壁垒"]

PROJECT_ANCHORS = [
    "平顶山多式联运平台建设和数据资产探索（联合推进）",
    "2024 年度 GS1 系统应用研究课题——绿色城配领域（参与项目研究）",
    "华豫冷链等交通/物流领域创业项目的培育与参赛获奖经验",
]


def _dim_table():
    rows = []
    for d in GENERIC_DIMS:
        rows.append(f"| {d} | ⬜ | |")
    for d in TRACK_SPECIAL_DIMS:
        rows.append(f"| **{d}（物流专项）** | ⬜ | |")
    return "\n".join(rows)


def build_report(project, track, stage, info):
    today = datetime.date.today().isoformat()
    info = info or {}
    strengths = info.get("strengths", "（待填写）")
    weaknesses = info.get("weaknesses", "（待填写）")
    standards_used = info.get("standards_used", "（待填写）")
    barcode_status = info.get("barcode_status", "（待填写）")
    notes = info.get("notes", "")

    std_rows = "\n".join(f"| {code} | {name} | {use} |" for code, name, use in LOGISTICS_STANDARDS)
    gs1_rows = "\n".join(f"| {k} | {v} |" for k, v in GS1_APPLICATIONS)
    anchor_rows = "\n".join(f"- {a}" for a in PROJECT_ANCHORS)

    return f"""# 交通/智慧物流赛道 创业项目诊断与赋能报告

> 生成日期：{today} ｜ 模块：大众创业导师 · 交通/智慧物流赛道细分板块
> 项目：{project} ｜ 赛道：{track} ｜ 阶段：{stage}

## 一、赛道专属诊断（评分表）

| 维度 | 得分(1-5) | 短板与改进 |
|---|---|---|
{_dim_table()}

## 二、项目现状速写
- 优势：{strengths}
- 短板：{weaknesses}
- 已采用标准：{standards_used}
- 条码/GS1 现状：{barcode_status}

## 三、标准化赋能映射（建议适用）
| 标准号 | 名称 | 对本项目的价值 |
|---|---|---|
{std_rows}

## 四、条码 / GS1 赋能映射（建议适用）
| 能力 | 说明 |
|---|---|
{gs1_rows}

## 五、赛道版 BP 包装建议
- 一句话定位：以（标准化 + 条码/GS1 追溯）为差异化壁垒的 {track} 赛道项目。
- 评审加分话术：用真实标准/课题锚定权威背书，凸显数据资产与可追溯合规。
- 高频追问预判：标准化符合性如何证明？追溯数据是否真实上链？多式联运数据如何贯通？

## 六、全生命周期赋能路线图（交通/智慧物流版）
| 阶段 | 标准化动作 | 条码/GS1 动作 | 创业辅导动作 |
|---|---|---|---|
| 创意/立项 | 标准符合性预判 | 编码规划 | 赛道与组别定位 |
| 产品开发 | 引用产品/冷链标准 | 商品条码申请 | 差异化定位 |
| 试产/上市 | 良好行为创建 | 追溯码部署 | 路演包装 |
| 成长/融资 | 参与团标研制 | 全链路追溯+数据资产 | 商业模式打磨 |
| 规模化 | 输出企业/参与地标 | 数字化追溯复制 | 复制扩张 |

## 七、领域锚定（真实经验，非经营承诺）
{anchor_rows}

## 八、备注
{notes if notes else '（无）'}

---
*本报告由 AI 生成，提供路径与合规要点参考；具体认证、编码申请、知识产权等请对接专业机构。表述不含任何政党身份。*
"""


def build_template():
    return build_report("（项目名）", "（冷链/多式联运/绿色城配/智慧物流园区）", "（阶段）", {
        "strengths": "", "weaknesses": "", "standards_used": "", "barcode_status": "", "notes": ""
    })


def main():
    p = argparse.ArgumentParser(description="交通/智慧物流赛道诊断与赋能报告生成器")
    p.add_argument("--template", action="store_true", help="仅输出空白模板")
    p.add_argument("--project", default="（项目名）")
    p.add_argument("--track", default="（赛道）")
    p.add_argument("--stage", default="（阶段）")
    p.add_argument("--json", help="输入 JSON 路径（strengths/weaknesses/standards_used/barcode_status/notes）")
    p.add_argument("--output", help="输出 Markdown 路径（默认 stdout）")
    args = p.parse_args()

    if args.template:
        out = build_template()
    else:
        info = None
        if args.json:
            try:
                with open(args.json, encoding="utf-8") as f:
                    info = json.load(f)
            except Exception as e:
                sys.stderr.write(f"读取 JSON 失败: {e}\n")
                sys.exit(1)
        out = build_report(args.project, args.track, args.stage, info)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(out)
        print(f"已生成报告: {args.output}")
    else:
        sys.stdout.write(out)


if __name__ == "__main__":
    main()
