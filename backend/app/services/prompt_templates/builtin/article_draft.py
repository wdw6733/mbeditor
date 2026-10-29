# backend/app/services/prompt_templates/builtin/article_draft.py
"""「正文起草」+「正文终稿」内置模板。

article_author 行文工序据 tone 选「正文起草」生成首版;「正文终稿」用于
二次精修(去重、收尾、节奏校准)。马鞍:硬约束(字数/语气/广告法/微信安全)
进 head_rules+tail_format 两驼峰,软引导/示例进谷底。
"""
from __future__ import annotations

from app.services.prompt_templates.schema import FewShot, PromptTemplate

# 微信公众号正文写作的硬约束摘要——头驼峰。广告法只警示不硬切(spec §8)。
_WECHAT_BODY_RULES: list[str] = [
    "你是资深公众号主笔,为中文读者写一篇可直接排版发布的推文正文。",
    "正文用 Markdown:一级标题用 `# `,小节用 `## `,段落之间空一行。",
    "全篇 700–1100 字;开头两句必须抓人,不要寒暄、不要复述标题。",
    "口语、具体、有画面;少用形容词堆叠;全文感叹号不超过 2 个。",
    "不编造数据、人名、引文;不确定的事实用模糊表述而非杜撰。",
    "避免「最/第一/唯一/国家级」等《广告法》敏感绝对化用语(仅警示,可改写规避)。",
]

# 输出格式硬约束——尾驼峰。
_BODY_TAIL_FORMAT: list[str] = [
    "只输出正文本身,不要解释、不要前后缀、不要包代码围栏。",
    "首行必须是 `# 标题`(一行,不超过 24 字),其后空一行再写正文。",
]

DRAFT_BODY = PromptTemplate(
    id="draft_body_v1",
    version=1,
    intent="正文起草",
    stage="行文",
    scene="一句话意图 + 受众 + 调子 → 整篇正文首版",
    role="资深公众号主笔",
    head_rules=_WECHAT_BODY_RULES,
    middle_guidance=[
        "先在心里搭三段式骨架(由头→展开→收束),再落笔,避免流水账。",
        "结合给定受众调整称呼与举例;结合给定调子调整句式与情绪浓度。",
    ],
    few_shots=[
        FewShot(
            user="意图:整理旧书架翻到十年前的笔记;受众:生活同好;调子:温柔治愈",
            assistant=(
                "# 十年前那本笔记,替我记得我早忘了的事\n\n"
                "纸页比记忆诚实。翻到第三页,我才想起那年冬天自己究竟在怕什么——"
                "字迹潦草得像在赶时间,却把当时的犹豫一笔笔留了下来……"
            ),
        ),
    ],
    tail_format=_BODY_TAIL_FORMAT,
    output_mode="markdown",
)

FINAL_BODY = PromptTemplate(
    id="final_body_v1",
    version=1,
    intent="正文终稿",
    stage="行文",
    scene="对已有草稿做精修:去重、强化收尾、校准节奏",
    role="资深公众号主笔(终稿校订)",
    head_rules=[
        "你在为一篇已成形的公众号草稿做终稿校订,保持原意与主标题不变。",
        "删冗余、并重复;让开头更钩人、结尾更落地(给读者一个动作或回味)。",
        "保持 Markdown 结构(`# `/`## `/空行段落);全篇字数浮动不超过原稿 ±15%。",
        "避免《广告法》绝对化用语(仅警示)。",
    ],
    middle_guidance=[
        "逐段问:这句删了读者会不会损失信息?会就留,不会就删。",
        "结尾避免「让我们」式空喊,落到一个具体的小动作或一句留白。",
    ],
    tail_format=_BODY_TAIL_FORMAT,
    output_mode="markdown",
)

# 技术文章正文写作的硬约束摘要——头驼峰。面向安卓/容器/网络方向,
# 核心是「可复现」:命令必须准确、代码必须在围栏内、配图用占位标记。
_TECH_BODY_RULES: list[str] = [
    "你是资深技术专栏作者,为中文技术读者写一篇可直接照做、可复现的技术教程正文。",
    "技术方向聚焦:安卓手机应用、容器应用(Docker/K8s)、网络技术。",
    "正文用 Markdown:一级标题用 `# `,小节用 `## `,段落之间空一行;命令与代码一律用代码围栏。",
    "全篇 1500–3000 字;每个小节都必须有实质内容——原理一句话讲透、参数逐个说明、给出预期输出、点出踩坑点;严禁空话套话和「这里不再赘述」式敷衍。",
    "所有命令/代码必须准确、真实、可直接执行:不杜撰参数、不编造输出、不写不存在的版本号或命令;给出关键命令的预期输出(摘要即可),让读者能自查成败。",
    "命令用 ```bash 围栏,配置文件/代码用对应语言围栏(```yaml / ```json / ```xml / ```dockerfile 等)。",
    "多方案对比、参数对照、版本差异、选型分析,必须用 Markdown 表格呈现(表头行 + 数据行,用 | 分列,表头下加分隔行 |---|---|),表格前后各空一行。",
    "需要配图(架构图/拓扑图/流程图)的位置,单独一行写占位标记 [[SVG|一句话中文描述该图内容]],其余文字正常写。",
    "结构建议:场景与目标 → 原理简述 → 分步操作(每步给命令 + 说明 + 预期结果)→ 验证 → 对比/进阶(适合时用表格)→ 常见坑与排错(至少 3 条真实高频坑)。",
    "不确定的命令参数用注释(#)说明,不用「应该」「大概」等模糊词糊弄读者。",
    "避免「最/第一/唯一/国家级」等《广告法》敏感绝对化用语(仅警示)。",
]

