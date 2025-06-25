from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from fastapi import APIRouter, UploadFile, File, HTTPException
import pandas as pd
from io import BytesIO
from typing import List
import requests

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
        
    return StreamingResponse(
        buffer,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": "attachment; filename=modificado.xlsx"}
    )
 
@app.post("/multi_file_xlsx")
async def converte_multiplos_arquivos(files: List[UploadFile] = File(...)):
    dataframes = []

    for idx, file in enumerate(files):
        df = pd.read_excel(file.file)
        df.insert(0, "Origem", f"Arquivo {idx + 1}")
        dataframes.append(df)

    df_concatenado = pd.concat(dataframes, ignore_index=True)

    buffer = BytesIO()
    with pd.ExcelWriter(buffer, engine="xlsxwriter") as writer:
        df_concatenado.to_excel(writer, index=False)
    buffer.seek(0)

    return StreamingResponse(
        buffer,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": "attachment; filename=concatenado.xlsx"}
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

@app.post("/concat_excel_from_urls")
def concat_excel_from_urls(urls: List[str]):
    dfs = []

    for idx, url in enumerate(urls):
        try:
            response = requests.get(url)
            response.raise_for_status()

            df = pd.read_excel(BytesIO(response.content))
            df["Arquivo"] = f"Arquivo {idx+1}"  # Identificador da origem
            dfs.append(df)
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Erro ao processar URL {url}: {str(e)}")

    if not dfs:
        raise HTTPException(status_code=400, detail="Nenhum arquivo válido foi processado.")

    df_concat = pd.concat(dfs, ignore_index=True)

    # Prepara para download
    output = BytesIO()
    with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
        df_concat.to_excel(writer, index=False)
    output.seek(0)

    return StreamingResponse(
        output,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": "attachment; filename=arquivos_concatenados.xlsx"}
    )
