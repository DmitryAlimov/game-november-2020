import pygame
import numpy as np
import time
import random
from os import path


#parameters===========================================================================================================#
WIDTH = 1000
HEIGHT = 1000
FPS = 30
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
CUSTOM_COLOR = (0, 0, 50)
#=====================================================================================================================#


#classes==============================================================================================================#
class Text:
    def __init__(self, line_max, width, size, color, x, y):
        self.arr = []
        self.line_start = 0
        self.line_max = line_max
        self.width = width
        self.font = pygame.font.SysFont('urwbookman', size)
        self.x = x
        self.y = y
        self.color = color
    def clear(self):
        self.line_start = 0
        while (len(self.arr) > 0):
            del self.arr[0]
    def add_line(self, str_inp):
        split = str_inp.split()
        if (len(split) != len(str_inp)) and (len(str_inp) > self.width):
            rb = ""
            for q in range(len(split)):
                if len(rb) < self.width:
                    rb = rb + split[q] + " "
                else:
                    self.arr.append(rb)
                    rb = split[q] + " "
            self.arr.append(rb)
        else:
            self.arr.append(str_inp)
    def out(self):
        for q in range(self.line_max):
            if self.line_start + q < len(self.arr):
                text = self.font.render(self.arr[self.line_start + q], True, self.color)
                screen.blit(text, [self.x, self.y + q*25])
    def out_hor(self):
        for q in range(self.line_max - self.line_start):
            if self.line_start + q < len(self.arr):
                text = self.font.render(self.arr[self.line_start + q], True, self.color)
                screen.blit(text, [self.x + q*WIDTH/5, self.y])
    def corr(self):
        if (len(self.arr) - self.line_max > 0):
            self.line_start = len(self.arr) - self.line_max


class ObjList:
    def __init__(self):
        self.arr = []
    def add(self, obj_inp):
        self.arr.append(obj_inp)
    def delete(self, str_inp):
        if len(self.arr) > 0:
            for qq in range(len(self.arr)):
                if qq < len(self.arr):
                    if self.arr[qq] == str_inp:
                        del self.arr[qq]
    def len(self):
        return len(self.arr)
    def getCreature(self, inp):
        for q in range(len(self.arr)):
            if self.arr[q].title == inp:
                break
        outp = Creature(title=self.arr[q].title, type=self.arr[q].type, min_lvl=self.arr[q].min_lvl, HP=self.arr[q].HP, defence=self.arr[q].defence, damage=self.arr[q].damage, special_effect=self.arr[q].special_effect, final_effect=self.arr[q].final_effect, imagename=self.arr[q].imagename, image_scale_x=self.arr[q].image_scale_x, image_scale_y=self.arr[q].image_scale_y, description=self.arr[q].description)
        return outp
    def getLocation(self, inp):
        for q in range(len(self.arr)):
            if self.arr[q].title == inp:
                break
        outp = Location(title=self.arr[q].title, special_effect=self.arr[q].special_effect, imagename=self.arr[q].imagename, description=self.arr[q].description)
        for w in range(self.arr[q].actions.len()):
            outp.actions.add(self.arr[q].actions.arr[w])
        for w in range(self.arr[q].move_idx.len()):
            outp.move_idx.add(self.arr[q].move_idx.arr[w])
        for w in range(self.arr[q].trade_idx.len()):
            outp.trade_idx.add(self.arr[q].trade_idx.arr[w])
        for w in range(self.arr[q].guard_idx.len()):
            outp.guard_idx.add(self.arr[q].guard_idx.arr[w])
        return outp
    def getThing(self, inp):
        for q in range(len(self.arr)):
            if self.arr[q].title == inp:
                break
        outp =  Thing(title=self.arr[q].title, type=self.arr[q].type, min_lvl=self.arr[q].min_lvl, max_lvl=self.arr[q].max_lvl, cost=self.arr[q].cost, manacost=self.arr[q].manacost, dist_defence_effect=self.arr[q].dist_defence_effect, comb_defence_effect=self.arr[q].comb_defence_effect, dist_damage_effect=self.arr[q].dist_damage_effect, comb_damage_effect=self.arr[q].comb_damage_effect, HP_effect=self.arr[q].HP_effect, mana_effect=self.arr[q].mana_effect, luck_effect=self.arr[q].luck_effect, imagename=self.arr[q].imagename, special_effect=self.arr[q].special_effect, passive_effect=self.arr[q].passive_effect, image_scale_x=self.arr[q].image_scale_x, image_scale_y=self.arr[q].image_scale_y, description=self.arr[q].description)
        return outp
    def get_ptr(self, inp):
        return self.arr[inp]
    def out(self):
        for q in range(len(self.arr)):
            TextMain.add_line(str(q) + " " + self.arr[q])
        update_graphics()
    def out_title(self):
        for q in range(len(self.arr)):
            TextMain.add_line(str(q) + " " + self.arr[q].title)
        update_graphics()
    def clear(self):
        self.arr = []
    def get_ind(self, inp):
        for q in range(len(self.arr)):
            if self.arr[q].title == inp:
                return q

