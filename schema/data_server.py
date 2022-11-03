from pydantic import BaseModel, Field


def to_camel(string: str) -> str:
    return ''.join(word.capitalize() if idx != 0 else word for idx, word in enumerate(string.split('_')))


class CamelCaseModel(BaseModel):
    class Config:
        aliases_generator = to_camel


class InstanceFluxRequest(CamelCaseModel):
    idauto: int
    name: str
    host: str
    pattern: str
    also_search_in_archive: bool
    recursive_search: bool
