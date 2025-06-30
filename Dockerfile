# Dockerfile.cloudrun - 專為 Cloud Run 部署優化

# 使用輕量的 Python 映像檔
FROM python:3.11-slim-bullseye

# 設定工作目錄
WORKDIR /app

# 複製依賴套件列表並安裝
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 複製我們的應用程式程式碼
# 注意：我們將會修改 app/main.py 來移除 nsjail
COPY ./app /app/

# 設定環境變數，讓 Gunicorn 知道要跑哪個 app
ENV APP_MODULE="main:app"
ENV PORT=8080

# 開放 8080 port
EXPOSE 8080

# 使用 Gunicorn 啟動應用
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "--workers", "2", "main:app"] 