class Hero:
    def __init__(self, name, imagename, loc):
        self.inventory = ObjList()
        self.actions = ObjList()
        self.name = name
        self.EXP = 0
        self.loc = loc
        self.level = 1
        self.HP = 100
        self.HP_max = 100
        self.money = 100
        self.mana = 100
        self.mana_max = 100
        self.dist_damage = 0
        self.comb_damage = 10
        self.dist_defence = 1
        self.comb_defence = 1
        self.luck = 30
        self.coex_start = np.zeros(3)
        self.coex = np.zeros(3)
        self.inventory_save = ObjList()
        self.loc_save = ""
        self.HP_max_save = 0
        self.mana_max_save = 0
        self.comb_damage_save = 0
        self.dist_damage_save = 0
        self.comb_defence_save = 0
        self.dist_defence_save = 0
        self.imagename = imagename
        self.image = pygame.image.load(imagename)
        self.image = pygame.transform.scale(self.image, (70, 70))
    def draw(self, x, y):
        rect = self.image.get_rect(center=(x, y))
        screen.blit(self.image, rect)
    def add_invent(self, inp):
        thing = Things.getThing(inp)
        if (thing.type != "ban") and (thing.type != "special"):
            if thing.min_lvl > self.level or thing.max_lvl < self.level:
                return -1
            if thing.cost > self.money:
                return -1
            if thing.manacost > self.mana:
                return -1
        self.money = self.money - thing.cost
        self.mana = self.mana - thing.manacost
        self.comb_defence = self.comb_defence + thing.comb_defence_effect
        self.dist_defence = self.dist_defence + thing.dist_defence_effect
        self.comb_damage = self.comb_damage + thing.comb_damage_effect
        self.dist_damage = self.dist_damage + thing.dist_damage_effect
        self.HP_max = self.HP_max + thing.HP_effect
        self.mana_max = self.HP_max + thing.mana_effect
        self.luck = self.luck + thing.luck_effect
        self.inventory.add(inp)
        return 1
    def find_invent(self, inp):
        for q in range (len(self.inventory.arr)):
            if (self.inventory.arr[q] == inp):
                return 1
        return -1
    def modify_invent(self, thing, mod):
        for q in range(len(self.inventory.arr)):
            if (self.inventory.arr[q] == thing):
                break
        if (q < self.inventory.len()):
            modified_thing = Things.getThing(self.inventory.arr[q])

            '''modification'''
            modified_thing.title = modified_thing.title + " " + mod
            if mod == "red":
                modified_thing.comb_damage_effect = modified_thing.comb_damage_effect + 5
            '''modification'''

            Things.arr.append(modified_thing)
            self.money = self.money + modified_thing.cost
            self.remove_invent(thing, "const")
            if self.add_invent(modified_thing.title) == -1:
                self.add_invent(thing)
                TextMain.add_line('modification failed')
                TextMain_out()
    def remove_invent(self, inp, time_type):
        if time_type == "const":
            for q in range (len(self.inventory.arr)):
                if (self.inventory.arr[q] == inp):
                    break
            thing = Things.getThing(inp)
            if (thing.type == "ban") or (thing.type == "special"):
                return -1
            self.comb_defence = self.comb_defence - thing.comb_defence_effect
            self.dist_defence = self.dist_defence - thing.dist_defence_effect
            self.comb_damage = self.comb_damage - thing.comb_damage_effect
            self.dist_damage = self.comb_damage - thing.comb_damage_effect
            self.HP_max = self.HP_max - thing.HP_effect
            self.mana_max = self.HP_max - thing.mana_effect
            self.luck = self.luck - thing.luck_effect
            self.inventory.delete(thing.title)
            self.inventory_save.delete(thing.title)
            return 1
        if time_type == "tmp":
            for q in range (len(self.inventory.arr)):
                if (self.inventory.arr[q] == inp):
                    break
            self.inventory.delete(inp)
            return 1
    def send_invent(self, inp, to_whoom):
        if h_coex_num() > 1:
            for q in range(len(self.inventory.arr)):
                if (self.inventory.arr[q] == inp):
                    break
            if q < len(self.inventory.arr):
                thing = Things.getThing(self.inventory.arr[q])
                Heroes[to_whoom].money = Heroes[to_whoom].money + thing.cost
                if Heroes[to_whoom].add_invent(inp) == 1:
                    self.remove_invent(inp, "const")
                else:
                    Heroes[to_whoom].money = Heroes[to_whoom].money - thing.cost
        else:
            TextMain.add_line("no Heroes")
            TextMain_out()
    def choose_invent(self):
        TextMain.add_line("----0 back")
        update_graphics()
        if self.inventory.len() > 0:
            for q in range(self.inventory.len()):
                TextMain.add_line("----" + str(q + 1))
                Things.getThing(self.inventory.arr[q - 1].title).info()
            TextMain_out()
            ch = choose(len(self.inventory.arr) + 1) - 1
            return ch
        return -1
    def use_invent(self):
        TextMain.add_line("")
        TextMain.add_line("----0 back")
        update_graphics()
        for q in range(len(self.inventory.arr)):
            TextMain.add_line("----" + str(q + 1))
            Things.getThing(self.inventory.arr[q].title).info()
        update_graphics()
        ch = choose(len(self.inventory.arr) + 1)
        if ch > 0:
            inp_thing = Things.getThing(self.inventory.arr[ch - 1].title)
            if self.mana > inp_thing.manacost:
                self.mana = self.mana - inp_thing.manacost
                action(inp_thing.special_effect, '')
    def save_parameters(self):
        self.inventory_save.clear()
        for q in range(self.inventory.len()):
            self.inventory_save.add(self.inventory.arr[q])
        self.loc_save = self.loc
        self.HP_max_save = self.HP_max
        self.mana_max_save = self.mana_max
        self.comb_damage_save = self.comb_damage
        self.dist_damage_save = self.dist_damage
        self.comb_defence_save = self.comb_defence
        self.dist_defence_save = self.dist_defence
    def load_parameters(self):
        self.inventory.clear()
        for q in range(self.inventory_save.len()):
            self.inventory.add(self.inventory_save.arr[q])
        self.loc = self.loc_save
        self.HP_max = self.HP_max_save
        self.mana_max = self.mana_max_save
        self.comb_damage = self.comb_damage_save
        self.dist_damage = self.dist_damage_save
        self.comb_defence = self.comb_defence_save
        self.dist_defence = self.dist_defence_save
    def atack(self):
        TextMain.add_line("")
        dmg = int(self.comb_damage*rand() - Enemies.arr[Enemy].defence)
        if dmg < 1:
            dmg = 1
        Enemies.arr[Enemy].HP = Enemies.arr[Enemy].HP - dmg
        TextMain.add_line(self.name + " atacks: " + str(dmg) + " damage")
        dmg = Creatures.getCreature(Enemy).damage - self.comb_defence
        if dmg < 1:
            dmg = 1
        self.HP = self.HP - dmg
        TextMain.add_line("you get: " + str(dmg) + " damage back")
        TextMain.corr()
        update_graphics()
        time.sleep(2)
    def lvl_up(self):
        TextMain.add_line(self.name + " lvl up")
        self.level = self.level + 1
        cnt_arrs = []
        type_arrs = []
        for w in range(4):
            cnt = 0
            cnt_arr = []
            type_arr = []
            for q in range(4):
                type_arr.append(random.randint(0, 8))
                if cnt < 4:
                    cnt_arr.append(1)
                    cnt = cnt + 1
                    if (cnt < 4) and (random.random() < 0.5):
                        cnt_arr[q] = cnt_arr[q] + 1
                        cnt = cnt + 1
                        if (cnt < 4) and (random.random() < 0.5):
                            cnt_arr[q] = cnt_arr[q] + 1
                            cnt = cnt + 1
            cnt_arrs.append(cnt_arr)
            type_arrs.append(type_arr)
            str_out = str(w) + " "

            for q in range(len(cnt_arr)):
                if cnt_arr[q] > 0:
                    str_out = str_out + " +"
                    if type_arr[q] == 0:
                        str_out = str_out + str(cnt_arr[q] * 5) + " " + "HP max"
                    if type_arr[q] == 1:
                        str_out = str_out + str(cnt_arr[q] * 5) + " " + "mana max"
                    if type_arr[q] == 2:
                        str_out = str_out + str(cnt_arr[q]) + " " + "comb damage"
                    if type_arr[q] == 3:
                        str_out = str_out + str(cnt_arr[q]) + " " + "dist damage"
                    if type_arr[q] == 4:
                        str_out = str_out + str(cnt_arr[q]) + " " + "comb defence"
                    if type_arr[q] == 5:
                        str_out = str_out + str(cnt_arr[q]) + " " + "distant defence"
                    if type_arr[q] == 6:
                        str_out = str_out + str(cnt_arr[q]) + " " + "luck"
                    if type_arr[q] == 7:
                        str_out = str_out + str(Heroes[h_curr].mana_max - Heroes[h_curr].mana) + " " + "mana"
                    if type_arr[q] == 8:
                        str_out = str_out + str(Heroes[h_curr].HP_max - Heroes[h_curr].HP) + " " + "HP"
                    str_out = str_out  + ";"
            TextMain.add_line("")
            TextMain.add_line(str_out)
        update_graphics()

        ch = choose(4)
        for q in range(len(cnt_arrs[ch])):
            if type_arrs[ch][q] == 0:
                Heroes[h_curr].HP_max = Heroes[h_curr].HP_max + 5*cnt_arrs[ch][q]
            if type_arrs[ch][q] == 1:
                Heroes[h_curr].mana_max = Heroes[h_curr].mana_max + 5*cnt_arrs[ch][q]
            if type_arrs[ch][q] == 2:
                Heroes[h_curr].comb_damage = Heroes[h_curr].comb_damage + cnt_arrs[ch][q]
            if type_arrs[ch][q] == 3:
                Heroes[h_curr].dist_damage = Heroes[h_curr].dist_damage + cnt_arrs[ch][q]
            if type_arrs[ch][q] == 4:
                Heroes[h_curr].comb_defence = Heroes[h_curr].comb_defence + cnt_arrs[ch][q]
            if type_arrs[ch][q] == 5:
                Heroes[h_curr].dist_defence = Heroes[h_curr].dist_defence + cnt_arrs[ch][q]
            if type_arrs[ch][q] == 6:
                Heroes[h_curr].luck = Heroes[h_curr].luck + cnt_arrs[ch][q]
            if type_arrs[ch][q] == 7:
                Heroes[h_curr].mana = Heroes[h_curr].mana_max
            if type_arrs[ch][q] == 8:
                Heroes[h_curr].comb_damage = Heroes[h_curr].HP_max
        update_graphics()




