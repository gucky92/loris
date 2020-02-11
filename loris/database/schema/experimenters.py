"""schema for experimenters
"""


import datajoint as dj

from loris.database.schema.base import COMMENTS, ManualLookup
from loris.database.attributes import truebool
from loris.database.attributes import lookupname


schema = dj.Schema('experimenters')


@schema
class Experimenter(dj.Manual):
    definition = f"""
    experimenter : varchar(31) # git user-name
    ---
    first_name : varchar(63)
    last_name : varchar(127)
    email : varchar(255)
    phone : varchar(16)
    date_joined : date
    active = 0 : <truebool> # active member of the lab
    """

    class EmergencyContact(dj.Part):
        definition = f"""
        -> Experimenter
        contact_name : varchar(255)
        ---
        relation : varchar(63)
        phone : varchar(16)
        email = null : varchar(255)
        {COMMENTS}
        """


@schema
class ExperimentalProject(ManualLookup, dj.Manual):
    primary_comment = 'name of experimental project'


@schema
class AssignedExperimentalProject(dj.Manual):
    definition = """
    -> Experimenter
    -> ExperimentalProject
    """
