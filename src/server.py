import os
import uvicorn
# import requests  <-- 이 줄이 빌드 실패의 주범이었습니다. 삭제했습니다.

from a2a.server.apps import A2AStarletteApplication
from a2a.server.request_handlers import DefaultRequestHandler
from a2a.server.tasks import InMemoryTaskStore
from a2a.types import AgentCapabilities, AgentCard, AgentSkill
from agent_executor import HelloMCPAgentExecutor

# ★ 중요: 날씨 전문가는 '666155' (옛날 서버) 주소를 씁니다.
MCP_SERVER_URL = os.environ.get(
    "MCP_SERVER_URL",
    "https://mcp-hello-py-hjk-666155174404.asia-northeast3.run.app"
)

SERVICE_URL = os.environ.get("SERVICE_URL", "")

def create_agent_card(host: str, port: int) -> AgentCard:
    skill = AgentSkill(
        id="korean_greeting",
        name="Korean Greeting",
        description="인사와 날씨 정보를 제공합니다.",
        tags=["greeting", "weather"],
        examples=["안녕", "강남구 날씨 어때?"],
    )

    agent_url = SERVICE_URL if SERVICE_URL else f"http://{host}:{port}/"

    return AgentCard(
        name="Hello MCP Agent",
        description="MCP 서버와 연결된 A2A 에이전트입니다.",
        url=agent_url,
        version="1.0.0",
        default_input_modes=["text"],
        default_output_modes=["text"],
        capabilities=AgentCapabilities(streaming=True),
        skills=[skill],
    )

def main():
    host = os.environ.get("HOST", "0.0.0.0")
    port = int(os.environ.get("PORT", 8080))

    agent_card = create_agent_card(host, port)
    
    request_handler = DefaultRequestHandler(
        agent_executor=HelloMCPAgentExecutor(MCP_SERVER_URL),
        task_store=InMemoryTaskStore(),
    )

    server = A2AStarletteApplication(
        agent_card=agent_card,
        http_handler=request_handler,
    )

    uvicorn.run(server.build(), host=host, port=port)

if __name__ == "__main__":
    main()