class Creature:
    def __init__(self, title, type,  HP, defence, damage, min_lvl, special_effect, final_effect, imagename, image_scale_x, image_scale_y, description):
        self.title = title
        self.type = type
        self.HP = HP
        self.defence = defence
        self.damage = damage
        self.damage = damage
        self.min_lvl = min_lvl
        self.special_effect = special_effect
        self.final_effect = final_effect
        self.imagename = imagename
        self.image_scale_x = image_scale_x
        self.image_scale_y = image_scale_y
        self.image = pygame.image.load(imagename)
        self.image = pygame.transform.scale(self.image, (image_scale_x, image_scale_y))
        self.description = description
    def draw(self, x, y):
        rect = self.image.get_rect(center=(x, y))
        screen.blit(self.image, rect)
    def info(self):
        TextMain.add_line(str(self.title) + " " + str(self.HP) + " " + str(self.defence) + " " + str(self.damage) + " " + str(self.special_effect))
        TextMain.add_line(self.description)
    def info_ent(self):
        TextEnemies.add_line(
            str(self.title) + " " + str(self.HP) + " " + str(self.defence) + " " + str(self.damage) + " " + str(
                self.special_effect))
        TextEnemies.add_line(self.description)
        TextEnemies.add_line("")
    def atack_comb(self, h):
        dmg = int(self.damage * rand() - Heroes[h].comb_defence)
        if dmg < 1:
            dmg = 1
        Heroes[h].HP = Heroes[h].HP - dmg
        TextMain.add_line(self.title + " atacks: " + str(dmg) + " damage")
        dmg = int(Heroes[h].comb_damage * rand() - self.defence)
        if dmg < 1:
            dmg = 1
        self.HP = self.HP - dmg
        TextMain.add_line(Heroes[h].name + " defends: " + str(dmg) + " damage")
        TextMain.corr()
        update_graphics()
        time.sleep(0.8)
    def atack_dist(self, h):
        dmg = self.damage*rand() - Heroes[h].dist_defence
        if dmg < 0:
            dmg = 1
        Heroes[h].HP = Heroes[h].HP - dmg
        TextMain.add_line(self.title + " shoots: " + str(dmg) + " damage")
        TextMain.corr()
        update_graphics()
        time.sleep(0.8)

