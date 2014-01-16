"""
vo.util.info

This module stores constant data that maps to resources in Vendetta Online,
such as system names.
"""


def short_system_name(long_name):
    """Generates a short system name from a long system name.
    """
    parts = long_name.split(' ')
    return parts[0].lower()


def sector_py2vo(x, y):
    """Converts an integral point sector to vendetta (inverse y) scheme.
    """
    return (x + 1, 16 - y)


def sector_vo2py(x, y):
    """Converts sector from Vendetta scheme (inverse y) to integral points.
    """
    return (x - 1, 16 - y)


def sector_py2vochar(x, y):
    """Converts an integral point sector to Vendetta scheme (letter + inverse y).
    """
    (x, y) = sector_py2vo(x, y)
    return (chr(x + ord('A') - 1), y)


def sector_vochar2py(x, y):
    """Converts sector from Vendetta scheme (letter + inverse y) to integral points.
    """
    return sector_vo2py(ord(x.upper()) - ord('A') + 1, y)


"""
System names, in order by the system id. System ids are zero-based, so the
index in this list maps to the system id.
"""
SYSTEM_NAMES = (
    None,  # placeholder, since array is 1-based (really vo devs?)
    'Sol II',
    'Betheshee',
    'Geira Rutilus',
    'Deneb',
    'Eo',
    'Cantus',
    'Metana',
    'Setalli Shinas',
    'Itan',
    'Pherona',
    'Artana Aquilus',
    'Divinia',
    'Jallik',
    'Edras',
    'Verasi',
    'Pelatus',
    'Bractus',
    'Nyrius',
    'Dau',
    'Sedina',
    'Azek',
    'Odia',
    'Latos',
    'Arta Caelestis',
    'Ukari',
    'Helios',
    'Initros',
    'Pyronis',
    'Rhamus',
    'Dantia',
)

"""
Dictionary of system name => system id. Just like in the SystemNames table
defined in Vendetta (in Lua), keys to this dictionary are all lower case, and
only use the first word of the system name.
"""
SYSTEM_ID = dict()
MAX_SYSTEM_ID = 1
for system_name in SYSTEM_NAMES:
    if system_name is not None:
        SYSTEM_ID[short_system_name(system_name)] = MAX_SYSTEM_ID
    MAX_SYSTEM_ID += 1

"""
A graph of system jumps defined using a dictionary. All systems in the graph
are represented as lower-case, using only the first word in the name (arta for
Arta Caelestis, etc.) Keys are system names and point to a set of systems
reachable from the key system. For example:

JUMPS['dau'] = set('arta', 'azek', 'nyrius')
"""
JUMPS = dict()

# UIT space
JUMPS['arta'     ] = set(('dau', 'ukari'))
JUMPS['azek'     ] = set(('dau', 'latos'))
JUMPS['dau'      ] = set(('arta', 'azek', 'nyrius'))
JUMPS['nyrius'   ] = set(('dau', 'verasi'))
JUMPS['verasi'   ] = set(('nyrius', 'edras'))

# Grey space
JUMPS['bractus'  ] = set(('odia', 'pelatus'))
JUMPS['edras'    ] = set(('pelatus', 'verasi', 'jallik'))
JUMPS['helios'   ] = set(('pyronis', 'ukari'))
JUMPS['latos'    ] = set(('azek', 'ukari', 'sedina'))
JUMPS['odia'     ] = set(('sedina', 'bractus'))
JUMPS['pelatus'  ] = set(('bractus', 'edras'))
JUMPS['sedina'   ] = set(('latos', 'odia'))
JUMPS['ukari'    ] = set(('helios', 'initros', 'latos', 'arta'))

# Serco space
JUMPS['geira'    ] = set(('deneb', 'betheshee'))
JUMPS['betheshee'] = set(('geira', 'sol'))
JUMPS['sol'      ] = set(('betheshee', 'dantia'))
JUMPS['dantia'   ] = set(('sol', 'pyronis', 'rhamus'))
JUMPS['pyronis'  ] = set(('dantia', 'initros', 'helios'))
JUMPS['rhamus'   ] = set(('dantia', 'initros'))
JUMPS['initros'  ] = set(('rhamus', 'pyronis', 'ukari'))

# Itani space
JUMPS['deneb'    ] = set(('geira', 'eo'))
JUMPS['eo'       ] = set(('deneb', 'cantus'))
JUMPS['cantus'   ] = set(('eo', 'metana'))
JUMPS['metana'   ] = set(('cantus', 'setalli'))
JUMPS['setalli'  ] = set(('metana', 'itan'))
JUMPS['itan'     ] = set(('setalli', 'pherona'))
JUMPS['pherona'  ] = set(('itan', 'artana'))
JUMPS['artana'   ] = set(('pherona', 'divinia'))
JUMPS['divinia'  ] = set(('artana', 'jallik'))
JUMPS['jallik'   ] = set(('divinia', 'edras'))

"""
Dictionary storing the location of jump points between systems.
For example:
    (x, y) = WORMHOLE['ukari']['arta']
"""
WORMHOLE = dict()
for system in SYSTEM_ID.keys():
    WORMHOLE[system] = dict()

# UIT space
WORMHOLE['arta'  ]['ukari' ] = sector_vochar2py('B', 7)
WORMHOLE['arta'  ]['dau'   ] = sector_vochar2py('O', 12)
WORMHOLE['dau'   ]['arta'  ] = sector_vochar2py('B', 9)
WORMHOLE['dau'   ]['azek'  ] = sector_vochar2py('E', 15)
WORMHOLE['dau'   ]['nyrius'] = sector_vochar2py('O', 6)
WORMHOLE['azek'  ]['dau'   ] = sector_vochar2py('J', 1)
WORMHOLE['azek'  ]['latos' ] = sector_vochar2py('I', 16)
WORMHOLE['nyrius']['dau'   ] = sector_vochar2py('B', 10)
WORMHOLE['nyrius']['verasi'] = sector_vochar2py('O', 15)
WORMHOLE['verasi']['nyrius'] = sector_vochar2py('C', 2)
WORMHOLE['verasi']['edras' ] = sector_vochar2py('O', 7)

