package com.sistemasolar.world;

import net.minecraft.world.entity.EntityType;
import net.minecraft.world.entity.monster.Slime;
import net.minecraft.world.level.Level;

public class AlienEntity extends Slime {
    public AlienEntity(EntityType<? extends Slime> type, Level level) {
        super(type, level);
    }
}
