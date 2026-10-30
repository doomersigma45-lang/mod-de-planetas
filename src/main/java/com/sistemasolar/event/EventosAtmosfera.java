package com.sistemasolar.event;

import com.sistemasolar.CorpoCeleste;
import com.sistemasolar.SistemaSolarMod;
import com.sistemasolar.item.ItensMod;
import com.sistemasolar.world.EspacoSolar;
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
        if (event.phase != TickEvent.Phase.END || event.player.level().isClientSide) return;

        Player player = event.player;
        boolean noEspaco = player.level().dimension().equals(EspacoSolar.DIMENSAO);
        if (noEspaco && !player.onGround()) {
            net.minecraft.world.phys.Vec3 movimento = player.getDeltaMovement();
            player.setDeltaMovement(movimento.x, Math.max(-0.04, Math.min(0.04, movimento.y)), movimento.z);
        }
        if (player.tickCount % 20 != 0) return;

        CorpoCeleste corpo = CorpoCeleste.porDimensao(player.level().dimension()).orElse(null);
        if (!noEspaco && (corpo == null || !corpo.precisaOxigenio())) {
            if (player instanceof net.minecraft.server.level.ServerPlayer serverPlayer && player.getY() > 256) {
                if (temOxigenio(player)) {
                    net.minecraft.server.level.ServerLevel espaco = serverPlayer.server.getLevel(EspacoSolar.DIMENSAO);
                    if (espaco != null) {
                        serverPlayer.teleportTo(espaco, player.getX(), 92.0, player.getZ(),
                                java.util.Set.of(), player.getYRot(), player.getXRot());
                        player.displayClientMessage(Component.literal("Você alcançou o espaço.")
                                .withStyle(ChatFormatting.AQUA), true);
                    }
                } else {
                    player.hurt(player.damageSources().drown(), 4.0F);
                    player.teleportTo(player.getX(), 250.0, player.getZ());
                    player.displayClientMessage(Component.literal("Você precisa do traje e de oxigênio para sair da atmosfera.")
                            .withStyle(ChatFormatting.RED), true);
                }
            }
            return;
        }

        ItemStack peitoral = player.getItemBySlot(EquipmentSlot.CHEST);
        boolean possuiOxigenio = temOxigenio(player);
        if (possuiOxigenio) {
            int restante = peitoral.getOrCreateTag().getInt("Oxygen") - 1;
            peitoral.getOrCreateTag().putInt("Oxygen", restante);
            if (restante % 400 == 0) {
                player.displayClientMessage(Component.literal("Oxigênio: " + (restante / 20) + " s")
                        .withStyle(ChatFormatting.AQUA), true);
            }
        } else {
            player.hurt(player.damageSources().drown(), 2.0F);
        }
    }
}
