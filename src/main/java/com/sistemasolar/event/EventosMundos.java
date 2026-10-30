package com.sistemasolar.event;

import com.sistemasolar.CorpoCeleste;
import com.sistemasolar.SistemaSolarMod;
import com.sistemasolar.world.EspacoSolar;
import com.sistemasolar.world.BlocosMod;
import net.minecraft.core.BlockPos;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.util.RandomSource;
import net.minecraft.world.level.ChunkPos;
import net.minecraft.world.level.block.Blocks;
import net.minecraft.world.level.block.state.BlockState;
import net.minecraft.world.level.levelgen.Heightmap;
import net.minecraftforge.event.level.ChunkEvent;
import net.minecraftforge.eventbus.api.SubscribeEvent;
import net.minecraftforge.fml.common.Mod;

@Mod.EventBusSubscriber(modid = SistemaSolarMod.MOD_ID, bus = Mod.EventBusSubscriber.Bus.FORGE)
public final class EventosMundos {
    private EventosMundos() { }

    @SubscribeEvent
    public static void gerarEstruturas(ChunkEvent.Load event) {
        if (!event.isNewChunk() || !(event.getLevel() instanceof ServerLevel level)) return;
        ChunkPos chunk = event.getChunk().getPos();
        int chunkX = chunk.x;
        int chunkZ = chunk.z;
        level.getServer().execute(() -> {
            if (!level.hasChunk(chunkX, chunkZ)) return;
            ChunkPos loadedChunk = new ChunkPos(chunkX, chunkZ);
            if (level.dimension().equals(EspacoSolar.DIMENSAO)) {
                gerarSistemaVisivel(level, loadedChunk);
                gerarAsteroide(level, loadedChunk);
                return;
            }
            CorpoCeleste corpo = CorpoCeleste.porDimensao(level.dimension()).orElse(null);
            if (corpo == CorpoCeleste.EUROPA || corpo == CorpoCeleste.PLUTAO) {
                gerarOceanoSobGelo(level, loadedChunk, corpo);
            }
            if (corpo == CorpoCeleste.PLUTAO) gerarCidadePlutoniana(level, loadedChunk);
            if (corpo == CorpoCeleste.IO) gerarVulcao(level, loadedChunk);
        });
    }

    private static RandomSource aleatorio(ServerLevel level, ChunkPos pos, long salt) {
        return RandomSource.create(level.getSeed() ^ ((long) pos.x * 341873128712L)
                ^ ((long) pos.z * 132897987541L) ^ salt);
    }

    private static void gerarOceanoSobGelo(ServerLevel level, ChunkPos chunk, CorpoCeleste corpo) {
        RandomSource random = aleatorio(level, chunk, corpo == CorpoCeleste.EUROPA ? 0x4555524F5041L : 0x504C55544F4FL);
        if (random.nextInt(2) != 0) return;
        int x0 = chunk.getMinBlockX() + 2;
        int z0 = chunk.getMinBlockZ() + 2;
        int menorSuperficie = 320;
        for (int x = x0; x < x0 + 12; x++) {
            for (int z = z0; z < z0 + 12; z++) {
                menorSuperficie = Math.min(menorSuperficie,
                        level.getHeight(Heightmap.Types.WORLD_SURFACE, x, z));
            }
        }
        int teto = menorSuperficie - 2;
        if (teto < 54 || teto > 220) return;
        int fundo = teto - 10;
        BlockState gelo = BlocosMod.SUPERFICIES.get(corpo).get().defaultBlockState();
        BlockState rocha = corpo == CorpoCeleste.EUROPA ? Blocks.DEEPSLATE.defaultBlockState()
                : Blocks.CALCITE.defaultBlockState();
        for (int x = x0; x < x0 + 12; x++) {
            for (int z = z0; z < z0 + 12; z++) {
                level.setBlock(new BlockPos(x, fundo, z), rocha, 2);
                for (int y = fundo + 1; y < teto; y++) {
                    level.setBlock(new BlockPos(x, y, z), Blocks.WATER.defaultBlockState(), 2);
                }
                level.setBlock(new BlockPos(x, teto, z), gelo, 2);
            }
        }
    }

