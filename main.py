import pygame as pg
import constants as c
from Enemy import Enemy  # From Enemy file import the enemy class
from world import World
from turret import Turret
from buttons import Button
import json
from turret_data import TURRET_DATA

# ---------- Initialize pygame ----------
pg.init()

# ---------- Create Clock ----------
clock = pg.time.Clock()

# ---------- Create game window ----------
screen = pg.display.set_mode((c.SCREEN_WIDTH + c.SIDE_PANEL, c.SCREEN_HEIGHT))
pg.display.set_caption("Tower Defense")

# ---------- Game Variables ----------
game_over = False
game_outcome = 0  # -1 is a loss | 1 is a win
level_started = False
last_enemy_spawn = pg.time.get_ticks()
placing_turrets = False
selected_turret = None
active_turret_type = "basic"
buy_buttons = {}

# ---------- Load Images ----------
# Map
map_image = pg.image.load('MapForEnemiesOrPlacingTurrets.png').convert_alpha()

# Turret Images
turret_spritesheets = {}
cursor_images = {}
turret_types = ["basic", "bomb", "ice", "tesla", "laser", "poison", "railgun", "flamethrower", "cannon"]

# --- Load button images into dictionary ---
turret_button_images = {}
for t_type in turret_types:
    level_images = []
    for x in range(1, c.TURRET_LEVELS + 1):
        # Load the level image
        img = pg.image.load(f"assets/images/turrets/{t_type}_{x}.png").convert_alpha()
        level_images.append(img)

    # Store the full list for the turrets to use
    turret_spritesheets[t_type] = level_images

    # --- ADD THIS LINE BELOW ---
    # This stores the Level 1 image specifically for your cursor and button previews
    cursor_images[t_type] = level_images[0]
# --- create button objects ---
for i, t_type in enumerate(turret_types):
    # Math for a 2-column grid in the side panel
    column = i // 5
    row = i % 5
    x_pos = c.SCREEN_WIDTH + 15 + (column * 110)
    y_pos = 100 + (row * 110)

    # Use the image loaded for turret type
    button_img = turret_button_images[t_type]
    buy_buttons[t_type] = Button(x_pos, y_pos, button_img, True)

# Enemies
enemy_images = {
    "weak": pg.image.load('Enemies/weak.png').convert_alpha(),
    "medium": pg.image.load('Enemies/medium.png').convert_alpha(),
    "strong": pg.image.load('Enemies/strong.png').convert_alpha(),
    "elite": pg.image.load('Enemies/elite.png').convert_alpha(),
}
# ------------------------------------------------- Buttons ------------------------------------------------------------
#  -- Turrets --
buy_turret_image = pg.transform.scale(pg.image.load("Turrets/General/BasicTurret.png").convert_alpha(), (150, 50))
bomb_turret_image = pg.transform.scale(pg.image.load('Turrets/General/BombTower.png').convert_alpha(), (150, 50))
cannon_turret_image = pg.transform.scale(pg.image.load('Turrets/General/cannon.png').convert_alpha(), (150, 50))
flamethrower_turret_image = pg.transform.scale(pg.image.load('Turrets/General/flamethrower.png').convert_alpha(), (150, 50))
ice_turret_image = pg.transform.scale(pg.image.load('Turrets/General/ice.png').convert_alpha(), (150, 50))
laser_turret_image = pg.transform.scale(pg.image.load('Turrets/General/laser.png').convert_alpha(), (150, 50))
poison_turret_image = pg.transform.scale(pg.image.load('Turrets/General/poison.png').convert_alpha(), (150, 50))
railgun_turret_image = pg.transform.scale(pg.image.load('Turrets/General/railgun.png').convert_alpha(), (150, 50))
tesla_turret_image = pg.transform.scale(pg.image.load('Turrets/General/tesla.png').convert_alpha(), (150, 50))

# -- General --
cancel_image = pg.transform.scale(pg.image.load("Turrets/General/cancel.png").convert_alpha(), (150, 50))
upgrade_turret_image = pg.transform.scale(pg.image.load('Turrets/General/UpgradeTurretButton.png').convert_alpha(), (150, 50))
begin_image = pg.transform.scale(pg.image.load('Turrets/General/BeginLevel.png').convert_alpha(), (150, 50))
restart_image = pg.image.load('Turrets/General/RestartGame.png').convert_alpha()
fast_forward_image = pg.transform.scale(pg.image.load('Turrets/General/FastForward.png').convert_alpha(), (150, 50))
sell_turret_image = pg.transform.scale(pg.image.load('Turrets/General/SellTurret.png').convert_alpha(), (150, 50))