class Thing:
    def __init__(self, title, type, min_lvl, max_lvl, cost, manacost, comb_defence_effect, dist_defence_effect, comb_damage_effect, dist_damage_effect, HP_effect, mana_effect, luck_effect, imagename, special_effect, passive_effect, image_scale_x, image_scale_y, description):
        self.title = title
        self.type = type
        self.min_lvl = min_lvl
        self.max_lvl = max_lvl
        self.cost = cost
        self.manacost = manacost
        self.comb_defence_effect = comb_defence_effect
        self.dist_defence_effect = dist_defence_effect
        self.comb_damage_effect = comb_damage_effect
        self.dist_damage_effect = dist_damage_effect
        self.HP_effect = HP_effect
        self.mana_effect = mana_effect
        self.luck_effect = luck_effect
        self.special_effect = special_effect
        self.passive_effect = passive_effect
        self.imagename = imagename
        self.image = pygame.image.load(imagename)
        self.image_scale_x = image_scale_x
        self.image_scale_y = image_scale_y
        self.image = pygame.transform.scale(self.image, (image_scale_x, image_scale_y))
        self.description = description
    def draw(self, x, y):
        rect = self.image.get_rect(center=(x, y))
        screen.blit(self.image, rect)
    def info(self):
        TextMain.add_line(self.title + "   lvl: " + str(self.min_lvl) + "-" + str(self.max_lvl) + " cost = " + str(self.cost))
        TextMain.add_line("      damage: +" + str(self.comb_damage_effect) + " defense = +" + str(self.comb_damage_effect) + " mana = +" + str(self.mana_effect) + " luck = +" + str(self.luck_effect))
        TextMain.add_line("      special_effect" + self.special_effect + " manacost = " + str(self.manacost) + " " + self.passive_effect)
        TextMain.add_line(self.description)

class Location:
    def __init__(self, title, imagename, special_effect, description):
        self.title = title
        self.move_idx = ObjList()
        self.trade_idx = ObjList()
        self.guard_idx = ObjList()
        self.actions = ObjList()
        self.imagename = imagename
        self.special_effect = special_effect
        self.image_scale_x = int(WIDTH*0.5)
        self.image_scale_y = int((HEIGHT - 60)*0.42)
        self.image = pygame.image.load(imagename)
        self.image = pygame.transform.scale(self.image, (self.image_scale_x, self.image_scale_y))
        self.description = description
    def draw(self, x, y):
        rect = self.image.get_rect(center=(x, y))
        screen.blit(self.image, rect)


class Missions:
    def __init__(self):
        self.titles = []
        self.locs = []
        self.texts = []
    def show(self, loc):
        for q in range(len(self.locs)):
            if self.locs[q] == loc:
                break
        if q < len(self.locs):
            TextMain.add_line(self.titles[q])
            TextMain.add_line(self.texts[q])
            TextMain.add_line("----0 Ok!")
            TextMain_out()
            choose(10)
    def check(self, loc):
        for q in range(len(self.locs)):
            if self.locs[q] == loc:
                break

        check = 1
        ''''check and award'''

        ''''check and award'''

        if check == 1:
            TextMain.add_line("Mission " + self.titles[q] + " is completed")
            TextMain_out()
#=====================================================================================================================#




#initialization=======================================================================================================#
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Legends Of The North Way")
clock = pygame.time.Clock()
keyinp = 0
#pygame.mixer.pre_init(44100, -16, 2, 2048)
#pygame.mixer.init()
#pygame.mixer.music.load("/home/dalimov/PycharmProjects/pygame/test_music.mp3")
#pygame.mixer.music.play()

