# dynamic_models.py
import datetime
from typing import Optional, List, Dict, Any, Type, Tuple, Union, Mapping
from pydantic import BaseModel, Field, EmailStr, create_model


def odoo_field_to_pydantic_type(field_info: dict) -> tuple:
    """
    Mapeia tipos de campos do Odoo para tipos Pydantic, estendido para cobrir mais tipos.
    """
    odoo_type = field_info['type']
    pydantic_type = (str, Field(default=None))  # Default para tipos não mapeados especificamente

    # Mapeamento expandido
    type_mapping = {
        'char': (str, Field(default=None)),
        'text': (str, Field(default=None)),
        'html': (str, Field(default=None)),
        'boolean': (bool, Field(default=False)),
        'integer': (Optional[int], Field(default=None)),
        'float': (float, Field(default=None)),
        'date': (Optional[datetime.date], Field(default=None)),
        'datetime': (Optional[datetime.datetime], Field(default=None)),
        'selection': (str, Field(default=None)),  # Assumindo que a seleção retorna uma string
        'many2one': (Optional[int], Field(default=None)),  # ID do registro relacionado
        'one2many': (List[int], Field(default_factory=list)),  # Lista de IDs para relacionamentos one2many
        'many2many': (List[int], Field(default_factory=list)),  # Lista de IDs para relacionamentos many2many
        'binary': (Optional[str], Field(default=None)),  # Dados binários codificados em base64
        'monetary': (float, Field(default=None)),  # Tratado como float
        'reference': (str, Field(default=None)),  # Referência a outro registro como "model,id"
        'email': (Optional[EmailStr], Field(default=None)),  # Campo de e-mail validado
        'json': (Dict[str, Any], Field(default_factory=dict)),  # ou (List[Any], Field(default_factory=list)) se aplicável
        # Adicione outros tipos conforme necessário
    }

    return type_mapping.get(odoo_type, (str, Field(default=None)))

def generate_pydantic_model_from_odoo(model_name: str, odoo: Any) -> Type[BaseModel]:
    """
    Gera um modelo Pydantic dinamicamente com base nos campos do modelo do Odoo.
    """
    fields_info = odoo.env[model_name].fields_get()

    pydantic_fields = {
        field: odoo_field_to_pydantic_type(info)
        for field, info in fields_info.items()
    }

    dynamic_model = create_model(model_name, **pydantic_fields, __base__=BaseModel)
    return dynamic_model