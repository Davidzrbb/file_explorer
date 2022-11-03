from module_vertica import vertica_manager
from fastapi import Depends, HTTPException, APIRouter
from module_vertica.crud import get_files
from module_vertica.modele import FileInVertica
from sqlalchemy import text
from vertica_python.vertica.cursor import Cursor
from schema.data_server import InstanceFluxRequest, ResponseModel, CamelCaseModel
import http3
import requests


def add_app_routes(router):
    invoices_callback_router = APIRouter()
    client = http3.AsyncClient()

    @router.get("/")
    async def find_all(db: Cursor = Depends(vertica_manager.get_db_generator)):
        return {"value": db.execute("select * from R1ODSGL1.explorator_virtual_dir").all()}

    @router.get("/name")
    async def find_by_name(val: str, db: Cursor = Depends(vertica_manager.get_db_generator)):
        db.execute(
            "update R1ODSGL1.explorator_virtual_dir set name ='/TEST/TEST1', pattern = '/app/raphael/scan-files/*/main.py' WHERE idauto = 250001")
        db.execute(
            "update R1ODSGL1.explorator_virtual_dir set name ='/TEST/TEST1/TEST2/TEST3', pattern = '/app/raphael/scan-files/*/main.py' WHERE idauto = 250006")
        list_folder_value: list[ResponseModel] = list()
        list_row: list[InstanceFluxRequest] = db.execute(
            "select * from R1ODSGL1.explorator_virtual_dir where name ilike :val", {"val": val + "%"}).all()

        if not list_row:
            raise HTTPException(status_code=404, detail="This path was not found")
        for flux_request in list_row:
            # si le path reçu est identique on envoie le pattern à l'api externe et on ajoute
            if flux_request.name == val:
                list_folder_value.append(list_folder(flux_request))
            else:
                # si le path de la bdd contient le path mais pas exact reçu on ajoute le path avec n+1
                response_model = ResponseModel()
                split_tmp = flux_request.name.split(val + "/")
                response_model.name = val + split_tmp[0].split("/")[0]
                response_model.type = "folder"
                response_model.list_sub_obj = None
                response_model.last_modified_date = None
                response_model.creation_date = None
                list_folder_value.append(response_model)
        return {list_folder_value}

    def list_folder(flux_request: InstanceFluxRequest):
        host = flux_request.host
        pattern = flux_request.pattern
        recursive = flux_request.recursive_search
        open_archive = flux_request.also_search_in_archive

        get_test_url = f"http://{host}/list_directory_pattern?pattern={pattern}&recursive={recursive}&open_archive={open_archive}"
        test_get_response = requests.get(get_test_url)
        if test_get_response.status_code == 200:
            return test_get_response.json()
        raise HTTPException(status_code=404, detail="Directory not found")
