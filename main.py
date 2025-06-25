from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from fastapi import APIRouter, UploadFile, File, HTTPException
import pandas as pd
from io import BytesIO

app = FastAPI()
 
@app.get("/ready")
async def ready():
 return "READY"

@app.post("/fatura_xlsx")
async def converte_arquivo(file: UploadFile = File(...)):
    df = pd.read_excel(file.file)
    df.insert(2, "c", "coluna nova")
   
    buffer = BytesIO()
    with pd.ExcelWriter(buffer, engine="xlsxwriter") as writer:
        df.to_excel(writer, index=False)
    buffer.seek(0)
    
    filename = 
    
    return StreamingResponse(
        buffer,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": f"attachment; filename="arquivo_modificado.xlsx"}
    )
     
@app.get("/dummy-xlsx")
async def get_dummy_xlsx():
    # Create a dummy dataframe
    df = pd.DataFrame({
        "A": [1, 2, 3],
        "B": ["x", "y", "z"]
        })
 
    # Write dataframe to a BytesIO buffer as Excel
    buffer = BytesIO()
    with pd.ExcelWriter(buffer, engine="xlsxwriter") as writer:
        df.to_excel(writer, index=False)
    buffer.seek(0)

    # Return as downloadable file
    return StreamingResponse(
        buffer,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": "attachment; filename=dummy.xlsx"}
        )
