"""
Data Validation Utilities
========================

Comprehensive validation functions to ensure data integrity and accuracy
throughout the analysis framework.
"""

import re
from datetime import datetime, date
from typing import Any, Dict, List, Optional, Union, Callable
from pathlib import Path
import hashlib
import json


class ValidationError(Exception):
    """Custom validation error with detailed information"""
    
    def __init__(self, message: str, field: Optional[str] = None, value: Any = None):
        self.message = message
        self.field = field
        self.value = value
        super().__init__(self.format_message())
    
    def format_message(self) -> str:
        """Format error message with field and value information"""
        if self.field:
            return f"{self.field}: {self.message}"
        return self.message
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert error to dictionary for API responses"""
        return {
            "error": "validation_error",
            "message": self.message,
            "field": self.field,
            "value": str(self.value) if self.value is not None else None
        }


class Validator:
    """Base validator class with common validation methods"""
    
    @staticmethod
    def required(value: Any, field_name: str) -> Any:
        """Validate that a value is not None or empty"""
        if value is None:
            raise ValidationError(f"{field_name} is required")
        
        if isinstance(value, str) and not value.strip():
            raise ValidationError(f"{field_name} cannot be empty", field_name, value)
        
        if isinstance(value, (list, dict)) and len(value) == 0:
            raise ValidationError(f"{field_name} cannot be empty", field_name, value)
        
        return value
    
    @staticmethod
    def string(value: Any, field_name: str, 
               min_length: Optional[int] = None,
               max_length: Optional[int] = None,
               pattern: Optional[str] = None) -> str:
        """Validate string value with optional constraints"""
        if not isinstance(value, str):
            raise ValidationError(f"{field_name} must be a string", field_name, value)
        
        if min_length is not None and len(value) < min_length:
            raise ValidationError(
                f"{field_name} must be at least {min_length} characters",
                field_name, value
            )
        
        if max_length is not None and len(value) > max_length:
            raise ValidationError(
                f"{field_name} must be at most {max_length} characters",
                field_name, value
            )
        
        if pattern is not None:
            if not re.match(pattern, value):
                raise ValidationError(
                    f"{field_name} does not match required pattern",
                    field_name, value
                )
        
        return value
    
    @staticmethod
    def integer(value: Any, field_name: str,
                min_value: Optional[int] = None,
                max_value: Optional[int] = None) -> int:
        """Validate integer value with optional bounds"""
        try:
            int_value = int(value)
        except (ValueError, TypeError):
            raise ValidationError(f"{field_name} must be an integer", field_name, value)
        
        if min_value is not None and int_value < min_value:
            raise ValidationError(
                f"{field_name} must be at least {min_value}",
                field_name, value
            )
        
        if max_value is not None and int_value > max_value:
            raise ValidationError(
                f"{field_name} must be at most {max_value}",
                field_name, value
            )
        
        return int_value
    
    @staticmethod
    def float_number(value: Any, field_name: str,
                     min_value: Optional[float] = None,
                     max_value: Optional[float] = None) -> float:
        """Validate float value with optional bounds"""
        try:
            float_value = float(value)
        except (ValueError, TypeError):
            raise ValidationError(f"{field_name} must be a number", field_name, value)
        
        if min_value is not None and float_value < min_value:
            raise ValidationError(
                f"{field_name} must be at least {min_value}",
                field_name, value
            )
        
        if max_value is not None and float_value > max_value:
            raise ValidationError(
                f"{field_name} must be at most {max_value}",
                field_name, value
            )
        
        return float_value
    
    @staticmethod
    def boolean(value: Any, field_name: str) -> bool:
        """Validate boolean value"""
        if isinstance(value, bool):
            return value
        
        if isinstance(value, str):
            if value.lower() in ('true', '1', 'yes', 'on'):
                return True
            elif value.lower() in ('false', '0', 'no', 'off'):
                return False
        
        raise ValidationError(f"{field_name} must be a boolean", field_name, value)
    
    @staticmethod
    def datetime_value(value: Any, field_name: str,
                       min_date: Optional[datetime] = None,
                       max_date: Optional[datetime] = None) -> datetime:
        """Validate datetime value"""
        if isinstance(value, datetime):
            dt_value = value
        elif isinstance(value, date):
            dt_value = datetime.combine(value, datetime.min.time())
        elif isinstance(value, str):
            try:
                # Try ISO format first
                dt_value = datetime.fromisoformat(value.replace('Z', '+00:00'))
            except ValueError:
                # Try common formats
                for fmt in [
                    '%Y-%m-%d %H:%M:%S',
                    '%Y-%m-%d',
                    '%d/%m/%Y',
                    '%m/%d/%Y'
                ]:
                    try:
                        dt_value = datetime.strptime(value, fmt)
                        break
                    except ValueError:
                        continue
                else:
                    raise ValidationError(
                        f"{field_name} is not a valid datetime",
                        field_name, value
                    )
        else:
            raise ValidationError(
                f"{field_name} must be a datetime",
                field_name, value
            )
        
        if min_date and dt_value < min_date:
            raise ValidationError(
                f"{field_name} cannot be before {min_date.isoformat()}",
                field_name, value
            )
        
        if max_date and dt_value > max_date:
            raise ValidationError(
                f"{field_name} cannot be after {max_date.isoformat()}",
                field_name, value
            )
        
        return dt_value
    
    @staticmethod
    def enum(value: Any, field_name: str, allowed_values: List[Any]) -> Any:
        """Validate that value is in allowed list"""
        if value not in allowed_values:
            raise ValidationError(
                f"{field_name} must be one of: {', '.join(map(str, allowed_values))}",
                field_name, value
            )
        return value
    
    @staticmethod
    def email(value: Any, field_name: str) -> str:
        """Validate email address"""
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        
        if not isinstance(value, str):
            raise ValidationError(f"{field_name} must be a string", field_name, value)
        
        if not re.match(email_pattern, value):
            raise ValidationError(
                f"{field_name} is not a valid email address",
                field_name, value
            )
        
        return value.lower()
    
    @staticmethod
    def uuid(value: Any, field_name: str) -> str:
        """Validate UUID format"""
        uuid_pattern = r'^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$'
        
        if not isinstance(value, str):
            raise ValidationError(f"{field_name} must be a string", field_name, value)
        
        if not re.match(uuid_pattern, value):
            raise ValidationError(
                f"{field_name} is not a valid UUID",
                field_name, value
            )
        
        return value.lower()
    
    @staticmethod
    def json_data(value: Any, field_name: str, schema: Optional[Dict] = None) -> Dict:
        """Validate JSON data with optional schema"""
        if isinstance(value, str):
            try:
                data = json.loads(value)
            except json.JSONDecodeError as e:
                raise ValidationError(
                    f"{field_name} is not valid JSON: {e}",
                    field_name, value
                )
        elif isinstance(value, dict):
            data = value
        else:
            raise ValidationError(
                f"{field_name} must be a JSON object",
                field_name, value
            )
        
        # TODO: Add JSON schema validation if schema provided
        
        return data
    
    @staticmethod
    def file_path(value: Any, field_name: str,
                  must_exist: bool = False,
                  allowed_extensions: Optional[List[str]] = None) -> Path:
        """Validate file path"""
        if not isinstance(value, (str, Path)):
            raise ValidationError(
                f"{field_name} must be a file path",
                field_name, value
            )
        
        path = Path(value)
        
        if must_exist and not path.exists():
            raise ValidationError(
                f"{field_name} file does not exist",
                field_name, value
            )
        
        if allowed_extensions:
            if path.suffix.lower().lstrip('.') not in allowed_extensions:
                raise ValidationError(
                    f"{field_name} must have one of these extensions: {', '.join(allowed_extensions)}",
                    field_name, value
                )
        
        return path


class CaseValidator(Validator):
    """Validator specific to case data"""
    
    @staticmethod
    def case_id(value: Any) -> str:
        """Validate case ID format"""
        pattern = r'^case_[0-9]{8}_[0-9]{6}_[a-f0-9]{8}$'
        return Validator.string(value, "case_id", pattern=pattern)
    
    @staticmethod
    def agent_id(value: Any) -> str:
        """Validate agent ID format"""
        pattern = r'^agent_[a-f0-9]{12}$'
        return Validator.string(value, "agent_id", pattern=pattern)
    
    @staticmethod
    def event_id(value: Any) -> str:
        """Validate event ID format"""
        pattern = r'^(event|evt)_[a-f0-9]{8,12}$'
        return Validator.string(value, "event_id", pattern=pattern)
    
    @staticmethod
    def agent_type(value: Any) -> str:
        """Validate agent type"""
        allowed = ['individual', 'organization', 'system', 'unknown']
        return Validator.enum(value, "agent_type", allowed)
    
    @staticmethod
    def confidence_level(value: Any) -> str:
        """Validate confidence level"""
        allowed = ['high', 'medium', 'low', 'insufficient']
        return Validator.enum(value, "confidence_level", allowed)
    
    @staticmethod
    def priority(value: Any) -> str:
        """Validate priority level"""
        allowed = ['low', 'medium', 'high']
        return Validator.enum(value, "priority", allowed)
    
    @staticmethod
    def status(value: Any) -> str:
        """Validate case status"""
        allowed = ['active', 'archived', 'pending']
        return Validator.enum(value, "status", allowed)


class EvidenceValidator(Validator):
    """Validator for evidence data"""
    
    @staticmethod
    def evidence_hash(value: Any, algorithm: str = 'sha256') -> str:
        """Validate evidence hash format"""
        hash_lengths = {
            'md5': 32,
            'sha1': 40,
            'sha256': 64,
            'sha512': 128
        }
        
        if algorithm not in hash_lengths:
            raise ValidationError(f"Unknown hash algorithm: {algorithm}")
        
        expected_length = hash_lengths[algorithm]
        pattern = f'^[a-f0-9]{{{expected_length}}}$'
        
        return Validator.string(value, "evidence_hash", pattern=pattern)
    
    @staticmethod
    def file_hash(file_path: Path, algorithm: str = 'sha256') -> str:
        """Calculate and return file hash"""
        if not file_path.exists():
            raise ValidationError(f"File does not exist: {file_path}")
        
        hash_func = getattr(hashlib, algorithm)()
        
        with open(file_path, 'rb') as f:
            for chunk in iter(lambda: f.read(4096), b''):
                hash_func.update(chunk)
        
        return hash_func.hexdigest()


class TimelineValidator(Validator):
    """Validator for timeline data"""
    
    @staticmethod
    def validate_timeline_consistency(events: List[Dict[str, Any]]) -> bool:
        """Validate that timeline events are consistent"""
        if not events:
            return True
        
        # Sort events by timestamp
        sorted_events = sorted(
            events,
            key=lambda e: datetime.fromisoformat(e['timestamp'])
        )
        
        # Check for logical consistency
        for i in range(1, len(sorted_events)):
            prev_event = sorted_events[i-1]
            curr_event = sorted_events[i]
            
            # Example: Check that effects don't precede causes
            if curr_event.get('caused_by') == prev_event['id']:
                prev_time = datetime.fromisoformat(prev_event['timestamp'])
                curr_time = datetime.fromisoformat(curr_event['timestamp'])
                
                if curr_time < prev_time:
                    raise ValidationError(
                        f"Event {curr_event['id']} cannot be caused by future event {prev_event['id']}"
                    )
        
        return True


class NetworkValidator(Validator):
    """Validator for network/graph data"""
    
    @staticmethod
    def validate_graph_consistency(nodes: List[str], edges: List[Tuple[str, str]]) -> bool:
        """Validate that all edges reference existing nodes"""
        node_set = set(nodes)
        
        for source, target in edges:
            if source not in node_set:
                raise ValidationError(f"Edge source '{source}' not in nodes")
            if target not in node_set:
                raise ValidationError(f"Edge target '{target}' not in nodes")
        
        return True
    
    @staticmethod
    def validate_no_self_loops(edges: List[Tuple[str, str]]) -> bool:
        """Validate that graph has no self-loops"""
        for source, target in edges:
            if source == target:
                raise ValidationError(f"Self-loop detected: {source} -> {target}")
        
        return True


def validate_request_data(data: Dict[str, Any], 
                         schema: Dict[str, Dict[str, Any]]) -> Dict[str, Any]:
    """
    Validate request data against a schema
    
    Args:
        data: Data to validate
        schema: Validation schema
        
    Returns:
        Validated and cleaned data
        
    Raises:
        ValidationError: If validation fails
    """
    validated = {}
    errors = []
    
    for field_name, field_schema in schema.items():
        field_type = field_schema.get('type', 'string')
        required = field_schema.get('required', False)
        default = field_schema.get('default')
        
        value = data.get(field_name, default)
        
        if required and value is None:
            errors.append(ValidationError(f"{field_name} is required"))
            continue
        
        if value is None:
            continue
        
        try:
            # Apply type-specific validation
            if field_type == 'string':
                validated[field_name] = Validator.string(
                    value, field_name,
                    min_length=field_schema.get('min_length'),
                    max_length=field_schema.get('max_length'),
                    pattern=field_schema.get('pattern')
                )
            elif field_type == 'integer':
                validated[field_name] = Validator.integer(
                    value, field_name,
                    min_value=field_schema.get('min_value'),
                    max_value=field_schema.get('max_value')
                )
            elif field_type == 'float':
                validated[field_name] = Validator.float_number(
                    value, field_name,
                    min_value=field_schema.get('min_value'),
                    max_value=field_schema.get('max_value')
                )
            elif field_type == 'boolean':
                validated[field_name] = Validator.boolean(value, field_name)
            elif field_type == 'datetime':
                validated[field_name] = Validator.datetime_value(
                    value, field_name,
                    min_date=field_schema.get('min_date'),
                    max_date=field_schema.get('max_date')
                )
            elif field_type == 'enum':
                validated[field_name] = Validator.enum(
                    value, field_name,
                    allowed_values=field_schema.get('values', [])
                )
            elif field_type == 'email':
                validated[field_name] = Validator.email(value, field_name)
            elif field_type == 'json':
                validated[field_name] = Validator.json_data(
                    value, field_name,
                    schema=field_schema.get('schema')
                )
            else:
                validated[field_name] = value
                
        except ValidationError as e:
            errors.append(e)
    
    if errors:
        # Combine all errors into one
        error_messages = [e.format_message() for e in errors]
        raise ValidationError("; ".join(error_messages))
    
    return validated