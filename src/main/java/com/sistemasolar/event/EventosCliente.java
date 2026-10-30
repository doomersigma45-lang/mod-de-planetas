package com.sistemasolar.event;

import com.sistemasolar.SistemaSolarMod;
import com.sistemasolar.world.AlienRenderer;
import com.sistemasolar.world.EntidadesMod;
import net.minecraftforge.api.distmarker.Dist;
import net.minecraftforge.client.event.EntityRenderersEvent;
import net.minecraftforge.eventbus.api.SubscribeEvent;
import net.minecraftforge.fml.common.Mod;

@Mod.EventBusSubscriber(modid = SistemaSolarMod.MOD_ID, bus = Mod.EventBusSubscriber.Bus.MOD, value = Dist.CLIENT)
public final class EventosCliente {
    private EventosCliente() { }

    @SubscribeEvent
    public static void registrarRenderizador(EntityRenderersEvent.RegisterRenderers event) {
        event.registerEntityRenderer(EntidadesMod.ALIEN.get(), AlienRenderer::new);
    }
}
