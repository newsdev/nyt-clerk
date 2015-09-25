import datetime

def current_term():
    now = datetime.datetime.now()
    return "%s" % (now.year - 1 if now.month < 10 else now.year)

def set_weighted_majvotes(obj):
    def weight_majvotes(obj):
        if ((int(obj.majvotes) + int(obj.minvotes)) < 9):
            """
            We assume missing justices voted with the majority.
            4 minority votes = 0 weighted votes.
            """
            WEIGHTED_VOTES = (9,8,7,6,0)
            return WEIGHTED_VOTES[int(obj.minvotes)]
        return int(obj.majvotes)

    if obj.decisiondirection == "1":
        obj.nyt_weighted_majvotes = weight_majvotes(obj)
    elif obj.decisiondirection == "2":
        obj.nyt_weighted_majvotes = weight_majvotes(obj) * -1
    elif obj.decisiondirection == "3":
        obj.nyt_weighted_majvotes = 0
    return obj