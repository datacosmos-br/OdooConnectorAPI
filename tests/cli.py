import os
import json
import requests
import click
import logging
from datetime import datetime
from tabulate import tabulate

# Definindo um novo nível de log para TRACE
TRACE = 5
logging.addLevelName(TRACE, "TRACE")

def trace(self, message, *args, **kwargs):
    if self.isEnabledFor(TRACE):
        self._log(TRACE, message, args, **kwargs)

# Configurando o logger
logging.basicConfig(level=logging.ERROR)  # Definindo o nível de log padrão como ERROR
logger = logging.getLogger(__name__)
logging.Logger.trace = trace
# Adicionando a entrada para nível de log TRACE
logging.TRACE = TRACE

CACHE_FILE = 'odoo_model_cache.json'

@click.command()
@click.option('--url', default='http://localhost:8000', help='URL base da API FastAPI do Odoo.')
@click.option('--log-level', default='error', help='Nível de log a ser utilizado (error, debug, trace)')
def list_odoo_fields(url, log_level):
    """Recupera e exibe todos os modelos do Odoo e seus campos em uma saída tabular."""

    # Configurando o nível de log com base no argumento fornecido
    numeric_level = getattr(logging, log_level.upper(), None)
    if not isinstance(numeric_level, int):
        raise ValueError(f'Invalid log level: {log_level}')
    logger.setLevel(numeric_level)

    def get_modules():
        logger.debug("Recuperando atualizações de módulos...")
        endpoint = f'{url}/object/ir.module.module/search_read'
        headers = {'Content-Type': 'application/json'}
        data = '{"args": [], "kwargs": {"fields": ["id", "name", "write_date"]}}'
        logger.trace(f"Submetendo requisição para {endpoint} com dados: {data}")
        try:
            response = requests.post(endpoint, headers=headers, data=data)
            response.raise_for_status()
            modules = response.json().get('result', [])
            logger.trace("Atualizações de módulos recuperadas com sucesso.")
            return {module['name']: module for module in modules}
        except Exception as e:
            logger.error(f"Erro ao recuperar atualizações de módulos: {e}")
            return {}

    def get_models():
        """Recupera todos os modelos disponíveis e suas informações."""
        logger.debug("Recuperando todos os modelos disponíveis...")
        endpoint = f'{url}/object/ir.model/search_read'
        headers = {'Content-Type': 'application/json'}
        data = '{"args": [], "kwargs": {"fields": ["id", "model", "modules", "write_date", "create_date", "field_id"]}}'
        logger.trace(f"Submetendo requisição para {endpoint} com dados: {data}")
        try:
            response = requests.post(endpoint, headers=headers, data=data)
            response.raise_for_status()
            models = response.json().get('result', [])
            logger.trace("Modelos recuperados com sucesso.")
            return models
        except Exception as e:
            logger.error(f"Erro ao recuperar modelos: {e}")
            return []

    def get_fields():
        """Recupera todos os campos disponíveis."""
        logger.debug("Recuperando todos os campos disponíveis...")
        endpoint = f'{url}/object/ir.model.fields/search_read'
        headers = {'Content-Type': 'application/json'}
        data = '{"args": [], "kwargs": {"fields": ["id", "name", "ttype", "model_id"]}}'
        logger.trace(f"Submetendo requisição para {endpoint} com dados: {data}")
        try:
            response = requests.post(endpoint, headers=headers, data=data)
            response.raise_for_status()
            fields = response.json().get('result', [])
            logger.trace("Campos recuperados com sucesso.")
            return fields
        except Exception as e:
            logger.error(f"Erro ao recuperar campos: {e}")
            return []

    # Verifica se há um cache local
    if os.path.exists(CACHE_FILE):
        logger.debug("Verificando existência de cache local.")
        with open(CACHE_FILE, 'r') as file:
            cached_data = json.load(file)
    else:
        logger.debug("Cache local não encontrado, inicializando com padrões.")
        cached_data = {'last_update': '1970-01-01 00:00:00', 'models': {}, 'fields': {}}

    # Recupera módulos, modelos e campos
    modules = get_modules()
    models = get_models()
    fields = get_fields()

    # Atualizando o cache com os dados recuperados
    max_update_time = datetime.min
    model_details = []

    for model in models:
        model_modules = model['modules'].split(', ')
        module_names = ', '.join([modules[mod]['name'] for mod in model_modules if mod in modules])
        module_write_dates = [datetime.strptime(modules[mod]['write_date'], '%Y-%m-%d %H:%M:%S') for mod in model_modules if mod in modules and modules[mod]['write_date']]
        max_model_update = max(module_write_dates) if module_write_dates else None

        if max_model_update:
            max_update_time = max(max_update_time, max_model_update)
            model['write_date'] = max_model_update.strftime('%Y-%m-%d %H:%M:%S')
        else:
            model['write_date'] = "No update date"

        for field_id in model['field_id']:
            field = next((fld for fld in fields if fld['id'] == field_id), None)
            if field:
                model_details.append({
                    'module': module_names or 'No module',
                    'model': model['model'],
                    'field': field['name'],
                    'type': field['ttype'],
                    'write_date': model.get('write_date', "No update date")
                })

    # Ajuste para o horário máximo de atualização
    if max_update_time == datetime.min:
        max_update_time = datetime.now()

    # Atualização do cache
    cached_data = {
        'last_update': max_update_time.strftime('%Y-%m-%d %H:%M:%S'),
        'modules': modules,
        'models': {model['id']: model for model in models},
        'fields': {field['id']: field for field in fields}
    }

    with open(CACHE_FILE, 'w') as file:
        json.dump(cached_data, file)
    logger.debug("Cache atualizado e salvo com sucesso.")

    # Preparando e exibindo a saída
    all_fields = [[detail['module'], detail['model'], detail['field'], detail['type']] for detail in model_details]
    click.echo(tabulate(all_fields, headers=['Módulo', 'Modelo', 'Campo', 'Tipo'], tablefmt="grid"))
    logger.debug("Listagem dos modelos e campos exibida com sucesso.")

if __name__ == '__main__':
    list_odoo_fields()