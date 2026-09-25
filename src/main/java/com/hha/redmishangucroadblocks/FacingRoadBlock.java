package com.hha.redmishangucroadblocks;

import net.minecraft.block.Block;
import net.minecraft.block.BlockState;
import net.minecraft.item.ItemPlacementContext;
import net.minecraft.state.StateManager;
import net.minecraft.state.property.DirectionProperty;
import net.minecraft.util.math.Direction;

public class FacingRoadBlock extends Block {

    public static final DirectionProperty FACING =
            DirectionProperty.of("facing", Direction.Type.HORIZONTAL);

    public FacingRoadBlock(Settings settings) {
        super(settings);

        setDefaultState(
                getStateManager()
                        .getDefaultState()
                        .with(FACING, Direction.NORTH)
        );
    }

    @Override
    protected void appendProperties(StateManager.Builder<Block, BlockState> builder) {
        builder.add(FACING);
    }

    @Override
    public BlockState getPlacementState(ItemPlacementContext ctx) {
        return getDefaultState().with(
                FACING,
                ctx.getHorizontalPlayerFacing()
        );
    }
}