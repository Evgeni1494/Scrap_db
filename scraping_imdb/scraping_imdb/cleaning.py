import re 


def cleaning_titre_original(titre_original):
    if titre_original :
        titre_original = titre_original.split(":")[-1].strip()
    return titre_original


def cleaning_duree(duree):
    if duree :
        duree = duree.strip()
        match = re.match(r'^(\d+)h\s*(?:(\d+)m)?$', duree)
        if match:
            heures, minutes = match.groups()
            heures = int(heures)
            minutes = int(minutes) if minutes is not None else 0
            if heures >= 0 and minutes >= 0:
                duree = heures * 60 + minutes
            elif heures >= 0:
                duree = heures * 60
        else:
            duree = None
    return duree
        

def cleaning_cout(cout):
    if cout : 
        cost_string = cout[0]
        cost_string = re.sub(r'[^\d\.\-\s]', '', cost_string)
        cost_number = int(cost_string)
        cout = cost_number
    return cout 

