package com.sistemasolar.item;

import com.sistemasolar.CorpoCeleste;
import com.sistemasolar.event.EventosAtmosfera;
import com.sistemasolar.world.EspacoSolar;
import net.minecraft.ChatFormatting;
import net.minecraft.network.chat.Component;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.world.InteractionHand;
import net.minecraft.world.InteractionResultHolder;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.TooltipFlag;
import net.minecraft.world.level.Level;
import net.minecraft.world.level.block.Blocks;
import net.minecraft.world.level.block.state.BlockState;
import net.minecraft.world.level.levelgen.Heightmap;

import java.util.List;

public class FogueteItem extends Item {
    private static final String DESTINO_TAG = "Destino";

    public FogueteItem() {
        super(new Item.Properties().stacksTo(1));
    }

    @Override
    public InteractionResultHolder<ItemStack> use(Level level, Player player, InteractionHand hand) {
        ItemStack stack = player.getItemInHand(hand);
        if (player.isCrouching()) {
            if (!level.isClientSide) {
                CorpoCeleste atual = destino(stack);
                CorpoCeleste[] corpos = CorpoCeleste.values();
                CorpoCeleste proximo = corpos[(atual.ordinal() + 1) % corpos.length];
                stack.getOrCreateTag().putString(DESTINO_TAG, proximo.name());
                player.displayClientMessage(Component.literal("Destino do foguete: " + proximo.nome())
                        .withStyle(ChatFormatting.AQUA), true);
            }
            return InteractionResultHolder.sidedSuccess(stack, level.isClientSide);
        }

        if (!level.isClientSide && player instanceof ServerPlayer serverPlayer) {
            if (!EventosAtmosfera.temOxigenio(serverPlayer)) {
                serverPlayer.sendSystemMessage(Component.literal("Vista o traje espacial completo e recarregue o oxigênio antes do voo.")
                        .withStyle(ChatFormatting.RED));
                return InteractionResultHolder.fail(stack);
            }

            boolean jaEstaNoEspaco = serverPlayer.level().dimension().equals(EspacoSolar.DIMENSAO);
            ServerLevel target = serverPlayer.server.getLevel(jaEstaNoEspaco
                    ? destino(stack).dimensao() : EspacoSolar.DIMENSAO);
            if (target == null) {
                String nome = jaEstaNoEspaco ? destino(stack).nome() : "espaço";
                serverPlayer.sendSystemMessage(Component.literal("Destino indisponível: " + nome)
                        .withStyle(ChatFormatting.RED));
                return InteractionResultHolder.fail(stack);
            }

            if (jaEstaNoEspaco) {
                CorpoCeleste corpo = destino(stack);
                serverPlayer.teleportTo(target, 0.5, landingY(target, corpo), 0.5,
                        java.util.Set.of(), serverPlayer.getYRot(), serverPlayer.getXRot());
                serverPlayer.sendSystemMessage(Component.literal("Pouso concluído em " + corpo.nome() + ".")
                        .withStyle(ChatFormatting.AQUA));
            } else {
                construirFoguete(level, serverPlayer.blockPosition());
                serverPlayer.teleportTo(target, 0.5, 92.0, 0.5,
                        java.util.Set.of(), serverPlayer.getYRot(), serverPlayer.getXRot());
                serverPlayer.sendSystemMessage(Component.literal("Lançamento concluído. Escolha um destino e use o foguete novamente para pousar.")
                        .withStyle(ChatFormatting.AQUA));
            }
        }
        return InteractionResultHolder.sidedSuccess(stack, level.isClientSide);
    }

    private static CorpoCeleste destino(ItemStack stack) {
        String value = stack.getOrCreateTag().getString(DESTINO_TAG);
        try {
            return value.isEmpty() ? CorpoCeleste.MARTE : CorpoCeleste.valueOf(value);
        } catch (IllegalArgumentException ignored) {
            return CorpoCeleste.MARTE;
        }
    }

