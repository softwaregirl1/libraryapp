
import hashlib
from PIL import Image, ImageDraw, ImageFont
import customtkinter as ctk

PALETTE = [
    ("#2D7DD2", "#1B5FA3"),  # blue
    ("#4CAF50", "#357A38"),  # green
    ("#E76F51", "#B84F35"),  # terracotta
    ("#8E44AD", "#6C3483"),  # purple
    ("#F4A261", "#C9793B"),  # amber
    ("#2A9D8F", "#1F7168"),  # teal
    ("#E63946", "#B32B35"),  # red
    ("#1F3A5F", "#14273F"),  # navy
]


def _pick_colors(seed_text: str):
    """Deterministically pick a palette pair based on the text, so the
    same book always gets the same cover color."""
    digest = hashlib.md5(seed_text.encode()).hexdigest()
    index = int(digest, 16) % len(PALETTE)
    return PALETTE[index]


def _get_font(size: int):
    # Falls back to PIL's default bitmap font if no system font is found
    for name in ("arialbd.ttf", "DejaVuSans-Bold.ttf", "Arial Bold.ttf"):
        try:
            return ImageFont.truetype(name, size)
        except (OSError, IOError):
            continue
    return ImageFont.load_default()


def make_book_cover(title: str, width: int = 90, height: int = 130) -> Image.Image:
    """Create a gradient book-cover thumbnail with the book's initials."""
    top_color, bottom_color = _pick_colors(title)
    top_rgb = tuple(int(top_color[i:i + 2], 16) for i in (1, 3, 5))
    bottom_rgb = tuple(int(bottom_color[i:i + 2], 16) for i in (1, 3, 5))

    img = Image.new("RGB", (width, height), top_rgb)
    draw = ImageDraw.Draw(img)

    # Vertical gradient
    for y in range(height):
        ratio = y / height
        r = int(top_rgb[0] + (bottom_rgb[0] - top_rgb[0]) * ratio)
        g = int(top_rgb[1] + (bottom_rgb[1] - top_rgb[1]) * ratio)
        b = int(top_rgb[2] + (bottom_rgb[2] - top_rgb[2]) * ratio)
        draw.line([(0, y), (width, y)], fill=(r, g, b))

    # Spine highlight (thin lighter strip on the left edge)
    draw.rectangle([0, 0, 4, height], fill=(255, 255, 255, 60))

    # Initials (up to 2 letters from the title)
    words = [w for w in title.split() if w.isalnum() or w[0].isalpha()]
    initials = "".join(w[0].upper() for w in words[:2]) if words else "?"

    font = _get_font(28)
    bbox = draw.textbbox((0, 0), initials, font=font)
    text_w, text_h = bbox[2] - bbox[0], bbox[3] - bbox[1]
    draw.text(((width - text_w) / 2 - bbox[0], (height - text_h) / 2 - bbox[1]),
              initials, font=font, fill="white")

    return img


def make_ctk_book_cover(title: str, width: int = 90, height: int = 130) -> ctk.CTkImage:
    pil_img = make_book_cover(title, width, height)
    return ctk.CTkImage(light_image=pil_img, dark_image=pil_img, size=(width, height))


def load_real_logo(path: str, max_size: int = 72) -> ctk.CTkImage:
    """Load an actual logo image file (e.g. the real Veritas University
    logo), scaled to fit within max_size while keeping its aspect ratio."""
    img = Image.open(path).convert("RGBA")
    img.thumbnail((max_size, max_size), Image.LANCZOS)
    return ctk.CTkImage(light_image=img, dark_image=img, size=img.size)


def make_logo(size: int = 64) -> ctk.CTkImage:
    """A simple open-book icon logo, drawn programmatically."""
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    cx, cy = size / 2, size / 2
    page_w = size * 0.38
    page_h = size * 0.5

    # Left page
    draw.polygon(
        [(cx, cy - page_h / 2), (cx - page_w, cy - page_h / 2 + 6),
         (cx - page_w, cy + page_h / 2 - 6), (cx, cy + page_h / 2)],
        fill="#F4A261"
    )
    # Right page
    draw.polygon(
        [(cx, cy - page_h / 2), (cx + page_w, cy - page_h / 2 + 6),
         (cx + page_w, cy + page_h / 2 - 6), (cx, cy + page_h / 2)],
        fill="#2D7DD2"
    )
    # Spine
    draw.line([(cx, cy - page_h / 2), (cx, cy + page_h / 2)], fill="white", width=3)

    return ctk.CTkImage(light_image=img, dark_image=img, size=(size, size))


def make_avatar(name: str, size: int = 40) -> ctk.CTkImage:
    """A circular avatar with the member's initial, colored by name."""
    top_color, bottom_color = _pick_colors(name)
    color = tuple(int(top_color[i:i + 2], 16) for i in (1, 3, 5))

    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw.ellipse([0, 0, size, size], fill=color)

    initial = name[0].upper() if name else "?"
    font = _get_font(int(size * 0.45))
    bbox = draw.textbbox((0, 0), initial, font=font)
    text_w, text_h = bbox[2] - bbox[0], bbox[3] - bbox[1]
    draw.text(((size - text_w) / 2 - bbox[0], (size - text_h) / 2 - bbox[1]),
              initial, font=font, fill="white")

    return ctk.CTkImage(light_image=img, dark_image=img, size=(size, size))


if __name__ == "__main__":
    make_book_cover("Clean Code").save("preview_cover1.png")
    make_book_cover("The Pragmatic Programmer").save("preview_cover2.png")
    make_book_cover("Introduction to Algorithms").save("preview_cover3.png")
    print("Saved 3 preview covers to the current folder.")