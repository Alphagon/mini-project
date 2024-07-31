from fastapi import FastAPI, HTTPException
import boto3
import json
import uvicorn

endpoint_name = "huggingface-pytorch-inference-2024-07-30-15-54-31-943"
boto_session = boto3.Session(region_name='ap-south-1')
sagemaker_runtime = boto_session.client('sagemaker-runtime')

app = FastAPI()

@app.post("/predict/")
async def predict(input_text: str):
    input_data = {"inputs": input_text}

    payload = json.dumps(input_data)
    response = sagemaker_runtime.invoke_endpoint(
    EndpointName=endpoint_name,
    Body=payload,
    ContentType='application/json'
    )

    result = response['Body'].read().decode('utf-8')
    result = json.loads(result)
    return result

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)