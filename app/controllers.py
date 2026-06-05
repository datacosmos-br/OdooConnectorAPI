"""Controllers module for the OdooConnectorAPI FastAPI application."""
# import json
# import math
from typing import Dict, Any, Optional, List, Type
from fastapi import APIRouter, HTTPException, Request, Depends, Query
from pydantic import BaseModel #, Field, EmailStr
from app.odoo_utils import odoo_connection
from app.dynamic_models import generate_pydantic_model_from_odoo

#from app.serializers import Serializer
#from app.exceptions import QueryFormatError

router = APIRouter()

@router.get("/test")
async def test_connection(odoo: Any = Depends(odoo_connection)) -> dict[str, str | Any]:
    """
    Test the connection with the Odoo service and retrieve user and company information.

    Args:
        odoo (Any): The Odoo service instance.

    Returns:
        dict[str, str | Any]: A dictionary containing the message indicating successful connection,
        user name, and company name.

    Raises:
        HTTPException: If the Odoo service is temporarily unavailable or if there is an error
        retrieving user or company information.
    """
    if not odoo:
        raise HTTPException(status_code=503, detail="Odoo service temporarily unavailable")

    try:
        user_id = odoo.env.uid
        user = odoo.env['res.users'].browse(user_id)
        user_name = user.name
        company = user.company_id.name

        return {
            "message": "Connection with Odoo established successfully.",
            "user": user_name,
            "company": company
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving user or company information: {str(e)}") from e


@router.post("/object/{model}/{function}")
async def call_model_function(model: str,        function: str,
                              request: Request,
                              odoo: Any = Depends(odoo_connection)):
    """
    Calls a model function in Odoo.

    This endpoint allows calling a specified function of a given Odoo model, using arguments and keyword arguments provided in the request body.

    Args:
        model (str): The name of the Odoo model.
        function (str): The name of the function to be called on the Odoo model.
        request (Request): The request object, expected to contain a JSON body with "args" and "kwargs".
        odoo: The Odoo client instance, obtained via dependency injection, used to perform the function call.

    Returns:
        dict: A dictionary containing the result of the function call, if successful.

    Raises:
        HTTPException: If the function call fails, an HTTP error is returned detailing the issue.
    """
    args = []
    kwargs = {}
    post = await request.json()
    if "args" in post:
        args = post["args"]
    if "kwargs" in post:
        kwargs = post["kwargs"]
    if not odoo:
        # If the Odoo client is not available, return a service unavailable error
        raise HTTPException(status_code=503, detail="Odoo service is currently unavailable.")

    try:
        # Attempt to call the specified function on the model with the provided arguments and keyword arguments
        result = odoo.execute_kw(model, function, args, kwargs)
        return {"result": result}
    except Exception as e:
        # If an error occurs during the function call, return an internal server error detailing the exception
        raise HTTPException(status_code=500, detail=f"Error calling Odoo model function: {str(e)}") from e

@router.post("/object/{model}/{rec_id}/{function}")
async def call_obj_function(model: str, rec_id: int, function: str,
                            request: Request,
                            odoo: Any = Depends(odoo_connection)):
    args = []
    kwargs = {}
    post = await request.json()
    if "args" in post:
        args = post["args"]
    if "kwargs" in post:
        kwargs = post["kwargs"]
    if not odoo:
        raise HTTPException(status_code=503, detail="Odoo service is currently unavailable.")

    try:
        obj = odoo.env[model].browse(rec_id)
        if not obj.exists():
            raise HTTPException(status_code=404, detail=f"Record with ID {rec_id} not found in model {model}.")
        if not hasattr(obj, function):
            raise HTTPException(status_code=400, detail=f"The method {function} is not available for model {model}.")
        result = getattr(obj, function)(*args, **kwargs)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e


# @router.get("/api/{model}/")
# async def get_model_data(model: str,
#                          query: str = "{*}", order: str = "", filter_condition: str = "",
#                          page: int = 1,      page_size: int = 10,
#                          odoo: Any = Depends(odoo_connection)) -> Dict[str, Any]:
#     try:
#         if filter_condition:
#             filters = json.loads(filter_condition)
#             record_ids = odoo.env[model].search(filters, order=order)
#         else:
#             record_ids = odoo.env[model].search([])
#
#         total_count = len(record_ids)
#         total_page_number = math.ceil(total_count / page_size)
#         start = page_size * (page - 1)
#         stop = start + page_size
#         # Usar os IDs para buscar os objetos de registro
#         record_objects = odoo.env[model].browse(record_ids[start:stop])
#
#         serializer = Serializer(record_objects, query, many=True)
#         data = serializer.data
#
#         return {
#             "count": total_count,
#             "prev": page - 1 if page > 1 else None,
#             "current": page,
#             "next": page + 1 if page < total_page_number else None,
#             "total_pages": total_page_number,
#             "result": data
#         }
#     except (SyntaxError, QueryFormatError) as e:
#         raise HTTPException(status_code=400, detail=str(e)) from e
#     except KeyError as e:
#         raise HTTPException(status_code=400, detail=f"The model `{model}` does not exist.") from e


# @router.get("/api/{model}/{rec_id}")
# async def get_model_rec(model: str,
#                         rec_id: int,
#                         query: str = "{*}",
#                         odoo: Any = Depends(odoo_connection)) -> Dict[str, Any]:
#     try:
#         record = odoo.env[model].browse(rec_id).ensure_one()
#         serializer = Serializer(record, query)
#         data = serializer.data
#         return dict(data)
#     except Exception as e:
#         raise HTTPException(status_code=400, detail=str(e)) from e

@router.post("/api/{model}/")
async def post_model_data(model: str,
                          data: Dict[str, Any],
                          context: Optional[Dict[str, Any]] = None,
                          odoo: Any = Depends(odoo_connection)) -> Dict[str, Any]:
    try:
        model_to_post = odoo.env[model]
        if context:
            record = model_to_post.with_context(**context).create(data)
        else:
            record = model_to_post.create(data)
        return record.id
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) from e