# Not yet configured
# basic_turret_image = pg.transform.scale(pg.image.load('Turrets/General/BasicTurret.png').convert_alpha(), (150, 50))
sniper_turret_image = pg.transform.scale(pg.image.load('Turrets/General/SniperTurret.png').convert_alpha(), (150, 50))

# GUI
heart_image = pg.image.load('Turrets/General/heart.png').convert_alpha()
coin_image = pg.image.load('Turrets/General/coin.png').convert_alpha()
logo_image = pg.image.load('Turrets/General/logo.png').convert_alpha()

# Load sounds (I don't have a sound yet but This is the code)
shot_fx = pg.mixer.Sound('Turrets/General/shot.ogg')
shot_fx.set_volume(0.25)

# ---------- Load Json data for level ----------
with open('Waypoints.tmj') as file:
    world_data = json.load(file)

# Load fonts for displaying text on the screen
text_font = pg.font.SysFont("Consolas", 24, bold=True)
large_font = pg.font.SysFont("Consolas", 36)


# Function for outputting text onto the screen
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))


def display_data():
    # Draw panel
    pg.draw.rect(screen, "grey100", (c.SCREEN_WIDTH, 0, c.SIDE_PANEL, 400), 10)
    pg.draw.rect(screen, "navyblue", (c.SCREEN_WIDTH, 0, c.SIDE_PANEL, c.SCREEN_HEIGHT))
    screen.blit(logo_image, (c.SCREEN_WIDTH, 825))
    # Display data:
    draw_text("Level: " + str(world.level), text_font, "white", c.SCREEN_WIDTH + 10, 10)
    screen.blit(heart_image, (c.SCREEN_WIDTH + 10, 25))
    draw_text(str(world.health), text_font, "red", c.SCREEN_WIDTH + 50, 40)
    screen.blit(coin_image, (c.SCREEN_WIDTH + 10, 55))
    draw_text(str(world.money), text_font, "green", c.SCREEN_WIDTH + 50, 70)


def create_turret(mouse_pos, turret_type):  # Add turret_type argument
    mouse_tile_x = mouse_pos[0] // c.TILE_SIZE
    mouse_tile_y = mouse_pos[1] // c.TILE_SIZE
    mouse_tile_num = (mouse_tile_y * c.COLS) + mouse_tile_x

    if world.tile_map[mouse_tile_num] == 884:
        space_is_free = True
        for turret in turret_group:
            if (mouse_tile_x, mouse_tile_y) == (turret.tile_x, turret.tile_y):
                space_is_free = False

        if space_is_free:
            # Look up the cost from the new dictionary in turret_data.py
            cost = TURRET_DATA[turret_type][0]["cost"]
            if world.money >= cost:
                # Pass the sheet for this type and the type string
                new_turret = Turret(turret_spritesheets[turret_type], mouse_tile_x, mouse_tile_y, shot_fx, turret_type)  # Add shot_fx once file for sound added
                turret_group.add(new_turret)
                world.money -= cost


def select_turret(mouse_pos):
    mouse_tile_x = mouse_pos[0] // c.TILE_SIZE
    mouse_tile_y = mouse_pos[1] // c.TILE_SIZE
    for turret in turret_group:
        if (mouse_tile_x, mouse_tile_y) == (turret.tile_x, turret.tile_y):
            return turret


def clear_selection():
    for turret in turret_group:
        turret.selected = False


# ---------- Create world ----------
world = World(world_data, map_image)
world.process_data()
world.process_enemies()

# ---------- Create Groups ----------
enemy_group = pg.sprite.Group()
turret_group = pg.sprite.Group()

# Create buttons
cancel_button = Button(c.SCREEN_WIDTH + 150, 1, cancel_image, True)
bomb_turret_button = Button(c.SCREEN_WIDTH + 150, 100, bomb_turret_image, True)
turret_button = Button(c.SCREEN_WIDTH, 100, buy_turret_image, True)
sell_turret_button = Button(c.SCREEN_WIDTH, 450, sell_turret_image, True)
# Create a dictionary to hold all buy buttons
# main.py
# Load your custom button graphics
turret_button_images = {}
for t_type in turret_types:
    # This assumes your buttons are named 'basic_btn.png', 'ice_btn.png', etc.
    # Adjust the path to match your actual folder!
    path = f'Turrets/General/{t_type}.png'
    img = pg.image.load(path).convert_alpha()
    turret_button_images[t_type] = pg.transform.scale(img, (90, 90))

