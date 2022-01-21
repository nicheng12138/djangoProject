TYPE_UINT8_MAX = 255
TYPE_UINT16_MAX = 65535
TYPE_UINT32_MAX = 4294967295
TYPE_INT32_MIN = -2147483648
TYPE_INT32_MAX = 2147483647
TYPE_UINT64_MAX = 18446744073709551615

UInt8Schema = {"type": "integer", "minimum": 0, "maximum": TYPE_UINT8_MAX}
UInt16Schema = {"type": "integer", "minimum": 0, "maximum": TYPE_UINT16_MAX}
UInt32Schema = {"type": "integer", "minimum": 0, "maximum": TYPE_UINT32_MAX}
Int32Schema = {"type": "integer", "minimum": TYPE_INT32_MIN, "maximum": TYPE_INT32_MAX}
UInt64Schema = {"type": "integer", "minimum": 0, "maximum": TYPE_UINT64_MAX}
UFloatSchema = {"type": "number", "minimum": 0}
DoubleSchema = {"type": "number"}
StringSchema = {"type": "string"}
BooleanSchema = {"type": "boolean"}


LoginSchema = {
	"type": "object",
	"properties": {
		"username": StringSchema,
		"password": StringSchema,
	},
	"required": ["username", "password"],
}

UpdateUserSchema = {
	"type": "object",
	"properties": {
		"username": StringSchema,
		"nickname": StringSchema,
		"picture": StringSchema,
	},
	"required": ["username", "password", "picture"],
}
