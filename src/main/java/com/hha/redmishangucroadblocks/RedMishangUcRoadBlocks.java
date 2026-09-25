package com.hha.redmishangucroadblocks;

import net.fabricmc.api.ModInitializer;

public class RedMishangUcRoadBlocks implements ModInitializer {
    public final static String MOD_ID = "red_mishanguc_roads";

    @Override
    public void onInitialize() {
        System.out.println("hello from "+MOD_ID+" loading blocks");
        ModBlocks.registerBlocks();
        ModItemGroups.registerItemGroups();
    }
}
