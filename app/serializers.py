"""Serializer module for the OdooConnectorAPI FastAPI application."""
from typing import Dict, Union, List, Any, TypeVar, Set, Tuple
from app.parser import Parser
from app.exceptions import QueryFormatError

# Define a generic type variable for records
RecordType = TypeVar('RecordType')

class Serializer(object):
    def __init__(self, record: RecordType, query: str = "{*}", many: bool = False):
        """
        Initializes the Serializer with a record, query, and a flag indicating if multiple records are handled.

        :param record: The record or records to be serialized.
        :param query: The RESTQL query string to dictate the serialization process.
        :param many: A boolean flag to indicate if the serializer is handling multiple records.
        """
        self.many = many
        self._record = record
        self._raw_query = query
        super().__init__()

    def get_parsed_restql_query(self) -> Dict[str, Union[List[Any], Dict[Any, Any]]]:
        """
        Parses the RESTQL query and returns it as a structured dictionary.

        :return: A dictionary representing the structured query.
        """
        parser = Parser(self._raw_query)
        try:
            parsed_restql_query = parser.get_parsed()
            return parsed_restql_query
        except SyntaxError as e:
            msg = f"QuerySyntaxError: {e.msg} on {e.text}"
            raise SyntaxError(msg) from None
        except QueryFormatError as e:
            msg = "QueryFormatError: " + str(e)
            raise QueryFormatError(msg) from None

    @property
    def data(self) -> Union[Dict[str, Any], List[Dict[str, Any]]]:
        """
        Serializes the record(s) based on the parsed RESTQL query.

        :return: A dictionary or list of dictionaries representing the serialized data.
        """
        parsed_restql_query = self.get_parsed_restql_query()
        if self.many:
            return [self.serialize(rec, parsed_restql_query) for rec in self._record]
        else:
            return self.serialize(self._record, parsed_restql_query)

    @property
    def data(self) -> Union[Dict[str, Any], List[Dict[str, Any]]]:
        """
        Serializes the record(s) based on the parsed RESTQL query.

        :return: A dictionary or list of dictionaries representing the serialized data.
        """
        parsed_restql_query = self.get_parsed_restql_query()
        if not parsed_restql_query or parsed_restql_query == {"include": ["*"]}:
            parsed_restql_query = {"include": self._record.fields_get().keys()}
        if self.many:
            return [self.serialize(rec, parsed_restql_query) for rec in self._record]
        else:
            return self.serialize(self._record, parsed_restql_query)


    @classmethod
    def build_flat_field(cls, rec: Any, field_name: str) -> Dict[str, Any]:
        """
        Builds a flat field for serialization.

        :param rec: The record containing the field.
        :param field_name: The name of the field to be serialized.
        :return: A dictionary representing the serialized field.
        """
        all_fields = rec.fields_get_keys()
        if field_name not in all_fields:
            msg = f"'{field_name}' field is not found"
            raise LookupError(msg)
        field_type = rec.fields_get(field_name).get(field_name).get('type')
        if field_type in ['one2many', 'many2many']:
            return {field_name: [record.id for record in rec[field_name]]}
        elif field_type in ['many2one']:
            return {field_name: rec[field_name].id}
        elif field_type == 'datetime' and rec[field_name]:
            return {field_name: rec[field_name].strftime("%Y-%m-%d-%H-%M")}
        elif field_type == 'date' and rec[field_name]:
            return {field_name: rec[field_name].strftime("%Y-%m-%d")}
        elif field_type == 'time' and rec[field_name]:
            return {field_name: rec[field_name].strftime("%H-%M-%S")}
        elif field_type == "binary" and isinstance(rec[field_name], bytes) and rec[field_name]:
            return {field_name: rec[field_name].decode("utf-8")}
        else:
            return {field_name: rec[field_name]}

    @classmethod
    def build_nested_field(cls,
                           rec: Any,
                           field_name: Any,
                           nested_parsed_query: Any):
        all_fields = rec.fields_get_keys()
        if field_name not in all_fields:
            msg = f"'{field_name}' field is not found"
            raise LookupError(msg)
        field_type = rec.fields_get(field_name).get(field_name).get('type')
        if field_type in ['one2many', 'many2many']:
            return {
                field_name: [
                    cls.serialize(record, nested_parsed_query)
                    for record
                    in rec[field_name]
                ]
            }
        if field_type in ['many2one']:
            return {
                field_name: cls.serialize(rec[field_name], nested_parsed_query)
            }
        else:
            # Not a nested field
            msg = f"'{field_name}' is not a nested field"
            raise ValueError(msg)

    @classmethod
    def serialize(cls, rec: Any, parsed_query: Any) -> Dict[str, Any]:
        data = {}
        all_fields = rec.fields_get().keys()
        include_fields, exclude_fields = cls._parse_query_fields(parsed_query, all_fields)

        # Process included fields
        for field in include_fields:
            if isinstance(field, dict):  # Nested fields
                for nested_field, nested_parsed_query in field.items():
                    data.update(cls.build_nested_field(rec, nested_field, nested_parsed_query))
            else:  # Flat fields
                data.update(cls.build_flat_field(rec, field))

        # Process excluded fields
        for field in exclude_fields:
            data.pop(field, None)  # Safely remove excluded fields

        return data


    @classmethod
    def _parse_query_fields(cls, parsed_query: Any, all_fields: List[str]) -> Tuple[Set[str], Set[str]]:
        """Helper method to determine included and excluded fields based on parsed query and available fields."""
        exclude_fields = set(parsed_query.get("exclude", []))

        if "*" in parsed_query.get("include", []):
            include_fields = set(all_fields) - exclude_fields
        else:
            include_fields = set(parsed_query.get("include", [])) - exclude_fields

        return include_fields, exclude_fields
