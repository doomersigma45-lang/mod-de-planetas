package com.sistemasolar.item;

import net.minecraft.sounds.SoundEvent;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.world.item.ArmorItem;
import net.minecraft.world.item.ArmorMaterial;
import net.minecraft.world.item.Items;
import net.minecraft.world.item.crafting.Ingredient;

public final class MaterialTrajeEspacial implements ArmorMaterial {
    public static final MaterialTrajeEspacial INSTANCE = new MaterialTrajeEspacial();

    private MaterialTrajeEspacial() { }

    @Override
    public int getDurabilityForType(ArmorItem.Type type) {
        return switch (type) {
            case HELMET -> 275;
            case CHESTPLATE -> 400;
            case LEGGINGS -> 375;
            case BOOTS -> 325;
        };
    }

    @Override
    public int getDefenseForType(ArmorItem.Type type) {
        return switch (type) {
            case HELMET -> 2;
            case CHESTPLATE -> 6;
            case LEGGINGS -> 5;
            case BOOTS -> 2;
        };
    }

    @Override public int getEnchantmentValue() { return 18; }
    @Override public SoundEvent getEquipSound() { return SoundEvents.ARMOR_EQUIP_IRON; }
    @Override public Ingredient getRepairIngredient() { return Ingredient.of(Items.IRON_INGOT); }
    @Override public String getName() { return "leather"; }
    @Override public float getToughness() { return 2.0F; }
    @Override public float getKnockbackResistance() { return 0.05F; }
}
