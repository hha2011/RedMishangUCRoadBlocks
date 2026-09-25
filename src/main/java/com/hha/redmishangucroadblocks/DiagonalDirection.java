package com.hha.redmishangucroadblocks;

import net.minecraft.util.StringIdentifiable;

public enum DiagonalDirection implements StringIdentifiable {
    NORTH_EAST("north_east"),
    SOUTH_EAST("south_east"),
    SOUTH_WEST("south_west"),
    NORTH_WEST("north_west");

    private final String name;

    DiagonalDirection(String name) {
        this.name = name;
    }

    @Override
    public String asString() {
        return name;
    }
}