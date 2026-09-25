package com.hha.redmishangucroadblocks;

import com.hha.redmishangucroadblocks.RedMishangUcRoadBlocks;
import net.minecraft.block.AbstractBlock;
import net.minecraft.block.Block;
import net.minecraft.item.BlockItem;
import net.minecraft.item.Item;
import net.minecraft.registry.Registries;
import net.minecraft.registry.Registry;
import net.minecraft.util.Identifier;

import java.util.ArrayList;

import static com.hha.redmishangucroadblocks.RedMishangUcRoadBlocks.MOD_ID;

public class ModBlocks {

    public static ArrayList<Block> modBlocks = new ArrayList<Block>();

    public enum RoadBlockType {
        NORMAL,
        AXIS,
        FACING,
        DIAGONAL_FACING,
        AXIS_DIAGONAL_FACING
    }

    public static void registerRoadBlock(String name, RoadBlockType type) {

        Block newBlock;

        switch (type) {

            case AXIS:
                newBlock = new AxisRoadBlock(
                        AbstractBlock.Settings.create().strength(4f)
                );
                break;

            case DIAGONAL_FACING:
                newBlock = new DiagonalFacingRoadBlock(
                        AbstractBlock.Settings.create().strength(4f)
                );
                break;

            case AXIS_DIAGONAL_FACING:
                newBlock = new AxisDiagonalFacingRoadBlock(
                        AbstractBlock.Settings.create().strength(4f)
                );
                break;

            case FACING:
                newBlock = new FacingRoadBlock(
                        AbstractBlock.Settings.create().strength(4f)
                );
                break;

            default:
                newBlock = new Block(
                        AbstractBlock.Settings.create().strength(4f)
                );
                break;
        }

        Registry.register(
                Registries.BLOCK,
                Identifier.of(
                        MOD_ID,
                        name
                ),
                newBlock
        );

        Registry.register(
                Registries.ITEM,
                Identifier.of(
                        MOD_ID,
                        name
                ),
                new BlockItem(
                        newBlock,
                        new Item.Settings()
                )
        );

        modBlocks.add(newBlock);
    }

    public static void registerBlocks() {
        System.out.println("["+MOD_ID+"] Block loading 0%");

        // axis=x / axis=z
        registerRoadBlock(
                "white_straight_line",
                RoadBlockType.AXIS
        );
        registerRoadBlock(
                "white_straight_thick_line",
                RoadBlockType.AXIS
        );
        registerRoadBlock(
                "white_bevel_angle_line",
                RoadBlockType.DIAGONAL_FACING
        );
        System.out.println("["+MOD_ID+"] Block loading 25%");
        registerRoadBlock(
                "white_bevel_angle_thick_line",
                RoadBlockType.DIAGONAL_FACING
        );
        registerRoadBlock(
                "yellow_offset_out_right_angle_line",
                RoadBlockType.DIAGONAL_FACING
        );
        System.out.println("["+MOD_ID+"] Block loading 50%");
        registerRoadBlock(
                "yellow_offset_straight_line",
                RoadBlockType.FACING
        );
        registerRoadBlock(
                "white_straight_line_with_asphalt",
                RoadBlockType.FACING
        );
        registerRoadBlock(
                "white_straight_thick_line_with_asphalt",
                RoadBlockType.FACING
        );
        registerRoadBlock(
                "red_and_asphalt",
                RoadBlockType.FACING
        );
        System.out.println("["+MOD_ID+"] Block loading 75%");
        registerRoadBlock(
                "white_thick_and_normal_right_angle_line",
                RoadBlockType.AXIS_DIAGONAL_FACING
        );
        System.out.println("["+MOD_ID+"] Block loading 100%");
    }
}