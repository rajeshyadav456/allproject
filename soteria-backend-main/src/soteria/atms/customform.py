import json
import logging
from dataclasses import InitVar, asdict, astuple, dataclass
from dataclasses import field as dc_field
from enum import Enum
from typing import List

from rest_framework.exceptions import ValidationError
from rest_framework.fields import JSONField

from soteria.utils import to_cs_str, to_pretty_str, to_safe_str

DEFAULT_SAFE_STRING_LENGTH = 30
logger = logging.getLogger(__name__)


@dataclass
class BaseDataClass:
    def as_dict(self):
        return asdict(self)

    def as_tuple(self):
        return astuple(self)

    def as_json(self):
        return json.dumps(self.as_dict())


class CustomFormFieldType(Enum):
    TEXT = "text"
    NUMBER = "number"
    TOGGLE = "toggle"
    DROPDOWN = "dropdown"
    RADIO = "radio"
    CHECKBOX = "checkbox"
    DATE = "date"
    TIME = "time"
    DATETIME = "datetime"


@dataclass
class CustomFormFieldOption(BaseDataClass):
    key: str
    value: str


@dataclass
class CustomFormField(BaseDataClass):
    name: str  # required
    type: str  # required
    label: str  # required
    required: bool = dc_field(default=False)
    fields: List["CustomFormField"] = dc_field(default=None)
    conditions: list = dc_field(default_factory=list)
    options: List[CustomFormFieldOption] = dc_field(default_factory=list)
    data: dict = dc_field(default_factory=lambda: {})
    settings: dict = dc_field(default_factory=lambda: {})

    def __post_init__(self):
        if self.fields:
            self.fields = [CustomFormField(**f) for f in self.fields]


@dataclass
class CustomForm(BaseDataClass):
    fields: List[CustomFormField]

    def __post_init__(self):
        self.fields = [CustomFormField(**f) for f in self.fields]

    def __iter__(self):
        return iter(self.fields)

    def get_fields_of_type(self, ftype: CustomFormFieldType):
        return [f for f in self.fields if f.type == ftype]

    @classmethod
    def from_dict(cls, custom_form):
        if not isinstance(custom_form, dict):
            custom_form = {}
        fields = custom_form.get("fields", [])
        if not fields or not isinstance(fields, list):
            return cls(fields=[])
        return cls(fields=fields)


@dataclass
class CustomFormFieldValue(BaseDataClass):
    key: str = dc_field(default=None)
    label: str = dc_field(default=None)
    data: List["CustomFormFieldData"] = dc_field(default=None)

    def __post_init__(self):
        if self.data:
            self.data = [CustomFormFieldData(**d) for d in self.data]
            self.key = None
            self.label = None
        elif self.label is not None:
            self.data = None
        elif self.label and self.data:
            raise TypeError("'data' and 'label' fields are mutually exclusive")


@dataclass
class CustomFormFieldData(BaseDataClass):
    name: str
    type: str
    label: str
    value: List[CustomFormFieldValue] = dc_field(default_factory=list)

    # TODO: adding for backward compatibility with earlier custom data
    options: List[CustomFormFieldOption] = dc_field(default_factory=list)

    def __post_init__(self):
        self.value = [CustomFormFieldValue(**v) for v in self.value]

    def __iter__(self):
        return iter(self.value)


@dataclass
class CustomFormData(BaseDataClass):
    data: List[CustomFormFieldData]

    def __post_init__(self):
        self.data = [CustomFormFieldData(**d) for d in self.data]

    def __iter__(self):
        return iter(self.data)

    @classmethod
    def from_dict(cls, custom_form_data):
        if not isinstance(custom_form_data, dict):
            custom_form_data = {}
        data = custom_form_data.get("data", [])
        if not data or not isinstance(data, list):
            return cls(data=[])
        return cls(data=data)

    def as_format_context(self):
        return create_format_context_from_custom_form_data(self)


@dataclass
class ContextCustomFormDataField(BaseDataClass):
    name: str
    type: str
    label: str
    value: str = dc_field(init=False)
    values: InitVar[List[CustomFormFieldValue]] = None

    def __post_init__(self, values):
        value_labels = [v.label if isinstance(v, CustomFormFieldValue) else v for v in values]
        self.value = to_cs_str(value_labels)
        self._values = value_labels

    # Add support for `[key]` lookup
    def __getitem__(self, item):
        return getattr(self, item)

    @property
    def label_length(self):
        return len(str(self.label))

    @property
    def label_safe(self):
        return to_safe_str(self.label, safe_length=DEFAULT_SAFE_STRING_LENGTH, suffix="...")

    @property
    def label_upper(self):
        return str(self.label).upper()

    @property
    def label_lower(self):
        return str(self.label).lower()

    @property
    def value_safe(self):
        return to_safe_str(self.value, safe_length=DEFAULT_SAFE_STRING_LENGTH, suffix="...")

    @property
    def value_pretty(self):
        return to_pretty_str(self._values, last_sep="and")

    @property
    def value_upper(self):
        return str(self.value).upper()

    @property
    def value_lower(self):
        return str(self.value).lower()

    @property
    def value_length(self):
        return len(str(self.value))

    @property
    def total_length(self):
        return self.label_length + self.value_length


def create_format_context_from_custom_form_data(
    custom_form_data: CustomFormData,
) -> dict:
    ctx = dict()
    for field_data in custom_form_data.data:
        ctx[field_data.name] = ContextCustomFormDataField(
            **{
                "name": field_data.name,
                "type": field_data.type,
                "label": field_data.label,
                "values": field_data.value,
            }
        )
    return ctx


def validate_custom_form_schema(custom_form_schema: dict) -> CustomForm:
    try:
        return CustomForm.from_dict(custom_form_schema)
    except TypeError as e:
        logger.debug(f"Got error while validating custom form schema :" f" {str(e)}")
        raise ValidationError("Custom form schema is not valid")


def validate_custom_form_data(custom_form_data: dict) -> CustomFormData:
    try:
        return CustomFormData.from_dict(custom_form_data)
    except TypeError as e:
        logger.debug(f"Got error while validating custom form data : {str(e)}")
        raise ValidationError("Custom form data is not valid")


class CustomFormSchemaJSONField(JSONField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("validators", [])
        kwargs["validators"].append(validate_custom_form_schema)
        super().__init__(*args, **kwargs)


class CustomFormDataJSONField(JSONField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("validators", [])
        kwargs["validators"].append(validate_custom_form_data)
        super().__init__(*args, **kwargs)
