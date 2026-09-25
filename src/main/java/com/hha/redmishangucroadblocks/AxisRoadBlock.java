package com.hha.redmishangucroadblocks;

import net.minecraft.block.Block;
import net.minecraft.block.BlockState;
import net.minecraft.item.ItemPlacementContext;
import net.minecraft.state.StateManager;
import net.minecraft.state.property.EnumProperty;
import net.minecraft.util.math.Direction;

public class AxisRoadBlock extends Block {

    public static final EnumProperty<Direction.Axis> AXIS =
            EnumProperty.of(
                    "axis",
                    Direction.Axis.class,
                    Direction.Axis.X,
                    Direction.Axis.Z
            );

    public AxisRoadBlock(Settings settings) {
        super(settings);

        setDefaultState(
                getStateManager()
                        .getDefaultState()
                        .with(AXIS, Direction.Axis.Z)
        );
    }

    @Override
    protected void appendProperties(StateManager.Builder<Block, BlockState> builder) {
        builder.add(AXIS);
    }

    @Override
    public BlockState getPlacementState(ItemPlacementContext ctx) {
        Direction direction = ctx.getHorizontalPlayerFacing();

        return getDefaultState().with(
                AXIS,
                direction.getAxis()
        );
    }
}