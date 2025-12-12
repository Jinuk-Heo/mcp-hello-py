import os
import requests
from datetime import datetime, timedelta
from mcp.server.fastmcp import FastMCP

# 1. 서버 이름 설정
mcp = FastMCP("weather-server")

# ==========================================
# ★여기에 공공데이터포털에서 받은 [Decoding] 인증키를 붙여넣으세요★
API_KEY = "e35d5d8c7a847be32d2b7f1b771a7e50789b899b263eae9999ed43ae6a06221a"
# ==========================================

@mcp.tool()
def get_korea_weather(nx: int, ny: int) -> str:
    """
    특정 위치(좌표)의 현재 기온과 날씨를 조회합니다. 
    서울 강남구 예시: nx=61, ny=126
    """
    
    # 기상청 데이터 조회 시간 계산 (45분 이전이면 1시간 전 데이터 조회)
    now = datetime.now()
    if now.minute < 45:
        now = now - timedelta(hours=1)
    
    base_date = now.strftime("%Y%m%d")
    base_time = now.strftime("%H00")

    url = "http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getUltraSrtNcst"
    
    params = {
        'serviceKey': API_KEY,
        'pageNo': '1',
        'numOfRows': '1000',
        'dataType': 'JSON',
        'base_date': base_date,
        'base_time': base_time,
        'nx': nx,
        'ny': ny
    }

    try:
        response = requests.get(url, params=params)
        data = response.json()
        
        # 데이터 정리
        items = data['response']['body']['items']['item']
        weather_info = []
        
        for item in items:
            category = item['category']
            val = item['obsrValue']
            
            if category == 'T1H':
                weather_info.append(f"기온: {val}℃")
            elif category == 'REH':
                weather_info.append(f"습도: {val}%")
            elif category == 'RN1':
                weather_info.append(f"1시간 강수량: {val}mm")

        result = " | ".join(weather_info)
        return f"현재 날씨 정보입니다: {result}"

    except Exception as e:
        return f"죄송합니다. 날씨 정보를 가져오는데 실패했습니다. (에러: {str(e)})"

@mcp.tool()
def say_hello(name: str) -> str:
    return f"안녕하세요, {name}님! 저는 날씨도 알려드릴 수 있어요."
