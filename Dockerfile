# 가벼운 파이썬 버전 사용
FROM python:3.11-slim

# 로그가 지연 없이 바로 찍히도록 설정 (에러 확인용)
ENV PYTHONUNBUFFERED=True

# 작업 폴더 설정
WORKDIR /app

# 패키지 설치
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 소스 코드 복사
COPY . .

# [핵심 수정]
# 1. 호스트를 무조건 0.0.0.0으로 엽니다 (localhost 아님)
# 2. 포트를 8080으로 고정합니다.
# 3. src 폴더 안의 server.py 파일의 app 객체를 실행합니다.
CMD ["uvicorn", "src.server:app", "--host", "0.0.0.0", "--port", "8080"]