@router.put("/api/{model}/{rec_id}/")
async def put_model_record(model: str,
                           rec_id: int,
                           data: Dict[str, Any],
                           context: Optional[Dict[str, Any]] = None,
                           odoo: Any = Depends(odoo_connection)):
    try:
        model_to_put = odoo.env[model]
        if context:
            rec = model_to_put.with_context(**context).browse(rec_id).ensure_one()
        else:
            rec = model_to_put.browse(rec_id).ensure_one()
        rec.write(data)
        return True
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) from e

# @router.put("/api/{model}/")
# async def put_model_records(model: str,
#                             filter_condition: Dict[str, Any],
#                             data: Dict[str, Any],
#                             context: Dict[str, Any] = None,
#                             odoo: Any = Depends(odoo_connection)):
#     try:
#         model_to_put = odoo.env[model]
#         if context:
#             recs = model_to_put.with_context(**context).search(filter_condition)
#         else:
#             recs = model_to_put.search(filter_condition)
#         recs.write(data)
#         return True
#     except Exception as e:
#         raise HTTPException(status_code=400, detail=str(e)) from e

@router.get("/api/{model_name}/")
async def list_records(model_name: str,
                       page: int = Query(1, alias="page"),
                       page_size: int = Query(10, alias="page_size"),
                       odoo: Any = Depends(odoo_connection)) -> List[Dict[str, Any]]:
    try:
        # Gerar modelo Pydantic dinamicamente com base no modelo do Odoo
        dynamic_model: Type[BaseModel] = generate_pydantic_model_from_odoo(model_name, odoo=odoo)

        # Buscar registros do modelo especificado
        record_ids = odoo.env[model_name].search([], limit=page_size, offset=(page - 1) * page_size)
        records = odoo.env[model_name].browse(record_ids)

        # Preparar dados para serialização
        records_data = [{field: getattr(record, field, None) for field in dynamic_model.model_fields} for record in records]

        # Serializar dados usando o modelo Pydantic dinâmico
        serialized_data = [dynamic_model(**data).model_dump() for data in records_data]

        return serialized_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to list {model_name}: {str(e)}") from e



@router.delete("/api/{model}/{rec_id}/")
async def delete_model_record(model: str,
                              rec_id: int,
                              odoo: Any = Depends(odoo_connection)):
    try:
        model_to_del_rec = odoo.env[model]
        rec = model_to_del_rec.browse(rec_id).ensure_one()
        rec.unlink()
        return True
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) from e

@router.delete("/api/{model}/")
async def delete_model_records(model: str,
                               filter_condition: Dict[str, Any],
                               odoo: Any = Depends(odoo_connection)):
    try:
        model_to_del_rec = odoo.env[model]
        recs = model_to_del_rec.search(filter_condition)
        recs.unlink()
        return True
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) from e

@router.get("/api/{model}/{rec_id}/{field}")
async def get_binary_record(model: str,
                            rec_id: int,
                            field: str,
                            odoo: Any = Depends(odoo_connection)):
    try:
        rec = odoo.env[model].browse(rec_id).ensure_one()
        src = getattr(rec, field).decode("utf-8")
        return src
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) from e










# @router.post("/api/dependency/modules")
# async def get_dependent_modules(module: str, odoo: Any = Depends(odoo_connection)) -> Dict[str, Any]:
#     def sanitize_cmd_module_depends(module_name):
#         OdooVerMajor = get_odoo_version('major')
#         if OdooVerMajor >= 16:
#             return f"_______{module_name}"
#         return module_name
#
#     def get_odoo_version(odoo: Any) -> int:
#         try:
#             # Acesse a tabela 'ir.module.module' e busque o registro do módulo 'base'
#             base_module = odoo.env['ir.module.module'].sudo().search([('name', '=', 'base')], limit=1)
#             if base_module:
#                 # Obtenha a versão do Odoo do registro do módulo 'base'
#                 return int(base_module[0].installed_version)
#         except Exception as e:
#             # Se ocorrer algum erro ao obter a versão do Odoo, registre-o ou lide com ele adequadamente
#             print(f"Error getting Odoo version: {e}")
#         # Se não for possível obter a versão do Odoo, retorne um valor padrão
#         return 0
#
#
#     try:
#         module_name = sanitize_cmd_module_depends(module)
#         result = await call_model(
#             'res.config.settings',
#             'onchange_module',
#             [False, False, module_name],
#             context={},
#         )
#         depend_names = []
#         if is_empty(result):
#             raise HTTPException(status_code=404, detail=f"The module '{module}' isn't installed")
#         else:
#             depend_names = result.warning.message.split('\n')[1:]
#             return {"dependent_modules": depend_names}
#     except HTTPException as e:
#         raise e
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))
#
# @router.get("/api/dependency/modules/options")
# async def get_module_options(arg_name: str, odoo: Any = Depends(odoo_connection)) -> Dict[str, Any]:
#     try:
#         if arg_name == 'module':
#             options = await cached_search_read(
#                 'options_ir.module.module_active',
#                 'ir.module.module',
#                 [],
#                 ['name'],
#                 context={'active_test': True},
#             )
#             options = [item.name for item in options]
#         else:
#             options = []
#         return {"options": options}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))
#
