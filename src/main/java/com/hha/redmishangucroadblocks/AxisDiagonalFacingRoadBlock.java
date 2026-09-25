package com.hha.redmishangucroadblocks;

import net.minecraft.block.Block;
import net.minecraft.block.BlockState;
import net.minecraft.item.ItemPlacementContext;
import net.minecraft.state.StateManager;
import net.minecraft.state.property.EnumProperty;
import net.minecraft.util.math.Direction;

public class AxisDiagonalFacingRoadBlock extends Block {

    public static final EnumProperty<Direction.Axis> AXIS =
            EnumProperty.of(
                    "axis",
                    Direction.Axis.class,
                    Direction.Axis.X,
                    Direction.Axis.Z
            );

    public static final EnumProperty<DiagonalDirection> FACING =
            EnumProperty.of(
                    "facing",
                    DiagonalDirection.class
            );

    public AxisDiagonalFacingRoadBlock(Settings settings) {
        super(settings);

        setDefaultState(
                getStateManager()
                        .getDefaultState()
                        .with(AXIS, Direction.Axis.Z)
                        .with(FACING, DiagonalDirection.NORTH_EAST)
        );
    }

    @Override
    public BlockState getPlacementState(ItemPlacementContext ctx) {
        float yaw = ctx.getPlayerYaw();
        yaw = (yaw % 360 + 360) % 360;

        Direction.Axis axis;

        if (ctx.getHorizontalPlayerFacing().getAxis() == Direction.Axis.X) {
            axis = Direction.Axis.X;
        } else {
            axis = Direction.Axis.Z;
        }

        DiagonalDirection diagonal;

        if (yaw >= 0 && yaw < 90) {
            diagonal = DiagonalDirection.SOUTH_WEST;
        } else if (yaw >= 90 && yaw < 180) {
            diagonal = DiagonalDirection.NORTH_WEST;
        } else if (yaw >= 180 && yaw < 270) {
            diagonal = DiagonalDirection.NORTH_EAST;
        } else {
            diagonal = DiagonalDirection.SOUTH_EAST;
        }

        return getDefaultState()
                .with(AXIS, axis)
                .with(FACING, diagonal);
    }

    @Override
    protected void appendProperties(StateManager.Builder<Block, BlockState> builder) {
        builder.add(AXIS, FACING);
    }
}