back = pygame.image.load('back.jpg')
back = pygame.transform.scale(back, (WIDTH, int(HEIGHT * 1.25)))
rect = back.get_rect(center=(WIDTH / 2, HEIGHT / 2))

tempo = 0
Enemy = 0
Enemies = ObjList()
Creatures = ObjList()
Locations = ObjList()
Things = ObjList()
Missions = Missions()
global h_curr
h_curr = 0
HeroStats = []
Heroes = []
TextMain = Text(line_max=int((HEIGHT/2 - 100)/25 - 1), width=67, size=18, color=CUSTOM_COLOR, x=30, y=HEIGHT/2)
TextLocation = Text(line_max=10, width=50, size=25, color=CUSTOM_COLOR, x=(WIDTH - 200)/2, y=20)
TextStats = Text(line_max=10, width=50, size=17, color=CUSTOM_COLOR, x=WIDTH-225, y=400)
TextInventory = Text(line_max=10, width=50, size=17, color=CUSTOM_COLOR, x=25, y=HEIGHT - 100)
TextEnemies = Text(line_max=10, width=50, size=17, color=RED, x=WIDTH - 225, y=650)
TextHeroesName= []
TextHeroesName.append(Text(line_max=10, width=50,size=15, color=CUSTOM_COLOR, x=WIDTH-225, y=115))
TextHeroesName.append(Text(line_max=10, width=50,size=15, color=CUSTOM_COLOR, x=WIDTH-225, y=225))
TextHeroesName.append(Text(line_max=10, width=50,size=15, color=CUSTOM_COLOR, x=WIDTH-225, y=335))
#=====================================================================================================================#




#loading==============================================================================================================#
file = open('creatures.txt', 'r')
q = 0
for line in file:
    if (q > 0) and (len(line) > 1):
        inp = line.split()
        if q % 3 == 1:
            inp_creature = Creature(title=inp[0], type=inp[1], HP=int(inp[2]), defence=int(inp[3]), damage=int(inp[4]), min_lvl=int(inp[5]), special_effect=inp[6], final_effect=inp[7],
                            imagename=inp[8], image_scale_x=int(inp[9]), image_scale_y=int(inp[10]),  description='')
        if q % 3 == 2:
            inp_creature.description = line
            Creatures.add(inp_creature)
    q = q + 1

file = open('things.txt', 'r')
q = 0
for line in file:
    if (q > 0) and (len(line) > 1):
        inp = line.split()
        if q % 3 == 1:
            inp_thing = Thing(title=inp[0], type=inp[1], min_lvl=int(inp[2]), max_lvl=int(inp[3]), cost=int(inp[4]), manacost=int(inp[5]), comb_defence_effect=int(inp[6]), dist_defence_effect=int(inp[7]), comb_damage_effect=int(inp[8]), dist_damage_effect=int(inp[9]), HP_effect=int(inp[10]), mana_effect=int(inp[11]), luck_effect=int(inp[12]), imagename=inp[13], special_effect=inp[14], passive_effect=inp[15], image_scale_x=int(inp[16]), image_scale_y=int(inp[17]),  description='')
        if q % 3 == 2:
            inp_thing.description = line
            Things.add(inp_thing)
    q = q + 1

file = open('locations.txt', 'r')
q = 0
for line in file:
    if (q > 0) and (len(line) > 1):
        inp = line.split()
        if q % 7 == 1:
            inp_location = Location(title=inp[0], special_effect=inp[1], imagename=inp[2], description='')
        if q % 7 == 2:
            for w in range(len(inp)):
                inp_location.actions.add(inp[w])
        if q % 7 == 3:
            for w in range(len(inp)):
                inp_location.move_idx.add(inp[w])
        if q % 7 == 4:
            for w in range(len(inp)):
                inp_location.trade_idx.add(inp[w])
        if q % 7 == 5:
            for w in range(len(inp)):
                inp_location.guard_idx.add(inp[w])
        if q % 7 == 6:
            inp_location.description = line
            Locations.add(inp_location)
    q = q + 1

file = open('missions.txt', 'r')
q = 0
for line in file:
    if (q > 0) and (len(line) > 1):
        if q % 4 == 1:
            Missions.titles.append(line)
        if q % 4 == 2:
            Missions.locs.append(line)
        if q % 4 == 3:
            Missions.texts.append(line)
    q = q + 1

file = open('heroes.txt', 'r')
q = 0
for line in file:
    if (q > 0) and (len(line) > 1):
        inp = line.split()
        if q % 2 == 1:
            HeroStats.append(Hero(name=inp[0], imagename=inp[1], loc=inp[2]))
    q = q + 1
for q in range(3):
    Heroes.append(HeroStats[q])
#=====================================================================================================================#


def hcrand(fight_location):
    cnt = 0
    ch_arr = np.zeros(3)
    for q in range(3):
        if (Heroes[q].loc == fight_location) and (Heroes[q].HP > 0):
            ch_arr[cnt] = q
            cnt = cnt + 1
    if cnt >= 1:
        i = random.randint(0, cnt-1)
        return int(ch_arr[i])
    else:
        return 0

def h_coex_num():
    cnt = 0
    for q in range(3):
        if (Heroes[h_curr].coex[q] == 1) and (Heroes[q].HP > 0):
            cnt = cnt + 1
    return cnt

