package com.hha.redmishangucroadblocks.client;

import net.fabricmc.fabric.api.client.command.v2.ClientCommandManager;
import net.fabricmc.fabric.api.client.command.v2.ClientCommandRegistrationCallback;
import net.minecraft.client.MinecraftClient;

public class RedReplaceCommand {

    public static void register() {
        ClientCommandRegistrationCallback.EVENT.register((dispatcher, registryAccess) -> {
            dispatcher.register(
                    ClientCommandManager.literal("redreplace")
                            .executes(context -> {

                                MinecraftClient client = MinecraftClient.getInstance();

                                runReplace(client,
                                        "mishanguc:road_with_white_thick_line",
                                        "red_mishanguc_roads:white_straight_thick_line"
                                );

                                runReplace(client,
                                        "mishanguc:road_with_white_line",
                                        "red_mishanguc_roads:white_straight_line"
                                );

                                runReplace(client,
                                        "mishanguc:road_with_white_ba_thick_line",
                                        "red_mishanguc_roads:white_bevel_angle_thick_line"
                                );

                                runReplace(client,
                                        "mishanguc:road_block",
                                        "red_terracotta"
                                );

                                runReplace(client,
                                        "mishanguc:road_with_white_ba_line",
                                        "red_mishanguc_roads:white_bevel_angle_line"
                                );

                                runReplace(client,
                                        "mishanguc:road_with_wt_n_ra_line",
                                        "red_mishanguc_roads:white_thick_and_normal_right_angle_line"
                                );

                                runReplace(client,
                                        "mishanguc:road_with_yellow_offset_out_ra_line",
                                        "red_mishanguc_roads:yellow_offset_out_right_angle_line"
                                );

                                runReplace(client,
                                        "mishanguc:road_with_yellow_offset_line",
                                        "red_mishanguc_roads:yellow_offset_straight_line"
                                );

                                return 1;
                            })
            );
        });
    }

    private static void runReplace(
            MinecraftClient client,
            String oldBlock,
            String newBlock
    ) {
        if (client.player != null) {
            client.player.networkHandler.sendChatCommand(
                    "//replace " + oldBlock + " ^" + newBlock
            );
        }
    }
}