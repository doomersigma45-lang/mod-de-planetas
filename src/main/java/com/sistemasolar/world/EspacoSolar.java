package com.sistemasolar.world;

import com.sistemasolar.SistemaSolarMod;
import net.minecraft.core.registries.Registries;
import net.minecraft.resources.ResourceKey;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.world.level.Level;

public final class EspacoSolar {
    public static final ResourceKey<Level> DIMENSAO = ResourceKey.create(Registries.DIMENSION,
            new ResourceLocation(SistemaSolarMod.MOD_ID, "espaco"));

    private EspacoSolar() { }
}
