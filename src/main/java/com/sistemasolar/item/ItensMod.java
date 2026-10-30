package com.sistemasolar.item;

import com.sistemasolar.CorpoCeleste;
import com.sistemasolar.SistemaSolarMod;
import net.minecraft.core.registries.Registries;
import net.minecraft.world.item.ArmorItem;
import net.minecraft.world.item.Item;
import net.minecraftforge.registries.DeferredRegister;
import net.minecraftforge.registries.RegistryObject;

import java.util.EnumMap;
import java.util.Map;

public final class ItensMod {
    public static final DeferredRegister<Item> ITEMS = DeferredRegister.create(Registries.ITEM, SistemaSolarMod.MOD_ID);
    public static final Map<CorpoCeleste, RegistryObject<Item>> LOCALIZADORES = new EnumMap<>(CorpoCeleste.class);

    static {
        for (CorpoCeleste corpo : CorpoCeleste.values()) {
            LOCALIZADORES.put(corpo, ITEMS.register(corpo.id() + "_locator",
                    () -> new LocalizadorItem(corpo)));
        }
    }

    public static final RegistryObject<Item> ROCKET = ITEMS.register("foguete_interplanetario",
            () -> new FogueteItem());
    public static final RegistryObject<Item> OXYGEN_CANISTER = ITEMS.register("cilindro_oxigenio",
            () -> new CilindroOxigenioItem());
    public static final RegistryObject<Item> SPACE_HELMET = ITEMS.register("capacete_espacial",
            () -> new ArmorItem(MaterialTrajeEspacial.INSTANCE, ArmorItem.Type.HELMET, new Item.Properties()));
    public static final RegistryObject<Item> SPACE_CHESTPLATE = ITEMS.register("peitoral_espacial",
            () -> new ArmorItem(MaterialTrajeEspacial.INSTANCE, ArmorItem.Type.CHESTPLATE, new Item.Properties()));
    public static final RegistryObject<Item> SPACE_LEGGINGS = ITEMS.register("calcas_espaciais",
            () -> new ArmorItem(MaterialTrajeEspacial.INSTANCE, ArmorItem.Type.LEGGINGS, new Item.Properties()));
    public static final RegistryObject<Item> SPACE_BOOTS = ITEMS.register("botas_espaciais",
            () -> new ArmorItem(MaterialTrajeEspacial.INSTANCE, ArmorItem.Type.BOOTS, new Item.Properties()));

    private ItensMod() { }
}
