import pygame
import numpy as np
import math
import random

class Particle:
    """Individual particle for effects"""
    
    def __init__(self, x, y, vx, vy, lifetime, color, size):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.lifetime = lifetime
        self.age = 0
        self.color = color
        self.size = size
        self.alive = True
    
    def update(self):
        """Update particle"""
        self.vy += 0.15  # gravity
        self.x += self.vx
        self.y += self.vy
        self.age += 1
        
        if self.age >= self.lifetime:
            self.alive = False
    
    def draw(self, surface):
        """Draw particle"""
        if not self.alive or self.size <= 0:
            return
        
        # Fade out
        alpha_ratio = 1 - (self.age / self.lifetime)
        color = (
            int(self.color[0] * alpha_ratio),
            int(self.color[1] * alpha_ratio),
            int(self.color[2] * alpha_ratio)
        )
        
        size = max(1, int(self.size * alpha_ratio))
        pygame.draw.circle(surface, color, (int(self.x), int(self.y)), size)


class ExplosionEffect:
    """Explosion/impact effect"""
    
    def __init__(self, x, y, intensity=30, colors=None):
        self.x = x
        self.y = y
        self.particles = []
        self.alive = True
        self.age = 0
        self.lifetime = 60  # frames
        
        if colors is None:
            colors = [
                (255, 120, 0),   # Orange
                (255, 200, 0),   # Yellow
                (255, 80, 0),    # Red-orange
                (255, 255, 0),   # Bright yellow
                (200, 80, 0),    # Dark orange
            ]
        
        # Create particles
        for _ in range(intensity):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(2, 8)
            vx = math.cos(angle) * speed
            vy = math.sin(angle) * speed
            
            particle = Particle(
                x, y, vx, vy,
                lifetime=random.randint(30, 60),
                color=random.choice(colors),
                size=random.randint(3, 10)
            )
            self.particles.append(particle)
        
        # Create shockwave
        self.shockwave_radius = 0
        self.max_shockwave_radius = 150
    
    def update(self):
        """Update effect"""
        self.age += 1
        
        # Update particles
        for particle in self.particles[:]:
            particle.update()
            if not particle.alive:
                self.particles.remove(particle)
        
        # Update shockwave
        self.shockwave_radius = (self.age / self.lifetime) * self.max_shockwave_radius
        
        if self.age >= self.lifetime:
            self.alive = False
    
    def draw(self, surface):
        """Draw effect"""
        # Draw particles
        for particle in self.particles:
            particle.draw(surface)
        
        # Draw shockwave ring
        if self.shockwave_radius > 0 and self.shockwave_radius < self.max_shockwave_radius:
            alpha_ratio = 1 - (self.age / self.lifetime)
            shockwave_color = (255, int(150 * alpha_ratio), 0)
            thickness = max(1, int(3 * alpha_ratio))
            
            pygame.draw.circle(
                surface,
                shockwave_color,
                (int(self.x), int(self.y)),
                int(self.shockwave_radius),
                thickness
            )


class FlashEffect:
    """Screen flash effect (white flash on impact)"""
    
    def __init__(self, duration=30, intensity=255):
        self.duration = duration
        self.age = 0
        self.intensity = intensity
        self.alive = True
    
    def update(self):
        """Update flash"""
        self.age += 1
        if self.age >= self.duration:
            self.alive = False
    
    def draw(self, surface):
        """Draw flash overlay"""
        if not self.alive:
            return
        
        # Fade out flash
        alpha_ratio = 1 - (self.age / self.duration)
        flash_color = (255, 255, 200)
        flash_surface = pygame.Surface(surface.get_size())
        flash_surface.fill(flash_color)
        flash_surface.set_alpha(int(100 * alpha_ratio))
        surface.blit(flash_surface, (0, 0))


class TrailEffect:
    """Particle trail for moving objects"""
    
    def __init__(self, max_particles=50):
        self.particles = []
        self.max_particles = max_particles
    
    def add_particle(self, x, y, color=(255, 150, 0), size=5, lifetime=20):
        """Add particle to trail"""
        vx = random.uniform(-1, 1)
        vy = random.uniform(-2, 0)
        
        particle = Particle(x, y, vx, vy, lifetime, color, size)
        self.particles.append(particle)
        
        # Limit particles
        if len(self.particles) > self.max_particles:
            self.particles.pop(0)
    
    def update(self):
        """Update trail"""
        for particle in self.particles[:]:
            particle.update()
            if not particle.alive:
                self.particles.remove(particle)
    
    def draw(self, surface):
        """Draw trail"""
        for particle in self.particles:
            particle.draw(surface)


class EffectManager:
    """Manages all visual effects"""
    
    def __init__(self):
        self.explosions = []
        self.flashes = []
        self.trails = []
    
    def add_explosion(self, x, y, intensity=30):
        """Add explosion effect"""
        self.explosions.append(ExplosionEffect(x, y, intensity))
    
    def add_flash(self, duration=30):
        """Add screen flash"""
        self.flashes.append(FlashEffect(duration))
    
    def add_trail(self, x, y, color=(255, 150, 0)):
        """Add to particle trail"""
        for trail in self.trails:
            trail.add_particle(x, y, color)
    
    def create_trail(self):
        """Create new trail effect"""
        trail = TrailEffect()
        self.trails.append(trail)
        return trail
    
    def update(self):
        """Update all effects"""
        # Update explosions
        for explosion in self.explosions[:]:
            explosion.update()
            if not explosion.alive:
                self.explosions.remove(explosion)
        
        # Update flashes
        for flash in self.flashes[:]:
            flash.update()
            if not flash.alive:
                self.flashes.remove(flash)
        
        # Update trails
        for trail in self.trails:
            trail.update()
    
    def draw(self, surface):
        """Draw all effects"""
        # Draw explosions
        for explosion in self.explosions:
            explosion.draw(surface)
        
        # Draw trails
        for trail in self.trails:
            trail.draw(surface)
        
        # Draw flashes last (on top)
        for flash in self.flashes:
            flash.draw(surface)
    
    def clear(self):
        """Clear all effects"""
        self.explosions.clear()
        self.flashes.clear()
        self.trails.clear()
