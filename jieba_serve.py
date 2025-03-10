import ray
from ray import serve
from module_a import segment_text
from fastapi import FastAPI, Request
import json

app = FastAPI()

@ray.remote
@serve.deployment(num_replicas=1)
@serve.ingress(app)
class JiebaSegmentorService:
    def __init__(self, config=None):
        if config is None:
            config = {}
        self.name = "jieba-segmentor"
        self.language = config.get("language", "chinese")
        print("Initialized Jieba Segmentor Service")

    @app.post("/segment")
    async def segment(self, request: Request):
        data = await request.json()
        text = data.get("text", "")
        mode = data.get("mode", "default")
        user_dict = data.get("user_dict", None)
        
        result = segment_text(text, mode, user_dict)
        return result
    
    @app.get("/")
    async def root(self):
        return {"status": "Jieba Segmentor Service is running"}

deployment = JiebaSegmentorService.bind()
serve.run(deployment, route_prefix="/")

if __name__ == "__main__":
    # 测试模式下直接启动服务
    serve.run(deployment, route_prefix="/")

