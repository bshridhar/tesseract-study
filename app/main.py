from fastapi import FastAPI, HTTPException
from app.schemas import TwoSumRequest, TwoSumResponse
from app.algorithms import two_sum

app = FastAPI(title="Two Sum API", version="0.1.0")

@app.post("/api/two-sum", response_model=TwoSumResponse)
def api_two_sum(payload: TwoSumRequest):
    nums = payload.nums
    target = payload.target
    result = two_sum(nums, target)
    if result is None:
        raise HTTPException(status_code=404, detail="No two sum solution found")
    return {"indices": result}
