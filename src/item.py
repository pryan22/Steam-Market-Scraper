class item:
    def __init__(self, _type:str, skin:str, price:str, quan:str, wear:str, stat:bool, souvenir:bool ):
        self._type = _type
        self.skin = skin
        self.price = price
        self.quan = quan
        self.wear = wear
        self.stat = stat
        self.souvenir = souvenir


#------------------------- Getters and Setters ----------------------
    @property
    def item_type(self):
        return self._type

    @item_type.setter
    def item_type(self, value):
        self._type = value

    @property
    def item_skin(self):
        return self.skin

    @item_skin.setter
    def item_skin(self, value):
        self.skin = value

    @property
    def item_price(self):
        return self.price

    @item_price.setter
    def item_price(self, value):
        self.price = value

    @property
    def item_quantity(self):
        return self.quan

    @item_quantity.setter
    def item_quantity(self, value):
        self.quan = value

    @property
    def item_wear(self):
        return self.wear

    @item_wear.setter
    def item_wear(self, value):
        self.wear = value

    @property
    def is_stat_track(self):
        return self.stat

    @is_stat_track.setter
    def is_stat_track(self, value):
        self.stat = value

    @property
    def is_souvenir(self):
        return self.souvenir

    @is_souvenir.setter
    def is_souvenir(self, value):
        self.souvenir = value