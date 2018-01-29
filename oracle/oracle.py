from pydispatch import dispatcher
from classes.feed import Feed

class Oracle:
  def __init__(self, watchList, holdingList):

    self.watchList = watchList
    self.holdingList = holdingList

    # event registration
    dispatcher.connect(self._handleSimonaFeedUpdate, signal='simona-feed-update', sender='simona')


  def _handleSimonaFeedUpdate(self, feed):
    print("Oracle has received feed from Simon since last update")
    print(feed.ticker)
