"""
MathLearnLab server configuration via pydantic-settings.
Reads from environment variables or .env file.
"""

import os
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # ── Server ──
    app_name: str = "数学博物馆"
    app_subtitle: str = "知其然，知其所以然"
    debug: bool = False
    host: str = "127.0.0.1"
    port: int = 8000

    # ── Paths ──
    content_dir: str = "content"
    data_dir: str = "data"

    # ── AI / DeepSeek API ──
    deepseek_api_key: str = ""
    deepseek_model: str = "deepseek-chat"
    max_grading_tokens: int = 2000
    max_chat_tokens: int = 4096

    # ── Auth / JWT ──
    jwt_secret_key: str = ""
    jwt_algorithm: str = "HS256"
    jwt_expire_minutes: int = 60 * 24  # 24 hours

    # ── Email / SMTP ──
    smtp_host: str = ""
    smtp_user: str = ""
    smtp_pass: str = ""
    admin_email: str = ""

    # ── Database ──
    database_url: str = ""

    # ── Museum Exhibits ──
    exhibits: dict = {
        "gaoshu":        {"zh": "展区", "en": "Exhibits",
                          "historian": "牛顿、莱布尼茨、柯西、欧拉…",
                          "big_question": "变化、累积、无穷——微积分如何改变了人类理解世界的方式？",
                          "big_question_en": "Change, accumulation, infinity — how did calculus transform our understanding of the world?",
                          "beauty": "微积分是人类思想史上最伟大的成就之一。从芝诺的飞矢不动悖论，到牛顿和莱布尼茨的激烈争论，到柯西用ε-δ语言为它打下坚实根基——这是一个跨越两千年的故事。",
                          "beauty_en": "Calculus is one of the greatest achievements in human intellectual history. From Zeno's arrow paradox to the Newton–Leibniz priority dispute to Cauchy's ε-δ foundations — a story spanning two millennia."},
        "limits":        {"zh": "极限 — 无限逼近的艺术", "en": "Limits — The Art of Infinite Approximation", "icon": "∞", "json": "limits.json",
                          "parent": "gaoshu", "order": 1,
                          "historian": "柯西、魏尔斯特拉斯",
                          "big_question": "如何用数学语言精确描述'无限接近'？",
                          "big_question_en": "How do we precisely describe 'approaching arbitrarily close' in mathematical language?",
                          "beauty": "ε-δ 定义用有限的符号捕捉了无穷的直觉",
                          "beauty_en": "The ε-δ definition captures the intuition of infinity with finite symbols",
                           "notebook": "notebooks/01-gaoshu/01-limits-continuity-differentiation"},
        "derivatives":   {"zh": "导数 — 瞬间的变化率",   "en": "Derivatives — Instantaneous Rate of Change",   "icon": "∆", "json": "derivatives.json",
                           "parent": "gaoshu", "order": 2,
                           "historian": "费马、牛顿、莱布尼茨",
                           "big_question": "如何在某一瞬间测量变化？",
                           "big_question_en": "How do we measure change at a single instant?",
                           "beauty": "泰勒展开：任何光滑函数都可以用多项式逼近",
                           "beauty_en": "Taylor expansion: any smooth function can be approximated by polynomials",
                           "notebook": "notebooks/01-gaoshu/01-limits-continuity-differentiation"},
        "integrals":     {"zh": "积分 — 和的极限",       "en": "Integrals — The Limit of Sums",       "icon": "∫", "json": "integrals.json",
                           "parent": "gaoshu", "order": 3,
                           "historian": "阿基米德、黎曼、勒贝格",
                           "big_question": "如何求一个曲线下方不规则图形的面积？",
                           "big_question_en": "How do we find the area under an irregular curve?",
                           "beauty": "微积分基本定理：微分和积分是互逆运算——这是数学史上最伟大的发现之一",
                           "beauty_en": "The Fundamental Theorem of Calculus: differentiation and integration are inverse operations — one of the greatest discoveries in mathematics",
                           "notebook": "notebooks/01-gaoshu/02-integration"},
        "series":        {"zh": "无穷级数 — 无限的拼图",  "en": "Infinite Series — The Puzzle of Infinity",  "icon": "∑", "json": "series.json",
                           "parent": "gaoshu", "order": 4,
                           "historian": "欧拉、傅里叶",
                           "big_question": "无穷多个数加起来可以是有限的吗？",
                           "big_question_en": "Can adding infinitely many numbers give a finite result?",
                           "beauty": "巴塞尔问题：1+1/4+1/9+1/16+... = π²/6 —— 自然数的倒数平方和竟然与圆周率有关",
                           "beauty_en": "The Basel problem: 1+1/4+1/9+1/16+... = π²/6 — the sum of reciprocal squares is related to π",
                           "notebook": "notebooks/01-gaoshu/03-infinite-series"},
        "multivariable": {"zh": "多元微积分 — 从平面到空间","en": "Multivariable Calculus — From Plane to Space","icon": "∂", "json": "multivariable.json",
                           "parent": "gaoshu", "order": 5,
                           "historian": "拉格朗日、高斯、格林",
                           "big_question": "如何在多维世界中理解变化、极值和流动？",
                           "big_question_en": "How do we understand change, extrema, and flow in multi-dimensional worlds?",
                           "beauty": "梯度下降：沿着最陡峭的方向下山——这个概念今天驱动着所有AI的学习",
                           "beauty_en": "Gradient descent: go downhill in the steepest direction — this concept drives all of modern AI",
                           "notebook": "notebooks/01-gaoshu/04-multivariable-calculus"},
        "fractal":       {"zh": "分形 — 无限自相似的宇宙", "en": "Fractals — The Infinitely Self-Similar Universe",
                          "historian": "曼德尔布罗特、朱利亚",
                          "big_question": "有限的面积可以有无限的周长吗？",
                          "big_question_en": "Can a finite area have an infinite perimeter?",
                          "beauty": "Mandelbrot 集：一个最简单的迭代公式 z→z²+c 能生成宇宙中最复杂的图形之一",
                          "beauty_en": "The Mandelbrot set: the simplest iteration z→z²+c generates one of the most complex shapes in the universe"},
        "linear-algebra":{"zh": "线性代数 — 空间的变换", "en": "Linear Algebra — Transformations of Space",
                          "historian": "凯莱、哈密顿、格拉斯曼",
                          "big_question": "一个矩阵乘以一个向量，到底在做一件什么事？",
                          "big_question_en": "What does multiplying a matrix by a vector actually do?",
                          "beauty": "特征向量是矩阵变换下\"方向不变\"的向量——它们揭示了系统的本质",
                          "beauty_en": "Eigenvectors are vectors whose direction is preserved by the transformation — they reveal the essence of the system",
                          "notebook": "02-xiandai/01-linear-algebra"},
        "probability":   {"zh": "概率论 — 不确定性的科学", "en": "Probability — The Science of Uncertainty",
                          "historian": "帕斯卡、伯努利、柯尔莫哥洛夫",
                          "big_question": "如何用数学描述\"随机\"？",
                          "big_question_en": "How do we describe randomness mathematically?",
                          "beauty": "大数定律：随机中蕴含着确定性——大量独立随机事件的平均值总是趋近于期望值",
                          "beauty_en": "The Law of Large Numbers: randomness contains certainty — the average of many independent events approaches the expected value",
                          "notebook": "03-gailvlun/01-probability"},
    }

    # ── Math Quotes ──
    quotes: list[str] = [
        "数学是上帝书写宇宙的语言。 — 伽利略",
        "数学的本质不在于数字，而在于严密的逻辑推理。 — 魏尔斯特拉斯",
        "一个好的符号就像一个设备正确的天平——它们替我们思考。 — 莱布尼茨",
        "如果我看得更远，那是因为我站在巨人的肩膀上。 — 牛顿",
        "数学是科学的皇后，数论是数学的皇后。 — 高斯",
        "对自然的深入研究是数学发现最肥沃的土壤。 — 傅里叶",
        "一个方程对我没有意义，除非它表达的是上帝的思想。 — 拉马努金",
        "纯数学是逻辑思想的诗集。 — 爱因斯坦",
        "在数学中，你不理解事物，你只是习惯它们。 — 冯·诺依曼",
        "数学是唯一的人类活动可以无限延续到未来而不会失去意义的。 — 哈代",
        "学习的唯一方式是通过发现。 — 费曼",
        "数学不是关于方程式的，它是关于思想之间的关系的。 — 威廉·瑟斯顿",
        "问题是数学的心脏。 — 哈尔莫斯",
        "在数学中，技巧比力量更重要。 — 卡尔达诺",
        "你必须理解数学。这不是可选的。 — 埃里克·韦恩斯坦",
        "数学是你在黑暗中摸索时照亮道路的光。 — 纳皮尔",
        "如果我有一个小时来解决一个问题，我会花 55 分钟思考问题，5 分钟思考解决方案。 — 爱因斯坦",
    ]

    difficulty: dict = {
        "basic":     {"zh": "基础", "label": "基础入门"},
        "advanced":  {"zh": "进阶", "label": "进阶提高"},
        "exam":      {"zh": "考研", "label": "考研难度"},
        "graduate":  {"zh": "研究生", "label": "研究生"},
        "phd":       {"zh": "博士", "label": "博士级"},
    }

    # ── Mathematicians ──
    mathematicians: dict = {
        "newton": {
            "name": "艾萨克·牛顿",
            "name_en": "Isaac Newton",
            "years": "1643–1727",
            "icon": "N",
            "contributions": "微积分、万有引力定律、光学",
            "contributions_en": "Calculus, law of universal gravitation, optics",
            "story": "1665年，剑桥因瘟疫关闭，23岁的牛顿回到乡下。在18个月里，他发明了微积分（他称之为\"流数法\"）——这可以计算任意瞬间的变化率。他还发现了万有引力定律，并证明白光由多种颜色组成。这18个月被称为科学史上最富有成果的\"奇迹年\"。",
            "story_en": "In 1665, Cambridge closed due to the plague, and 23-year-old Newton returned to the countryside. In 18 months, he invented calculus (which he called \"the method of fluxions\") — a way to calculate rates of change at any instant. He also discovered the law of universal gravitation and proved that white light is composed of multiple colors. These 18 months became known as the most productive \"miracle year\" in the history of science.",
            "quote": "如果说我看得比别人更远，那是因为我站在巨人的肩膀上。",
            "exhibits": ["derivatives", "integrals"],
            "bio": "1643年生于英国林肯郡乌尔索普。父亲早逝，母亲改嫁，幼年由外祖母抚养。1661年考入剑桥大学三一学院。1665年伦敦大瘟疫期间返乡，在一年半里完成了微积分、万有引力、光学三大发现。1687年发表《自然哲学的数学原理》，奠定了经典物理学的基石。晚年担任皇家学会会长、造币厂厂长，主导了英国币制改革。1727年逝世，葬于威斯敏斯特大教堂。",
            "bio_en": "Born in 1643 in Woolsthorpe, Lincolnshire, England. His father died before he was born and his mother remarried, leaving him to be raised by his grandmother. He entered Trinity College, Cambridge in 1661. During the London plague of 1665, he returned home and completed his three great discoveries in calculus, universal gravitation, and optics in just 18 months. In 1687 he published the Principia Mathematica, laying the foundation of classical physics. He later served as President of the Royal Society and Master of the Mint. He died in 1727 and was buried in Westminster Abbey.",
            "ideas": "微积分（流数法）：历史上第一次系统地提供了描述变化与累积的数学语言——从瞬时速度到曲线下面积，全部统一在微分与积分这对互逆运算之下。万有引力定律：宇宙中任意两个有质量的物体之间都存在与质量乘积成正比、与距离平方成反比的引力——这统一了天体力学和地面力学。三大运动定律：惯性定律、F=ma、作用与反作用——构成了经典力学的完整框架。光的粒子说与反射式望远镜：认为光由微粒组成，并据此发明了反射式望远镜以避免色差。",
            "ideas_en": "Calculus (method of fluxions): the first systematic mathematical language for describing change and accumulation — from instantaneous velocity to area under a curve, all unified under the inverse operations of differentiation and integration. Law of universal gravitation: every particle of matter attracts every other particle with a force proportional to the product of their masses and inversely proportional to the square of the distance between them — unifying celestial and terrestrial mechanics. Three laws of motion: inertia, F=ma, and action-reaction — the complete framework of classical mechanics. Corpuscular theory of light and the reflecting telescope: proposed that light consists of particles, and invented the reflecting telescope to eliminate chromatic aberration.",
            "anecdotes": "牛顿被苹果砸中脑袋而悟出万有引力的故事虽经伏尔泰文学渲染，但确有来源——牛顿晚年多次对友人提及这个花园里的灵感时刻。他投入炼金术研究的时间远超科学：留下的炼金术手稿超过100万字，比他的科学著作总量还多。他还花费大量精力推算圣经编年史，甚至根据圣经预言推算了世界末日的日期。他与莱布尼茨就微积分优先权展开了长达数十年的激烈论战，这场争论甚至演变为英德两国民族主义之争。",
            "anecdotes_en": "The story of Newton being hit on the head by an apple and discovering universal gravitation was popularized by Voltaire, but it has some basis — Newton mentioned the garden inspiration to friends in his later years. He devoted far more time to alchemy than to science: his alchemical manuscripts exceed one million words, more than all his scientific writings combined. He also spent enormous energy calculating biblical chronology and even predicted the date of the apocalypse based on biblical prophecy. His decades-long priority dispute with Leibniz over the invention of calculus escalated into a nationalist conflict between England and Germany.",
        },
        "leibniz": {
            "name": "戈特弗里德·莱布尼茨",
            "name_en": "Gottfried Leibniz",
            "years": "1646–1716",
            "icon": "L",
            "contributions": "微积分符号系统（∫, d/dx）、二进制、哲学",
            "contributions_en": "Calculus notation (∫, d/dx), binary system, philosophy",
            "story": "莱布尼茨独立于牛顿发明了微积分，但他设计的符号系统——∫ 表示积分、d/dx 表示微分——比牛顿的\"流数法\"符号优雅得多，至今仍在被全世界使用。这引发了一场关于\"谁先发明微积分\"的激烈争论，延续了数十年。历史对两个人的贡献都给予了高度认可。",
            "story_en": "Leibniz independently invented calculus, but the notation he designed — ∫ for integrals and d/dx for derivatives — was far more elegant than Newton's \"method of fluxions\" and is still used worldwide today. This sparked a bitter decades-long dispute over who invented calculus first. History has given full recognition to both men's contributions.",
            "quote": "∫ 是一个最美的字母，它把无穷细小的部分加总成完整的整体。",
            "exhibits": ["derivatives", "integrals", "series"],
            "bio": "1646年生于德国莱比锡。15岁入莱比锡大学攻读法律，20岁完成博士论文。他不仅是数学家，更是哲学家、法学家、外交家、历史学家、神学家——真正的百科全书式天才。曾为汉诺威公爵服务数十年，在欧洲各国从事外交与学术交流。晚年因微积分优先权争论声誉受损，1716年在汉诺威孤独去世，只有秘书参加葬礼。",
            "bio_en": "Born in 1646 in Leipzig, Germany. Entered Leipzig University at 15 to study law and completed his doctoral dissertation at 20. He was not only a mathematician but also a philosopher, jurist, diplomat, historian, and theologian — a true universal genius. He served the Duke of Hanover for decades, engaging in diplomatic and academic exchanges across Europe. In his later years, his reputation suffered from the calculus priority dispute. He died alone in Hanover in 1716, with only his secretary attending his funeral.",
            "ideas": "微积分符号系统：∫（将拉丁语 summa 的首字母 s 拉长）表示积分，d/dx 表示微分——优雅的符号使微积分易于学习和运用。二进制：1679年发明二进制算术，用0和1表示一切数字。单子论：提出宇宙由无数不可分的\"单子\"组成，每种单子从不同视角反映宇宙整体。通用语言理想：梦想创造一种符号推理系统（characteristica universalis），使一切争论都可像数学一样通过计算解决——被誉为计算机科学的哲学先驱。",
            "ideas_en": "Calculus notation: ∫ (an elongated 's' from the Latin summa) for integration, d/dx for differentiation — elegant notation that made calculus easy to learn and apply. Binary system: invented in 1679, representing all numbers using only 0 and 1. Monadology: proposed that the universe is composed of infinitely many indivisible \"monads,\" each reflecting the whole universe from its own perspective. Universal language ideal: dreamed of creating a symbolic reasoning system (characteristica universalis) that would allow all disputes to be resolved through calculation like mathematics — he is regarded as a philosophical pioneer of computer science.",
            "anecdotes": "莱布尼茨通过传教士了解中国的《易经》，发现二进制与阴阳爻完全吻合后深受震撼，认为这印证了他关于\"从无（0）中生有（1）\"的创世哲学。他一生追求\"世界和平\"的宏大构想，写过《论永久和平》并游说欧洲君主们。他还是最早的女权倡导者之一——他曾说\"如果女人有机会接受同等教育，她们在科学上的成就不亚于男人\"。他的二进制三百多年后成为数字计算机的基石——真正的超前于时代者。",
            "anecdotes_en": "When Leibniz learned of the Yijing (I Ching) through missionaries, he was astonished to find its yin-yang trigrams perfectly matched his binary system, seeing it as confirmation of his philosophy of \"creation from nothing\" (0 and 1). He pursued grand visions of world peace throughout his life, writing On Perpetual Peace and lobbying European monarchs. He was also an early advocate for women's rights — he once said that if women had equal educational opportunities, they would achieve as much as men in science. His binary system became the foundation of digital computers three centuries later — truly ahead of his time.",
        },
        "euler": {
            "name": "莱昂哈德·欧拉",
            "name_en": "Leonhard Euler",
            "years": "1707–1783",
            "icon": "E",
            "contributions": "e^(iπ)+1=0、图论、分析学、流体力学",
            "contributions_en": "Euler's formula e^(iπ)+1=0, graph theory, analysis, fluid mechanics",
            "story": "欧拉是历史上最高产的数学家——他发表了超过850篇论文和著作。即使在双目失明的最后17年，他依然以惊人的速度产出数学成果。他发现了最美公式 e^(iπ)+1=0，将五个最重要的数学常数统一在一个方程中。他还解决了著名的巴塞尔问题：1+1/4+1/9+1/16+... = π²/6。",
            "story_en": "Euler was the most prolific mathematician in history — he published over 850 papers and books. Even in his final 17 years of total blindness, he continued producing mathematical results at an astonishing rate. He discovered the most beautiful formula e^(iπ)+1=0, which unifies the five most important mathematical constants in a single equation. He also solved the famous Basel problem: 1+1/4+1/9+1/16+... = π²/6.",
            "quote": "数学是真实世界的语言，上帝用它书写了宇宙。",
            "exhibits": ["series", "integrals", "multivariable"],
            "bio": "1707年生于瑞士巴塞尔。13岁入巴塞尔大学，师从约翰·伯努利。1727年赴圣彼得堡科学院。在俄罗斯期间因过度用眼，1738年右眼失明。1766年左眼完全失明。但凭借惊人的记忆力和心算能力，在完全失明后的17年产出超过全部工作的一半。后应腓特烈大帝邀请在柏林科学院工作25年。1783年在圣彼得堡因脑溢血去世，正坐在书桌前演算。",
            "bio_en": "Born in 1707 in Basel, Switzerland. Entered the University of Basel at 13, studying under Johann Bernoulli. He moved to the St. Petersburg Academy of Sciences in 1727. Overwork caused him to lose sight in his right eye in 1738, and his left eye by 1766. Yet despite total blindness, his final 17 years produced more than half of his total work, thanks to his extraordinary memory and mental calculation abilities. He later worked at the Berlin Academy for 25 years at the invitation of Frederick the Great. He died of a cerebral hemorrhage in St. Petersburg in 1783 while sitting at his desk calculating.",
            "ideas": "分析学奠基：系统建立了函数概念，统一了指数函数、三角函数和对数函数的分析处理。最美公式 e^(iπ)+1=0：将 e、i、π、1、0 五个最重要的数学常数统一在一个等式中——被称为\"上帝的公式\"。巴塞尔问题：证明了自然数倒数平方和收敛于 π²/6，一举成名。图论起源：解决柯尼斯堡七桥问题，开创了图论这一全新分支。现代符号的发明者：f(x)、π、e、i、Σ、Δ、sin/cos/tan 等符号都出自欧拉之手——没有欧拉，我们今天的数学书写方式将完全不同。",
            "ideas_en": "Foundations of analysis: systematically established the concept of functions and unified the analytical treatment of exponential, trigonometric, and logarithmic functions. Euler's formula e^(iπ)+1=0: unifies the five most important constants — e, i, π, 1, 0 — in a single equation, often called \"God's formula.\" Basel problem: proved that the sum of reciprocal squares converges to π²/6, bringing him instant fame. Origin of graph theory: solved the Königsberg bridge problem, founding an entirely new branch of mathematics. Inventor of modern notation: f(x), π, e, i, Σ, Δ, sin/cos/tan — all originated with Euler. Without him, modern mathematical notation would look completely different.",
            "anecdotes": "欧拉可以一边哄着坐在膝盖上的孩子，一边在纸上演算最深的数学问题，精确到小数点后多位。他的记忆力惊人：能完整背诵维吉尔的《埃涅阿斯纪》全文，并能说出每一页的第一行和最后一行的内容。他曾与法国哲学家狄德罗打赌，当着凯瑟琳大帝的面煞有介事地写下\"a + b^n/n = x，故上帝存在\"——完全不懂数学的狄德罗无言以对，被吓得离开了圣彼得堡。失明后他的工作效率反而更高，因为不受视觉干扰，全部精力集中于数学本质。",
            "anecdotes_en": "Euler could hold a child on his knee while calculating the deepest mathematical problems to many decimal places. His memory was phenomenal: he could recite Virgil's Aeneid from beginning to end and recall the first and last lines of any page. He once challenged the French philosopher Diderot in front of Catherine the Great, solemnly writing \"a + b^n/n = x, therefore God exists\" — Diderot, who knew no mathematics, was left speechless and fled St. Petersburg. After going blind, Euler's productivity actually increased, since without visual distractions he could focus entirely on the essence of mathematics.",
        },
        "gauss": {
            "name": "卡尔·弗里德里希·高斯",
            "name_en": "Carl Friedrich Gauss",
            "years": "1777–1855",
            "icon": "G",
            "contributions": "数论、正态分布、最小二乘法、曲面理论",
            "contributions_en": "Number theory, normal distribution, least squares, differential geometry",
            "story": "高斯3岁时就能纠正父亲的算术错误；10岁时，老师让全班算1+2+...+100，他几秒内就发现了配对法(1+100)×50=5050。成年后，他几乎在所有数学分支都做出了深远贡献。他发明的\"最小二乘法\"至今是数据拟合的基石；他的曲面理论为后来的爱因斯坦广义相对论铺平了道路。",
            "story_en": "At age 3, Gauss could correct his father's arithmetic errors. At 10, when his teacher asked the class to sum 1+2+...+100, he instantly found the pairing method (1+100)×50=5050. As an adult, he made profound contributions to nearly every branch of mathematics. His method of least squares remains the foundation of data fitting; his curved surface theory later paved the way for Einstein's general relativity.",
            "quote": "数学是科学的皇后，数论是数学的皇后。",
            "exhibits": ["integrals", "multivariable", "series"],
            "bio": "1777年生于德国布伦瑞克的贫苦家庭——母亲不识字，父亲做苦工。3岁纠正父亲算账错误，7岁入学即展露天赋。布伦瑞克公爵慷慨资助其上中学和大学。18岁发明最小二乘法，19岁发现正十七边形的尺规作图法——这是两千年来正多边形作图问题的首次突破。1807年任哥廷根天文台台长，此后终生在此工作。1855年安详离世。",
            "bio_en": "Born in 1777 to a poor family in Brunswick, Germany — his mother was illiterate and his father worked as a laborer. He corrected his father's accounting at age 3 and showed his genius from his first day of school. The Duke of Brunswick generously funded his education through secondary school and university. At 18 he invented the method of least squares; at 19 he discovered how to construct a regular 17-gon with compass and straightedge — the first advance in polygon construction in 2,000 years. In 1807 he became director of the Göttingen Observatory, where he worked for the rest of his life. He died peacefully in 1855.",
            "ideas": "《算术研究》：现代数论的奠基之作，系统阐述了同余理论、二次互反律，至今仍是数论的核心。正态分布（高斯分布）：误差理论的核心，自然与社会科学中最重要的概率分布，\"钟形曲线\"无处不在。最小二乘法：从冗余观测数据中找出最佳拟合的数学方法，一切数据科学的起点。内蕴几何：在《关于曲面的一般研究》中提出曲面本身的几何性质与外部嵌入无关——这被称为\"内蕴几何\"，后来成为爱因斯坦广义相对论的数学语言。天文学：用最小二乘法仅从少量观测数据就精准计算出了谷神星的轨道，轰动天文学界。",
            "ideas_en": "Disquisitiones Arithmeticae: the foundational text of modern number theory, systematically presenting congruence theory and quadratic reciprocity — still central to number theory today. Normal distribution (Gaussian distribution): the core of error theory and the most important probability distribution in the natural and social sciences — the bell curve is everywhere. Least squares: the mathematical method for finding the best fit from redundant observational data — the starting point of all data science. Intrinsic geometry: in his General Investigations of Curved Surfaces, he proposed that a surface's geometric properties are independent of how it is embedded in space — this \"intrinsic geometry\" later became the mathematical language of Einstein's general relativity. Astronomy: using least squares, he calculated the orbit of Ceres from minimal observational data, stunning the astronomical world.",
            "anecdotes": "高斯对自己的成果极度挑剔——他的座右铭是\"Pauca sed matura\"（少些，但要成熟）。他拒绝发表非欧几何的发现，因为在信中担心\"波奥提亚人的叫嚣\"（保守派攻击）。这些工作在他去世后由鲍耶和罗巴切夫斯基独立重新发现。他还拒绝了多个学术机构的频繁邀请，包括柏林大学，因为他厌倦城市生活——\"哥廷根虽然小，但有天文台就够了\"。他母亲晚年由他亲自照料，母子感情极深，母亲活到97岁。",
            "anecdotes_en": "Gauss was extremely demanding of his own work — his motto was \"Pauca sed matura\" (few, but ripe). He refused to publish his discoveries in non-Euclidean geometry, fearing \"the clamor of the Boeotians\" (conservative critics). These works were independently rediscovered by Bolyai and Lobachevsky after his death. He repeatedly declined offers from other institutions, including the University of Berlin, because he disliked city life — \"Göttingen may be small, but it has an observatory, and that is enough.\" He cared for his elderly mother himself in his later years; their bond was deep, and she lived to age 97.",
        },
        "fourier": {
            "name": "约瑟夫·傅里叶",
            "name_en": "Joseph Fourier",
            "years": "1768–1830",
            "icon": "F",
            "contributions": "傅里叶级数、傅里叶变换、热传导方程",
            "contributions_en": "Fourier series, Fourier transform, heat equation",
            "story": "傅里叶在研究热传导时提出了一个疯狂的想法：任何周期函数都可以表示成正弦波和余弦波的无穷和。当时绝大多数数学家认为这不可能，但他坚持了自己的发现。今天，傅里叶变换是现代世界最重要的数学工具之一——MP3音频压缩、JPEG图片、5G通信、量子力学都依赖它。",
            "story_en": "While studying heat conduction, Fourier proposed a radical idea: any periodic function can be expressed as an infinite sum of sine and cosine waves. Most mathematicians of the time thought this was impossible, but he persisted. Today, the Fourier transform is one of the most important mathematical tools in the modern world — MP3 audio compression, JPEG images, 5G communications, and quantum mechanics all depend on it.",
            "quote": "对自然的深入研究是数学发现最肥沃的土壤。",
            "exhibits": ["series", "derivatives"],
            "bio": "1768年生于法国欧塞尔。父母早逝，幼年入军校。法国大革命期间加入革命委员会，因罗伯斯庇尔倒台险些被送上断头台。1798年随拿破仑远征埃及，被任命为下埃及总督。1807年在格勒诺布尔担任地方长官期间完成《热的解析理论》。1817年当选法国科学院院士。1830年在巴黎去世。",
            "bio_en": "Born in 1768 in Auxerre, France. Orphaned young, he entered a military school. During the French Revolution he joined the Revolutionary Committee and narrowly escaped the guillotine after Robespierre's fall. In 1798 he accompanied Napoleon on the Egyptian expedition and was appointed Governor of Lower Egypt. While serving as prefect in Grenoble in 1807, he completed his Analytical Theory of Heat. He was elected to the French Academy of Sciences in 1817. He died in Paris in 1830.",
            "ideas": "傅里叶级数：任何周期函数（无论多么\"不光滑\"）都可以表示为不同频率正弦波的无穷和——即 f(x) = a₀/2 + Σ(a_n cos(nx) + b_n sin(nx))。傅里叶变换：将时间域的信号转换到频率域——这是现代信号处理、图像处理、音频编码的数学根基。热传导方程：建立了热在固体中传播的偏微分方程 ∂u/∂t = α∇²u，并发明了分离变量法来求解。更深远的影响：揭示了\"时域\"和\"频域\"之间的深刻对偶关系，这一思想贯穿整个现代数学与工程学。",
            "ideas_en": "Fourier series: any periodic function (no matter how \"rough\") can be expressed as an infinite sum of sine waves of different frequencies — i.e., f(x) = a₀/2 + Σ(a_n cos(nx) + b_n sin(nx)). Fourier transform: converts a signal from the time domain to the frequency domain — the mathematical foundation of modern signal processing, image processing, and audio coding. Heat equation: established the partial differential equation ∂u/∂t = α∇²u governing heat propagation in solids, and invented separation of variables to solve it. Broader impact: revealed the profound duality between the \"time domain\" and \"frequency domain\" — a concept that permeates all of modern mathematics and engineering.",
            "anecdotes": "傅里叶坚信\"沙漠中的热量促进文明\"——拿破仑远征埃及时他被任命为下埃及总督，在沙漠中他深入研究了热现象。他后来的热学理论深受埃及经历启发。他的房间里总是保持极高的温度，常年穿着沉重的大衣工作——现代医学史家推测他患有甲状腺功能亢进。拉普拉斯和拉格朗日最初激烈反对他的级数理论——拉格朗日当面对他说\"不连续函数不可能用连续的正弦波表示\"。傅里叶后来出版的《热的解析理论》被誉为\"一首伟大的数学诗篇\"。",
            "anecdotes_en": "Fourier believed that \"the heat of the desert advances civilization\" — when Napoleon invaded Egypt, Fourier was appointed Governor of Lower Egypt, and his deep study of heat phenomena there profoundly inspired his later thermal theory. He kept his rooms at extremely high temperatures and always wore a heavy coat while working — modern medical historians suspect he suffered from hyperthyroidism. Laplace and Lagrange initially fiercely opposed his series theory — Lagrange told him to his face that \"a discontinuous function cannot be represented by continuous sine waves.\" Fourier's published Analytical Theory of Heat was later hailed as \"a great mathematical poem.\"",
        },
        "ramanujan": {
            "name": "斯里尼瓦瑟·拉马努金",
            "name_en": "Srinivasa Ramanujan",
            "years": "1887–1920",
            "icon": "R",
            "contributions": "无穷级数、整数分拆、模形式、π的公式",
            "contributions_en": "Infinite series, integer partitions, modular forms, formulas for π",
            "story": "拉马努金出身于印度贫困家庭，几乎完全靠自学。他用粉笔在石板上计算，在笔记本上记录了近4000个惊人的公式——没有任何证明，但他声称\"女神在梦中告诉他这些结果\"。1913年他写信给英国数学家哈代，哈代看后大惊失色，说\"这些公式一定是对的，因为没有人能编造出这么复杂的东西\"。他32岁英年早逝，但他的笔记至今仍然在被研究。",
            "story_en": "Ramanujan came from a poor Indian family and was almost entirely self-taught. He calculated on slate with chalk and recorded nearly 4,000 astonishing formulas in his notebooks — without any proofs, claiming \"the goddess revealed them to me in dreams.\" In 1913 he wrote to the British mathematician G. H. Hardy, who was stunned and said, \"These formulas must be true, because no one could have the imagination to invent something so complicated.\" He died young at 32, but his notebooks are still being studied today.",
            "quote": "一个方程对我没有意义，除非它表达的是上帝的思想。",
            "exhibits": ["series", "integrals"],
            "bio": "1887年生于印度泰米尔纳德邦的贫困婆罗门家庭。因痴迷数学荒废其他科目，两次失去大学奖学金。没有大学文凭，在港口做月薪20卢比的抄写员糊口。1913年，26岁的他写信给剑桥大学哈代教授，附上120个惊人公式。哈代邀请他到剑桥，一战期间赴英，被三一学院录取。英国寒冷潮湿的气候严重损害了他的健康。1919年返回印度，1920年病逝，年仅32岁。",
            "bio_en": "Born in 1887 in a poor Brahmin family in Tamil Nadu, India. Obsessed with mathematics to the exclusion of all other subjects, he lost his university scholarships twice. With no degree, he worked as a clerk for 20 rupees a month. In 1913, at age 26, he wrote to Professor Hardy at Cambridge with 120 astonishing formulas. Hardy invited him to Cambridge; he traveled to England during World War I and was admitted to Trinity College. The cold, damp English climate severely damaged his health. He returned to India in 1919 and died in 1920 at just 32.",
            "ideas": "无穷级数大师：发现了数千个涉及π、e、zeta函数的收敛级数公式——速度极快，适合数值计算。π的计算公式：他给出了一个收敛极快的π公式（每步增加8位精度），被计算机用于将π计算到数十亿位。整数分拆理论：与哈代合作发展了精确的分拆函数 p(n) 的渐近公式，创造了\"圆法\"。模形式与模拟θ函数：他发现的一类称为\"模拟θ函数\"的对象，在80年后被证明与弦理论中黑洞的微观状态计数直接相关——物理学家发现拉马努金一个世纪前就已经在研究黑洞物理了。拉马努金θ函数：现在已成为现代数学和理论物理中的核心对象。",
            "ideas_en": "Master of infinite series: discovered thousands of rapidly converging series formulas involving π, e, and the zeta function — extremely fast for numerical computation. Formulas for π: gave a series for π that converges extremely rapidly (adding 8 decimal digits per term), later used by computers to calculate π to billions of digits. Integer partition theory: in collaboration with Hardy, developed asymptotic formulas for the partition function p(n) and created the \"circle method.\" Mock modular forms: a class of objects he discovered called \"mock theta functions\" was shown 80 years later to be directly related to the microscopic state counting of black holes in string theory — physicists discovered that Ramanujan had been studying black hole physics a century earlier. Ramanujan theta functions: now central objects in modern mathematics and theoretical physics.",
            "anecdotes": "1729的故事：哈代去医院探病时说出租车牌号1729\"很枯燥\"，拉马努金立即反驳：\"不，1729很有趣——它是能用两种方式表示成两个正整数的立方和的最小正整数：1³+12³=9³+10³。\"这个数字此后被称为\"哈代-拉马努金数\"。他声称印度女神纳玛吉里（Namagiri）在梦中给他启示公式——每天凌晨他记下梦中出现的公式，早晨再验证。由于穷得买不起纸，他在石板上用粉笔演算，用胳膊肘擦掉重写，以至于肘部永远有一层石灰印记。他的笔记本直到2012年才被完全数字化，至今数学家仍在不断从中发现新的深刻结果。",
            "anecdotes_en": "The number 1729: when Hardy visited Ramanujan in the hospital and remarked that the taxi number 1729 was \"rather dull,\" Ramanujan immediately countered: \"No, it is a very interesting number — it is the smallest positive integer expressible as the sum of two positive cubes in two different ways: 1³+12³ = 9³+10³.\" This number became known as the \"Hardy-Ramanujan number.\" He claimed that the Hindu goddess Namagiri revealed formulas to him in dreams — he would write them down upon waking each morning and verify them later. Too poor to buy paper, he calculated on slate with chalk, erasing with his elbow, which was permanently covered in chalk powder. His notebooks were not fully digitized until 2012, and mathematicians are still discovering new deep results from them.",
        },
        "cauchy_weierstrass": {
            "name": "柯西 & 魏尔斯特拉斯",
            "name_en": "Cauchy & Weierstrass",
            "years": "1789–1857 / 1815–1897",
            "icon": "C",
            "contributions": "ε-δ极限定义、分析严密化、复分析",
            "contributions_en": "ε-δ definition of limits, rigorous analysis, complex analysis",
            "story": "牛顿和莱布尼茨发明微积分后，\"无穷小量\"到底是不是零这个问题困扰了数学家们近200年。柯西率先用不等式而非模糊的\"无穷小\"来定义极限。魏尔斯特拉斯进一步完善了这个方法，发明了著名的 ε-δ 定义。从此，微积分终于有了牢不可破的逻辑基础——数学分析诞生了。",
            "story_en": "After Newton and Leibniz invented calculus, the question of whether \"infinitesimals\" were really zero troubled mathematicians for nearly 200 years. Cauchy was the first to define limits using inequalities instead of vague \"infinitesimals.\" Weierstrass further refined this approach, inventing the famous ε-δ definition. From that point on, calculus finally had a solid logical foundation — mathematical analysis was born.",
            "quote": "数学的本质不在于数字，而在于严密的逻辑推理。 — 魏尔斯特拉斯",
            "exhibits": ["limits"],
            "bio": "柯西（1789–1857）：生于法国大革命前夕的巴黎，工程师出身，后任巴黎综合理工学院教授。坚定的天主教徒和保皇党人。1830年七月革命后因拒绝宣誓效忠新政府而流亡布拉格。一生发表约800篇论文，仅次于欧拉。魏尔斯特拉斯（1815–1897）：生于德国，父亲强迫他学法律。他自学数学，在偏僻中学当教师15年，期间独立完成了大量分析学工作。1856年41岁时终于被柏林大学聘为教授，大器晚成的典范。",
            "bio_en": "Cauchy (1789–1857): born in Paris on the eve of the French Revolution, trained as an engineer, later professor at the École Polytechnique. A devout Catholic and royalist. After the 1830 July Revolution, he refused to swear allegiance to the new government and went into exile in Prague. Published about 800 papers in his lifetime, second only to Euler. Weierstrass (1815–1897): born in Germany, forced by his father to study law. He taught himself mathematics and spent 15 years teaching at a remote secondary school, independently completing major work in analysis. In 1856, at age 41, he was finally appointed professor at the University of Berlin — a classic late bloomer.",
            "ideas": "柯西的极限定义：在《分析教程》（1821）中用\"变量无限趋近固定值\"取代了模糊的无穷小概念，首次为微积分提供了逻辑基础。复变函数论：柯西发现了复函数积分的基本定理（柯西积分定理）和留数定理，奠定了复分析的基础。魏尔斯特拉斯的ε-δ语言：用精确的不等式表述极限——\"对任意ε>0，存在δ>0使得...\"——这是现代分析学的标准语言，至今不变。魏尔斯特拉斯函数：构造了处处连续但处处不可导的函数，震惊了整个数学界——它证明了连续并不等于可导。魏尔斯特拉斯逼近定理：任何连续函数都可以用多项式一致逼近——这是函数逼近论的起点。",
            "ideas_en": "Cauchy's limit definition: in his 1821 Cours d'Analyse, he replaced the vague concept of \"infinitesimals\" with \"a variable approaching a fixed value,\" providing the first logical foundation for calculus. Complex analysis: Cauchy discovered the fundamental theorem of complex integration (Cauchy's integral theorem) and the residue theorem, laying the foundation for complex analysis. Weierstrass's ε-δ language: precise inequality formulation of limits — \"for any ε>0, there exists δ>0 such that...\" — the standard language of modern analysis, unchanged to this day. Weierstrass function: constructed a function that is continuous everywhere but differentiable nowhere, shocking the entire mathematical world — it proved that continuity does not imply differentiability. Weierstrass approximation theorem: any continuous function can be uniformly approximated by polynomials — the starting point of approximation theory.",
            "anecdotes": "魏尔斯特拉斯在偏僻中学教授数学、物理、植物学、地理、体育共5门学科，每周28节课。他后来回忆说：\"在那些年里，我不得不把大部分精力花在教学上，但我的数学思想从未停止。\"他每晚批改完学生作业后继续钻研数学到凌晨，完全与世隔绝地进行原创研究。1841年他独立发现了椭圆函数的级数展开，但未投稿发表。直到1854年他发表一篇关于阿贝尔函数的论文后声名鹊起——柯尼斯堡大学立即授予他名誉博士学位，柏林大学随后聘为正教授。这一年他已41岁，从中学教师一跃成为欧洲数学界的核心人物。",
            "anecdotes_en": "Weierstrass taught five subjects at a remote secondary school — mathematics, physics, botany, geography, and physical education — totaling 28 hours per week. He later recalled, \"In those years, I had to devote most of my energy to teaching, but my mathematical thoughts never stopped.\" Every night after grading homework, he would continue his mathematical research until dawn, working in complete isolation. In 1841 he independently discovered the series expansion of elliptic functions but never submitted it for publication. When he finally published a paper on Abelian functions in 1854, he shot to fame — the University of Königsberg immediately awarded him an honorary doctorate, and the University of Berlin appointed him full professor. At 41, he had gone from a secondary school teacher to the central figure of European mathematics.",
        },
        "fermat": {
            "name": "皮埃尔·德·费马",
            "name_en": "Pierre de Fermat",
            "years": "1607–1665",
            "icon": "Fp",
            "contributions": "费马大定理、解析几何、概率论、数论",
            "contributions_en": "Fermat's Last Theorem, analytic geometry, probability theory, number theory",
            "story": "费马是\"业余数学家之王\"——他的职业是法官，数学只是业余爱好。但他在数论、解析几何、概率论、微积分等多个领域做出了开创性贡献。他在《算术》一书页边写下的那条著名注释——\"我确信我已发现了一种美妙的证明，但这页边太窄了，写不下\"——困扰了数学家358年，直到1994年才由安德鲁·怀尔斯最终证明。",
            "story_en": "Fermat was the \"prince of amateurs\" — his profession was magistrate, and mathematics was just a hobby. Yet he made groundbreaking contributions to number theory, analytic geometry, probability theory, and calculus. His famous marginal note in Diophantus's Arithmetica — \"I have discovered a truly marvelous proof of this, which this margin is too narrow to contain\" — baffled mathematicians for 358 years, until Andrew Wiles finally proved it in 1994.",
            "quote": "我确信我已发现了一种美妙的证明，但这页边太窄了，写不下。",
            "exhibits": ["derivatives", "integrals", "series"],
            "bio": "1607年生于法国博蒙-德洛马涅。毕业于奥尔良大学法律系，终身从事地方法官工作。他在业余时间疯狂地研究数学——白天审案，晚上演算。与同时代数学家通过书信交流，但几乎不公开发表。1637年与笛卡尔各自独立发现了解析几何的基本原理。与帕斯卡通信创立了概率论的数学基础。1665年在卡斯特尔去世。",
            "bio_en": "Born in 1607 in Beaumont-de-Lomagne, France. He graduated in law from the University of Orléans and worked as a magistrate for his entire life. In his spare time, he pursued mathematics with passion — judging cases by day, calculating by night. He corresponded with contemporary mathematicians but almost never published. In 1637, independently of Descartes, he discovered the fundamentals of analytic geometry. Together with Pascal, he founded the mathematical theory of probability. He died in Castres in 1665.",
            "ideas": "费马大定理：方程 x^n + y^n = z^n 在 n>2 时没有正整数解——最简单的陈述，最艰难的问题。解析几何先驱：1636年独立于笛卡尔发现直线和曲线的方程表示法——\"费马坐标\"比笛卡尔的直角坐标系更早。变分法的起点：提出了光学中\"费马原理\"——光在两点间总是走所需时间最短的路径——这是变分法的最早表述。费马小定理：如果p是素数且a不能被p整除，则a^(p-1) ≡ 1 (mod p)——这是现代密码学（RSA算法）的基础定理之一。无穷递降法：费马发明了一种强有力的反证技巧——假设存在一个最小的反例，然后构造出更小的反例导致矛盾。",
            "ideas_en": "Fermat's Last Theorem: the equation x^n + y^n = z^n has no positive integer solutions for n > 2 — the simplest statement, the most difficult problem. Pioneer of analytic geometry: independently of Descartes, he discovered in 1636 that lines and curves can be represented by equations — his \"Fermat coordinates\" preceded Descartes's Cartesian coordinate system. Origin of calculus of variations: proposed \"Fermat's principle\" in optics — light always takes the path of least time between two points — the earliest formulation of the calculus of variations. Fermat's Little Theorem: if p is prime and a is not divisible by p, then a^(p-1) ≡ 1 (mod p) — a foundational theorem of modern cryptography (the RSA algorithm). Infinite descent: Fermat invented a powerful proof by contradiction — assuming a minimal counterexample exists, then constructing a smaller one to reach a contradiction.",
            "anecdotes": "费马最著名的举动是喜欢写信挑衅全欧洲的数学家——他会宣称自己证明了一个定理但不公布证明过程，让对方尝试证明。\"无穷递降法\"就是他在1659年写给卡尔卡维的信中首次描述的——信末他写道：\"但我没有时间详述了。\"如果他在1621年的时候真的拿出了证明方法，358年后怀尔斯的证明用了一个世纪的现代数学成果（包括模形式、椭圆曲线、伽罗瓦表示等），才终于完成了费马的\"美妙证明\"——这说明费马那页边可能根本写不下。有趣的是，虽然他的大定理是最有名的未解猜想，但他一生中只把很少的作品公开——死后他的儿子才把他的手稿整理出版。",
            "anecdotes_en": "Fermat's most famous habit was writing letters to provoke mathematicians across Europe — he would announce he had proven a theorem but refused to share the proof, challenging others to prove it themselves. The \"infinite descent\" method was first described in his 1659 letter to Carcavi, which ended: \"But I have no time to elaborate.\" 358 years later, Wiles's proof used a full century of modern mathematics (modular forms, elliptic curves, Galois representations) to finally complete Fermat's \"marvelous proof\" — suggesting the margin truly couldn't contain it. Interestingly, although his Last Theorem is his most famous unsolved conjecture, he published very little during his lifetime — his son compiled and published his manuscripts after his death.",
        },
    }

    # ── Navigation tree — Museum floor plan ──
    nav_tree: list[dict] = [
        {
            "section": "序幕",
            "entries": [
                {"label": "首页", "route": "/"},
            ],
        },
        {
            "section": "微积分",
            "entries": [
                {"label": "展区", "route": "/gaoshu"},
                {"label": "极限 — 无限逼近", "route": "/exhibit/limits"},
                {"label": "导数 — 瞬间变化率", "route": "/exhibit/derivatives"},
                {"label": "积分 — 和的极限", "route": "/exhibit/integrals"},
                {"label": "无穷级数 — 无限拼图", "route": "/exhibit/series"},
                {"label": "多元微积分 — 从平面到空间", "route": "/exhibit/multivariable"},
            ],
        },
        {
            "section": "数学家长廊",
            "entries": [
                {"label": "牛顿 & 莱布尼茨", "route": "/mathematicians/newton"},
                {"label": "欧拉", "route": "/mathematicians/euler"},
                {"label": "高斯", "route": "/mathematicians/gauss"},
                {"label": "傅里叶", "route": "/mathematicians/fourier"},
                {"label": "柯西 & 魏尔斯特拉斯", "route": "/mathematicians/cauchy_weierstrass"},
                {"label": "拉马努金", "route": "/mathematicians/ramanujan"},
                {"label": "费马", "route": "/mathematicians/fermat"},
            ],
        },
        {
            "section": "展区",
            "entries": [
                {"label": "数学之美", "route": "/gallery"},
                {"label": "函数工坊", "route": "/workshop"},
                {"label": "分形探索", "route": "/fractal"},
                {"label": "线性代数", "route": "/exhibit/linear-algebra"},
            ],
        },
        {
            "section": "工具",
            "entries": [
                {"label": "练习", "route": "/practice/limits"},
                {"label": "错题本", "route": "/error-log"},
            ],
        },
    ]

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8", "extra": "ignore"}
    """pydantic model config"""


