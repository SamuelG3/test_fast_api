from fastapi import FastAPI
from fastapi.responses import StreamingResponse
import pandas as pd
from io import BytesIO
 
app = FastAPI()
 
@app.get("/ready")
async def ready():
   return "READY"


@app.post("/fatura_xlsx")
async def converte-arquivo(file: UploadFile = File(...)):
    try:
        df = pd.read_excel(file.file)
        df.insert(2, "c", "coluna nova")
        # Write dataframe to a BytesIO buffer as Excel
        buffer = BytesIO()
        with pd.ExcelWriter(buffer, engine="xlsxwriter") as writer:
            df.to_excel(writer, index=False)
        buffer.seek(0)
       
        return StreamingResponse(
               buffer,
               media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
               headers={"Content-Disposition": "attachment; filename=dummy.xlsx"}
           )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
     
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
