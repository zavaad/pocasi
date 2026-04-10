#!/usr/bin/env python3
"""Generates simple weather app icons (PNG) without any external dependencies."""
import struct, zlib, os

def make_png(size, bg_color, text_emoji=None):
    """Create a simple PNG with gradient background."""
    pixels = []
    r1, g1, b1 = 13, 27, 62    # dark blue top
    r2, g2, b2 = 26, 42, 74    # lighter blue bottom
    for y in range(size):
        row = []
        t = y / size
        r = int(r1 + (r2-r1)*t)
        g = int(g1 + (g2-g1)*t)
        b = int(b1 + (b2-b1)*t)
        for x in range(size):
            row.extend([r, g, b, 255])
        pixels.append(bytes([0]) + bytes(row))  # filter type 0 per row

    def chunk(name, data):
        c = name + data
        return struct.pack('>I', len(data)) + c + struct.pack('>I', zlib.crc32(c) & 0xffffffff)

    ihdr = struct.pack('>IIBBBBB', size, size, 8, 2, 0, 0, 0)
    raw = b''.join(pixels)
    idat = zlib.compress(raw)

    png = b'\x89PNG\r\n\x1a\n'
    png += chunk(b'IHDR', ihdr)
    png += chunk(b'IDAT', idat)
    png += chunk(b'IEND', b'')
    return png

os.makedirs('icons', exist_ok=True)
for size in [192, 512]:
    with open(f'icons/icon-{size}.png', 'wb') as f:
        f.write(make_png(size, None))
    print(f'icons/icon-{size}.png created ({size}x{size})')

print('Icons generated successfully!')
print('Note: These are simple gradient icons. Replace with custom SVG/PNG for better look.')
