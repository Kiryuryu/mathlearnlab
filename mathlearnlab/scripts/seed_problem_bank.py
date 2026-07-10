#!/usr/bin/env python3
"""
Seed problem bank generator.

Uses Claude API to generate an initial set of practice problems for each topic.
Run once to bootstrap the problem bank. Requires ANTHROPIC_API_KEY in
.streamlit/secrets.toml or as environment variable.

Usage:
    python scripts/seed_problem_bank.py                    # seed all topics
    python scripts/seed_problem_bank.py --topic integrals  # seed one topic
    python scripts/seed_problem_bank.py --count 20         # 20 problems per topic
"""

import argparse
import os
import sys
import json
import toml

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ocr_practice.config import TOPICS
from ocr_practice.utils.api_client import generate_problems
from ocr_practice.utils.problem_loader import save_problems


def get_api_key() -> str:
    """Get API key from Streamlit secrets or env var."""
    # Try Streamlit secrets first
    secrets_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        ".streamlit", "secrets.toml",
    )
    if os.path.exists(secrets_path):
        secrets = toml.load(secrets_path)
        key = secrets.get("ANTHROPIC_API_KEY", "")
        if key and key != "your-api-key-here":
            return key

    # Fall back to env var
    key = os.environ.get("ANTHROPIC_API_KEY", "")
    if key:
        return key

    print("❌ 未找到 ANTHROPIC_API_KEY。请在 .streamlit/secrets.toml 中设置，"
          "或设置环境变量 ANTHROPIC_API_KEY")
    sys.exit(1)


TOPIC_AREAS = {
    "limits": [
        "极限的计算（重要极限、等价无穷小）",
        "左右极限与极限存在性",
        "连续性与间断点分类",
        "无穷小的比较与阶",
    ],
    "derivatives": [
        "导数定义与可导性判断",
        "复合函数与隐函数求导",
        "中值定理（Rolle、Lagrange、Cauchy）",
        "泰勒公式与函数逼近",
        "函数单调性与极值问题",
    ],
    "integrals": [
        "不定积分的换元法与分部积分",
        "定积分的计算与对称性利用",
        "定积分的应用（面积、体积、弧长）",
        "反常积分的收敛性判别",
    ],
    "series": [
        "数项级数的审敛法",
        "幂级数的收敛半径与收敛域",
        "幂级数求和函数",
        "函数的幂级数展开（泰勒级数）",
        "傅里叶级数",
    ],
    "multivariable": [
        "偏导数与全微分的计算",
        "方向导数与梯度",
        "多元函数的极值与条件极值（拉格朗日乘数法）",
        "二重积分的计算与坐标变换",
        "曲线积分与格林公式",
    ],
}


def seed_topic(topic_key: str, count: int, api_key: str):
    """Generate problems for one topic across its sub-areas."""
    topic = TOPICS[topic_key]
    areas = TOPIC_AREAS.get(topic_key, [topic["zh"]])

    print(f"\n{'='*60}")
    print(f"生成 {topic['zh']} 题库...")
    print(f"{'='*60}")

    all_problems = []
    per_area = max(1, count // len(areas))

    for area in areas:
        print(f"  → {area} ({per_area} 题)...")
        try:
            problems = generate_problems(
                topic_zh=topic["zh"],
                knowledge_area=area,
                count=per_area,
                difficulty="mixed",
                api_key=api_key,
            )
            all_problems.extend(problems)
            print(f"    ✅ 生成了 {len(problems)} 题")
        except Exception as e:
            print(f"    ❌ 失败: {e}")
            continue

    if all_problems:
        save_problems(topic_key, all_problems, append=True)
        print(f"\n  💾 保存了 {len(all_problems)} 道题到 {topic['json']}")


def main():
    parser = argparse.ArgumentParser(description="Seed math problem bank")
    parser.add_argument("--topic", type=str, default=None,
                        help="Specific topic to seed (limits, derivatives, integrals, series, multivariable)")
    parser.add_argument("--count", type=int, default=12,
                        help="Number of problems per topic")
    args = parser.parse_args()

    api_key = get_api_key()

    topics_to_seed = [args.topic] if args.topic else list(TOPICS.keys())

    for tk in topics_to_seed:
        if tk not in TOPICS:
            print(f"❌ 未知 topic: {tk}")
            continue
        seed_topic(tk, args.count, api_key)

    print(f"\n🎉 完成! 总共处理了 {len(topics_to_seed)} 个 topic。")


if __name__ == "__main__":
    main()
