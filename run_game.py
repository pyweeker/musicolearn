#! /usr/bin/env python3
# -*- coding: utf-8 -*-


import math
from typing import Optional, Union #, NoneType
import arcade

import time

from frozendict import frozendict

print("Chords and degres :")
print("http://www.piano-keyboard-guide.com/key-of-c.html")

import music21
from music21 import *



application_path_timidity = "/usr/bin/timidity"
music21.environment.set('midiPath', application_path_timidity)

import operator


from collections import OrderedDict


"""
Common chord progressions in the key of C major are as follows:

    I – IV – V (C – F- G)
    I – vi – IV – V (C – Am – F – G)
    ii – V – I (Dm7 – G7 – Cmaj7)

The following are diagrams of the C major key signature and the notes of the C major scale on the treble and bass clefs.
 This scale has no sharps and no flats. On piano, you play white keys only.



So what are the notes of these chords?

    Chord I, C major consists of the notes, C – E – G, while C major seventh consists of the notes, C – E – G – B.
    Chord ii, D minor consists of the notes, D – F – A. D minor seventh consists of the notes, D – F – A – C.
    Chord iii, E minor contains the notes, E – G – B. E minor seventh contains the notes, E – G – B – D.
    Chord IV, F major contains the notes, F – A – C. F major seventh contains the notes, F – A – C – E.
    Chord V, G major contains the notes, G – B – D. G dominant seventh contains the notes, G – B – D – F.
    Chord vi, A minor consists of the notes, A – C – E. A minor seventh consists of the note, A – C – E – G.
    Lastly, chord vii°, B diminished consists of the notes, B – D – F, while B minor seventh flat five consists of the notes, B – D – F – A.



Here are the chords in C major. I shall list both the triads (three note chords) and four note extended chords (with sevenths). Roman numerals indicate each chord’s position relative to the scale. Numerals that represent a major chord are usually capitalized, and minor and diminished chords are lower case.

    I – C major, C major seventh (Cmaj, Cmaj7)
    ii – D minor, D minor seventh (Dm, Dm7)
    iii – E minor, E minor seventh (Em, Em7)
    IV – F major, F major seventh (F, Fmaj 7)
    V – G major, G dominant seventh (G, G7)
    vi – A minor, A minor seventh (Am, Am7)
    vii° – B diminished, B minor seventh flat five (B°, Bm7b5)

Clearly, the basic chords/triads in the key of C major are C major, D minor, E minor, F major, G major, A minor, and B diminished.
"""


SCREEN_TITLE = "Musicolearn"

# How big are our image tiles?
SPRITE_IMAGE_SIZE = 128

# Scale sprites up or down
SPRITE_SCALING_PLAYER = 0.5
SPRITE_SCALING_TILES = 0.5

# Scaled sprite size for tiles
SPRITE_SIZE = int(SPRITE_IMAGE_SIZE * SPRITE_SCALING_PLAYER)

# Size of grid to show on screen, in number of tiles
SCREEN_GRID_WIDTH = 25
SCREEN_GRID_HEIGHT = 15

# Size of screen to show, in pixels
SCREEN_WIDTH = SPRITE_SIZE * SCREEN_GRID_WIDTH
SCREEN_HEIGHT = SPRITE_SIZE * SCREEN_GRID_HEIGHT

HALF_SCREEN_WIDTH = SCREEN_WIDTH // 2
HALF_SCREEN_HEIGHT = SCREEN_HEIGHT // 2

# --- Physics forces. Higher number, faster accelerating.

# Gravity
GRAVITY = 1500

# Damping - Amount of speed lost per second
DEFAULT_DAMPING = 1.0
PLAYER_DAMPING = 0.4

#PLAYER_DAMPING = 0.9


# Friction between objects
PLAYER_FRICTION = 1.0
WALL_FRICTION = 0.7
DYNAMIC_ITEM_FRICTION = 0.6

ICE_FRICTION = 0.0



# Mass (defaults to 1)
PLAYER_MASS = 2.0

# Keep player from going too fast
PLAYER_MAX_HORIZONTAL_SPEED = 450
PLAYER_MAX_VERTICAL_SPEED = 1600

# Force applied while on the ground
PLAYER_MOVE_FORCE_ON_GROUND = 8000

# Force applied when moving left/right in the air
PLAYER_MOVE_FORCE_IN_AIR = 900

# Strength of a jump
PLAYER_JUMP_IMPULSE = 1800

# Close enough to not-moving to have the animation go to idle.
DEAD_ZONE = 0.1

# Constants used to track if the player is facing left or right
RIGHT_FACING = 0
LEFT_FACING = 1

# How many pixels to move before we change the texture in the walking animation
DISTANCE_TO_CHANGE_TEXTURE = 20

# How much force to put on the bullet
BULLET_MOVE_FORCE = 4500

# Mass of the bullet
BULLET_MASS = 0.1

# Make bullet less affected by gravity
BULLET_GRAVITY = 300

# GAMEPAD BUTTON CONFIG

JUMPBTN = 0 # A


LIVES_AT_START = 3

SCORE_XOFFSET = 10
SCORE_YOFFSET = 10

TILE_SCALING = 0.5


print("MEMO : press T on Tiled to place objects likes keys on object mode (no simple tiles)")


