
def bin_to_hex(bin_str):
	if len(bin_str) % 4 != 0 or any(bit not in '01' for bit in bin_str):
		return "invalid binary"

	return hex(int(bin_str, 2))[2:].upper()
