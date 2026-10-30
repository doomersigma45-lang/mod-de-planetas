package com.sistemasolar.item;

import com.sistemasolar.CorpoCeleste;
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

import java.util.List;
import java.util.Set;

public class LocalizadorItem extends Item {
    private final CorpoCeleste destino;

    public LocalizadorItem(CorpoCeleste destino) {
        super(new Item.Properties().stacksTo(1));
        this.destino = destino;
    }

    @Override
    public InteractionResultHolder<ItemStack> use(Level level, Player player, InteractionHand hand) {
        ItemStack stack = player.getItemInHand(hand);
        if (!level.isClientSide && player instanceof ServerPlayer serverPlayer) {
            ServerLevel target = serverPlayer.server.getLevel(destino.dimensao());
            if (target == null) {
                serverPlayer.sendSystemMessage(Component.literal("Destino indisponível: " + destino.nome())
                        .withStyle(ChatFormatting.RED));
            } else if (serverPlayer.serverLevel() == target) {
                serverPlayer.sendSystemMessage(Component.literal("Você já está em " + destino.nome() + ".")
                        .withStyle(ChatFormatting.GRAY));
            } else {
                serverPlayer.teleportTo(target, 0.5, 100.0, 0.5, Set.of(),
                        serverPlayer.getYRot(), serverPlayer.getXRot());
                serverPlayer.sendSystemMessage(Component.literal("Destino: " + destino.nome())
                        .withStyle(ChatFormatting.AQUA));
            }
        }
        return InteractionResultHolder.sidedSuccess(stack, level.isClientSide);
    }

    @Override
    public void appendHoverText(ItemStack stack, Level level, List<Component> tooltip, TooltipFlag flag) {
        tooltip.add(Component.literal("Clique com o botão direito para viajar até " + destino.nome() + ".")
                .withStyle(ChatFormatting.GRAY));
    }
}
