package com.sistemasolar.item;

import com.sistemasolar.CorpoCeleste;
import com.sistemasolar.event.EventosAtmosfera;
import net.minecraft.ChatFormatting;
import net.minecraft.core.BlockPos;
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
            CorpoCeleste destino = destino(stack);
            if (destino.precisaOxigenio() && !EventosAtmosfera.temOxigenio(serverPlayer)) {
                serverPlayer.sendSystemMessage(Component.literal("Vista o traje espacial completo e recarregue o oxigênio antes do lançamento.")
                        .withStyle(ChatFormatting.RED));
                return InteractionResultHolder.fail(stack);
            }

            ServerLevel target = serverPlayer.server.getLevel(destino.dimensao());
            if (target == null) {
                serverPlayer.sendSystemMessage(Component.literal("Destino indisponível: " + destino.nome())
                        .withStyle(ChatFormatting.RED));
                return InteractionResultHolder.fail(stack);
            }

            BlockPos pos = landingPosition(target, destino);
            serverPlayer.teleportTo(target, pos.getX() + 0.5, pos.getY(), pos.getZ() + 0.5,
                    java.util.Set.of(), serverPlayer.getYRot(), serverPlayer.getXRot());
            serverPlayer.sendSystemMessage(Component.literal("Lançamento concluído. Destino: " + destino.nome())
                    .withStyle(ChatFormatting.AQUA));
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

    private static BlockPos landingPosition(ServerLevel level, CorpoCeleste destino) {
        int topY = level.getHeight(Heightmap.Types.WORLD_SURFACE, 0, 0);
        int y = destino == CorpoCeleste.TERRA ? topY + 1 : Math.max(100, topY + 3);
        if (destino.precisaOxigenio()) {
            for (int x = -2; x <= 2; x++) {
                for (int z = -2; z <= 2; z++) {
                    level.setBlockAndUpdate(new BlockPos(x, y - 1, z), Blocks.SMOOTH_STONE.defaultBlockState());
                    for (int dy = 0; dy < 3; dy++) {
                        level.setBlockAndUpdate(new BlockPos(x, y + dy, z), Blocks.AIR.defaultBlockState());
                    }
                }
            }
        }
        return new BlockPos(0, y, 0);
    }

    @Override
    public void appendHoverText(ItemStack stack, Level level, List<Component> tooltip, TooltipFlag flag) {
        tooltip.add(Component.literal("Clique com o botão direito para lançar.").withStyle(ChatFormatting.GRAY));
        tooltip.add(Component.literal("Agache + clique direito para selecionar o destino.")
                .withStyle(ChatFormatting.GRAY));
        tooltip.add(Component.literal("Destino: " + destino(stack).nome()).withStyle(ChatFormatting.AQUA));
    }
}
