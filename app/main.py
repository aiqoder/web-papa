from .api import app

if __name__ == "__main__":
    import uvicorn
    
    # 直接运行应用
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
