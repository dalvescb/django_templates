from django.db import models

class GamingCompany(models.Model):
    """GamingCompany keeps track of the different companies making consoles

    Attributes
    ----------
    name : (CharField) primary key, the name of the company (i.e Microsoft, Sony, etc)
    """
    name = models.CharField(max_length=30,primary_key=True)

    def __str__(self):
        return self.name

class Console(models.Model):
    """Console keeps track of the different consoles games can be played on

    Attributes
    ----------
    id   : (AutoField) auto incrementing integer primary key
    name : (CharField) the name of the console (i.e Playstation, Xbox etc)
    generation : (PositiveIntegerField) the generation of the console (i.e 0, 1, ...  etc)
    company : (ForeignKey) a relation to the GamingCompany that makes the console
    """
    name = models.CharField(max_length=30)
    generation = models.PositiveIntegerField()
    company = models.ForeignKey(GamingCompany,
                                on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Game(models.Model):
    """Game keeps track of different video games

    Attributes
    ----------
    name : (CharField) primary key, the name of the game (i.e Tetris,Super Mario  etc)
    consoles : (ManyToManyField) a relation to the different consoles the game can be played on
    """
    name = models.CharField(max_length=30,primary_key=True)
    consoles = models.ManyToManyField(Console)

    def __str__(self):
        return self.name

class Player(models.Model):
    """Player keeps track of video game players

    Attributes
    ----------
    name : (CharField) primary key, the name of the player (i.e Jim, John etc)
    games : (ManyToManyField) a relation to the different games players play
    fav_console : (ForeignKey) a relation to the single favourite console of the player
    """
    name = models.CharField(max_length=30,primary_key=True)
    games = models.ManyToManyField(Game)
    fav_console = models.ForeignKey(Console,
                                    on_delete=models.CASCADE)

    def __str__(self):
        return self.name
