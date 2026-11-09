"""Эффект «жидкое стекло» (как Liquid Glass в iOS 26 / Telegram) поверх готового кадра.
Стекло = форма со скруглением (SDF): фон под ней преломляется у края, слегка увеличивается,
может размываться (матовое), по краю блик сверху-слева и тёмный кант снизу, мягкая тень."""
import numpy as np
from PIL import Image, ImageFilter


def sdf_rrect(X, Y, cx, cy, hw, hh, r):
    r = min(r, hw, hh)
    qx = np.abs(X - cx) - (hw - r); qy = np.abs(Y - cy) - (hh - r)
    out = np.hypot(np.maximum(qx, 0), np.maximum(qy, 0))
    return out + np.minimum(np.maximum(qx, qy), 0) - r


def sample(src, X, Y):
    H, W = src.shape[:2]
    X = np.clip(X, 0, W - 1.001); Y = np.clip(Y, 0, H - 1.001)
    x0 = X.astype(np.int32); y0 = Y.astype(np.int32); fx = (X - x0)[..., None]; fy = (Y - y0)[..., None]
    a = src[y0, x0]; b = src[y0, x0 + 1]; c = src[y0 + 1, x0]; d = src[y0 + 1, x0 + 1]
    return (a * (1 - fx) + b * fx) * (1 - fy) + (c * (1 - fx) + d * fx) * fy


def glass(img, cx, cy, w, h, r=None, zoom=1.06, refr=34, bevel=30, blur=0, tint=0.12,
          tint_col=(255, 255, 255), shadow=0.13, chroma=0.10, spec=0.85, alpha=1.0):
    """img: float32 HxWx3 (0..255), меняется на месте. w, h — полный размер формы."""
    if w < 4 or h < 4 or alpha <= 0: return img
    H, W = img.shape[:2]; hw, hh = w / 2, h / 2; r = hh if r is None else r
    m = 40
    x0, x1 = int(max(0, cx - hw - m)), int(min(W, cx + hw + m)); y0, y1 = int(max(0, cy - hh - m)), int(min(H, cy + hh + m + 20))
    Y, X = np.mgrid[y0:y1, x0:x1].astype(np.float32)
    d = sdf_rrect(X, Y, cx, cy, hw, hh, r)
    # тень: размытая маска со сдвигом вниз
    if shadow > 0:
        sm = Image.fromarray((np.clip(0.5 - sdf_rrect(X, Y - 10, cx, cy, hw, hh, r), 0, 1) * 255).astype(np.uint8))
        sm = np.asarray(sm.filter(ImageFilter.GaussianBlur(14)), np.float32) / 255 * (d > -2)
        img[y0:y1, x0:x1] *= (1 - shadow * alpha * sm)[..., None]
    inside = np.clip(0.5 - d, 0, 1)
    gy, gx = np.gradient(d); n = np.hypot(gx, gy) + 1e-6; nx, ny = gx / n, gy / n
    t = np.clip(-d / bevel, 0, 1); edge = (1 - t) ** 2.2           # 1 у края, 0 внутри
    src = img
    if blur > 0:
        pad = int(blur * 3 + refr + 10); bx0, by0 = max(0, x0 - pad), max(0, y0 - pad)
        crop = Image.fromarray(np.clip(img[by0:min(H, y1 + pad), bx0:min(W, x1 + pad)], 0, 255).astype(np.uint8))
        bl = np.asarray(crop.filter(ImageFilter.GaussianBlur(blur)), np.float32)
        src = img.copy(); src[by0:by0 + bl.shape[0], bx0:bx0 + bl.shape[1]] = bl
    out = np.empty(X.shape + (3,), np.float32)
    for ch, k in enumerate((1 - chroma, 1.0, 1 + chroma)):   # хроматика: каналы преломляются чуть по-разному
        off = refr * edge * k
        SX = cx + (X - cx) / zoom + nx * off; SY = cy + (Y - cy) / zoom + ny * off
        out[..., ch] = sample(src[..., ch:ch + 1], SX, SY)[..., 0]
    tc = np.array(tint_col, np.float32)
    out = out * (1 - tint) + tc * tint
    out *= (1 - 0.10 * edge ** 1.5)[..., None]                       # объём у края
    # блики: тонкий кант + рефлекс сверху-слева, слабый снизу-справа
    rim = np.exp(d / 2.2) * (d < 0.5)
    lit = np.clip(nx * -0.55 + ny * -0.83, 0, 1); back = np.clip(nx * 0.55 + ny * 0.83, 0, 1)
    hl = spec * (rim * (0.35 + 0.65 * lit) + 0.45 * edge * lit ** 3 + 0.25 * rim * back)
    out = out + (255 - out) * np.clip(hl, 0, 1)[..., None]
    a = (inside * alpha)[..., None]
    img[y0:y1, x0:x1] = img[y0:y1, x0:x1] * (1 - a) + out * a
    return img


def spring(x, k=7.0, w=15.0):
    """1 -> 0 с перелётом (желе). x — секунды с начала движения."""
    x = np.maximum(x, 0); return np.exp(-k * x) * np.cos(w * x)


def ease(x):
    x = min(max(x, 0), 1); return 1 - (1 - x) ** 3
