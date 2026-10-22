#!/usr/bin/env python3
"""AWTRIX NG weather backgrounds: full-width 32x8 animated GIFs.

The sun or moon stays at the left edge (x 0..7). Clouds drift from left to right across the whole
display and are semi-transparent, so the sun/moon shows through them dimmed - by day and night
the sky looks different even under thick cloud (night clouds are darker).

File name:  Wx<Type><Body>.gif   e.g. WxCloudHeavySun, WxCloudHeavyMoon3North, WxCloudHeavyMoon3South
  Type = Clear | CloudPart | Cloud | CloudFog | CloudDrizzle | CloudSleet | CloudRain | CloudHeavy |
         CloudSnow | CloudSnowHeavy | CloudThunder | CloudHail
  Body = Sun | Moon0 | Moon4 | Moon<n>North | Moon<n>South     (n = 1,2,3,5,6,7)
Moon phases: 0 new, 1 waxing crescent, 2 first quarter, 3 waxing gibbous, 4 full,
             5 waning gibbous, 6 last quarter, 7 waning crescent. New and full moon look the same on
             both hemispheres, so they have no North/South suffix. The south set is the mirror image.

Every frame is fully opaque (no transparency), because AWTRIX keeps the previous frame's pixels
where a GIF is transparent. One GIF is at most about 3.6 KB; one hemisphere is about 285 KB,
both about 476 KB (a 4 MB board has only 512 KB of storage for everything).

No dependencies. Usage:
  python3 make_weather_backgrounds.py [outdir] [--hemisphere north|south|both]   (default north)
"""
import math
import os
import random
import struct
import sys

W, H, BW = 32, 8, 8


# ---------------------------------------------------------------- colour helpers
def split(c):
    return (c >> 16) & 255, (c >> 8) & 255, c & 255


def pack(r, g, b):
    return (min(255, max(0, int(r + .5))) << 16) | (min(255, max(0, int(g + .5))) << 8) | min(255, max(0, int(b + .5)))


def mix(a, b, t):
    """b over a with opacity t"""
    ar, ag, ab = split(a)
    br, bg, bb = split(b)
    return pack(ar + (br - ar) * t, ag + (bg - ag) * t, ab + (bb - ab) * t)


def scale(c, k):
    r, g, b = split(c)
    return pack(r * k, g * k, b * k)


# ---------------------------------------------------------------- sun and moon (8x8 tile)
DISC = {(x, y) for y in range(8) for x in range(8) if (x - 3.5) ** 2 + (y - 3.5) ** 2 <= 16}
RIM = 0xFFB300
CORE = [0xFFCC00, 0xFFD633, 0xFFE066, 0xFFEB8A, 0xFFF5BF]       # pulsing 4x4 core
LIT, DARK = 0xE8E4C9, 0x404040                                   # moon: lit part, dark grey shadow
TERM = [1, .5, 0, -.5, -1, -.5, 0, .5]                           # terminator per phase


def lit(n, x, y):
    """Lit pixel in phase n, northern hemisphere (0 new, 4 full, waxing = lit on the right)."""
    if n == 0:
        return False
    if n == 4:
        return True
    u = (x - 3.5) / math.sqrt(16 - (y - 3.5) ** 2)
    return u >= TERM[n] if n < 4 else u <= -TERM[n]


