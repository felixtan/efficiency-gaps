def set_year_if_valid(self, year):
    """
    Raises
        TypeError: A non-Int value was passed
    """
    try:
        if isinstance(year, int):
            self.year = year
        else:
            raise TypeError("Year has invalid type {}".format(type(year)))
    except TypeError as error:
        raise error
