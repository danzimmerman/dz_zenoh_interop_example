# ...existing code...

from typing import List, Tuple, Sequence
from dataclasses import fields, dataclass


# CDR string type
@dataclass
class CDRString:
	value: str

# CDR sequence type (variable-length array)
@dataclass
class CDRSequence:
	value: List[Any]
	elem_type: Any

# CDR fixed-length array type
@dataclass
class CDRArray:
	value: Sequence[Any]
	elem_type: Any
	length: int

def cdr_serialize_string(obj: CDRString) -> bytes:
	# CDR string: uint32 length (including null), UTF-8 bytes, null terminator
	encoded = obj.value.encode('utf-8')
	length = len(encoded) + 1
	packed = struct.pack('>I', length) + encoded + b'\x00'
	return packed

def cdr_deserialize_string(data: bytes) -> Tuple[CDRString, int]:
	length = struct.unpack('>I', data[:4])[0]
	str_bytes = data[4:4+length-1]
	val = str_bytes.decode('utf-8')
	return CDRString(val), 4 + length

def cdr_serialize_sequence(obj: CDRSequence) -> bytes:
	# CDR sequence: uint32 length, then elements
	length = len(obj.value)
	packed = struct.pack('>I', length)
	for elem in obj.value:
		packed += cdr_serialize(obj.elem_type(elem))
	return packed

def cdr_deserialize_sequence(data: bytes, elem_type: Any) -> Tuple[CDRSequence, int]:
	length = struct.unpack('>I', data[:4])[0]
	offset = 4
	elems = []
	for _ in range(length):
		elem, used = cdr_deserialize(data[offset:], elem_type)
		elems.append(elem.value)
		offset += used
	return CDRSequence(elems, elem_type), offset

def cdr_serialize_array(obj: CDRArray) -> bytes:
	# CDR array: fixed number of elements
	packed = b''
	for elem in obj.value:
		packed += cdr_serialize(obj.elem_type(elem))
	return packed

def cdr_deserialize_array(data: bytes, elem_type: Any, length: int) -> Tuple[CDRArray, int]:
	offset = 0
	elems = []
	for _ in range(length):
		elem, used = cdr_deserialize(data[offset:], elem_type)
		elems.append(elem.value)
		offset += used
	return CDRArray(elems, elem_type, length), offset

# ...existing code...


class CDRStructBase:
	"""
	Base class for CDR-decodable structs. Inherit and define dataclass fields.
	"""
	def serialize(self) -> bytes:
		data = b''
		for f in fields(self):
			val = getattr(self, f.name)
			cdr_type = _python_to_cdr_type(f.type)
			if issubclass(f.type, CDRStructBase):
				data += val.serialize()
			elif cdr_type:
				data += cdr_serialize(cdr_type(val))
			elif f.type is str:
				data += cdr_serialize_string(CDRString(val))
			elif f.type is list:
				# Assume list of primitives, get element type from annotation
				elem_type = f.metadata.get('cdr_elem_type', int)
				data += cdr_serialize_sequence(CDRSequence(val, elem_type))
			elif f.type is tuple:
				# Fixed-length array, get element type and length
				elem_type = f.metadata.get('cdr_elem_type', int)
				length = f.metadata.get('cdr_length', len(val))
				data += cdr_serialize_array(CDRArray(val, elem_type, length))
			else:
				raise TypeError(f"Unsupported field type: {f.type}")
		return data

	@classmethod
	def deserialize(cls, data: bytes):
		offset = 0
		kwargs = {}
		for f in fields(cls):
			cdr_type = _python_to_cdr_type(f.type)
			if issubclass(f.type, CDRStructBase):
				val = f.type.deserialize(data[offset:])
				used = len(val.serialize())
			elif cdr_type:
				val, used = cdr_deserialize(data[offset:], cdr_type)
				val = val.value
			elif f.type is str:
				val, used = cdr_deserialize_string(data[offset:])
				val = val.value
			elif f.type is list:
				elem_type = f.metadata.get('cdr_elem_type', int)
				val, used = cdr_deserialize_sequence(data[offset:], elem_type)
				val = val.value
			elif f.type is tuple:
				elem_type = f.metadata.get('cdr_elem_type', int)
				length = f.metadata.get('cdr_length', None)
				if length is None:
					raise ValueError('cdr_length metadata required for tuple field')
				val, used = cdr_deserialize_array(data[offset:], elem_type, length)
				val = tuple(val.value)
			else:
				raise TypeError(f"Unsupported field type: {f.type}")
			kwargs[f.name] = val
			offset += used
		return cls(**kwargs)

