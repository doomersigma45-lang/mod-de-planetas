package com.sistemasolar;

import com.sistemasolar.item.ItensMod;
import com.sistemasolar.world.BlocosMod;
import com.sistemasolar.world.EntidadesMod;
import net.minecraft.world.Difficulty;
import net.minecraft.world.entity.SpawnPlacements;
import net.minecraft.world.entity.monster.Slime;
import net.minecraft.world.item.CreativeModeTabs;
import net.minecraft.world.level.levelgen.Heightmap;
import net.minecraftforge.event.entity.EntityAttributeCreationEvent;
import net.minecraftforge.event.BuildCreativeModeTabContentsEvent;
import net.minecraftforge.eventbus.api.IEventBus;
import net.minecraftforge.fml.common.Mod;
import net.minecraftforge.fml.javafmlmod.FMLJavaModLoadingContext;
import net.minecraftforge.fml.event.lifecycle.FMLCommonSetupEvent;

@Mod(SistemaSolarMod.MOD_ID)
public class SistemaSolarMod {
    public static final String MOD_ID = "sistemasolar";

    public SistemaSolarMod() {
        IEventBus modBus = FMLJavaModLoadingContext.get().getModEventBus();
        ItensMod.ITEMS.register(modBus);
        BlocosMod.BLOCKS.register(modBus);
        BlocosMod.ITEMS.register(modBus);
        EntidadesMod.ENTITY_TYPES.register(modBus);
        modBus.addListener(this::addCreativeItems);
        modBus.addListener(this::commonSetup);
        modBus.addListener(this::registerEntityAttributes);
    }

    private void registerEntityAttributes(EntityAttributeCreationEvent event) {
        event.put(EntidadesMod.ALIEN.get(), Slime.createAttributes().build());
    }

    private void commonSetup(FMLCommonSetupEvent event) {
        event.enqueueWork(() -> SpawnPlacements.register(EntidadesMod.ALIEN.get(),
                SpawnPlacements.Type.ON_GROUND, Heightmap.Types.MOTION_BLOCKING_NO_LEAVES,
                (type, level, reason, pos, random) -> level.getDifficulty() != Difficulty.PEACEFUL
                        && level.getBlockState(pos).isAir()));
    }

    private void addCreativeItems(BuildCreativeModeTabContentsEvent event) {
        if (event.getTabKey().equals(CreativeModeTabs.TOOLS_AND_UTILITIES)) {
            ItensMod.ITEMS.getEntries().forEach(item -> event.accept(item.get()));
        }
        if (event.getTabKey().equals(CreativeModeTabs.BUILDING_BLOCKS)) {
            BlocosMod.ITEMS.getEntries().forEach(item -> event.accept(item.get()));
        }
    }
}