    private static int landingY(ServerLevel level, CorpoCeleste destino) {
        int topY = level.getHeight(Heightmap.Types.WORLD_SURFACE, 0, 0);
        int y = destino == CorpoCeleste.TERRA ? topY + 1 : Math.max(60, topY + 1);
        if (destino.precisaOxigenio()) {
            for (int x = -2; x <= 2; x++) {
                for (int z = -2; z <= 2; z++) {
                    level.setBlockAndUpdate(new net.minecraft.core.BlockPos(x, y - 1, z), Blocks.SMOOTH_STONE.defaultBlockState());
                    for (int dy = 0; dy < 3; dy++) {
                        level.setBlockAndUpdate(new net.minecraft.core.BlockPos(x, y + dy, z), Blocks.AIR.defaultBlockState());
                    }
                }
            }
        }
        return y;
    }

    private static void construirFoguete(Level level, net.minecraft.core.BlockPos playerPos) {
        int x0 = playerPos.getX() + 5;
        int z0 = playerPos.getZ() + 5;
        int ground = level.getHeight(Heightmap.Types.WORLD_SURFACE, x0, z0) - 1;
        BlockState pad = Blocks.SMOOTH_QUARTZ.defaultBlockState();
        for (int x = -4; x <= 4; x++) for (int z = -4; z <= 4; z++) {
            level.setBlockAndUpdate(new net.minecraft.core.BlockPos(x0 + x, ground, z0 + z), pad);
        }
        BlockState hull = Blocks.WHITE_CONCRETE.defaultBlockState();
        BlockState stripe = Blocks.RED_CONCRETE.defaultBlockState();
        BlockState glass = Blocks.LIGHT_BLUE_STAINED_GLASS.defaultBlockState();
        for (int y = 1; y <= 13; y++) {
            for (int dx = -1; dx <= 1; dx++) for (int dz = -1; dz <= 1; dz++) {
                if (Math.abs(dx) == 1 || Math.abs(dz) == 1) {
                    BlockState state = y == 7 ? stripe : hull;
                    if (y >= 10 && y <= 11 && dz == -1) state = glass;
                    level.setBlockAndUpdate(new net.minecraft.core.BlockPos(x0 + dx, ground + y, z0 + dz), state);
                } else {
                    level.setBlockAndUpdate(new net.minecraft.core.BlockPos(x0 + dx, ground + y, z0 + dz), Blocks.AIR.defaultBlockState());
                }
            }
        }
        for (int dy = 1; dy <= 3; dy++) {
            level.setBlockAndUpdate(new net.minecraft.core.BlockPos(x0 - 2, ground + dy, z0), stripe);
            level.setBlockAndUpdate(new net.minecraft.core.BlockPos(x0 + 2, ground + dy, z0), stripe);
            level.setBlockAndUpdate(new net.minecraft.core.BlockPos(x0, ground + dy, z0 - 2), stripe);
            level.setBlockAndUpdate(new net.minecraft.core.BlockPos(x0, ground + dy, z0 + 2), stripe);
        }
        level.setBlockAndUpdate(new net.minecraft.core.BlockPos(x0, ground + 14, z0), Blocks.IRON_BLOCK.defaultBlockState());
        level.setBlockAndUpdate(new net.minecraft.core.BlockPos(x0, ground + 15, z0), Blocks.END_ROD.defaultBlockState());
        for (int dx = -2; dx <= 2; dx++) for (int dz = -2; dz <= 2; dz++) {
            if (Math.abs(dx) == 2 || Math.abs(dz) == 2) {
                level.setBlockAndUpdate(new net.minecraft.core.BlockPos(x0 + dx, ground + 1, z0 + dz), Blocks.IRON_BLOCK.defaultBlockState());
            }
        }
    }

    @Override
    public void appendHoverText(ItemStack stack, Level level, List<Component> tooltip, TooltipFlag flag) {
        tooltip.add(Component.literal("Clique direito para ir ao espaço ou pousar no destino.").withStyle(ChatFormatting.GRAY));
        tooltip.add(Component.literal("Agache + clique direito para selecionar o destino.")
                .withStyle(ChatFormatting.GRAY));
        tooltip.add(Component.literal("Destino: " + destino(stack).nome()).withStyle(ChatFormatting.AQUA));
    }
}