    private static void gerarCidadePlutoniana(ServerLevel level, ChunkPos chunk) {
        RandomSource random = aleatorio(level, chunk, 0x504C55544F4EL);
        if (random.nextInt(5) != 0) return;
        int x0 = chunk.getMinBlockX() + 4 + random.nextInt(8);
        int z0 = chunk.getMinBlockZ() + 4 + random.nextInt(8);
        int ground = level.getHeight(Heightmap.Types.WORLD_SURFACE, x0, z0) - 1;
        if (ground < 48 || ground > 150) return;
        int floors = 5 + random.nextInt(15);
        int width = 4 + random.nextInt(3);
        BlockState frame = random.nextBoolean() ? Blocks.QUARTZ_BLOCK.defaultBlockState() : Blocks.IRON_BLOCK.defaultBlockState();
        BlockState glass = Blocks.CYAN_STAINED_GLASS.defaultBlockState();
        for (int y = 0; y < floors; y++) {
            for (int dx = -width; dx <= width; dx++) {
                for (int dz = -width; dz <= width; dz++) {
                    boolean wall = Math.abs(dx) == width || Math.abs(dz) == width;
                    BlockState state = wall ? ((y % 4 == 0 || dx == -width || dx == width) ? frame : glass)
                            : Blocks.AIR.defaultBlockState();
                    level.setBlock(new BlockPos(x0 + dx, ground + 1 + y, z0 + dz), state, 2);
                }
            }
            if (y % 4 == 0) {
                level.setBlock(new BlockPos(x0, ground + 1 + y, z0), Blocks.SEA_LANTERN.defaultBlockState(), 2);
            }
        }
        for (int dx = -width; dx <= width; dx++) {
            for (int dz = -width; dz <= width; dz++) {
                level.setBlock(new BlockPos(x0 + dx, ground, z0 + dz), Blocks.SMOOTH_QUARTZ.defaultBlockState(), 2);
            }
        }
        for (int y = 0; y < Math.min(4, floors); y++) {
            level.setBlock(new BlockPos(x0, ground + 1 + y, z0 - width), Blocks.AIR.defaultBlockState(), 2);
        }
    }

    private static void gerarVulcao(ServerLevel level, ChunkPos chunk) {
        RandomSource random = aleatorio(level, chunk, 0x494F564F4C43414EL);
        if (random.nextInt(22) != 0) return;
        int x0 = chunk.getMinBlockX() + 8;
        int z0 = chunk.getMinBlockZ() + 8;
        int ground = level.getHeight(Heightmap.Types.WORLD_SURFACE, x0, z0) - 1;
        if (ground < 35 || ground > 130) return;
        int radius = 6 + random.nextInt(3);
        int height = 9 + random.nextInt(8);
        for (int y = 0; y <= height; y++) {
            int ring = Math.max(1, radius - (y * radius / (height + 2)));
            for (int dx = -radius; dx <= radius; dx++) {
                for (int dz = -radius; dz <= radius; dz++) {
                    int distance = dx * dx + dz * dz;
                    if (distance > ring * ring || distance < Math.max(0, ring - 2) * Math.max(0, ring - 2)) continue;
                    level.setBlock(new BlockPos(x0 + dx, ground + y, z0 + dz),
                            (y % 3 == 0 ? Blocks.BLACKSTONE : Blocks.BASALT).defaultBlockState(), 2);
                }
            }
        }
        level.setBlock(new BlockPos(x0, ground + height - 1, z0), Blocks.LAVA.defaultBlockState(), 2);
        level.setBlock(new BlockPos(x0 + 1, ground + height - 1, z0), Blocks.MAGMA_BLOCK.defaultBlockState(), 2);
        level.setBlock(new BlockPos(x0 - 1, ground + height - 1, z0), Blocks.MAGMA_BLOCK.defaultBlockState(), 2);
    }

