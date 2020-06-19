class SingleEntry:
  def __init__(self):
    self.rank = ""
    self.title = ""
    self.num_words = -1
    self.points = -1
    self.comments = -1
   
  def __str__(self):
    return {'rank': self.rank, 'title': self.title, 'num_words': self.num_words, 'points': self.points, 'comments': self.comments}

  def __repr__(self):
    return self.rank +"\t"+ self.title +"\t"+ str(self.num_words) +"\t" + str(self.points) +"\t"+ str(self.comments) +"\n"