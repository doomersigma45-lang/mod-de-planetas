package com.sistemasolar.world;

import com.sistemasolar.SistemaSolarMod;
import net.minecraft.core.registries.Registries;
import net.minecraft.world.entity.EntityType;
import net.minecraft.world.entity.MobCategory;
import net.minecraftforge.registries.DeferredRegister;
import net.minecraftforge.registries.RegistryObject;

public final class EntidadesMod {
    public static final DeferredRegister<EntityType<?>> ENTITY_TYPES =
            DeferredRegister.create(Registries.ENTITY_TYPE, SistemaSolarMod.MOD_ID);
    public static final RegistryObject<EntityType<AlienEntity>> ALIEN = ENTITY_TYPES.register("alien",
            () -> EntityType.Builder.<AlienEntity>of(AlienEntity::new, MobCategory.MONSTER)
                    .sized(0.9F, 1.6F).clientTrackingRange(8).build("sistemasolar:alien"));

    private EntidadesMod() { }
}