def get_settings_dict() -> dict:
    """Return settings as plain dict for Jinja2 template context.
    Must convert nested dicts and non-serializable values to plain types."""
    s = settings
    gaoshu_subtopics = sorted(
        [(k, v) for k, v in s.exhibits.items() if k != "gaoshu"],
        key=lambda kv: kv[1].get("order", 99)
    )
    return {
        "app_name": s.app_name,
        "app_subtitle": s.app_subtitle,
        "debug": s.debug,
        "content_dir": s.content_dir,
        "data_dir": s.data_dir,
        "deepseek_model": s.deepseek_model,
        "exhibits": settings.exhibits,
        "difficulty": s.difficulty,
        "nav_tree": s.nav_tree,
        "gaoshu_subtopics": gaoshu_subtopics,
    }


def validate_settings():
    """Validate required settings. Raises RuntimeError if invalid.
    Skips in test/CI environments where real keys aren't needed."""
    is_testing = os.getenv("PYTEST_CURRENT_TEST") or os.getenv("CI") == "true"
    if is_testing:
        return
    if not Settings().debug:
        jwt_key = os.getenv("JWT_SECRET_KEY", "")
        if not jwt_key:
            raise RuntimeError(
                "JWT_SECRET_KEY environment variable is required in non-debug mode. "
                "Generate one with: python -c \"import secrets; print(secrets.token_urlsafe(32))\""
            )
    if not os.getenv("DEEPSEEK_API_KEY", ""):
        raise RuntimeError(
            "DEEPSEEK_API_KEY environment variable is required. "
            "Set it to your DeepSeek API key (OpenAI-compatible endpoint)."
        )


# Singleton instance — validated lazily on first access
_settings_instance = None


def get_settings() -> Settings:
    global _settings_instance
    if _settings_instance is None:
        _settings_instance = Settings()
        if not _settings_instance.debug:
            validate_settings()
    return _settings_instance


settings = get_settings()
