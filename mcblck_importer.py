import json
import math
import os
import sys
import tkinter as tk
from tkinter import ttk, messagebox
from pathlib import Path

try:
    from PIL import Image, ImageTk, ImageDraw
except ImportError:
    print("This program requires Pillow.")
    print("Install it with:")
    print("    pip install pillow")
    sys.exit(1)


# ============================================================
# Configuration
# ============================================================

TEXTURE_EXTENSIONS = [".png", ".jpg", ".jpeg", ".webp"]

FACE_COLORS = {
    "top": "#dddddd",
    "bottom": "#777777",
    "north": "#bbbbbb",
    "south": "#aaaaaa",
    "west": "#999999",
    "east": "#888888",
}


# ============================================================
# Utility functions
# ============================================================

def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_json(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)

    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write("\n")


def find_texture(mod_root, texture_identifier):
    """
    Converts:

        red_mishanguc_roads:block/white_straight_line

    into:

        src/main/resources/assets/red_mishanguc_roads/textures/block/white_straight_line.png
    """

    if ":" in texture_identifier:
        namespace, path = texture_identifier.split(":", 1)
    else:
        namespace = None
        path = texture_identifier

    if path.startswith("block/"):
        relative = Path("textures") / path
    elif path.startswith("item/"):
        relative = Path("textures") / path
    else:
        relative = Path("textures") / path

    if namespace:
        texture_root = (
            mod_root
            / "src"
            / "main"
            / "resources"
            / "assets"
            / namespace
        )
    else:
        texture_root = (
            mod_root
            / "src"
            / "main"
            / "resources"
            / "assets"
        )

    base = texture_root / relative

    for extension in TEXTURE_EXTENSIONS:
        candidate = Path(str(base) + extension)

        if candidate.exists():
            return candidate

    # Also allow the identifier to already contain an extension.
    if base.exists():
        return base

    return None


def check_resource_path(identifier):
    """
    Minecraft resource paths cannot contain spaces.
    """
    if ":" in identifier:
        namespace, path = identifier.split(":", 1)
    else:
        namespace, path = None, identifier

    problems = []

    if " " in path:
        problems.append("contains spaces")

    if "\\" in path:
        problems.append("contains backslashes")

    if namespace and " " in namespace:
        problems.append("namespace contains spaces")

    return problems


# ============================================================
# Minecraft generation
# ============================================================

def generate_model(model_definition):
    """
    Turns the simplified .mcblck model format into a normal
    Minecraft cube model.
    """

    textures = model_definition.get("textures", {})

    return {
        "parent": "minecraft:block/cube",
        "textures": textures
    }


def generate_blockstate(mcblck):
    return mcblck["blockstate"]


def import_block(mcblck_path, mod_root):
    """
    Imports the .mcblck into the Fabric mod.
    """

    mcblck = load_json(mcblck_path)

    if mcblck.get("format") != "mcblck":
        raise ValueError("This file is not a valid mcblck file.")

    version = mcblck.get("version")

    if version != 1:
        raise ValueError(
            f"Unsupported mcblck version: {version}"
        )

    block = mcblck["block"]

    mod_id = block["mod_id"]
    block_id = block["id"]

    resources = (
        mod_root
        / "src"
        / "main"
        / "resources"
        / "assets"
        / mod_id
    )

    models_dir = resources / "models" / "block"
    blockstates_dir = resources / "blockstates"
    lang_dir = resources / "lang"

    models_dir.mkdir(parents=True, exist_ok=True)
    blockstates_dir.mkdir(parents=True, exist_ok=True)
    lang_dir.mkdir(parents=True, exist_ok=True)

    # --------------------------------------------------------
    # Models
    # --------------------------------------------------------

    model_definitions = mcblck.get("models", {})

    generated_models = []

    for model_id, model_definition in model_definitions.items():

        model_name = model_definition.get("name", model_id)

        model_json = generate_model(model_definition)

        model_path = models_dir / f"{model_name}.json"

        save_json(model_path, model_json)

        generated_models.append(
            {
                "id": model_id,
                "name": model_name,
                "path": model_path,
                "definition": model_definition
            }
        )

    # --------------------------------------------------------
    # Blockstate
    # --------------------------------------------------------

    blockstate = generate_blockstate(mcblck)

    blockstate_path = blockstates_dir / f"{block_id}.json"

    save_json(blockstate_path, blockstate)

    # --------------------------------------------------------
    # Language
    # --------------------------------------------------------

    translations = mcblck.get("translation", {})

    lang_path = lang_dir / "en_us.json"

    if lang_path.exists():
        lang_data = load_json(lang_path)
    else:
        lang_data = {}

    # Merge instead of replacing.
    for key, value in translations.items():
        lang_data[key] = value

    # Sort keys to keep the file tidy.
    lang_data = dict(sorted(lang_data.items()))

    save_json(lang_path, lang_data)

    return {
        "mod_id": mod_id,
        "block_id": block_id,
        "resources": resources,
        "models": generated_models,
        "blockstate": blockstate_path,
        "lang": lang_path
    }


