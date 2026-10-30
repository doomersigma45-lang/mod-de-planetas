package com.sistemasolar.item;

import com.sistemasolar.CorpoCeleste;
import com.sistemasolar.SistemaSolarMod;
import net.minecraft.core.registries.Registries;
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

    private ItensMod() { }
}
