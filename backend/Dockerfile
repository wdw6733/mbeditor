FROM python:3.11-slim

ENV PLAYWRIGHT_BROWSERS_PATH=/ms-playwright \
    PLAYWRIGHT_DOWNLOAD_HOST=https://cdn.npmmirror.com/binaries/playwright

WORKDIR /app

# 换国内 Debian 源,加速 fonts-noto-cjk 等 apt 包下载(python:3.11-slim 用
# deb822 格式 /etc/apt/sources.list.d/debian.sources;兼容旧 sources.list)。
RUN sed -i 's|deb.debian.org|mirrors.tuna.tsinghua.edu.cn|g; s|security.debian.org|mirrors.tuna.tsinghua.edu.cn|g' \
        /etc/apt/sources.list.d/debian.sources 2>/dev/null || \
    sed -i 's|deb.debian.org|mirrors.tuna.tsinghua.edu.cn|g; s|security.debian.org|mirrors.tuna.tsinghua.edu.cn|g' \
        /etc/apt/sources.list 2>/dev/null || true

# CJK fonts first — needed for Playwright/Chromium to render Chinese <text>
# inside user-supplied SVGs during publish-time rasterization.
RUN apt-get update \
    && apt-get install -y --no-install-recommends fonts-noto-cjk \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -i https://mirrors.tencent.com/pypi/simple -r requirements.txt

# Chromium + its apt-level runtime deps for headless SVG rasterization.
# playwright 走 npmmirror 国内镜像加速下载。
RUN playwright install --with-deps chromium \
    && chmod -R a+rX /ms-playwright

COPY . .

RUN chmod +x entrypoint.sh \
    && groupadd --system app \
    && useradd --system --gid app --home-dir /app app \
    && chown -R app:app /app

USER app

CMD ["./entrypoint.sh"]
