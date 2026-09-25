package com.hha.redmishangucroadblocks.client;

import com.hha.redmishangucroadblocks.client.RedReplaceCommand;
import net.fabricmc.api.ClientModInitializer;

public class RedMishangUcRoadBlocksClient implements ClientModInitializer {

    @Override
    public void onInitializeClient() {
        RedReplaceCommand.register();
    }
}