def _python_to_cdr_type(pytype):
	"""Map Python type to CDR dataclass type."""
	mapping = {
		int: CDRInt32,  # Default to int32
		float: CDRFloat32,
		bool: CDRBoolean,
		str: CDRChar,
		CDRInt8: CDRInt8,
		CDRUInt8: CDRUInt8,
		CDRInt16: CDRInt16,
		CDRUInt16: CDRUInt16,
		CDRInt32: CDRInt32,
		CDRUInt32: CDRUInt32,
		CDRInt64: CDRInt64,
		CDRUInt64: CDRUInt64,
		CDRFloat32: CDRFloat32,
		CDRFloat64: CDRFloat64,
		CDRChar: CDRChar,
		CDRBoolean: CDRBoolean,
	}
	return mapping.get(pytype, None)

from dataclasses import dataclass
from typing import Any, Tuple
import struct

# CDR primitive types
@dataclass
class CDRInt8:
	value: int

@dataclass
class CDRUInt8:
	value: int

@dataclass
class CDRInt16:
	value: int

@dataclass
class CDRUInt16:
	value: int

@dataclass
class CDRInt32:
	value: int

@dataclass
class CDRUInt32:
	value: int

@dataclass
class CDRInt64:
	value: int

@dataclass
class CDRUInt64:
	value: int

@dataclass
class CDRFloat32:
	value: float

@dataclass
class CDRFloat64:
	value: float

@dataclass
class CDRChar:
	value: str  # single character

@dataclass
class CDRBoolean:
	value: bool

# Mapping of CDR types to struct format and alignment
CDR_FORMATS = {
	CDRInt8: ('b', 1),
	CDRUInt8: ('B', 1),
	CDRInt16: ('h', 2),
	CDRUInt16: ('H', 2),
	CDRInt32: ('i', 4),
	CDRUInt32: ('I', 4),
	CDRInt64: ('q', 8),
	CDRUInt64: ('Q', 8),
	CDRFloat32: ('f', 4),
	CDRFloat64: ('d', 8),
	CDRChar: ('c', 1),
	CDRBoolean: ('?', 1),
}

def cdr_serialize(obj: Any) -> bytes:
	"""
	Serialize a CDR primitive dataclass to CDR byte stream (big-endian, aligned).
	"""
	fmt, align = CDR_FORMATS[type(obj)]
	# CDR uses big-endian ('>')
	if type(obj) is CDRChar:
		val = obj.value.encode('utf-8')[:1]
	else:
		val = obj.value
	packed = struct.pack('>' + fmt, val)
	# Alignment: pad to align
	pad_len = (align - (len(packed) % align)) % align
	return packed + (b'\x00' * pad_len)

def cdr_deserialize(data: bytes, cdr_type: Any) -> Tuple[Any, int]:
	"""
	Deserialize CDR byte stream to CDR primitive dataclass.
	Returns (instance, bytes_consumed)
	"""
	fmt, align = CDR_FORMATS[cdr_type]
	size = struct.calcsize(fmt)
	val = struct.unpack('>' + fmt, data[:size])[0]
	if cdr_type is CDRChar:
		val = val.decode('utf-8')
	obj = cdr_type(val)
	# Alignment: skip padding
	pad_len = (align - (size % align)) % align
	return obj, size + pad_len

# Example decorated dataclass for a CDR struct
@dataclass
class ExampleCDRStruct(CDRStructBase):
	a: int  # int32
	b: float  # float32
	c: bool  # boolean