def update_Text():
    TextStats.clear()
    TextStats.add_line(Heroes[h_curr].name)
    TextStats.add_line(" HP:       " + str(Heroes[h_curr].HP) + "/" + str(Heroes[h_curr].HP_max))
    TextStats.add_line(" Mana:    " + str(Heroes[h_curr].mana) + "/" + str(Heroes[h_curr].mana_max))
    TextStats.add_line(" Damage: " + str(Heroes[h_curr].comb_damage) + " (dist " + str(Heroes[h_curr].comb_damage) + ")")
    TextStats.add_line(" Defence: " + str(Heroes[h_curr].comb_defence) + " (dist " + str(Heroes[h_curr].dist_defence) + ")")
    TextStats.add_line(" Money:   " + str(Heroes[h_curr].money))
    TextStats.add_line(" Luck:      " + str(Heroes[h_curr].luck))

    TextEnemies.clear()
    if Enemies.len() > 0:
        TextEnemies.add_line('You are fighting with:')
    for q in range(Enemies.len()):
        Enemies.arr[q].info_ent()

    TextInventory.clear()

    for q in range(Heroes[h_curr].inventory.len()):
        TextInventory.add_line(Heroes[h_curr].inventory.arr[q])

    TextLocation.clear()
    TextLocation.add_line(Heroes[h_curr].loc)

    for q in range(3):
        TextHeroesName[q].clear()
        TextHeroesName[q].add_line(Heroes[q].name + " " + Heroes[q].loc)


def readkey():
    inp = -10
    while inp == -10:
        for i in pygame.event.get():
            if i.type == pygame.QUIT:
                exit()
        keys = pygame.key.get_pressed()
        for q in range(len(keys)):
            if keys[q] > 0:
                inp = q
    if (inp > 47) and (inp < 58):
        return (inp - 48)
    if inp == 113:
        return -3
    if inp == 97:
        return -1
    return -10

def choose(max):
    TextMain.corr()
    update_graphics()
    if max > 0:
        keyinp = -10
        while (keyinp < 0) or (keyinp >= max):
            keyinp = readkey()
            time.sleep(0.28)
            if keyinp < 0:
                TextMain.line_start = TextMain.line_start + keyinp + 2
                if TextMain.line_start < 0:
                    TextMain.line_start = 0
                update_graphics()
            if (keyinp >= 0) and (keyinp < max):
                return keyinp
    else:
        return -1

def update_graphics():
    update_Text()

    screen.blit(back, rect)
    TextMain.out()
    TextInventory.out_hor()
    TextLocation.out()
    TextStats.out()
    TextEnemies.out()
    TextHeroesName[0].out()
    TextHeroesName[1].out()
    TextHeroesName[2].out()

    curr_loc = Locations.getLocation(Heroes[h_curr].loc)
    curr_loc.draw((WIDTH-200)/2, (HEIGHT)/4 + 10)
    for q in range(Heroes[h_curr].inventory.len()):
        Things.getThing(Heroes[h_curr].inventory.arr[q]).draw(WIDTH/5*q + 65, HEIGHT - 42)
    for q in range(3):
        if q == h_curr:
            Heroes[q].image = pygame.image.load(Heroes[q].imagename)
            Heroes[q].image = pygame.transform.scale(Heroes[q].image, (100, 70))
            Heroes[q].draw(WIDTH - 180, 60 + 110*q)
            Heroes[q].image = pygame.image.load(Heroes[q].imagename)
            Heroes[q].image = pygame.transform.scale(Heroes[q].image, (70, 70))
        else:
            Heroes[q].draw(WIDTH - 180, 60 + 110*q)


    #Enemy.draw(300, 200)
    pygame.display.update()


def TextMain_out():
    TextMain.corr()
    update_graphics()
    time.sleep(1)

def action(action_title, inp):
    if action_title=="move":
        move()
    if action_title=="fight":
        fight(inp)
    if action_title=="use_invent":
        Heroes[h_curr].use_invent()
    if action_title == "treat":
        treat()
    if action_title == "trade":
        trade()
    if action_title == "send_invent":
        send_invent()
    if action_title == "show_mission":
        Missions.show(Heroes[h_curr].loc)
    if action_title == "check_mission":
        Missions.check(Heroes[h_curr].loc)

def send_invent():
    if h_coex_num() > 1:
        TextMain.add_line("What?")
        ch = Heroes[h_curr].choose_invent()
        if ch > -1:
            inp = Heroes[h_curr].inventory.arr[ch]
            TextMain.add_line("Whoom?")
            ch = choose_another_coex_hero()
            if ch > -1:
                Heroes[h_curr].send_invent(inp=inp, to_whoom=ch)
    else:
        TextMain.add_line("no Heroes to send")
        update_graphics()

def choose_another_coex_hero():
    ch_arr = np.zeros(3)
    cnt = 0
    for q in range(3):
        if (Heroes[q].HP > 0) and (Heroes[h_curr].coex[q] == 1) and (q != h_curr):
            TextMain.add_line("    " + str(cnt) + " " + Heroes[q].name)
            ch_arr[cnt] = q
            cnt = cnt + 1
    ch = choose(cnt)
    return int(ch_arr[ch])

def treat():
    Heroes[h_curr].HP = Heroes[h_curr].HP + 50

