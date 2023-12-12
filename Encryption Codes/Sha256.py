from base64 import encode
import struct

def right_rotate(n, b):
    return (n >> b) | (n << (32 - b)) & 0xFFFFFFFF

def sha256(message):
    # Constants for SHA-256
    h0 = 0x6a09e667
    h1 = 0xbb67ae85
    h2 = 0x3c6ef372
    h3 = 0xa54ff53a
    h4 = 0x510e527f
    h5 = 0x9b05688c
    h6 = 0x1f83d9ab
    h7 = 0x5be0cd19

    k = [
        0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5,
        0x3956c25b, 0x59f111f1, 0x923f82a4, 0xab1c5ed5,
        0xd807aa98, 0x12835b01, 0x243185be, 0x550c7dc3,
        0x72be5d74, 0x80deb1fe, 0x9bdc06a7, 0xc19bf174,
        0xe49b69c1, 0xefbe4786, 0x0fc19dc6, 0x240ca1cc,
        0x2de92c6f, 0x4a7484aa, 0x5cb0a9dc, 0x76f988da,
        0x983e5152, 0xa831c66d, 0xb00327c8, 0xbf597fc7,
        0xc6e00bf3, 0xd5a79147, 0x06ca6351, 0x14292967,
        0x27b70a85, 0x2e1b2138, 0x4d2c6dfc, 0x53380d13,
        0x650a7354, 0x766a0abb, 0x81c2c92e, 0x92722c85,
        0xa2bfe8a1, 0xa81a664b, 0xc24b8b70, 0xc76c51a3,
        0xd192e819, 0xd6990624, 0xf40e3585, 0x106aa070,
        0x19a4c116, 0x1e376c08, 0x2748774c, 0x34b0bcb5,
        0x391c0cb3, 0x4ed8aa4a, 0x5b9cca4f, 0x682e6ff3,
        0x748f82ee, 0x78a5636f, 0x84c87814, 0x8cc70208,
        0x90befffa, 0xa4506ceb, 0xbef9a3f7, 0xc67178f2
    ]

    message = bytearray(message)
    ml = len(message) * 8

    # Pre-processing: append a single '1' bit, followed by 0 bits, and the message length in bits
    message.append(0x80)
    while len(message) % 64 != 56:
        message.append(0x00)
    message += struct.pack('>Q', ml)

    chunks = [message[i:i + 64] for i in range(0, len(message), 64)]

    for chunk in chunks:
        w = [0] * 64
        for i in range(16):
            w[i] = struct.unpack('>I', chunk[i * 4:i * 4 + 4])[0]

        for i in range(16, 64):
            s0 = right_rotate(w[i - 15], 7) ^ right_rotate(w[i - 15], 18) ^ (w[i - 15] >> 3)
            s1 = right_rotate(w[i - 2], 17) ^ right_rotate(w[i - 2], 19) ^ (w[i - 2] >> 10)
            w[i] = (w[i - 16] + s0 + w[i - 7] + s1) & 0xFFFFFFFF

        a, b, c, d, e, f, g, h = h0, h1, h2, h3, h4, h5, h6, h7

        for i in range(64):
            S1 = right_rotate(e, 6) ^ right_rotate(e, 11) ^ right_rotate(e, 25)
            ch = (e & f) ^ ((~e) & g)
            temp1 = h + S1 + ch + k[i] + w[i]
            S0 = right_rotate(a, 2) ^ right_rotate(a, 13) ^ right_rotate(a, 22)
            maj = (a & b) ^ (a & c) ^ (b & c)
            temp2 = S0 + maj

            h = g
            g = f
            f = e
            e = (d + temp1) & 0xFFFFFFFF
            d = c
            c = b
            b = a
            a = (temp1 + temp2) & 0xFFFFFFFF

        h0 = (h0 + a) & 0xFFFFFFFF
        h1 = (h1 + b) & 0xFFFFFFFF
        h2 = (h2 + c) & 0xFFFFFFFF
        h3 = (h3 + d) & 0xFFFFFFFF
        h4 = (h4 + e) & 0xFFFFFFFF
        h5 = (h5 + f) & 0xFFFFFFFF
        h6 = (h6 + g) & 0xFFFFFFFF
        h7 = (h7 + h) & 0xFFFFFFFF

    # Concatenate the hash values
    hash_value = (h0 << 192 | h1 << 160 | h2 << 128 | h3 << 96 | h4 << 64 | h5 << 32 | h6)

    return format(hash_value, '064x')

message = "Hello, world!".encode('utf-8')
#user_input = input("Enter a message: ")
#message = user_input.encode('utf-8')
result = sha256(message)
print("SHA-256 => Short-form:", result[-18:])
print("SHA-256:", result)
