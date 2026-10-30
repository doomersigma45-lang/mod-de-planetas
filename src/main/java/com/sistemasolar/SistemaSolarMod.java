package com.sistemasolar;

import com.sistemasolar.item.ItensMod;
import net.minecraft.world.item.CreativeModeTabs;
import net.minecraftforge.event.BuildCreativeModeTabContentsEvent;
import net.minecraftforge.eventbus.api.IEventBus;
import net.minecraftforge.fml.common.Mod;
import net.minecraftforge.fml.javafmlmod.FMLJavaModLoadingContext;

@Mod(SistemaSolarMod.MOD_ID)
public class SistemaSolarMod {
    public static final String MOD_ID = "sistemasolar";

    public SistemaSolarMod() {
        IEventBus modBus = FMLJavaModLoadingContext.get().getModEventBus();
        ItensMod.ITEMS.register(modBus);
        modBus.addListener(this::addCreativeItems);
    }

    private void addCreativeItems(BuildCreativeModeTabContentsEvent event) {
        if (event.getTabKey().equals(CreativeModeTabs.TOOLS_AND_UTILITIES)) {
            ItensMod.ITEMS.getEntries().forEach(item -> event.accept(item.get()));
        }
    }
}
