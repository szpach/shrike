import sys


def get_padding(current_length, desired_length):
    if current_length >= desired_length:
        return ''
    else:
        return b'\x00' * (desired_length - current_length)


def prepare_payload(js_bytes: bytes):
    comment_marker = b'\xFF\xFE'
    js_payload_start = b'\x2A\x2F\x3D\x31\x3B'
    js_payload_end = b'\x2F\x2A'
    js_payload = js_payload_start + js_bytes + js_payload_end
    payload_length = (len(js_payload) + 2).to_bytes(2, 'big')

    return comment_marker + payload_length + js_payload


def read_bytes(file_name):
    with open(file_name, 'rb') as file:
        binary_data: bytes = file.read()

    return binary_data


def write_bytes(file_name, binary_data: bytes):
    with open(file_name, 'wb') as file:
        file.write(binary_data)


def replace_bytes(binary_data: bytes, old_bytes, new_bytes):
    return binary_data.replace(old_bytes, new_bytes)


def add_bytes(binary_data: bytes, offset, bytes_to_add):
    return binary_data[:offset] + bytes_to_add + binary_data[offset:]


def find_bytes(binary_data: bytes, bytes_seq):
    try:
        return binary_data.index(bytes_seq)
    except ValueError:
        return -1


def get_bytes(binary_data: bytes, offset_from, offset_to):
    return binary_data[offset_from:offset_to]


# Used for debugging
def print_bytes(binary_data: bytes, offset_from, offset_to):
    count = offset_from
    for byte in binary_data[offset_from:offset_to]:
        if (count - offset_from) % 16 == 0:
            print('\n' + format(count, '08X'), end='  ')
        print(format(byte, '02X'), end=' ')
        count += 1


def make_polyglot(jpeg_file, js_file, output_file):
    jpeg_bytes = read_bytes(jpeg_file)
    js_bytes = read_bytes(js_file)

    # Modifying 0xFFE0 marker length to /*
    ffe0_location = find_bytes(jpeg_bytes, b'\xFF\xE0')
    ffe0_size_var = get_bytes(jpeg_bytes, ffe0_location + 2, ffe0_location + 4)
    jpeg_bytes = replace_bytes(jpeg_bytes, ffe0_size_var, b'\x2F\x2A')
    padding = get_padding(int.from_bytes(ffe0_size_var, byteorder='big'), int.from_bytes(b'\x2F\x2A', byteorder='big'))
    jpeg_bytes = add_bytes(jpeg_bytes, ffe0_location + 2 + int.from_bytes(ffe0_size_var, byteorder='big'), padding)

    # Inserting 0xFFFE with js payload
    jpeg_comment = prepare_payload(js_bytes)
    ffc4_location = find_bytes(jpeg_bytes, b'\xFF\xC4')
    jpeg_bytes = add_bytes(jpeg_bytes, ffc4_location, jpeg_comment)

    # Adding */// before 0xFFD9
    jpeg_bytes = replace_bytes(jpeg_bytes, get_bytes(jpeg_bytes, len(jpeg_bytes) - 6, len(jpeg_bytes) - 2), b'\x2A\x2F\x2F\x2F')

    write_bytes(output_file, jpeg_bytes)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print('Usage:\npython3 shrike.py [jpeg file path].jpg [js file path].js')
        sys.exit()
    else:
        output = 'polyglot_' + sys.argv[1]
        make_polyglot(sys.argv[1], sys.argv[2], output)
        print('Saved to ' + output)
