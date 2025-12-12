FROM python:3.10-slim-bookworm

# 设置工作目录
WORKDIR /app

# 复制项目文件
COPY pyproject.toml requirements.txt /app/
COPY app /app/app
COPY configs /app/configs

# 使用国内源安装Python依赖，跳过Playwright浏览器安装
RUN pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

# 暴露端口
EXPOSE 8000

# 启动命令
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
