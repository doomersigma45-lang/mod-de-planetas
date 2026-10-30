package com.sistemasolar.world;

import net.minecraft.client.model.SlimeModel;
import net.minecraft.client.renderer.entity.EntityRendererProvider;
import net.minecraft.client.renderer.entity.MobRenderer;
import net.minecraft.client.model.geom.ModelLayers;
import net.minecraft.resources.ResourceLocation;

public class AlienRenderer extends MobRenderer<AlienEntity, SlimeModel<AlienEntity>> {
    private static final ResourceLocation TEXTURE = new ResourceLocation("minecraft", "textures/entity/slime/slime.png");

    public AlienRenderer(EntityRendererProvider.Context context) {
        super(context, new SlimeModel<>(context.bakeLayer(ModelLayers.SLIME)), 0.5F);
    }

    @Override
    public ResourceLocation getTextureLocation(AlienEntity entity) {
        return TEXTURE;
    }
}
