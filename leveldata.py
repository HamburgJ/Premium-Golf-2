#Level class that handles all the levels
class level():
    def __init__(self, blocks, par, tileset):
        self.blocks = blocks
        self.width = len(self.blocks[0])*35
        self.par = par
        self.tileset = tileset
        self.num = len(levels)+1
        temprow = 0
        for row in blocks:
            tempcol = 0
            for col in row:
                #Get the position of the ball
                if col == "B":
                    self.startpos = (tempcol*35 + 35/2 -4,(temprow+1)*35-1)
                #Find where the hold is
                elif col == "H":
                    self.x_hole = tempcol*35
                    self.y_hole = (temprow+1)*35
                tempcol += 1
            temprow += 1
        del temprow
        del tempcol

levels = []

#Create all the levels

levels.append(level([
"                         ",
"                         ",
"                         ",
"                         ",
"           n             ",
"           l             ",
"       ^^  l   ^         ",
"     (=========)         ",
"                         ",
"                     ^ H ",
"          n          ====",
"          l  n      =XXXX",
"          l  l   ^==XXXXX",
"       ^ Bl  l  ==XXXXXXX",
"^B ^ ^ =========XXXXXXXXX",
"=======XXXXXXXXXXXXXXXXXX",
"XXXXXXXXXXXXXXXXXXXXXXXXX",], 3, "grass"))
          
levels.append(level([
"                            n                   ",
"                       ^^   l ^                 ",
"                   (====================)       ",
"                                                ",
"                                                ",
"n                                               ",
"l B ^^        n                                 ",
"======= ^ ^   l                                 ",
"XXXXXXX====== l^                                ",
"XXXXXXXXXXXXX===                                ",
"XXXXXXXXXXXXXXXX=^                              ",
"XXXXXXXXXXXXXXXXX==                       ^  H ^",
"XXXXXXXXXXXXXXXXXXX=^^      n            =======",
"XXXXXXXXXXXXXXXXXXXX==      l      ^ ^ ==XXXXXXX",
"XXXXXXXXXXXXXXXXXXXXXX=== ^ l  ^  =====XXXXXXXXX",
"XXXXXXXXXXXXXXXXXXXXXXXXX=========XXXXXXXXXXXXXX",
"XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",], 4, "grass"))

levels.append(level([
"                                                                                                        ",
"                                                                                                        ",
"                                                                                      H     ^           ",
"                                                                                   (============)       ",
"                                                                                                       ^",
"                                                                                                     (==",
"                                                                                                        ",
"                                                                   ^                                    ",
"                                                                ^ == ^                             ^^  ^",
"               ^                                            ^  ===XX== ^                        ^ ======",
"              ==  ^                                         ===XXXXXXX===^^                  ^ ^==XXXXXX",
"             =XX=== ^ ^  n                  n         ^ ====XXXXXXXXXXXXX=== ^         n  ^^====XXXXXXXX",
"        ^^ ==XXXXXX===== l^ ^ ^^ ^          l    ^  ^===XXXXXXXXXXXXXXXXXXXX==^        l ===XXXXXXXXXXXX",
" ^B  ^ ====XXXXXXXXXXXXX===========  ^  ^^ ^l   ^====XXXXXXXXXXXXXXXXXXXXXXXXX===^^^ ^ ==XXXXXXXXXXXXXXX",
"=======XXXXXXXXXXXXXXXXXXXXXXXXXXXX==============XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX======XXXXXXXXXXXXXXXXX",
"XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
"XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"], 9, "grass"))

levels.append(level([
"                                             ",
"                                             ",
"                                             ",
"                           ^  ^^   ^         ",
"                          (========)         ",
"                                             ",
"                                             ",
"                                             ",
"                    ^===  n           ^  H   ",
"                   ==XXX= l           (===)  ",
"                 ^=XXXXXX==                  ",
"                 =XXXXXXXXX== ^              ",
" n          ^^ ==XXXXXXXXXXXX===             ",
" l    ^^ ^  ===XXXXXXXXXXXXXXXXX== ^    n    ",
"^lB  ^======XXXXXXXXXXXXXXXXXXXXXX===  ^l  ^ ",
"======XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX========",
"XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"], 5, "castle"))

levels.append(level([
"                         ",
"                         ",
"                         ",
"  H    ^                 ",
"=========)               ",
"                         ",
"               n         ",
"          ^    l   ^     ",
"      (==================",
"                         ",
"         ^               ",
"=============)         n ",
"              n        l ",
"           ^  l   ^  ^ l ",
"  B ^  ==================",
"=======XXXXXXXXXXXXXXXXXX",
"XXXXXXXXXXXXXXXXXXXXXXXXX",], 6, "castle"))