'''
# basic_turret_button = Button(c.SCREEN_WIDTH, 100, buy_turret_image, True)
sniper_turret_button = Button(c.SCREEN_WIDTH, 50, buy_turret_image, True)
cannon_turret_image = Button(c.SCREEN_WIDTH, 150, cannon_turret_image, True)
flamethrower_turret_image = Button(c.SCREEN_WIDTH, 200, flamethrower_turret_image, True)
ice_turret_image = Button(c.SCREEN_WIDTH + 150, 200, ice_turret_image, True)
laser_turret_image = Button(c.SCREEN_WIDTH, 250, laser_turret_image, True)
poison_turret_image = Button(c.SCREEN_WIDTH + 150, 250, poison_turret_image, True)
railgun_turret_image = Button(c.SCREEN_WIDTH, 300, railgun_turret_image, True)
tesla_turret_image = Button(c.SCREEN_WIDTH + 150, 300, tesla_turret_image, True)
'''

upgrade_button = Button(c.SCREEN_WIDTH, 400, upgrade_turret_image, True)
begin_button = Button(c.SCREEN_WIDTH, 700, begin_image, True)
restart_button = Button(100 + 75, 125 + 75, restart_image, True)
fast_forward_button = Button(c.SCREEN_WIDTH + -150, 700, fast_forward_image, False)

