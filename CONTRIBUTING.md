# Contributing to Red Mishang UC Road Blocks

Thank you for contributing to Red Mishang UC Road Blocks!

This guide explains how to add a new road block and submit it as a pull request.

## Before You Start

Make sure you have:

* Git installed
* A GitHub account
* A Java development environment suitable for Fabric 1.20.1
* A working copy of the project
* Minecraft 1.20.1
* Fabric Loader
* Fabric API
* Mishang Urban Construction
* WorldEdit for testing the replacement commands

Before creating a new block, check whether the block has already been added.

---

# 1. Fork the Repository

Go to the GitHub repository and click **Fork**.

This creates your own copy of the project where you can make changes without modifying the main repository directly.

Clone your fork:

```bash
git clone https://github.com/YOUR_USERNAME/Red-Mishang-UC-Road-Blocks.git
cd Red-Mishang-UC-Road-Blocks
```

Open the project in IntelliJ IDEA or another Java IDE.

---

# 2. Create Your Block

Red Mishang UC Road Blocks currently supports several different block orientations.

Choose the block class that matches the block you are adding.

### Axis blocks

Use `AxisRoadBlock` for blocks with:

```text
axis=x
axis=z
```

Example:

```mcfunction
/setblock ~ ~ ~ red_mishanguc_roads:my_block[axis=x]
```

### Normal directional blocks

Use `FacingRoadBlock` for:

```text
facing=north
facing=east
facing=south
facing=west
```

### Diagonal directional blocks

Use `DiagonalFacingRoadBlock` for:

```text
facing=north_east
facing=south_east
facing=south_west
facing=north_west
```

### Axis + diagonal directional blocks

Use `AxisDiagonalFacingRoadBlock` for blocks containing both:

```text
axis=x/z
facing=north_east/south_east/south_west/north_west
```

---

# 3. Register the Block

Open:

```text
src/main/java/com/hha/redmishangucroadblocks/ModBlocks.java
```

Add your block to `registerBlocks()`.

For example:

```java
registerRoadBlock(
        "my_new_road_block",
        RoadBlockType.AXIS
);
```

Use the appropriate `RoadBlockType` for your block.

The name should:

* Use lowercase letters
* Use underscores instead of spaces
* Describe the block clearly
* Match the name used by the blockstate, model, and texture files

For example:

```text
white_straight_line
white_bevel_angle_line
yellow_offset_straight_line
```

---

# 4. Add the Blockstate

Create:

```text
src/main/resources/assets/red_mishanguc_roads/blockstates/my_new_road_block.json
```

The blockstate must match the properties used by your block.

For an axis block:

```json
{
  "variants": {
    "axis=x": {
      "model": "red_mishanguc_roads:block/my_new_road_block"
    },
    "axis=z": {
      "model": "red_mishanguc_roads:block/my_new_road_block"
    }
  }
}
```

For a diagonal block:

```json
{
  "variants": {
    "facing=south_west": {
      "model": "red_mishanguc_roads:block/my_new_road_block"
    },
    "facing=north_west": {
      "model": "red_mishanguc_roads:block/my_new_road_block",
      "y": 90
    },
    "facing=north_east": {
      "model": "red_mishanguc_roads:block/my_new_road_block",
      "y": 180
    },
    "facing=south_east": {
      "model": "red_mishanguc_roads:block/my_new_road_block",
      "y": 270
    }
  }
}
```

Make sure every possible blockstate has a corresponding variant.

---

# 5. Add the Block Model

Create:

```text
src/main/resources/assets/red_mishanguc_roads/models/block/my_new_road_block.json
```

For example:

```json
{
  "textures": {
    "particle": "minecraft:block/red_terracotta",
    "line": "red_mishanguc_roads:block/my_new_road_block"
  },
  "elements": [
    ...
  ]
}
```

Keep models as simple as possible when possible.

If the model needs a mirrored version for another axis, create a separate model rather than trying to force an incorrect rotation.

For example:

```text
my_new_road_block.json
my_new_road_block_z.json
```

---

# 6. Add the Texture

Put the texture in:

```text
src/main/resources/assets/red_mishanguc_roads/textures/block/
```

For example:

```text
my_new_road_block.png
```