CHORDDETECTOR_TEXTURE = arcade.load_texture("resources/images/misc/grey_1px_2560_alpha_75.png")


#  !!!!!!!!!!!!! PAS DE DIESE / BEMOL ni OCTAVE ICI !!!!!!!!!!!!!!!!!
INDEX_TO_INTERNATIONAL = {0:'C', 1:'D', 2:'E', 3:'F', 4:'G', 5:'A', 6:'B'}
INDEX_TO_FR = {0:'Do', 1:'Re', 2:'Mi', 3:'Fa', 4:'Sol', 5:'La', 6:'Si'}
#  !!!!!!!!!!!!! PAS DE DIESE / BEMOL ni OCTAVE ICI !!!!!!!!!!!!!!!!!

CHORDDETECTOR_CENTER_PIXEL_SHIFT = 0

SOUND_PATH = "./resources/sounds/"

class PlayerSprite(arcade.Sprite):
    """ Player Sprite """
    def __init__(self,
                 ladder_list: arcade.SpriteList,
                 hit_box_algorithm):
        """ Init """
        # Let parent initialize
        super().__init__()

        

        # Set our scale
        self.scale = SPRITE_SCALING_PLAYER

        # Images from Kenney.nl's Character pack
        
        main_path = ":resources:images/animated_characters/female_person/femalePerson"
        

        # Load textures for idle standing
        self.idle_texture_pair = arcade.load_texture_pair(f"{main_path}_idle.png",
                                                          hit_box_algorithm=hit_box_algorithm)
        self.jump_texture_pair = arcade.load_texture_pair(f"{main_path}_jump.png")
        self.fall_texture_pair = arcade.load_texture_pair(f"{main_path}_fall.png")

        # Load textures for walking
        self.walk_textures = []
        for i in range(8):
            texture = arcade.load_texture_pair(f"{main_path}_walk{i}.png")
            self.walk_textures.append(texture)

        # Load textures for climbing
        self.climbing_textures = []
        texture = arcade.load_texture(f"{main_path}_climb0.png")
        self.climbing_textures.append(texture)
        texture = arcade.load_texture(f"{main_path}_climb1.png")
        self.climbing_textures.append(texture)

        # Set the initial texture
        self.texture = self.idle_texture_pair[0]

        # Hit box will be set based on the first image used.
        self.hit_box = self.texture.hit_box_points

        # Default to face-right
        self.character_face_direction = RIGHT_FACING

        # Index of our current texture
        self.cur_texture = 0

        # How far have we traveled horizontally since changing the texture
        self.x_odometer = 0
        self.y_odometer = 0

        self.ladder_list = ladder_list
        self.is_on_ladder = False

    def pymunk_moved(self, physics_engine, dx, dy, d_angle):
        """ Handle being moved by the pymunk engine """
        # Figure out if we need to face left or right
        if dx < -DEAD_ZONE and self.character_face_direction == RIGHT_FACING:
            self.character_face_direction = LEFT_FACING
        elif dx > DEAD_ZONE and self.character_face_direction == LEFT_FACING:
            self.character_face_direction = RIGHT_FACING

        # Are we on the ground?
        is_on_ground = physics_engine.is_on_ground(self)

        # Are we on a ladder?
        if len(arcade.check_for_collision_with_list(self, self.ladder_list)) > 0:
            if not self.is_on_ladder:
                self.is_on_ladder = True
                self.pymunk.gravity = (0, 0)
                self.pymunk.damping = 0.0001
                self.pymunk.max_vertical_velocity = PLAYER_MAX_HORIZONTAL_SPEED
        else:
            if self.is_on_ladder:
                self.pymunk.damping = 1.0
                self.pymunk.max_vertical_velocity = PLAYER_MAX_VERTICAL_SPEED
                self.is_on_ladder = False
                self.pymunk.gravity = None

        # Add to the odometer how far we've moved
        self.x_odometer += dx
        self.y_odometer += dy

        if self.is_on_ladder and not is_on_ground:
            # Have we moved far enough to change the texture?
            if abs(self.y_odometer) > DISTANCE_TO_CHANGE_TEXTURE:

                # Reset the odometer
                self.y_odometer = 0

                # Advance the walking animation
                self.cur_texture += 1

            if self.cur_texture > 1:
                self.cur_texture = 0
            self.texture = self.climbing_textures[self.cur_texture]
            return

        # Jumping animation
        if not is_on_ground:
            if dy > DEAD_ZONE:
                self.texture = self.jump_texture_pair[self.character_face_direction]
                return
            elif dy < -DEAD_ZONE:
                self.texture = self.fall_texture_pair[self.character_face_direction]
                return

        # Idle animation
        if abs(dx) <= DEAD_ZONE:
            self.texture = self.idle_texture_pair[self.character_face_direction]
            return

        # Have we moved far enough to change the texture?
        if abs(self.x_odometer) > DISTANCE_TO_CHANGE_TEXTURE:

            # Reset the odometer
            self.x_odometer = 0

            # Advance the walking animation
            self.cur_texture += 1
            if self.cur_texture > 7:
                self.cur_texture = 0
            self.texture = self.walk_textures[self.cur_texture][self.character_face_direction]

