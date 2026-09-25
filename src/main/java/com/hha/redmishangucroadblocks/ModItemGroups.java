package com.hha.redmishangucroadblocks;

import net.fabricmc.fabric.api.itemgroup.v1.FabricItemGroup;
import net.minecraft.item.ItemGroup;
import net.minecraft.item.ItemStack;
import net.minecraft.registry.Registries;
import net.minecraft.registry.Registry;
import net.minecraft.text.Text;
import net.minecraft.util.Identifier;

public class ModItemGroups {

    public static final ItemGroup RED_MISHANGUC_ROADS = Registry.register(
            Registries.ITEM_GROUP,
            Identifier.of(
                    RedMishangUcRoadBlocks.MOD_ID,
                    "red_mishanguc_roads"
            ),
            FabricItemGroup.builder()
                    .displayName(Text.translatable(
                            "itemGroup.red_mishanguc_roads"
                    ))
                    .icon(() -> new ItemStack(ModBlocks.modBlocks.get(0)))
                    .entries((context, entries) -> {
                        for (var block : ModBlocks.modBlocks) {
                            entries.add(block);
                        }
                    })
                    .build()
    );

    public static void registerItemGroups() {
        // This method exists so the group gets initialized.
    }
}