def fight(inp, h_curr):
    TextMain.clear()
    rw = h_curr
    fight_location = Locations.getLocation(Heroes[h_curr].loc).title
    if str(type(inp)) == "<class '__main__.ObjList'>":
        for q in range(inp.len()):
            Enemies.add(Creatures.getCreature(inp.arr[q]))
    if str(type(inp)) == "<class 'list'>":
        for q in range(len(inp)):
            Enemies.add(Creatures.getCreature(inp[q]))
    if str(type(inp)) == "<class 'str'>":
        Enemies.add(Creatures.getCreature(inp))

    coex_update("curr")
    TextMain.add_line("The Battle Begun!")
    update_graphics()

    h_fight_num = 1
    cnt = 0
    while (Enemies.len() > 0) and (h_fight_num > 0):
        h_fight_num = 0
        for q in range(3):
            if Heroes[q].loc == fight_location:
                h_fight_num = h_fight_num + 1
        if h_fight_num == 0:
            break
        check = 0
        for q in range(Enemies.len()):
            if Enemies.arr[q].HP > 0:
                check = 1
        if check == 0:
            break

        cnt = cnt + 1
        TextMain.clear()
        TextMain.add_line('----TURN-' + str(cnt) + '------------------------------------------------------')
        TextMain_out()

        for q in range(Enemies.len()):
            if q < Enemies.len():
                if (Enemies.arr[q].type != "dist"):
                    Enemies.arr[q].atack_comb(hcrand(fight_location))
                else:
                    Enemies.arr[q].atack_dist(hcrand(fight_location))
                if (Enemies.arr[q].special_effect != "none"):
                    TextMain.add_line(Enemies.arr[q].title + " uses " + Enemies.arr[q].special_effect)
                    action(Enemies.arr[q].special_effect)
                    TextMain_out()

        for e in range(3):
            if Heroes[e].loc == fight_location:
                h_curr = e

                check = 0
                for q in range(Enemies.len()):
                    if Enemies.arr[q].HP > 0:
                        check = 1
                if check == 0:
                    break

                TextMain.add_line("")
                TextMain.add_line(Heroes[h_curr].name + ' chooses action:')
                TextMain.add_line('0 atack')
                TextMain.add_line('1 use_inventory')
                TextMain.add_line('2 escape')
                update_graphics()
                ch = choose(3)
                if (ch == 0) and (Enemies.len() > 1):
                    TextMain.add_line(Heroes[h_curr].name + ' chooses the aim:')
                    for q in range(Enemies.len()):
                        TextMain.add_line(str(q) + " " + Enemies.arr[q].title)
                    update_graphics()
                    Enemy = choose(Enemies.len())
                else:
                    Enemy = 0

                if ch == 0:
                    Heroes[h_curr].atack()
                if ch == 1:
                    Heroes[h_curr].use_invent()
                if ch == 2:
                    action("move", "")
                    TextMain.clear()
                update_graphics()

                for q in range(Enemies.len()):
                    if q < Enemies.len():
                        if Enemies.arr[q].HP < 1:
                            TextMain.add_line(Enemies.arr[q].title + " dies " + Enemies.arr[q].final_effect)
                            action(Enemies.arr[q].final_effect, "")
                            for scn in range(Locations.len()):
                                if Locations.arr[scn].title == fight_location:
                                    Locations.arr[scn].guard_idx.delete(Enemies.arr[q].title)
                            del Enemies.arr[q]
                            TextMain_out()
                            TextMain_out()
                if Enemies.len() == 0:
                    break

    Enemies.clear()
    h_curr = rw

def move():
    TextMain.clear()
    TextMain.add_line("Where")
    curr_loc = Locations.getLocation(Heroes[h_curr].loc)
    for q in range(curr_loc.move_idx.len()):
        TextMain.add_line("----" + str(q) + " " + curr_loc.move_idx.arr[q])
        TextMain.add_line("      " + curr_loc.description)
        str_out = "      Guard: "
        for w in range(Locations.getLocation(curr_loc.move_idx.arr[q]).guard_idx.len()):
            str_out = str_out + Locations.getLocation(curr_loc.move_idx.arr[q]).guard_idx.arr[w] + "; "
        TextMain.add_line(str_out)
    TextMain_out()
    ch = choose(curr_loc.move_idx.len())
    Heroes[h_curr].loc = curr_loc.move_idx.arr[ch]

def trade():
    curr_loc = Locations.getLocation(Heroes[h_curr].loc)
    TextMain.add_line("----0 back")
    for q in range(curr_loc.trade_idx.len()):
        TextMain.add_line("----" + str(q + 1))
        Things.getThing(curr_loc.trade_idx.arr[q]).info()
    ch = choose(curr_loc.trade_idx.len() + 1)
    if ch > 0:
        Heroes[h_curr].add_invent(curr_loc.trade_idx.arr[ch - 1])

def actions():
    for q in range(Heroes[h_curr].inventory.len()):
        action(Things.getThing(Heroes[h_curr].inventory.arr[q]).passive_effect, '')

    curr_location = Locations.getLocation(Heroes[h_curr].loc)
    Heroes[h_curr].actions = curr_location.actions
    TextMain.clear()
    TextMain.add_line(Locations.getLocation(Heroes[h_curr].loc).title + ": " + Locations.getLocation(Heroes[h_curr].loc).description)
    update_graphics()

    Heroes[h_curr].actions.out()
    cnt = 0
    ch_arr = np.zeros(3)
    for q in range(3):
        if (Heroes[h_curr].coex_start[q] == 1) and (Heroes[h_curr].coex[q] == 0) and (Heroes[q].HP > 0):
            TextMain.add_line(str(Heroes[h_curr].actions.len() + cnt) + ' Follow ' + Heroes[q].name)
            ch_arr[cnt] = q
            cnt = cnt + 1
    ch = choose(Heroes[h_curr].actions.len() + cnt)
    if ch < Heroes[h_curr].actions.len():
        action(Heroes[h_curr].actions.arr[ch], "")
    else:
        Heroes[h_curr].loc = Heroes[int(ch_arr[ch - Heroes[h_curr].actions.len()])].loc

