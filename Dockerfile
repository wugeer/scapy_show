FROM python:3.12-slim

WORKDIR /app

# 安装系统依赖和wget（用于健康检查）
RUN apt-get update && apt-get install -y wget && apt-get clean

# 安装Python依赖
RUN pip install jieba ray[serve]

# 复制模块代码
COPY module_a.py /app/
COPY jieba_serve.py /app/

# 暴露Ray Serve端口
EXPOSE 8000

# 设置环境变量
ENV PYTHONUNBUFFERED=1

# 启动脚本
COPY start.sh /app/
RUN chmod +x /app/start.sh

CMD ["/app/start.sh"]