class BulletSprite(arcade.SpriteSolidColor):
    """ Bullet Sprite """
    def pymunk_moved(self, physics_engine, dx, dy, d_angle):
        """ Handle when the sprite is moved by the physics engine. """
        # If the bullet falls below the screen, remove it
        if self.center_y < -100:
            self.remove_from_sprite_lists()


class ChordDetectorSprite(arcade.Sprite):
    """ Player Sprite """
    def __init__(self,
                 ladder_list: arcade.SpriteList,
                 hit_box_algorithm):
        """ Init """
        # Let parent initialize
        super().__init__()

        

        # Set our scale
        self.scale = SPRITE_SCALING_PLAYER

        # Images from Kenney.nl's Character pack
        
        #main_path = ":resources:images/misc/grey_128_2560_alpha_75.png"

        self.texture = CHORDDETECTOR_TEXTURE

class GameWindow(arcade.Window):
    """ Main Window """

    def __init__(self, width, height, title):
        """ Create the variables """

        # Init the parent class
        super().__init__(width, height, title, fullscreen=True)

        self.fuckingdict = dict() # writting at init time to provide frozen_fuckingdict once init finished
        self.frozen_fuckingdict = None #read acces


        #self.hit_sound = arcade.load_sound("./resources/sounds/hit4.wav")

        self.hit_sound = arcade.load_sound("./resources/sounds/A4.wav")

        self.C4_sound = arcade.load_sound("./resources/sounds/C4.wav")
        self.D4_sound = arcade.load_sound("./resources/sounds/D4.wav")
        self.E4_sound = arcade.load_sound("./resources/sounds/E4.wav")
        self.F4_sound = arcade.load_sound("./resources/sounds/F4.wav")
        self.G4_sound = arcade.load_sound("./resources/sounds/G4.wav")
        self.A4_sound = arcade.load_sound("./resources/sounds/A4.wav")
        self.B4_sound = arcade.load_sound("./resources/sounds/B4.wav")



        self.sounds_list = [self.C4_sound,self.D4_sound,self.E4_sound,self.F4_sound,self.G4_sound,self.A4_sound,self.B4_sound]


        self.chord_list = list()

        self.data_sound = None #self.sounds_list[index_sound]           
        self.my_soundplayer = None #arcade.play_sound(self.data_sound)

        self.last_fusion_virgin_list = ['']


        #............................................................

        #camera demo example vsync:
        self.set_vsync(True)

        #mouse tracker:
        self.mouse_pos = 0, 0
        #.............................................
        self.time = 0


        #*********





        # ////////////////////////////////////////////////////////////////
        self.joysticks = None
        #....................

        # Get list of game controllers that are available
        joysticks = arcade.get_joysticks()

        # If we have any...
        if joysticks:
            # Grab the first one in  the list
            self.joystick = joysticks[0]

            # Open it for input
            self.joystick.open()

            print("joystick open")

            # Push this object as a handler for joystick events.
            # Required for the on_joy* events to be called.
            self.joystick.push_handlers(self)
        else:
            # Handle if there are no joysticks.
            print("There are no joysticks, plug in a joystick and run again.")
            self.joystick = None

        # ////////////////////////////////////////////////////////////////

        self.score = 0
        self.lives = 0
        #self.inventory = set() #TypeError: unhashable type: 'set'      inventory_text_top = f"iiiiiiiiiiiiiiiiiiiii _TOP_    Inventory: {self.fuckingdict[self.inventory]}"
        
        self.inventory = str() # renomer cela car c est pu un set a cause du pb hashable en temps que clef de dico
        self.inventory = Optional[arcade.Sprite] #= None

        #self.frozen_inventory = "STR frozendict()"
        self.frozen_inventory = None

        self.master_status_png: Optional[arcade.Sprite] = None
        #self.master_status_name: str()

        # Player sprite
        self.player_sprite: Optional[PlayerSprite] = None
        self.chorddetector_sprite: Optional[ChordDetectorSprite] = None

        # Sprite lists we need
        self.player_list: Optional[arcade.SpriteList] = None
        self.chorddetector_list: Optional[arcade.SpriteList] = None

        self.wall_list: Optional[arcade.SpriteList] = None
        self.bullet_list: Optional[arcade.SpriteList] = None
        
        self.ladder_list: Optional[arcade.SpriteList] = None


        self.startposition_list: Optional[arcade.SpriteList] = None

        # Track the current state of what key is pressed
        self.left_pressed: bool = False
        self.right_pressed: bool = False
        self.up_pressed: bool = False
        self.down_pressed: bool = False

        # Physics engine
        self.physics_engine = Optional[arcade.PymunkPhysicsEngine]

        # Set background color
        arcade.set_background_color(arcade.color.AMAZON)



    def crash_debug(self, msg):
        print("\n\n\n...................   crash_debug   .............")
        print(msg)
        print("\n\n\n_________________________________________________")

        assert False

    def fill_fuckingdict(self):

        NB_TEXTURES_IN_INIT_TEXTURES_LAYER = 7
        nb_tex_plus_one = NB_TEXTURES_IN_INIT_TEXTURES_LAYER + 1

        #i = 1
        i = 0

        for tex in self.init_notes_list[i:nb_tex_plus_one]:

            mytexobj = tex.texture

            new_key_value = {mytexobj:i}

            self.fuckingdict.update(new_key_value)

            i += 1

        #fuckfuckfuck = {None:0} # j hesite entre value = none et value=0 et value=''
        #fuckfuckfuck = {None:None} # j hesite entre value = none et value=0 et value=''
        #fuckfuckfuck = {typing.Union[arcade.sprite.Sprite, NoneType]:None}
        
        #fuckfuckfuck = {Union[arcade.sprite.Sprite, NoneType]:None}


        #Union[datetime, None]

        # $$$$$

        # https://stackoverflow.com/questions/39429526/how-to-specify-nullable-return-type-with-type-hints

        fuckfuckfuck = {Union[arcade.sprite.Sprite, None]:None}

        # $$$$$

        



        self.fuckingdict.update(fuckfuckfuck)


        

    

    def setup(self):
        """ Set up everything with the game """

        self.lives = LIVES_AT_START

        # Create the sprite lists
        self.player_list = arcade.SpriteList()
        self.chorddetector_list = arcade.SpriteList()

        self.bullet_list = arcade.SpriteList()

        # Read in the tiled map

        map_name = "resources/tmx_maps/Chords_C_major_shift.tmx"

        my_map = arcade.tilemap.read_tmx(map_name)

        self.init_notes_list = arcade.tilemap.process_layer(my_map,
                                                      #'Platforms',
                                                      'init_notes_layer',
                                                      SPRITE_SCALING_TILES,
                                                      hit_box_algorithm="Detailed")

        for spt in self.init_notes_list:
            print(f"\n ini_note   {spt.texture}")


        
        self.fill_fuckingdict()

        print(f"self.fuckingdict     {self.fuckingdict}")


        #fuckingdict_with_emptystring_amorce = {'':'amorce'}
        fuckingdict_with_emptystring_amorce = {None:''}
        fuckingdict_with_emptystring_amorce.update(self.fuckingdict)
        print(f"fuckingdict_with_emptystring_amorce = {fuckingdict_with_emptystring_amorce}")        
        self.frozen_fuckingdict = frozendict(fuckingdict_with_emptystring_amorce)

        print(self.frozen_fuckingdict)

        

        #self.crash_debug("GRAAL")

        

        # Read in the map layers
        self.wall_list = arcade.tilemap.process_layer(my_map,
                                                      #'Platforms',
                                                      'notes_layer',
                                                      SPRITE_SCALING_TILES,
                                                      hit_box_algorithm="Detailed")

        for spt in self.wall_list:
            print(f"\n wall_note   {spt.texture}")


        self.interlines_list = arcade.tilemap.process_layer(my_map,
                                                      #'Platforms',
                                                      'interlines_layer',
                                                      SPRITE_SCALING_TILES,
                                                      hit_box_algorithm="Detailed")
        

        


        self.ladder_list = arcade.tilemap.process_layer(my_map,
                                                        'ladders',
                                                        SPRITE_SCALING_TILES,
                                                        use_spatial_hash=True,
                                                        hit_box_algorithm="Detailed")

               

        

        startposition_layer_name = 'Startposition'

        self.startposition_list = arcade.tilemap.process_layer(map_object=my_map,
                                                      layer_name=startposition_layer_name,
                                                      scaling=TILE_SCALING,
                                                      use_spatial_hash=True)

        start_XY = tuple((self.startposition_list[0].center_x,self.startposition_list[0].center_y))




        # Create player sprite
        self.player_sprite = PlayerSprite(self.ladder_list, hit_box_algorithm="Detailed")




        self.player_sprite.center_x = start_XY[0]
        self.player_sprite.center_y = start_XY[1]

        # Add to player sprite list
        self.player_list.append(self.player_sprite)

        self.chorddetector_sprite = ChordDetectorSprite(self.ladder_list, hit_box_algorithm="Detailed")

        self.chorddetector_sprite.center_x = start_XY[0] + CHORDDETECTOR_CENTER_PIXEL_SHIFT
        self.chorddetector_sprite.center_y = start_XY[1]

        self.chorddetector_list.append(self.chorddetector_sprite) 

        

        # Moving Sprite
        self.autonom_moving_sprites_list = arcade.tilemap.process_layer(my_map,
                                                                'Moving Platforms',
                                                                SPRITE_SCALING_TILES)

        # --- Pymunk Physics Engine Setup ---

        # The default damping for every object controls the percent of velocity
        # the object will keep each second. A value of 1.0 is no speed loss,
        # 0.9 is 10% per second, 0.1 is 90% per second.
        # For top-down games, this is basically the friction for moving objects.
        # For platformers with gravity, this should probably be set to 1.0.
        # Default value is 1.0 if not specified.
        damping = DEFAULT_DAMPING

        # Set the gravity. (0, 0) is good for outer space and top-down.
        gravity = (0, -GRAVITY)

        # Create the physics engine
        self.physics_engine = arcade.PymunkPhysicsEngine(damping=damping,
                                                         gravity=gravity)

        def wall_hit_handler(bullet_sprite, _wall_sprite, _arbiter, _space, _data): # BBBBUUUUUUUULLLLLLLLLLLEEEEEEEEETTTTTTTTT
            """ Called for bullet/wall collision """
            #arcade.play_sound(self.hit_sound)



            _wall_sprite.guid = _wall_sprite.texture
            #self.inventory = str(_wall_sprite.guid)
            self.inventory = _wall_sprite.guid

            self.frozen_inventory = self.fuckingdict[self.inventory]
            bullet_sprite.remove_from_sprite_lists()


            index_sound = self.frozen_fuckingdict[self.inventory]

            #arcade.play_sound(self.sounds_list[index_sound])


            self.data_sound = self.sounds_list[index_sound]

            #self.my_soundplayer = arcade.play_sound(self.sounds_list[index_sound])
            self.my_soundplayer = arcade.play_sound(self.data_sound)


            for snd in self.sounds_list:
                print(snd)



        self.physics_engine.add_collision_handler("bullet", "wall", post_handler=wall_hit_handler)




        def init_notes_hit_handler(bullet_sprite, _init_notes_sprite, _arbiter, _space, _data):
            """ Called for bullet/wall collision """
            arcade.play_sound(self.hit_sound)
            bullet_sprite.remove_from_sprite_lists()

            _init_notes_sprite.guid = _init_notes_sprite.texture
            #self.inventory = str(_init_notes_sprite.guid)
            self.inventory = _init_notes_sprite.guid

            self.frozen_inventory = self.fuckingdict[self.inventory]


            

        self.physics_engine.add_collision_handler("bullet", "init_notes", post_handler=init_notes_hit_handler)



        def item_hit_handler(bullet_sprite, item_sprite, _arbiter, _space, _data):
            """ Called for bullet/wall collision """
            bullet_sprite.remove_from_sprite_lists()
            item_sprite.remove_from_sprite_lists()

        self.physics_engine.add_collision_handler("bullet", "item", post_handler=item_hit_handler)




        # Add the player.
        # For the player, we set the damping to a lower value, which increases
        # the damping rate. This prevents the character from traveling too far
        # after the player lets off the movement keys.
        # Setting the moment to PymunkPhysicsEngine.MOMENT_INF prevents it from
        # rotating.
        # Friction normally goes between 0 (no friction) and 1.0 (high friction)
        # Friction is between two objects in contact. It is important to remember
        # in top-down games that friction moving along the 'floor' is controlled
        # by damping.
        self.physics_engine.add_sprite(self.player_sprite,
                                       friction=PLAYER_FRICTION,
                                       mass=PLAYER_MASS,
                                       moment=arcade.PymunkPhysicsEngine.MOMENT_INF,
                                       collision_type="player",
                                       max_horizontal_velocity=PLAYER_MAX_HORIZONTAL_SPEED,
                                       max_vertical_velocity=PLAYER_MAX_VERTICAL_SPEED)

        # Create the walls.
        # By setting the body type to PymunkPhysicsEngine.STATIC the walls can't
        # move.
        # Movable objects that respond to forces are PymunkPhysicsEngine.DYNAMIC
        # PymunkPhysicsEngine.KINEMATIC objects will move, but are assumed to be
        # repositioned by code and don't respond to physics forces.
        # Dynamic is default.

        self.physics_engine.add_sprite_list(self.init_notes_list,
                                            friction=WALL_FRICTION,
                                            collision_type="init_notes",
                                            body_type=arcade.PymunkPhysicsEngine.STATIC)

        self.physics_engine.add_sprite_list(self.wall_list,
                                            friction=WALL_FRICTION,
                                            collision_type="wall",
                                            body_type=arcade.PymunkPhysicsEngine.STATIC)



        



    def spawn_player(self, continue_position= None):

        #continue are flaged position to avoid to respawn far at start level position, usefull for wide and hardcore maps

        if continue_position is None:

            self.physics_engine.remove_sprite(self.player_sprite)
            
            #self.player_sprite.remove_from_sprite_lists()
            start_XY = tuple((self.startposition_list[0].center_x,self.startposition_list[0].center_y))

             # Create player sprite
            self.player_sprite = PlayerSprite(self.ladder_list, hit_box_algorithm="Detailed")


            self.player_sprite.center_x = start_XY[0]
            self.player_sprite.center_y = start_XY[1]

            #self.player_list.append(player_sprite)

            #del self.player_list[:]
            #self.player_list.append(self.player_sprite)
            self.player_list[0] = self.player_sprite
            self.chorddetector_sprite = ChordDetectorSprite(self.ladder_list, hit_box_algorithm="Detailed")

            self.chorddetector_sprite.center_x = start_XY[0]
            self.chorddetector_sprite.center_y = start_XY[1]

            self.chorddetector_list.append(self.chorddetector_sprite) 
            
            

            self.physics_engine.add_sprite(self.player_sprite,
                                       friction=PLAYER_FRICTION,
                                       mass=PLAYER_MASS,
                                       moment=arcade.PymunkPhysicsEngine.MOMENT_INF,
                                       collision_type="player",
                                       max_horizontal_velocity=PLAYER_MAX_HORIZONTAL_SPEED,
                                       max_vertical_velocity=PLAYER_MAX_VERTICAL_SPEED)

            # Add to player sprite list
            #self.player_list.append(self.player_sprite)




    def make_midi_files_for_chords(self):

        for i in range(0,len(self.chord_list)):
            s = stream.Stream()
            
            #note_list[i].duration='whole'
            chord_root_name = [''.join(self.chord_list[i])]

            
            self.chord_list[i] = chord.Chord(self.chord_list[i])
            
            
            s.append(self.chord_list[i])

            

            fp = s.write('midi', fp=f"dirchord/{chord_root_name}.mid")






    




    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed. """

            

        if key == arcade.key.LEFT:
            self.left_pressed = True
        elif key == arcade.key.RIGHT:
            self.right_pressed = True
        elif key == arcade.key.UP:
            self.up_pressed = True
            # find out if player is standing on ground, and not on a ladder
            if self.physics_engine.is_on_ground(self.player_sprite) \
                    and not self.player_sprite.is_on_ladder:
                # She is! Go ahead and jump
                impulse = (0, PLAYER_JUMP_IMPULSE)
                self.physics_engine.apply_impulse(self.player_sprite, impulse)
        elif key == arcade.key.DOWN:
            self.down_pressed = True

        elif key == arcade.key.ESCAPE:
            raise Exception("\n\n      See You soon, fork it share it !")


        elif key == arcade.key.NUM_0:

            self.make_midi_files_for_chords()
            #raise Exception("\n\n      NUM_0 !")

    def on_key_release(self, key, modifiers):
        """Called when the user releases a key. """

        if key == arcade.key.LEFT:
            self.left_pressed = False
        elif key == arcade.key.RIGHT:
            self.right_pressed = False
        elif key == arcade.key.UP:
            self.up_pressed = False
        elif key == arcade.key.DOWN:
            self.down_pressed = False

    def on_mouse_press(self, x, y, button, modifiers):
        """ Called whenever the mouse button is clicked. """

        bullet = BulletSprite(20, 5, arcade.color.DARK_YELLOW)
        self.bullet_list.append(bullet)

        # Position the bullet at the player's current location
        start_x = self.player_sprite.center_x
        start_y = self.player_sprite.center_y
        bullet.position = self.player_sprite.position

        # Get from the mouse the destination location for the bullet
        # IMPORTANT! If you have a scrolling screen, you will also need
        # to add in self.view_bottom and self.view_left.
        dest_x, dest_y = self.mouse_coordinates_to_world(x, y)

        # Do math to calculate how to get the bullet to the destination.
        # Calculation the angle in radians between the start points
        # and end points. This is the angle the bullet will travel.
        x_diff = dest_x - start_x
        y_diff = dest_y - start_y
        angle = math.atan2(y_diff, x_diff)

        # What is the 1/2 size of this sprite, so we can figure out how far
        # away to spawn the bullet
        size = max(self.player_sprite.width, self.player_sprite.height) / 2

        # Use angle to to spawn bullet away from player in proper direction
        bullet.center_x += size * math.cos(angle)
        bullet.center_y += size * math.sin(angle)

        # Set angle of bullet
        bullet.angle = math.degrees(angle)

        # Gravity to use for the bullet
        # If we don't use custom gravity, bullet drops too fast, or we have
        # to make it go too fast.
        # Force is in relation to bullet's angle.
        bullet_gravity = (0, -BULLET_GRAVITY)

        # Add the sprite. This needs to be done AFTER setting the fields above.
        self.physics_engine.add_sprite(bullet,
                                       mass=BULLET_MASS,
                                       damping=1.0,
                                       friction=0.6,
                                       collision_type="bullet",
                                       gravity=bullet_gravity,
                                       elasticity=0.9)

        # Add force to bullet
        force = (BULLET_MOVE_FORCE, 0)
        self.physics_engine.apply_force(bullet, force)


    def on_mouse_motion(self, x, y, dx, dy):
        self.mouse_pos = x, y


    # noinspection PyMethodMayBeStatic
    def on_joybutton_press(self, _joystick, button):
        """ Handle button-down event for the joystick """
        print("Button {} down".format(button))
        if button == JUMPBTN:




            if self.physics_engine.is_on_ground(self.player_sprite) and not self.player_sprite.is_on_ladder:


                # She is! Go ahead and jump
                impulse = (0, PLAYER_JUMP_IMPULSE)
                self.physics_engine.apply_impulse(self.player_sprite, impulse)


    def on_update(self, delta_time):

        #
        #
        #
        


        self.chorddetector_list[0].center_x = self.player_list[0].center_x + CHORDDETECTOR_CENTER_PIXEL_SHIFT
        self.chorddetector_list[0].center_y = self.player_list[0].center_y


        chorddetector_cross_chords_list = arcade.check_for_collision_with_list(self.chorddetector_list[0], self.wall_list)
        for bidul in chorddetector_cross_chords_list:
            print(f" $$$$$$  bidul.texture  {bidul.texture}   bidul.texture.ident {self.frozen_fuckingdict[bidul.texture]}")

            #arcade.play_sound(self.sounds_list[self.frozen_fuckingdict[bidul.texture]])


        print("~~~~~~~~~~~~~~~~ 1 ~~~~~~~~~~~~~~~~~~~~~")


        list_1 = chorddetector_cross_chords_list
        print(list_1)

        list_2 = list(dict.fromkeys(list_1))

        
        print(list_2)

        print("~~~~~~~~~~~~~~~~~ 2 ~~~~~~~~~~~~~~~~~~~~")
        list_3 = list(OrderedDict.fromkeys(list_1))

        print(list_3)

        print("~~~~~~~~~~~~~~~~~ 3 ~~~~~~~~~~~~~~~~~~~~")


        new_list = sorted(chorddetector_cross_chords_list, key=operator.attrgetter("center_y")) # ordre de hauteur est important car si renversement un ou deux

        #no_duplicata_list = list(OrderedDict.fromkeys(new_list))  ??

        no_duplicata_list = list(dict.fromkeys(new_list))

        virgin_list = list()

        for sortedchord in no_duplicata_list:
            ident = self.frozen_fuckingdict[sortedchord.texture]
            anglosax = INDEX_TO_INTERNATIONAL[ident]
            fr = INDEX_TO_FR[ident]

            print(f"   sortedchord.texture  {sortedchord.texture}  ___ id  {id(sortedchord.texture)} >>>>>     sortedchord.texture.ident {ident}   <<< {anglosax}  <=> {fr}   ")

            if anglosax not in virgin_list:
                virgin_list.append(anglosax)

        print(f" \n ...  virgin_list     {virgin_list}")

        #for virg in virgin_list:
        #    virg += '4'

        #print(f" \n ...  virgin_list+4     {virgin_list}")

        #four = [virg for (virg+='4' in virgin_list)]
        #print(f"four = {four}")

        virgin_4_list = list()

        for i in range(0,len(virgin_list)):
            #virgin_4_list[i] = (virgin_list[i] += '4')
            virgin_list[i] += '4'

        #print(f" \n ...  virgin_4_list    {virgin_4_list}")
        print(f" \n ...  virgin_list     {virgin_list}")


        fusion_virgin_list = [''.join(virgin_list[:])]

        print(f" \n ...  fusion_virgin_list     {fusion_virgin_list}")

        if not virgin_list in self.chord_list:
            if len(virgin_list) >2:
                self.chord_list.append(virgin_list)


        for chord in self.chord_list:
            print(f" \n $  {chord}")



        






        #arcade.play_sound(self.sounds_list[self.frozen_fuckingdict[bidul.texture]])

        #self.datamusic =

        #self.soun

        #~~~~~~~~~~~~~~~~

        #self.data_sound = self.sounds_list[index_sound]

        if fusion_virgin_list == ['']:
            fusion_virgin_list = ['C4']


        sound_path = SOUND_PATH + fusion_virgin_list[0] + ".wav"

        print(f"sound_path  {sound_path}")

        if self.last_fusion_virgin_list != fusion_virgin_list:

            try:
                self.data_sound = arcade.load_sound(sound_path)
                print(f"self.data_sound  {self.data_sound}")
                self.my_soundplayer = arcade.play_sound(self.data_sound)
            except:
                pass


            self.last_fusion_virgin_list = fusion_virgin_list







      


        if self.joystick:

            #print(self.joystick.x)
            #print(f"joystick   {self.joystick.x}  {self.joystick.y}")


            #MOVEMENT_SPEED = 1000

            # x-axis
            #self.change_x = self.joystick.x * MOVEMENT_SPEED
            # Set a "dead zone" to prevent drive from a centered joystick
            #if abs(self.change_x) > DEAD_ZONE:
            #    self.change_x = 0
            #    print("DZ")

            
        

            



            if self.joystick.x < -0.3: #and not self.right_pressed:
                # Create a force to the left. Apply it.

                #if is_on_ground or self.player_sprite.is_on_ladder:
                if self.physics_engine.is_on_ground(self.player_sprite):# or self.player_sprite.is_on_ladder:

                    force = (-PLAYER_MOVE_FORCE_ON_GROUND, 0)
                else:
                    force = (-PLAYER_MOVE_FORCE_IN_AIR, 0)
                self.physics_engine.apply_force(self.player_sprite, force)
                # Set friction to zero for the player while moving
                self.physics_engine.set_friction(self.player_sprite, 0)
            elif self.joystick.x > 0.3: #and not self.left_pressed:
                # Create a force to the right. Apply it.
                if self.physics_engine.is_on_ground(self.player_sprite):# or self.player_sprite.is_on_ladder:
                    force = (PLAYER_MOVE_FORCE_ON_GROUND, 0)
                else:
                    force = (PLAYER_MOVE_FORCE_IN_AIR, 0)
                self.physics_engine.apply_force(self.player_sprite, force)
                # Set friction to zero for the player while moving
                self.physics_engine.set_friction(self.player_sprite, 0)


            #if self.player_sprite.is_on_ladder:
            if self.player_sprite.is_on_ladder:
            


                if self.joystick.y > 0.3:
                    
                    force = (0, -PLAYER_MOVE_FORCE_ON_GROUND)
                    self.physics_engine.apply_force(self.player_sprite, force)
                    # Set friction to zero for the player while moving
                    self.physics_engine.set_friction(self.player_sprite, 0)

                elif self.joystick.y < -0.3:
                    
                    force = (0, PLAYER_MOVE_FORCE_ON_GROUND)
                    self.physics_engine.apply_force(self.player_sprite, force)
                    # Set friction to zero for the player while moving
                    self.physics_engine.set_friction(self.player_sprite, 0)


        # /////////////////////////////////////////////////////////////////////////





        # Update player forces based on keys pressed
        if self.left_pressed and not self.right_pressed:
            # Create a force to the left. Apply it.
            if self.physics_engine.is_on_ground(self.player_sprite) or self.player_sprite.is_on_ladder:
                force = (-PLAYER_MOVE_FORCE_ON_GROUND, 0)
            else:
                force = (-PLAYER_MOVE_FORCE_IN_AIR, 0)
            self.physics_engine.apply_force(self.player_sprite, force)
            # Set friction to zero for the player while moving
            self.physics_engine.set_friction(self.player_sprite, 0)
        elif self.right_pressed and not self.left_pressed:
            # Create a force to the right. Apply it.
            

            #if self.player_sprite.is_on_ground or self.player_sprite.is_on_ladder:
            #if self.player_sprite.is_on_ground or self.player_sprite.is_on_ladder:
            if self.physics_engine.is_on_ground(self.player_sprite):
            
                force = (PLAYER_MOVE_FORCE_ON_GROUND, 0)
            else:
                force = (PLAYER_MOVE_FORCE_IN_AIR, 0)
            self.physics_engine.apply_force(self.player_sprite, force)
            # Set friction to zero for the player while moving
            self.physics_engine.set_friction(self.player_sprite, 0)
        elif self.up_pressed and not self.down_pressed:
            # Create a force to the right. Apply it.
            if self.player_sprite.is_on_ladder:
                force = (0, PLAYER_MOVE_FORCE_ON_GROUND)
                self.physics_engine.apply_force(self.player_sprite, force)
                # Set friction to zero for the player while moving
                self.physics_engine.set_friction(self.player_sprite, 0)
        elif self.down_pressed and not self.up_pressed:
            # Create a force to the right. Apply it.
            if self.player_sprite.is_on_ladder:
                force = (0, -PLAYER_MOVE_FORCE_ON_GROUND)
                self.physics_engine.apply_force(self.player_sprite, force)
                # Set friction to zero for the player while moving
                self.physics_engine.set_friction(self.player_sprite, 0)



        else:
            # Player's feet are not moving. Therefore up the friction so we stop.
            self.physics_engine.set_friction(self.player_sprite, 1.0)

        

        


        # Move items in the physics engine
        self.physics_engine.step()
        #-------------------------------------------------------------------------------------- * * * * *

        
        

    def center_on_player(self):
        w_width, w_height = self.get_size()
        arcade.set_viewport(
        self.player_sprite.center_x - w_width // 2,
        self.player_sprite.center_x + w_width // 2,
        self.player_sprite.center_y - w_height // 2,
        self.player_sprite.center_y + w_height // 2,
    )

    def mouse_coordinates_to_world(self, x, y):
        """
        Calculates in game position of mouse
        """
        w_width, w_height = self.get_size()
        left, right, bottom, top = self.get_viewport()

        x = left + (right - left) * x / w_width
        y = bottom + (top - bottom) * y / w_height

        return x, y
        
    def on_draw(self):
        """ Draw everything """
        arcade.start_render()
        self.center_on_player()

        score_text = f"$$$$$$$$$$$$$$$$    Score: {self.score}"
        #arcade.draw_text(score_text, 10 + SCORE_XOFFSET, 10 + SCORE_YOFFSET,
        #                 arcade.csscolor.YELLOW, 18)


        arcade.draw_text(score_text, 50, 500, arcade.csscolor.RED, 25)


        inventory_text = f"iiiiiiiiiiiiiiiiiiiiiiiiiiiii    Inventory: {self.inventory}"

        #arcade.draw_text(inventory_text, 80, 1700, arcade.csscolor.YELLOW, 30)
        arcade.draw_text(inventory_text, 80, 200, arcade.csscolor.YELLOW, 30)



        print(f"\n\n self.frozen_fuckingdict      {self.frozen_fuckingdict}")

        print(f"\n\n self.inventory      {self.inventory}       type(self.inventory)  {type(self.inventory)} ")


        str_self_inventory = str(self.inventory)
        #inventory_text_top = f"iiiiiiiiiiiiiiiiiiiii _TOP_    Inventory: {self.frozen_fuckingdict[str_self_inventory]}"
        inventory_text_top = f"iiiiiiiiiiiiiiiiiiiii _TOP_    Inventory: {self.frozen_fuckingdict[self.inventory]}"


        


        arcade.draw_text(inventory_text_top, -100, 1200, arcade.csscolor.RED, 20)
        arcade.draw_text(inventory_text_top, 80, 300, arcade.csscolor.RED, 20)


        inventory_text_up = f"iiiiiiiiiiiiiiiiiiiii _up_    Inventory: {self.inventory}"
        arcade.draw_text(inventory_text_up, -100, 1100, arcade.csscolor.BLUE, 20)


        inventory_text_centers = f"____     inventory_text_centers   Inventory: {self.inventory}"
        arcade.draw_text(inventory_text_centers, -100, 1000, arcade.csscolor.WHITE, 20)






        self.init_notes_list.draw()


        self.wall_list.draw()
        self.interlines_list.draw()

        
        self.ladder_list.draw()
        self.bullet_list.draw()

        self.player_list.draw()

        self.chorddetector_list.draw()

        




        

        # for item in self.player_list:
        #     item.draw_hit_box(arcade.color.RED)
        # for item in self.coins_list:
        #     item.draw_hit_box(arcade.color.RED)

        #____________________
        world_pos = self.mouse_coordinates_to_world(*self.mouse_pos)
        arcade.draw_circle_filled(*world_pos, 10, arcade.color.BLUE)

        

def main():
    """ Main method """
    window = GameWindow(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