# Grey space
WORMHOLE['helios' ]['pyronis'] = sector_vochar2py('B', 7)
WORMHOLE['helios' ]['ukari'  ] = sector_vochar2py('O', 12)
WORMHOLE['ukari'  ]['helios' ] = sector_vochar2py('B', 5)
WORMHOLE['ukari'  ]['initros'] = sector_vochar2py('A', 10)
WORMHOLE['ukari'  ]['arta'   ] = sector_vochar2py('L', 2)
WORMHOLE['ukari'  ]['latos'  ] = sector_vochar2py('O', 13)
WORMHOLE['latos'  ]['ukari'  ] = sector_vochar2py('B', 6)
WORMHOLE['latos'  ]['azek'   ] = sector_vochar2py('H', 2)
WORMHOLE['latos'  ]['sedina' ] = sector_vochar2py('O', 12)
WORMHOLE['sedina' ]['latos'  ] = sector_vochar2py('B', 8)
WORMHOLE['sedina' ]['odia'   ] = sector_vochar2py('O', 6)
WORMHOLE['odia'   ]['sedina' ] = sector_vochar2py('B', 13)
WORMHOLE['odia'   ]['bractus'] = sector_vochar2py('O', 7)
WORMHOLE['bractus']['odia'   ] = sector_vochar2py('B', 14)
WORMHOLE['bractus']['pelatus'] = sector_vochar2py('E', 2)
WORMHOLE['pelatus']['bractus'] = sector_vochar2py('K', 15)
WORMHOLE['pelatus']['edras'  ] = sector_vochar2py('G', 2)
WORMHOLE['edras'  ]['pelatus'] = sector_vochar2py('H', 15)
WORMHOLE['edras'  ]['verasi' ] = sector_vochar2py('B', 11)
WORMHOLE['edras'  ]['jallik' ] = sector_vochar2py('I', 2)

# Serco space
WORMHOLE['geira'    ]['deneb'    ] = sector_vochar2py('O', 4)
WORMHOLE['geira'    ]['betheshee'] = sector_vochar2py('L', 15)
WORMHOLE['betheshee']['geira'    ] = sector_vochar2py('D', 2)
WORMHOLE['betheshee']['sol'      ] = sector_vochar2py('O', 6)
WORMHOLE['sol'      ]['betheshee'] = sector_vochar2py('B', 15)
WORMHOLE['sol'      ]['dantia'   ] = sector_vochar2py('O', 14)
WORMHOLE['dantia'   ]['sol'      ] = sector_vochar2py('B', 5)
WORMHOLE['dantia'   ]['pyronis'  ] = sector_vochar2py('O', 2)
WORMHOLE['dantia'   ]['rhamus'   ] = sector_vochar2py('O', 13)
WORMHOLE['rhamus'   ]['dantia'   ] = sector_vochar2py('B', 6)
WORMHOLE['rhamus'   ]['initros'  ] = sector_vochar2py('O', 5)
WORMHOLE['pyronis'  ]['dantia'   ] = sector_vochar2py('B', 11)
WORMHOLE['pyronis'  ]['helios'   ] = sector_vochar2py('O', 9)
WORMHOLE['pyronis'  ]['initros'  ] = sector_vochar2py('K', 15)
WORMHOLE['initros'  ]['rhamus'   ] = sector_vochar2py('B', 14)
WORMHOLE['initros'  ]['pyronis'  ] = sector_vochar2py('D', 2)
WORMHOLE['initros'  ]['ukari'    ] = sector_vochar2py('O', 12)

# Itani space
WORMHOLE['deneb'  ]['geira'  ] = sector_vochar2py('B', 12)
WORMHOLE['deneb'  ]['eo'     ] = sector_vochar2py('O', 3)
WORMHOLE['eo'     ]['deneb'  ] = sector_vochar2py('C', 12)
WORMHOLE['eo'     ]['cantus' ] = sector_vochar2py('P', 11)
WORMHOLE['cantus' ]['eo'     ] = sector_vochar2py('A', 7)
WORMHOLE['cantus' ]['metana' ] = sector_vochar2py('K', 2)
WORMHOLE['metana' ]['cantus' ] = sector_vochar2py('G', 16)
WORMHOLE['metana' ]['setalli'] = sector_vochar2py('P', 6)
WORMHOLE['setalli']['metana' ] = sector_vochar2py('B', 8)
WORMHOLE['setalli']['itan'   ] = sector_vochar2py('O', 13)
WORMHOLE['itan'   ]['setalli'] = sector_vochar2py('B', 6)
WORMHOLE['itan'   ]['pherona'] = sector_vochar2py('P', 6)
WORMHOLE['pherona']['itan'   ] = sector_vochar2py('B', 14)
WORMHOLE['pherona']['artana' ] = sector_vochar2py('P', 7)
WORMHOLE['artana' ]['pherona'] = sector_vochar2py('B', 7)
WORMHOLE['artana' ]['divinia'] = sector_vochar2py('K', 1)
WORMHOLE['divinia']['artana' ] = sector_vochar2py('A', 13)
WORMHOLE['divinia']['jallik' ] = sector_vochar2py('O', 11)
WORMHOLE['jallik' ]['divinia'] = sector_vochar2py('C', 2)
WORMHOLE['jallik' ]['edras'  ] = sector_vochar2py('E', 15)
