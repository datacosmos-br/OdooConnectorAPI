"""Parser module for the OdooConnectorAPI FastAPI application."""
import re
from typing import Any, Dict
from pypeg2 import List, contiguous, csl, name, optional, parse # type: ignore
from app.exceptions import QueryFormatError

class BaseArgument(List):
    """Base class for arguments, providing a method to get the argument value."""
    @property
    def value(self) -> str:
        """Returns the first element of the list as its value."""
        return self[0]

class ArgumentWithoutQuotes(BaseArgument):
    """Represents an argument specified without quotes."""
    grammar = name(), ':', re.compile(r'[^,:"\'\)]+')

class ArgumentWithSingleQuotes(BaseArgument):
    """Represents an argument enclosed in single quotes."""
    grammar = name(), ':', "'", re.compile(r'[^\']+'), "'"

class ArgumentWithDoubleQuotes(BaseArgument):
    """Represents an argument enclosed in double quotes."""
    grammar = name(), ':', '"', re.compile(r'[^"]+'), '"'

class Arguments(List):
    """Represents a list of arguments."""
    grammar = optional(csl([ArgumentWithoutQuotes, ArgumentWithSingleQuotes, ArgumentWithDoubleQuotes]))

class ArgumentsBlock(List):
    """Represents a block of arguments."""
    grammar = optional('(', Arguments, ')')

    @property
    def arguments(self):
        """Returns the arguments within the block, or an empty list if none."""
        if self[0] is None:
            return []  # No arguments
        return self[0]

class IncludedField(List):
    """Represents a field to be included in the serialization."""
    grammar = name()

class ExcludedField(List):
    """Represents a field to be excluded from the serialization."""
    grammar = contiguous('-', name())

class AllFields(str):
    """Represents a wildcard for including all fields."""
    grammar = '*'


class BlockBody(List):
    """Represents the body of a block, containing fields and arguments."""
    grammar = optional(csl(['ParentField', IncludedField, ExcludedField, AllFields]))


class Block(List):
    """Represents a complete block, including arguments and body."""
    grammar = ArgumentsBlock, '{', BlockBody, '}'

    @property
    def arguments(self) -> Any:
        """Returns the arguments of the block."""
        return self[0].arguments

    @property
    def body(self) -> Any:
        """Returns the body of the block."""
        return self[1]


class ParentField(List):
    """
    Represents a parent field with a nested block.
    This class redefines itself to include a nested Block instance.
    """
    grammar = IncludedField, Block

    @property
    def name(self):
        """Returns the name of the parent field."""
        return self[0].name

    @property
    def block(self):
        """Returns the nested block of the parent field."""
        return self[1]

class Parser:
    """Parser class for parsing and transforming a query into a structured format."""
    def __init__(self, query) -> None:
        self._query = query

    def get_parsed(self) -> Any:
        """Parses the query and transforms it into a structured representation."""
        parse_tree = parse(self._query, Block)
        return self._transform_block(parse_tree)

    def _transform_block(self, block: Block) -> Dict[str, Any]:
        """Transforms a Block into a structured dictionary."""
        # Initial structure for fields
        fields = {"include": [], "exclude": [], "arguments": {}}

        # Process arguments
        for argument in block.arguments:
            argument_dict = {str(argument.name): argument.value}
            fields['arguments'].update(argument_dict)

        # Process body fields
        for field in block.body:
            field_transformed = self._transform_field(field)
            if isinstance(field_transformed, dict):
                fields["include"].append(field_transformed)
            elif isinstance(field_transformed, IncludedField):
                fields["include"].append(str(field_transformed.name))
            elif isinstance(field_transformed, ExcludedField):
                fields["exclude"].append(str(field_transformed.name))
            elif isinstance(field_transformed, AllFields):
                fields["include"].append("*")

        # Handle include/exclude logic
        self._handle_include_exclude_logic(fields)
        return fields

    def _transform_field(self, field):
        """Transforms a field into its structured representation."""
        if isinstance(field, ParentField):
            return self._transform_parent_field(field)
        return field

    def _transform_parent_field(self, parent_field) -> Dict[str, Any]:
        """Transforms a ParentField into a dictionary with its name and block transformed."""
        parent_field_name = str(parent_field.name)
        parent_field_value = self._transform_block(parent_field.block)
        return {parent_field_name: parent_field_value}

    def _handle_include_exclude_logic(self, fields: Dict[str, Any]):
        """Handles the logic for including and excluding fields."""
        if fields["exclude"]:
            add_include_all_operator = "*" not in fields["include"]
            for field in fields["include"]:
                if isinstance(field, str) and field != "*":
                    raise QueryFormatError("Cannot include and exclude fields on the same field level")
            if add_include_all_operator:
                fields["include"].append("*")