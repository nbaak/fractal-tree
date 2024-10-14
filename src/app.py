#!/usr/bin/env python3

import pygame
import datetime


def take_screenshot(surface):
    now = datetime.datetime.now()
    timestamp = now.strftime("%Y%m%d%H%M%S")
    filename = f"screenshot_{timestamp}.png"
    pygame.image.save(surface, filename)
    print(f"Screenshot saved as {filename}")
    
    
def grow_tree(surface:pygame.surface.Surface, start:pygame.Vector2, radius:int, phi:int, beta:int, color:pygame.color.Color, depth:int=12) -> None:
    """
    Draws a fractal tree on the provided surface starting from a given point.

    Parameters:
    -----------
    surface: pygame.surface.Surface
        The surface on which the tree will be drawn.
    start: pygame.Vector2
        The starting point (position) of the tree.
    radius: int
        The length of the current branch.
    phi: int
        The angle of the current branch in degrees.
    beta: int
        The angle at which branches split from each other.
    color: pygame.color.Color
        Color for the tree.
    depth: int
        The current recursion depth.

    Returns:
    --------
    None
        This function does not return any value; it modifies the surface by drawing the tree.
    """
    if not depth: 
        return 
    
    # calculate new endpoint
    dest = pygame.Vector2()
    dest.from_polar((radius, phi))
    dest = start + dest * depth
    
    # change color
    h, s, v, a = color.hsva
    
    v = min(100, (v - depth) % 100)
    s = min(100, (s - depth) % 100)
    
    color = pygame.Color(0)
    color.hsva = (h, s, v, a)
    
    pygame.draw.line(surface, color, start, dest, 3)
    
    grow_tree(surface, dest, radius, phi + beta, beta, color, depth - 1)
    grow_tree(surface, dest, radius, phi - beta, beta, color, depth - 1)


def main():
    pygame.init()

    window_dimensions = width, height = 1800, 1000

    surface = pygame.display.set_mode(window_dimensions)
    pygame.display.set_caption("Pygame App")
    surface.fill('black')
    
    # Fractal Tree can be grown before going in infinite loop
    
    center = width // 2
    root = pygame.Vector2(center, height)
    radius = 10
    phi = 270
    beta = 20
    color = pygame.color.Color(0, 0, 255, 0)
    max_depth = 13
    
    grow_tree(surface, root, radius, phi, beta, color, max_depth)
    
    # loop only to end the programm or take screenshots
    running = True

    while running:
        # Handle Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:
                match event.key:
                    case pygame.K_q: running = False
                    case pygame.K_SPACE: take_screenshot(surface)
                    
        # App
        pygame.display.flip()


if __name__ == "__main__":
    main()