# ============================================================
# Preview renderer
# ============================================================

class BlockPreview:
    """
    A simple isometric Minecraft-block preview.

    It renders the three visible faces:
        top
        left
        right

    Multiple models are displayed independently.
    """

    def __init__(self, parent, mod_root):
        self.parent = parent
        self.mod_root = mod_root

        self.images = []

    def get_texture_image(self, texture_id, size):
        path = find_texture(self.mod_root, texture_id)

        if path is None:
            return self.make_missing_texture(size, texture_id)

        try:
            image = Image.open(path).convert("RGBA")
            image.thumbnail((size, size), Image.Resampling.NEAREST)

            canvas = Image.new(
                "RGBA",
                (size, size),
                (0, 0, 0, 0)
            )

            x = (size - image.width) // 2
            y = (size - image.height) // 2

            canvas.alpha_composite(image, (x, y))

            return canvas

        except Exception:
            return self.make_missing_texture(size, texture_id)

    def make_missing_texture(self, size, texture_id):
        image = Image.new(
            "RGBA",
            (size, size),
            (180, 180, 180, 255)
        )

        draw = ImageDraw.Draw(image)

        # Minecraft-style missing texture
        tile = max(4, size // 8)

        for y in range(0, size, tile):
            for x in range(0, size, tile):

                if ((x // tile) + (y // tile)) % 2 == 0:
                    draw.rectangle(
                        [x, y, x + tile, y + tile],
                        fill=(255, 0, 255, 255)
                    )
                else:
                    draw.rectangle(
                        [x, y, x + tile, y + tile],
                        fill=(0, 0, 0, 255)
                    )

        return image

    def make_face(self, texture, width, height, brightness=1.0):
        """
        Makes a rectangular texture face.
        """

        image = texture.resize(
            (width, height),
            Image.Resampling.NEAREST
        ).convert("RGBA")

        if brightness != 1.0:
            pixels = image.load()

            for y in range(image.height):
                for x in range(image.width):
                    r, g, b, a = pixels[x, y]

                    pixels[x, y] = (
                        int(r * brightness),
                        int(g * brightness),
                        int(b * brightness),
                        a
                    )

        return image

    def create_cube(self, model_definition):
        """
        Creates an isometric cube image using the model's
        texture assignments.
        """

        face_size = 128

        textures = model_definition.get("textures", {})

        top_id = textures.get("top")
        west_id = textures.get("west")
        north_id = textures.get("north")

        if top_id is None:
            top_id = textures.get("up")

        if west_id is None:
            west_id = textures.get("side")

        if north_id is None:
            north_id = textures.get("side")

        if top_id is None:
            top_id = ""

        if west_id is None:
            west_id = ""

        if north_id is None:
            north_id = ""

        top = self.get_texture_image(top_id, face_size)
        left = self.get_texture_image(west_id, face_size)
        right = self.get_texture_image(north_id, face_size)

        # Canvas
        width = 420
        height = 350

        result = Image.new(
            "RGBA",
            (width, height),
            (0, 0, 0, 0)
        )

        # ----------------------------------------------------
        # Make isometric-looking faces.
        #
        # We don't need perfect 3D rendering here; the goal is
        # to give a quick visual preview of the model.
        # ----------------------------------------------------

        cube_width = 180
        cube_height = 100
        side_height = 150

        center_x = width // 2
        top_y = 60

        # Top
        top_face = Image.new(
            "RGBA",
            (cube_width, cube_height),
            (0, 0, 0, 0)
        )

        top_scaled = top.resize(
            (cube_width, cube_height),
            Image.Resampling.NEAREST
        )

        # Shear top into a parallelogram.
        top_skew = top_scaled.transform(
            (cube_width, cube_height),
            Image.Transform.AFFINE,
            (1, 0.5, -cube_height * 0.25, 0, 1, 0),
            resample=Image.Resampling.BILINEAR
        )

        # Instead of complicated perspective warping, use
        # polygons and texture previews clipped approximately
        # to each face.

        draw = ImageDraw.Draw(result)

        top_points = [
            (center_x, top_y),
            (center_x + cube_width // 2, top_y + cube_height // 2),
            (center_x, top_y + cube_height),
            (center_x - cube_width // 2, top_y + cube_height // 2),
        ]

        left_points = [
            top_points[2],
            top_points[3],
            (
                top_points[3][0],
                top_points[3][1] + side_height
            ),
            (
                top_points[2][0],
                top_points[2][1] + side_height
            ),
        ]

        right_points = [
            top_points[2],
            top_points[1],
            (
                top_points[1][0],
                top_points[1][1] + side_height
            ),
            (
                top_points[2][0],
                top_points[2][1] + side_height
            ),
        ]

        # Draw base colors first.
        draw.polygon(
            top_points,
            fill="#cccccc",
            outline="#333333"
        )

        draw.polygon(
            left_points,
            fill="#999999",
            outline="#333333"
        )

        draw.polygon(
            right_points,
            fill="#aaaaaa",
            outline="#333333"
        )

        # ----------------------------------------------------
        # Texture approximation
        # ----------------------------------------------------

        # Top texture
        top_texture = top.resize(
            (cube_width, cube_height),
            Image.Resampling.NEAREST
        )

        result.alpha_composite(
            top_texture,
            (
                center_x - cube_width // 2,
                top_y + cube_height // 4
            )
        )

        # The above texture is deliberately allowed to extend
        # beyond the polygon because this is a lightweight
        # preview, not the Minecraft renderer.

        return result

    def add_model(self, parent, model):
        frame = ttk.Frame(parent)
        frame.pack(fill="x", padx=10, pady=10)

        model_name = model["name"]

        ttk.Label(
            frame,
            text=f"Model: {model_name}",
            font=("Segoe UI", 12, "bold")
        ).pack(anchor="w")

        image = self.create_cube(model["definition"])

        photo = ImageTk.PhotoImage(image)

        self.images.append(photo)

        label = ttk.Label(
            frame,
            image=photo
        )

        label.pack()

        textures = model["definition"].get("textures", {})

        texture_text = "\n".join(
            f"{face}: {texture}"
            for face, texture in textures.items()
        )

        ttk.Label(
            frame,
            text=texture_text,
            justify="left"
        ).pack(anchor="w")


# ============================================================
# Preview window
# ============================================================

def show_preview(imported, mod_root):
    window = tk.Tk()

    window.title(
        f"MCBLCK Preview - {imported['block_id']}"
    )

    window.geometry("700x800")

    # --------------------------------------------------------
    # Header
    # --------------------------------------------------------

    header = ttk.Frame(window)
    header.pack(fill="x", padx=15, pady=15)

    ttk.Label(
        header,
        text=imported["block_id"],
        font=("Segoe UI", 18, "bold")
    ).pack(anchor="w")

    ttk.Label(
        header,
        text=f"Namespace: {imported['mod_id']}"
    ).pack(anchor="w")

    # --------------------------------------------------------
    # Scrollable preview
    # --------------------------------------------------------

    container = ttk.Frame(window)
    container.pack(fill="both", expand=True)

    canvas = tk.Canvas(container)

    scrollbar = ttk.Scrollbar(
        container,
        orient="vertical",
        command=canvas.yview
    )

    content = ttk.Frame(canvas)

    content.bind(
        "<Configure>",
        lambda e: canvas.configure(
            scrollregion=canvas.bbox("all")
        )
    )

    canvas.create_window(
        (0, 0),
        window=content,
        anchor="nw"
    )

    canvas.configure(
        yscrollcommand=scrollbar.set
    )

    canvas.pack(
        side="left",
        fill="both",
        expand=True
    )

    scrollbar.pack(
        side="right",
        fill="y"
    )

    preview = BlockPreview(
        content,
        mod_root
    )

    for model in imported["models"]:
        preview.add_model(
            content,
            model
        )

    # --------------------------------------------------------
    # Import information
    # --------------------------------------------------------

    info = ttk.LabelFrame(
        content,
        text="Imported files"
    )

    info.pack(
        fill="x",
        padx=10,
        pady=15
    )

    ttk.Label(
        info,
        text=f"Blockstate:\n{imported['blockstate']}"
    ).pack(anchor="w", padx=10, pady=5)

    ttk.Label(
        info,
        text=f"Language:\n{imported['lang']}"
    ).pack(anchor="w", padx=10, pady=5)

    window.mainloop()


# ============================================================
# Validation
# ============================================================

def validate_mcblck(mcblck, mod_root):
    warnings = []

    block = mcblck["block"]

    mod_id = block["mod_id"]

    if ":" in mod_id:
        warnings.append(
            f"mod_id '{mod_id}' should not contain ':'"
        )

    for model_id, model in mcblck.get("models", {}).items():

        textures = model.get("textures", {})

        for face, texture in textures.items():

            problems = check_resource_path(texture)

            for problem in problems:
                warnings.append(
                    f"Model '{model_id}', face '{face}': "
                    f"texture '{texture}' {problem}"
                )

            if find_texture(mod_root, texture) is None:
                warnings.append(
                    f"Model '{model_id}', face '{face}': "
                    f"texture '{texture}' was not found."
                )

    return warnings


# ============================================================
# Main
# ============================================================

def main():
    import tkinter as tk
    from tkinter import filedialog

    # --------------------------------------------------------
    # Get .mcblck file
    # --------------------------------------------------------

    if len(sys.argv) >= 2:
        mcblck_path = Path(sys.argv[1]).resolve()
    else:
        # Open a normal file picker.
        root = tk.Tk()
        root.withdraw()

        selected_file = filedialog.askopenfilename(
            title="Open MCBLCK file",
            filetypes=[
                ("MCBLCK files", "*.mcblck"),
                ("JSON files", "*.json"),
                ("All files", "*.*")
            ]
        )

        root.destroy()

        # User cancelled the dialog.
        if not selected_file:
            return

        mcblck_path = Path(selected_file).resolve()

    # --------------------------------------------------------
    # Get mod root
    # --------------------------------------------------------

    if len(sys.argv) >= 3:
        mod_root = Path(sys.argv[2]).resolve()
    else:
        # Assume the script is being run from the mod root.
        mod_root = Path.cwd().resolve()

    # --------------------------------------------------------
    # Validate file
    # --------------------------------------------------------

    if not mcblck_path.exists():
        print("ERROR: File does not exist:")
        print(mcblck_path)
        return

    try:
        mcblck = load_json(mcblck_path)

        warnings = validate_mcblck(
            mcblck,
            mod_root
        )

        print()
        print("========================================")
        print(" MCBLCK IMPORTER")
        print("========================================")
        print()

        print(f"File:     {mcblck_path}")
        print(f"Mod root: {mod_root}")
        print()

        if warnings:
            print("WARNINGS:")
            print()

            for warning in warnings:
                print(f"  ! {warning}")

            print()

        imported = import_block(
            mcblck_path,
            mod_root
        )

        print("Imported successfully!")
        print()

        print("Models:")

        for model in imported["models"]:
            print(f"  {model['name']}.json")

        print()

        print(
            f"Blockstate: "
            f"{imported['blockstate']}"
        )

        print(
            f"Language:   "
            f"{imported['lang']}"
        )

        print()

        # Show GUI preview.
        show_preview(
            imported,
            mod_root
        )

    except Exception as e:
        print()
        print("ERROR:")
        print(e)
        print()

        try:
            messagebox.showerror(
                "MCBLCK Importer",
                str(e)
            )
        except Exception:
            pass


if __name__ == "__main__":
    main()