# ---------- Game loop ----------
run = True
while run:

    clock.tick(c.FPS)

    display_data()

    # ---------- Draw buttons ----------
    # button for placing turrets
    '''
    # 'Turret Buy' button will show the price near it:
    draw_text(str(c.BUY_COST), text_font, "grey100", c.SCREEN_WIDTH + 215, 140)
    screen.blit(coin_image, (c.SCREEN_WIDTH + 260, 130))
    '''
    # Draw all buttons from dictionary

    for i, t_type in enumerate(turret_types):
        # Math for 2 columns
        column = i // 5
        row = i % 5
        x_pos = c.SCREEN_WIDTH + 15 + (column * 110)
        y_pos = 100 + (row * 110)

        # Get specific button image for turret
        button_img = turret_button_images[t_type]

        # Create button
        buy_buttons[t_type] = Button(x_pos, y_pos, button_img, True)

    if cancel_button.draw(screen):
        placing_turrets = False

    # if a turret is selected then show buttons
    if selected_turret:
        # 1. Handle SELLING first
        refund = int(selected_turret.total_cost * c.REFUND_TURRET_RATE)
        draw_text(str(refund), text_font, "grey100", c.SCREEN_WIDTH + 215, 475)
        screen.blit(coin_image, (c.SCREEN_WIDTH + 200, 475))

        if sell_turret_button.draw(screen):
            world.money += refund
            selected_turret.kill()
            selected_turret = None  # Now it is None...

        # 2. Handle UPGRADING only if the turret WASN'T sold (if it's still not None)
        if selected_turret is not None:
            if selected_turret.upgrade_level < c.TURRET_LEVELS:
                draw_text(str(c.UPGRADE_COST), text_font, "grey100", c.SCREEN_WIDTH + 215, 425)
                screen.blit(coin_image, (c.SCREEN_WIDTH + 200, 425))

                if upgrade_button.draw(screen):
                    # Small fix here: Check UPGRADE_COST, not the base cost of a new turret!
                    if world.money >= c.UPGRADE_COST:
                        selected_turret.upgrade()
                        world.money -= c.UPGRADE_COST

    ''' ---------------------------------------- UPDATING SECTION ---------------------------------------- '''

    # --- STEP 3: Draw the buttons and the turret preview ---
    for t_type, button in buy_buttons.items():
        # Draw the actual button graphic
        if button.draw(screen):
            placing_turrets = True
            active_turret_type = t_type

        # Draw the Level 1 turret sprite underneath the button as a preview
        # We grab the image from the cursor_images dictionary you already have
        preview_img = pg.transform.scale(cursor_images[t_type], (35, 35))

        # Position the preview image slightly overlapping the bottom of the button
        screen.blit(preview_img, (button.rect.right - 35, button.rect.bottom - 30))

        # Draw the cost text
        cost = TURRET_DATA[t_type][0]["cost"]
        draw_text(str(cost), text_font, "grey100", button.rect.centerx - 15, button.rect.bottom + 2)

    '''if game_over == False:
        # check if player has lost
        if world.health <= 0:
            game_over = True
            game_outcome = -1  # Loss
        # Check if player has won
        if world.level > c.TOTAL_LEVELS:
            game_over = True
            game_outcome = 1  # Win

        # ---------- Update Groups ----------
        enemy_group.update(world)
        turret_group.update(enemy_group, world)

        # Highlight selected turret
        if selected_turret:
            selected_turret.selected = True'''

    ''' ---------------------------------------- DRAWING SECTION ---------------------------------------- '''

    # -------------------- Draw level --------------------
    world.draw(screen)

    # -------------------- Draw enemy path (draw waypoints) (optional) --------------------
    pg.draw.lines(screen, "grey0", False, world.waypoints)

    # -------------------- Draw Groups --------------------
    enemy_group.draw(screen)
    for turret in turret_group:
        turret.draw(screen)

    # Check if you have lost the game
    if game_over == False:
        # -------------------- Check if level has been started --------------------
        if level_started == False:
            if begin_button.draw(screen):
                level_started = True
        else:
            # Fast-forward option
            world.game_speed = 1
            if fast_forward_button.draw(screen):
                world.game_speed = 3
            # -------------------- Spawn enemies --------------------
            if pg.time.get_ticks() - last_enemy_spawn > (c.SPAWN_COOLDOWN / world.game_speed):
                # -------------------- Enemy --------------------
                if world.spawned_enemies < len(world.enemy_list):
                    enemy_type = world.enemy_list[world.spawned_enemies]
                    enemy = Enemy(enemy_type, world.waypoints, enemy_images)
                    enemy_group.add(enemy)  # add enemy to enemy list
                    world.spawned_enemies += 1
                    last_enemy_spawn = pg.time.get_ticks()

        # Check if wave has finished
        if world.check_level_complete() == True:
            world.money += c.LEVEL_COMPLETE_REWARD
            world.level += 1
            level_started = False
            last_enemy_spawn = pg.time.get_ticks()
            world.reset_level()
            world.process_enemies()

        # Draw turret on mouse when placing
        if placing_turrets:
            mouse_pos = pg.mouse.get_pos()
            # Change cursor_turret to use the active type
            cursor_img = cursor_images[active_turret_type]
            rect = cursor_img.get_rect()
            rect.center = mouse_pos
            screen.blit(cursor_img, rect)
    else:
        pg.draw.rect(screen, "darkgreen", (200 + 75, 200 + 75, 400, 200), border_radius=30)
        if game_outcome == -1:
            draw_text("GAME OVER", large_font, "grey0", 310 + 75, 230 + 75)
        elif game_outcome == 1:
            draw_text("YOU WIN!", large_font, "grey0", 310 + 75, 230 + 75)
        if restart_button.draw(screen):
            game_over = False
            level_started = False
            placing_turrets = False
            selected_turret = None
            last_enemy_spawn = pg.time.get_ticks()
            world = World(world_data, map_image)
            world.process_data()
            world.process_enemies()
            # Clear Groups
            enemy_group.empty()
            turret_group.empty()

    # print(turret_group)  # FOR DEBUGGING HOW MANY TURRETS EXIST

    # ------------------------------ Event Handler ------------------------------
    for event in pg.event.get():
        # Quit Game
        if event.type == pg.QUIT:
            run = False
        # Mouse Click
        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = pg.mouse.get_pos()
            # Check if mouse is on the turret place area
            if mouse_pos[0] < c.SCREEN_WIDTH and mouse_pos[1] < c.SCREEN_HEIGHT:
                # Clear selected turrets
                selected_turret = None
                clear_selection()
                # Check if there is enough money for buying a turret
                if placing_turrets == True:
                    # if world.money >= c.BUY_COST:  # money handled inside create_turret
                    create_turret(mouse_pos, active_turret_type)
                else:
                    selected_turret = select_turret(mouse_pos)

    # -------------------- Update display --------------------
    pg.display.flip()  # Or use: pg.display.update()

pg.quit()
