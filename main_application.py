import uvicorn
import traceback
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import api_integration 
import reflex_controller

app = FastAPI(title="Project Reflex Host Application")

@app.middleware("http")
async def reflex_middleware(request: Request, call_next):
    try:
        response = await call_next(request)
        return response
    except Exception as exc:
        print(f"\n!!! CRASH DETECTED !!!")
        trace = traceback.format_exc()
        
        target_file = "api_integration.py"
        target_function = "fetch_user_data"
        
        print(f"Reflex Agent Initialized for: {target_file}:{target_function}")
        
        try:
            reflex_brain = reflex_controller.ReflexBrainController()
            reflex_brain.heal_api_integration(trace, target_file, target_function)
        except Exception as e:
            print(f"Fatal Error: Reflex Arc failed: {e}")
            return JSONResponse(status_code=500, content={"message": "System failure during healing."})

        # --- THE FIX: Safely Hot-Reload the newly written code ---
        import importlib
        importlib.reload(api_integration)

        try:
            print("\nRunning healed logic post-validation...")
            # Run the request again with the newly reloaded code
            re_run_response = api_integration.fetch_user_data("123")
            print("System Healed: Request succeeded after autonomous patch.")
            
            return JSONResponse(status_code=200, content={"message": "Project Reflex Healed this application automatically.", "healed_data": re_run_response})
            
        except Exception as retry_exc:
            print(f"Healing verification failed: {retry_exc}")
            return JSONResponse(status_code=500, content={"message": "Reflex attempt failed verification.", "error": str(retry_exc)})

@app.get("/get-user-profile/{user_id}")
async def get_user_profile(user_id: str):
    user_data = api_integration.fetch_user_data(user_id)
    return {"status": "success", "profile": user_data}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)