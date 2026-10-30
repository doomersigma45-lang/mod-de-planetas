package com.sistemasolar.world;

import com.sistemasolar.CorpoCeleste;
import com.sistemasolar.SistemaSolarMod;
import net.minecraft.core.registries.Registries;
import net.minecraft.world.item.BlockItem;
import net.minecraft.world.item.Item;
import net.minecraft.world.level.block.Block;
import net.minecraft.world.level.block.Blocks;
import net.minecraft.world.level.block.state.BlockBehaviour;
import net.minecraftforge.registries.DeferredRegister;
import net.minecraftforge.registries.RegistryObject;

import java.util.EnumMap;
import java.util.Map;
import java.util.function.Supplier;

public final class BlocosMod {
    public static final DeferredRegister<Block> BLOCKS = DeferredRegister.create(Registries.BLOCK, SistemaSolarMod.MOD_ID);
    public static final DeferredRegister<Item> ITEMS = DeferredRegister.create(Registries.ITEM, SistemaSolarMod.MOD_ID);
    public static final Map<CorpoCeleste, RegistryObject<Block>> SUPERFICIES = new EnumMap<>(CorpoCeleste.class);

    static {
        adicionar(CorpoCeleste.MARTE, "rocha_marciana", Blocks.RED_SANDSTONE);
        adicionar(CorpoCeleste.VENUS, "basalto_venusiano", Blocks.BASALT);
        adicionar(CorpoCeleste.MILLER, "arenito_miller", Blocks.SANDSTONE);
        adicionar(CorpoCeleste.NETUNO, "gelo_neptuniano", Blocks.PACKED_ICE);
        adicionar(CorpoCeleste.PLUTAO, "gelo_plutoniano", Blocks.BLUE_ICE);
        adicionar(CorpoCeleste.CERES, "rocha_ceresiana", Blocks.TUFF);
        adicionar(CorpoCeleste.LUA, "regolito_lunar", Blocks.ANDESITE);
        adicionar(CorpoCeleste.SATURNO, "rocha_saturiana", Blocks.ORANGE_TERRACOTTA);
        adicionar(CorpoCeleste.JUPITER, "rocha_jupiteriana", Blocks.RED_SANDSTONE);
        adicionar(CorpoCeleste.URANO, "gelo_uraniano", Blocks.BLUE_ICE);
        adicionar(CorpoCeleste.HAUMEA, "gelo_haumeano", Blocks.PACKED_ICE);
        adicionar(CorpoCeleste.SEDNA, "gelo_vermelho_sedna", Blocks.RED_TERRACOTTA);
        adicionar(CorpoCeleste.TITAN, "rocha_titana", Blocks.ORANGE_TERRACOTTA);
        adicionar(CorpoCeleste.EUROPA, "gelo_europeano", Blocks.BLUE_ICE);
        adicionar(CorpoCeleste.IO, "rocha_vulcanica_io", Blocks.BLACKSTONE);
    }

    private static void adicionar(CorpoCeleste corpo, String id, Block texturaBase) {
        Supplier<Block> bloco = () -> new Block(BlockBehaviour.Properties.copy(texturaBase));
        RegistryObject<Block> registrado = BLOCKS.register(id, bloco);
        ITEMS.register(id, () -> new BlockItem(registrado.get(), new Item.Properties()));
        SUPERFICIES.put(corpo, registrado);
    }

    private BlocosMod() { }
}
