def set_user_for_sharding(query_set, owner):
    if query_set._hints == None:
        query_set._hints = {'owner' : owner }
    else:
        query_set._hints['owner'] = owner
    print query_set._hints
