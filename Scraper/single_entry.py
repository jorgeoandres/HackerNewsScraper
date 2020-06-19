class SingleEntry:
  """
    SingleEntry encapsulates rank, title, number of words, points and comments of news entries.
  """
  def __init__(self):
    """
        Construct a new 'SigleEntry' object.

        :param rank: Number rank of entry
        :param title: Title of entry
        :param num_words: Number of words in the title of entry
        :param points: Number of points of entry
        :param comments: Number of comments of entry
        :return: returns nothing
    """
    self.rank = ""
    self.title = ""
    self.num_words = -1
    self.points = -1
    self.comments = -1
   
  def __str__(self):
    """
    Override of __str__ function provides dict representation of the Object.
    """
    return {'rank': self.rank, 'title': self.title, 'num_words': self.num_words, 'points': self.points, 'comments': self.comments}

  def __repr__(self):
    """
    Override of __repr__ represents the object as string.
    """
    return self.rank +"\t"+ self.title +"\t"+ str(self.num_words) +"\t" + str(self.points) +"\t"+ str(self.comments) +"\n"