    private static void gerarSistemaVisivel(ServerLevel level, ChunkPos chunk) {
        // Corpos em escala reduzida para ficarem visíveis da área inicial do espaço.
        baseOrbitalSeIntersecta(level, chunk);
        esferaSeIntersecta(level, chunk, 0, 94, -112, 15, Blocks.ORANGE_TERRACOTTA.defaultBlockState());
        esferaSeIntersecta(level, chunk, 136, 102, 44, 18, Blocks.ORANGE_CONCRETE.defaultBlockState());
        esferaSeIntersecta(level, chunk, -162, 88, 50, 22, Blocks.LIGHT_BLUE_CONCRETE.defaultBlockState());
        esferaSeIntersecta(level, chunk, 260, 125, -90, 18, Blocks.YELLOW_TERRACOTTA.defaultBlockState());
        esferaSeIntersecta(level, chunk, -275, 92, -120, 16, Blocks.PACKED_ICE.defaultBlockState());
        anelPlanetarioSeIntersecta(level, chunk, -275, 92, -120, 21, 32);
        esferaSeIntersecta(level, chunk, 88, 104, 280, 11, Blocks.BLUE_ICE.defaultBlockState());
        esferaSeIntersecta(level, chunk, -96, 76, 294, 10, Blocks.PURPLE_TERRACOTTA.defaultBlockState());
        naveAbandonadaSeIntersecta(level, chunk);
    }

    private static void anelPlanetarioSeIntersecta(ServerLevel level, ChunkPos chunk, int cx, int cy, int cz,
                                                    int innerRadius, int outerRadius) {
        int minX = Math.max(chunk.getMinBlockX(), cx - outerRadius);
        int maxX = Math.min(chunk.getMaxBlockX(), cx + outerRadius);
        int minZ = Math.max(chunk.getMinBlockZ(), cz - outerRadius);
        int maxZ = Math.min(chunk.getMaxBlockZ(), cz + outerRadius);
        if (minX > maxX || minZ > maxZ) return;
        for (int x = minX; x <= maxX; x++) for (int z = minZ; z <= maxZ; z++) {
            int dx = x - cx, dz = z - cz;
            int distancia = dx * dx + dz * dz;
            if (distancia >= innerRadius * innerRadius && distancia <= outerRadius * outerRadius) {
                BlockState ring = (Math.abs(dx + dz) % 5 == 0) ? Blocks.YELLOW_CONCRETE.defaultBlockState()
                        : Blocks.SANDSTONE.defaultBlockState();
                level.setBlock(new BlockPos(x, cy, z), ring, 2);
            }
        }
    }

    private static void baseOrbitalSeIntersecta(ServerLevel level, ChunkPos chunk) {
        int minX = Math.max(chunk.getMinBlockX(), -8), maxX = Math.min(chunk.getMaxBlockX(), 8);
        int minZ = Math.max(chunk.getMinBlockZ(), -8), maxZ = Math.min(chunk.getMaxBlockZ(), 8);
        if (minX > maxX || minZ > maxZ) return;
        for (int x = minX; x <= maxX; x++) for (int z = minZ; z <= maxZ; z++) {
            boolean borda = Math.abs(x) == 8 || Math.abs(z) == 8;
            BlockState state = borda ? Blocks.LIGHT_BLUE_CONCRETE.defaultBlockState()
                    : Blocks.IRON_BLOCK.defaultBlockState();
            level.setBlock(new BlockPos(x, 88, z), state, 2);
        }
        level.setBlock(new BlockPos(0, 89, 0), Blocks.SEA_LANTERN.defaultBlockState(), 2);
    }

