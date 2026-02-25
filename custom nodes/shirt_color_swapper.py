"""
ShirtColorSwapper v3 - ComfyUI Custom Node
Adds "white" preset as first option — returns original image unchanged (mockup is already white).
Recolors other colors using luminosity-preserving transfer for realistic fabric appearance.
"""

import torch
import numpy as np


PRESET_COLORS = {
    "white":  None,        # passthrough — no recoloring
    "blue":   "#1E3A6E",
    "green":  "#1E4D2B",
    "black":  "#1A1A1A",
    "custom": None,        # uses hex_color input
}


def hex_to_rgb(hex_str: str):
    hex_str = hex_str.strip().lstrip("#")
    if len(hex_str) != 6:
        raise ValueError(f"Invalid hex: #{hex_str} — must be 6 chars e.g. #1E3A6E")
    return (
        int(hex_str[0:2], 16) / 255.0,
        int(hex_str[2:4], 16) / 255.0,
        int(hex_str[4:6], 16) / 255.0,
    )


def luminosity_color_transfer(img, mask, target_rgb, blend_strength):
    lum = (
        img[..., 0] * 0.2126 +
        img[..., 1] * 0.7152 +
        img[..., 2] * 0.0722
    )
    tr, tg, tb = target_rgb
    recolored = np.stack([lum * tr, lum * tg, lum * tb], axis=-1)

    if max(tr, tg, tb) < 0.15:
        recolored = recolored + np.stack([lum * 0.08] * 3, axis=-1)

    recolored = np.clip(recolored, 0.0, 1.0)
    mask_3ch = np.stack([mask, mask, mask], axis=-1)
    result = img * (1.0 - mask_3ch * blend_strength) + recolored * (mask_3ch * blend_strength)
    return np.clip(result, 0.0, 1.0)


class ShirtColorSwapper:
    """
    Recolors a white shirt mockup using luminosity-preserving color transfer.
    Select 'white' to keep the original mockup color unchanged.
    Select 'custom' and enter any hex code for your own color.
    """

    CATEGORY = "ecommerce/mockup"
    RETURN_TYPES = ("IMAGE",)
    RETURN_NAMES = ("image",)
    FUNCTION = "swap_color"

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image": ("IMAGE",),
                "mask": ("MASK",),
                "color_preset": (list(PRESET_COLORS.keys()), {"default": "white"}),
                "hex_color": ("STRING", {
                    "default": "#1E3A6E",
                    "multiline": False,
                    "placeholder": "Only used when color_preset = custom",
                }),
                "blend_strength": ("FLOAT", {
                    "default": 1.0,
                    "min": 0.0,
                    "max": 1.0,
                    "step": 0.05,
                    "display": "slider",
                }),
            },
        }

    def swap_color(self, image, mask, color_preset, hex_color, blend_strength):
        # White = passthrough, return original image untouched
        if color_preset == "white":
            return (image,)

        # Resolve target color
        if color_preset == "custom":
            try:
                target_rgb = hex_to_rgb(hex_color)
            except ValueError as e:
                print(f"[ShirtColorSwapper] {e} — falling back to blue")
                target_rgb = hex_to_rgb("#1E3A6E")
        else:
            target_rgb = hex_to_rgb(PRESET_COLORS[color_preset])

        # Prepare arrays
        img_np = image[0].cpu().numpy().astype(np.float32)
        msk_np = mask[0].cpu().numpy().astype(np.float32)

        if msk_np.ndim == 3:
            msk_np = msk_np[0]

        if msk_np.shape != img_np.shape[:2]:
            from PIL import Image as PILImage
            msk_pil = PILImage.fromarray((msk_np * 255).astype(np.uint8))
            msk_pil = msk_pil.resize((img_np.shape[1], img_np.shape[0]), PILImage.NEAREST)
            msk_np = np.array(msk_pil).astype(np.float32) / 255.0

        result_np = luminosity_color_transfer(img_np, msk_np, target_rgb, blend_strength)
        result = torch.from_numpy(result_np).unsqueeze(0)
        return (result,)


NODE_CLASS_MAPPINGS = {
    "ShirtColorSwapper": ShirtColorSwapper,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "ShirtColorSwapper": "👕 Shirt Color Swapper",
}
