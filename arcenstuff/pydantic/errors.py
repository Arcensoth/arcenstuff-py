from pydantic.errors import PydanticTypeError

__all__ = (
    "MissingType",
    "UnknownType",
    "InvalidModule",
    "InvalidModuleFunction",
    "UnexpectedInstance",
)


class MissingType(PydanticTypeError):
    msg_template = "Missing or malformed type field `{type_field}`"


class UnknownType(PydanticTypeError):
    msg_template = "Encountered unknown type `{type_name}`"


class InvalidModule(PydanticTypeError):
    msg_template = (
        "Module `{module_name}` could not be imported,"
        " or does not contain a `{function_name}` function"
    )


class InvalidModuleFunction(PydanticTypeError):
    msg_template = (
        "Function `{function_name}` in module `{module_name}` caused an error"
    )


class UnexpectedInstance(PydanticTypeError):
    msg_template = (
        "Expected an instance of `{expected_type.__name__}`"
        " but got `{actual_type.__name__}` from function `{function_name}`"
        " in module `{module_name}`"
    )