    private static void esferaSeIntersecta(ServerLevel level, ChunkPos chunk, int cx, int cy, int cz, int radius, BlockState state) {
        int minX = Math.max(chunk.getMinBlockX(), cx - radius);
        int maxX = Math.min(chunk.getMaxBlockX(), cx + radius);
        int minZ = Math.max(chunk.getMinBlockZ(), cz - radius);
        int maxZ = Math.min(chunk.getMaxBlockZ(), cz + radius);
        if (minX > maxX || minZ > maxZ) return;
        int r2 = radius * radius;
        for (int x = minX; x <= maxX; x++) for (int z = minZ; z <= maxZ; z++) {
            int dx = x - cx, dz = z - cz;
            int remain = r2 - dx * dx - dz * dz;
            if (remain < 0) continue;
            int dy = (int) Math.sqrt(remain);
            for (int y = cy - dy; y <= cy + dy; y++) {
                if (dx * dx + dz * dz + (y - cy) * (y - cy) <= r2) {
                    level.setBlock(new BlockPos(x, y, z), state, 2);
                }
            }
        }
    }

    private static void naveAbandonadaSeIntersecta(ServerLevel level, ChunkPos chunk) {
        int minX = Math.max(chunk.getMinBlockX(), 32), maxX = Math.min(chunk.getMaxBlockX(), 58);
        int minZ = Math.max(chunk.getMinBlockZ(), 18), maxZ = Math.min(chunk.getMaxBlockZ(), 39);
        if (minX > maxX || minZ > maxZ) return;
        for (int x = minX; x <= maxX; x++) for (int z = minZ; z <= maxZ; z++) {
            for (int y = 86; y <= 96; y++) {
                boolean shell = x == 32 || x == 58 || z == 18 || z == 39 || y == 86 || y == 96;
                BlockState state = shell ? Blocks.IRON_BLOCK.defaultBlockState() : Blocks.AIR.defaultBlockState();
                if (shell && (x == 32 || x == 58) && y > 88 && y < 95) state = Blocks.LIGHT_BLUE_STAINED_GLASS.defaultBlockState();
                level.setBlock(new BlockPos(x, y, z), state, 2);
            }
        }
        for (int x = minX; x <= maxX; x++) for (int z = minZ; z <= maxZ; z++) {
            if (x > 32 && x < 58 && z > 18 && z < 39) {
                level.setBlock(new BlockPos(x, 87, z), Blocks.SMOOTH_STONE.defaultBlockState(), 2);
            }
        }
        level.setBlock(new BlockPos(45, 88, 18), Blocks.AIR.defaultBlockState(), 2);
        level.setBlock(new BlockPos(45, 89, 18), Blocks.AIR.defaultBlockState(), 2);
        level.setBlock(new BlockPos(45, 90, 18), Blocks.AIR.defaultBlockState(), 2);
        level.setBlock(new BlockPos(39, 92, 28), Blocks.SEA_LANTERN.defaultBlockState(), 2);
        level.setBlock(new BlockPos(51, 92, 28), Blocks.SEA_LANTERN.defaultBlockState(), 2);
    }

    private static void gerarAsteroide(ServerLevel level, ChunkPos chunk) {
        RandomSource random = aleatorio(level, chunk, 0x41535445524F4944L);
        if (random.nextInt(10) != 0) return;
        int cx = chunk.getMinBlockX() + 4 + random.nextInt(8);
        int cz = chunk.getMinBlockZ() + 4 + random.nextInt(8);
        int cy = 78 + random.nextInt(42);
        int radius = 2 + random.nextInt(4);
        BlockState[] palette = {Blocks.ANDESITE.defaultBlockState(), Blocks.TUFF.defaultBlockState(), Blocks.IRON_ORE.defaultBlockState()};
        for (int dx = -radius; dx <= radius; dx++) for (int dy = -radius; dy <= radius; dy++) for (int dz = -radius; dz <= radius; dz++) {
            if (dx * dx + dy * dy + dz * dz <= radius * radius && cx + dx >= chunk.getMinBlockX()
                    && cx + dx <= chunk.getMaxBlockX() && cz + dz >= chunk.getMinBlockZ() && cz + dz <= chunk.getMaxBlockZ()) {
                BlockState state = random.nextInt(18) == 0 ? palette[2] : palette[random.nextInt(2)];
                level.setBlock(new BlockPos(cx + dx, cy + dy, cz + dz), state, 2);
            }
        }
    }
}
