package com.sistemasolar.event;

import com.sistemasolar.CorpoCeleste;
import com.sistemasolar.SistemaSolarMod;
import com.sistemasolar.item.ItensMod;
import net.minecraft.ChatFormatting;
import net.minecraft.network.chat.Component;
import net.minecraft.world.entity.EquipmentSlot;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.item.ItemStack;
import net.minecraftforge.event.TickEvent;
import net.minecraftforge.eventbus.api.SubscribeEvent;
import net.minecraftforge.fml.common.Mod;

@Mod.EventBusSubscriber(modid = SistemaSolarMod.MOD_ID, bus = Mod.EventBusSubscriber.Bus.FORGE)
public final class EventosAtmosfera {
    private EventosAtmosfera() { }

    public static boolean temTrajeCompleto(Player player) {
        return player.getItemBySlot(EquipmentSlot.HEAD).is(ItensMod.SPACE_HELMET.get())
                && player.getItemBySlot(EquipmentSlot.CHEST).is(ItensMod.SPACE_CHESTPLATE.get())
                && player.getItemBySlot(EquipmentSlot.LEGS).is(ItensMod.SPACE_LEGGINGS.get())
                && player.getItemBySlot(EquipmentSlot.FEET).is(ItensMod.SPACE_BOOTS.get());
    }

    public static boolean temOxigenio(Player player) {
        if (!temTrajeCompleto(player)) return false;
        ItemStack peitoral = player.getItemBySlot(EquipmentSlot.CHEST);
        return peitoral.getOrCreateTag().getInt("Oxygen") > 0;
    }

    @SubscribeEvent
    public static void onPlayerTick(TickEvent.PlayerTickEvent event) {
        if (event.phase != TickEvent.Phase.END || event.player.level().isClientSide
                || event.player.tickCount % 20 != 0) return;

        CorpoCeleste corpo = CorpoCeleste.porDimensao(event.player.level().dimension()).orElse(null);
        if (corpo == null || !corpo.precisaOxigenio()) return;

        Player player = event.player;
        ItemStack peitoral = player.getItemBySlot(EquipmentSlot.CHEST);
        boolean possuiOxigenio = temOxigenio(player);
        if (possuiOxigenio) {
            int restante = peitoral.getOrCreateTag().getInt("Oxygen") - 1;
            peitoral.getOrCreateTag().putInt("Oxygen", restante);
            if (restante % 60 == 0) {
                player.displayClientMessage(Component.literal("Oxigênio: " + (restante / 60) + " min")
                        .withStyle(ChatFormatting.AQUA), true);
            }
        } else {
            player.hurt(player.damageSources().drown(), 2.0F);
        }
    }
}
