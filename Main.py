import Landscape
import Algorithms


def drive():
    landscape = Landscape.Landscape(area_width=5, mines_count=5)
    sweeper = Algorithms.Sweeper()
    sweeper.load(landscape)
    sweeper.run()


drive()
