from module_vertica import vertica_manager
from fastapi import Depends, HTTPException, APIRouter
from vertica_python.vertica.cursor import Cursor
from schema.data_server import InstanceFluxRequest
import http3
import requests


def add_app_routes(router):
    invoices_callback_router = APIRouter()
    client = http3.AsyncClient()

    @router.get("/")
    async def find_all(db: Cursor = Depends(vertica_manager.get_db_generator)):
        return {"value": db.execute("select * from R1ODSGL1.explorator_virtual_dir").all()}

    @router.get("/name/{val}")
    async def find_by_name(val: str, db: Cursor = Depends(vertica_manager.get_db_generator)):
        list_row: list[InstanceFluxRequest] = db.execute(
            "select * from R1ODSGL1.explorator_virtual_dir WHERE name = :val",
            {"val": val}).all()
        if not list_row:
            raise HTTPException(status_code=404, detail="This name was not found")
        for flux_request in list_row:
            list_folder_value = list_folder(flux_request)

        return {"value": list_folder_value}

    def list_folder(flux_request: InstanceFluxRequest):
        host = flux_request.host
        dirpath = "/app/raphael"
        # dirpath = flux_request.pattern.split("*")[0]
        recursive = False
        get_test_url = f"http://{host}/list_directory_path?dirpath={dirpath}&recursive={recursive}"
        if get_test_url
        test_get_response = requests.get(get_test_url).json()
        print(test_get_response)
