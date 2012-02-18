import sys

from gtfs.feed import Feed, FileNotFoundError
from gtfs.schedule import Schedule
from gtfs.entity import *

DEFAULT_CONNECTION_STRING = "sqlite:///:memory:"

def load(feed_filename, connection_string=DEFAULT_CONNECTION_STRING):
    schedule = Schedule(connection_string)
    schedule.create_tables()

    schedule.engine.execute("PRAGMA synchronous=OFF")

    fd = Feed(feed_filename)

    for gtfs_class in (Agency, Route, Stop, Trip, StopTime,
                       ServicePeriod, ServiceException,
                       Fare, FareRule, ShapePoint,
                       Frequency, Transfer):

        print "loading %s" % gtfs_class

        filename = gtfs_class.__tablename__ + ".txt"

        try:
            records = fd.get_reader(filename)

            for (i, record) in enumerate(records):
                if (i % 25000) == 0:
                    sys.stdout.write(".")
                    sys.stdout.flush()
                    schedule.session.commit()

                instance = gtfs_class(**record)
                schedule.session.add(instance)
            print
            schedule.session.commit()
        except (FileNotFoundError):
            optional_files = ['calendar_dates', 'fare_rules',
                              'frequencies', 'transfers']
            if filename in optional_files:
                print "Optional file %s not found. Continuing." % filename
                continue

    return schedule