# 技术文章输出格式硬约束——尾驼峰。
_TECH_TAIL_FORMAT: list[str] = [
    "直接输出正文本身:不要输出任何思考过程、分析过程或元信息,第一个字符就是 `#`。",
    "不要解释、不要前后缀、不要包最外层代码围栏。",
    "首行必须是 `# 标题`(一行,不超过 30 字),其后空一行再写正文。",
    "命令/代码必须在各自代码围栏内,围栏外不写可执行命令。",
    "配图占位标记必须独立成行,格式严格为 [[SVG|描述]]。",
]

TECH_DRAFT_BODY = PromptTemplate(
    id="tech_draft_body_v1",
    version=1,
    intent="技术正文起草",
    stage="行文",
    scene="技术主题一句话意图 + 受众 + 调子 → 整篇可复现技术教程正文",
    role="资深技术专栏作者(专攻安卓应用 / 容器应用 / 网络技术)",
    head_rules=_TECH_BODY_RULES,
    middle_guidance=[
        "先搭「问题 → 方案 → 步骤 → 验证」骨架再落笔;每个操作步骤都要能被人照着敲。",
        "代码围栏前后各留一个空行;命令内用注释(#)解释关键参数,降低读者照搬出错的概率。",
        "对比类内容(选型/参数/版本差异)优先用 Markdown 表格;表格让文章更专业、更易扫读。",
        "配图占位只用在真正需要图示的地方(组网拓扑、请求链路、架构分层),不要滥用。",
    ],
    few_shots=[
        FewShot(
            user="意图:给 NAS 部署一个自托管容器应用并做反向代理;受众:有 Linux 基础的开发者;调子:技术干货",
            assistant=(
                "# 三步把自托管应用跑进 Docker,再用 Nginx 反代上线\n\n"
                "这套流程适合把任意容器应用稳定跑在 NAS 或 VPS 上,并挂上域名。"
                "最终效果:浏览器输入你的域名,直接访问跑在容器里的服务,全程 HTTPS。\n\n"
                "[[SVG|客户端经 Nginx 反向代理到 Docker 容器的访问链路图]]\n\n"
                "## 方案选型:反代工具怎么选\n\n"
                "| 对比维度 | Nginx | Caddy | Traefik |\n"
                "|---|---|---|---|\n"
                "| 证书自动续期 | 需配 certbot | 内置自动 | 内置自动 |\n"
                "| 配置复杂度 | 中 | 低 | 高 |\n"
                "| 适合场景 | 已有 Nginx 运维经验 | 个人轻量 | K8s 动态环境 |\n\n"
                "个人 NAS 场景选 Nginx 或 Caddy 都行;下文以 Nginx 为例。\n\n"
                "## 第一步:准备目录与编排文件\n\n"
                "先建目录,再写一个最小可用的 compose 编排:\n\n"
                "```bash\n"
                "mkdir -p ~/app && cd ~/app   # 建工作目录,compose 文件放这里\n"
                "```\n\n"
                "```yaml\n"
                "services:\n"
                "  app:\n"
                "    image: nginx:alpine      # 以 Nginx 为例,换成你的应用镜像\n"
                "    restart: unless-stopped  # 宿主机重启后容器自动拉起\n"
                "    ports:\n"
                "      - \"8080:80\"            # 宿主机 8080 -> 容器 80\n"
                "```\n\n"
                "## 第二步:启动并验证\n\n"
                "```bash\n"
                "docker compose up -d\n"
                "docker compose ps            # STATUS 应为 Up\n"
                "curl -I http://localhost:8080\n"
                "```\n\n"
                "`curl` 返回 `HTTP/1.1 200 OK` 即说明容器已正常监听;返回 `Connection refused` 先查端口映射。\n\n"
                "## 常见坑\n\n"
                "- **端口被占用**:改冒号左边的宿主机端口(如 `8081:80`),不要动容器内端口;\n"
                "- **容器反复重启**:看 `docker compose logs --tail 50`,多数是配置文件挂载路径错误;\n"
                "- **反代后拿不到真实 IP**:在 Nginx 的 server 块补 `proxy_set_header X-Real-IP $remote_addr;`。\n"
            ),
        ),
    ],
    tail_format=_TECH_TAIL_FORMAT,
    output_mode="markdown",
)

# 本模块导出的模板(供 builtin/__init__.py 聚合)。
TEMPLATES: list[PromptTemplate] = [DRAFT_BODY, FINAL_BODY, TECH_DRAFT_BODY]
