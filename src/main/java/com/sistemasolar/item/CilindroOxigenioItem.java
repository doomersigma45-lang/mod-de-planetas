package com.sistemasolar.item;

import net.minecraft.ChatFormatting;
import net.minecraft.network.chat.Component;
import net.minecraft.world.InteractionHand;
import net.minecraft.world.InteractionResultHolder;
import net.minecraft.world.entity.EquipmentSlot;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.TooltipFlag;
import net.minecraft.world.level.Level;

import java.util.List;

public class CilindroOxigenioItem extends Item {
    public static final int CARGA_COMPLETA = 2400;

    public CilindroOxigenioItem() {
        super(new Item.Properties().stacksTo(16));
    }

    @Override
    public InteractionResultHolder<ItemStack> use(Level level, Player player, InteractionHand hand) {
        ItemStack cilindro = player.getItemInHand(hand);
        if (!level.isClientSide) {
            ItemStack peitoral = player.getItemBySlot(EquipmentSlot.CHEST);
            if (peitoral.is(ItensMod.SPACE_CHESTPLATE.get())) {
                peitoral.getOrCreateTag().putInt("Oxygen", CARGA_COMPLETA);
                if (!player.getAbilities().instabuild) cilindro.shrink(1);
                player.displayClientMessage(Component.literal("Oxigênio recarregado.")
                        .withStyle(ChatFormatting.AQUA), true);
            } else {
                player.displayClientMessage(Component.literal("Equipe o peitoral espacial antes de recarregar.")
                        .withStyle(ChatFormatting.RED), true);
            }
        }
        return InteractionResultHolder.sidedSuccess(cilindro, level.isClientSide);
    }

    @Override
    public void appendHoverText(ItemStack stack, Level level, List<Component> tooltip, TooltipFlag flag) {
        tooltip.add(Component.literal("Recarrega até 2 minutos de oxigênio.").withStyle(ChatFormatting.GRAY));
    }
}
