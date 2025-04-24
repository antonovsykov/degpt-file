FROM python:3.11-slim-bookworm as base

WORKDIR /app/fileanalysis

COPY . .

RUN pip3 install uv

# 安装 Python 依赖
RUN uv pip install --system -r requirements.txt --no-cache-dir

RUN apt-get update && \
    apt-get install -y \
    wget \
    curl \
    libreoffice \
    # 清理缓存以减小镜像体积
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

EXPOSE 8080

HEALTHCHECK CMD curl --silent --fail http://localhost:8080/health | jq -e '.status == true' || exit 1

# 时区设置
ENV TZ=Asia/Shanghai
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

CMD [ "bash", "start.sh"]