package com.hha.redmishangucroadblocks;

import net.minecraft.block.Block;
import net.minecraft.block.BlockState;
import net.minecraft.item.ItemPlacementContext;
import net.minecraft.state.StateManager;
import net.minecraft.state.property.EnumProperty;

public class DiagonalFacingRoadBlock extends Block {

    public static final EnumProperty<DiagonalDirection> FACING =
            EnumProperty.of("facing", DiagonalDirection.class);

    public DiagonalFacingRoadBlock(Settings settings) {
        super(settings);

        setDefaultState(
                getStateManager()
                        .getDefaultState()
                        .with(FACING, DiagonalDirection.NORTH_EAST)
        );
    }

    @Override
    protected void appendProperties(StateManager.Builder<Block, BlockState> builder) {
        builder.add(FACING);
    }

    @Override
    public BlockState getPlacementState(ItemPlacementContext ctx) {
        float yaw = ctx.getPlayerYaw();

        yaw = (yaw % 360 + 360) % 360;

        DiagonalDirection direction;

        if (yaw >= 0 && yaw < 90) {
            direction = DiagonalDirection.SOUTH_WEST;
        } else if (yaw >= 90 && yaw < 180) {
            direction = DiagonalDirection.NORTH_WEST;
        } else if (yaw >= 180 && yaw < 270) {
            direction = DiagonalDirection.NORTH_EAST;
        } else {
            direction = DiagonalDirection.SOUTH_EAST;
        }

        return getDefaultState().with(FACING, direction);
    }
}