def body_pixel(body, f, x, y):
    if (x, y) not in DISC:
        return 0
    if body[0] == 'sun':
        t = f % 16
        t = t if t <= 8 else 16 - t
        return CORE[min(t // 2, 4)] if 2 <= x <= 5 and 2 <= y <= 5 else RIM
    n, south = body[1], body[2]
    return LIT if lit(n, 7 - x if south else x, y) else DARK        # south = mirror image


# ---------------------------------------------------------------- weather types
# P: cloud pattern period (px), spp: frames per px of drift, delay: 1/100 s, n: frames
# blobs: (cx, cy, rx, ry), gain: density gain, amax: max cloud opacity over sun/moon
# tint: (day, night) cloud colour, precip: list of (kind, count)
T = {
    'Clear':          dict(P=1, spp=1, delay=20, n=16, blobs=[], precip=[]),
    'CloudPart':      dict(P=32, spp=1, delay=30, n=32, amax=.70, gain=1.7, tint=(0x8C96A8, 0x34405C),
                           blobs=[(7, 2.2, 6, 2.3), (23, 3.3, 7, 2.6)], precip=[]),
    'Cloud':          dict(P=32, spp=1, delay=30, n=32, amax=.75, gain=1.9, tint=(0x7A8498, 0x2C3448),
                           blobs=[(3, 2, 8, 3), (12, 3.2, 8, 3), (20, 2, 8, 3), (28, 3.2, 8, 3)], precip=[]),
    'CloudFog':       dict(P=16, spp=1, delay=40, n=16, amax=.60, tint=(0x808A94, 0x363E4A),
                           blobs=[], precip=[], fog=True),
    'CloudDrizzle':   dict(P=16, spp=2, delay=15, n=32, amax=.75, gain=1.8, tint=(0x6E788C, 0x282E40),
                           blobs=[(3, 2, 7, 3), (11, 3, 6, 3)], precip=[('drizzle', 5)]),
    'CloudSleet':     dict(P=16, spp=2, delay=15, n=32, amax=.78, gain=1.9, tint=(0x667086, 0x262C3E),
                           blobs=[(3, 2.3, 8, 3.2), (11, 3, 6, 3)], precip=[('rain', 5), ('snow', 5)]),
    'CloudRain':      dict(P=16, spp=2, delay=15, n=32, amax=.78, gain=1.9, tint=(0x636D82, 0x242A3C),
                           blobs=[(3, 2.3, 8, 3.2), (11, 3, 6, 3)], precip=[('rain', 9)]),
    'CloudHeavy':     dict(P=16, spp=2, delay=15, n=32, amax=.82, gain=2.1, tint=(0x4A5266, 0x1C2230),
                           blobs=[(3, 2.5, 8, 3.6), (11, 3, 7, 3.4)], precip=[('heavy', 13)]),
    'CloudSnow':      dict(P=16, spp=2, delay=15, n=32, amax=.75, gain=1.9, tint=(0x7C869C, 0x2E364A),
                           blobs=[(3, 2.3, 8, 3.2), (11, 3, 6, 3)], precip=[('snow', 8)]),
    'CloudSnowHeavy': dict(P=16, spp=2, delay=15, n=32, amax=.82, gain=2.1, tint=(0x667086, 0x262C3E),
                           blobs=[(3, 2.5, 8, 3.6), (11, 3, 7, 3.4)], precip=[('blizzard', 14)]),
    'CloudThunder':   dict(P=16, spp=2, delay=15, n=32, amax=.82, gain=2.1, tint=(0x40485C, 0x181E2C),
                           blobs=[(3, 2.5, 8, 3.6), (11, 3, 7, 3.4)], precip=[('rain', 9)], bolt=True),
    'CloudHail':      dict(P=16, spp=2, delay=15, n=32, amax=.82, gain=2.1, tint=(0x40485C, 0x181E2C),
                           blobs=[(3, 2.5, 8, 3.6), (11, 3, 7, 3.4)], precip=[('hail', 7), ('rain', 5)], bolt=True),
}
ALV = [0, .35, .65, 1.0]                      # quantised cloud density -> opacity factor
DROP = {'rain': 0x5FA5FF, 'heavy': 0x6EB4FF, 'drizzle': 0x4678BE, 'snow': 0xEBF0FF,
        'blizzard': 0xFFFFFF, 'hail': 0xFFFFFF}
SWAY = [0, 1, 1, 0, -1, -1, 0, 0]
BOLTS = {5: (1.0, 11), 6: (.5, 11), 19: (1.0, 25), 20: (.5, 25), 21: (.2, 25)}   # frame -> (strength, x)
BOLT_DX = [0, 0, -1, -1, 0, 0]


def streams(name, spec):
    """Fixed, deterministic drop positions per type: (kind, x, phase)."""
    rnd = random.Random(sum(map(ord, name)))
    out = []
    for kind, cnt in spec:
        for i in range(cnt):
            x = (int((i + .5) * W / cnt) + rnd.randint(-1, 1)) % W
            out.append((kind, x, rnd.randint(0, 15)))
    return out


def cloud_alpha(t, x, y, f):
    shift = f // t['spp']
    if t.get('fog'):
        v = .5 + .5 * math.sin(2 * math.pi * (x - shift) / 16 + .9 * y)
        d = v * (1 if 2 <= y <= 5 else .6 if y in (1, 6) else 0)
        d *= 1.15
    else:
        d = 0.0
        for cx, cy, rx, ry in t['blobs']:
            dx = (x - cx - shift + t['P'] / 2) % t['P'] - t['P'] / 2
            d = max(d, 1 - (dx / rx) ** 2 - ((y - cy) / ry) ** 2)
        d = min(1.0, d * t['gain'])
    lvl = 0 if d < .12 else 1 if d < .40 else 2 if d < .70 else 3
    return ALV[lvl] * t['amax']


def render(name, body, f):
    """One full 32x8 frame as 8 rows of RGB ints."""
    t = T[name]
    day = body[0] == 'sun'
    tint = t['tint'][0 if day else 1] if t['blobs'] or t.get('fog') else 0
    flash = BOLTS.get(f % t['n'], (0, 0))[0] if t.get('bolt') else 0
    if flash:
        tint = scale(tint, 1 + .7 * flash)
    g = [[0] * W for _ in range(H)]
    for y in range(H):
        for x in range(W):
            c = body_pixel(body, f, x, y) if x < BW else 0
            a = cloud_alpha(t, x, y, f) if (t['blobs'] or t.get('fog')) else 0
            g[y][x] = mix(c, tint, a) if a else c
    k = 1 if day else .72
    for kind, x0, ph in streams(name, t['precip']):
        if kind == 'hail':
            y = (2 * f + ph) % 8
        elif kind in ('rain', 'heavy'):
            y = (f + ph) % 8
        else:                                   # drizzle, snow, blizzard fall one row per 2 frames
            y = ((f + ph) // 2) % 8
        x = x0
        if kind == 'snow':
            x = (x0 + SWAY[(y + ph) % 8]) % W
        elif kind == 'blizzard':
            x = (x0 + y // 2) % W
        col = scale(DROP[kind], k)
        for yy in ([y, y - 1] if kind == 'heavy' else [y]):
            if 2 <= yy < H:
                g[yy][x] = col
    if flash:
        bx = BOLTS[f % t['n']][1]
        for i, dx in enumerate(BOLT_DX):
            g[1 + i][(bx + dx) % W] = scale(0xFFF0A0, flash)
    return g


# ---------------------------------------------------------------- GIF writer (opaque frames)
def lzw(data, mcs):
    clear, eoi = 1 << mcs, (1 << mcs) + 1
    out, acc, nb = bytearray(), 0, 0

    def emit(code, size):
        nonlocal acc, nb
        acc |= code << nb
        nb += size
        while nb >= 8:
            out.append(acc & 255)
            acc >>= 8
            nb -= 8

    def reset():
        return {bytes([i]): i for i in range(clear)}, eoi + 1, mcs + 1

    table, nxt, size = reset()
    emit(clear, size)
    w = b''
    for v in data:
        wc = w + bytes([v])
        if wc in table:
            w = wc
            continue
        emit(table[w], size)
        table[wc] = nxt
        nxt += 1
        if nxt > (1 << size) and size < 12:
            size += 1
        if nxt >= 4095:
            emit(clear, size)
            table, nxt, size = reset()
        w = bytes([v])
    if w:
        emit(table[w], size)
    emit(eoi, size)
    if nb:
        out.append(acc & 255)
    return bytes(out)


def write_gif(path, frames, delay):
    w, h = len(frames[0][0]), len(frames[0])
    if all(fr == frames[0] for fr in frames):
        frames = frames[:1]                                  # static picture -> single frame
    cols = sorted({c for fr in frames for r in fr for c in r})
    assert len(cols) <= 256, (path, len(cols))
    idx = {c: i for i, c in enumerate(cols)}
    bits = max(2, (len(cols) - 1).bit_length())
    pal = [split(c) for c in cols] + [(0, 0, 0)] * ((1 << bits) - len(cols))
    b = bytearray(b'GIF89a' + struct.pack('<HHBBB', w, h, 0x80 | (bits - 1), 0, 0))
    for r, g_, bl in pal:
        b += bytes((r, g_, bl))
    if len(frames) > 1:
        b += b'\x21\xFF\x0BNETSCAPE2.0\x03\x01\x00\x00\x00'
    for fr in frames:
        b += b'\x21\xF9\x04' + bytes((1 << 2,)) + struct.pack('<H', delay) + b'\x00\x00'   # opaque, disposal 1
        b += b'\x2C' + struct.pack('<HHHHB', 0, 0, w, h, 0) + bytes((bits,))
        data = lzw(bytes(idx[c] for r in fr for c in r), bits)
        for i in range(0, len(data), 255):
            blk = data[i:i + 255]
            b += bytes((len(blk),)) + blk
        b += b'\x00'
    b += b'\x3B'
    with open(path, 'wb') as fh:
        fh.write(b)
    return len(b)


def bodies(hemis):
    """(file name part, body tuple) for every wanted body."""
    out = [('Sun', ('sun',)), ('Moon0', ('moon', 0, False)), ('Moon4', ('moon', 4, False))]
    for n in (1, 2, 3, 5, 6, 7):
        if hemis in ('north', 'both'):
            out.append(('Moon%dNorth' % n, ('moon', n, False)))
        if hemis in ('south', 'both'):
            out.append(('Moon%dSouth' % n, ('moon', n, True)))
    return out


def main():
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    hemis = sys.argv[sys.argv.index('--hemisphere') + 1] if '--hemisphere' in sys.argv else 'north'
    if args and args[0] == hemis:
        args = args[1:]
    out = args[0] if args else 'icons'
    os.makedirs(out, exist_ok=True)
    total = files = 0
    for name, t in T.items():
        sub = 0
        for part, body in bodies(hemis):
            sub += write_gif(os.path.join(out, 'Wx%s%s.gif' % (name, part)),
                             [render(name, body, f) for f in range(t['n'])], t['delay'])
            files += 1
        total += sub
        print('%-15s %2d frames, %3d ms, %2d files %6d B' % (name, t['n'], t['delay'] * 10, len(bodies(hemis)), sub))
    print('%d files, %d bytes (%.0f KB)' % (files, total, total / 1024))


if __name__ == '__main__':
    main()