ESCAPE_CHAR = b'\x42'
END_CHAR    = b'\x66'

def _format(byts):
	transform_bytes = bytes()
	for byte in byts:
		if byte is ESCAPE_CHAR: transform_bytes += ESCAPE_CHAR
		transform_bytes += bytes([byte])
	return transform_bytes + END_CHAR