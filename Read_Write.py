import struct
import snap7

client = snap7.client.Client()
client.connect("192.168.1.205", 0, 1, 102)
print(client.get_connected())
print("====================")

def set_int(bytearray_: bytearray, byte_index: int, _int: int):
    _int = int(_int)
    _bytes = struct.unpack('2B', struct.pack('>h', _int))
    bytearray_[byte_index:byte_index + 2] = _bytes
    return bytearray_

def get_int(bytearray_: bytearray, byte_index: int):
    data = bytearray_[byte_index:byte_index + 2]
    data[1] = data[1] & 0xff
    data[0] = data[0] & 0xff
    packed = struct.pack('2B', *data)
    value = struct.unpack('>h', packed)[0]
    return value

# Đọc cả thanh ghi
reading = client.db_read(2, 0, 56)

# Tạo vòng lặp để set giá trị cho từng giá trị cho mỗi thanh ghi
for i in range(0, 28):
    set_int(reading, 4, 30) # set giá trị 30 cho vị trí 4 trong thanh ghi
    set_int(reading, 8, 60) # set giá trị 60 cho vị trí 8 trong thanh ghi
    # set_int(reading, i * 2, i)
    print(i)
client.db_write(2, 0, reading) # Sau khi set xong hết toàn bộ giá tri cho thanh ghi. Một lần ghi và gửi toàn bộ nó lên cho PLC

# Để lấy từng giá trị trong thanh ghi ==> Sử dụng luôn get_int
x = get_int(reading, 6)
print(x)