Textures should normally be PNG files.

If you are modifying or reusing an existing Mishang Urban Construction asset, make sure you have permission to redistribute it and document the asset in `NOTICE.md`.

---

# 7. Add the Item Model

The inventory item can have a completely different texture from the block.

Create:

```text
src/main/resources/assets/red_mishanguc_roads/models/item/my_new_road_block.json
```

Example:

```json
{
  "parent": "minecraft:item/generated",
  "textures": {
    "layer0": "red_mishanguc_roads:block/my_new_road_block"
  }
}
```

Then add the corresponding texture:

```text
src/main/resources/assets/red_mishanguc_roads/textures/item/my_new_road_block.png
```

---

# 8. Add the Translation

Open:

```text
src/main/resources/assets/red_mishanguc_roads/lang/en_us.json
```

Add:

```json
"block.red_mishanguc_roads.my_new_road_block": "My New Road Block"
```

Use a clear name that describes the block.

---

# 9. Add the WorldEdit Conversion

If the block is intended to replace a Mishang Urban Construction block, add its conversion to the `/redreplace` command.

For example:

```java
runReplace(
        client,
        "mishanguc:my_original_block",
        "red_mishanguc_roads:my_new_road_block"
);
```

Make sure the original Mishang UC block actually corresponds to your new block.

Do not add unrelated replacements.

---

# 10. Test the Block

Run the game from your development environment.

Test:

* The block appears in the creative tab
* The item has the correct texture
* The block has the correct texture
* Every orientation works
* `/setblock` works for every state
* Placing the block gives the expected orientation
* The block does not have missing-texture errors
* The model does not appear mirrored incorrectly
* `/redreplace` correctly converts the original block
* The game does not produce errors in the log

For example:

```mcfunction
/setblock ~ ~ ~ red_mishanguc_roads:my_new_road_block[axis=x]
```

Test every relevant state.

---

# 11. Check Your Changes

Before committing, check which files changed:

```bash
git status
```

Make sure you have not accidentally included:

```text
.idea/
.gradle/
build/
run/
logs/
crash-reports/
```

These should normally be ignored by `.gitignore`.

---

# 12. Commit Your Changes

Add the files:

```bash
git add .
```

Create a descriptive commit:

```bash
git commit -m "Add my new road block"
```

Then push it to your fork:

```bash
git push
```

---

# 13. Create a Pull Request

Go to your fork on GitHub.

GitHub should show an option to create a pull request from your recently pushed branch.

Create the pull request against the main Red Mishang UC Road Blocks repository.

Use a descriptive title, for example:

```text
Add white diagonal road line
```

In the description, explain:

* What block you added
* Which Mishang UC block it replaces
* Which orientation type it uses
* Whether you added new textures
* Whether any existing assets were reused
* How you tested it

Example:

```markdown
## Added

Added `white_diagonal_line`.

## Replacement

Replaces:

`mishanguc:road_with_white_diagonal_line`

with:

`red_mishanguc_roads:white_diagonal_line`

## Orientation

Uses diagonal facing:

- north_east
- south_east
- south_west
- north_west

## Assets

Added a new textures:
white_diagonal_line.png

## Testing

Tested all four orientations in Minecraft 1.20.1.
```

---

# Asset Licensing

If your contribution contains assets from another project, do not assume that the project's MIT license covers them.

Add the relevant information to:

```text
NOTICE.md
```

Include:

* Original project
* Original author
* Original asset
* File path in this project
* License
* Permission, if applicable
* Whether the asset was modified

If you are unsure whether an asset can be redistributed, ask before submitting the pull request.

---

# Pull Request Checklist

Before submitting your pull request, check all of these:

* [ ] The project builds successfully
* [ ] The block is registered
* [ ] The block appears in the creative tab
* [ ] The blockstate is present
* [ ] The block model is present
* [ ] The item model is present
* [ ] Textures are present
* [ ] The language entry is present
* [ ] All orientations have been tested
* [ ] `/setblock` works
* [ ] `/redreplace` has been updated if necessary
* [ ] No generated files are included
* [ ] Third-party assets are documented in `NOTICE.md`
* [ ] The changes are limited to the intended feature

Thank you for contributing!
