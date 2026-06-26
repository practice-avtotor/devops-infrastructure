from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="ML Mock Service")

class AnalyzeRequest(BaseModel):
    text: str

class TranslateRequest(BaseModel):
    text: str
    target_lang: str = "ru"

@app.get("/health")
async def health():
    return {"status": "healthy", "service": "ml-mock"}

@app.post("/analyze-structure")
async def analyze_structure(request: AnalyzeRequest):
    # Эмуляция анализа структуры карты
    return {
        "status": "ok",
        "structure": {
            "operation": "12345",
            "parts": ["ABC-001", "ABC-002"],
            "quantities": {"ABC-001": 4, "ABC-002": 2}
        },
        "confidence": 0.95
    }

@app.post("/translate")
async def translate(request: TranslateRequest):
    # Эмуляция перевода
    return {
        "status": "ok",
        "original": request.text,
        "translation": f"[MOCK] {request.text} translated to {request.target_lang}",
        "target_lang": request.target_lang
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000)
