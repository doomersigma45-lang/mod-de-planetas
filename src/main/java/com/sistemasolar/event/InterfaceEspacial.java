package com.sistemasolar.event;

import com.sistemasolar.SistemaSolarMod;
import com.sistemasolar.item.CilindroOxigenioItem;
import com.sistemasolar.item.ItensMod;
import net.minecraft.client.Minecraft;
import net.minecraft.client.player.LocalPlayer;
import net.minecraft.network.chat.Component;
import net.minecraft.world.entity.EquipmentSlot;
import net.minecraft.world.item.ItemStack;
import net.minecraftforge.api.distmarker.Dist;
import net.minecraftforge.client.event.RenderGuiOverlayEvent;
import net.minecraftforge.client.gui.overlay.VanillaGuiOverlay;
import net.minecraftforge.eventbus.api.SubscribeEvent;
import net.minecraftforge.fml.common.Mod;

@Mod.EventBusSubscriber(modid = SistemaSolarMod.MOD_ID, bus = Mod.EventBusSubscriber.Bus.FORGE, value = Dist.CLIENT)
public final class InterfaceEspacial {
    private InterfaceEspacial() { }

    @SubscribeEvent
    public static void mostrarOxigenio(RenderGuiOverlayEvent.Post event) {
        if (!event.getOverlay().id().equals(VanillaGuiOverlay.HOTBAR.id())) return;
        Minecraft minecraft = Minecraft.getInstance();
        LocalPlayer player = minecraft.player;
        if (player == null || !player.getItemBySlot(EquipmentSlot.HEAD).is(ItensMod.SPACE_HELMET.get())) return;
        ItemStack tank = player.getItemBySlot(EquipmentSlot.CHEST);
        if (!tank.is(ItensMod.SPACE_CHESTPLATE.get())) return;

        int oxygen = tank.getOrCreateTag().getInt("Oxygen");
        int x = event.getWindow().getGuiScaledWidth() / 2 + 98;
        int y = event.getWindow().getGuiScaledHeight() - 48;
        int width = 42;
        int filled = Math.max(0, Math.min(width, oxygen * width / CilindroOxigenioItem.CARGA_COMPLETA));
        event.getGuiGraphics().fill(x, y, x + width, y + 6, 0xFF242424);
        event.getGuiGraphics().fill(x, y, x + filled, y + 6, oxygen > 400 ? 0xFF42D9E8 : 0xFFE04A4A);
        event.getGuiGraphics().drawString(minecraft.font,
                Component.literal("O₂ " + (oxygen / 20) + "s"), x, y - 10, 0xFFFFFFFF, true);
    }
}
