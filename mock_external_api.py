import uvicorn
from fastapi import FastAPI, HTTPException, Request

app = FastAPI(title="Mock External Provider API")

USERS_DB = {
    "123": {"name": "Alice Smith", "plan": "premium"},
    "456": {"name": "Bob Jones", "plan": "basic"},
}

@app.post("/v1/get-user", status_code=200) 
async def get_user_v1_broken(request: Request):
    try:
        data = await request.json()
        user_id = data.get("account_id") 
        
        if user_id in USERS_DB:
            return USERS_DB[user_id]
        
        # We raise the exact error here so the agent can read it
        raise HTTPException(status_code=400, detail="Bad Request: Missing account_id parameter")
        
    except HTTPException:
        raise # Let the HTTP error pass through cleanly
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid Request: {e}")

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8001)