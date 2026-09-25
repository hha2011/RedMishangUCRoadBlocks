# Red Mishang UC Road Blocks

[![Minecraft](https://img.shields.io/badge/Minecraft-1.20.1-62B47A?logo=minecraft&logoColor=white)](https://www.minecraft.net/)
[![Fabric](https://img.shields.io/badge/Fabric-1.20.1-DBD0B4?logo=fabric&logoColor=white)](https://fabricmc.net/)
[![Fabric API](https://img.shields.io/badge/Fabric%20API-Required-DBD0B4?logo=fabric&logoColor=white)](https://modrinth.com/mod/fabric-api)
[![Fabric Loader](https://img.shields.io/badge/Fabric%20Loader-Required-DBD0B4?logo=fabric&logoColor=white)](https://fabricmc.net/)
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE.md)

Red Mishang UC Road Blocks is a Minecraft Fabric 1.20.1 mod that provides
red-terracotta variants of road blocks from Mishang Urban Construction.

The project is intended to make it easier to build roads using red variants
of Mishang UC's road markings and related blocks.

## Features

* Red-terracotta road blocks
* White road markings
* Different road-line orientations
* Axis-based blocks using `axis=x` and `axis=z`
* Four-direction blocks using `facing=north`, `east`, `south`, and `west`
* Diagonal blocks using:

    * `facing=north_east`
    * `facing=south_east`
    * `facing=south_west`
    * `facing=north_west`
* Combined axis and diagonal-direction blocks
* A command for converting existing Mishang UC road blocks to their red variants

## Requirements

* Minecraft 1.20.1
* Fabric Loader
* Fabric API
* Mishang Urban Construction

## Red Road Conversion

The mod includes the `/redreplace` command, which performs a series of
WorldEdit replacements for supported Mishang UC road blocks.

The command is intended to make converting an existing road layout to the
corresponding red variants quicker.

WorldEdit is required for the replacement commands.

## Block Orientation

Some blocks use the `axis` property:

```text
axis=x
axis=z
```

Other blocks use a four-way `facing` property:

```text
facing=north
facing=east
facing=south
facing=west
```

Diagonal road blocks use:

```text
facing=north_east
facing=south_east
facing=south_west
facing=north_west
```

For example:

```mcfunction
/setblock ~ ~ ~ red_mishanguc_roads:white_straight_line[axis=x]
```

or:

```mcfunction
/setblock ~ ~ ~ red_mishanguc_roads:white_diagonal_line[facing=north_east]
```

## Resource Packs

The project is designed with Minecraft's resource-pack system in mind.
Textures and models are kept as normal Minecraft resource assets so that
resource packs can override them.

At present, resource packs cannot directly register new blocks. Adding
completely new block types requires support from the mod itself.

## Building

Clone the repository and run the Gradle build:

```bash
./gradlew build
```

On Windows:

```bat
gradlew.bat build
```

The resulting JAR will be placed in:

```text
build/libs/
```

## License

The source code of Red Mishang UC Road Blocks is licensed under the MIT
License. See `LICENSE.md`.

Assets originating from Mishang Urban Construction are separate from the
project's own source code and are subject to their original licensing terms
and/or permissions from their copyright holder.

## Credits

This project is based on and intended to complement:

**Mishang Urban Construction**

The original Mishang UC project and its assets remain the property of their
respective authors and contributors.

Please refer to the original project for its licensing terms and attribution
requirements.

## Disclaimer

Red Mishang UC Road Blocks is an independent project and is not affiliated
with or endorsed by the creators of Mishang Urban Construction unless
explicitly stated otherwise.