def rand():
    return (2/3 + 2/3*random.random())

def coex_update(inp):
    for q in range(3):
        for w in range(3):
            if inp == "start":
                Heroes[q].coex_start[w] = 0
            else:
                Heroes[q].coex[w] = 0
    for q in range(3):
        for w in range(3):
            if (Heroes[q].HP > 0) and (Heroes[w].HP > 0) and (Heroes[q].loc == Heroes[w].loc):
                if inp == "start":
                    Heroes[q].coex_start[w] = 1
                else:
                    Heroes[q].coex[w] = 1

coex_update("curr")
Heroes[0].add_invent("treater")
Heroes[0].send_invent("treater", 1)

def trade_rand(n):
    if Heroes[h_curr].money > 50:
        Heroes[h_curr].money = Heroes[h_curr].money - 50
        arr = get_acc_lvl("thing", n)
        for q in range(len(arr)):
            Locations.arr[Locations.get_ind(Heroes[h_curr].loc)].trade_idx.arr.append(arr[q])

def fight_rand(n):
    if Heroes[h_curr].money > 50:
        Heroes[h_curr].money = Heroes[h_curr].money - 50
        arr = get_acc_lvl("creature", n)
        for q in range(len(arr)):
            Locations.arr[Locations.get_ind(Heroes[h_curr].loc)].guard_idx.arr.append(arr[q])

def get_acc_lvl(inp, n):
    arr = []
    arr_out = []
    if inp == "thing":
        min = Heroes[h_curr].level - 2
        max = int(Heroes[h_curr].level*1.8) + 2
        for q in range(Things.len()):
            if (Things.arr[q].max_lvl > min) and (Things.arr[q].min_lvl < max):
                arr.append(Things.arr[q].title)
    if inp == "creature":
        min = int(Heroes[h_curr].level/2) - 2
        max = Heroes[h_curr].level + 2
        for q in range(Creatures.len()):
            if (Creatures.arr[q].min_lvl > min) and (Creatures.arr[q].min_lvl < max):
                arr.append(Creatures.arr[q].title)
    if len(arr) == 0:
        return []
    for q in range(n):
        arr_out.append(arr[random.randint(0, len(arr) - 1)])
    return arr_out

def lvl_up_chack():
    for q in range(3):
        for w in range(80):
            if (Heroes[q].level == w) and (Heroes[q].EXP >= int(5 * w * pow(w, 0.5))):
                Heroes[q].lvl_up()

def award(n):
    for e in range(n):
        TextMain.clear()
        rb = int(100*rand())
        rb2 = int(5 * rand())
        cnt = 0
        things_loc = get_acc_lvl(inp="thing", n=10)
        things_out = []
        for q in range(len(things_loc)):
            check = 0
            for w in range(q):
                if (len(things_out) > 0) and (w < len(things_out)):
                    if things_out[w] == things_loc[q]:
                        check = 1
            if check == 0:
                things_out.append(things_loc[q])
        cnt = 0
        TextMain.add_line("----0 +" + str(rb) + " money")
        TextMain.add_line("----1 +" + str(rb2) + " EXP")
        for q in range(3):
            if q < len(things_out):
                cnt = cnt + 1
                TextMain.add_line("----" + str(q+2) + " Get " + things_out[q])
        ch = choose(2 + cnt)
        if ch == 0:
            Heroes[h_curr].money = Heroes[h_curr].money + rb
        if ch == 1:
            Heroes[h_curr].EXP = Heroes[h_curr].EXP + rb2
        if ch > 1:
            Heroes[h_curr].money =  Heroes[h_curr].money + Things.getThing(things_out[ch - 2]).cost
            check = Heroes[h_curr].add_invent(things_out[ch - 2])
            if check == -1:
                Heroes[h_curr].money = Heroes[h_curr].money - Things.getThing(things_out[ch - 2]).cost + rb
        TextMain_out()

Heroes[1].modify_invent('treater', 'red')

#running==============================================================================================================#
running = True
while running:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            inp = event.key
            if (inp > 47) and (inp < 58):
                keyinp = inp - 48
            if inp > 1073741000:
                keyinp = inp - 1073741912
            if inp == 1073741906:
                keyinp = -1
            if inp == 1073741905:
                keyinp = -3

    lvl_up_chack()
    for q in range(3):
        if Heroes[q].luck > 30:
            Heroes[q].luck = Heroes[q].luck - 5
        if Heroes[q].luck < 30:
            Heroes[q].luck = Heroes[q].luck + 5
        if Heroes[q].mana < Heroes[q].mana_max:
            Heroes[q].mana = Heroes[q].mana + 1

    for q in range(Locations.len()):
        action(Locations.arr[q].special_effect, '')
    h_curr = 0
    coex_update("start")
    for q in range(3):
        coex_update("curr")
        if Heroes[h_curr].HP > 0:
            actions()
            update_graphics()
            h_curr = h_curr + 1
    for q in range(3):
        if Locations.getLocation(Heroes[q].loc).guard_idx.len() > 0:
            h_curr = q
            #fight(Locations.getLocation(Heroes[q].loc).guard_idx, h_curr)


pygame.quit()
