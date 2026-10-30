package com.sistemasolar;

import net.minecraft.core.registries.Registries;
import net.minecraft.resources.ResourceKey;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.world.level.Level;

import java.util.Arrays;
import java.util.Optional;

public enum CorpoCeleste {
    MARTE("marte", "Marte"),
    VENUS("venus", "Vênus"),
    MILLER("miller", "Planeta Miller"),
    NETUNO("netuno", "Netuno"),
    PLUTAO("plutao", "Plutão"),
    CERES("ceres", "Ceres"),
    LUA("lua", "Lua"),
    SATURNO("saturno", "Saturno"),
    JUPITER("jupiter", "Júpiter"),
    URANO("urano", "Urano"),
    HAUMEA("haumea", "Haumea"),
    SEDNA("sedna", "Sedna"),
    TITAN("titan", "Titã"),
    EUROPA("europa", "Europa"),
    IO("io", "Io"),
    TERRA("overworld", "Terra", "minecraft");

    private final String id;
    private final String nome;
    private final String namespace;

    CorpoCeleste(String id, String nome) {
        this(id, nome, SistemaSolarMod.MOD_ID);
    }

    CorpoCeleste(String id, String nome, String namespace) {
        this.id = id;
        this.nome = nome;
        this.namespace = namespace;
    }

    public String id() {
        return id;
    }

    public String nome() {
        return nome;
    }

    public ResourceKey<Level> dimensao() {
        return ResourceKey.create(Registries.DIMENSION, new ResourceLocation(namespace, id));
    }

    public boolean precisaOxigenio() {
        return this != TERRA;
    }

    public static Optional<CorpoCeleste> porDimensao(ResourceKey<Level> key) {
        return Arrays.stream(values()).filter(corpo -> corpo.dimensao().equals(key)).findFirst();
    }
}
